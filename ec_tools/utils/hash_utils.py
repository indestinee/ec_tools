import hashlib
import hmac


def hmac_sha256(key: bytes, value: bytes) -> bytes:
    sha256 = hmac.new(key, value, hashlib.sha256)
    return sha256.digest()


def hmac_sha256_text(key: str, value: str, encoding="utf-8") -> str:
    return hmac_sha256(key.encode(encoding), value.encode(encoding)).hex()


def hmac_md5_text(key: str, value: str, encoding="utf-8") -> str:
    return hmac.new(
        key.encode(encoding=encoding), value.encode(encoding=encoding), hashlib.md5
    ).hexdigest()
