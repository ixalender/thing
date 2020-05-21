
from typing import List, Optional
from pydantic import BaseModel


class Item(BaseModel):
    uuid: str
    title: str


class TaskCheckListItem(Item):
    status: bool


class Task(Item):
    check_list: List[TaskCheckListItem]
    status: bool


class Project(Item):
    tasks: List[Task]


class Area(Item): ...


class TaskFilter(BaseModel):
    uuid: Optional[str]
    project: Optional[Project]
    status: Optional[str]


class ProjectFilter(BaseModel):
    uuid: Optional[str]
    area: Optional[Area]
