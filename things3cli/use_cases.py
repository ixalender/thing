
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

    def to_md(self) -> str:
        PROJECT_TEMPLATE_MD = textwrap.dedent("""
        # {title}

        {notes}

        ```
        {tasks}
        ```
        """)

        TASK_TEMPLATE_MD = """[{status}] {title}"""

        def match_status(status: TaskStatus):
            match = {
                TaskStatus.new: ' ',
                TaskStatus.completed: 'x',
            }
            return match[status]

        md_data = PROJECT_TEMPLATE_MD.format(
            title=self.title,
            notes=self.notes,
            tasks='\n'.join(map(
                lambda t: TASK_TEMPLATE_MD.format(
                    status=match_status(t.status),
                    title=t.title
                ), self.tasks or []
            )),
        )

        return md_data


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
