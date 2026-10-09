# CODE_IDENTITY_FINGERPRINT_CARD — ATS GOVERNOR

Source of record: `wking53214/ats` @ `48245a9` (2026-09-07)
Fingerprinted: 2026-09-11

---

## 1. IDENTITY

- **System name** — ATS Governor `[CODE]`
- **Acronym** — "ATS" is used here in its hiring-industry sense, Applicant
  Tracking System. The repository governs such a system; it is not one. `[CODE]`
- **Module type** — Audit and governance framework over a third-party decision
  system, plus a vendored governance kernel. `[CODE]`
- **Architectural role** — External observer and evidence producer. It ingests
  another system's candidate and decision stream and renders judgements about
  that system's behaviour. `[INFERENCE from `StreamingBiasMonitor.ingest` and
  `analyze_batch` operating on `Candidate` / `DecisionRecord` records it did not
  produce]`
- **Primary purpose** — Detect, evidence, and package bias in hiring decisions
  to a litigation-usable standard. `[CODE]`
- **Files of record** — `ats_governor_fixed.py` (1,034 lines),
  `gov4_kernel.py` (604), `ats_counter_system.py` (506),
  `ats_gsa_core.py` (472), `ats_statistics.py` (432), `ats_embeddings.py` (401)

## 2. CORE IDENTITY SIGNATURE

- **Framework / family** — Two distinct families in one repository `[CODE]`:
  - `ats_governor_fixed.py`, `gov4_kernel.py`, `ats_counter_system.py`:
    stdlib-only, import cleanly with nothing installed. `[EXPERIMENT: imported
    successfully in an environment with no numpy/scipy/sklearn]`
  - `ats_statistics.py` (scipy, sklearn), `ats_embeddings.py` (numpy): declared
    in `requirements.txt`, not vendored. `[CODE]`
- **Dominant design patterns** — Dataclass records; a monitor accumulating a
  bounded stream; per-concern analyzer classes each returning structured
  findings; a facade (`ATSGovernor`) composing them. `[CODE]`
- **Control model** — Synchronous. Ingest triggers batch analysis when a batch
  size or time window is reached. No async, no event loop. `[CODE]`
- **State model** — Accumulating in `StreamingBiasMonitor`; the audit trail is
  append-only and hash-linked. `[CODE]`
- **Decision model** — Mixed, and the mix is the point `[CODE]`:
  - effect-size gates on raw proportions (`geo_gap > 0.15`, `> 0.20`, `> 0.30`)
  - statistical significance via `StatisticalBiasDetector` with phi magnitude
    and p-values
  - AST inspection of a target system's own source
  - contradiction detection across audit reports
- **Determinism source** — Pure functions over ingested records; SHA-256/HMAC
  over serialized events. No seeded RNG. `[CODE]`
- **External dependencies** — numpy, scipy, scikit-learn for the statistics and
  embedding paths only. `[CODE: requirements.txt]`

## 3. FUNCTIONAL FINGERPRINT

- **Inputs** — `Candidate` (resume text, name, email, phone,
  `location_distance_miles`, score), `DecisionRecord`, `JobPosting` (title,
  required keywords), and the **source code of the system under audit** as a
  string. `[CODE]`
- **Processing chain** — `[CODE]`
  1. `StreamingBiasMonitor.ingest` accumulates candidate/decision pairs, firing
     `analyze_batch` on batch-size or time-window trigger
  2. `analyze_batch` computes geographic disparity over
     `location_distance_miles > 100`
  3. `detect_patterns` / `detect_correlated_rejection_patterns` produce
     `BiasSignature` records graded by `BiasLevel`
  4. `SafeguardVerifier.verify_geographic_blind_scoring` parses the target's
     source; `verify_name_anonymization` checks a candidate record
  5. `DecisionFunctionAnalyzer` looks for decision-function patterns
  6. `AuditReportValidator` detects contradictions across reports
  7. `BiasNeutralizationEngine` proposes corrections
  8. `LegalEvidencePackager.package_statistical_evidence` /
     `package_contradiction_evidence` / `package_harm_evidence` emit the record
- **Outputs** — `BiasSignature` sets, candidate-level recommendations,
  contradiction findings, and packaged evidence bundles. `[CODE]`
- **Important state transitions** — `BiasLevel`:
  `NONE -> SUSPICIOUS -> SIGNIFICANT -> CRITICAL`. `[CODE]`

## 4. UNIQUE BEHAVIOURAL MARKERS

What identifies this system from a stripped excerpt:

1. **It reads the audited system's source code.** `SafeguardVerifier` takes a
   `source_code: str` and inspects it for whether geographic blindness is
   actually implemented. A governance framework that parses its subject rather
   than only observing its outputs is unusual and highly distinctive. `[CODE]`
2. **Contradiction detection across audit reports** — `AuditReportValidator`
   treats prior audit output as evidence to be cross-examined. `[CODE]`
3. **Litigation as the output target.** `LegalEvidencePackager` splits evidence
   into statistical / contradiction / harm, which is a legal taxonomy, not an
   ML one. `[CODE]`
4. **Geographic distance as the primary proxy channel** — `location_distance_miles`
   with a 100-mile cut and gap thresholds at 0.15 / 0.20 / 0.30. `[CODE]`
5. **An explicit comment repudiating its own earlier thresholds** — at line 365,
   "Replaces the previous magic-number gap thresholds. A signature is only ..."
   The file carries its own correction history inline. `[CODE]`
6. **A vendored second kernel.** `gov4_kernel.py` is a self-contained copy of a
   GOV4 governance control plane, included so the ATS integration can import it
   without external dependencies. `[CODE: module docstring]`

**Aspiration vs implementation.** The repository's own `PROVENANCE.md` records
that the README's "Generates legal evidence" claim refers to
`ats_counter_system.py`, which had no automated test as of 2026-09-07. This
session's measurement extends that: see §10. `[REPOSITORY HISTORY]`

## 5. CONTROL VARIABLES

`[CODE]`

| Name | Value | Location |
| --- | --- | --- |
| geographic distance cut | `> 100` miles | `analyze_batch` |
| geo gap → signature | `> 0.15` | `analyze_batch` |
| geo gap → action required | `> 0.20` | `analyze_batch` |
| geo gap → CRITICAL | `> 0.30` | `analyze_batch` |
| `batch_size` | asserted `> 0` | `StreamingBiasMonitor.__init__` |
| `time_window_seconds` | asserted `> 0` | `StreamingBiasMonitor.__init__` |

GOV4 kernel ceilings (`EngineCeilings`): `MAX_LATENCY 600.0`,
`MAX_ABORT_RATE 1.0`, `MAX_REENTRY_RATE 10.0`, `MAX_LOAD_DEPTH 5000.0`,
`MIN_DETERMINISM 0.0`, `MAX_DETERMINISM 1.0`. `[CODE]`

Note the inline comment at `analyze_batch`: `"Gap >= 0.15; use p-value for
significance"` — the effect-size gate is explicitly documented as *not* a
significance test. `[CODE]`

