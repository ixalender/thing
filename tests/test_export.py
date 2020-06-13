
import pytest
import argparse
import subprocess

from thing.commands.export import ExportSubCommand, ExportOutput, export
from thing.use_cases import ProjectViewUseCase, ProjectView
from thing.things3.models import Area, Task, TaskStatus


mock_project = ProjectView(
    title='title',
    notes='notes',
    area=Area(
        uuid='uuid',
        title='title',
        projects=None
    ),
    tasks=[
        Task(
            uuid='taask_uuid',
            title='test_task',
            project='proj_uuid',
            notes='Simple task note',
            status=TaskStatus.new
        )
    ]
)


@pytest.fixture
def mock_response(monkeypatch):

    def mock_get_project(*args, **kwargs):
        return mock_project

    monkeypatch.setattr(ProjectViewUseCase, "get_project", mock_get_project)


def test_export(mock_response):
    export(argparse.Namespace(**dict(
        type=ExportSubCommand.project,
        uuid=mock_project.tasks[0].project,
        output=ExportOutput.clipboard,
    )))
    
    content = subprocess.check_output(['pbpaste'])
    
    assert content.decode('utf-8') == mock_project.to_md()

