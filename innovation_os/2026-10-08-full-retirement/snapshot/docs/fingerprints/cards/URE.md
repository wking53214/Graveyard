# CODE_IDENTITY_FINGERPRINT_CARD — URE (Universal Resilience Engine)

Source of record: `wking53214/touchstone` @ `0db5600`
Primary file: `specimens/superseded/ure-universal-resilience-engine-flattened.py`
(11,273 bytes, **0 newlines** — a flattened single-line source)
Fingerprinted: 2026-09-12

---

## 0. PROVENANCE AND STATUS — read first

URE's source exists. It is in TOUCHSTONE, a **specimen corpus**, under
`specimens/superseded/` — the directory that corpus reserves for "approaches
tried and replaced, kept beside what replaced them, with the reason recorded".
`[CODE]`

Three facts constrain every claim below:

1. **The file does not parse.** All line breaks were destroyed by a copy-paste
   through a chat interface. `ast.parse` raises `SyntaxError` at line 1;
   `wc -l` reports 0 lines while the file carries 11 KB. Structure below was
   recovered by regex, and is marked approximate where that matters. `[CODE]`
2. **Nothing imports or runs it.** `resilience_stability_kernel.py`'s header
   states URE's version of the shared energy primitive is deliberately not
   wired in, because "its regime classifier is hardcoded rather than derived
   from its inputs ... so it isn't a source of real logic to share, and nothing
   in this repo consumes it." `[CODE]`
3. **It is superseded by SRE.** See §9. This is the single most important fact
   about URE and it was not previously recorded anywhere in this archive.

So: URE is real code, preserved deliberately, **not running anywhere**, and
retained as a specimen rather than as a live system.

## 1. IDENTITY

- **System name** — Universal Resilience Engine. The expansion appears in the
  filename; the string "Universal Resilience" appears in no source file in any
  of the 24 repositories examined. `[CODE]`
- **Module type** — Single-module analytical engine.
- **Architectural role** — Telemetry-driven resilience/risk analytics.
- **Primary purpose** — Ingest an operational telemetry vector, measure drift
  from a baseline as a weighted-squared-deviation energy, classify an
  operational regime, and emit a composite risk score with an entropy modifier.
- **Status** — Superseded specimen. Not deployed, not consumed, not tested.

## 2. CORE IDENTITY SIGNATURE

- **Framework / family** — stdlib only: `math`, `dataclasses`, `datetime`,
  `enum`, `typing`. `[CODE]`
- **Dominant design patterns** — Config dataclass holding all tunables; a
  telemetry struct; a pipeline/monitor/classifier triple; one orchestrator
  composing them.
- **Control model** — Synchronous. A single `run_diagnostic_sweep` entry point.
- **State model** — Stateless per sweep; baseline supplied as an argument.
- **Decision model** — Threshold classification over computed scalars.
- **Determinism source** — Pure functions. No RNG, no clock dependence in the
  computation path.
- **External dependencies** — None.

## 3. FUNCTIONAL FINGERPRINT

- **Inputs** — `SystemMetricsTelemetry`: `containment_efficiency`,
  `processing_latency`, `recurrent_action_rate`, `dropout_rate`,
  `automation_trigger_rate`, `determinism_index`, `repeat_step_rate`,
  `reentry_rate`, `escalation_rate`, `abrupt_disconnect_rate`,
  `backlog_depth`. Plus a baseline of the same shape. `[CODE, approximate]`
- **Processing chain** — `[CODE]`
  `TelemetryIngestionPipeline.parse_vector` →
  `StabilityMonitor.calculate_system_energy` →
  `SystemRegimeClassifier.classify_current_regime` →
  `calculate_shannon_entropy` →
  `IntegratedResilienceOrchestrator.evaluate_composite_risk` →
  `run_diagnostic_sweep`
- **Outputs** — `ClassificationResult`, `RegimeClassificationProfile`,
  `DiagnosticEvaluationSummary`.

## 4. UNIQUE BEHAVIOURAL MARKERS

1. **Lyapunov-style tracking energy.** Verbatim from the source:
   ```
   accumulated_deviation += weight * ((current_val - baseline_val) ** 2)
   return 0.5 * accumulated_deviation
   ```
   A weighted sum of squared deviations from baseline, halved. The docstring
   calls it "Lyapunov-style tracking energy", and the hedge is accurate: it is
   a quadratic distance, not a Lyapunov exponent. `[CODE]`
2. **Shannon entropy over the regime probability vector** —
   `-Σ p·log(p)` for `p > 0`, computed over the classification distribution
   rather than over raw inputs. `[CODE]`
