from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class RetryAttempt:
    attempt_id: str
    artifact_id: str
    branch_id: str
    parent_artifact_id: Optional[str]
    evidence_id: str
    decision_state: str
    fingerprint: str
    retry_count: int = 0
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    artifact_hash: str = ""
    evidence_version: str = ""


__all__ = ["RetryAttempt"]
