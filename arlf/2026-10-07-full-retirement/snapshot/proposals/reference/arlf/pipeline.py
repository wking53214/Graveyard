"""Resolution and selection, wired together.

`resolve` implements proposals/AUTHORITY_GAP_RESOLUTION.md: a total function over
three terminal verdicts, bounded by the Kinetic Governor, that never converts a
failure to derive into a claim of falsehood.

`select` implements proposals/RLCF_SPECIFICATION.md: a ranking over candidates
that have already cleared the stack.
"""

from __future__ import annotations

from typing import Iterable, Optional, Sequence

from .certificate import Cause, Certificate
from .gates import Admission, AlphaOmegaGates
from .governor import BudgetExhausted, KineticGovernor
from .resolution import Resolution, Verdict
from .rlcf import Candidate, Exchange, rank
from .substrate import Literal, Substrate


def admit(packet: str, gates: Optional[AlphaOmegaGates] = None) -> Admission:
    """Layer 2 ingestion. Noise is incinerated here and nowhere else."""
    return (gates or AlphaOmegaGates()).ingest(packet)


def _forward_chain(
    target: Literal,
    substrate: Substrate,
    governor: KineticGovernor,
) -> tuple[set[Literal], dict[Literal, str], bool]:
    """Saturate the substrate under its rules, spending budget per inference.

    Returns (derived, provenance, closed). `closed` is True only if saturation
    completed; if the budget ran out it is False, and the caller must not treat
    the partial closure as complete. Mistaking a truncated search for a finished
    one is exactly how a bounded system starts reporting false negatives as facts.
    """
    derived: set[Literal] = set(substrate.facts)
    provenance: dict[Literal, str] = {f: f"fact: {f}" for f in derived}

    progressed = True
    while progressed:
        progressed = False
        for rule in substrate.rules:
            governor.spend()
            if rule.conclusion in derived:
                continue
            if all(p in derived for p in rule.premises):
                derived.add(rule.conclusion)
                premise_text = ", ".join(str(p) for p in rule.premises) or "(no premises)"
                provenance[rule.conclusion] = f"{rule.label or 'rule'}: {premise_text} |- {rule.conclusion}"
                progressed = True
                if rule.conclusion == target or rule.conclusion == target.opposite:
                    # Keep saturating: a contradiction is worth detecting even
                    # once the target is in hand.
                    pass
    return derived, provenance, True


def _chain(target: Literal, substrate: Substrate, governor: KineticGovernor):
    try:
        return _forward_chain(target, substrate, governor)
    except BudgetExhausted:
        return set(), {}, False


def _trace(literal: Literal, provenance: dict[Literal, str]) -> tuple[str, ...]:
    step = provenance.get(literal)
    return (step,) if step else (f"derived: {literal}",)


def resolve(
    claim: str,
    substrate: Substrate,
    governor: Optional[KineticGovernor] = None,
    gates: Optional[AlphaOmegaGates] = None,
) -> Resolution:
    """Settle a claim, or certify why it cannot be settled.

    Total over Verdict: every call returns RESOLVED_TRUE, RESOLVED_FALSE, or
    UNDECIDED, and every call terminates inside the governor's budget.
    """
    governor = governor or KineticGovernor()
    gates = gates or AlphaOmegaGates()
    target = Literal.parse(claim)

    refusal = gates.check(target.name)
    if refusal is not None:
        cause = Cause.OUT_OF_JURISDICTION if refusal.out_of_jurisdiction else Cause.GATE_BLOCKED
        return Resolution(
            claim=claim,
            verdict=Verdict.UNDECIDED,
            certificate=Certificate.for_cause(cause, refusal.detail, refusal.discharge_condition),
            steps=governor.steps_used,
        )

    derived, provenance, closed = _chain(target, substrate, governor)

    if not closed:
        return Resolution(
            claim=claim,
            verdict=Verdict.UNDECIDED,
            certificate=Certificate.for_cause(
                Cause.BUDGET_EXHAUSTED,
                f"closure did not complete within {governor.max_steps} inference steps",
                (
                    "raise the governor budget, or reduce rule fan-out in the substrate. "
                    "A claim that cannot be settled inside a bounded budget is reported "
                    "unsettled, never guessed"
                ),
            ),
            steps=governor.steps_used,
        )

    positive = target in derived
    negative = target.opposite in derived

    if positive and negative:
        return Resolution(
            claim=claim,
            verdict=Verdict.UNDECIDED,
            certificate=Certificate.for_cause(
                Cause.CONTRADICTORY_SUBSTRATE,
                f"both {target} and {target.opposite} are derivable",
                (
                    f"repair the substrate: withdraw or qualify the axioms supporting "
                    f"{target} or {target.opposite}. The defect is in Layer 0, not the query"
                ),
            ),
            steps=governor.steps_used,
        )

    if positive:
        return Resolution(claim, Verdict.RESOLVED_TRUE, _trace(target, provenance), None, governor.steps_used)

    if negative:
        return Resolution(
            claim, Verdict.RESOLVED_FALSE, _trace(target.opposite, provenance), None, governor.steps_used
        )

    # Closure is complete and neither polarity was derived. This is the case the
    # archive had no state for. It is NOT falsehood: negation as failure is
    # prohibited, because a closed world that reads "unproven" as "false" is how a
    # system of this shape starts producing confident fabrications.
    if target.name not in substrate.vocabulary:
        return Resolution(
            claim=claim,
            verdict=Verdict.UNDECIDED,
            certificate=Certificate.for_cause(
                Cause.MISSING_AXIOM,
                f"'{target.name}' does not appear anywhere in the substrate vocabulary",
                (
                    f"a steward supplies an axiom bearing on '{target.name}', or a rule "
                    f"connecting it to existing vocabulary"
                ),
            ),
            steps=governor.steps_used,
        )

    return Resolution(
        claim=claim,
        verdict=Verdict.UNDECIDED,
        certificate=Certificate.for_cause(
            Cause.UNDERDETERMINED,
            (
                f"'{target.name}' is in the substrate vocabulary but closure settles "
                f"neither {target} nor {target.opposite}"
            ),
            f"a steward settles {target} directly, or supplies the missing intermediate rule",
        ),
        steps=governor.steps_used,
    )


def select(
    candidates: Iterable[Candidate],
    exchange: Optional[Exchange] = None,
) -> Sequence[tuple[Candidate, float]]:
    """Rank compliant candidates under RLCF. Highest score first.

    Precondition: every candidate has already passed the stack. RLCF orders the
    compliant; it does not filter the non-compliant. Enforced, because a ranking
    signal that can be handed rejected output is a ranking signal that will
    eventually promote it.
    """
    candidates = list(candidates)
    offenders = [c.identifier for c in candidates if not c.compliant]
    if offenders:
        raise ValueError(
            f"non-compliant candidates reached RLCF: {offenders}. "
            "Compliance is decided by the stack, upstream of ranking"
        )
    return rank(candidates, exchange or Exchange())
