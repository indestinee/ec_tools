import dataclasses
import json
from typing import Dict

from ec_tools.tools.cipher.aes_config import AesMode


@dataclasses.dataclass
class ChunkConfig:
    salt: bytes
    aes_mode: AesMode
    iterations: int
    chunk_size: int
    file_size: int

    def to_json(self) -> Dict[str, str]:
        return {
            "salt": self.salt.hex(),
            "mode": self.aes_mode.name,
            "iterations": self.iterations,
            "chunk_size": self.chunk_size,
            "file_size": self.file_size,
        }

    def to_json_bytes(self) -> bytes:
        return json.dumps(self.to_json()).encode("utf-8")

    @classmethod
    def from_json(cls, json_str: str) -> "ChunkConfig":
        data = json.loads(json_str)
        return cls(
            salt=bytes.fromhex(data["salt"]),
            aes_mode=AesMode[data["mode"]],
            iterations=data["iterations"],
            chunk_size=data["chunk_size"],
            file_size=data["file_size"],
        )
