from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Decision:
    decision_id: str
    problem_id: str
    context: str
    options: List[str]
    selected_option: str
    rejected_options: List[str]
    assumptions: List[str]
    confidence: float
    approval: str
    alternatives: List[str] = field(default_factory=list)
    state: str = "CURRENT"
    current: bool = True
    lineage_hash: Optional[str] = None
    branch_id: Optional[str] = None
    created: datetime = field(default_factory=datetime.now)
