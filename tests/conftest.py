import pytest

from jupyterhub_client.api import JupyterHubAPI


@pytest.fixture
async def hub():
    yield JupyterHubAPI('http://localhost:8000', 'super-secret')
