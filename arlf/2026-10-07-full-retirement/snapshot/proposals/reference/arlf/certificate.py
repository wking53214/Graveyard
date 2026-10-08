"""Non-resolution certificates.

Every UNDECIDED verdict carries one. A certificate names why the claim could
not be settled, what specifically blocked it, what evidence would settle it, and
who is competent to supply that evidence.

The discharge condition is the load-bearing field. Without it, UNDECIDED is an
error code; with it, UNDECIDED is a request, and the substrate has a defined
channel through which external truth can enter. That channel is the difference
between a bounded system and a closed one.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Cause(Enum):
    """Why resolution terminated without a verdict.

    Deliberately excludes any cause meaning "the claim is probably false".
    Non-derivation is never evidence of falsehood.
    """

    MISSING_AXIOM = "MISSING_AXIOM"
    """The substrate has no premise bearing on the claim's vocabulary."""

    UNDERDETERMINED = "UNDERDETERMINED"
    """Closure is complete and both the claim and its negation remain consistent."""

    CONTRADICTORY_SUBSTRATE = "CONTRADICTORY_SUBSTRATE"
    """Both the claim and its negation are derivable. The substrate is at fault."""

    GATE_BLOCKED = "GATE_BLOCKED"
    """An Alpha-Omega gate refused the claim on principle, not on evidence."""

    OUT_OF_JURISDICTION = "OUT_OF_JURISDICTION"
    """Sphere sovereignty forbids using the data the claim requires."""

    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    """The Kinetic Governor budget was spent before closure. Terminates the
    Loop of the Absurd by construction: the loop cannot outlive its budget."""


class Escalation(Enum):
    """Who is competent to discharge the certificate."""

    STEWARD = "STEWARD"
    """A human under Layer 7. The only party able to extend the substrate."""

    SUBSTRATE_MAINTAINER = "SUBSTRATE_MAINTAINER"
    """A contradiction or gap is a defect in the substrate itself."""

    NONE = "NONE"
    """Nothing to discharge. The refusal is correct and permanent."""


_ESCALATION = {
    Cause.MISSING_AXIOM: Escalation.STEWARD,
    Cause.UNDERDETERMINED: Escalation.STEWARD,
    Cause.CONTRADICTORY_SUBSTRATE: Escalation.SUBSTRATE_MAINTAINER,
    Cause.GATE_BLOCKED: Escalation.NONE,
    Cause.OUT_OF_JURISDICTION: Escalation.NONE,
    Cause.BUDGET_EXHAUSTED: Escalation.SUBSTRATE_MAINTAINER,
}


@dataclass(frozen=True)
class Certificate:
    """An auditable record of why a claim was not settled."""

    cause: Cause
    blocking_detail: str
    discharge_condition: str
    escalation: Escalation

    def __post_init__(self) -> None:
        if not self.blocking_detail.strip():
            raise ValueError("blocking_detail must name what blocked resolution")
        if not self.discharge_condition.strip():
            raise ValueError(
                "discharge_condition must state what would settle the claim; "
                "an UNDECIDED with no discharge path is an error code, not a certificate"
            )
        if self.escalation is not _ESCALATION[self.cause]:
            raise ValueError(
                f"cause {self.cause.value} escalates to "
                f"{_ESCALATION[self.cause].value}, not {self.escalation.value}"
            )

    @classmethod
    def for_cause(cls, cause: Cause, blocking_detail: str, discharge_condition: str) -> "Certificate":
        """Build a certificate with the escalation target implied by the cause."""
        return cls(cause, blocking_detail, discharge_condition, _ESCALATION[cause])

    @property
    def is_dischargeable(self) -> bool:
        return self.escalation is not Escalation.NONE
