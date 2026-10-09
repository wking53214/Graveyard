from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any

@dataclass
class Report:
    name: str
    created_at: datetime
    sections: Dict[str, Any]
