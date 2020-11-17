import argparse


def cli():
    parser = argparse.ArgumentParser(description='JupyterHub traffic simulator')
    parser.add_argument('username', type=str, help='username to simulate traffic')
    parser.add_argument('--service-token', type=str, default=os.environ.get('JUPYTERHUB_TRAFFIC_SERVICE_TOKEN'), help='service token used to login to jupyterhub')
    return parser.parse_args()
