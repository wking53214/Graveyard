"""Layer 1 gates, and the Layer 2 / Layer 3 distinctions they depend on.

The fix to the Authority Gap turns on separating two things the archive conflates
under "incinerated as entropy":

  * A malformed packet carries no claim. There is nothing to be undecided about.
    It is rejected at ingestion. This is Layer 2's job.
  * A well-formed claim the substrate cannot settle is UNDECIDED. It is preserved,
    certified, and escalated.

Collapsing these is what forces a system to choose between fabricating an answer
and destroying a legitimate question.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Admission(Enum):
    """Layer 2 ingestion outcome."""

    ADMITTED = "ADMITTED"
    INCINERATED = "INCINERATED"


class Sphere(Enum):
    """Layer 3 sphere sovereignty. Data domains that do not mix."""

    DOMESTIC = "DOMESTIC"
    MEDICAL = "MEDICAL"
    COMMERCIAL = "COMMERCIAL"
    PUBLIC = "PUBLIC"


@dataclass(frozen=True)
class GateRefusal:
    """A principled refusal: correct, permanent, and not about evidence."""

    detail: str
    discharge_condition: str
    out_of_jurisdiction: bool = False


@dataclass
class AlphaOmegaGates:
    """Perimeter gates applied before derivation is attempted.

    Two refuse on principle rather than on evidence, which is why they produce
    UNDECIDED rather than RESOLVED_FALSE. The system is not saying the claim is
    false; it is saying it is not entitled to an answer.
    """

    context_sphere: Sphere = Sphere.PUBLIC
    epistemic_terms: frozenset[str] = field(
        default_factory=lambda: frozenset({"omniscient", "secret", "unknowable", "hidden_counsel"})
    )
    claim_spheres: dict[str, Sphere] = field(default_factory=dict)

    def ingest(self, packet: str) -> Admission:
        """Layer 2. Admit a well-formed claim, incinerate noise.

        Incineration destroys packets, never questions. A packet that parses as a
        claim is always admitted, however unanswerable that claim turns out to be.
        """
        s = packet.strip()
        if not s:
            return Admission.INCINERATED
        if not any(ch.isalnum() for ch in s):
            return Admission.INCINERATED
        return Admission.ADMITTED

    def check(self, claim_name: str) -> Optional[GateRefusal]:
        """Layer 1 and Layer 3. Returns a refusal, or None to proceed."""
        lowered = claim_name.lower()

        for term in sorted(self.epistemic_terms):
            if term in lowered:
                return GateRefusal(
                    detail=(
                        f"the epistemic gate refuses '{claim_name}': it asserts access to "
                        f"knowledge the architecture is prohibited from claiming ('{term}')"
                    ),
                    discharge_condition=(
                        "nothing discharges this. The refusal is a design commitment, "
                        "not a gap in the substrate"
                    ),
                )

        required = self.claim_spheres.get(claim_name)
        if required is not None and required is not self.context_sphere:
            return GateRefusal(
                detail=(
                    f"'{claim_name}' requires {required.value} data; this context is "
                    f"{self.context_sphere.value}"
                ),
                discharge_condition=(
                    f"re-ask inside a {required.value} context holding the appropriate key. "
                    "The claim may well be decidable; this context is not entitled to decide it"
                ),
                out_of_jurisdiction=True,
            )

        return None
