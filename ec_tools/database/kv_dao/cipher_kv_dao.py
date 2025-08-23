import dataclasses
from typing import List, Optional

from ec_tools.database.kv_dao.kv_dao import KvDao
from ec_tools.database.kv_dao.sqlite_kv_dao import SqliteKvDao
from ec_tools.database.sqlite_client.sqlite_client import SqliteClient
from ec_tools.tools.cipher import AesCipherGenerator, AesMode, Cipher, CipherGenerator


@dataclasses.dataclass
class CipherKvDao:
    kv_dao: KvDao
    cipher_generator: CipherGenerator

    encoding: str = "utf-8"

    @classmethod
    def create_sqlite_dao(
        cls,
        db_path: str,
        encoding: str = "utf-8",
        mode: AesMode = AesMode.AES_256_CBC,
        table_name: Optional[str] = None,
    ) -> "CipherKvDao":
        return CipherKvDao(
            SqliteKvDao(sqlite_client=SqliteClient(db_path), table_name=table_name),
            AesCipherGenerator(encoding, mode),
        )

    def get(self, key: str, password: str, default: Optional[str] = None) -> Optional[str]:
        value = self.get_bytes(key, password, default.encode(self.encoding) if default else None)
        return value.decode(self.encoding) if value else None

    def get_bytes(self, key: str, password: str, default: Optional[bytes] = None) -> Optional[bytes]:
        value = self.kv_dao.get(key)
        if value:
            return self.cipher_generator.decrypt(password.encode(self.encoding), Cipher.loads(value))
        return default

    def set(self, key: str, password: str, value: str, duration: float = None) -> None:
        return self.set_bytes(key, password, value.encode(self.encoding), duration)

    def set_bytes(self, key: str, password: str, value: bytes, duration: float = None) -> None:
        cipher = self.cipher_generator.encrypt(password.encode(self.encoding), value)
        return self.kv_dao.set(key, cipher.dumps(), duration)

    def delete(self, key: str) -> None:
        return self.kv_dao.delete(key)

    def clear(self) -> None:
        return self.kv_dao.clear()

    def keys(self) -> List[str]:
        return self.kv_dao.keys()
