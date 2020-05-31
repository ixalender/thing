
import typing
import sqlite3
from typing import List, Generic, TypeVar, Any, NewType, Optional
from pydantic.generics import GenericModel
from pydantic import validator, parse_obj_as, BaseModel

from .models import Task, Project, Area
from .exceptions import Things3DataBaseException, Things3NotFoundException


class Query(BaseModel):
    def execute(self) -> List[dict]: ...

    def execute_for_one(self) -> dict: ...

    class Config:
        arbitrary_types_allowed = True


class SqliteQuery(Query):
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

    def execute(self) -> List[dict]:
        try:
            self.connection.row_factory = self._dict_factory
            cursor = self.connection.cursor()
            cursor.execute(self.sql)
            tasks = cursor.fetchall()
            # print(tasks)
            if not tasks:
                raise Things3NotFoundException('Couldn\'t find any data')

            return tasks

        except sqlite3.OperationalError as ex:
            raise Things3DataBaseException(ex)
    
    def execute_for_one(self) -> dict:
        try:
            self.connection.row_factory = self._dict_factory
            cursor = self.connection.cursor()
            cursor.execute(self.sql)
            task = cursor.fetchone()
            if task is None:
                raise Things3NotFoundException('Couldn\'t find any data for one')

            return task

        except sqlite3.OperationalError as ex:
            raise Things3DataBaseException(ex)

