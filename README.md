# ec_tools

A lightweight Python toolbox for data modeling, SQLite DAOs, encrypted key-value storage, and small productivity utilities.

## Highlights
- Data objects with JSON serialization and type-aware formatting.
- SQLite client + DAO layer with query generation.
- KV DAO with optional AES-backed encryption.
- Encryption helpers for bytes, chunks, and files.
- Utility helpers for IO, hashing, logging, and timing.

## Requirements
- Python >= 3.12

## Install (from source)
```bash
pip install -e .
```

## Quick start
### Encrypted KV storage with a KeyManager
```python
from ec_tools.database import CipherKvDao, SqliteClient, SqliteKvDao
from ec_tools.tools.cipher import AesCipherGenerator
from ec_tools.tools.key_manager import KeyManager

sqlite_client = SqliteClient(":memory:")
kv_dao = SqliteKvDao(sqlite_client)
cipher_generator = AesCipherGenerator()
cipher_kv_dao = CipherKvDao(kv_dao, cipher_generator)

manager = KeyManager(cipher_kv_dao, "my-password")
manager.refresh_keys(["token", "cookie"])
print(manager.get_key("token"))
```

### Build headers from stored secrets
```python
from ec_tools.tools.headers_manager import HeadersManager

headers = HeadersManager(manager, ["token"], {"User-Agent": "ec-tools"}).get()
print(headers)
```

## Data objects
Define dataclasses that serialize to/from JSON with helpers for enums, lists, sets, and nested objects.
```python
import dataclasses
from ec_tools.data import DataObject

@dataclasses.dataclass
class User(DataObject):
    name: str
    age: int

user = User.from_json({"name": "Ada", "age": "42"})
print(user.to_json())
```

## Encryption helpers
- `AesCipher` for encrypting/decrypting bytes.
- Chunked and file-level encryption utilities in `ec_tools.tools.cipher`.

## Project layout
- `ec_tools/data`: data-object helpers and JSON formatting.
- `ec_tools/database`: SQLite client, DAO, and KV DAO.
- `ec_tools/tools`: key/headers managers, cipher tools, thread pool.
- `ec_tools/utils`: IO, hashing, logging, and timing helpers.

## Development
```bash
pytest
```

## License
MIT
