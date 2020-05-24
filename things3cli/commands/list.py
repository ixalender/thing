import argparse
from enum import Enum
from things3cli.things3.repository import Things3SqliteStorage
from things3cli.exceptions import Things3CliException
from things3cli.things3.use_cases import AreaListUseCase, ProjectListUseCase
from things3cli.things3.models import ProjectFilter


class ListSubCommand(str, Enum):
    areas = 'areas'
    projects = 'projects'
    tasks = 'tasks'


def list(args: argparse.Namespace) -> int:
    repo = Things3SqliteStorage()
    if args.type == ListSubCommand.areas:
        au = AreaListUseCase(repo)
        areas = au.get_areas()
        for a in areas:
            print(a.uuid, a.title)
        
    elif args.type == ListSubCommand.projects:
        pu = ProjectListUseCase(repo)
        projects = pu.get_projects(ProjectFilter(area=args.area))
        for p in projects:
            print(p.uuid, p.title, p.area)
    elif args.type == ListSubCommand.tasks:
        print(args.project)
    else:
        raise Things3CliException(f"Unknown item type to list {args.type}")

    return 0