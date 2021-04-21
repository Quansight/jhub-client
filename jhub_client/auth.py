import aiohttp
import yarl


async def token_authentication(api_token):
    return aiohttp.ClientSession(
        headers={"Authorization": f"token {api_token}"},
    )


async def basic_authentication(hub_url, username, password):
    session = aiohttp.ClientSession(
        headers={"Referer": str(yarl.URL(hub_url) / "hub" / "api")},
    )

    await session.post(
        yarl.URL(hub_url) / "hub" / "login",
        data={
            "username": username,
            "password": password,
        },
    )

    return session
