from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ApprovalRecord:
    approval_id: str
    target_id: str
    reviewer: str
    decision: str
    rationale: str
    decision_id: Optional[str] = None
    lineage_hash: Optional[str] = None
    created: datetime = field(default_factory=datetime.now)
