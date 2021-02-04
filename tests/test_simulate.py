import uuid

import pytest

from jhub_client.simulate import simulate_users
from jhub_client.utils import parse_notebook_cells


@pytest.mark.asyncio
async def test_n_users():
    NUM_USERS = 10

    def generate_user_workflow():
        while True:
            yield (f'user-{uuid.uuid4()}', parse_notebook_cells('tests/assets/notebook/simple.ipynb'))

    await simulate_users(
        hub_url='http://localhost:8000',
        num_users=NUM_USERS,
        user_generator=generate_user_workflow(), workflow='concurrent')
