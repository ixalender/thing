import argparse
from enum import Enum
from pydantic import BaseModel

from things3cli.exceptions import Things3CliException
from things3cli.things3.repository import Things3SqliteStorage
from things3cli.things3.exceptions import Things3StorageException
from things3cli.things3.models import Item, ProjectFilter
from things3cli.use_cases import ProjectViewUseCase
from things3cli.view import print_object


class ExportSubCommand(str, Enum):
    area = 'area'
    project = 'project'


def _save_to_md(content: str) -> None:
    print(content)


def export(args: argparse.Namespace) -> int:
    repo = Things3SqliteStorage()
    try:
        if args.type == ExportSubCommand.project:
            pro_usecase = ProjectViewUseCase(repo)
            project_view = pro_usecase.get_project(ProjectFilter(uuid=args.uuid))
            _save_to_md(project_view.to_md())

        elif args.type == ExportSubCommand.area:
            raise NotImplementedError('Not implemented')

        else:
            raise Things3CliException(f"Unknown item type to show {args.type}")
    except Things3StorageException as ex:
        raise Things3CliException(ex)

    return 0
