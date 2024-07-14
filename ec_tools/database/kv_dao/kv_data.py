import dataclasses
from typing import List

from ec_tools.database.sqlite_dao.sqlite_data_object import SqliteDataObject


@dataclasses.dataclass
class KvData(SqliteDataObject):
    key: str
    value: str
    expired_at: float = None

    @classmethod
    def primary_keys(cls) -> List[str]:
        return ["key", "expired_at"]

    @classmethod
    def unique_keys(cls) -> List[List[str]]:
        return [["key"]]
