import uuid

import pytest

from jupyterhub_client.api import JupyterKernelAPI


@pytest.mark.asyncio
async def test_hub_connection(hub):
    """Test we can connect to jupyterhub cluster"""
    async with hub:
        await hub.info()


@pytest.mark.asyncio
async def test_hub_user(hub):
    """Test that we can create a user"""

    username = f'test-{uuid.uuid4()}'

    async with hub:
        assert (await hub.get_user(username)) is None
        await hub.create_user(username)
        assert (await hub.get_user(username))['name'] == username
        await hub.delete_user(username)
        assert (await hub.get_user(username)) is None


@pytest.mark.asyncio
async def test_hub_server(hub):
    """Test that we can create a server for a given user"""
    username = f'test-{uuid.uuid4()}'

    async with hub:
        await hub.create_user(username)
        jupyter = await hub.create_server(username)
        async with jupyter:
            await jupyter.list_kernels()
        await hub.delete_server(username)
        await hub.delete_user(username)


@pytest.mark.asyncio
async def test_hub_kernel(hub):
    """Test that we can create a kernel and execute code for a given user"""
    username = f'test-{uuid.uuid4()}'

    async with hub:
        await hub.create_user(username)
        async with (await hub.create_server(username)) as jupyter:
            kernel_id = (await jupyter.create_kernel())['id']
            async with JupyterKernelAPI(jupyter.api_url / 'kernels' / kernel_id, jupyter.api_token) as kernel:
                assert await kernel.send_code(username, '''
a = 10
1 + 2
''') == '3'
                # prove that kernel is stateful
                assert await kernel.send_code(username, '''
a
''') == '10'
            await jupyter.delete_kernel(kernel_id)
        await hub.delete_server(username)
        await hub.delete_user(username)