3. **Entropy as a risk *multiplier*, not an output.** `entropy_modifier_floor`
   0.5 and `entropy_modifier_sensitivity` 0.15 shape how much uncertainty
   amplifies the composite risk score. `[CODE]`
4. **Hardcoded regime distribution.** The classifier returns a distribution
   driven principally by `backlog_depth` through
   `regime_backlog_surge_weight` / `_saturated_weight` / `_stable_weight` and
   `regime_latency_weight` — not learned, not fitted. **This is the single
   most important caveat on the card.** It matches the handoff's own warning,
   and it is independently corroborated by
   `resilience_stability_kernel.py`'s header ("its regime classifier is
   hardcoded rather than derived from its inputs"). `[CODE]`

**Aspiration vs implementation.** The name says "Universal Resilience Engine".
The code is one stdlib module computing a quadratic drift score and a
threshold classification with a hand-weighted regime distribution. It is not
predictive, not learned, and not universal. Describing its classifier as an ML
model would be false.

## 5. CONTROL VARIABLES

`SystemResilienceConfig`, complete. `[CODE]` These values are the strongest
discriminator URE has, and §9 uses them.

| Field | Value |
| --- | --- |
| `stability_stable_threshold` | 1e-4 |
| `stability_marginal_threshold` | 1e-2 |
| `energy_threshold` | 0.10 |
| `risk_threshold` | 0.75 |
| `dropout_risk_weight` | 2.0 |
| `escalation_risk_weight` | 1.5 |
| `reentry_risk_weight` | 1.5 |
| `backlog_risk_weight` | 0.01 |
| `entropy_modifier_floor` | 0.5 |
| `entropy_modifier_sensitivity` | 0.15 |
| `novelty_uncertainty_weight` | 0.4 |
| `complexity_uncertainty_weight` | 0.6 |
| `demand_shock_dampening_factor` | 0.6 |
| `dropout_threshold_floor` | 0.05 |
| `regime_backlog_surge_weight` | 0.02 |
| `regime_backlog_saturated_weight` | 0.03 |
| `regime_latency_weight` | 0.01 |
| `regime_backlog_stable_weight` | 0.01 |

## 6. SECURITY / TRUST MARKERS

**None.** No authentication, authorization, validation, provenance, integrity,
audit, or cryptographic mechanism of any kind. No `hashlib`, no `hmac`. It is a
pure calculation module with no trust boundary. `[CODE]`

That absence is itself identifying: every other governance-family system in
this portfolio carries at least SHA-256 hashing.

## 7. STATE MACHINE IDENTITY

`OperationalRegime`: `STABLE`, `SURGE`, `RESOURCE_OVERLOAD`,
`ANOMALOUS_CRITICAL`, `SATURATED`, `CONTESTED`. `[CODE]`

A second enum carries `NEUTRAL`, `REGRESSIVE`, `RISK_INCREASING` — a trend
classification, probably `ClassificationResult`. `[CODE, approximate]`

No degraded/recovery/quarantine/freeze states. Regimes are classifications of
an observed system, not operating states of URE itself.

## 8. OUTPUT FINGERPRINT

`DiagnosticEvaluationSummary` carrying regime, energy, entropy and composite
risk. No schema version, no provenance, no chaining — contrast OBSERVE's
`FusedVerdict`, which carries all three.

## 9. ARCHITECTURAL CLASSIFICATION

- **Domain** — Operational resilience analytics (contact-centre / queue
  telemetry, judging by the metric vocabulary)
- **Layer** — Analytical, below governance
- **Role** — Capability provider
- **Classification** — **Member of a resilience-engine family**, see below.

### The resilience-engine family `[CODE]`

URE is not a standalone system. Four implementations of one design exist:

| Implementation | Location | State |
| --- | --- | --- |
| **URE** | `touchstone/specimens/superseded/` | Flattened, superseded, unconsumed |
| **SRE** (System Resilience Evaluator) | `touchstone/specimens/pairs/` | Flattened original + 570-line verified reconstruction |
| **SOLVAR** `LyapunovStabilityModule` | `touchstone/specimens/pairs/` | Same formula, IVR/cohort domain |
| **GOV4** `RegimeClassifier` | `ats/gov4_kernel.py` | Live, tested (14 tests pass) |

**URE and SRE are the same system under a systematic rename.** Every one of
URE's ten classes maps 1:1 to an SRE class, and the telemetry fields map
field-for-field: `[CODE]`

