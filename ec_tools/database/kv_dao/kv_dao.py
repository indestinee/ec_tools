import abc
from typing import Any, List

ONE_THOUSAND_YEAR = 86400 * 365 * 1000


class KvDao(abc.ABC):
    _default_duration: float

    def __init__(self, default_duration: float = ONE_THOUSAND_YEAR):
        self._default_duration = default_duration

    def get(self, key: str, default: Any = None) -> Any:
        return self._get(key) or default

    def set(self, key: str, value: str, duration: float = None) -> None:
        self._set(key, value, duration or self._default_duration)

    def keys(self) -> List[str]: ...

    @abc.abstractmethod
    def delete(self, key: str) -> None: ...

    @abc.abstractmethod
    def clear(self) -> None: ...

    @abc.abstractmethod
    def _get(self, key: str) -> Any: ...

    @abc.abstractmethod
    def _set(self, key: str, value: str, duration: float) -> None: ...

    def __getitem__(self, key: str) -> Any:
        return self._get(key)

    def __contains__(self, key: str) -> bool:
        return self._get(key) is not None
