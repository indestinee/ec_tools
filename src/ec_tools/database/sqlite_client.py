import sqlite3
import threading
from ec_tools import basic_tools
from ec_tools.database.database_client import DatabaseClientInterface
from ec_tools.basic_tools.colorful_log import ec_tools_local_logger


class SqliteClient(DatabaseClientInterface):
    def __init__(self, name, logger=ec_tools_local_logger):
        super().__init__()
        self.db_name = basic_tools.touch_suffix(name, '.db')
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.lock = threading.Lock()
        self.logger = logger

    def commit(self):
        self.conn.commit()

    def execute(self, *args, **kwargs):
        try:
            self.lock.acquire()
            result = self.cursor.execute(*args, **kwargs)
            if isinstance(result, sqlite3.Cursor):
                result = result.fetchall()
            self.conn.commit()
            return result
        except Exception as e:
            self.logger.error(e)
            raise e
        finally:
            self.lock.release()
