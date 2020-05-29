
import argparse
from enum import Enum

from things3cli.exceptions import Things3CliException
from things3cli.things3.repository import Things3SqliteStorage
from things3cli.things3.exceptions import Things3StorageException
from things3cli.things3.models import Item, ProjectFilter
from things3cli.use_cases import ProjectViewUseCase
from things3cli.view import print_object


class ShowSubCommand(str, Enum):
    area = 'area'
    project = 'project'
    task = 'task'


def show(args: argparse.Namespace) -> int:
    repo = Things3SqliteStorage()
    try:
        if args.type == ShowSubCommand.project:
            pu = ProjectViewUseCase(repo)
            project = pu.get_project(ProjectFilter(uuid=args.uuid))
            display_object(project)
        elif args.type == ShowSubCommand.area:
            raise NotImplementedError('Not implemented')
        elif args.type == ShowSubCommand.task:
            raise NotImplementedError('Not implemented')
        else:
            raise Things3CliException(f"Unknown item type to show {args.type}")
    except Things3StorageException as ex:
        raise Things3CliException(ex)

    return 0


def display_object(item: Item) -> None:
    print_object(item.dict())
