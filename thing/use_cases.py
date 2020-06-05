
import textwrap
from typing import List, Optional
from pydantic import BaseModel

from .things3.models import TaskFilter, ProjectFilter, AreaFilter, Task, Project, Area, TaskStatus
from .things3.repository import TaskStorage


class ProjectView(BaseModel):
    title: str
    notes: str
    area: Area
    tasks: Optional[List[Task]]

    def _match_status(self, status: TaskStatus):
            match = {
                TaskStatus.new: ' ',
                TaskStatus.completed: 'x',
            }
            return match[status]
    
    def _format_tasks(self):
        TASK_TEMPLATE_MD = """[{status}] {title}"""
        return '\n'.join(map(
            lambda t: TASK_TEMPLATE_MD.format(
                status=self._match_status(t.status),
                title=t.title
            ), self.tasks or []
        ))

    def __str__(self):
        PROJECT_PLAIN_TEXT = textwrap.dedent("""
        {title}
        {notes}
        
        {tasks}
        """)
        
        return PROJECT_PLAIN_TEXT.format(
            title=self.title,
            notes=self.notes,
            tasks=self._format_tasks()
        )

    def to_md(self) -> str:
        PROJECT_TEMPLATE_MD = textwrap.dedent("""
        # {title}

        {notes}

        ```
        {tasks}
        ```
        """)

        md_data = PROJECT_TEMPLATE_MD.format(
            title=self.title,
            notes=self.notes,
            tasks=self._format_tasks()
        )
        return md_data


class TaskView(BaseModel):
    uuid: str
    title: str
    project: str
    status: str
    

class TaskListUseCase:
    def __init__(self, repo: TaskStorage) -> None:
        self.repo = repo

    def get_tasks(self, filters: TaskFilter) -> List[TaskView]:
        return list(map(lambda t: TaskView(
            uuid=t.uuid,
            status=t.status.name,
            title=t.title,
            project=t.project,
        ), self.repo.get_tasks(filters)))


class ProjectListUseCase:
    def __init__(self, repo: TaskStorage) -> None:
        self.repo = repo

    def get_projects(self, filters: ProjectFilter) -> List[Project]:
        projects = self.repo.get_projects(filters)
        return projects


class AreaListUseCase:
    def __init__(self, repo: TaskStorage) -> None:
        self.repo = repo

    def get_areas(self) -> List[Area]:
        return self.repo.get_areas()


class ProjectViewUseCase:
    def __init__(self, repo: TaskStorage) -> None:
        self.repo = repo

    def get_project(self, filters: ProjectFilter) -> ProjectView:
        project = self.repo.get_project(filters)
        area = self.repo.get_area(AreaFilter(uuid=project.area))
        tasks = self.repo.get_tasks(TaskFilter(project_uuid=project.uuid))

        return ProjectView(
            title=project.title,
            notes=project.notes,
            area=area,
            tasks=tasks
        )
