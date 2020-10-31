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
        self.execute("PRAGMA FOREIGN_KEYS=ON")

    def commit(self):
        self.conn.commit()

    def execute(self, sqls, args=[]):
        with self.lock:
            if isinstance(sqls, str):
                return self._execute_one(sqls, args)
            num_q = sum([sql.count('?') for sql in sqls])
            assert num_q == len(args), 'num(?) != len(args): {} != {}'.format(num_q, len(args))
            start_index, results = 0, []
            for sql in sqls:
                params_cnt = sql.count('?')
                result = self._execute_one(sql, args[start_index: start_index + params_cnt])
                results.append(result)
                start_index += params_cnt
            self.commit()

    def _execute_one(self, sql, args):
        result = self.cursor.execute(sql, args)
        if isinstance(result, sqlite3.Cursor):
            result = result.fetchall()
        return result
