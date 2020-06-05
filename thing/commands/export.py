import argparse
import subprocess
from subprocess import TimeoutExpired, CalledProcessError
from enum import Enum
from pydantic import BaseModel

from thing.exceptions import ThingException
from thing.things3.repository import Things3SqliteStorage
from thing.things3.exceptions import Things3StorageException
from thing.things3.models import Item, ProjectFilter
from thing.use_cases import ProjectViewUseCase
from thing.view import print_object


class ExportSubCommand(str, Enum):
    area = 'area'
    project = 'project'


class ExportOutput(str, Enum):
    file = 'file'
    clipboard = 'clipboard'


def _save_to_file(file_path: str, content: str) -> None:
    try:
        with open(file_path, 'w') as f:
            f.write(content)
    except IOError as ex:
        raise ThingException(f'Couldn\'t save to output file {file_path}: {ex}')


def _save_to_clipboard(content: str) -> None:
    try:
        subprocess.run('pbcopy', universal_newlines=True, input=content)
    except (CalledProcessError, TimeoutExpired) as ex:
        raise ThingException(ex)


def _proc_output(args: argparse.Namespace, content: str) -> int:
    outputs = ', '.join(map(lambda i: i.value, iter(ExportOutput)))
    if args is None:
        raise ThingException(f'You should specify the way to export [{outputs}].')

    if args.output == ExportOutput.file:
        _save_to_file(args.file_path, content)
    elif args.output == ExportOutput.clipboard:
        _save_to_clipboard(content)
    else:
        raise ThingException(f'You should specify the way to export [{outputs}].')
    print('Done!')
    return 0


def export(args: argparse.Namespace) -> int:
    repo = Things3SqliteStorage()

    try:
        if args.type == ExportSubCommand.project:
            pro_usecase = ProjectViewUseCase(repo)
            project_view = pro_usecase.get_project(ProjectFilter(uuid=args.uuid))
            return _proc_output(args, project_view.to_md())

        elif args.type == ExportSubCommand.area:
            raise NotImplementedError('Not implemented')

        else:
            types = ', '.join(list(map(lambda i: i.value, iter(ExportSubCommand))))
            raise ThingException(f"Unknown item to export, you should choose one of: {types}")
    except Things3StorageException as ex:
        raise ThingException(ex)

    return 0
