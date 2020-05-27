
import typing
import sqlite3
from typing import List, Generic, TypeVar, Any, NewType
from pydantic.generics import GenericModel
from pydantic import validator, parse_obj_as

from .models import Task, Project, Area
from .exceptions import Things3DataBaseException, Things3NotFoundException


DataT = TypeVar('DataT', Project, Task, Area)


class Query(GenericModel, Generic[DataT]):
    def execute(self) -> List[DataT]: ...

    def execute_for_one(self) -> DataT: ...

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
                raise Things3NotFoundException('Couldn\'t find any data')

            return tasks

        except sqlite3.OperationalError as ex:
            raise Things3DataBaseException(ex)
    
    def execute_for_one(self) -> DataT:
        try:
            self.connection.row_factory = self._dict_factory
            cursor = self.connection.cursor()
            cursor.execute(self.sql)
            row = cursor.fetchone()
            if row is None:
                raise Things3NotFoundException('Couldn\'t find any data for one')
            task = parse_obj_as(DataT, row)

            return task

        except sqlite3.OperationalError as ex:
            raise Things3DataBaseException(ex)

