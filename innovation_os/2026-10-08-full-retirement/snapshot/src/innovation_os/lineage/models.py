from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class LineageRecord:
    artifact_id: str
    canonical_hash: str
    parent_artifact_id: Optional[str] = None
    parent_hash: Optional[str] = None
    branch_id: Optional[str] = None
    lineage_hash: Optional[str] = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    version: int = 1
    provenance_status: Optional[str] = None


@dataclass
class LineageEvent:
    sequence: int
    event_type: str
    subject_id: str
    payload: dict
    previous_hash: Optional[str]
    event_hash: str
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


__all__ = ["LineageRecord", "LineageEvent"]
