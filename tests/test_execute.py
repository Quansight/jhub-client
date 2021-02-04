import pytest

from jhub_client.execute import execute_code, execute_notebook


@pytest.mark.asyncio
@pytest.mark.parametrize('cells', [
    ([
        ('import time; time.sleep(1); 1', '1'),
        ('2**3', '8'),
        ('a = 10; 1 + 2', '3'),
        ('a', '10'),
    ]),
])
async def test_execute_code(cells):
    # 1. create user
    # 2. create user jupyterlab server
    # 3. create jupyterlab kernel
    # 4. create websocket connection to jupyterlab kernel
    # 5. send code to jupyterlab kernel and check results match
    await execute_code(hub_url='http://localhost:8000', cells=cells, create_user=True, delete_user=True, temporary_user=True)


@pytest.mark.asyncio
@pytest.mark.parametrize('notebook_path', [
   'tests/assets/notebook/simple.ipynb',
])
async def test_execute_notebook(notebook_path):
    await execute_notebook(hub_url='http://localhost:8000', notebook_path=notebook_path, create_user=True, delete_user=True, temporary_user=True)
