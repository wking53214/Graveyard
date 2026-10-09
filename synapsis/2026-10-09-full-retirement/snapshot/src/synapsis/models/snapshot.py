from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

@dataclass
class Snapshot:
    name: str
    created_at: datetime
    data: Dict[str, Any]
