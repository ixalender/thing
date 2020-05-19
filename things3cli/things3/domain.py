
from typing import List, Optional
from pydantic import BaseModel


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
