import logging
import time
import unittest

from ec_tools.database import SqliteKvDao, SqliteClient

logging.basicConfig(level=logging.DEBUG)


class KvDaoTest(unittest.TestCase):
    sqlite_client = SqliteClient(":memory:")
    kv_dao = SqliteKvDao(sqlite_client)

    def test(self):
        logging.info("dao: %s", self.kv_dao)
        self.kv_dao.drop_table()
        self.kv_dao.create_table()

        # tests default get
        self.assertEqual(self.kv_dao.get("hello", "??"), "??")
        self.assertEqual(self.kv_dao.get("hello"), None)

        # tests set and get
        self.kv_dao.set("hi", "how are you")
        self.kv_dao.set("hello", "world", 1)
        self.assertEqual(self.kv_dao.get("hi"), "how are you")
        self.assertEqual(self.kv_dao.get("hello"), "world")
        self.assertEqual(self.kv_dao.get("hello", "??"), "world")
        time.sleep(1)

        # hello is expired, while hi is not
        self.assertTrue("hi" in self.kv_dao)
        self.assertFalse("hello" in self.kv_dao)
        self.assertEqual(self.kv_dao["hi"], "how are you")
        self.assertEqual(self.kv_dao["hello"], None)
        self.assertEqual(self.kv_dao.get("hi"), "how are you")
        self.assertEqual(self.kv_dao.get("hello"), None)

        # delete hi
        self.kv_dao.delete("hi")
        self.assertEqual(self.kv_dao.get("hi"), None)
