from typing import Dict, List, TypeAlias, Union

JsonType: TypeAlias = Union[None, int, str, bool, float, List["JsonType"], Dict[str, "JsonType"]]
