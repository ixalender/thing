
import sqlite3
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

from . import DATABASE_FILE


class TaskType(int, Enum):
    task = 0
    project = 1
    heading = 2


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect('file:' + DATABASE_FILE + '?mode=ro', uri=True)
    return connection


class Task(BaseModel):
    uuid: str
    title: str
    check_list: List[TaskCheckListItem]
    status: bool


class TaskCheckListItem(BaseModel):
    uuid: str
    title: str
    status: bool


class Project(BaseModel):
    uuid: str
    title: str
    tasks: List[Task]


class Area(BaseModel):
    uuid: str
    title: str


class TaskFilter(BaseModel):
    uuid: Optional[str]
    project: Optional[Project]
    status: Optional[str]


class ProjectFilter(BaseModel):
    uuid: Optional[str]
    area: Optional[Area]
