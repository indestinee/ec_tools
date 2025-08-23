import dataclasses
from typing import Any, Collection, Dict, List, Type

from ec_tools.database.sqlite_client.sqlite_query import SqliteQuery
from ec_tools.database.sqlite_dao.sqlite_data_object import SqliteDataObject
from ec_tools.utils.misc import remove_none_from_dict


class SqliteQueryGenerator:
    _data_type: Type[SqliteDataObject]
    _table_name: str
    _primary_keys: List[str]
    _unique_keys: List[List[str]]
    _field_names: List[str]

    def __init__(self, clz: Type[SqliteDataObject], table_name: str):
        self._data_type = clz
        self._table_name = table_name
        self._primary_keys = clz.primary_keys()
        self._unique_keys = clz.unique_keys()
        self._field_names = clz.field_names()
        if self._primary_keys:
            self._unique_keys.append(self._primary_keys)

    @property
    def create_table_sql(self) -> List[SqliteQuery]:
        db_columns = self._build_db_columns()
        primary_sqls = self._build_primary_sql()
        constraint_sqls = self._build_constraint_sqls()
        return [
            SqliteQuery(
                f"CREATE TABLE IF NOT EXISTS {self._table_name}",
                f"({', '.join(db_columns + primary_sqls + constraint_sqls)})",
            ),
        ] + [
            SqliteQuery(
                f"CREATE INDEX IF NOT EXISTS {'__'.join(['index', *index])} ON {self._table_name}",
                f"({', '.join(index)})",
            )
            for index in self._data_type.extra_indexes()
            if index
        ]

    @property
    def drop_table_sql(self) -> SqliteQuery:
        return SqliteQuery(f"DROP TABLE IF EXISTS {self._table_name}")

    def insert_sql(self, objs: Collection[SqliteDataObject], supplement: str = "") -> SqliteQuery:
        items = [obj.to_json() for obj in objs]
        return SqliteQuery(
            f"INSERT {supplement} INTO {self._table_name}",
            f"({', '.join(self._field_names)})",
            f"VALUES ({', '.join('?' * len(self._field_names))})",
            args=[[item[field_name] for field_name in self._field_names] for item in items],
        )

    def query_by_values_sql(
        self,
        value_map: Dict[str, Any],
        limit: int,
        offset: int,
        fields: List[str] = None,
    ):
        value_map = remove_none_from_dict(value_map)
        keys = self._filter_keys(value_map.keys())
        fields = self._filter_keys(fields)
        field_str = ", ".join(fields) if fields else "*"
        return SqliteQuery(
            f"SELECT {field_str} FROM {self._table_name}",
            f"WHERE {' AND '.join([f'{key} = ?' for key in keys])}" if keys else "",
            f"LIMIT {limit} OFFSET {offset}",
            args=[value_map[key] for key in keys],
        )

    def delete_by_values_sql(self, value_map: Dict[str, Any]):
        value_map = remove_none_from_dict(value_map)
        keys = self._filter_keys(value_map.keys())
        return SqliteQuery(
            f"DELETE FROM {self._table_name}",
            f"WHERE {' AND '.join([f'{key} = ?' for key in keys])}" if keys else "",
            args=[value_map[key] for key in keys],
        )

    def count_by_values_sql(self, value_map: Dict[str, Any], group_by: List[str]):
        value_map = remove_none_from_dict(value_map)
        keys = self._filter_keys(value_map.keys())
        group_by = self._filter_keys(group_by)
        group_by_str = "".join([f"{key}, " for key in group_by])
        return SqliteQuery(
            f"SELECT {group_by_str}COUNT(*) AS count FROM {self._table_name}",
            f"WHERE {' AND '.join([f'{key} = ?' for key in keys])}" if keys else "",
            f"GROUP BY {', '.join(group_by)}" if group_by else "",
            args=[value_map[key] for key in keys],
        )

    def _build_db_columns(self) -> List[str]:
        return [
            f"{field.name} {self._determine_db_type(field)}"
            f"{' NOT NULL' if field.name in self._primary_keys else ''}"
            for field in dataclasses.fields(self._data_type)
        ]

    @classmethod
    def _determine_db_type(cls, field: dataclasses.Field) -> str:
        if field.type is float and field.name.endswith("_at"):
            return "TIMESTAMP"
        if field.type is float:
            return "REAL"
        if field.type is int or field.type is bool:
            return "INTEGER"
        return "TEXT"

    def _build_primary_sql(self) -> List[str]:
        if not self._primary_keys:
            return []
        return [f"PRIMARY KEY ({', '.join(self._primary_keys)})"]

    def _build_constraint_sqls(self) -> List[str]:
        if not self._unique_keys:
            return []
        return [
            f"CONSTRAINT {'__'.join(['unique', *unique])} UNIQUE ({', '.join(unique)})" for unique in self._unique_keys
        ]

    # avoid injection or unexpected behavior
    def _filter_keys(self, keys: Collection[str], strict: bool = True):
        if strict:
            unexpected_keys = [key for key in keys if key not in self._field_names]
            assert len(unexpected_keys) == 0, f"unexpected keys found: {unexpected_keys}"
        return [key for key in keys if key in self._field_names]
