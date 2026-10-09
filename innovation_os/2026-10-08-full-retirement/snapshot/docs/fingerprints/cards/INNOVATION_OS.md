# CODE_IDENTITY_FINGERPRINT_CARD — INNOVATION OS

Source of record: `wking53214/innovation_os` @ `3bb189d` (2026-09-07)
Fingerprinted: 2026-09-11

This card covers the repository as a whole and treats `src/innovation_os/` and
`src/innovation_os/intelligence/` separately, because they have materially
different identities and materially different maturity.

---

## 1. IDENTITY

- **System name** — Innovation OS `[CODE]`
- **Module type** — Application framework. A wide, shallow set of small engines
  over dataclass models. `[CODE]`
- **Architectural role** — Traceability spine for a decision lifecycle. `[CODE]`
- **Primary purpose** — Preserve the relationship between a problem, the
  alternatives considered, the evaluation performed, the decision made, and the
  authorisation that permits implementation, so a decision can be examined in
  context rather than only as its output. `[CODE + README]`
- **Governing principle** — "AI proposes. Systems evaluate. Humans authorize."
  This is load-bearing: it is the reason provenance distinguishes *who
  originated* an artifact from *where it came from*. `[CODE:
  `provenance/provenance.py` module docstring]`

## 2. CORE IDENTITY SIGNATURE

- **Framework / family** — stdlib-only. `dataclasses`, `datetime`, `typing`,
  `enum`, `hashlib`. No web framework, no ORM, no numpy in the core. `[CODE]`
- **Dominant design patterns** — One package per concept; a `models.py` of
  dataclasses plus an `engine.py` of operations; in-memory stores.
- **Control model** — Synchronous method calls. No async anywhere. `[CODE]`
- **State model** — In-memory and accumulating. `storage/database.py` is 139
  lines. `[CODE]`
- **Decision model** — Rule and state-machine based; explicit status
  transitions rather than scoring.
- **Determinism source** — Canonical serialization plus SHA-256 in
  `LineageEngine` (`canonicalize_artifact`, `hash_artifact`). `[CODE]`
- **External dependencies** — None required. Installs editable via
  `pyproject.toml`, `src/` layout. `[CODE]`

## 3. FUNCTIONAL FINGERPRINT

- **Inputs** — Problems, ideas, conversations, repository scans, code artifacts.
- **Processing chain** — the declared lifecycle `[CODE: ARCHITECTURE.md, and
  package names corroborate each stage exists]`:
  Problem → Ideation → Alignment → Review → Nature-inspired translation →
  Solution → Forecast / Code Registry → Human approval
- **Outputs** — Artifacts with provenance records, lineage edges, decision
  records, branch alternatives, review findings, approval records.
- **Important state transitions** — `ProvenanceStatus` transitions are recorded
  as `StatusTransition` objects retaining the prior status, never as a silent
  overwrite. `[CODE]`

## 4. UNIQUE BEHAVIOURAL MARKERS

The repository's real distinguishing work is concentrated in four packages.
They are the genuine substance of Innovation OS.

1. **Provenance separates origin from location.** `status` records *who*
   originated an artifact, under a closed "Article II" taxonomy; `source`
   records *where* it came from and "carries no authority claim". The module
   docstring states the two must not be conflated, and registration without an
   explicit status determination is a `TypeError`, "not a guess". 622 lines,
   the largest package outside `intelligence/`. `[CODE]`
2. **A status change is a recorded transition.** `StatusTransition` retains
   `from_status` so the prior determination survives the change. `[CODE]`
3. **Retry/oscillation guarding on regeneration.** `RetryGuardEngine` implements
   `detect_cycle`, `allow_reentry`, and `register_attempt` keyed on
   `(artifact_id, branch_id, parent_artifact_id, evidence_id, decision_state,
   artifact_hash, evidence_version)`. It exists to stop repeated regeneration
   that produces no materially new evidence. `[CODE]`
4. **Canonical artifact hashing** — `LineageEngine.canonicalize_artifact` +
   `hash_artifact` give a stable identity for a structure, which is what makes
   (3) possible. `[CODE]`
5. **A constitutional vocabulary.** The provenance module cites "Article II"
   and "Article II.A" as external governing text with its own event taxonomy,
   and is careful to mark where its own mapping is *not* constitutional. A
   codebase that distinguishes its implementation choices from the document
   that authorises them is unusual. `[CODE]`

**Aspiration vs implementation.** See §10. The gap between the architecture the
repository describes and the code that exists is the single most important fact
on this card, and the repository is partly honest about it already:
`CODEX_CONTEXT.md` flags the historical `decision/` vs `decisions/` overlap and
the two graph implementations, and instructs that they not be merged
incidentally. `[CODE]`

## 5. CONTROL VARIABLES

Sparse, and that is itself the signature. Across all 351 files: **5 named
tunables, 3 enums, 20 raise sites in 13,879 lines** — roughly one raise per 694
lines. `[EXPERIMENT: `tools/fingerprint/extract_signature.py`]`

For comparison, `sentinel_os` has 291 raise sites in 47,204 lines (one per 162)
and 17 tunables. A system with few thresholds and few raises is one that mostly
records rather than decides.

