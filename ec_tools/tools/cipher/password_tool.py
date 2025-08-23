import hashlib

from ec_tools.tools.cipher.cipher import SecrectKey


def generate_password(password: str, salt: str, iterations: int) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha512",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        iterations,
    )


def generate_key(password: bytes, salt: bytes, key_size: int, iv_size: int, iterations: int):
    hsh = hashlib.pbkdf2_hmac(
        "sha512",
        password,
        salt,
        iterations,
        dklen=key_size + iv_size,
    )
    return SecrectKey(
        key=hsh[:key_size],
        iv=hsh[key_size:],
        salt=salt,
    )
