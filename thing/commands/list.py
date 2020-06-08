import argparse
from enum import Enum
from typing import List, Optional, Sequence, Union
from pydantic import BaseModel

from thing.things3.repository import Things3SqliteStorage
from thing.things3.exceptions import Things3StorageException
from thing.things3.models import ProjectFilter, TaskFilter, Item
from thing.use_cases import AreaListUseCase, ProjectListUseCase, TaskListUseCase
from thing.exceptions import ThingException
from thing.view import print_table


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
            display_list(areas)
            
        elif args.type == ListSubCommand.projects:
            pu = ProjectListUseCase(repo)
            projects = pu.get_projects(ProjectFilter(area=args.area))
            display_list(projects, exclude=['area', 'notes'])

        elif args.type == ListSubCommand.tasks:
            tu = TaskListUseCase(repo)
            tasks = tu.get_tasks(TaskFilter(project_uuid=args.project))
            display_list(tasks, exclude=['project', 'check_list'])
        
        elif args.type is None:
            types = ', '.join(list(map(lambda i: i.value, iter(ListSubCommand))))
            raise ThingException(f"You should add the type of task you want to list, like: {types}")
        else:
            raise ThingException(f"Unknown item type to list {args.type}")
    except Things3StorageException as ex:
        raise ThingException(ex)

    return 0


def display_list(data: Sequence[Union[Item, BaseModel]], exclude: Optional[List[str]] = None):
    to_exclude = exclude or []

    def filter_keys(obj: dict) -> dict:
        out = dict()
        for k, v in obj.items():
            if k not in to_exclude:
                out[k] = v
        return out
    
    out_list = list(map(lambda a: filter_keys(a.dict()), data))
    print_table(out_list)
