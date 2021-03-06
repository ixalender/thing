
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class TaskStatus(int, Enum):
    new = 0
    canceled = 2
    completed = 3


class TaskType(int, Enum):
    task = 0
    project = 1
    heading = 2


class Item(BaseModel):
    uuid: str
    title: str


class TaskCheckListItem(Item):
    status: bool


class Task(Item):
    project: str
    notes: str
    status: TaskStatus
    check_list: Optional[List[TaskCheckListItem]]


class Project(Item):
    area: str
    notes: Optional[str]
    tasks: Optional[int]


class Area(Item):
    projects: Optional[int]


class TaskFilter(BaseModel):
    uuid: Optional[str]
    project_uuid: Optional[str]
    statuses: Optional[List[TaskStatus]] = [
        TaskStatus.new,
        TaskStatus.completed
    ]


class ProjectFilter(BaseModel):
    uuid: Optional[str]
    area: Optional[str]
    statuses: Optional[List[TaskStatus]] = [
        TaskStatus.new,
        TaskStatus.completed
    ]


class AreaFilter(BaseModel):
    uuid: str
