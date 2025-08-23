import logging

from ec_tools.database import CipherKvDao, SqliteClient, SqliteKvDao
from ec_tools.tools.cipher import AesCipherGenerator
from ec_tools.tools.headers_manager import HeadersManager
from ec_tools.tools.key_manager import KeyManager

logging.basicConfig(level=logging.DEBUG)


class HeadersManagerTest:
    sqlite_client = SqliteClient(":memory:")
    kv_dao = SqliteKvDao(sqlite_client)
    cipher_generator = AesCipherGenerator()
    cipher_kv_dao = CipherKvDao(kv_dao, cipher_generator)
    manager = HeadersManager(
        KeyManager(cipher_kv_dao, "12345678", hint_function=lambda: print("hi")),
        ["cookies", "auth"],
        {"a": "c"},
    )

    def test(self):
        print(self.manager.get())
        print(self.manager.get())


def test():
    HeadersManagerTest().test()


if __name__ == "__main__":
    test()
