
import sys
import argparse
import textwrap


from .version import __version__


HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


def print_version() -> None:
    print(__version__)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="store_true", help="show version and exit")
    subparsers = parser.add_subparsers(
        dest="command", description="Get help for commands with things3cli COMMAND --help"
    )
    return parser


def check_args(args: argparse.Namespace):
    if "version" in args and args.version:
        print_version()
        sys.exit(0)


def run_command(args: argparse.Namespace) -> int:
    return 0


def cli() -> int:
    try:
        sys.stderr.write(f"{HIDE_CURSOR}")
        parser = get_parser()
        parsed_args = parser.parse_args()
        check_args(parsed_args)
        if not parsed_args.command:
            parser.print_help()
            return 1
        return run_command(parsed_args)
    except KeyboardInterrupt:
        return 1
    finally:
        sys.stderr.write(f"{SHOW_CURSOR}")


if __name__ == '__main__':
    sys.exit(cli())
