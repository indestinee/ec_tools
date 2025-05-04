import abc
import dataclasses
import time
from typing import List

from ec_tools.data.data_object import DataObject


@dataclasses.dataclass
class SqliteDataObject(abc.ABC, DataObject):
    """
    - primary_keys: define the primary keys of the object
    - extra_indexes: append extra indexes with default index (primary keys)
    - unique_keys: append extra unique constraints with default unique constraint (primary keys)
    - use _load__xxx to override loading json field to class field
    - use _dump__xxx to override dumping class field to json field
    """

    created_at: float = dataclasses.field(default_factory=time.time, kw_only=True)
    updated_at: float = dataclasses.field(default_factory=time.time, kw_only=True)

    @classmethod
    @abc.abstractmethod
    def primary_keys(cls) -> List[str]: ...

    @classmethod
    def extra_indexes(cls) -> List[List[str]]:
        return []

    @classmethod
    def unique_keys(cls) -> List[List[str]]:
        return []

    @classmethod
    def table_name(cls) -> str:
        return cls.__name__
