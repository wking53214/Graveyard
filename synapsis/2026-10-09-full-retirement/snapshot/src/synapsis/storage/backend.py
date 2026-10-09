from abc import ABC, abstractmethod
from typing import Any, Dict

class StorageBackend(ABC):

    @abstractmethod
    def write(self, key: str, data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def read(self, key: str) -> Dict[str, Any] | None:
        pass
