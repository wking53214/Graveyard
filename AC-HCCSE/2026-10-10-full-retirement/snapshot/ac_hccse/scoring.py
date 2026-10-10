"""
Friction scoring.

The score is dimensionless on purpose. Duration is divided by a baseline
rather than used raw, so a 900-second call is not automatically "worse" than
four transfers -- the two signals are put on a comparable scale first and then
added. Without that, whichever quantity happened to have larger units would
dominate the category assignment.

Every weight and threshold is configurable. In the original engine they were
literals scattered through the method body, which made the scoring model
impossible to tune or to state plainly. `DEFAULT_SCORING` reproduces those
original values exactly.
"""

from __future__ import annotations

from dataclasses import dataclass

from .records import CategoryType, EvaluatedRecord, InteractionRecord

__all__ = ["ScoringConfig", "DEFAULT_SCORING", "RecordEvaluator"]


@dataclass(frozen=True)
class ScoringConfig:
    """Weights and cut points for friction scoring.

    `baseline_duration_seconds` is what a normal interaction is expected to
    take. It is clamped to at least 1.0 at use so a misconfigured zero cannot
    divide by zero.
    """

    baseline_duration_seconds: float = 300.0
    routing_weight: float = 0.5
    beta_threshold: float = 1.2
    gamma_threshold: float = 3.0

    def __post_init__(self) -> None:
        if self.beta_threshold >= self.gamma_threshold:
            raise ValueError(
                "beta_threshold must be below gamma_threshold, got "
                f"{self.beta_threshold} and {self.gamma_threshold}"
            )


DEFAULT_SCORING = ScoringConfig()


class RecordEvaluator:
    """Turns an interaction into a category using a dimensionless score."""

    def __init__(self, config: ScoringConfig = DEFAULT_SCORING):
        self.config = config

    @property
    def _baseline(self) -> float:
        return max(1.0, self.config.baseline_duration_seconds)

    def score(self, record: InteractionRecord) -> float:
        """The raw friction score, before it is bucketed into a category."""
        routing_component = record.routing_count * self.config.routing_weight
        duration_component = record.duration_seconds / self._baseline
        return routing_component + duration_component

    def classify(self, score: float) -> CategoryType:
        if score < self.config.beta_threshold:
            return CategoryType.ALPHA
        if score < self.config.gamma_threshold:
            return CategoryType.BETA
        return CategoryType.GAMMA

    def evaluate(self, record: InteractionRecord) -> EvaluatedRecord:
        score = self.score(record)
        return EvaluatedRecord(
            record=record,
            category=self.classify(score),
            friction_score=score,
            evaluation_metadata=f"Score: {score:.2f}",
        )
