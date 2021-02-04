import uuid

import pytest

from jhub_client.api import JupyterKernelAPI, JupyterAPI


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
        try:
            await hub.create_user(username)
            await hub.create_server(username)
            jupyter = JupyterAPI(hub.hub_url / 'user' / username, hub.api_token)
            async with jupyter:
                await jupyter.list_kernels()
            await hub.delete_server(username)
        finally:
            await hub.delete_user(username)


@pytest.mark.asyncio
async def test_hub_kernel(hub):
    """Test that we can create a kernel and execute code for a given user"""
    username = f'test-{uuid.uuid4()}'

    async with hub:
        try:
            await hub.create_user(username)
            await hub.create_server(username)
            jupyter = JupyterAPI(hub.hub_url / 'user' / username, hub.api_token)
            async with jupyter:
                kernel_id = (await jupyter.create_kernel())['id']
                kernel = JupyterKernelAPI(jupyter.api_url / 'kernels' / kernel_id, jupyter.api_token)
                async with kernel:
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
        finally:
            await hub.delete_user(username)
