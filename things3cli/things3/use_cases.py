
from typing import List

from .domain import TaskFilter, ProjectFilter, Task, Project
from .repository import TaskStorage


class TasksListUseCase:
    def __init__(self, repo: TaskStorage) -> None:
        self.repo = repo

    def get_tasks(self, filters: TaskFilter) -> List[Task]:
        return self.repo.get_tasks(filters)


class ProjectListUseCase:
    def __init__(self, repo: TaskStorage) -> None:
        self.repo = repo

    def get_projects(self, filters: ProjectFilter) -> List[Project]:
        return self.repo.get_projects(filters)


class ExportProjectUseCase:
    def export_project(self, project: Project) -> None:
        pass
