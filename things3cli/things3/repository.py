
import typing
import sqlite3
from typing import List, Generic, TypeVar, Any, NewType
from pydantic import validator, parse_obj_as

from .exceptions import Things3DataBaseException, Things3StorageException, Things3NotFoundException
from .models import Task, TaskFilter, Project, ProjectFilter, Area, AreaFilter, Item
from .models import TaskStatus, TaskType
from .query import SqliteQuery
from . import DATABASE_FILE


class TaskStorage(object):
    def get_projects(self, filters: ProjectFilter) -> List[Project]: ...

    def get_project(self, filters: ProjectFilter) -> Project: ...

    def get_areas(self) -> List[Area]: ...

    def get_area(self, filters: AreaFilter) -> Area: ...
    
    def get_tasks(self, filters: TaskFilter) -> List[Task]: ...


class Things3SqliteStorage(TaskStorage):
    def get_areas(self) -> List[Area]:
        sql = f"""
            SELECT
                area.uuid AS uuid,
                area.title AS title,
                (
                    SELECT
                        COUNT(uuid)
                    FROM TMTask AS project
                    WHERE
                        project.area = area.uuid AND
                        project.trashed = 0 AND
                        project.status = {TaskStatus.new}
                ) AS projects
            FROM
                TMArea AS area
            ORDER BY area.title COLLATE NOCASE
        """
        try:
            q = SqliteQuery(connection=self._get_connection(), sql=sql)
            areas: List[dict] = q.execute()
            return list(map(lambda t: parse_obj_as(Area, t), areas))

        except Things3NotFoundException as ex:
            raise Things3StorageException(f'There are no any Areas')
        except Things3DataBaseException as ex:
            raise Things3StorageException(ex)

    def get_projects(self, filters: ProjectFilter) -> List[Project]:
        sql = f"""
            SELECT
                project.uuid AS uuid,
                project.title AS title,
                project.area AS area,
                (
                    SELECT
                        COUNT(uuid)
                    FROM TMTask AS task
                    WHERE
                        task.project = project.uuid AND
                        task.trashed = 0 AND
                        task.status = {TaskStatus.new}
                ) AS tasks
            FROM
                TMTask AS project
            WHERE
                project.type == {TaskType.project} AND
                project.trashed == 0 AND
                project.area == '{filters.area}'
            ORDER BY project.title COLLATE NOCASE
        """
        try:
            q = SqliteQuery(connection=self._get_connection(), sql=sql)
            projects: List[dict] = q.execute()
            return list(map(lambda t: parse_obj_as(Project, t), projects))

        except Things3NotFoundException as ex:
            raise Things3StorageException(f'There are no any projects for area {filters.area}')
        except Things3DataBaseException as ex:
            raise Things3StorageException(ex)
    
    def get_project(self, filters: ProjectFilter) -> Project:
        sql = f"""
            SELECT
                project.uuid AS uuid,
                project.title AS title,
                CASE
                    WHEN project.notes IS NULL THEN ''
                    ELSE project.notes
                END AS notes,
                project.area AS area
            FROM
                TMTask AS project
            WHERE
                project.uuid == '{filters.uuid}' AND
                project.type == {TaskType.project} AND
                project.trashed == 0
        """
        try:
            q = SqliteQuery(connection=self._get_connection(), sql=sql)
            project: dict = q.execute_for_one()
            return parse_obj_as(Project, project)

        except Things3NotFoundException as ex:
            raise Things3StorageException(f'There is no any project with id {filters.uuid}')
        except Things3DataBaseException as ex:
            raise Things3StorageException(ex)

    def get_area(self, filters: AreaFilter) -> Area:
        sql = f"""
            SELECT
                area.uuid AS uuid,
                area.title AS title
            FROM
                TMArea AS area
            WHERE
                area.uuid == '{filters.uuid}'
            ORDER BY area.title COLLATE NOCASE
        """
        try:
            q = SqliteQuery(connection=self._get_connection(), sql=sql)
            area: dict = q.execute_for_one()
            return parse_obj_as(Area, area)

        except Things3NotFoundException as ex:
            raise Things3StorageException(f'There is no any area with id {filters.uuid}')
        except Things3DataBaseException as ex:
            raise Things3StorageException(ex)

    def get_tasks(self, filters: TaskFilter) -> List[Task]:
        sql = f"""
            SELECT
                task.uuid AS uuid,
                task.title AS title,
                CASE
                    WHEN task.project IS NULL THEN heading.project
                    ELSE task.project
                END AS project,
                task.status AS status
            FROM
                TMTask AS task
            LEFT OUTER JOIN TMTask heading
                ON task.actionGroup = heading.uuid
            LEFT OUTER JOIN TMTask project_heading
                ON heading.project = project_heading.uuid
            WHERE
                task.type == {TaskType.task} AND
                task.status IN ({TaskStatus.new}, {TaskStatus.completed}) AND
                task.trashed == 0 AND
                (task.project == '{filters.project_uuid}' OR heading.project == '{filters.project_uuid}')
            ORDER BY task.title COLLATE NOCASE
        """
        try:
            q = SqliteQuery(connection=self._get_connection(), sql=sql)
            tasks: List[dict] = q.execute()
            return list(map(lambda t: parse_obj_as(Task, t), tasks))

        except Things3NotFoundException as ex:
            raise Things3StorageException(f'There are no any tasks for project {filters.project}')
        except Things3DataBaseException as ex:
            raise Things3StorageException(ex)

    def _get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            'file:' + DATABASE_FILE + '?mode=ro', uri=True)
        return connection
    