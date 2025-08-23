import os

from ec_tools.tools.cipher.aes_config import AesMode
from ec_tools.tools.cipher.chunk_config import ChunkConfig
from ec_tools.tools.cipher.chunk_encryption_utils import decrypt_by_chunk, encrypt_by_chunk
from ec_tools.utils.io_utils import chunk_read_file


def encrypt_file(
    input_file: str,
    output_file: str,
    password: str,
    aes_mode: AesMode = AesMode.AES_256_CBC,
    iterations: int = 10000,
    chunk_size: int = 1024 * 1024,
):
    assert chunk_size % aes_mode.value.key_size == 0, "Chunk size must be a multiple of the AES key size."
    salt = os.urandom(32)
    file_size = os.path.getsize(input_file)
    outf = open(output_file, "wb")
    inf = open(input_file, "rb")
    chunk_config = ChunkConfig(
        salt=salt, aes_mode=aes_mode, iterations=iterations, chunk_size=chunk_size, file_size=file_size
    )
    outf.write(chunk_config.to_json_bytes() + b"\n")
    input_generator = chunk_read_file(inf, chunk_size)
    for encrypt_chunk in encrypt_by_chunk(input_generator, password, salt, aes_mode, iterations):
        outf.write(encrypt_chunk)
        outf.flush()
    inf.close()
    outf.close()


def decrypt_file(input_file: str, output_file: str, password: str):
    inf = open(input_file, "rb")
    outf = open(output_file, "wb")
    header = inf.readline().decode("utf-8").strip()
    chunk_config = ChunkConfig.from_json(header)
    chunk_generator = chunk_read_file(inf, chunk_config.chunk_size + chunk_config.aes_mode.value.key_size * 2)
    for decrypted_chunk in decrypt_by_chunk(chunk_generator, password, chunk_config):
        outf.write(decrypted_chunk)
        outf.flush()
    outf.close()
    inf.close()
