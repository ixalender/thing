
import argparse
from enum import Enum

from things3cli.exceptions import Things3CliException
from things3cli.things3.repository import Things3SqliteStorage
from things3cli.things3.exceptions import Things3StorageException
from things3cli.things3.use_cases import ProjectViewUseCase
from things3cli.things3.models import Item, ProjectFilter
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
            print_object(project.dict())
        elif args.type == ShowSubCommand.area:
            return 0
        elif args.type == ShowSubCommand.task:
            return 0
        else:
            raise Things3CliException(f"Unknown item type to show {args.type}")
    except Things3StorageException as ex:
        raise Things3CliException(ex)

    return 0


def print_task(task_item: Item) -> None:
    print(task_item)