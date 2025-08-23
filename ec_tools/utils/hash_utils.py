import hashlib
import hmac


def hmac_sha256(key: bytes, value: bytes) -> bytes:
    sha256 = hmac.new(key, value, hashlib.sha256)
    return sha256.digest()


def hmac_sha256_text(key: str, value: str, encoding="utf-8") -> str:
    return hmac_sha256(key.encode(encoding), value.encode(encoding)).hex()


def hmac_md5_text(key: str, value: str, encoding="utf-8") -> str:
    return hmac.new(key.encode(encoding=encoding), value.encode(encoding=encoding), hashlib.md5).hexdigest()


def calc_md5(file_path: str, batch_size: int = 8192) -> str:
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(batch_size):
            hasher.update(chunk)
    return hasher.hexdigest()
