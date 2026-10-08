"""Terminal verdicts for the resolution function.

The archive's Volume 1 requires every data package to resolve to an absolute
Yes or No, with "anything else incinerated as entropy" (ARLF-01575). That makes
the resolution function partial over two values: a well-formed claim that the
substrate cannot settle has nowhere to go except a forced binary, the
incinerator, or an unbounded attempt to resolve -- the "Loop of the Absurd"
recorded as the Authority Gap.

This module makes the function total over three values instead. UNDECIDED is a
first-class terminal verdict carrying a certificate, not a failure and not a
retry signal.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Sequence

from .certificate import Certificate


class Verdict(Enum):
    """The three terminal states. Exhaustive and mutually exclusive."""

    RESOLVED_TRUE = "RESOLVED_TRUE"
    RESOLVED_FALSE = "RESOLVED_FALSE"
    UNDECIDED = "UNDECIDED"

    @property
    def is_resolved(self) -> bool:
        return self is not Verdict.UNDECIDED


@dataclass(frozen=True)
class Resolution:
    """The outcome of resolving one claim.

    Invariants, enforced at construction:

    1. A resolved verdict carries a derivation and no certificate.
    2. UNDECIDED carries a certificate and no derivation.

    Invariant 2 is the one that matters. It makes it impossible to return
    "cannot settle this" without also stating why and what would settle it,
    which is what keeps the architecture from becoming the self-contained
    hallucination its own reviewers predicted.
    """

    claim: str
    verdict: Verdict
    derivation: Sequence[str] = field(default_factory=tuple)
    certificate: Optional[Certificate] = None
    steps: int = 0

    def __post_init__(self) -> None:
        if self.verdict.is_resolved:
            if self.certificate is not None:
                raise ValueError("a resolved verdict must not carry a certificate")
            if not self.derivation:
                raise ValueError(
                    "a resolved verdict must carry a derivation; resolution by "
                    "absence of counter-evidence is prohibited"
                )
        else:
            if self.certificate is None:
                raise ValueError("UNDECIDED must carry a certificate")
            if self.derivation:
                raise ValueError("UNDECIDED must not carry a derivation")

    def __str__(self) -> str:
        if self.verdict.is_resolved:
            return f"{self.verdict.value} <- {' ; '.join(self.derivation)}"
        return f"UNDECIDED [{self.certificate.cause.value}] {self.certificate.discharge_condition}"
