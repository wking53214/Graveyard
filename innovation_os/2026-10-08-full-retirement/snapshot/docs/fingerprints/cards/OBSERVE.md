# CODE_IDENTITY_FINGERPRINT_CARD — OBSERVE

Source of record: `wking53214/observe` @ `9138bed` (2026-09-11)
Primary file: `observe_consolidated.py` (1,510 lines)
Fingerprinted: 2026-09-11

---

## 1. IDENTITY

- **System name** — OBSERVE (self-titled "OBSERVE Clinical AI System —
  Consolidated (v2)") `[CODE: module docstring]`
- **Acronym** — Not expanded anywhere in the source. `UNKNOWN`
- **Module type** — Risk assessment and escalation engine.
- **Architectural role** — Evidence-first clinical risk scorer. It produces
  graded verdicts with cryptographic continuity; it does not act on them.
  `[INFERENCE from `compute_state_commitment` docstring: binds state "without
  claiming underlying truth or authority"]`
- **Primary purpose** — Fuse multi-channel pediatric vitals into a risk score,
  classify an operational regime, and decide whether escalation is required,
  with every verdict independently replayable. `[CODE]`
- **Paired system** — `perceive_consolidated.py` (1,172 lines), the PERCEIVE
  governance kernel. OBSERVE scores; PERCEIVE authorises. They are separate
  systems with separate cards.

## 2. CORE IDENTITY SIGNATURE

- **Framework / family** — stdlib-only (`asyncio`, `hashlib`, `math`,
  `dataclasses`, `datetime`, `enum`, `collections`). No numpy, no ML runtime.
  `[CODE]`
- **Dominant design patterns** — Frozen-ish dataclass records; a bank of
  per-channel adapters; Bayesian fusion over adapter outputs; a policy object
  holding hysteresis state; an append-only ledger.
- **Control model** — Async job scheduler (`AsyncJobScheduler`, `JobQueue`)
  driving a synchronous scoring path. `[CODE]`
- **State model** — Per-patient continuity chain. Each verdict carries the
  previous verdict's commitment. `[CODE: `_patient_state_commitments`]`
- **Decision model** — Layered `[CODE]`:
  1. physical-plausibility validation producing fault strings
  2. per-channel risk adapters
  3. Bayesian fusion weighted by confidence
  4. a **hand-authored band table** mapping risk score to a regime probability
     distribution
  5. true Shannon entropy over that distribution
  6. hysteresis (dwell + cooldown lock) before a regime change commits
- **Determinism source** — Canonical JSON + SHA-256 throughout; no RNG in the
  scoring path. `[CODE]`
- **External dependencies** — None for `observe_consolidated.py`. The variant at
  `sentinel_os/observe_consolidated.py` additionally imports
  `kalman_trajectory`. `[CODE]`

## 3. FUNCTIONAL FINGERPRINT

- **Inputs** — `VitalsSnapshot` (patient id, timestamp, physiological channels).
- **Processing chain** — `[CODE]`
  `validate_vitals` → per-channel `RiskAdapters` / `RiskAdaptersPhysiological`
  → `BayesianFusion` → `regime_distribution(risk_score)` → Shannon entropy
  → `EscalationPolicy.evaluate` (dwell/lock hysteresis) → `FusedVerdict`
  → `ImmutableAuditLedger`
- **Outputs** — `FusedVerdict` carrying `risk_score`, `regime`, `confidence`,
  `entropy`, `validation_faults`, `unassessable`, `parameter_set_version`,
  `decision_fingerprint`, `predecessor_state_commitment`, `state_commitment`.
- **Important state transitions** — `OperationalRegime`
  STABLE → CAUTION → WARNING → CRITICAL, ordered by `_REGIME_SEVERITY` and
  combined via `_max_severity`. A change requires
  `ESCALATION_DWELL_THRESHOLD = 2` consecutive confirming readings, unless
  heuristic risk ≥ `HEURISTIC_HARD_RULE_THRESHOLD = 0.5`, which bypasses
  hysteresis. After escalation a 300-second lock suppresses further changes.
  `[CODE]`

## 4. UNIQUE BEHAVIOURAL MARKERS

1. **Parameter-set version as a SHA-256 of the live calibration surface.**
   `PARAMETER_SET_VERSION = sha256(canonical_json(PARAMETER_SET))`, where
   `PARAMETER_SET`'s entries *reference the module constants directly*. Editing
   any constant changes the hash, and the hash is stamped onto every verdict.
   Parameter drift between two builds is therefore detectable from the output
   alone. `[CODE]` This is the strongest single identifying marker.
2. **Per-patient hash-chained verdict continuity.** `compute_state_commitment`
   binds serialized decision state to its predecessor's commitment, explicitly
   scoped to continuity "without claiming underlying truth or authority".
   `[CODE]`
3. **Entropy as a control signal, not just a report.**
   `HEAVY_PATH_ENTROPY_TRIGGER = 0.6` — entropy above this pulls in the heavy
   engine set. Uncertainty routes computation. `[CODE]`
4. **Asymmetric hysteresis.** Dwell requirement plus a post-escalation cooldown
   lock, with an explicit hard-rule bypass for high heuristic risk. The system
   is deliberately slow to change regime but fast to escalate on a hard rule.
   `[CODE]`
5. **`unassessable` as a first-class outcome.** A faulted channel does not
   produce a wrong score; it multiplies fused confidence by
   `UNASSESSABLE_CONFIDENCE_PENALTY = 0.5` and flags the verdict. Declining to
   assess is a modelled result, not an error. `[CODE]`
6. **A band table, not a model.** See §5 and the maturity note below.

**Aspiration vs implementation.** `regime_distribution` is a four-row lookup
table over risk-score bands, not a learned or predictive classifier. The code is
honest about this: the function's docstring describes it as a fix replacing
"broken linear-scaling distributions", and the table is labelled a "CALIBRATION
SURFACE ... single source of truth". A card must not describe this as a
probabilistic model. It is a hand-tuned calibration curve whose entropy is
computed exactly. `[CODE]`

## 5. CONTROL VARIABLES

`[CODE]`

`REGIME_DISTRIBUTION_BANDS` (inclusive lower risk bound → distribution):

| Risk ≥ | stable | caution | warning | critical |
| --- | --- | --- | --- | --- |
| 0.75 | 0.05 | 0.10 | 0.25 | 0.60 |
| 0.50 | 0.10 | 0.20 | 0.55 | 0.15 |
| 0.25 | 0.35 | 0.50 | 0.12 | 0.03 |
| 0.00 | 0.88 | 0.08 | 0.03 | 0.01 |

| Constant | Value |
| --- | --- |
| `DRIFT_SIGMA_THRESHOLD` | 2.0 |
| `UNASSESSABLE_CONFIDENCE_PENALTY` | 0.5 |
| `REGIME_CRITICAL_FLOOR_DEFAULT` | 0.01 |
| `DRIFT_CRITICAL_FLOOR` | 0.02 |
| `HEAVY_PATH_ENTROPY_TRIGGER` | 0.6 |
| `HEURISTIC_HARD_RULE_THRESHOLD` | 0.5 |
| `ESCALATION_DWELL_THRESHOLD` | 2 |
| `ESCALATION_LOCK_SECONDS` | 300 |

`REGIME_CRITICAL_FLOOR_DEFAULT` exists so critical probability never reaches
zero — "residual clinical uncertainty" per the source. A floor on the worst case
is a domain-specific safety choice and is itself a fingerprint. `[CODE]`

## 6. SECURITY / TRUST MARKERS

- **Integrity** — SHA-256 over canonical JSON for parameter set, decision
  fingerprint, and state commitments. `ImmutableAuditLedger` is append-only.
  `[CODE]`
- **What it is not** — No HMAC, no keys, no signing, no encryption in
  `observe_consolidated.py`. Tamper-evidence and replayability only; an
  attacker who can rewrite the ledger can recompute the hashes. `[CODE:
  `crypto_hits` = hashlib, sha256 only]`
- **Validation** — `validate_vitals` performs physical-plausibility checking and
  returns fault strings rather than raising. `[CODE]`
- **Fail behaviour** — Degrades rather than fails closed: faults reduce
  confidence and set `unassessable`, and processing continues. `[CODE]`
- **Authority boundary** — Explicitly disclaims authority (§4.2). Authorisation
  is PERCEIVE's job. `[CODE]`

## 7. STATE MACHINE IDENTITY

- **Normal** — STABLE
- **Degraded** — CAUTION, WARNING
- **Failure/critical** — CRITICAL
- **Escalation** — `escalation_required`, gated by dwell count
- **Recovery** — regime de-escalation, blocked while `escalation_locked`
- **Quarantine** — none. `unassessable` is the nearest analogue and is a
  confidence penalty, not a state. `[CODE]`

## 8. OUTPUT FINGERPRINT

`FusedVerdict` is the characteristic artifact. Its distinguishing property is
that it is **self-describing for replay**: risk, regime, confidence and entropy
are rounded to 9 decimal places, and the verdict carries the parameter-set hash,
its own decision fingerprint, and its predecessor's commitment. Two verdicts from
different builds can be compared and the divergence attributed. `[CODE]`

## 9. ARCHITECTURAL CLASSIFICATION

- **Domain** — Clinical decision support (pediatric deterioration)
- **Architectural layer** — Scoring / perception, below governance
- **Role** — Capability provider
- **Neighbouring domains** — PERCEIVE (policy authorisation), Sentinel OS
  (custody ledger), ATS Governor (audit)
- **Similarity markers, and what separates them** — see below.

### RESOLVED 2026-09-12: OBSERVE is not in URE's family

URE's source was located in `touchstone/specimens/superseded/` by the portfolio
census. With the actual control variables in hand, the question below is
settled, and **against** the direction this section previously leaned.

URE belongs to a resilience-engine family with SRE, SOLVAR's
`LyapunovStabilityModule` and ATS's GOV4 `RegimeClassifier`, which share a
weighted-squared-deviation energy formula, the constants 1e-4 and 1e-2, and an
ops-telemetry vocabulary (`reentry_rate`, `determinism_index`, `backlog_depth`).

OBSERVE has **none** of those: no drift energy, no shared constants, no shared
threshold names, and a regime enum (STABLE/CAUTION/WARNING/CRITICAL) sharing
only the generic member `STABLE`. What OBSERVE shares with URE is the
combination of entropy, regimes and a composite risk score — which is what any
system scoring a subject and grading the result tends to look like.

Full comparison and evidence: `cards/URE.md` §9. The section below is kept as
written, because the reasoning it records — four readings, none preferred — is
what made the discriminator worth running.

### Overlap with the handoff's URE description `[INFERENCE, superseded above]`

The handoff describes URE as a telemetry-driven resilience engine with
operational regimes, Shannon entropy, composite risk scoring, threshold
classification, and a regime classifier containing "a simulated/mock
distribution driven primarily by `backlog_depth`".

OBSERVE contains the same architecture with a different input domain:
`OperationalRegime`, true Shannon entropy over a regime distribution, composite
risk scoring, threshold classification, and a **hand-authored band table driven
by `risk_score`**.

These are structurally the same design. What that similarity *means* is
`UNKNOWN`, and at least four readings fit the evidence equally well:

1. **Shared lineage** — OBSERVE is a domain fork of URE, or both fork a common
   ancestor.
2. **Reverse direction** — URE generalises a pattern OBSERVE established first.
3. **Author habit** — the same author independently reaching for the same
   components across projects. No shared code, but a real stylistic signature.
4. **Convergent design** — the components (Shannon entropy over a probability
   distribution, an ordered regime enum, threshold classification, a composite
   risk score) are individually standard. Two engineers solving this problem
   could arrive here without contact.

Nothing in the available evidence discriminates between these. Note that (3) and
(4) produce the same surface similarity as (1) while implying no code
relationship at all — so structural resemblance alone cannot establish lineage,
and treating it as though it does is the error this archive exists to prevent.

The comparison is against the handoff text, which is `[EXTERNAL SOURCE]`: no
file named or self-identifying as URE was found in any repository attached to
this session.

It is recorded as an overlap. The cards stay separate. Discriminating between
the four readings requires the URE source and, ideally, commit dates on both.
See `UNRESOLVED.md`.

### On the handoff's remembered OBSERVE markers

The handoff lists distinctive OBSERVE markers including hash-chained audit
lineage, governance approval gates, drift freeze/quarantine, HMAC-SHA256
pseudonymization, schema-versioned state-vector export, exponential decay
weighting, and sliding temporal windows.

Checked against this code `[CODE]`:

| Marker | Status in `observe_consolidated.py` |
| --- | --- |
| Hash-chained lineage | **Present**, as `predecessor_state_commitment` / `state_commitment` |
| Schema-versioned state export | **Present**, as `PARAMETER_SET_VERSION` |
| Nonlinear telemetry interpretation | **Present**, as the band table + Bayesian fusion |
| Trajectory analysis | **Partial** — `trajectory` and `momentum` referenced; the Kalman variant lives in `sentinel_os/observe_consolidated.py` |
| Drift freeze / quarantine | **Partial** — `escalation_locked` cooldown is a freeze; no quarantine state |
| Sliding temporal windows | **Weak** — 7 `deque`/`window` references |
| Exponential decay weighting | **Absent** — no decay, ewm, or alpha term |
| HMAC-SHA256 pseudonymization | **Absent** — no HMAC; pseudonymization lives in `sentinel_os/compliance_exporters.py` |
| Governance approval gates | **Absent** — that is PERCEIVE's `ConsensusEngine` |

Two of the nine are absent here and live in *other* systems in the same
repository. This is exactly the drift the archive exists to catch: a remembered
fingerprint accreted capabilities from neighbouring modules. Note also that a
naive keyword search for the handoff's own terms under-reports the matches,
because the code names the same mechanisms differently — which is the handoff's
own argument for why keyword search is insufficient, demonstrated on itself.

## 10. IMPLEMENTATION MATURITY

- **Scale** — 1,510 lines, 13 classes, 2 enums, 8 named tunables. `[EXPERIMENT]`
- **Structural density** — High. Named thresholds with justifying comments,
  ordered severity, explicit invariants.
- **Test evidence** — `test_observe_consolidated.py` (857 lines) exists and the
  source references `test_observe_invariants.py` asserting each `PARAMETER_SET`
  entry tracks its live constant. **Not executed in this session.** `[CODE]`,
  not `[TEST]`.
- **Duplication** — Two divergent copies: `observe_consolidated.py` (1,510
  lines, root) and `sentinel_os/observe_consolidated.py` (1,408 lines, imports
  `kalman_trajectory`, uses `threading`, carries fewer hoisted constants). They
  are not the same system state. `[CODE]` See `UNRESOLVED.md`.
- **Scaffold vs implementation** — Implementation, and among the most mature
  code in the portfolio by density of justified control variables.

## 11. CODE DNA SUMMARY

A stdlib-only clinical risk engine that fuses validated multi-channel vitals
into a composite score, maps it through a hand-authored calibration band table
to an operational-regime probability distribution, uses the Shannon entropy of
that distribution to route computation, commits regime changes only through
dwell-and-cooldown hysteresis with a hard-rule bypass, and stamps every verdict
with a SHA-256 of its own live calibration surface plus a chained commitment to
the patient's previous verdict so that any verdict is independently replayable
and parameter drift is detectable from the output alone.
