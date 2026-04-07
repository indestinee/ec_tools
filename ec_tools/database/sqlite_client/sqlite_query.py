import dataclasses
from typing import Any, List


@dataclasses.dataclass
class SqliteQuery:
    sql: str
    args: List[Any] = dataclasses.field(default_factory=list)

    def __init__(self, *sqls: str, args: List[Any] = None):
        self.sql = "\n".join(sqls)
        self.args = list(args) if args is not None else []

    def __str__(self) -> str:
        sql = self.sql.replace("\n", " ").replace("  ", " ")
        return f"{sql}; args={self.args}" if self.args else sql

    def __repr__(self) -> str:
        return str(self)
