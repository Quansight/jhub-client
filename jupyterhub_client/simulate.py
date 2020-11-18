import uuid
import difflib
import json

from jupyterhub_client.api import JupyterHubAPI, JupyterKernelAPI


async def execute_code(hub_url, cells, username=None, username_format='user-{id}', timeout=None):
    username = username or username_format.format(id=str(uuid.uuid4()))
    hub = JupyterHubAPI(hub_url)

    async with hub:
        try:
            await hub.create_user(username)
            jupyter = await hub.create_server(username)
            async with jupyter:
                kernel_id = (await jupyter.create_kernel())['id']
                async with JupyterKernelAPI(jupyter.api_url / 'kernels' / kernel_id, jupyter.api_token) as kernel:
                    for i, (code, expected_result) in enumerate(cells):
                        kernel_result = await kernel.send_code(username, code, timeout=timeout)
                        if kernel_result != expected_result:
                            diff = ''.join(difflib.unified_diff(kernel_result, expected_result))
                            raise ValueError(f'execution of cell={i} code={code} did not match expected result diff={diff}')
                await jupyter.delete_kernel(kernel_id)
            await hub.delete_server(username)
        finally:
            await hub.delete_user(username)


async def execute_notebook(hub_url, notebook_path, username=None, username_format='user-{id}', timeout=None):
    with open(notebook_path) as f:
        notebook_data = json.load(f)

    cells = []
    for cell in notebook_data['cells']:
        if cell['cell_type'] == 'code':
            cells.append((''.join(cell['source']), ''.join(cell['outputs'][0]['data']['text/plain'])))

    print(cells)

    await execute_code(hub_url, cells, username=username, username_format=username_format, timeout=timeout)
