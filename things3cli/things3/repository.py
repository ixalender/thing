
import sqlite3
import typing
from typing import List, Generic, TypeVar, Any, NewType
from pydantic.generics import GenericModel
from pydantic import validator, parse_obj_as

from .exceptions import Things3DataBaseException, Things3StorageException, Things3NotFoundException
from .models import Task, TaskFilter, Project, ProjectFilter, Area, Item
from .models import TaskStatus, TaskType
from . import DATABASE_FILE


DataT = TypeVar('DataT', Project, Task, Area)


class TaskStorage(object):
    def get_projects(self, filters: ProjectFilter) -> List[Project]: ...

    def get_areas(self) -> List[Area]: ...
    
    def get_tasks(self, filters: TaskFilter) -> List[Task]: ...


class Query(GenericModel, Generic[DataT]):
    def execute(self) -> List[DataT]: ...

    class Config:
        arbitrary_types_allowed = True


class SqliteQuery(Query, GenericModel, Generic[DataT]):
    connection: sqlite3.Connection
    sql: str

    @validator('connection', always=True)
    def check_connection(cls, v):
        if v is None:
            raise ValueError('must provide connection')
        return v

    @validator('sql', always=True)
    def check_sql(cls, v):
        if v is None:
            raise ValueError('must provide sql')
        return v

    def _dict_factory(self, cursor, row) -> dict:
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def execute(self) -> List[DataT]:
        try:
            self.connection.row_factory = self._dict_factory
            cursor = self.connection.cursor()
            cursor.execute(self.sql)
            rows = cursor.fetchall()
            tasks = list(map(lambda t: parse_obj_as(DataT, t), rows))
            if not tasks:
                raise Things3NotFoundException('Couldn\'t find any tasks')

            return tasks

        except sqlite3.OperationalError as ex:
            raise Things3DataBaseException(ex)


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
            q = SqliteQuery[Area](connection=self._get_connection(), sql=sql)
            return q.execute()
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
            q = SqliteQuery[Project](connection=self._get_connection(), sql=sql)
            return q.execute()
        except Things3NotFoundException as ex:
            raise Things3StorageException(f'There are no any projects for area {filters.area}')
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
                (task.project == '{filters.project}' OR heading.project == '{filters.project}')
            ORDER BY task.title COLLATE NOCASE
        """
        try:
            q = SqliteQuery[Task](connection=self._get_connection(), sql=sql)
            return q.execute()
        except Things3NotFoundException as ex:
            raise Things3StorageException(f'There are no any tasks for project {filters.project}')
        except Things3DataBaseException as ex:
            raise Things3StorageException(ex)

    def _get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            'file:' + DATABASE_FILE + '?mode=ro', uri=True)
        return connection
    