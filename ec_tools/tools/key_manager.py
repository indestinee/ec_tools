import dataclasses
import threading
from typing import Callable, Dict, List, Optional

from ec_tools.database import CipherKvDao


def _collect_user_input(field: str, retries: int = 10) -> str:
    for _ in range(retries):
        try:
            value = input(f"Enter field {field}: ")
            value = value.strip()
            if not value:
                continue
            return value
        except Exception:
            continue
    raise RuntimeError(f"Failed to input {field}")


@dataclasses.dataclass
class KeyManager:
    cipher_kv_dao: CipherKvDao
    password: str

    lock = threading.Lock()
    expiration_time: float = 1000 * 365 * 86400
    hint_function: Optional[Callable] = None

    def get_key(self, key: str) -> str:
        with self.lock:
            return self.cipher_kv_dao.get(key, self.password)

    def get_keys(self, keys: List[str]) -> Dict[str, str]:
        result = self._get_keys(keys)
        missing_keys = [key for key in keys if result.get(key, None) is None]
        if missing_keys:
            if self.hint_function:
                self.hint_function()
            self.refresh_keys(keys)
        return self._get_keys(keys)

    def refresh_keys(self, keys: List[str]):
        for key in keys:
            self._collect(key)

    def _collect(self, field: str) -> str:
        with self.lock:
            value = _collect_user_input(field)
            self.cipher_kv_dao.set(field, self.password, value, self.expiration_time)
            return value

    def _get_keys(self, keys: List[str]) -> Dict[str, Optional[str]]:
        return {k: self.cipher_kv_dao.get(k, self.password) for k in keys}
