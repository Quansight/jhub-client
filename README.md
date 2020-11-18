# JupyterHub Client

Automation of JupyterHub via python client.

# CLI

## Run notebook as given user

```shell
python -m jupyterhub_client run --username <username> --notebook <notebook> --hub http://localhost:8000
```

## Simulation of several users connecting to server

```shell
python -m jupyterhub_client simulate --users <num_users> --notebook <notebook> --hub http://localhost:8000
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
