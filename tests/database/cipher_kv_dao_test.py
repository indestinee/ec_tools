import logging
import time
import unittest

from ec_tools.database import SqliteKvDao, SqliteClient, CipherKvDao
from ec_tools.tools.cipher import AesCipherGenerator

logging.basicConfig(level=logging.DEBUG)


class CipherKvDaoTest(unittest.TestCase):
    sqlite_client = SqliteClient(":memory:")
    kv_dao = SqliteKvDao(sqlite_client)
    cipher_generator = AesCipherGenerator()
    cipher_kv_dao = CipherKvDao(kv_dao, cipher_generator)

    def test(self):
        password = "abcdefg12345678"

        logging.info("dao: %s", self.kv_dao)
        self.kv_dao.drop_table()
        self.kv_dao.create_table()

        # tests default get
        self.assertEqual(self.cipher_kv_dao.get("hello", password, "??"), "??")
        self.assertEqual(self.cipher_kv_dao.get_bytes("hello", password, b"??"), b"??")
        self.assertEqual(self.cipher_kv_dao.get("hello", password, None), None)
        self.assertEqual(self.cipher_kv_dao.get_bytes("hello", password, None), None)

        # tests set and get
        self.cipher_kv_dao.set("hi", password, "how are you")
        self.cipher_kv_dao.set_bytes("hihi", password, b"how are you")
        self.cipher_kv_dao.set("hello", password, "world", 1)
        self.assertEqual(self.cipher_kv_dao.get("hi", password), "how are you")
        self.assertEqual(self.cipher_kv_dao.get_bytes("hihi", password), b"how are you")
        self.assertEqual(self.cipher_kv_dao.get("hello", password), "world")
        time.sleep(1)

        self.assertEqual(self.cipher_kv_dao.get("hi", password), "how are you")
        self.cipher_kv_dao.delete("hi")
        self.assertEqual(self.cipher_kv_dao.get("hi", password), None)
