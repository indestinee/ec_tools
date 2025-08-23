import os
from typing import Generator

from Crypto.Cipher import AES

from ec_tools.tools.cipher import password_tool
from ec_tools.tools.cipher.aes_config import AesMode
from ec_tools.tools.cipher.chunk_config import ChunkConfig
from ec_tools.tools.cipher.cipher import SecrectKey


def padding_chunk(chunk: bytes, block_size: int) -> bytes:
    pad_size = (block_size - (len(chunk) % block_size)) % block_size
    return chunk + os.urandom(pad_size)


def encrypt_by_chunk(
    chunk_generator: Generator[bytes, None, None],
    password: str,
    salt: str,
    aes_mode: AesMode = AesMode.AES_256_CBC,
    interations: int = 10000,
) -> Generator[bytes, None, None]:
    secret_key: SecrectKey = password_tool.generate_key(
        password=password.encode("utf-8"),
        salt=salt,
        key_size=aes_mode.value.key_size,
        iv_size=aes_mode.value.iv_size,
        iterations=interations,
    )
    aes = AES.new(secret_key.key, aes_mode.value.mode, iv=secret_key.iv)
    for chunk in chunk_generator:
        chunk = padding_chunk(chunk, aes_mode.value.key_size)
        chunk = os.urandom(aes_mode.value.key_size) + chunk + os.urandom(aes_mode.value.key_size)
        encrypted_chunk = aes.encrypt(chunk)
        yield encrypted_chunk


def decrypt_by_chunk(
    chunk_generator: Generator[bytes, None, None],
    password: str,
    chunk_config: ChunkConfig,
) -> Generator[bytes, None, None]:
    secret_key: SecrectKey = password_tool.generate_key(
        password=password.encode("utf-8"),
        salt=chunk_config.salt,
        key_size=chunk_config.aes_mode.value.key_size,
        iv_size=chunk_config.aes_mode.value.iv_size,
        iterations=chunk_config.iterations,
    )
    aes = AES.new(secret_key.key, chunk_config.aes_mode.value.mode, iv=secret_key.iv)
    total_read = 0
    for chunk in chunk_generator:
        if total_read == chunk_config.file_size:
            raise Exception("File size mismatch, decryption may be incorrect.")
        decrypted_chunk = aes.decrypt(chunk)
        decrypted_chunk = decrypted_chunk[
            chunk_config.aes_mode.value.key_size : len(decrypted_chunk) - chunk_config.aes_mode.value.key_size
        ]
        total_read += len(decrypted_chunk)
        if total_read > chunk_config.file_size:
            trip_size = total_read - chunk_config.file_size
            total_read -= trip_size
            decrypted_chunk = decrypted_chunk[:-trip_size]
        yield decrypted_chunk
