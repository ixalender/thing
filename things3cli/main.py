
import sys
import argparse
import textwrap

from .version import __version__
from .exceptions import Things3CliException
from . import commands

from .things3.models import Project, ProjectFilter, TaskCheckListItem


HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


COMMAND_EXPORT = 'export'
COMMAND_SHOW = 'show'


def print_version() -> None:
    print(__version__)


def _add_export(subparsers):
    p = subparsers.add_parser(
        "export",
        help="Export project or task",
        description="Export project or task",
    )
    p.add_argument("thing_uuid", help="Project or task uuid")
    p.add_argument(
        "--format",
        "-f",
        action="store_true",
        help="Export format"
    )


def _add_tasks(subparsers):
    p = subparsers.add_parser(
        "tasks",
        help="Show tasks list",
        description="Show tasks list",
    )
    p.add_argument("project", help="Project uuid")


def _add_projects(subparsers):
    p = subparsers.add_parser(
        "projects",
        help="Show projects list",
        description="Show projects list",
    )
    p.add_argument("area", help="Area uuid")


def _add_areas(subparsers):
    p = subparsers.add_parser(
        "areas",
        help="Show areas list",
        description="Show areas list",
    )


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        action="store_true",
        help="show version and exit")
    subparsers = parser.add_subparsers(
        dest="command",
        description="Get help for commands with things3cli COMMAND --help"
    )
    _add_areas(subparsers)
    _add_projects(subparsers)
    _add_tasks(subparsers)
    _add_export(subparsers)

    return parser


def check_args(args: argparse.Namespace):
    if "version" in args and args.version:
        print_version()
        sys.exit(0)


def run_command(args: argparse.Namespace) -> int:
    if args.command == COMMAND_EXPORT:
        return commands.export(args.thing_uuid)
    else:
        raise Things3CliException(f"Unknown command {args.command}")


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
