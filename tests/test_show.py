
import pytest
import argparse
import subprocess

from thing.commands.show import ShowSubCommand, show
from thing.use_cases import TaskView, TaskViewUseCase
from thing.things3.models import Task, TaskStatus
from thing.things3.repository import Things3SqliteStorage


mock_task_view = TaskView(
    title='title',
    notes='notes',
    project='project_uuid',
    status=TaskStatus.completed
)

mock_task = Task(
    uuid='task_uuid',
    title='Task title',
    notes='Simple task note',
    project='project_uuid',
    status=TaskStatus.completed
)


@pytest.fixture
def mock_response(monkeypatch):

    def mock_get_task(*args, **kwargs):
        return mock_task

    # monkeypatch.setattr(TaskViewUseCase, "get_task", mock_get_task)
    monkeypatch.setattr(Things3SqliteStorage, "get_task", mock_get_task)


def test_show_task(capsys, mock_response):
    result = show(argparse.Namespace(**dict(
        type=ShowSubCommand.task,
        uuid='123'
    )))
    assert result == 0

    captured = capsys.readouterr()
    assert '[x]' in captured.out
