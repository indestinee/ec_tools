import enum
import json

from ec_tools.data import JsonType


class CustomizedJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, enum.Enum):
            return obj.name
        return json.JSONEncoder.default(self, obj)


def load_json(path: str) -> JsonType:
    with open(path, "r") as f:
        return json.load(f)


def load_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def load_binary(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()
