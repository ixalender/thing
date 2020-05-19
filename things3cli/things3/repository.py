
from typing import List

from .domain import Task, TaskFilter, Project, ProjectFilter


class TaskStorage(object):
    def get_projects(self, filters: ProjectFilter) -> List[Project]: ...
    def get_tasks(self, filters: TaskFilter) -> List[Task]: ...


class Things3Storage(TaskStorage):
    def get_projects(self, filters: ProjectFilter) -> List[Project]:
        pass

    def get_tasks(self, filters: TaskFilter) -> List[Task]:
        pass
