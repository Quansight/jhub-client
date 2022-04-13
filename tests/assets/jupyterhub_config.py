from jupyterhub.auth import DummyAuthenticator
from jupyterhub.spawner import SimpleLocalProcessSpawner

c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.password = "test"
c.JupyterHub.spawner_class = SimpleLocalProcessSpawner

c.JupyterHub.users = ["user1"]
c.JupyterHub.admin_users = ["user1"]
c.JupyterHub.admin_access = True

c.JupyterHub.services = [
    {
        "name": "my-service",
        "api_token": "GiJ96ujfLpPsq7oatW1IJuER01FbZsgyCM0xH6oMZXDAV6zUZsFy3xQBZakSBo6P",
        "oauth_no_confirm": True,
        "admin": True,
    }
]
