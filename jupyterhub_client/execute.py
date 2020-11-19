import uuid
import difflib
import logging
import textwrap

from jupyterhub_client.api import JupyterHubAPI, JupyterKernelAPI
from jupyterhub_client.utils import parse_notebook_cells

logger = logging.getLogger(__name__)


async def execute_code(hub_url, cells, username=None, create_user=False, delete_user=False, username_format='user-{id}', timeout=None):
    username = username or username_format.format(id=str(uuid.uuid4()))
    hub = JupyterHubAPI(hub_url)

    async with hub:
        try:
            if (await hub.get_user(username)) is None:
                if create_user:
                    await hub.create_user(username)
                else:
                    raise ValueError(f'current username={username} does not exist and create_user={create_user}')
            jupyter = await hub.create_server(username)
            async with jupyter:
                kernel_id = (await jupyter.create_kernel())['id']
                async with JupyterKernelAPI(jupyter.api_url / 'kernels' / kernel_id, jupyter.api_token) as kernel:
                    for i, (code, expected_result) in enumerate(cells):
                        kernel_result = await kernel.send_code(username, code, timeout=timeout)
                        logger.debug(f'kernel execucting cell={i} code=\n{textwrap.indent(code, "   >>> ")}')
                        logger.debug(f'kernel result cell={i} result=\n{textwrap.indent(kernel_result, "   | ")}')
                        if kernel_result != expected_result:
                            diff = ''.join(difflib.unified_diff(kernel_result, expected_result))
                            logger.error(f'kernel result did not match expected result diff={diff}')
                            raise ValueError(f'execution of cell={i} did not match expected result diff={diff}')
                await jupyter.delete_kernel(kernel_id)
            await hub.delete_server(username)
        finally:
            if delete_user:
                await hub.delete_user(username)


async def execute_notebook(hub_url, notebook_path, **kwargs):
    cells = parse_notebook_cells(notebook_path)
    await execute_code(hub_url, cells, **kwargs)
