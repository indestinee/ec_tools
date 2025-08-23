import dataclasses
import enum

from Crypto.Cipher import AES


@dataclasses.dataclass
class AesConfig:
    key_size: int
    iv_size: int
    mode: int


class AesMode(enum.Enum):
    AES_128_CBC = AesConfig(16, 16, AES.MODE_CBC)
    AES_192_CBC = AesConfig(24, 16, AES.MODE_CBC)
    AES_256_CBC = AesConfig(32, 16, AES.MODE_CBC)
