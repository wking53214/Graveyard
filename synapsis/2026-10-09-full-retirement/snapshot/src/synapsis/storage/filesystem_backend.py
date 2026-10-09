from pathlib import Path
import json
from typing import Any, Dict
from synapsis.storage.backend import StorageBackend

class FilesystemStorageBackend(StorageBackend):

    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        return self.root / f"{key}.json"

    def write(self, key: str, data: Dict[str, Any]) -> None:
        path = self._path(key)
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def read(self, key: str) -> Dict[str, Any] | None:
        path = self._path(key)
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
