import logging
import sqlite3
import threading

from ec_tools.database.sqlite_client.sqlite_query import SqliteQuery

sqlite3.register_adapter(bool, int)
sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))


class SqliteClient:
    _db_path: str
    _conn: sqlite3.Connection
    _cursor: sqlite3.Cursor
    _lock: threading.Lock
    _logger: logging.Logger = logging.getLogger("SqliteClient")

    def __init__(self, db_path: str):
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
        self._cursor = self._conn.cursor()
        self._lock = threading.Lock()
        self._cursor.execute("PRAGMA foreign_keys = ON")

    def __del__(self):
        self._conn.commit()
        self._conn.close()

    def execute(self, *queries: SqliteQuery, commit=True):
        _ = [self._logger.debug("SQL: %s", query) for query in queries]
        with self._lock:
            results = [self._cursor.execute(query.sql, query.args).fetchall() for query in queries]
            if commit:
                self._conn.commit()
            return results

    def batch_insert(self, query: SqliteQuery):
        with self._lock:
            self._logger.debug("SQL: %s", query)
            result = self._cursor.executemany(query.sql, query.args).fetchall()
            self._conn.commit()
            return result

    def __str__(self):
        return f"SqliteClient(db_path={self._db_path})"

    def __repr__(self):
        return str(self)
