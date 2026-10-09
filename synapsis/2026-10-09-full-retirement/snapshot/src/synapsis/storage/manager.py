from pathlib import Path
from typing import Any, Dict

from synapsis.storage.filesystem_backend import FilesystemStorageBackend
from synapsis.config.loader import load_config

class StorageManager:

    def __init__(self):
        config = load_config("storage")
        backend_type = config.get("default_backend", "filesystem")

        if backend_type == "filesystem":
            root = Path(config.get("sqlite_path", "data/knowledge"))
            self.backend = FilesystemStorageBackend(root)
        else:
            raise ValueError(f"Unknown backend: {backend_type}")

    def write(self, key: str, data: Dict[str, Any]) -> None:
        self.backend.write(key, data)

    def read(self, key: str) -> Dict[str, Any] | None:
        return self.backend.read(key)
