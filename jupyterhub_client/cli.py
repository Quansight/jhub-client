import argparse
import logging
import asyncio


def cli(args=None):
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="jupyterhub client cli")
    subparser = parser.add_subparsers(help="jupyterhub client cli")
    create_run_subcommand(subparser)
    parser.set_defaults(func=None)
    args = parser.parse_args(args)

    if args.func is None:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args.func(args)


def create_run_subcommand(subparser):
    subparser = subparser.add_parser("run")
    subparser.add_argument("-u", "--username", type=str, help="username to run notebook as", required=True)
    subparser.add_argument("-n", "--notebook", type=str, help="notebook to run", required=True)
    subparser.add_argument("--hub", type=str, default="http://localhost:8000", help="url for running jupyterhub cluster")
    subparser.set_defaults(func=handle_run)


def handle_run(args):
    from jupyterhub_client.execute import execute_notebook

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        execute_notebook(
            hub_url=args.hub,
            notebook_path=args.notebook,
            username=args.username))
