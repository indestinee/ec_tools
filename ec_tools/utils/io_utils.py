import json
import os
from io import TextIOWrapper
from typing import Generator, List

from ec_tools.data import CustomizedJsonEncoder, JsonType


def chunk_read_file(fp: TextIOWrapper, chunk_size: int = 1024 * 1024) -> Generator[str, None, None]:
    while True:
        chunk = fp.read(chunk_size)
        if not chunk:
            break
        yield chunk


def load_json(path: str, default: JsonType = None, encoding: str = "utf-8") -> JsonType:
    if os.path.isfile(path):
        with open(path, "r", encoding=encoding) as f:
            return json.load(f)
    if default is not None:
        return default
    raise IOError(f"no such file {path}")


def load_file(path: str, encoding: str = "utf-8") -> str:
    with open(path, "r", encoding=encoding) as f:
        return f.read()


def load_binary(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def load_file_by_lines(path: str, encoding: str = "utf-8") -> List[str]:
    with open(path, "r", encoding=encoding) as f:
        rows = [row.strip() for row in f.readlines()]
        return [row for row in rows if row]


def touch_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def dump_json(data: JsonType, path: str, encoding: str = "utf-8"):
    with open(path, "w", encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=False, indent=2, cls=CustomizedJsonEncoder)


def dump_binary(data: bytes, path: str):
    with open(path, "wb") as f:
        f.write(data)


def dump_file(data: str, path: str, encoding: str = "utf-8"):
    with open(path, "w", encoding=encoding) as f:
        f.write(data)
