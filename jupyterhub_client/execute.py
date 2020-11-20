import uuid
import difflib
import logging
import textwrap
import datetime

from jupyterhub_client.api import JupyterHubAPI, JupyterKernelAPI, JupyterAPI
from jupyterhub_client.utils import parse_notebook_cells, tangle_cells

logger = logging.getLogger(__name__)


DAEMONIZED_STOP_SERVER_HEADER = '''
def _jupyerhub_client_stop_server():
    import urllib.request
    request = urllib.request.Request(url="{delete_server_endpoint}", method= "DELETE")
    request.add_header("Authorization", "token {api_token}")
    urllib.request.urlopen(request)

def custom_exc(shell, etype, evalue, tb, tb_offset=None):
     _jupyerhub_client_stop_server()

get_ipython().set_custom_exc((Exception,), custom_exc)
'''


async def execute_code(hub_url, cells, username=None, create_user=False, delete_user=False, username_format='user-{id}', timeout=None, daemonized=False, validate=False, stop_server=True):
    username = username or username_format.format(id=str(uuid.uuid4()))
    hub = JupyterHubAPI(hub_url)

    async with hub:
        try:
            jupyter = await hub.ensure_server(username, create_user=create_user)

            async with jupyter:
                kernel_id, kernel = await jupyter.ensure_kernel()
                async with kernel:
                    if daemonized and stop_server:
                        await kernel.send_code(username, DAEMONIZED_STOP_SERVER_HEADER.format(
                            delete_server_endpoint = hub.api_url / 'users' / username / 'server',
                            api_token=hub.api_token
                        ), wait=False)

                    for i, (code, expected_result) in enumerate(cells):
                        kernel_result = await kernel.send_code(username, code, timeout=timeout, wait=(not daemonized))
                        if daemonized:
                            logger.debug(f'kernel submitted cell={i} code=\n{textwrap.indent(code, "   >>> ")}')
                        else:
                            logger.debug(f'kernel execucting cell={i} code=\n{textwrap.indent(code, "   >>> ")}')
                            logger.debug(f'kernel result cell={i} result=\n{textwrap.indent(kernel_result, "   | ")}')
                            if validate and kernel_result != expected_result:
                                diff = ''.join(difflib.unified_diff(kernel_result, expected_result))
                                logger.error(f'kernel result did not match expected result diff={diff}')
                                raise ValueError(f'execution of cell={i} did not match expected result diff={diff}')

                    if daemonized and stop_server:
                        await kernel.send_code(username, '__jupyterhub_client_stop_server()', wait=False)
                if not daemonized:
                    await jupyter.delete_kernel(kernel_id)
            if not daemonized and stop_server:
                await hub.delete_server(username)
        finally:
            if delete_user and not daemonized:
                await hub.delete_user(username)


async def execute_notebook(hub_url, notebook_path, **kwargs):
    cells = parse_notebook_cells(notebook_path)
    await execute_code(hub_url, cells, **kwargs)
