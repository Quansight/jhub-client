# JupyterHub Client

Automation of JupyterHub

# Command Line Usage

Bellow are some example use cases of the tool

## Run notebook as given user syncronously

You can run a given notebook as a pre-existing user syncronously. The
api token either has to be for the given user or an admin token.

```shell
export JUPYTERHUB_API_TOKEN=<api-token>
jhubctl --verbose run --username <username> --notebook <notebook> --hub <hub_url>
```

## Run notebook as given user syncronously and validate notebook output matches

You can run a given notebook as a pre-existing user syncronously. The
api token either has to be for the given user or an admin token.

```shell
export JUPYTERHUB_API_TOKEN=<api-token>
jhubctl run --username <username> --notebook <notebook> --hub <hub_url> --validate
```

## Run notebook asyncronously and shutdown server after completion

You can run a given notebook as a pre-existing user asyncronously and
stop server after completion. The api token either has to be for the
given user or an admin token.

```shell
export JUPYTERHUB_API_TOKEN=<api-token>
jhubctl run --username <username> --notebook <notebook> --hub <hub_url> --daemonize --stop-server
```

## Run a given notebook as a temporary user

Additionally you can temporarily create a user `user-<uuid>` or supply
the temporary user's username. The username will be deleted upon
completion. The api token requires admin permissions.

```shell
export JUPYTERHUB_API_TOKEN=<api-token>
jhubctl run --temporary-user --notebook <notebook> --hub <hub_url> [--username <username>]
```

## Simulation of several users connecting to server

Requires api token with admin permissions. The simulate command will
create `N` temporary users concurrently and run a given notebook.

```shell
export JUPYTERHUB_API_TOKEN=<api-token>
jhubctl simulate --users <num_users> --notebook <notebook> --hub <hub_url>
```

# Testing

Bring up test jupyterhub cluster

```shell
cd tests/assets
docker-compose up --build
```

Run unit tests

```shell
pytest
```
