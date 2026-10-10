"""
Aggregation and directives.

A review group collects evaluated interactions and answers one question: does
this batch need somebody's attention, and at what level?

The directive rule is intentionally blunt and intentionally asymmetric. A
single GAMMA escalates the whole batch, while BETA needs to clear a count
threshold. That is a deliberate bias toward surfacing the severe-and-rare over
the moderate-and-common, and it is the kind of rule that should be visible and
tunable rather than buried in an if-chain -- which is where it lived in the
original engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping

from .records import AllocationLevel, CategoryType, EvaluatedRecord

__all__ = ["DirectiveConfig", "DEFAULT_DIRECTIVE", "Directive", "ReviewGroup"]


@dataclass(frozen=True)
class DirectiveConfig:
    """When a batch escalates."""

    gamma_escalation_count: int = 1   # this many GAMMA triggers systemic review
    beta_escalation_count: int = 3    # this many BETA triggers process analysis


DEFAULT_DIRECTIVE = DirectiveConfig()


@dataclass(frozen=True)
class Directive:
    """What the batch calls for, and why."""

    level: AllocationLevel
    text: str
    reason: str


class ReviewGroup:
    """Collects evaluated records for one team and compiles their metrics."""

    def __init__(
        self,
        group_id: str,
        participant_identifiers: Iterable[str],
        config: DirectiveConfig = DEFAULT_DIRECTIVE,
    ):
        self.group_id = group_id
        self.participant_identifiers: List[str] = list(participant_identifiers)
        self.config = config
        self.processed_collection: List[EvaluatedRecord] = []

    def add_record(self, evaluated_item: EvaluatedRecord) -> None:
        self.processed_collection.append(evaluated_item)

    def extend(self, evaluated_items: Iterable[EvaluatedRecord]) -> None:
        self.processed_collection.extend(evaluated_items)

    def category_counts(self) -> Dict[CategoryType, int]:
        counts = {category: 0 for category in CategoryType}
        for item in self.processed_collection:
            counts[item.category] += 1
        return counts

    def determine_directive(self, counts: Mapping[CategoryType, int]) -> Directive:
        gamma = counts[CategoryType.GAMMA]
        beta = counts[CategoryType.BETA]

        if gamma >= self.config.gamma_escalation_count:
            return Directive(
                level=AllocationLevel.STAGE_SYSTEM,
                text="Escalate to systemic review assembly",
                reason=f"{gamma} record(s) in GAMMA",
            )
        if beta >= self.config.beta_escalation_count:
            return Directive(
                level=AllocationLevel.STAGE_SECONDARY,
                text="Initiate targeted process analysis sequence",
                reason=f"{beta} record(s) in BETA",
            )
        return Directive(
            level=AllocationLevel.STAGE_FIRST,
            text="Maintain current baseline monitoring protocols",
            reason="no category crossed its escalation threshold",
        )

    def compile_metrics(self) -> Dict[str, Any]:
        """Batch summary. An empty group reports `empty` rather than a clean
        bill of health -- no evidence is not the same as no problem."""
        if not self.processed_collection:
            return {"group_id": self.group_id, "status": "empty"}

        counts = self.category_counts()
        directive = self.determine_directive(counts)
        return {
            "group_id": self.group_id,
            "count_alpha": counts[CategoryType.ALPHA],
            "count_beta": counts[CategoryType.BETA],
            "count_gamma": counts[CategoryType.GAMMA],
            "action_directive": directive.text,
            "action_level": directive.level.name,
            "action_reason": directive.reason,
        }
