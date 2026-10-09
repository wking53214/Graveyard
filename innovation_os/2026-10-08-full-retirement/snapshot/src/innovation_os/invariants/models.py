from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass
class InvariantViolation:
    violation_id: str
    subject_type: str
    subject_id: str
    rule_name: str
    context: Dict[str, Any]
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    severity: str = "error"


__all__ = ["InvariantViolation"]
