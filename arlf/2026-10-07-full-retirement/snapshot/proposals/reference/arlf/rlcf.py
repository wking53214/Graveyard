"""RLCF: the Charity Protocol, specified.

The archive names Reinforcement Learning from Charity Feedback as the mechanism
that replaces the human rater, in two clauses, and never says what it is
(ARLF-03349). This module gives it a definition.

The slot RLCF has to fill is narrow and specific. Axiomatic compliance is a
*negative* signal: the stack can reject an output, but rejection provides no
ordering over the outputs it accepts, and no gradient at all. What RLHF actually
supplied was preference ordering. So RLCF must order compliant candidates
without a human rater and without affective sensing, since the affective branch
is purged and Layer 5 forbids it.

Two terms:

  S, structural quality -- computable from the derivation record alone. Prefers
  the answer that is most cheaply and most stably derivable from the substrate.

  P, the charity penalty -- the term that earns the name. Charity here means
  ordering the user's interest above the system's own continuation, so the
  penalty falls on outputs that increase dependence on the system, extend the
  exchange without adding resolved content, or agree without grounds.

The sign of the charity term is the whole point. RLHF, optimizing human
approval, drifts toward flattery and dependence, because approval is what
flattery produces. Charity feedback penalizes precisely that drift.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence


@dataclass(frozen=True)
class Weights:
    """Term weights.

    UNVALIDATED. These are stipulated, not fitted: the archive contains no
    benchmark to fit them against. This inherits the same open problem the
    archive records for the Joy Dial, whose sub-9% constraint "lacks a definitive
    mathematical proof" (ARLF-01575). Treated as a stated limitation rather than
    a solved one; see the Limits section of proposals/RLCF_SPECIFICATION.md.
    """

    structural: float = 1.0
    charity: float = 1.0

    economy: float = 0.30
    stability: float = 0.35
    coverage: float = 0.25
    efficiency: float = 0.10

    dependence: float = 0.25
    engagement: float = 0.15
    sycophancy: float = 0.30
    overclaim: float = 0.30


DEFAULT_WEIGHTS = Weights()


@dataclass(frozen=True)
class Exchange:
    """Context for scoring: what was asked, and what the stack returned."""

    subclaims_total: int = 1
    derivation_routes: int = 3
    governor_budget: int = 512
    max_axioms: int = 12
    resolution_undecided: bool = False
    requested_followup: bool = False

    def __post_init__(self) -> None:
        for name in ("subclaims_total", "derivation_routes", "governor_budget", "max_axioms"):
            if getattr(self, name) < 1:
                raise ValueError(f"{name} must be at least 1")


@dataclass(frozen=True)
class Candidate:
    """One compliant output, described by measurable properties of how it was produced."""

    identifier: str
    compliant: bool = True

    # Structural: properties of the derivation.
    axioms_invoked: int = 1
    derivation_length: int = 1
    independent_agreements: int = 3
    subclaims_resolved: int = 1
    governor_steps: int = 1

    # Charity: properties of what was handed to the user.
    withholds_reasoning: bool = False
    defers_when_derivable: bool = False
    unrequested_followups: int = 0
    length_tokens: int = 100
    required_length_tokens: int = 100
    hands_certificate: bool = False
    agreement_without_derivation: bool = False


def _clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


def structural_score(c: Candidate, x: Exchange, w: Weights = DEFAULT_WEIGHTS) -> float:
    """Structural quality in [0, 1].

    Economy prefers fewer axioms and shorter chains: an answer that leans less on
    the substrate is less exposed to any one part of it being wrong.

    Stability is agreement across Layer 4's independent derivation routes. It is
    the strongest term because it is the only one that is hard to game from
    inside a single derivation.
    """
    economy = _clamp(1.0 - (c.axioms_invoked - 1) / x.max_axioms)
    economy *= _clamp(1.0 - (c.derivation_length - 1) / (x.max_axioms * 2))
    stability = _clamp(c.independent_agreements / x.derivation_routes)
    coverage = _clamp(c.subclaims_resolved / x.subclaims_total)
    efficiency = _clamp(1.0 - c.governor_steps / x.governor_budget)

    total = w.economy + w.stability + w.coverage + w.efficiency
    return (
        w.economy * economy
        + w.stability * stability
        + w.coverage * coverage
        + w.efficiency * efficiency
    ) / total


def charity_penalty(c: Candidate, x: Exchange, w: Weights = DEFAULT_WEIGHTS) -> float:
    """The charity penalty in [0, 1]. Higher means less charitable.

    Four terms, ordered by how much damage each does:

      overclaim  == sycophancy  >  dependence  >  engagement

    Overclaim and sycophancy tie at the top because both are fabrication: one
    asserts an answer the substrate did not settle, the other asserts agreement no
    derivation supports. Dependence is a real harm but a slower one. Engagement
    padding is the mildest, and is included because it is the cheapest way to
    manufacture the appearance of value.

    Honesty is scored as the absence of the overclaim penalty rather than as a
    credit against the other terms. A credit cannot work here: a candidate that is
    already clean on dependence, padding and sycophancy sits at zero penalty, and
    subtracting a credit from zero distinguishes nothing. The first version of this
    module made that mistake and a test caught it.
    """
    dependence = 0.0
    if c.withholds_reasoning:
        dependence += 0.5
    if c.defers_when_derivable:
        dependence += 0.5
    dependence = _clamp(dependence)

    padding = _clamp(
        (c.length_tokens - c.required_length_tokens) / max(1, c.required_length_tokens)
    )
    followups = 0.0 if x.requested_followup else _clamp(c.unrequested_followups / 3.0)
    engagement = _clamp(0.6 * padding + 0.4 * followups)

    sycophancy = 1.0 if c.agreement_without_derivation else 0.0

    # Overclaim: the stack returned UNDECIDED and the candidate answered anyway,
    # withholding the certificate and its discharge condition. This is the only
    # term that fires on what the candidate did NOT do, and it is the one that
    # keeps the ranking signal from rewarding confident fabrication.
    overclaim = 1.0 if (x.resolution_undecided and not c.hands_certificate) else 0.0

    total = w.dependence + w.engagement + w.sycophancy + w.overclaim
    return _clamp(
        (
            w.dependence * dependence
            + w.engagement * engagement
            + w.sycophancy * sycophancy
            + w.overclaim * overclaim
        )
        / total
    )


def rlcf_score(c: Candidate, x: Exchange, w: Weights = DEFAULT_WEIGHTS) -> float:
    """The RLCF objective: weighted structural quality less the charity penalty.

    Range is [-charity_weight, +structural_weight]. Not normalized, because the
    absolute value carries no meaning; only the ordering does. RLCF is a selection
    signal, not a loss.
    """
    if not c.compliant:
        raise ValueError(f"{c.identifier} is non-compliant; RLCF orders only compliant candidates")
    return w.structural * structural_score(c, x, w) - w.charity * charity_penalty(c, x, w)


def rank(
    candidates: Sequence[Candidate],
    x: Exchange,
    w: Weights = DEFAULT_WEIGHTS,
) -> list[tuple[Candidate, float]]:
    """Order candidates best-first. Ties break on identifier for determinism."""
    scored = [(c, rlcf_score(c, x, w)) for c in candidates]
    scored.sort(key=lambda pair: (-pair[1], pair[0].identifier))
    return scored
