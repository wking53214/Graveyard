"""
Core record types.

The vocabulary here is deliberately neutral -- ALPHA/BETA/GAMMA rather than
"fine"/"annoyed"/"furious". That was a choice in the original engine, and it is
kept: the categories describe how far an interaction deviates from the
operational baseline, not how a customer feels. Nothing here infers emotion,
and a category is not a judgement about the person on either end of the call.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

__all__ = [
    "CategoryType",
    "AllocationLevel",
    "InteractionRecord",
    "EvaluatedRecord",
]


class CategoryType(Enum):
    """How far an interaction sits from the expected baseline."""

    ALPHA = "alpha"      # within normal range
    BETA = "beta"        # elevated friction, worth watching
    GAMMA = "gamma"      # substantial deviation, worth acting on


class AllocationLevel(Enum):
    """Escalation tiers a directive can call for."""

    STAGE_FIRST = 1      # handle in the normal queue
    STAGE_SECONDARY = 2  # targeted analysis of the process
    STAGE_SYSTEM = 3     # systemic review


@dataclass(frozen=True)
class InteractionRecord:
    """One completed customer interaction.

    `routing_count` is how many times the interaction was handed to a
    different processor. It is the strongest friction signal in the model:
    being passed around costs a caller more than simply waiting.
    """

    record_id: str
    source_id: str
    processor_id: str
    content_text: str
    duration_seconds: int
    routing_count: int
    completion_status: bool


@dataclass(frozen=True)
class EvaluatedRecord:
    """An interaction plus the category the evaluator assigned it."""

    record: InteractionRecord
    category: CategoryType
    friction_score: float
    evaluation_metadata: str

    @property
    def record_id(self) -> str:
        return self.record.record_id
