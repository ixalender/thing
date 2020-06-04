
import argparse
from enum import Enum

from thing.exceptions import ThingException
from thing.things3.repository import Things3SqliteStorage
from thing.things3.exceptions import Things3StorageException
from thing.things3.models import Item, ProjectFilter
from thing.use_cases import ProjectViewUseCase
from thing.view import print_object


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
            types = ', '.join(list(map(lambda i: i.value, iter(ShowSubCommand))))
            raise ThingException(f"Unknown item type to show, try to choose one of: {types}")
    except Things3StorageException as ex:
        raise ThingException(ex)

    return 0


def display_object(item: Item) -> None:
    print_object(item.dict())
