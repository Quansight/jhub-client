import aiohttp
import yarl


async def token_authentication(api_token):
    return aiohttp.ClientSession(headers={"Authorization": f"token {api_token}"})


async def basic_authentication(hub_url, username, password):
    session = aiohttp.ClientSession()

    await session.post(
        yarl.URL(hub_url) / "login",
        data={
            "username": username,
            "password": password,
        },
    )

    return session
