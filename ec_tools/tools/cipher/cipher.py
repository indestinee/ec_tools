import dataclasses
import json


@dataclasses.dataclass
class Cipher:
    cipher_text: str
    mode: str
    salt: str

    def dumps(self) -> str:
        return json.dumps(dataclasses.asdict(self))

    @classmethod
    def loads(cls, text: str) -> "Cipher":
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