## 6. SECURITY / TRUST MARKERS

- **Integrity** — SHA-256 canonical hashing in `LineageEngine`. `[CODE]`
- **Provenance** — the strongest trust mechanism present, see §4.1.
- **Fail-closed surface** — Narrow. `RetryGuardEngine` fail-closes through
  `IntelligenceRuntime._guard_execution`, which raises `RuntimeError` on
  oscillation detection and on retry-budget exhaustion. `[CODE]`
- **Authentication / authorization** — None. `intelligence/governance/access_control.py`
  exists as a module name; the package totals 236 lines across 9 files. `[CODE]`
- **Cryptographic mechanisms** — `hashlib`/SHA-256 only. No HMAC, no signing,
  no keys. `[EXPERIMENT: `crypto_hits`]`

## 7. STATE MACHINE IDENTITY

- **Normal** — artifact statuses: PENDING, ACCEPTED, APPROVED, REJECTED `[CODE]`
- **Degraded / failure / quarantine / freeze** — **none**. `[EXPERIMENT: no
  state vocabulary beyond those four across the whole tree]`

A lifecycle state machine exists (`lifecycle/state_machine.py`, 126 lines). An
*operational* state machine — degradation, quarantine, recovery — does not.

## 8. OUTPUT FINGERPRINT

`ProvenanceRecord` (artifact_id, status, source, created, history),
`StatusTransition`, `LineageEdge`, `ProvenanceEvent`, decision and branch
records, and `IntelligenceArtifact` (identity, confidence, provenance,
metadata, payload).

## 9. ARCHITECTURAL CLASSIFICATION

- **Domain** — Innovation and decision lifecycle management
- **Architectural layer** — Application, above the governance stack
- **Role** — Traceability spine and record keeper
- **Neighbouring domains** — Sentinel OS (custody ledger and governance of
  automated decisions), OBSERVE/PERCEIVE (the governed action gate)
- **Declared future integrations** — "Sentinel OS, Synapsis, Governance systems,
  Simulation systems, Deployment runtime". Declared, not built: no import of any
  of them exists. `[CODE: docs/architecture/intelligence_v2/api/integration_contract.md]`
- **Similarity markers, and what separates them** — Innovation OS and Sentinel
  OS both centre on provenance, decisions, approval and audit. They are
  separated by *position*: Sentinel governs decisions made by other systems at
  runtime and must prove what happened after the fact; Innovation OS records how
  a decision came to be proposed in the first place. Sentinel's ledger is
  Postgres and event-sourced; Innovation OS's is in-memory dataclasses.

## 10. IMPLEMENTATION MATURITY

Measured, not characterised.

| Measure | `src/innovation_os/` total | of which `intelligence/` |
| --- | --- | --- |
| `.py` files | 351 | 160 |
| Lines | 13,879 | 4,700 |
| Mean lines/file | 40 | 29 |
| Files under 40 lines | 224 of 351 (64%) | — |
| Enums | 3 | **0** |
| Named tunables | 5 | 4 |
| Raise sites | 20 | **7** |
| Crypto primitives | hashlib, sha256 | 1 hit total |

`[EXPERIMENT: `tools/fingerprint/extract_signature.py`, 2026-09-11]`

**Test evidence** — 309 tests, **309 passed in 0.52s**, 629 assertions across
169 test files. `[TEST: observed 2026-09-11]`

A suite of 309 tests that completes in half a second performs no I/O, no
iteration at scale, and no non-trivial computation. Combined with the density
figures above, the conclusion is not in doubt: **`intelligence/` is scaffolding,
not implementation.** Representative, not cherry-picked:

```python
# intelligence/cognition/perceiver.py — the file in its entirety
@dataclass
class Perceiver:
    """Extracts meaning from observations."""
    def perceive(self, observation):
        return {"type": "perception", "input": observation}
```

`Reasoner.reason` has the same shape. `intelligence/repository/fingerprint_engine.py`
is 28 lines returning a dict of `path`, `dependencies`, and `consumer_count`.

**What is real.** Four packages carry genuine implementation:
`provenance/` (622), `lineage/` (433), `registry/` (356), `retry_guard/` (181),
plus `context_envelope/` (262) and `invariants/` (165). Within `intelligence/`,
`kernel/cognitive_kernel.py` is a working registry-and-dispatch router and
`runtime/runtime.py` (142 lines) is the only module that performs real
cross-boundary work.

**Scaffold vs implementation** — The repository is a well-organised, honestly
documented *architectural skeleton* with four load-bearing packages. The naming
describes an intended system; the code implements a small fraction of it. Both
facts belong on the card.

## 11. CODE DNA SUMMARY

A stdlib-only, synchronous, in-memory traceability spine for a
problem-to-authorisation decision lifecycle, whose genuine implemented substance
is a provenance store that refuses to conflate origin with location and refuses
to register an artifact without an explicit origin determination, a canonical
artifact-hashing lineage engine, and an oscillation/retry guard built on it —
surrounded by a 160-file, 4,700-line `intelligence/` subsystem that names a full
cognitive architecture but implements it as pass-through scaffolding with no
enums, no operational state machine, and seven raise sites.
