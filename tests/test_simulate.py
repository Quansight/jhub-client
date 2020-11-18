import pytest

from jupyterhub_client.simulate import execute_code

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
    await execute_code(hub_url='http://localhost:8000', cells=cells)
