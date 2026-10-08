# Resolution of the Authority Gap

`PROPOSAL` · new work · no evidence grade
Implementation: `reference/arlf/resolution.py`, `certificate.py`, `pipeline.py`
Tests: `reference/tests/test_resolution.py`, `test_certificate.py`, `test_loop_of_the_absurd.py`

## The gap as recorded

`ARLF-01575`, Ghost Problem 2:

> **The Authority Gap:** When the rigid truth gates encounter complex,
> high-entropy data, the system risks entering an infinite "Loop of the Absurd"
> because it lacks a clear protocol to handle valid unknowns safely.

The cause is Volume 1. Truth is set as a static binary constant at 1.000 Parity;
data packages "must resolve to an absolute Yes/No; anything else is incinerated
as entropy."

That makes the resolution function **partial over two values**. A well-formed
claim the substrate cannot settle has three places to go, and all three are
defects:

1. **Forced binary.** Pick Yes or No anyway. This is fabrication, and it is the
   mechanism behind the reviewers' prediction that the architecture would become
   "a self-contained hallucination, making decisions for the physical world based
   on data that no longer exists" (`ARLF-03324`, section IV).
2. **Incineration.** Destroy the packet. The question is lost, and the substrate
   never learns it was asked.
3. **Recursion.** Keep trying. This is the Loop of the Absurd by name.

## The fix

Make the function **total over three values**.

| Verdict | Requires | Carries |
|---|---|---|
| `RESOLVED_TRUE` | A derivation of the claim | The derivation |
| `RESOLVED_FALSE` | A derivation of the claim's negation | The derivation |
| `UNDECIDED` | Nothing further; terminal | A non-resolution certificate |

`UNDECIDED` is a verdict, not an error, not a retry signal, and not a lower
confidence score. The function still terminates on every input and still returns
exactly one value. It just has a third value to return.

### Five invariants

**1. Totality.** `resolve()` returns one of three verdicts for every admitted
input and always terminates.

**2. Negation as failure is prohibited.** `RESOLVED_FALSE` requires a derivation
of the negation. Failure to derive the claim is never evidence of its falsehood.
This is the invariant that matters, and it is enforced in the type: a resolved
verdict cannot be constructed without a derivation.

A closed-world system that reads unproven as false is not merely imprecise. It is
the exact machine the Black Paper described, because every gap in its substrate
becomes a confident negative assertion about the world.

**3. Bounded.** Every resolution runs under a Kinetic Governor step budget.
Exhaustion yields `UNDECIDED` with cause `BUDGET_EXHAUSTED`. The Loop of the
Absurd becomes impossible rather than unlikely: the loop cannot outlive its
budget, and a truncated search is never reported as a completed one.

**4. Certified.** Every `UNDECIDED` names its cause, what specifically blocked
resolution, what would settle it, and who is competent to supply that. A
certificate without a discharge condition fails construction.

**5. Entropy and unknowns are separated.** This is the distinction the archive
collapses. A malformed packet carries no claim and is incinerated at Layer 2
ingestion. A well-formed claim the substrate cannot settle is preserved,
certified and escalated. Incineration destroys noise, never questions.

### Causes

| Cause | Meaning | Escalates to |
|---|---|---|
| `MISSING_AXIOM` | The claim's vocabulary is absent from the substrate | Steward |
| `UNDERDETERMINED` | Closure completed; both polarities remain consistent | Steward |
| `CONTRADICTORY_SUBSTRATE` | Both polarities derivable. A Layer 0 defect | Substrate maintainer |
| `GATE_BLOCKED` | An Alpha-Omega gate refused on principle, not evidence | Nobody. Correct and permanent |
| `OUT_OF_JURISDICTION` | Sphere sovereignty forbids the data required | Nobody in this context |
| `BUDGET_EXHAUSTED` | Closure did not complete in budget | Substrate maintainer |

No cause means "probably false." The taxonomy has no such state by design.

