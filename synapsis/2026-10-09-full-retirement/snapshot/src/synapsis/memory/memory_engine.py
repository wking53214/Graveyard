from datetime import datetime
from typing import Dict, Any

from synapsis.storage.manager import StorageManager

class MemoryEngine:

    def __init__(self):
        self.storage = StorageManager()

    def save(self, key: str, data: Dict[str, Any]) -> None:
        payload = {
            "saved_at": datetime.now().isoformat(),
            "data": data
        }
        self.storage.write(key, payload)

    def load(self, key: str) -> Dict[str, Any] | None:
        return self.storage.read(key)

    def list(self) -> Dict[str, Any]:
        # Filesystem backend stores JSON files under a directory.
        # We expose a simple list of keys.
        root = self.storage.backend.root
        return [p.stem for p in root.glob("*.json")]
