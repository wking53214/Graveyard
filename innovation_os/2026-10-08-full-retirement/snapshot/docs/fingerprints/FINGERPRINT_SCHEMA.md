# Fingerprint card schema

Every card under `cards/` uses these sections in this order. A section with
nothing established says `UNKNOWN`; it is never deleted, because the absence of
a state machine or a security model is itself part of a system's identity.

Every substantive claim carries an evidence tag from `README.md`.

---

## 1. IDENTITY

- **System name** — as the code and its repository use it.
- **Acronym** — expanded if the expansion is evidenced; `UNKNOWN` if it is folklore.
- **Module type** — kernel / engine / adapter / harness / library / application / scaffold.
- **Architectural role** — the job it holds in a larger composition.
- **Primary purpose** — one sentence, derived from behaviour.
- **Source of record** — repository, path, commit.

## 2. CORE IDENTITY SIGNATURE

- **Framework / family** — stdlib-only, numpy, async, framework-bound.
- **Dominant design patterns** — what recurs structurally.
- **Control model** — synchronous call chain, async, event loop, reducer, pipeline.
- **State model** — immutable / accumulating / event-sourced / stateless.
- **Decision model** — threshold, rule, policy VM, statistical, consensus, learned.
- **Determinism source** — seeded RNG, canonical serialization, pure functions, or none.
- **External dependencies** — what it cannot run without.

## 3. FUNCTIONAL FINGERPRINT

- **Inputs** — what it consumes and in what shape.
- **Processing chain** — the ordered stages, as the code performs them.
- **Outputs** — what it emits.
- **Transformations** — what materially changes between input and output.
- **Important state transitions** — what moves and what triggers it.

## 4. UNIQUE BEHAVIOURAL MARKERS

The section that does the actual discriminating work. What would let someone
identify this system from a code excerpt with the names stripped out?

Prefer: distinctive algorithms, unusual mathematical models, specific state
machines, cryptographic mechanisms, specialized data structures, governance
controls, orchestration patterns, validation mechanisms, persistence models,
characteristic output shapes.

**Record aspiration separately.** Where a name or docstring claims a behaviour
the code does not implement, both go on the card: the claim, and what is
actually there. That mismatch is often the single most identifying fact about a
module, and it is what stops a later reader from re-importing the claim as fact.

## 5. CONTROL VARIABLES

Constants, thresholds, limits, seeds, tunables, configuration structures,
scoring weights, policy values. Give names and values; the specific numbers are
frequently the strongest fingerprint a system has.

## 6. SECURITY / TRUST MARKERS

Authentication, authorization, validation, provenance, integrity, cryptographic
mechanisms, fail-closed vs fail-open behaviour, quarantine, freeze states, audit.

State the actual property, not the label. "SHA-256 hash chain, tamper-evidence
and ordering only, no confidentiality, no key management" — not "cryptographic".

## 7. STATE MACHINE IDENTITY

Normal, degraded, failure, escalation, recovery, and quarantine states, plus
what moves between them. `UNKNOWN` or "none" is a real and common answer.

## 8. OUTPUT FINGERPRINT

The characteristic artifacts the system produces, including shape and any
schema versioning. Output structure is durable identity: it survives refactors
that rename everything inside.

## 9. ARCHITECTURAL CLASSIFICATION

- **Domain**
- **Architectural layer**
- **Role**
- **Neighbouring domains**
- **Similarity markers** — which other systems in the archive this resembles,
  and, explicitly, what still separates them.

## 10. IMPLEMENTATION MATURITY

Not in the original card format; added because the portfolio needs it. The
sections above describe what the system is organised to do. This one records
how much of that exists, with measurements rather than adjectives.

- **Scale** — files, lines.
- **Structural density** — enums, tunables, raise sites per line. A subsystem
  with no enums and almost no raise sites has no state machine and no
  fail-closed surface, whatever its class names suggest.
- **Test evidence** — count and observed result, or `UNKNOWN`.
- **Executability** — does it run from a clone? What is missing?
- **Scaffold vs implementation** — stated plainly.

## 11. CODE DNA SUMMARY

One sentence describing the system's actual code-derived identity. It must be
defensible to someone reading the source with the card in hand. If the honest
sentence is less impressive than the system's name, the honest sentence wins.
