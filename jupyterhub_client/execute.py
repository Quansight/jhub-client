import uuid
import difflib
import logging
import textwrap
import datetime

from jupyterhub_client.api import JupyterHubAPI, JupyterKernelAPI, JupyterAPI
from jupyterhub_client.utils import parse_notebook_cells, tangle_cells

logger = logging.getLogger(__name__)


async def execute_code(hub_url, cells, username=None, create_user=False, delete_user=False, username_format='user-{id}', timeout=None, daemonized=False, validate=False):
    username = username or username_format.format(id=str(uuid.uuid4()))
    hub = JupyterHubAPI(hub_url)

    async with hub:
        try:
            jupyter = await hub.ensure_server(username, create_user=create_user)

            async with jupyter:
                kernel_id, kernel = await jupyter.ensure_kernel()
                async with kernel:
                    for i, (code, expected_result) in enumerate(cells):
                        kernel_result = await kernel.send_code(username, code, timeout=timeout, wait=(not daemonized))
                        if not daemonized:
                            logger.debug(f'kernel execucting cell={i} code=\n{textwrap.indent(code, "   >>> ")}')
                            logger.debug(f'kernel result cell={i} result=\n{textwrap.indent(kernel_result, "   | ")}')
                            if validate and kernel_result != expected_result:
                                diff = ''.join(difflib.unified_diff(kernel_result, expected_result))
                                logger.error(f'kernel result did not match expected result diff={diff}')
                                raise ValueError(f'execution of cell={i} did not match expected result diff={diff}')
                if not daemonized:
                    await jupyter.delete_kernel(kernel_id)
            if not daemonized:
                await hub.delete_server(username)
        finally:
            if delete_user and not daemonized:
                await hub.delete_user(username)


async def execute_notebook(hub_url, notebook_path, **kwargs):
    cells = parse_notebook_cells(notebook_path)
    await execute_code(hub_url, cells, **kwargs)