| URE | SRE |
| --- | --- |
| `IntegratedResilienceOrchestrator` | `SystemResilienceEvaluator` |
| `StabilityMonitor` | `SystemStabilityValidator` |
| `SystemRegimeClassifier` | `TelemetryProfileDetector` |
| `TelemetryIngestionPipeline` | `OperationalLoadPipeline` |
| `SystemMetricsTelemetry` | `TelemetryMetrics` |
| `RegimeClassificationProfile` | `ClassificationProfile` |
| `DiagnosticEvaluationSummary` | `AnalyticalReport` |
| `ClassificationResult` | `EvaluationVerdict` |
| `containment_efficiency` | `containment_ratio` |
| `processing_latency` | `processing_latency` *(identical)* |
| `recurrent_action_rate` | `recurrent_request_ratio` |
| `dropout_rate` | `termination_ratio` |
| `determinism_index` | `determinism_coefficient` |
| `repeat_step_rate` | `duplicate_execution_ratio` |
| `reentry_rate` | `reentry_coefficient` |
| `escalation_rate` | `escalation_ratio` |
| `backlog_depth` | `buffer_backlog_depth` |

Nine of nine telemetry fields correspond, one identically. This is systematic
synonym substitution, not convergent design.

**The shared numeric core.** SOLVAR's `LyapunovStabilityModule` and SRE's
`SystemStabilityValidator` implement the same weighted-squared-deviation
formula against the same two constants, `1e-4` and `1e-2` — URE's
`stability_stable_threshold` and `stability_marginal_threshold` exactly.
`resilience_stability_kernel.py` was built 2026-09-03 as the de-duplicated
implementation and its header states the conclusion directly: *"That isn't
coincidence — it's the same design, copy-pasted and reskinned per source
repo."* `[CODE]`

**GOV4 shares the vocabulary.** `ats/gov4_kernel.py`'s `Regime` enum is
`STABLE, SURGE, SATURATED, CONFUSION, ANOMALOUS, PANIC` — four of six members
shared with URE's. It carries a `LyapunovConfig` of weighted terms
(`w_latency` 0.20, `w_abort` 0.30, `w_reentry` 0.20, `w_load` 0.15, `w_det`
0.15) and computes entropy and energy the same way. `reentry_rate` and
`determinism_index` appear by those exact names in both. `[CODE]`

### Correction: URE is *not* an OBSERVE variant

An earlier version of `cards/OBSERVE.md` recorded shared architectural lineage
between URE and OBSERVE as one of four competing readings. With URE's source in
hand, that reading is the weakest of them:

| | URE | OBSERVE |
| --- | --- | --- |
| Regime members | STABLE, SURGE, RESOURCE_OVERLOAD, ANOMALOUS_CRITICAL, SATURATED, CONTESTED | STABLE, CAUTION, WARNING, CRITICAL |
| Shared members | — | `STABLE` only, which is generic |
| Drift energy | weighted squared deviation, halved | **none** |
| Stability constants | 1e-4 / 1e-2 | **none** |
| Metric domain | queue/ops telemetry | clinical vitals |
| Threshold names in common | — | **none** |
| Integrity mechanisms | none | SHA-256 parameter set, decision fingerprint, state-commitment chain |

OBSERVE shares only the generic combination — entropy, regimes, a composite
risk score — which is the combination that shows up wherever someone scores a
system and grades the result. The specific evidence, vocabulary and constants,
puts URE with **SRE, SOLVAR and GOV4**, and puts OBSERVE outside that family.

This is what the discriminator named in `UNRESOLVED.md` U-1 was for, and it
pointed away from the reading the earlier card leaned toward. Recorded as a
correction rather than quietly amended.

## 10. IMPLEMENTATION MATURITY

- **Scale** — 11,273 bytes, 1 line, 10 classes, 11 functions. `[EXPERIMENT]`
- **Parse status** — Does not parse. `SyntaxError` at line 1. `[EXPERIMENT]`
- **Test evidence** — **None.** No test references URE in any repository.
- **Executability** — Cannot be imported. Cannot have produced any result
  attributed to it in its current state.
- **Consumers** — None, by explicit design decision. `[CODE]`
- **Scaffold vs implementation** — Real implementation, structurally complete,
  in an unusable file format, deliberately retired in favour of SRE.

## 11. CODE DNA SUMMARY

A superseded, flattened, stdlib-only operational-resilience module that scores
drift from a telemetry baseline as a halved weighted sum of squared deviations
against 1e-4/1e-2 stability bands, classifies a six-member operational regime
from a hand-weighted distribution driven mainly by backlog depth, and amplifies
a composite risk score by the Shannon entropy of that distribution — carrying
no trust, integrity or audit mechanism of any kind, retained as a specimen
beside SRE, its own systematic rename and working reconstruction.
