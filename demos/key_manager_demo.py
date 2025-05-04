import logging
import time
import unittest

from ec_tools.database import SqliteKvDao, SqliteClient, CipherKvDao
from ec_tools.tools.cipher import AesCipherGenerator
from ec_tools.tools.key_manager import KeyManager

logging.basicConfig(level=logging.DEBUG)


class KeyManagerTest:
    sqlite_client = SqliteClient(":memory:")
    kv_dao = SqliteKvDao(sqlite_client)
    cipher_generator = AesCipherGenerator()
    cipher_kv_dao = CipherKvDao(kv_dao, cipher_generator)
    manager = KeyManager(cipher_kv_dao, "12345678", hint_function=lambda: print("hi"))

    def test(self):
        print(self.manager.get_keys(["a", "b", "c"]))
        print(self.manager.get_key("a"))
        print(self.manager.get_key("d"))


def test():
    KeyManagerTest().test()


if __name__ == "__main__":
    test()
