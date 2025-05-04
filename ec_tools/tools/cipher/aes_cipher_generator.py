import json
import os
import hashlib
import dataclasses
import enum
from Crypto.Cipher import AES

from ec_tools.utils.hash_utils import hmac_sha256
from ec_tools.tools.cipher.cipher_generator import Cipher, CipherGenerator, SecrectKey


@dataclasses.dataclass
class AesConfig:
    key_size: int
    iv_size: int
    mode: int


class AesMode(enum.Enum):
    AES_128_CBC = AesConfig(16, 16, AES.MODE_CBC)
    AES_192_CBC = AesConfig(24, 16, AES.MODE_CBC)
    AES_256_CBC = AesConfig(32, 16, AES.MODE_CBC)


@dataclasses.dataclass
class AesCipherGenerator(CipherGenerator):
    mode: AesMode = AesMode.AES_256_CBC
    pbkdf2_iterations: int = 10000
    _DIVIDER = b"\0"

    def decrypt(self, password: bytes, cipher: Cipher) -> bytes:
        salt = bytes.fromhex(cipher.salt)
        secrect_key = self._generate_key(password, salt)
        aes = AES.new(secrect_key.key, self.mode.value.mode, iv=secrect_key.iv)
        augmented_text = aes.decrypt(bytes.fromhex(cipher.cipher_text))
        decoded = bytes.fromhex(augmented_text.hex()[::2])
        divider_index = decoded.find(self._DIVIDER)
        assert divider_index != -1, "invalid cipher: divider not found"
        text_length = int(decoded[:divider_index].decode(self.encoding))
        data = decoded[divider_index + len(self._DIVIDER) :]
        return data[:text_length]

    def encrypt(self, password: bytes, plain_text: bytes) -> Cipher:
        secrect_key = self._generate_key(password, os.urandom(self.mode.value.key_size))
        text_length = len(plain_text)
        plain_text = str(text_length).encode(self.encoding) + self._DIVIDER + plain_text
        augmented_text = self._augment_bytes(plain_text, self.mode.value.key_size)
        aes = AES.new(secrect_key.key, self.mode.value.mode, iv=secrect_key.iv)
        cipher_text = aes.encrypt(augmented_text)
        return Cipher(
            cipher_text=cipher_text.hex(),
            salt=secrect_key.salt.hex(),
            mode=self.mode.name,
        )

    @classmethod
    def _augment_bytes(self, data: bytes, padding_size: int) -> bytes:
        padded_text = (data + os.urandom(padding_size - len(data) % padding_size)).hex()
        random_bytes = os.urandom(len(padded_text)).hex()
        mixture = bytes.fromhex("".join(map("".join, zip(padded_text, random_bytes))))
        return mixture

    def _generate_key(self, password: bytes, salt: bytes):
        hsh = hashlib.pbkdf2_hmac(
            "sha512",
            password,
            salt,
            self.pbkdf2_iterations,
            dklen=self.mode.value.key_size + self.mode.value.iv_size,
        )
        return SecrectKey(
            key=hsh[: self.mode.value.key_size],
            iv=hsh[self.mode.value.key_size :],
            salt=salt,
        )
