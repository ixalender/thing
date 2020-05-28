from typing import List, Any
import argparse
from enum import Enum
from things3cli.things3.repository import Things3SqliteStorage
from things3cli.exceptions import Things3CliException
from things3cli.things3.exceptions import Things3StorageException
from things3cli.things3.use_cases import AreaListUseCase, ProjectListUseCase, TaskListUseCase
from things3cli.things3.models import ProjectFilter, TaskFilter
from things3cli.view import print_table


class ListSubCommand(str, Enum):
    areas = 'areas'
    projects = 'projects'
    tasks = 'tasks'


def show_list(args: argparse.Namespace) -> int:
    repo = Things3SqliteStorage()
    try:
        if args.type == ListSubCommand.areas:
            au = AreaListUseCase(repo)
            areas = au.get_areas()
            print_table(list(map(lambda a: a.dict(), areas)))
            
        elif args.type == ListSubCommand.projects:
            pu = ProjectListUseCase(repo)
            projects = pu.get_projects(ProjectFilter(area=args.area))
            print_table(list(map(lambda a: a.dict(), projects)))

        elif args.type == ListSubCommand.tasks:
            tu = TaskListUseCase(repo)
            tasks = tu.get_tasks(TaskFilter(project=args.project))
            print_table(list(map(lambda a: a.dict(), tasks)))
        
        elif args.type is None:
            types = ', '.join(list(map(lambda i: i.value, iter(ListSubCommand))))
            raise Things3CliException(f"You should add the type of task you want to list, like: {types}")
        else:
            raise Things3CliException(f"Unknown item type to list {args.type}")
    except Things3StorageException as ex:
        raise Things3CliException(ex)

    return 0


def print_list(data: List[Any]):
    for el in data:
        print(el)
