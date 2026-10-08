# ARLF: Overview at Peak

`RECONSTRUCTION` · primary sources `ARLF-03349`, `ARLF-01575` · supporting `ARLF-02104`, `ARLF-03330`

**Canonical reading: Architectural Recursive Logic Feedback.** See `NOMENCLATURE.md` for the
determination and the evidence behind it. The affective reading, which the corpus develops in
parallel and which its review panel destroyed, is preserved in `spec/variant/`.

## Definition

ARLF replaces the probabilistic, human-supplied training signal of RLHF with deterministic internal
structural verification. Where RLHF asks a human whether an output is good, ARLF asks the
architecture whether an output is compliant.

The clearest statement is the White Paper v1.0 summary (`ARLF-01575`):

> The document details the transition from traditional, probabilistic RLHF (Reinforcement Learning
> from Human Feedback) to a deterministic, structural approach called ARLF (Architectural Recursive
> Logic Feedback).

And the framing statement from the day the framework was coined (`ARLF-03349`):

> Frame ARLF as the terminal replacement for the RLHF/RLAIF industrial feedback loop. [...]
> **The ARLF Mechanism:** Detail the shift from external human input to internal, recursive
> architectural verification.

*External human input* out. *Internal recursive architectural verification* in. That is the whole
proposal, and the Architect's own framing was that it "would be the largest change in the existence
of AI" (`ARLF-03357`).

## The three claims

**1. Human feedback is the bottleneck, not the ceiling.** RLHF is characterized as entropic and
subjective. The corpus names the failure the *Lazy Evaluator problem*, and the review panel conceded
it: "Human-in-the-loop (RLHF) is failing because humans are bored, biased, and easily manipulated"
(`ARLF-03327`, `[C]`).

**2. Compliance is checkable where correctness is not.** The substitution that makes the framework
coherent. A model cannot verify that an output is *good*, but a deterministic stack can verify that
an output *resolved through its gates*. `ARLF-01575` states the replacement precisely: the
architecture "replaces 'Probabilistic Correctness' with 'Axiomatic Compliance.'" Truth is set as a
static binary constant at 1.000 Parity; anything that fails to resolve to an absolute yes or no "is
incinerated as entropy."

**3. A fixed reference beats a learned one.** Verification runs against The Root, a sovereign logic
center held in deliberate isolation, rather than against retrieved external data. The corpus frames
this as solving the grounding problem by fiat (`ARLF-03327`, `[E]`).

Claim 1 survived review intact. Claim 2 is the durable contribution and is what the successor
architecture implements. Claim 3 is what drew the charge of epistemic closure, and it is the claim
that remains genuinely contested in the record.

## Why the architectural reading is the framework

The distinction is not cosmetic. The two readings share an acronym and nothing else structural:

| | Architectural Recursive Logic Feedback | Affective Recursive Loop Framework |
|---|---|---|
| Signal closing the loop | Internal structural verification | Physiological and sentiment data |
| Replaces | The human rater's probabilistic subjectivity | The human rater's judgment entirely |
| Requires emotion recognition | No | Yes |
| Condemned by the review panel | No | Yes, unanimously |
| Status after 2026-05-30 | Present in White Paper v1.0 doctrine | Purged as a systemic hazard |
| Realized in the successor stack | Yes, as the 7-Layer No-Trust Stack | No, actively blocked at Layer 5 |

Four of the six critiques in the adversarial review and four of the six Black Paper disaster vectors
attach specifically to physiological sensing. Remove the affective gradient and they lose their
target. The architectural reading is the half of ARLF that no reviewer ever condemned, and it is the
half that has a realized implementation path.

## Structure of this specification

| File | Subject |
|---|---|
| `01_MECHANISM.md` | The recursive verification mechanism, the Jester as logic core, RLCF |
| `02_DETERMINISTIC_STACK.md` | The realized form: the 7-Layer No-Trust Stack, volumes, protocols, gaps |
| `03_STRUCTURAL_SEEDS.md` | The seven works assembled into the framework, and which carry forward |
| `variant/` | The affective branch: its specification, its review, its purge |

## Scope

ARLF is a module, not the whole system. Verified explicitly during review (`ARLF-03330`):

> The document provided was the Affective Recursive Loop Framework (ARLF), not the entire Citadel.
> [...] the technical meat of the submission was strictly the specialized module for replacing human
> feedback.

Note that the document submitted for review was the *affective* one. This is the central fact of the
record: the reading that went to the panel and was destroyed is not the reading that survived.

## Maturity

| Attribute | Value | Evidence |
|---|---|---|
| Doctrine | Stated in White Paper v1.0 | `ARLF-01575` |
| Architectural realization | 7-Layer No-Trust Stack, Layer 0 through Layer 7 | `ARLF-01575`, `ARLF-02104` |
| Artifact class | System Prompt | `ARLF-01758` |
| Maturity | Conceptual / Theoretical | `ARLF-01758`, `ARLF-01753` |
| Executable implementation | None in corpus | `U` |
| Loss function | Never specified | `U` |
| Benchmark or run log | None | `U` |

ARLF's peak was documentary throughout. The architectural reading has something the affective one
never had, which is a specified mechanism at the stack level with named layers and stated functions.
What it still lacks is the thing the review demanded: "Strip the metaphysical language and provide
the actual loss equations" (`ARLF-03333`, Table 6). No record in 4,911 answers that.

## Status

Peak capacity: **2026-06-04T06:03:09Z**, the White Paper v1.0 doctrinal statement. Determination and
the rejected candidates: `reports/PEAK_CAPACITY.md`. Verdict: `reports/VERDICT.md`. Disposition of
both readings: `reports/DISPOSITION.md`.
