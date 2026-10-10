"""
Routing the next interaction.

Two competing pulls: send work to whoever is least loaded, or send it to
whoever has dealt with this customer before. The original engine weighted
continuity at 0.7 against capacity at 0.3, so history wins unless nobody has
any -- a defensible choice, since re-explaining a problem to a new person is
most of what makes an interaction go badly.

Those weights are the whole policy of the module, so they are named and
configurable rather than inline literals.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping, Optional, Sequence

__all__ = ["AllocationConfig", "DEFAULT_ALLOCATION", "ResourceAllocator"]


@dataclass(frozen=True)
class AllocationConfig:
    """How capacity and continuity trade off."""

    capacity_weight: float = 0.3
    history_weight: float = 0.7


DEFAULT_ALLOCATION = AllocationConfig()


class ResourceAllocator:
    """Scores processors for suitability, highest score wins."""

    def __init__(self, config: AllocationConfig = DEFAULT_ALLOCATION):
        self.config = config

    def calculate_priority(
        self,
        workload_distribution: Mapping[str, int],
        interaction_history: Mapping[str, Sequence[str]],
        target_source_id: str,
    ) -> Dict[str, float]:
        """Score every processor. Load is inverted so lighter load scores higher;
        negative loads are clamped to zero rather than producing a score above 1."""
        scores: Dict[str, float] = {}
        for processor_id, load_count in workload_distribution.items():
            capacity_coefficient = 1.0 / (1.0 + float(max(0, load_count)))
            has_history = target_source_id in interaction_history.get(processor_id, ())
            history_coefficient = 1.0 if has_history else 0.0
            scores[processor_id] = (
                capacity_coefficient * self.config.capacity_weight
                + history_coefficient * self.config.history_weight
            )
        return scores

    def select_processor(
        self,
        workload_distribution: Mapping[str, int],
        interaction_history: Mapping[str, Sequence[str]],
        target_source_id: str,
    ) -> Optional[str]:
        """The actual routing decision. Ties break on processor id so the
        choice is deterministic rather than dict-order dependent. Returns None
        when there is nobody to route to."""
        scores = self.calculate_priority(
            workload_distribution, interaction_history, target_source_id
        )
        if not scores:
            return None
        return min(scores.items(), key=lambda kv: (-kv[1], kv[0]))[0]
