import copy
import dataclasses
from typing import Dict, List

from ec_tools.tools.key_manager import KeyManager


@dataclasses.dataclass
class HeadersManager:
    key_manager: KeyManager
    stored_keys: List[str]

    default_headers_template: Dict[str, str] = dataclasses.field(default_factory=dict)

    def get(self):
        headers = copy.deepcopy(self.default_headers_template)
        headers.update(self.key_manager.get_keys(self.stored_keys))
        return headers

    def refresh(self):
        return self.key_manager.refresh_keys(self.stored_keys)
