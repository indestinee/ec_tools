import json
import os
import hashlib
import dataclasses
import abc
from Crypto.Cipher import AES

from ec_tools.utils.hash_utils import hmac_sha256


@dataclasses.dataclass
class Cipher:
    cipher_text: str
    mode: str
    salt: str

    def dumps(self) -> str:
        return json.dumps(dataclasses.asdict(self))

    @classmethod
    def loads(self, text: str) -> "Cipher":
        return Cipher(**json.loads(text))


@dataclasses.dataclass
class SecrectKey:
    key: bytes
    iv: bytes
    salt: bytes

    def __str__(self) -> str:
        return f"SecretKey(key={len(self.key)},iv={len(self.iv)},salt={len(self.salt)})"

    def __repr__(self) -> str:
        return str(self)


@dataclasses.dataclass
class CipherGenerator(abc.ABC):
    encoding: str = "utf-8"

    @abc.abstractmethod
    def decrypt(self, password: bytes, cipher: Cipher) -> bytes: ...

    @abc.abstractmethod
    def encrypt(self, password: bytes, plain_text: bytes) -> Cipher: ...

    def decrypt_str(self, password: str, cipher: Cipher) -> str:
        return self.decrypt(password.encode(self.encoding), cipher).decode("utf-8")

    def encrypt_str(self, password: str, text: str) -> Cipher:
        return self.encrypt(
            password=password.encode(self.encoding),
            plain_text=text.encode(self.encoding),
        )
