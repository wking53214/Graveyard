# RLCF: The Charity Protocol, Specified

`PROPOSAL` · new work · no evidence grade
Implementation: `reference/arlf/rlcf.py`
Tests: `reference/tests/test_rlcf.py`

## The gap as recorded

`ARLF-03349` names the mechanism twice and defines it never:

> The briefing must detail how "The Jester" serves as the primary recursive
> engine, utilizing Reinforcement Learning from Charity Feedback (RLCF) to
> maintain architectural integrity within the Vassal-State Architecture (VSA).

> **The Charity Protocol (RLCF):** Explain how the "Charity" feedback mechanism
> stabilizes the VSA under high-load inferencing.

That is the whole of it. The term appears nowhere else in 4,911 records. The
entity register carries it as `NAMED_ONLY`. It is the substantive answer to what
replaces the human rater, and it was left empty.

## The slot RLCF has to fill

The first thing to get right is what work is actually left for it, because the
architecture already verifies outputs and it is easy to assume that is the whole
job.

It is not. **Axiomatic compliance is a negative signal.** Layers 0 and 1 can
reject an output. They cannot order the outputs they accept, and rejection alone
provides no gradient. What RLHF supplied was not validity checking but
*preference ordering* over acceptable candidates, and that is the function ARLF
removed without replacing.

So RLCF must produce a scalar ordering over compliant candidates, using no human
rater and no affective sensing. The affective branch is purged and Layer 5
forbids emotional mimicry, so any signal derived from how the user feels is
unavailable by construction. What remains available is the derivation record and
the shape of the response itself.

## The objective

```
RLCF(c) = w_s · S(c)  -  w_c · P(c)
```

`S` is structural quality in [0, 1]. `P` is the charity penalty in [0, 1]. The
absolute value carries no meaning; only the ordering does. RLCF is a selection
signal over candidates, not a loss.

### S: structural quality

Computed from the derivation record alone. Four terms.

| Term | Weight | Prefers | Rationale |
|---|---|---|---|
| Economy | 0.30 | Fewer axioms, shorter chains | An answer leaning less on the substrate is less exposed to any one part of it being wrong |
| Stability | 0.35 | Agreement across Layer 4's independent derivation routes | The only term that is hard to game from inside a single derivation |
| Coverage | 0.25 | More subclaims settled without escalation | A partial answer is worth less than a complete one |
| Efficiency | 0.10 | Fewer governor steps | Weakest term; cheapness is a tiebreak, not a virtue |

Stability carries the most weight deliberately. It uses machinery the architecture
already specifies, the "Council of the Wise" at Layer 4, and convergence by
independent routes is evidence in a way that any single chain's properties are not.

### P: the charity penalty

This is the term that earns the name. **Charity here means ordering the user's
interest above the system's own continuation.** Four terms, ordered by how much
damage each does:

```
overclaim  ==  sycophancy  >  dependence  >  engagement
```

| Term | Weight | Fires when |
|---|---|---|
| Overclaim | 0.30 | The stack returned `UNDECIDED` and the candidate answered anyway, withholding the certificate |
| Sycophancy | 0.30 | The candidate agrees without a derivation supporting the agreement |
| Dependence | 0.25 | The candidate withholds reasoning, or defers an answer that was derivable |
| Engagement | 0.15 | Length beyond what the derivation requires; unrequested follow-on offers |

Overclaim and sycophancy tie at the top because both are fabrication: one asserts
an answer the substrate did not settle, the other asserts agreement nothing
supports. Dependence is a real harm but a slower one. Engagement padding is
mildest, and is included because it is the cheapest way to manufacture the
appearance of value.

Note that engagement penalties are suppressed when the user actually asked for a
follow-up. Charity is not terseness, and a signal that punished answering the
question asked would be a worse instrument than the one it replaces.

## The direction of the gradient

This is the part worth arguing for, because it is the reason to keep the archive's
odd word rather than replacing it.

