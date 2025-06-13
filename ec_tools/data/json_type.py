from typing import Union, List, Dict, TypeAlias

JsonType: TypeAlias = Union[
    None, int, str, bool, float, List["JsonType"], Dict[str, "JsonType"]
]
