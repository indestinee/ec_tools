import time
from typing import Any, List, Optional

from ec_tools.database.kv_dao.kv_dao import ONE_THOUSAND_YEAR, KvDao
from ec_tools.database.kv_dao.kv_data import KvData
from ec_tools.database.sqlite_client.sqlite_client import SqliteClient
from ec_tools.database.sqlite_client.sqlite_query import SqliteQuery
from ec_tools.database.sqlite_dao.sqlite_dao import SqliteDao


class SqliteKvDao(SqliteDao[KvData], KvDao):
    def __init__(
        self,
        sqlite_client: SqliteClient,
        default_duration: float = ONE_THOUSAND_YEAR,
        table_name: Optional[str] = None,
    ):
        SqliteDao.__init__(self, sqlite_client=sqlite_client, data_type=KvData, table_name=table_name)
        KvDao.__init__(self, default_duration=default_duration)

    def _get(self, key: str) -> Any:
        rows = self.execute(
            SqliteQuery(
                f"SELECT value FROM {self._table_name}",
                "WHERE key = ? AND expired_at > ?",
                args=[key, time.time()],
            ),
            commit=False,
        )[0]
        return rows[0]["value"] if rows else None

    def _set(self, key: str, value: str, duration: float) -> None:
        return self.insert_or_replace([KvData(key=key, value=value, expired_at=time.time() + duration)])

    def keys(self) -> List[str]:
        rows = self.execute(
            SqliteQuery(
                f"SELECT key FROM {self._table_name}",
                "WHERE expired_at > ?",
                args=[time.time()],
            ),
            commit=False,
        )[0]
        return [row["key"] for row in rows]

    def delete(self, key: str) -> None:
        return self.delete_by_values(key=key)

    def clear(self) -> None:
        return self.delete_by_values()
