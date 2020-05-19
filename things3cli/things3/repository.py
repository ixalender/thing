
import sqlite3
from typing import List
from enum import Enum

from .domain import Task, TaskFilter, Project, ProjectFilter
from . import DATABASE_FILE


class TaskType(int, Enum):
    task = 0
    project = 1
    heading = 2


class TaskStorage(object):
    def get_projects(self, filters: ProjectFilter) -> List[Project]: ...

    def get_tasks(self, filters: TaskFilter) -> List[Task]: ...


class Things3SqliteStorage(TaskStorage):
    def get_projects(self, filters: ProjectFilter) -> List[Project]:
        pass

    def get_tasks(self, filters: TaskFilter) -> List[Task]:
        pass

    def _get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            'file:' + DATABASE_FILE + '?mode=ro', uri=True)
        return connection
