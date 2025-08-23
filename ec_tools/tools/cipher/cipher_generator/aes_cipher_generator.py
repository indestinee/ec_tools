import dataclasses
import os

from Crypto.Cipher import AES

from ec_tools.tools.cipher import password_tool
from ec_tools.tools.cipher.aes_config import AesMode
from ec_tools.tools.cipher.cipher import Cipher
from ec_tools.tools.cipher.cipher_generator.cipher_generator import CipherGenerator


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
    def _augment_bytes(cls, data: bytes, padding_size: int) -> bytes:
        padded_text = (data + os.urandom(padding_size - len(data) % padding_size)).hex()
        random_bytes = os.urandom(len(padded_text)).hex()
        mixture = bytes.fromhex("".join(map("".join, zip(padded_text, random_bytes))))
        return mixture

    def _generate_key(self, password: bytes, salt: bytes):
        return password_tool.generate_key(
            password,
            salt,
            self.mode.value.key_size,
            self.mode.value.iv_size,
            self.pbkdf2_iterations,
        )