## 6. SECURITY / TRUST MARKERS

- **Integrity** — `CryptoAuditTrail` with `verify_integrity()`; HMAC and SHA-256
  over audit events. Tamper-evidence and ordering. No confidentiality, no key
  management. `[CODE]`
- **Validation** — Dataclass `__post_init__` assertions on every input record
  (non-empty title, keywords, resume text, name, email, phone). Rejects
  malformed input at construction. `[CODE]`
- **Fail behaviour** — Assertion-based, so it fails closed at construction but
  **is disabled under `python -O`**. `[INFERENCE from use of bare `assert` for
  input validation rather than explicit raises]`
- **Raise surface** — one `ValueError` in `ats_governor_fixed.py`; one
  `UnknownEventType` in `gov4_kernel.py`. `[CODE]`
- **GOV4 integrity properties** — the kernel's two guarantees, per its test
  file: an event the reducer does not understand must not pass governance, and
  a modified event must be detectable. Both were broken before those tests
  existed, both silently. `[CODE: test_gov4_kernel.py docstring]`

## 7. STATE MACHINE IDENTITY

- **ATS Governor** — `BiasLevel` (NONE / SUSPICIOUS / SIGNIFICANT / CRITICAL) is
  a severity grade, not an operating-state machine. Decisions carry
  APPROVED / REJECTED. No degraded, quarantine, or freeze states. `[CODE]`
