
import sys
import argparse
import textwrap

from .version import __version__
from .exceptions import Things3CliException
from . import commands
from .commands.list import ListSubCommand
from .commands.show import ShowSubCommand
from .things3.models import Project, ProjectFilter, TaskCheckListItem


HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


def print_version() -> None:
    print(__version__)


def _add_tasks(subparsers):
    p = subparsers.add_parser(
        ListSubCommand.tasks.value,
        help="Show tasks list",
        description="Show tasks list",
    )
    p.add_argument("project", help="Project uuid")


def _add_projects(subparsers):
    p = subparsers.add_parser(
        ListSubCommand.projects.value,
        help="Show projects list",
        description="Show projects list",
    )
    p.add_argument("area", help="Area uuid")


def _add_project(subparsers):
    p = subparsers.add_parser(
        ShowSubCommand.project.value,
        help="Show project",
        description="Show project",
    )
    p.add_argument("uuid", help="Project uuid")


def _add_areas(subparsers):
    p = subparsers.add_parser(
        ListSubCommand.areas.value,
        help="Show areas list",
        description="Show areas list",
    )


def _add_export(subparsers):
    p = subparsers.add_parser(
        commands.CMD_EXPORT,
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


def _add_list(subparsers):
    p = subparsers.add_parser(
        commands.CMD_LIST,
        help="Show list of any type of items",
        description="Show list of any type of items",
    )
    type_subparsers = p.add_subparsers(
        dest="type",
        description="Get help for commands with things3cli COMMAND --help"
    )
    _add_areas(type_subparsers)
    _add_projects(type_subparsers)
    _add_tasks(type_subparsers)


def _add_show(subparsers):
    p = subparsers.add_parser(
        commands.CMD_SHOW,
        help="Show any type of items",
        description="Show any type of items",
    )
    type_subparsers = p.add_subparsers(
        dest="type",
        description="Get help for commands with things3cli COMMAND --help"
    )
    _add_project(type_subparsers)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        action="store_true",
        help="show version and exit")
    subparsers = parser.add_subparsers(
        dest="command",
        description="Command"
    )
    _add_list(subparsers)
    _add_show(subparsers)
    _add_export(subparsers)

    return parser


def check_args(args: argparse.Namespace):
    if "version" in args and args.version:
        print_version()
        sys.exit(0)


def run_command(args: argparse.Namespace) -> int:
    try:
        if args.command == commands.CMD_EXPORT:
            return commands.export(args.thing_uuid)
        elif args.command == commands.CMD_LIST:
            return commands.list(args)
        elif args.command == commands.CMD_SHOW:
            return commands.show(args)
        else:
            raise Things3CliException(f"Unknown command {args.command}")
    except Things3CliException as ex:
        print(ex)
    
    return 1


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
