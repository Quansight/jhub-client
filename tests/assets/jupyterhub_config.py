from jupyterhub.auth import DummyAuthenticator
from jupyterhub.spawner import SimpleLocalProcessSpawner

c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.password = 'test'
c.JupyterHub.spawner_class = SimpleLocalProcessSpawner

c.JupyterHub.admin_access = True

c.JupyterHub.services = [
 {
        'name': 'my-service',
        'api_token': 'super-secret',
        'oauth_no_confirm': True,
        'admin': True
    }
]
