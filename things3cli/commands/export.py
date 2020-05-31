import argparse
import subprocess
from subprocess import TimeoutExpired, CalledProcessError
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


class ExportOutput(str, Enum):
    file = 'file'
    clipboard = 'clipboard'


def _save_to_file(file_path: str, content: str) -> None:
    try:
        with open(file_path, 'w') as f:
            f.write(content)
    except IOError as ex:
        raise Things3CliException(f'Couldn\'t save to output file {file_path}: {ex}')


def _save_to_clipboard(content: str) -> None:
    try:
        subprocess.run('pbcopy', universal_newlines=True, input=content)
    except (CalledProcessError, TimeoutExpired) as ex:
        raise Things3CliException(ex)


def _proc_output(args: argparse.Namespace, content: str) -> int:
    if args is None:
        outputs = ', '.join(map(lambda i: i.value, iter(ExportOutput)))
        raise Things3CliException(f'You should specify the way to export [{outputs}].')

    if args.output == ExportOutput.file:
        _save_to_file(args.file_path, content)
    elif args.output == ExportOutput.clipboard:
        _save_to_clipboard(content)
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
            raise Things3CliException(f"Unknown item type to show {args.type}")
    except Things3StorageException as ex:
        raise Things3CliException(ex)

    return 0
