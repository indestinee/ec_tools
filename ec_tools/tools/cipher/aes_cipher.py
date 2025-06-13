import hashlib
import os
import dataclasses

from Crypto.Cipher import AES
from ec_tools.tools.cipher.cipher import SecrectKey
from ec_tools.tools.cipher.aes_config import AesMode


@dataclasses.dataclass
class AesCipher:
    password: bytes
    aes_mode: AesMode

    def __init__(
        self,
        password: str,
        salt: str,
        iterations: int = 10000,
        aes_mode: AesMode = AesMode.AES_256_CBC,
    ):
        self.aes_mode = aes_mode
        self.password = self.generate_password(password, salt, iterations)

    def encrypt(self, plain_text: bytes) -> bytes:
        size = len(plain_text)
        data = self._augment_bytes(plain_text)
        secret_key = self.generate_key(self.password, os.urandom(32), 10)
        aes = AES.new(secret_key.key, self.aes_mode.value.mode, iv=secret_key.iv)
        cipher_text = aes.encrypt(data)
        return str(size).encode("utf-8") + b"\0" + secret_key.salt + cipher_text

    def decrypt(self, cipher_text: bytes) -> bytes:
        zero = cipher_text.index(b"\0")
        size = int(cipher_text[:zero].decode("utf-8"))
        salt = cipher_text[zero + 1 : zero + 1 + 32]
        data = cipher_text[zero + 1 + 32 :]
        secret_key = self.generate_key(self.password, salt, 10)
        aes = AES.new(secret_key.key, self.aes_mode.value.mode, iv=secret_key.iv)
        decrypted_data = aes.decrypt(data)
        return self._recover_bytes(decrypted_data, size)

    def _augment_bytes(self, data: bytes) -> bytes:
        return b"".join(
            [
                os.urandom(self.aes_mode.value.key_size),
                data,
                os.urandom(self.aes_mode.value.key_size),
                os.urandom(
                    self.aes_mode.value.key_size
                    - len(data) % self.aes_mode.value.key_size
                ),
            ]
        )

    def _recover_bytes(self, data: bytes, size: int) -> bytes:
        return data[self.aes_mode.value.key_size : self.aes_mode.value.key_size + size]

    @classmethod
    def generate_password(cls, password: str, salt: str, iterations: int) -> bytes:
        return hashlib.pbkdf2_hmac(
            "sha512",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            iterations,
        )

    def generate_key(self, password: bytes, salt: bytes, iterations: int):
        hsh = hashlib.pbkdf2_hmac(
            "sha512",
            password,
            salt,
            iterations,
            dklen=self.aes_mode.value.key_size + self.aes_mode.value.iv_size,
        )
        return SecrectKey(
            key=hsh[: self.aes_mode.value.key_size],
            iv=hsh[self.aes_mode.value.key_size :],
            salt=salt,
        )
