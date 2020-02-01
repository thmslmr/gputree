import argparse

from gputree.app import App
from gputree.utils import parse_hosts_option
from gputree import __DESCRIPTION__, __VERSION__


def main():
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

    hosts = parse_hosts_option(args.hosts)

    app = App(hosts, args.timeout)
    app.main()
