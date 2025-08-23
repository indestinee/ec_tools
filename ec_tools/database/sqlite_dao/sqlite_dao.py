from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from ec_tools.database.sqlite_client.sqlite_client import SqliteClient
from ec_tools.database.sqlite_client.sqlite_query import SqliteQuery
from ec_tools.database.sqlite_dao.sqlite_data_object import SqliteDataObject
from ec_tools.database.sqlite_dao.sqlite_query_generator import SqliteQueryGenerator

T = TypeVar("T", bound=SqliteDataObject)


class SqliteDao(Generic[T]):
    _sqlite_client: SqliteClient
    _data_type: Type[T]
    _sql_generator: SqliteQueryGenerator
    _table_name: str

    def __init__(
        self,
        sqlite_client: SqliteClient,
        data_type: Type[T],
        table_name: Optional[str] = None,
    ):
        self._sqlite_client = sqlite_client
        self._data_type = data_type
        self._table_name = table_name or self._data_type.__name__
        self._sql_generator = SqliteQueryGenerator(clz=self._data_type, table_name=self._table_name)
        self.create_table()

    @property
    def table_name(self):
        return self._table_name

    def create_table(self):
        self._sqlite_client.execute(*self._sql_generator.create_table_sql)

    def drop_table(self):
        self._sqlite_client.execute(self._sql_generator.drop_table_sql)

    def insert(self, objs: List[T]):
        return self._sqlite_client.batch_insert(self._sql_generator.insert_sql(objs=objs))

    def insert_or_replace(self, objs: List[T]):
        return self._sqlite_client.batch_insert(self._sql_generator.insert_sql(objs=objs, supplement="OR REPLACE"))

    def insert_or_ignore(self, objs: List[T]):
        return self._sqlite_client.batch_insert(self._sql_generator.insert_sql(objs=objs, supplement="OR IGNORE"))

    def delete_by_values(self, **value_map):
        return self._sqlite_client.execute(
            self._sql_generator.delete_by_values_sql(value_map),
        )

    def count_by_values(self, **value_map) -> int:
        return self.count_group_by_values([], **value_map)[0]["count"]

    def count_group_by_values(self, group_by: List[str], **value_map) -> List[Dict[str, Any]]:
        return self._sqlite_client.execute(
            self._sql_generator.count_by_values_sql(value_map, group_by or []),
            commit=False,
        )[0]

    def query_by_values(self, limit: int = 100, offset: int = 0, **value_map) -> List[T]:
        return list(
            map(
                self._data_type.from_json,
                self.query_fields_by_values([], limit, offset, **value_map),
            )
        )

    def query_fields_by_values(
        self, fields: List[str], limit: int = 100, offset: int = 0, **value_map
    ) -> List[Dict[str, Any]]:
        return self._sqlite_client.execute(
            self._sql_generator.query_by_values_sql(value_map, limit=limit, offset=offset, fields=fields or []),
            commit=False,
        )[0]

    def execute(self, *queries: SqliteQuery, commit: bool = True):
        return self._sqlite_client.execute(*queries, commit=commit)

    def __str__(self):
        return f"SqliteDao<{self._data_type.__name__}>(sqlite_client={self._sqlite_client})"

    def __repr__(self):
        return str(self)
