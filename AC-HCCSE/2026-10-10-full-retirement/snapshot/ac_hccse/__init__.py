"""
AC-HCCSE -- Anti-Cog / Human-Centered Customer Service Engine.

Scores completed customer interactions for *friction*, groups them for review,
and decides who should handle the next one.

The core idea is that the cost of a bad support experience is mostly structural
rather than emotional: being transferred repeatedly, and being kept on the line,
are things a system can measure without guessing at anyone's state of mind. So
the engine scores those two signals on a shared dimensionless scale, buckets
the result, and escalates on the pattern rather than on any single call.

  1. Score an interaction against a baseline           (scoring.py)
  2. Bucket it -- ALPHA / BETA / GAMMA                 (records.py)
  3. Aggregate a batch and issue a directive           (review.py)
  4. Route the next interaction: capacity vs. history  (allocation.py)
  5. Draw a reproducible subset for human review       (sampling.py)
  6. Run the whole pipeline                            (orchestration.py)

Nothing here infers emotion or scores a person. A category describes an
interaction's distance from the operational baseline; what to do about it is a
directive for a human, not an action the engine takes.
"""

from .records import (
    AllocationLevel,
    CategoryType,
    EvaluatedRecord,
    InteractionRecord,
)
from .scoring import DEFAULT_SCORING, RecordEvaluator, ScoringConfig
from .review import DEFAULT_DIRECTIVE, Directive, DirectiveConfig, ReviewGroup
from .allocation import DEFAULT_ALLOCATION, AllocationConfig, ResourceAllocator
from .sampling import DataSampler
from .orchestration import OrchestrationSystem

__all__ = [
    "CategoryType", "AllocationLevel", "InteractionRecord", "EvaluatedRecord",
    "ScoringConfig", "DEFAULT_SCORING", "RecordEvaluator",
    "DirectiveConfig", "DEFAULT_DIRECTIVE", "Directive", "ReviewGroup",
    "AllocationConfig", "DEFAULT_ALLOCATION", "ResourceAllocator",
    "DataSampler",
    "OrchestrationSystem",
]
