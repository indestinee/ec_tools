import abc
import dataclasses

from ec_tools.tools.cipher.cipher import Cipher


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
