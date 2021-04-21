import aiohttp
import yarl


async def token_authentication(api_token, verify_ssl=True):
    return aiohttp.ClientSession(
        headers={"Authorization": f"token {api_token}"},
        connector=aiohttp.TCPConnector(ssl=None if verify_ssl else False),
    )


async def basic_authentication(hub_url, username, password, verify_ssl=True):
    session = aiohttp.ClientSession(
        headers={"Referer": str(yarl.URL(hub_url) / "hub" / "api")},
        connector=aiohttp.TCPConnector(ssl=None if verify_ssl else False),
    )

    await session.post(
        yarl.URL(hub_url) / "hub" / "login",
        data={
            "username": username,
            "password": password,
        },
    )

    return session
