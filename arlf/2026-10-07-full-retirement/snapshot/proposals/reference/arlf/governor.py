"""The 0.815 Kinetic Governor: a bounded budget on every resolution.

The archive specifies the governor as a "mechanical rev-limiter" forcing a
Liturgical Pause of 13ms to 200ms so "computational speed does not outpace human
capacity for oversight" (ARLF-01575). Here it does a second job: it bounds
derivation.

Budget exhaustion is what makes the Loop of the Absurd impossible rather than
merely unlikely. A resolution that cannot finish inside its budget returns
UNDECIDED with cause BUDGET_EXHAUSTED. It never guesses, and it never runs on.
"""

from __future__ import annotations

from dataclasses import dataclass

PAUSE_FLOOR_MS = 13.0
PAUSE_CEILING_MS = 200.0
KINETIC_CONSTANT = 0.815


class BudgetExhausted(Exception):
    """Raised internally when the step budget is spent. Never escapes resolve()."""


@dataclass
class KineticGovernor:
    """A step budget with a derived pause, consumed one inference at a time."""

    max_steps: int = 512
    steps_used: int = 0

    def __post_init__(self) -> None:
        if self.max_steps < 1:
            raise ValueError("max_steps must be at least 1")

    def spend(self, n: int = 1) -> None:
        """Consume budget. Raises BudgetExhausted once the limit is passed."""
        self.steps_used += n
        if self.steps_used > self.max_steps:
            raise BudgetExhausted(
                f"step budget {self.max_steps} exhausted after {self.steps_used} steps"
            )

    @property
    def remaining(self) -> int:
        return max(0, self.max_steps - self.steps_used)

    @property
    def exhausted(self) -> bool:
        return self.steps_used >= self.max_steps

    def pause_ms(self) -> float:
        """The Liturgical Pause for this resolution.

        Scales with budget consumed, clamped to the archive's stated band. Longer
        derivations earn a longer pause: the harder the machine worked, the more
        time the human gets to look at it.
        """
        fraction = min(1.0, self.steps_used / self.max_steps)
        span = (PAUSE_CEILING_MS - PAUSE_FLOOR_MS) * KINETIC_CONSTANT
        return round(PAUSE_FLOOR_MS + span * fraction, 3)

    def reset(self) -> None:
        self.steps_used = 0
