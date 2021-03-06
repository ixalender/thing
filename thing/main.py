
import sys
import argparse

from .version import __version__
from .exceptions import ThingException
from . import commands
from .commands.list import ListSubCommand
from .commands.show import ShowSubCommand


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
        help="Specified project",
        description="Specified project",
    )
    p.add_argument("uuid", help="Project uuid")


def _add_task(subparsers):
    p = subparsers.add_parser(
        ShowSubCommand.task.value,
        help="Specified task",
        description="Specified task",
    )
    p.add_argument("uuid", help="Task uuid")


def _add_export_project(subparsers):
    p = subparsers.add_parser(
        ShowSubCommand.project.value,
        help="Specified project",
        description="Specified project",
    )
    p.add_argument("uuid", help="Project uuid")
    outout_subparsers = p.add_subparsers(
        dest="output",
        description="Get help for commands with thing COMMAND --help"
    )
    _add_file(outout_subparsers)
    _add_clipborad(outout_subparsers)


def _add_areas(subparsers):
    p = subparsers.add_parser(
        ListSubCommand.areas.value,
        help="Show areas list",
        description="Show areas list",
    )


def _add_file(subparsers):
    p = subparsers.add_parser(
        'file',
        help="Specified path of output file",
        description="Specified path of output file",
    )
    p.add_argument("file_path", help="Path to file")


def _add_clipborad(subparsers):
    p = subparsers.add_parser(
        'clipboard',
        help="Clipboard as an output of exported markdown text",
        description="Clipboard as an output of exported markdown text",
    )


def _add_export(subparsers):
    p = subparsers.add_parser(
        commands.CMD_EXPORT,
        help="Export project or task",
        description="Export project or task",
    )
    type_subparsers = p.add_subparsers(
        dest="type",
        description="Get help for commands with thing COMMAND --help"
    )
    _add_export_project(type_subparsers)


def _add_list(subparsers):
    p = subparsers.add_parser(
        commands.CMD_LIST,
        help="Show list of any type of items",
        description="Show list of any type of items",
    )
    type_subparsers = p.add_subparsers(
        dest="type",
        description="Get help for commands with thing COMMAND --help"
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
        description="Get help for commands with thing COMMAND --help"
    )
    _add_project(type_subparsers)
    _add_task(type_subparsers)


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
            return commands.export(args)
        elif args.command == commands.CMD_LIST:
            return commands.show_list(args)
        elif args.command == commands.CMD_SHOW:
            return commands.show(args)
        else:
            raise ThingException(f"Unknown command {args.command}")
    except ThingException as ex:
        print(f'\nError: {ex}\n')
    
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