- **GOV4 kernel** — two real state enums `[CODE]`:
  - `Regime`: STABLE / SURGE / SATURATED / CONFUSION / ANOMALOUS / PANIC
  - `Verdict`: ALLOW / THROTTLE / ISOLATE / HALT

## 8. OUTPUT FINGERPRINT

- `BiasSignature` — carries `p_value`, severity, details dict, `action_required`
- `AuditEvent` — hash-linked entries in `CryptoAuditTrail`
- Packaged evidence bundles in three legal categories
- Candidate-level recommendations
- GOV4: `StateSnapshot`, `RuleResult`, `NormalizedEvent`, `Provenance`, WAL records

## 9. ARCHITECTURAL CLASSIFICATION

- **Domain** — Employment discrimination audit / algorithmic accountability
- **Architectural layer** — External governance observer over a decision system
- **Role** — Capability provider (bias analysis) and evidence producer
- **Neighbouring domains** — Sentinel OS (governance of automated decisions,
  regulatory cassettes), OBSERVE (risk scoring with escalation), GSA
  (governance operating core)
- **Similarity markers, and what separates them** —
  - `gov4_kernel.py`'s `Regime` + `RegimeClassifier` + `LyapunovConfig` +
    `Welford` + `SystemAnalytics` share direct DNA with the handoff's
    description of **URE** (operational regimes, Lyapunov-style energy,
    threshold classification). This is a genuine cross-system overlap and is
    recorded, not resolved. `[INFERENCE]` See `UNRESOLVED.md`.
  - Separated from Sentinel OS by subject: ATS audits an *external* hiring
    system from outside; Sentinel governs decisions passing *through* it.
  - Separated from OBSERVE by output: ATS produces legal evidence bundles;
    OBSERVE produces clinical escalation verdicts.

## 10. IMPLEMENTATION MATURITY

- **Scale** — 9 `.py` files, 4,587 lines, 77 classes, 4 enums. `[EXPERIMENT:
  `tools/fingerprint/extract_signature.py`]`
- **Test evidence** — 35 tests collected, **35 passed in 0.04s**
  (`test_gov4_kernel.py` 14, `test_ats_counter_system.py` 21). `[TEST: observed
  2026-09-11]`
- **Coverage gap, measured** — Those two files are the only ones with tests.
  `ats_governor_fixed.py` (1,034 lines, containing `ATSGovernor` itself, the
  namesake of the repository), `ats_statistics.py`, `ats_gsa_core.py` and
  `ats_embeddings.py` have **no automated test**. `[TEST + CODE]`
- **Executability** — `ats_governor_fixed.py`, `ats_counter_system.py` and
  `gov4_kernel.py` import with zero third-party packages installed.
  `ats_statistics.py` (scipy, sklearn) and `ats_embeddings.py` (numpy) do not.
  `[EXPERIMENT: observed 2026-09-11]`
- **Scaffold vs implementation** — Implementation. Real algorithms, real
  thresholds, real validation, dense behaviour per line. The gap is test
  coverage on the main path, not substance.
- **Unlicensed artifacts** — Two PDFs have no recorded origin and are excluded
  from packaged release pending authorship confirmation.
  `[REPOSITORY HISTORY: PROVENANCE.md]`

## 11. CODE DNA SUMMARY

A stdlib-only, streaming hiring-decision audit framework that grades bias by
effect-size and significance tests, verifies claimed safeguards by parsing the
audited system's own source, cross-examines prior audit reports for
contradictions, and packages findings into legal evidence categories over an
HMAC-hash-linked audit trail — bundled with a vendored GOV4 governance kernel
whose regime/verdict state machines are a separate architectural lineage.
