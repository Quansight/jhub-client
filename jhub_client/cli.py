import argparse
import logging
import asyncio
import sys
import json

logger = logging.getLogger(__name__)


def cli(args=None):
    parser = argparse.ArgumentParser(description="jupyterhub client cli")
    subparser = parser.add_subparsers(help="jupyterhub client cli")
    create_run_subcommand(subparser)
    parser.set_defaults(func=None)
    parser.add_argument("-v", "--verbose", action="store_true", help="turn on jhub_client debugging")
    args = parser.parse_args(args)

    if args.func is None:
        parser.print_help(sys.stderr)
        sys.exit(1)

    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=logging_level)
    args.func(args)


def create_run_subcommand(subparser):
    subparser = subparser.add_parser("run")
    subparser.add_argument("-n", "--notebook", type=str, help="notebook to run", required=True)
    subparser.add_argument("--hub", type=str, default="http://localhost:8000", help="url for running jupyterhub cluster")
    subparser.add_argument("-u", "--username", type=str, help="username to run notebook as")
    subparser.add_argument("--user-options", type=str, help="json object representing user server options")
    subparser.add_argument("--temporary-user", action='store_true', default=False, help="create user temporarily if does not exist")
    subparser.add_argument('-d', '--daemonize', action='store_true', default=False, help='run notebook asyncronously')
    subparser.add_argument('--stop-server', action='store_true', default=False, help='stop server after completion of notebook')
    subparser.add_argument('--validate', action='store_true', default=False, help='validate notebook output matches')
    subparser.add_argument('--kernel-spec', type=str, help='kernel spec to launch is not specified will use default')
    subparser.add_argument('--output-filename', type=str, help='output filename for results of running notebook')
    subparser.set_defaults(func=handle_run)


def handle_run(args):
    from jhub_client.execute import execute_notebook
    from jhub_client.utils import render_notebook

    loop = asyncio.get_event_loop()

    try:
        user_options = json.loads(args.user_options or '{}')
    except json.decoder.JSONDecodeError:
        logger.error(f'unable to json parse user options="{args.user_options}"')
        sys.exit(1)

    kwargs = {
        'hub_url': args.hub,
        'notebook_path': args.notebook,
        'username': args.username,
        'temporary_user': args.temporary_user,
        'create_user': args.temporary_user,
        'delete_user': args.temporary_user,
        'validate': args.validate,
        'daemonized': args.daemonize,
        'stop_server': args.stop_server,
        'user_options': args.user_options,
        'kernel_spec': args.kernel_spec,
    }

    if args.daemonize and args.temporary_user:
        logger.warning('running notebook in daemonized mode will not delete temporary user')

    if args.daemonize and args.validate:
        logger.error('running notebook in daemonized mode does not support validation')
        sys.exit(1)

    if args.daemonize and args.output_filename:
        logger.error('running notebooks in daemonized mode does not support writing output to notebook')
        sys.exit(1)

    cell_results = loop.run_until_complete(execute_notebook(**kwargs))

    if args.output_filename:
        output_notebook = render_notebook(cell_results)

        with open(args.output_filename, 'w') as f:
            json.dump(output_notebook, f, indent=4)
