import pytest

from jhub_client.api import JupyterHubAPI


@pytest.fixture
async def hub():
    yield JupyterHubAPI(
        hub_url='http://localhost:8000',
        api_token='GiJ96ujfLpPsq7oatW1IJuER01FbZsgyCM0xH6oMZXDAV6zUZsFy3xQBZakSBo6P')