`MISSING_AXIOM` and `UNDERDETERMINED` are distinguished by vocabulary membership,
because they ask for different things: the first needs a new premise, the second
needs an existing one settled.

`GATE_BLOCKED` and `OUT_OF_JURISDICTION` are worth noting as the two cases where
`UNDECIDED` is not a deficiency. A system that declines to answer a medical
question from a commercial context is working correctly, and saying so beats both
answering and pretending not to know.

## Where this puts the human

The Sabbath Protocol at Layer 7 exists to "preserve human stewardship and agency"
(`ARLF-01575`). Under this proposal that clause does concrete work: **the steward
is the arbiter of the undecidable.**

This resolves the framework's central tension rather than splitting the
difference. ARLF's case against RLHF was the Lazy Evaluator problem: humans are
"bored, biased, and easily manipulated" when rating answers the machine could
check itself. That case is sound, and nothing here weakens it. The human is
removed from routine quality judgment and reinstated at the only place where a
human is not substitutable, which is extending the substrate.

The substrate grows only by discharge: a named steward, a stated rationale, an
audit entry. It never ingests its own conclusions. That single restriction
answers the model-collapse objection directly, since collapse requires a system
that feeds on its own synthetic output.

## What this gives up

**1.000 Parity is weakened.** The system is no longer binary-complete, and that
is the actual price. The archive's version bought completeness with fabrication;
this version buys honesty with incompleteness. There is no third option, and
anyone claiming a deterministic system that answers every well-formed question
correctly is selling something.

**`UNDECIDED` rate becomes a system health metric.** A system that returns
`UNDECIDED` to most inputs is honest and useless. This proposal defines the state
but sets no coverage target, and a real deployment needs one. `U` on what an
acceptable rate is.

**Steward throughput becomes the bottleneck.** Every dischargeable certificate is
a demand on human attention. ARLF exists to remove humans from the loop, and this
fix reinstates them at the boundary, so the framework's headline efficiency claim
is narrower than it appeared: the machine handles the decidable at machine speed
and the undecidable queues for a person.

**The cause distinctions are approximations.** Telling `UNDERDETERMINED` from
`MISSING_AXIOM` in the general case is not decidable; the implementation decides
it by vocabulary membership within budget, which is a heuristic that will
sometimes name the wrong cause.

## Alternatives considered

**Confidence scores instead of a third verdict.** Rejected. A probability
reintroduces exactly the probabilistic drift Layer 1 exists to truncate, and in
practice a threshold on a score is a forced binary with extra steps.

**Paraconsistent logic for the contradiction case.** Rejected as premature.
Tolerating contradictions lets a defective substrate keep operating, and
`CONTRADICTORY_SUBSTRATE` treats a contradiction as a defect to repair, which it
is.

**Retry with an expanded budget.** Rejected as the default. It is the Loop of the
Absurd with a counter. Raising the budget is a deliberate operator decision that
the certificate recommends; it is not automatic.

**Open-world assumption throughout.** This is effectively what the proposal
adopts for the resolution function, without adopting the full machinery.
`UNDECIDED` is the open-world reading of non-derivability.

## Verification

`reference/tests/test_loop_of_the_absurd.py` constructs substrates that diverge
or blow up under an unbounded resolver, including a 5,000-rule chain and a dense
fan-out, and asserts termination with `BUDGET_EXHAUSTED` inside budget. It also
asserts that exhaustion never returns a verdict at any budget from 1 step upward,
and that a sufficient budget still resolves reachable claims, so the bound does
not make the system useless.

`test_resolution.py` asserts the negation-as-failure prohibition directly:
unknown symbols and unsettled-but-known symbols both return `UNDECIDED`, never
`RESOLVED_FALSE`.

`test_certificate.py` walks the full discharge cycle: a claim is `UNDECIDED` with
`MISSING_AXIOM`, a steward discharges the axiom with authority and rationale, and
the same claim then resolves. It also asserts that resolution never writes derived
facts back into the substrate.
