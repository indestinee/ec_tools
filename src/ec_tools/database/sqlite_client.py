import sqlite3
import threading
from ec_tools import basic_tools
from ec_tools.database.database_client import DatabaseClientInterface
from ec_tools.basic_tools.colorful_log import ec_tools_local_logger

DICT_FACTORY = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


class SqliteClient(DatabaseClientInterface):
    def __init__(self, name, logger=ec_tools_local_logger, return_dict=False):
        super().__init__()
        self.db_name = basic_tools.touch_suffix(name, '.db')
        self.logger = logger
        self.return_dict = return_dict
        self.lock = threading.Lock()
        self.conn, self.cursor = None, None
        self.__connect_db()
        self.execute("PRAGMA FOREIGN_KEYS=ON")

    def commit(self):
        self.conn.commit()

    def execute(self, sqls, args=None):
        if args is None:
            args = []
        with self.lock:
            if isinstance(sqls, str):
                result = self.__execute_one(sqls, args)
                self.commit()
                return result
            else:
                num_q = sum([sql.count('?') for sql in sqls])
                assert num_q == len(args), 'num(?) != len(args): {} != {}'.format(num_q, len(args))
                start_index, results = 0, []
                for sql in sqls:
                    params_cnt = sql.count('?')
                    result = self.__execute_one(sql, args[start_index: start_index + params_cnt])
                    results.append(result)
                    start_index += params_cnt
                self.commit()

    def __execute_one(self, sql, args):
        try:
            result = self.cursor.execute(sql, args)
        except sqlite3.OperationalError as e:
            self.logger.warn(e)
            self.logger.print_exception()
            self.__connect_db()
            result = self.cursor.execute(sql, args)
        if isinstance(result, sqlite3.Cursor):
            result = result.fetchall()
        return result

    def __connect_db(self):
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        if self.return_dict:
            self.conn.row_factory = DICT_FACTORY
        self.cursor = self.conn.cursor()
