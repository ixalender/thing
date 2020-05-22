import argparse
from enum import Enum
from things3cli.exceptions import Things3CliException


class ListSubCommand(str, Enum):
    areas = 'areas'
    projects = 'projects'
    tasks = 'tasks'


def list(args: argparse.Namespace) -> int:
    if args.type == ListSubCommand.areas:
        pass
    elif args.type == ListSubCommand.projects:
        pass
    elif args.type == ListSubCommand.tasks:
        print(args.project)
    else:
        raise Things3CliException(f"Unknown item type to list {args.type}")

    return 0