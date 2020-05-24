
from typing import List

from .models import TaskFilter, ProjectFilter, Task, Project, Area
from .repository import TaskStorage


class TaskListUseCase:
    def __init__(self, repo: TaskStorage) -> None:
        self.repo = repo

    def get_tasks(self, filters: TaskFilter) -> List[Task]:
        return self.repo.get_tasks(filters)


class ProjectListUseCase:
    def __init__(self, repo: TaskStorage) -> None:
        self.repo = repo

    def get_projects(self, filters: ProjectFilter) -> List[Project]:
        return self.repo.get_projects(filters)


class AreaListUseCase:
    def __init__(self, repo: TaskStorage) -> None:
        self.repo = repo

    def get_areas(self) -> List[Area]:
        return self.repo.get_areas()


class ExportProjectUseCase:
    def export_project(self, project: Project) -> None:
        pass
