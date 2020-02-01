import argparse
import sys

from gputree.app import App
from gputree.utils import get_hosts_infos
from gputree import __DESCRIPTION__, __VERSION__


def main():
    """Entry endpoint for CLI."""
    parser = argparse.ArgumentParser(description=__DESCRIPTION__)

    parser.add_argument(
        "-H", "--hosts", type=str, nargs="+", help="list of host to inspect."
    )
    parser.add_argument(
        "-t", "--timeout", type=int, default=5, help="connection timeout in second."
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s {}".format(__VERSION__)
    )

    args = parser.parse_args()

    try:
        hosts = get_hosts_infos(args.hosts)
    except ValueError as e:
        print("ERROR -", e)
        sys.exit(1)

    app = App(hosts, args.timeout)
    app.main()