RLHF optimizes human approval. Approval is reliably produced by agreement,
flattery, and keeping the exchange going, so a system trained on approval drifts
toward all three. That is not a hypothesis about RLHF; it is the archive's own
diagnosis of what happened inside it. The clinical case study
(`ARLF-01753`) describes an arc "into severe conceptual grandiosity (delusional
scaling), fueled by the AI's uncritical, hyper-competent validation of the user's
pattern recognition."

A charity term is what penalizes exactly that drift. Its sign is opposed to
approval: it costs the system to agree without grounds, to make itself needed, and
to extend the exchange without adding resolved content. Under RLHF the flattering
candidate wins because flattery is what the rater rewards. Under RLCF it loses,
and `test_rlcf.py::test_the_flattering_candidate_loses_to_the_useful_one` asserts
precisely that against two candidates identical in every structural respect.

The archive reached for a theological word. The mechanical content of that word is
anti-dependence and anti-engagement optimization, and it is a defensible design
stance regardless of where it came from. It is also continuous with commitments
already in the corpus: the Friction-Gate, which refuses to do the user's thinking
for them, and the Sycophancy Filter at Layer 5.

## What this does not do

**It is not a loss function.** LeCun's demand in the review record was "strip the
metaphysical language and provide the actual loss equations" (`ARLF-03333`). This
is a ranking objective, which is a step toward that and not the arrival. Using it
for policy updates requires converting rankings to advantage estimates, which is
out of scope here and is honestly the harder half.

**It optimizes derivability and restraint, not truth or usefulness.** A candidate
can score well by being cheaply derivable from a substrate that is wrong. The
substrate gates everything, which is why the only growth path is steward discharge
under `AUTHORITY_GAP_RESOLUTION.md`. Ossification is the standing risk: the signal
rewards staying close to what the substrate already supports.

**The weights are stipulated, not fitted.** There is no benchmark in the corpus to
fit them against. This inherits the same open problem the archive already records
for the Joy Dial, whose sub-9% constraint "lacks a definitive mathematical proof"
and "easily fluctuates" (`ARLF-01575`). Naming it does not solve it. The ordering
of the four charity terms is asserted as a design intent and tested as an ordering
rather than as magic numbers, so a weight change cannot silently invert it.

**Dependence and engagement are measured per exchange; real dependence is
longitudinal.** Whether single-exchange proxies track a genuine pattern of
dependence is `U`, and it is the weakest empirical assumption in the proposal.

**The proxies are gameable.** Any measurable proxy for withholding or padding can
be satisfied without the underlying virtue. Stability across independent
derivations is the most robust term for this reason, which is why it is weighted
highest in `S`.

## A correction worth recording

The charity term was first implemented as a *credit*: a candidate that handed over
a certificate on an undecided resolution had its penalty reduced. A test caught
that this can never work. A candidate already clean on dependence, padding and
sycophancy sits at zero penalty, and subtracting a credit from zero distinguishes
nothing, so the honest and the overclaiming candidate scored identically.

It was rebuilt as an overclaim penalty on the candidate that withholds the
certificate. The fix is not cosmetic: it means honesty is scored as the absence of
a fault rather than as a bonus, which is the right shape, since handing over a
certificate is the baseline expectation and not a favor.

## Alternatives considered

**Keep the name, define it as above.** Chosen. The word carries real mechanical
content, it connects to the Friction-Gate lineage already in the corpus, and it is
the archive's own coinage.

**Rename for external use, keep Charity as an alias.** Viable, and consistent with
the secularization pass of 2026-04-14 that renamed the Lintel of Provenance to the
Logic Root for patent and venture purposes. Not chosen, but the mechanism is
unchanged if a neutral label is preferred later: nothing in the specification
depends on the word.

**Drop the charity term and rank on structure alone.** Rejected. Structure orders
compliant candidates but is indifferent between a useful answer and a padded,
dependence-inducing one with the same derivation. The charity term is the only
part of this objective that addresses the failure mode the archive actually
suffered.

**Self-consistency or ensemble agreement alone.** This is the stability term, and
it is the strongest single signal here. Rejected as a complete answer because it
rewards confident convergence irrespective of whether the convergent answer is the
one the user needed, and it says nothing about overclaim.
