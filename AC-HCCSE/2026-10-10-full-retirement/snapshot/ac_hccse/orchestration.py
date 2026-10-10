"""
The pipeline, wired together.

Evaluate a batch, compile it into a directive, and decide where the next
interaction should go. Each stage is usable on its own; this is the
convenience path that runs them in order.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

from .allocation import DEFAULT_ALLOCATION, AllocationConfig, ResourceAllocator
from .records import EvaluatedRecord, InteractionRecord
from .review import DEFAULT_DIRECTIVE, DirectiveConfig, ReviewGroup
from .sampling import DataSampler
from .scoring import DEFAULT_SCORING, RecordEvaluator, ScoringConfig

__all__ = ["OrchestrationSystem"]


class OrchestrationSystem:
    """Coordinates evaluation, aggregation, allocation and sampling."""

    def __init__(
        self,
        scoring: ScoringConfig = DEFAULT_SCORING,
        allocation: AllocationConfig = DEFAULT_ALLOCATION,
        directive: DirectiveConfig = DEFAULT_DIRECTIVE,
        sample_seed: Optional[int] = None,
    ):
        self.evaluator = RecordEvaluator(scoring)
        self.allocator = ResourceAllocator(allocation)
        self.sampler = DataSampler(sample_seed)
        self.directive_config = directive

    def process_records(
        self, records: Iterable[InteractionRecord]
    ) -> List[EvaluatedRecord]:
        return [self.evaluator.evaluate(item) for item in records]

    def new_group(self, group_id: str, participants: Iterable[str]) -> ReviewGroup:
        """A review group already carrying this system's directive config."""
        return ReviewGroup(group_id, participants, self.directive_config)

    def execute_group_compilation(
        self, review_group: ReviewGroup, evaluated_items: Iterable[EvaluatedRecord]
    ) -> Dict[str, Any]:
        review_group.extend(evaluated_items)
        return review_group.compile_metrics()

    def route_next(
        self,
        workload_distribution: Mapping[str, int],
        interaction_history: Mapping[str, Sequence[str]],
        target_source_id: str,
    ) -> Optional[str]:
        return self.allocator.select_processor(
            workload_distribution, interaction_history, target_source_id
        )

    def retrieve_sample(
        self, records: Sequence[InteractionRecord], sample_size: int = 1
    ) -> List[InteractionRecord]:
        return self.sampler.extract_subset(records, sample_size)
