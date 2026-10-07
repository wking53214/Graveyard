# SEAM INVENTORY — wking53214/SAGE-K

**Repo state analyzed:** commit `baf5ec8` ("Rebuild as installable package; fix adapter sync/async bug and chain-verification bug"), HEAD at time of clone.
**Method:** full read of all 20 tracked files (~4,470 lines); import graph traced statically and confirmed by execution; test suite run (4 passed); environment gate and import-isolation behavior verified empirically.

---

## PHASE 1: COMPONENT ENUMERATION

**Total: 30 components. Enumeration is exhaustive for tracked files.**

### Python modules

| ID | Component | Lines |
|---|---|---|
| C1 | `sage_k/__init__.py` — package facade / re-export surface | 90 |
| C2 | `sage_k/scenarios.py` — scenario dataclass, lifecycle, hash binding, `ScenarioLibrary` | 266 |
| C3 | `sage_k/generator.py` — `ScenarioGenerator`, `InterpretationContext`, `ModelClient` protocol, `StubModelClient` | 211 |
| C4 | `sage_k/harness.py` — `TestHarness`, `TestRun`, `ScenarioResult`, `Resolver` protocol | 263 |
| C5 | `sage_k/drift.py` — `DriftAnalyzer`, `DriftReport`, `ZoneDrift`, `ToleranceConfig`, `calibration_suggestion` | 303 |
| C6 | `sage_k/realignment.py` — `RealignmentRecord`, `RealignmentTrail`, `Approver`, `VersionChange`, `RegulatoryEvent` | 370 |
| C7 | `sage_k/report.py` — `monthly_drift_report`, `annual_realignment_report` markdown renderers | 302 |
| C8 | `sage_k/kernel.py` — `Fortress` simulation kernel, guardrail classes, agents, audit-log writer | 443 |
| C9 | `sage_k/gsa_adapter.py` — `GsaUniversalAdapter`, `GsaContextEnvelope`, `compute_state_signature`, `GsaTemporalDoorwayGate` | 296 |
| C10 | `sage_k/graph_extractor.py` — `GraphExtractor` AST visitor, `extract_graph`, `ExtractorGsaAdapterModule` | 167 |

### Entry points and tests

| ID | Component |
|---|---|
| C11 | `tests/test_sanity.py` — 4 tests |
| C12 | `examples/run_kernel_stress_test.py` — `__main__` entry point |
| C13 | `examples/run_wrapped_kernel_demo.py` — `__main__` entry point |
| C14 | `examples/run_graph_extractor_demo.py` — `__main__` entry point |

### Configuration and metadata

| ID | Component |
|---|---|
| C15 | `pyproject.toml` — setuptools build config, `dependencies = []`, package find pattern `sage_k*` |
| C16 | `requirements.txt` — 8 pinned third-party packages |
| C17 | `.gitignore` |
| C18 | `README.md` |
| C19 | `PROVENANCE.md` |
| C20 | `TRANSCRIPT.md` — 1,352-line source conversation, retained verbatim |
| C27 | Git history / commit record (treated by C19 as evidentiary) |

### Data stores

| ID | Component |
|---|---|
| C21 | Scenario JSON file store — path supplied by caller at `ScenarioLibrary.save/load` |
| C22 | `fortress_audit.log` — HMAC-signed JSON-lines append log (gitignored; created on any kernel run) |

### External interfaces

| ID | Component |
|---|---|
| C23 | Environment variables: `FORTRESS_AUDIT_LOG`, `FORTRESS_AUDIT_KEY`, `FORTRESS_ENV`, `FORTRESS_RUN_ID` |
| C24 | `ModelClient` — external LLM interface (Protocol only; no production implementation in repo) |
| C25 | `Resolver` — external "Sentinel" interface (Protocol only; no implementation in repo) |
| C26 | `numpy` — optional soft dependency, `try/except ImportError` |

### Schemas (serialized or contract-bearing)

| ID | Component |
|---|---|
| C28 | `Scenario` schema — hash-bound, JSON-serialized |
| C29 | `GsaContextEnvelope` schema — frozen dataclass, crosses every adapter call |
| C30 | `RealignmentRecord` schema — hash-sealed, JSON-serialized |

**Coverage note:** no component was skipped. `__pycache__` artifacts are untracked build output and are excluded.

---

## PHASE 2: SEAM EXTRACTION

**Total: 39 seams (S1–S39).**

---

**SEAM ID:** S1
**NAME:** Package export surface (`__all__`)
**TYPE:** OTHER — visibility boundary: what the package name exposes versus what the package directory contains. Secondary: DATA
**SIDE A:** C1
**SIDE B:** C2, C3, C4, C5, C6, C7 (exported) / C8, C9, C10 (not exported)
**WHAT CROSSES:** 30 named symbols from six modules. Zero symbols from `kernel`, `gsa_adapter`, `graph_extractor`. [OBSERVED]
**CONTRACT:** A consumer writing `import sage_k` receives only the six-module symbol set; the other three modules require explicit submodule import. [OBSERVED]
**ENFORCEMENT:** Explicit `from .x import (...)` list plus `__all__` at `sage_k/__init__.py:28-90`. Verified by execution: after `import sage_k`, `sage_k.kernel` and `sage_k.gsa_adapter` are absent from `sys.modules`. [OBSERVED]
**LOCATION:** `sage_k/__init__.py:28-90`
**ORIGIN:** NO EVIDENCE — no comment, doc, or commit message explains the exclusion.
**DEPENDS ON:** none
**FAILURE MODE:** If the exclusion is unintentional, consumers of the package-level API silently cannot reach C8/C9/C10 and may conclude those components do not exist. C11–C14 do not rely on this seam; they import submodules directly.
**CONFIDENCE:** high — statically read and empirically confirmed.

---

**SEAM ID:** S2
**NAME:** Subsystem partition (no name in the system)
**TYPE:** OTHER — disjointness boundary: two module clusters share no import edge and no symbol. Secondary: none
**SIDE A:** C2, C3, C4, C5, C6, C7
**SIDE B:** C8, C9, C10
**WHAT CROSSES:** Nothing. Zero imports in either direction; zero shared symbols; zero shared vocabulary. Grep for `kernel|gsa_adapter|Fortress|GraphExtractor` across C1–C7 returns no hits; grep for `Sentinel|scenario|regulation|zone` across C8–C10 returns no hits. [OBSERVED]
**CONTRACT:** Neither side assumes anything about the other. [OBSERVED]
**ENFORCEMENT:** Absence of imports only. No packaging, namespace, or dependency mechanism holds this apart. [OBSERVED]
**LOCATION:** Full import graph. Cluster A internal edges: `generator→scenarios`, `harness→scenarios`, `drift→harness`, `realignment→drift`, `report→drift`, `report→realignment`. Cluster B internal edges: `kernel→gsa_adapter`, `graph_extractor→gsa_adapter`.
**ORIGIN:** NO EVIDENCE — C19 documents the provenance of C8/C9/C10 (extracted from a Gemini transcript) and says nothing about C2–C7. C20 contains no reference to C2–C7's subject matter. The commit that introduced both clusters gives one line of message covering only C8/C9.
**DEPENDS ON:** none
**FAILURE MODE:** Nothing breaks if it fails, because nothing crosses. If a future edge is added, no mechanism would report it.
**CONFIDENCE:** high — verified by both static grep and runtime module-loading check.

---

**SEAM ID:** S3
**NAME:** Approval gate (`Scenario.approve`)
**TYPE:** CONTROL — authority to make an expected answer authoritative crosses here. Secondary: IDENTITY, TIME, TRUST
**SIDE A:** C3 (AI generation), C2 (`PROPOSED` scenarios)
**SIDE B:** C2 (`APPROVED` scenarios), C4 (execution)
**WHAT CROSSES:** An `expected` option string, an approver identity string, and a rationale string, supplied by the caller of `approve()`. [OBSERVED]
**CONTRACT:** Side B assumes that any scenario in `APPROVED` had its expected answer supplied by a human at approval time and not at generation time; and that `expected` is one of `options`. [DOCUMENTED — `scenarios.py:146-153`, `generator.py:4-15`]
**ENFORCEMENT:** `approve()` raises `ValueError` on: re-approval of an already-approved scenario, `expected` not in `options`, or an empty/whitespace approver string. `is_runnable` requires `status in {APPROVED}` and `expected is not None`. `TestHarness.run` skips anything failing `is_runnable`. [OBSERVED — `scenarios.py:146-190`, `harness.py:198-204`]
**LOCATION:** `sage_k/scenarios.py` — `Scenario.approve`, `Scenario.reject`, `Scenario.retire`, `Scenario.is_runnable`, `RUNNABLE_STATUSES`; `sage_k/harness.py:197-204`
**ORIGIN:** DOCUMENTED — `scenarios.py:17-25` and `generator.py:4-15` both state the constraint as: generation is a creativity problem where models are strong, judgment is a liability problem that does not delegate.
**DEPENDS ON:** none
**FAILURE MODE:** If the gate fails, a machine-supplied expectation becomes the scored baseline, and the entire drift metric (C5) measures the model against itself. C4, C5, C6, C7 all rely on this.
**CONFIDENCE:** high — the checks are direct, unconditional, and in one place.

---

**SEAM ID:** S4
**NAME:** Content-hash binding
**TYPE:** TRUST — scenario content is validated before it is allowed to run. Secondary: DATA, PERSISTENCE
**SIDE A:** C2 (`Scenario.content_hash`, sealed at approval)
**SIDE B:** C4 (`TestHarness.run`)
**WHAT CROSSES:** A SHA-256 hex digest over a canonicalized subset of scenario fields. [OBSERVED]
**CONTRACT:** Side B assumes an approved scenario's substantive content is byte-identical to what the approver saw. [DOCUMENTED — `scenarios.py:27-36`]
**ENFORCEMENT:** `hashable_content()` covers `scenario_id`, `regulation_id`, `zone`, `question`, `situation`, `sorted(options)`, `expected` — and deliberately excludes `status`, `approved_by`, timestamps, and the hash itself. `verify_hash()` raises `ScenarioIntegrityError` if the recomputed digest differs or if no hash was ever recorded. The harness calls it per scenario before invoking the resolver, and converts the exception into a `RESULT_ERROR` row rather than aborting the run. Canonicalization is `json.dumps(sort_keys=True, separators=(",",":"), default=str)`. [OBSERVED — `scenarios.py:112-142`, `harness.py:206-218`]
**LOCATION:** `sage_k/scenarios.py:72-142`; `sage_k/harness.py:206-218`
**ORIGIN:** DOCUMENTED — `scenarios.py:27-36` states that approval covers an exact fact set and an exact expected answer, so editing an approved scenario is a new scenario requiring new approval.
**DEPENDS ON:** S3
**FAILURE MODE:** An approved scenario could be edited post-approval and still score, meaning the recorded legal sign-off would cover content nobody approved. C4's result rows and everything downstream (C5, C6, C7) would carry that silently.
**CONFIDENCE:** high — verified by reading; the exclusion set is explicit and commented.

---

**SEAM ID:** S5
**NAME:** Model commentary versus authoritative answer
**TYPE:** TRUST — a model-supplied value is accepted only into a non-authoritative field. Secondary: IDENTITY
**SIDE A:** C3 / C24 (model output)
**SIDE B:** C2 (`Scenario.expected`)
**WHAT CROSSES:** `model_suggested_answer` and `model_reasoning`, written via `setdefault` into `scenario.situation` under keys `_model_suggested_answer` and `_model_reasoning`. `expected` is left at its default of `None`. [OBSERVED]
**CONTRACT:** Side B assumes nothing arriving from C3 is authoritative. [DOCUMENTED — `generator.py:4-10`, `generator.py:174-177`]
**ENFORCEMENT:** `ScenarioGenerator.generate` never assigns to `expected`; the `Scenario` constructor call at `generator.py:166-173` omits it. `generated_by` is stamped with the generator label. [OBSERVED]
**LOCATION:** `sage_k/generator.py:166-179`
**ORIGIN:** DOCUMENTED — `generator.py:4-15`, stated as "the one thing this module must not do."
**DEPENDS ON:** S3
**FAILURE MODE:** If breached, `expected` would carry a model's opinion and S3's human-authority guarantee would be void without any signal.
**ADDITIONAL OBSERVED FACT:** because the commentary is stored inside `situation`, it is (a) covered by the S4 content hash and (b) passed to the resolver as part of the scenario object at `harness.py:221`. No code strips underscore-prefixed keys before the resolver call. [OBSERVED]
**CONFIDENCE:** high for the assignment behavior; the downstream visibility of `_model_suggested_answer` to the resolver is directly readable at `harness.py:221`.

---

**SEAM ID:** S6
**NAME:** Declared ambiguity zone vocabulary
**TYPE:** DATA — a closed vocabulary governs what may cross. Secondary: TRUST
**SIDE A:** C3 / C24 (model-proposed `zone` strings)
**SIDE B:** C2 (`ScenarioLibrary`), C5 (zone grouping)
**WHAT CROSSES:** A `zone` string that must be a member of `InterpretationContext.ambiguity_zones`. [OBSERVED]
**CONTRACT:** Side B assumes every scenario's zone is one the business declared. [DOCUMENTED — `generator.py:131-137`]
**ENFORCEMENT:** `if zone not in declared: self.rejected.append(...); continue` — dropped with a reason, not coerced to a nearest match. Rejections are exposed on `ScenarioGenerator.rejected` rather than swallowed. Also enforced: at least 2 distinct options, non-empty question. [OBSERVED — `generator.py:150-165`]
**LOCATION:** `sage_k/generator.py:139-165`
**ORIGIN:** DOCUMENTED — `generator.py:133-137` states a model inventing its own zone signals an incomplete declared zone list, which is a human conversation rather than a rounding error.
**DEPENDS ON:** none
**FAILURE MODE:** Zone-level drift localization (C5's entire output shape) becomes meaningless if zones are open-vocabulary; drift reports would fragment across near-duplicate zone names.
**CONFIDENCE:** high

---

**SEAM ID:** S7
**NAME:** Model client injection
**TYPE:** DATA — a string-in/string-out contract, then a JSON schema contract. Secondary: TRUST, CONTROL
**SIDE A:** C3
**SIDE B:** C24 (external model), or `StubModelClient`
**WHAT CROSSES:** A prompt string out (built by `InterpretationContext.prompt`), a raw completion string back, expected to be JSON with a top-level `scenarios` list. [OBSERVED]
**CONTRACT:** Side A assumes only that the client exposes `complete(prompt: str) -> str`. It does not assume valid JSON. [OBSERVED]
**ENFORCEMENT:** `ModelClient` is a `typing.Protocol` — structural, unenforced at runtime, no `runtime_checkable`, no isinstance check. The client is a constructor argument; nothing in C3 constructs a network client. `_parse` strips a leading markdown fence, then raises `ValueError` on `JSONDecodeError` or on a missing/non-list `scenarios` key. Batch size bounded 1..100 by `MAX_SCENARIOS_PER_BATCH`. [OBSERVED — `generator.py:44-48, 139-141, 183-197`]
**LOCATION:** `sage_k/generator.py:44-48`, `113-123`, `183-197`
**ORIGIN:** DOCUMENTED — `generator.py:25-30` states the injection posture matches "sealed_channel and twin_client elsewhere in this codebase" and that nothing here reaches the network on its own. Neither named component exists in this repo. [OBSERVED]
**DEPENDS ON:** none
**FAILURE MODE:** A malformed model response raises `ValueError` out of `generate()` and no scenarios are created. A well-formed but wrong response produces `PROPOSED` scenarios, which S3 then blocks from running.
**CONFIDENCE:** high for the mechanics; the referenced sibling components are absent from this repo, so the stated posture cannot be corroborated here.

---

**SEAM ID:** S8
**NAME:** Resolver injection (the boundary to the system under test)
**TYPE:** DATA — a callable contract. Secondary: TRUST, CONTROL
**SIDE A:** C4
**SIDE B:** C25 (external "Sentinel")
**WHAT CROSSES:** A `Scenario` object out; an option string or `None` back; or an exception. [OBSERVED]
**CONTRACT:** Side A assumes only `__call__(scenario) -> Optional[str]`. It explicitly does not assume the answer is one of `options`, does not assume the call succeeds, and treats `None` as a legitimate answer rather than a failure. [DOCUMENTED — `harness.py:35-42, 64-72`]
**ENFORCEMENT:** `Resolver` is a `typing.Protocol`, structural and unenforced. The call is wrapped in `try/except Exception`, and any exception becomes a `RESULT_ERROR` row carrying the exception type and message. The whole `Scenario` object is passed, including `situation` in full. [OBSERVED — `harness.py:220-234`]
**LOCATION:** `sage_k/harness.py:64-72`, `182-234`
**ORIGIN:** DOCUMENTED — `harness.py:35-42` states injection is what lets the same harness probe a proposed interpretation in shadow before deployment.
**DEPENDS ON:** S4 (hash verified before the resolver is called)
**FAILURE MODE:** A resolver that raises on every scenario produces an all-ERROR run; C5 then reports `alignment=None` and `STATE_UNKNOWN` rather than a passing score (see S10, S12).
**CONFIDENCE:** high

---

**SEAM ID:** S9
**NAME:** Four-outcome scoring (`TestHarness._score`)
**TYPE:** DATA — an untyped resolver answer is classified into a closed result vocabulary. Secondary: none
**SIDE A:** C25 raw answer
**SIDE B:** C4 `ScenarioResult.result`, consumed by C5, C7
**WHAT CROSSES:** One of exactly four string constants: `MATCH`, `MISMATCH`, `INDETERMINATE`, `ERROR`. [OBSERVED]
**CONTRACT:** Side B assumes refusals are distinguishable from wrong answers and from unrunnable scenarios. [DOCUMENTED — `harness.py:16-33`]
**ENFORCEMENT:** Single static method, one choke point, ordered checks: `None` → INDETERMINATE; not in `options` → ERROR; `== expected` → MATCH; else MISMATCH. [OBSERVED — `harness.py:245-263`]
**LOCATION:** `sage_k/harness.py:54-57`, `245-263`
**ORIGIN:** DOCUMENTED — `harness.py:29-33` states that collapsing INDETERMINATE into pass or fail produces a metric that lies, giving the worked example of a system that answers "I don't know" to everything.
**DEPENDS ON:** S8
**FAILURE MODE:** Collapsing the four states into two would let a refusal-heavy resolver score as either perfect or total failure, neither describing reality. C5's state machine and C7's report columns both depend on the distinction.
**CONFIDENCE:** high

---

**SEAM ID:** S10
**NAME:** Alignment denominator (`decided` versus `total`)
**TYPE:** DATA — constrains which results may enter the headline metric. Secondary: OTHER (accounting boundary)
**SIDE A:** C4 `results` list
**SIDE B:** C4 `alignment` property, consumed by C5, C6, C7
**WHAT CROSSES:** `matched / (matched + mismatched)`, or `None`. [OBSERVED]
**CONTRACT:** Downstream assumes `alignment is None` means "no evidence," never "perfect." [DOCUMENTED — `harness.py:135-145`]
**ENFORCEMENT:** `decided = matched + mismatched`; `alignment` returns `None` when `decided == 0` rather than `1.0`. Separately, non-runnable scenarios go to a `skipped` list with a per-scenario reason string rather than being dropped, so the candidate set is `all scenarios for the regulation`, not `runnable only`. [OBSERVED — `harness.py:126-145`, `192-204`]
**LOCATION:** `sage_k/harness.py:104-170`, `192-204`
**ORIGIN:** DOCUMENTED — `harness.py:139-142` calls returning 1.0 for an empty run "the single most dangerous number this module could produce"; `scenarios.py:38-43` states a shrinking denominator is the easiest way to make drift disappear.
**DEPENDS ON:** S9
**FAILURE MODE:** A zero-evidence run would report perfect agreement. C5's `STATE_UNKNOWN` path and C7's "this is not a pass" language both consume the `None`.
**CONFIDENCE:** high

---

**SEAM ID:** S11
**NAME:** TestRun to DriftAnalyzer handoff
**TYPE:** DATA
**SIDE A:** C4
**SIDE B:** C5
**WHAT CROSSES:** A `TestRun` object. C5 reads `by_zone()`, `alignment`, `regulation_id`, `interpretation_version`, `run_id`, and each result's `.result` and `.scenario_id`. [OBSERVED]
**CONTRACT:** Side B assumes `result` strings match the harness vocabulary. [OBSERVED]
**ENFORCEMENT:** Python attribute access only; no schema validation. C5 re-derives counts by comparing against **string literals** `"MATCH"`, `"MISMATCH"`, `"INDETERMINATE"`, `"ERROR"` rather than importing the `RESULT_*` constants that C4 defines and C1 re-exports. The vocabulary is therefore duplicated across the seam. [OBSERVED — `drift.py:187-190, 214`]
**LOCATION:** `sage_k/drift.py:49`, `175-227`
**ORIGIN:** NO EVIDENCE
**DEPENDS ON:** S9, S10
**FAILURE MODE:** If a constant in C4 changed value, C5's comparisons would silently stop matching and every zone would report `decided=0` → `alignment=None` → `STATE_UNKNOWN` → `RISK_MEDIUM`. Nothing would raise. C6 and C7 consume the result.
**CONFIDENCE:** high — the literal duplication is directly readable.

---

**SEAM ID:** S12
**NAME:** Zone tolerance configuration
**TYPE:** OTHER — a policy/parameter boundary separating a business-set threshold from the mechanical evaluation that applies it. Secondary: IDENTITY
**SIDE A:** C5 `ToleranceConfig` / `ZoneTolerance` (caller-supplied)
**SIDE B:** C5 `DriftAnalyzer._state`
**WHAT CROSSES:** A mode string plus two floats, and optionally `set_by`, `set_at`, `rationale`. [OBSERVED]
**CONTRACT:** `_state` assumes an unconfigured zone should be loud, not quiet. [DOCUMENTED — `drift.py:92-98`]
**ENFORCEMENT:** `for_zone()` falls back to `self.default`, which defaults to `mode=STRICT`. Under `STRICT`, both float thresholds are ignored and any single mismatch yields `BREACH`. `ZoneTolerance.__post_init__` validates `0 <= breach_below <= watch_below <= 1` for non-STRICT modes only. `flagged` is true for `WATCH`, `BREACH`, and `UNKNOWN`. [OBSERVED — `drift.py:82-87`, `105-106`, `212`, `229-246`]
**LOCATION:** `sage_k/drift.py:64-115`, `229-254`
**ORIGIN:** DOCUMENTED — `drift.py:11-23` states there is no defensible universal answer to acceptable drift, so the default is conservative, and the intended path is calibration from evidence rather than permanent strictness.
**DEPENDS ON:** S11
**FAILURE MODE:** A newly discovered zone inheriting a permissive default would pass without anyone having considered it. `set_by`/`set_at`/`rationale` carry the human attribution for a changed threshold; nothing enforces that they are populated.
**CONFIDENCE:** high

---

**SEAM ID:** S13
**NAME:** Calibration advisory boundary
**TYPE:** CONTROL — a suggestion crosses; authority to change the passing grade does not. Secondary: DATA
**SIDE A:** C5 `calibration_suggestion`
**SIDE B:** C5 `ToleranceConfig` (unmodified), C7 (rendering)
**WHAT CROSSES:** A dict of per-zone observed min/mean and suggested watch/breach floats, plus a `__status__` readiness block. [OBSERVED]
**CONTRACT:** Side B assumes nothing is set as a side effect. [DOCUMENTED — `drift.py:261-269`]
**ENFORCEMENT:** Pure function over a `Sequence[DriftReport]`; returns a dict; no reference to any `ToleranceConfig` instance in its body. Returns `{"__status__": {"ready": False, ...}}` when fewer than `min_periods` (default 3) reports are supplied. [OBSERVED — `drift.py:257-303`]
**LOCATION:** `sage_k/drift.py:257-303`; rendered at `report.py:204-231`
**ORIGIN:** DOCUMENTED — `drift.py:265-269` states an automatically tightening threshold would let the system quietly redefine its own passing grade, "exactly the failure this whole subsystem exists to catch."
**DEPENDS ON:** S12
**FAILURE MODE:** Auto-applied thresholds would make the metric self-referential: the system would grade itself against its own recent behavior.
**CONFIDENCE:** high

---

**SEAM ID:** S14
**NAME:** DriftReport embedding into the realignment record
**TYPE:** DATA. Secondary: PERSISTENCE
**SIDE A:** C5
**SIDE B:** C6
**WHAT CROSSES:** An `Optional[DriftReport]` held by reference on `RealignmentRecord.drift`; serialized via `to_dict()` into `structured_data()` and into `hashable_content()`. [OBSERVED]
**CONTRACT:** Side B assumes `DriftReport` exposes `risk_level`, `zones`, `overall_alignment`, `flagged_zones`, `to_dict()`. [OBSERVED]
**ENFORCEMENT:** Type annotation only; `Optional`, and every read site is `if self.drift:`-guarded. [OBSERVED — `realignment.py:174-189`, `198-211`, `223-239`, `305-306`, `321-323`]
**LOCATION:** `sage_k/realignment.py:59`, `145`, `174-239`
**ORIGIN:** NO EVIDENCE
**DEPENDS ON:** S11, S12
**FAILURE MODE:** A record with `drift=None` is constructible and sealable; `quick_view()` then reports `risk_level="UNKNOWN"` with an empty drift summary, and the seal covers `"drift": None`. The record is valid and signed with no evidence attached.
**CONFIDENCE:** high

---

**SEAM ID:** S15
**NAME:** Record seal (`RealignmentRecord.seal` / `verify`)
**TYPE:** TRUST. Secondary: PERSISTENCE, IDENTITY
**SIDE A:** C6 substantive fields
**SIDE B:** C6 narrative fields, C7, C27
**WHAT CROSSES:** A SHA-256 digest over a deliberately partial field set. [OBSERVED]
**CONTRACT:** A typo fix in prose must not void a legal sign-off; a changed decision must. [DOCUMENTED — `realignment.py:34-40`, `223-225`]
**ENFORCEMENT:** `hashable_content()` includes `record_id`, `regulation_id`, `interpretation_version`, both dates, `legal_sign_off`, `decision`, `sorted(checks_deployed)`, `checks_config`, `drift.to_dict()`, `version_change.to_dict()`, `approved_by`. It **excludes** `context`, `business_rationale`, `legal_assessment`, `decision_rationale`, `regulatory_events`, `outcome_correlation`, `open_questions`, `trigger`. `verify()` returns `False` rather than raising, including when `record_hash is None`. Canonicalization matches S4's (`sort_keys`, tight separators, `default=str`). [OBSERVED — `realignment.py:223-253`]
**LOCATION:** `sage_k/realignment.py:77-78`, `223-253`
**ORIGIN:** DOCUMENTED — `realignment.py:34-40`
**DEPENDS ON:** S14
**FAILURE MODE:** Excluded fields can be edited post-seal without detection; `regulatory_events` and `outcome_correlation` are structured evidence that the seal does not cover. C7 prints `Record sealed: NO - hash does not verify` and `RealignmentTrail.unsealed()` lists the record; both consume a boolean that is also `False` for a never-sealed record, so "tampered" and "never sealed" are indistinguishable at those call sites. [OBSERVED]
**CONFIDENCE:** high — the inclusion/exclusion set is explicit and the non-raising return is directly readable.

---

**SEAM ID:** S16
**NAME:** Record construction invariants (`__post_init__`)
**TYPE:** TRUST — validation before a record can exist. Secondary: CONTROL, IDENTITY
**SIDE A:** any caller constructing a `RealignmentRecord`
**SIDE B:** C6, C7, C27
**WHAT CROSSES:** Constructor arguments. [OBSERVED]
**CONTRACT:** Downstream assumes every record has a valid decision, an approver, and a `version_change` whenever the decision is `UPDATE`. [OBSERVED]
**ENFORCEMENT:** Three `ValueError` raises in `__post_init__`: decision not in `VALID_DECISIONS`; `decision == UPDATE` with `version_change is None`; empty `approved_by` (message: "a realignment record with no approver is not a governance record"). [OBSERVED — `realignment.py:161-170`]
**LOCATION:** `sage_k/realignment.py:66`, `161-170`
**ORIGIN:** DOCUMENTED in the error message text itself; no separate rationale block.
**DEPENDS ON:** none
**FAILURE MODE:** An unapprovable or unattributed record would enter the trail and the seal (S15) would cover an empty approver list.
**CONFIDENCE:** high

---

**SEAM ID:** S17
**NAME:** Interpretation version boundary (`VersionChange`)
**TYPE:** TIME — a lifecycle/phase boundary between interpretation versions. Secondary: DATA
**SIDE A:** decisions made under `from_version`
**SIDE B:** decisions made under `to_version`
**WHAT CROSSES:** `from_version`, `to_version`, `activation_date`, `reason`, `changes`, `decisions_affected`, `affected_date_range`, `retroactive_retest` (default `"NOT_REQUESTED"`), `retroactive_scope`, `known_deltas`. [OBSERVED]
**CONTRACT:** Decisions made under v1 remain governed by v1, and whether anyone re-tested them is recorded rather than assumed. [DOCUMENTED — `realignment.py:42-48`, `report.py:146-156`]
**ENFORCEMENT:** NO EVIDENCE — this is a recorded assertion in a dataclass and a rendered paragraph. No code in the repo routes, filters, or gates any behavior on `interpretation_version`. `TestRun.interpretation_version` and `DriftReport.interpretation_version` are carried and printed, never compared. [OBSERVED]
**LOCATION:** `sage_k/realignment.py:109-126`, `164-168`; `sage_k/report.py:136-160`
**ORIGIN:** DOCUMENTED — `realignment.py:46-48` attributes the rule to a named person ("Wm's rule"): you go back as far as the business wants to, and that choice is recorded rather than assumed either way.
**DEPENDS ON:** S16
**FAILURE MODE:** Version scoping is documentary only. If a consumer treats the recorded scope as enforced, decisions could be evaluated against the wrong interpretation with no mechanism reporting it.
**CONFIDENCE:** high for the absence of enforcement — grep confirms `interpretation_version` is never used in a conditional anywhere in the repo.

---

**SEAM ID:** S18
**NAME:** Record-to-rendering boundary
**TYPE:** DATA — one direction only. Secondary: none
**SIDE A:** C6, C5
**SIDE B:** C7
**WHAT CROSSES:** Read-only attribute and method access; a markdown string returns. [OBSERVED]
**CONTRACT:** Rendering must not be able to change the artifact of record. [DOCUMENTED — `report.py:4-7`]
**ENFORCEMENT:** Both public functions take records and return `str`. Every call into C5/C6 from C7 is a reader: `quick_view()`, `narrative()` (unused by the renderer, which reads the fields directly), `verify()`, `trail.history()`, `trail.zone_trend()`, `trail.unsealed()`, `calibration_suggestion()`. No assignment to any record attribute appears in C7. [OBSERVED]
**LOCATION:** `sage_k/report.py:61-302`
**ORIGIN:** DOCUMENTED — `report.py:4-7` states the report is generated from the record so the meeting document and the archive document can never disagree.
**DEPENDS ON:** S14, S15
**FAILURE MODE:** If rendering mutated records, the archived artifact and the document read in the room could diverge, which is the specific outcome the seam exists to prevent.
**CONFIDENCE:** high — verified by reading every call site in C7.

---

**SEAM ID:** S19
**NAME:** Longitudinal trail assembly (`RealignmentTrail`)
**TYPE:** TIME — a multi-record temporal view built over single-period records. Secondary: DATA
**SIDE A:** C6 individual `RealignmentRecord` instances
**SIDE B:** C6 `RealignmentTrail`, C7 `_multi_year_block`
**WHAT CROSSES:** Per-record rows sorted by `realignment_date` (string sort), zone trend points, version changes, regulatory events, and unsealed record IDs. [OBSERVED]
**CONTRACT:** Side B assumes the day-one record shape already carries the slots a longitudinal view needs, so no record is reformatted or rewritten. [DOCUMENTED — `realignment.py:23-32`, `277-284`]
**ENFORCEMENT:** `RealignmentTrail` holds a plain list and only reads. Slots `regulatory_events`, `version_change`, `open_questions` exist with empty defaults on every record. Sorting is lexicographic on the ISO date string. [OBSERVED — `realignment.py:286-370`]
**LOCATION:** `sage_k/realignment.py:277-370`; `sage_k/report.py:254-302`
**ORIGIN:** DOCUMENTED — `realignment.py:23-32` describes this as the migration path, chosen so there is no reformatting step later.
**DEPENDS ON:** S15, S16
**FAILURE MODE:** The multi-year slope detection at `report.py:276-293` compares only first and last trend points; if the trail's ordering assumption failed, "slipping" zones would be computed against the wrong endpoints. `unsealed()` is the integrity gate on the whole trend block.
**CONFIDENCE:** high

---

**SEAM ID:** S20
**NAME:** Scenario library persistence
**TYPE:** PERSISTENCE — what survives restart. Secondary: DATA, TRUST
**SIDE A:** C2 in-memory `ScenarioLibrary`
**SIDE B:** C21 JSON file at a caller-supplied path
**WHAT CROSSES:** `{"scenarios": [ ...asdict(Scenario)... ]}` written with `indent=2, sort_keys=True`. [OBSERVED]
**CONTRACT:** A reloaded library must carry the same hash bindings, so S4 still holds across a restart. [INFERRED — the round-trip of `content_hash` is observable, but no doc states this intent]
**ENFORCEMENT:** `Scenario.from_dict` filters to `cls.__dataclass_fields__`, so unknown keys in the file are dropped silently and no error is raised. `content_hash` is a declared field and round-trips. `ScenarioLibrary.add` raises `ValueError` on duplicate `scenario_id`. No file locking, no atomic write, no schema version field. [OBSERVED — `scenarios.py:197-200`, `217-221`, `251-266`]
**LOCATION:** `sage_k/scenarios.py:249-266`
**ORIGIN:** DOCUMENTED — `scenarios.py:203-210` states the storage is deliberately dull and swappable, and that the governance value sits in the approval gate and hash binding rather than in where rows sit.
**DEPENDS ON:** S4
**FAILURE MODE:** A truncated or concurrently written file loses scenarios; because the harness enumerates from the library, missing scenarios vanish from both the results and the skipped list, shrinking the denominator that S10 exists to protect. A hand-edited file is caught by S4 at run time, not at load time.
**CONFIDENCE:** high for the mechanics; medium on the CONTRACT field, which is inferred.

---

**SEAM ID:** S21
**NAME:** `GsaContextEnvelope` immutability
**TYPE:** STATE — mutable state is isolated by making the carrier frozen. Secondary: DATA
**SIDE A:** C9 adapter, C8 kernel, C10 extractor
**SIDE B:** all callers holding an envelope reference
**WHAT CROSSES:** `payload_data`, `session_state_mapping`, `header_mapping`, `status_string`. [OBSERVED]
**CONTRACT:** A module receiving an envelope cannot mutate the caller's copy; every change produces a new object. [OBSERVED]
**ENFORCEMENT:** `@dataclass(frozen=True)`. All modification sites use `dataclasses.replace`. Outbound headers pass through `_local_deep_freeze`, converting dicts to `MappingProxyType` and lists to tuples recursively. **Partial:** `payload_data` and `session_state_mapping` are typed `Dict[str, Any]` and are not frozen — only `header_mapping` is deep-frozen, and only on the outbound path. `field(default_factory=dict)` on `header_mapping` means a default-constructed envelope has a plain mutable dict there. [OBSERVED — `gsa_adapter.py:60-71`, `80-86`, `224-227`]
**LOCATION:** `sage_k/gsa_adapter.py:60-86`, `189`, `224-227`; `sage_k/kernel.py:439-443`; `sage_k/graph_extractor.py:163-167`
**ORIGIN:** DOCUMENTED — `gsa_adapter.py:60-66` notes `_local_deep_freeze` is a local replacement for an external `universal_foundation.deep_freeze_structure_function` that does not exist in this repo; C20 confirms the original artifacts imported that missing module.
**DEPENDS ON:** none
**FAILURE MODE:** If a wrapped module mutated `payload_data` in place, the hash computed at Phase 3 (S22) would cover the mutated content while an upstream holder of the same dict would observe the change out of band.
**CONFIDENCE:** high

---

**SEAM ID:** S22
**NAME:** GSA hash-chain continuity (`gsa_interlock_hash` / `gsa_chain_history`)
**TYPE:** TRUST — inbound state is validated before the wrapped module runs. Secondary: DATA, TIME
**SIDE A:** upstream adapter step (or a hand-seeded caller)
**SIDE B:** C9 Phase 2 execution
**WHAT CROSSES:** A SHA-256 hex digest over `parent`, `iter`, sorted merge anchors, and JSON-serialized payload and session state. [OBSERVED]
**CONTRACT:** Side B assumes an envelope arriving with a chain history longer than one entry was produced by the immediately preceding adapter step and has not been altered since. [OBSERVED]
**ENFORCEMENT:** `compute_state_signature`; on mismatch the adapter returns early with `status_string = "GSA_CHAIN_BREAK: ..."` — it does **not** raise, so a caller that ignores `status_string` proceeds with an unverified envelope. Verification runs only when `len(hash_history) > 1`; a one-entry history is treated as a seed anchor. [OBSERVED — `gsa_adapter.py:89-112`, `167-186`]
**LOCATION:** `sage_k/gsa_adapter.py:89-112`, `144-186`, `202-227`
**ORIGIN:** DOCUMENTED — C20 shows the user supplied `gsa_universal_interlock_wrapper.py` as a template and instructed the model to "wrap the final code in the below wrapper." The `len(hash_history) > 1` condition is documented at `gsa_adapter.py:21-33` as a fix for a defect in the source artifact, which checked `if hash_history:` and compared a seed entry against a hardcoded `"GENESIS_ANCHOR"` prior anchor that never matched how the seed was actually signed.
**DEPENDS ON:** S21
**FAILURE MODE:** A tampered or reordered envelope would execute the wrapped module. Because the failure surfaces as a status string rather than an exception, detection depends entirely on the caller checking it. C11's tests assert on `status_string`; C13 and C14 print it.
**CONFIDENCE:** high

---

**SEAM ID:** S23
**NAME:** Wrapped-module dispatch (sync/async duck-typing)
**TYPE:** CONTROL — authority to execute crosses into an arbitrary wrapped module. Secondary: DATA
**SIDE A:** C9 `GsaUniversalAdapter`
**SIDE B:** C8 `Fortress`, C10 `ExtractorGsaAdapterModule`, or any object with a matching attribute
**WHAT CROSSES:** A `GsaContextEnvelope` in, a `GsaContextEnvelope` out, via one of three paths. [OBSERVED]
**CONTRACT:** Side A assumes the module exposes `execute_governance_logic` or `execute_governance_module`, or is callable through a `translation_bridge`; and that the return value is an envelope-shaped object with `header_mapping` and `payload_data`. [OBSERVED]
**ENFORCEMENT:** `hasattr` checks in order, then `await result if inspect.isawaitable(result) else result`. The third path uses `asyncio.get_event_loop().run_in_executor(None, self.bridge, self.module, working_envelope)`. Notably, `ComposableLegoModule` is declared as a `Protocol` requiring `async def process_payload`, but: it is not `runtime_checkable`, no `isinstance` check exists, it is not used as a type annotation anywhere, and neither wrapped module in this repo implements `process_payload` at all — the adapter looks for two differently-named methods. The Protocol is therefore documentary. [OBSERVED — `gsa_adapter.py:74-77`, `191-200`; confirmed by grep]
**LOCATION:** `sage_k/gsa_adapter.py:74-77`, `115-130`, `191-200`
**ORIGIN:** DOCUMENTED — `gsa_adapter.py:6-19` states the two source artifacts diverged here (one always awaited, one never did), that each is correct only for its own module type, and that the `inspect.isawaitable` branch was introduced so both work.
**DEPENDS ON:** S22
**FAILURE MODE:** An object with neither method silently takes the executor path, where the default bridge is `lambda m, env: env` — the module never runs, the envelope passes through unchanged, and the adapter still stamps a valid outbound hash over it. That outcome is indistinguishable at the seam from a module that ran and changed nothing.
**CONFIDENCE:** high

---

**SEAM ID:** S24
**NAME:** Static anchor and re-entry (`gsa_set_static_anchor_id` / `gsa_reentry_target_id`)
**TYPE:** TIME — a checkpoint/save-state boundary. Secondary: TRUST, STATE
**SIDE A:** an earlier adapter step that set an anchor
**SIDE B:** a later step re-entering at that anchor
**WHAT CROSSES:** An anchor ID string and the hash recorded under it in `gsa_static_anchors`. [OBSERVED]
**CONTRACT:** A re-entering envelope's `gsa_interlock_hash` must equal the hash saved at the named anchor. [OBSERVED]
**ENFORCEMENT:** Equality check; on mismatch returns early with `status_string = "GSA_ANCHOR_MISMATCH: ..."`. `gsa_reentry_target_id` is popped on success (single-use). [OBSERVED — `gsa_adapter.py:145-156`, `204`, `215-216`]
**LOCATION:** `sage_k/gsa_adapter.py:135`, `138`, `145-156`, `204`, `215-220`
**ORIGIN:** DOCUMENTED as inherited — C20 shows this logic present verbatim in the user-supplied wrapper template. No statement of what requirement produced it.
**DEPENDS ON:** S22
**FAILURE MODE:** A pipeline could resume from a checkpoint whose state does not match what was saved. **No code in this repo ever writes `gsa_set_static_anchor_id` or `gsa_reentry_target_id`** — grep finds only the reads and the pop. The path is reachable only from a caller outside the repo that builds headers by hand, and is exercised by no test or example. [OBSERVED]
**CONFIDENCE:** high for the mechanics and for the absence of any in-repo producer.

---

**SEAM ID:** S25
**NAME:** Fork/join convergence (`gsa_graph_forks` / `gsa_branch_hash_*`)
**TYPE:** CONTROL — merge authority: only the named actor may consume a branch. Secondary: DATA
**SIDE A:** parallel branch producers
**SIDE B:** the adapter whose `actor_name` matches a fork's recorded target
**WHAT CROSSES:** Branch hashes, joined with `"||"` into a composite upstream hash and also passed as `extra_anchors` to the signature function. [OBSERVED]
**CONTRACT:** An adapter merges exactly those forks whose recorded value equals `type(underlying_module).__name__`. [OBSERVED]
**ENFORCEMENT:** `target_merge_keys = [k for k, v in fork_tracking.items() if v == self.actor_name]`; consumed keys are popped from both the fork map and the headers. Identity is a class-name string, not a token or instance identity, so two adapters wrapping different instances of the same class are indistinguishable at this seam. [OBSERVED — `gsa_adapter.py:129`, `159-165`, `207-212`]
**LOCATION:** `sage_k/gsa_adapter.py:129`, `134`, `158-165`, `188`, `207-212`
**ORIGIN:** DOCUMENTED as inherited from the user-supplied wrapper template in C20. No requirement stated.
**DEPENDS ON:** S22
**FAILURE MODE:** A branch could be merged by the wrong actor or dropped. **Nothing in this repo ever populates `gsa_graph_forks` with a non-empty value or writes any `gsa_branch_hash_*` key** — the adapter reads the map, filters it, and writes it back. The merge branch is therefore unreachable from any in-repo caller. [OBSERVED]
**CONFIDENCE:** high

---

**SEAM ID:** S26
**NAME:** Temporal doorway gate (`GsaTemporalDoorwayGate`)
**TYPE:** TIME — a rendezvous window boundary. Secondary: TRUST
**SIDE A:** an envelope carrying `gsa_target_exit_hash`
**SIDE B:** the gate's rotating hash value
**WHAT CROSSES:** A target hash string; on success, `gsa_doorway_cleared_hash` and `gsa_doorway_timestamp_ns` are written into headers. [OBSERVED]
**CONTRACT:** An envelope passes only if its target hash matches the value currently held by the rotating worker, within `gsa_doorway_timeout_seconds` (default 3.0). [OBSERVED]
**ENFORCEMENT:** `asyncio.Lock`-guarded polling loop at 5 ms intervals against a hash rotated every `rotation_interval_seconds` (default 0.05) from `f"{seed}||{time.time_ns()}"`. Three distinct outcomes, all returned as `status_string` values, none raised: `GSA_DOORWAY_REJECT` (no target supplied), `GSA_EXIT_HANDSHAKE_COMPLETED`, `GSA_DOORWAY_TIMEOUT`. The gate's own docstring states it is a self-contained polling rendezvous rather than an external security boundary. [OBSERVED — `gsa_adapter.py:230-296`]
**LOCATION:** `sage_k/gsa_adapter.py:230-296`
**ORIGIN:** DOCUMENTED as inherited from the wrapper template in C20.
**DEPENDS ON:** S21
**FAILURE MODE:** An envelope passes outside its window, or blocks for the timeout duration. **The class is never instantiated anywhere in the repo** — it appears only in its own definition, in `__all__`, and in a docstring reference. `start_gate_engine` is never called, so absent external use `_current_doorway_hash` stays `""` and every call times out. [OBSERVED]
**CONFIDENCE:** high

---

**SEAM ID:** S27
**NAME:** `MandateLayer` action clamp
**TYPE:** CONTROL — bounds the magnitude of action an agent is permitted to apply. Secondary: STATE
**SIDE A:** C8 agent output (`ConservativeAgent` / `AggressiveAgent` / `ReactiveAgent`)
**SIDE B:** C8 state update in `run_cycle`
**WHAT CROSSES:** A `{"delta": float}` dict. [OBSERVED]
**CONTRACT:** Side B assumes no delta reaches the state update unclamped. [OBSERVED]
**ENFORCEMENT:** Two-stage clamp: a velocity limit `(|distance| * 0.35) / (1 + volatility * 0.15)`, itself bounded to `[1.2, 28.0]`; then an absolute projected-KPI bound of `target + 15.0` above and `target - 75.0` below. The dict is **mutated in place** and also returned; the caller uses the return value. [OBSERVED — `kernel.py:182-200`, `392`]
**LOCATION:** `sage_k/kernel.py:182-200`; called at `kernel.py:392`
**ORIGIN:** NO EVIDENCE — the thresholds are unexplained magic numbers; the module docstring describes the layer's function but not what requirement produced these bounds.
**DEPENDS ON:** none
**FAILURE MODE:** An unclamped `AggressiveAgent` delta (gain 0.35) could drive the KPI past `InvariantMonitor`'s `|state| > 250` bound, tripping `STATE_DIVERGENCE`. The clamp is the only thing between agent output and the state variable.
**CONFIDENCE:** high

---

**SEAM ID:** S28
**NAME:** Learning freeze (`InvariantMonitor` → `freeze_timer`)
**TYPE:** STATE — isolates learned weights from further mutation. Secondary: CONTROL, TIME
**SIDE A:** C8 invariant violations
**SIDE B:** C8 `Policy.weight_policy_matrix`, `WorldModel` weights, agent selection
**WHAT CROSSES:** A violation list; a learning-rate modifier; a countdown integer. [OBSERVED]
**CONTRACT:** Downstream learning updates assume they are suppressed while the state is misbehaving. [OBSERVED]
**ENFORCEMENT:** Graded, three levels: any violation multiplies the learning modifier by 0.1 and zeroes exploration; two or more violations set `freeze_timer = 8`; while `freeze_timer > 0` the selection path is bypassed (forced agent index 0, probabilities `[1.0, 0.0, 0.0]`) and `Policy.update` is skipped entirely. Separately, `DriftMonitor` firing multiplies the modifier by 0.25 and decays every policy weight by 0.995. Both `Policy.update` and `WorldModel.update` early-return when their learning rate is `<= 0`. [OBSERVED — `kernel.py:147-161`, `340-364`, `410-423`]
**LOCATION:** `sage_k/kernel.py:147-161`, `164-179`, `338`, `340-364`, `410-423`
**ORIGIN:** NO EVIDENCE for the specific thresholds. The module docstring states the guardrails "clamp the action and can freeze learning if the state misbehaves," and explicitly warns that names such as "Lyapunov Stability Engines" in the source artifacts are naming rather than specification.
**DEPENDS ON:** S27
**FAILURE MODE:** Weights would keep updating on divergent or NaN-adjacent states, compounding the divergence. Note the ordering: `freeze_timer` is decremented inside `_execute_agent_action`, so by the time `if self.freeze_timer == 0` is checked at the end of the same step, a timer that was 1 at selection is 0 at update — the last frozen step still performs a policy update. [OBSERVED]
**CONFIDENCE:** high — the ordering interaction is directly readable at `kernel.py:355-359` and `420-423`.

---

**SEAM ID:** S29
**NAME:** Numeric safety check (`IntegrityLayer.analyze`)
**TYPE:** TRUST — a value is validated before entering the monitoring pipeline. Secondary: none
**SIDE A:** C8 `running_predictive_error` from `WorldModel.update`
**SIDE B:** C8 volatility history, distortion score, regime classification
**WHAT CROSSES:** A float error value. [OBSERVED]
**CONTRACT:** Downstream statistics assume finite input. [OBSERVED]
**ENFORCEMENT:** `if math.isnan(...) or math.isinf(...): raise ValueError("Numeric Safety Exception: ...")`. This is the only place in C8 that raises rather than degrading. Upstream, `WorldModel.update` clamps predictive error to `[-12, 12]`, and `Policy.select` clamps the softmax matching score to `<= 5.0` before `math.exp`. [OBSERVED — `kernel.py:118-119`, `227`, `256`]
**LOCATION:** `sage_k/kernel.py:117-132`
**ORIGIN:** NO EVIDENCE
**DEPENDS ON:** none
**FAILURE MODE:** NaN propagates into `deque` history, then into `statistics.stdev`, then into every threshold comparison — where all comparisons against NaN are `False`, so `RegimeEngine` would report `STABLE` and `InvariantMonitor` would report no violations. The check is what prevents a silently-healthy-looking divergent run.
**CONFIDENCE:** high

---

**SEAM ID:** S30
**NAME:** Audit log HMAC signing
**TYPE:** PERSISTENCE — a durability boundary; what survives the process. Secondary: TRUST, IDENTITY
**SIDE A:** C8 `audit_append`
**SIDE B:** C22 `fortress_audit.log`
**WHAT CROSSES:** JSON lines of `{ts, run_id, event, data, hmac}`. Written once per simulation step from `run_cycle` with event type `"action_enforced"`. [OBSERVED]
**CONTRACT:** A later reader assumes the HMAC lets it detect tampering. [INFERRED — no reader exists in the repo and no doc states the verification procedure]
**ENFORCEMENT:** `hmac.new(key, message, hashlib.sha256).hexdigest()`. The signature is computed over `json.dumps(record, separators=(",",":"), sort_keys=True)` of the record **before** the `hmac` field is added; the record is then mutated and written with plain `json.dumps(record)` — different separators, no `sort_keys`. A verifier must therefore strip `hmac` and re-serialize with the tight canonical form, which is not documented anywhere. `IOError` is caught and passed, so a failed write is silent. The docstring states this is integrity/tamper-evidence only, not encryption. [OBSERVED — `kernel.py:74-92`]
**LOCATION:** `sage_k/kernel.py:62-92`, `394-399`; `.gitignore:7`
**ORIGIN:** NO EVIDENCE for the design; the file is gitignored, which is DOCUMENTED at `.gitignore:7`.
**DEPENDS ON:** S31 (key source)
**FAILURE MODE:** Under the default key the signature is forgeable by anyone who knows the default. A disk-full or permissions failure produces no audit record and no error. Running the test suite writes ~36 KB to this file as a side effect of `Fortress.run_cycle`. [OBSERVED — file created during test run]
**CHANGED 2026-10-01:** there is no longer a default key (see S31). The forgeability described above now applies only when the published literal is set explicitly; with no key set, records are signed with a per-process random key and cannot be verified after the process exits.
**CONFIDENCE:** high for the mechanics; the CONTRACT field is inferred because no verifier exists.

---

**SEAM ID:** S31
**NAME:** Environment configuration and production key gate
**TYPE:** OTHER — a deployment-configuration boundary between process environment and module state. Secondary: TRUST, IDENTITY
**SIDE A:** C23 environment variables
**SIDE B:** C8 module-level constants
**WHAT CROSSES:** `FORTRESS_AUDIT_LOG` (path, default `"fortress_audit.log"`), `FORTRESS_AUDIT_KEY` (no default: when unset, a random per-process key is used), `FORTRESS_ENV`, and `FORTRESS_RUN_ID` (written, not read from outside). [OBSERVED]
**CONTRACT:** A production deployment must not run on a missing key or on the published development key. [OBSERVED, enforced directly]
**CHANGED 2026-09-24:** the `"development-key"` default was removed. With `FORTRESS_AUDIT_KEY` unset the kernel signs with a random per-process key, and `FORTRESS_ENV=production` without a key raises at import.
**CHANGED 2026-10-01:** production also refuses the literal `"development-key"` when it is set explicitly (the 2026-09-24 change had dropped that check). A `RuntimeWarning` is raised at import when the key is unset, and when it is the published literal outside production. Behavior is pinned by `tests/test_audit_key.py`. Line citations into `kernel.py` elsewhere in this document were recorded against the original reconstruction; since then code after the imports has moved down by 2 lines and code after the audit-key block by 27.
**ENFORCEMENT:** `if os.getenv("FORTRESS_ENV") == "production" and (not _CONFIGURED_AUDIT_KEY or _CONFIGURED_AUDIT_KEY == _PUBLISHED_DEFAULT_KEY): raise RuntimeError(...)`. Evaluated at **module import time**, once, at `kernel.py:79-82`. Verified empirically: `FORTRESS_ENV=production python -c "import sage_k.kernel"` raises, and so does the same with `FORTRESS_AUDIT_KEY=development-key`. The gate is one-directional: it catches a missing key and the published key in production but not a weak non-default key, and not production running under any other `FORTRESS_ENV` spelling. [OBSERVED]
**LOCATION:** `sage_k/kernel.py:69-98`
**ORIGIN:** DOCUMENTED in the exception message: "Production deployments require unique cryptographic keys."
**DEPENDS ON:** none
**FAILURE MODE:** Audit records signed with a publicly known key (only if the published literal is set explicitly outside production), or, with no key set, signed with a key that exists only inside the process, so records cannot be verified after it exits and logs appended by several runs mix keys. Because the check is import-time, changing the environment after import has no effect, and because C1 does not import C8 (S1), `import sage_k` alone never triggers the gate.
**CONFIDENCE:** high — confirmed by execution.

---

**SEAM ID:** S32
**NAME:** Global seeding side effect (`set_global_seed`)
**TYPE:** STATE — process-global mutable state crossed from a constructor. Secondary: OTHER
**SIDE A:** C8 `Fortress.__init__`
**SIDE B:** the `random` module's global state, `os.environ`, and optionally `numpy.random`
**WHAT CROSSES:** An integer seed. [OBSERVED]
**CONTRACT:** Callers get reproducible runs. [DOCUMENTED — docstring at `kernel.py:45`]
**ENFORCEMENT:** None isolating the effect. `random.seed(seed)` mutates the process-wide RNG; `os.environ["FORTRESS_RUN_ID"]` is set to a SHA-256 of the seed; numpy is seeded if importable. `Fortress.__init__` calls it unconditionally, so constructing a `Fortress` reseeds the interpreter's RNG for everything else in the process. No `random.Random` instance is used. Early-returns when `seed is None`. [OBSERVED — `kernel.py:44-54`, `330`]
**LOCATION:** `sage_k/kernel.py:44-54`, `329-330`
**ORIGIN:** NO EVIDENCE
**DEPENDS ON:** none
**FAILURE MODE:** Any unrelated code in the same process that relies on `random` has its stream reset when a `Fortress` is constructed. Conversely, `Fortress.run_cycle` called twice on one instance does not re-seed, so the second run continues the stream rather than repeating — visible in C12, which constructs one instance and calls `run_cycle` 20 times.
**CONFIDENCE:** high

---

**SEAM ID:** S33
**NAME:** Optional numpy dependency
**TYPE:** OTHER — a soft-dependency boundary: presence changes behavior, absence does not fail. Secondary: none
**SIDE A:** C8
**SIDE B:** C26
**WHAT CROSSES:** An import attempt and, if it succeeds, a seed call. [OBSERVED]
**CONTRACT:** Absence is acceptable. [OBSERVED]
**ENFORCEMENT:** `try: import numpy as np / np.random.seed(seed) / except ImportError: pass`, inside the function body rather than at module level. numpy is used nowhere else in the package. [OBSERVED]
**LOCATION:** `sage_k/kernel.py:49-53`
**ORIGIN:** NO EVIDENCE
**DEPENDS ON:** S32
**FAILURE MODE:** Runs are reproducible with numpy installed and reproducible without it, but not necessarily reproducible *between* the two environments if any future code path used numpy randomness. Currently no such path exists.
**CONFIDENCE:** high

---

**SEAM ID:** S34
**NAME:** AST parse boundary
**TYPE:** DATA — arbitrary text is admitted only if it parses as Python. Secondary: TRUST
**SIDE A:** C29 `envelope.payload_data["source_code_target"]`, or a caller-supplied string
**SIDE B:** C10 `GraphExtractor` visitor
**WHAT CROSSES:** A Python source string in; a `Graph` of `Node` and `Edge` frozen dataclasses out. [OBSERVED]
**CONTRACT:** Side B assumes a parseable module. [OBSERVED]
**ENFORCEMENT:** `ast.parse(source)` — raises `SyntaxError`, which is **not caught** by `extract_graph`, by `ExtractorGsaAdapterModule.execute_governance_logic`, or by `GsaUniversalAdapter.process_payload`. The key read uses `.get("source_code_target", "")`, so a missing key yields an empty string, which parses successfully into an empty graph. Call resolution is name-based only: the module docstring states two different objects sharing a method name resolve to the same edge target. [DOCUMENTED — `graph_extractor.py:9-16`; OBSERVED for the exception path]
**LOCATION:** `sage_k/graph_extractor.py:140-145`, `156-167`
**ORIGIN:** NO EVIDENCE for the boundary itself. C19 documents that C10 is unrelated to C8 and was a separate code sample given the same wrapper treatment, retained because the source repo bundled it that way.
**DEPENDS ON:** S23
**FAILURE MODE:** Unparseable input raises out through the adapter, bypassing Phase 3 entirely — no outbound hash is stamped and no `GSA_*` status string is produced. This is the only path in C9 where a failure escapes as an exception rather than as a status string. Missing input produces a valid empty result indistinguishable from a genuinely empty module.
**CONFIDENCE:** high

---

**SEAM ID:** S35
**NAME:** Declared versus actual dependencies
**TYPE:** OTHER — a dependency-declaration boundary between what installation promises and what the code imports. Secondary: none
**SIDE A:** C15 `pyproject.toml`, C16 `requirements.txt`
**SIDE B:** C1–C14 actual imports
**WHAT CROSSES:** Package names. [OBSERVED]
**CONTRACT:** NO EVIDENCE — the two files state different things and nothing reconciles them.
**ENFORCEMENT:** None. `pyproject.toml` declares `dependencies = []`, so `pip install -e .` installs nothing beyond the package. `requirements.txt` pins eight packages: `fastapi`, `uvicorn`, `psycopg2-binary`, `anthropic`, `pytest`, `numpy`, `pydantic`, `python-dotenv`. Of these, only `numpy` appears in code (soft, S33) and `pytest` is needed to run C11. The other six are referenced nowhere in any tracked `.py` file. Installation succeeded and all four tests passed with none of them installed. [OBSERVED — grep plus execution]
**LOCATION:** `pyproject.toml:8-11`; `requirements.txt:1-8`
**ORIGIN:** NO EVIDENCE
**DEPENDS ON:** none
**FAILURE MODE:** A reader takes `requirements.txt` as a statement of what the system needs or touches — implying a web service, a Postgres store, and an Anthropic API client — none of which exist in the tracked code. C19 mentions `psycopg2` nowhere; `scenarios.py:203-210` mentions pointing storage at Postgres "later," which is the closest thing to a corroborating reference and does not account for the other five.
**CONFIDENCE:** high

---

**SEAM ID:** S36
**NAME:** Documentation-to-code boundary
**TYPE:** OTHER — a description boundary: what the repo's prose asserts versus what the tree contains. Secondary: none
**SIDE A:** C18 `README.md`, C19 `PROVENANCE.md`
**SIDE B:** C1–C16
**WHAT CROSSES:** File names, a run command, a layout diagram, a layer table, and a file inventory. [OBSERVED]
**CONTRACT:** NO EVIDENCE
**ENFORCEMENT:** None. Specific divergences, all directly checkable:
- C18's Quick Start is `python GSA_Governance_Operating_Core_Enterprise.py`; that file does not exist in the tree.
- C18's "Project Layout" shows a three-entry repo (`GSA_Governance_Operating_Core_Enterprise.py`, `README.md`, `.gitignore`) against an actual 20 tracked files.
- C18's 21-row "Implemented Layers" table (Human Approval Workflow, Immutable Audit Ledger, Rate Limiting, Circuit Breaker Protection, Adaptive Threshold Control, Resilience Plane, Production Entrypoint, and so on) names capabilities; grep finds no rate limiter, no circuit breaker, and no ledger type in the tracked code.
- C18 states "No external dependencies — pure standard library," which agrees with C15 and contradicts C16 (see S35).
- C19 describes a five-file repo containing `artifact_1.py`, `artifact_2.py`, `artifact_3.py`; commit `baf5ec8` deleted all three.
- Neither C18 nor C19 mentions C2–C7 at all; grep for "scenario" returns zero hits in both. [OBSERVED]
**LOCATION:** `README.md` (whole file); `PROVENANCE.md` sections "Line and file counts," "Whether the artifacts execute"
**ORIGIN:** NO EVIDENCE for C18's state. C19's origin is DOCUMENTED — it describes itself as an archival record written against the pre-rebuild tree, and it correctly describes that tree.
**DEPENDS ON:** S37
**FAILURE MODE:** A reader following C18 cannot run the system; a reader following C19 looks for three files that no longer exist; a reader of either concludes C2–C7 are not present. C20 remains the only accurate record of C8/C9/C10's provenance.
**CONFIDENCE:** high — every divergence was checked directly against the tree.

---

**SEAM ID:** S37
**NAME:** Rebuild commit boundary
**TYPE:** TIME — a lifecycle boundary between the archived artifact and the reconstructed package. Secondary: PERSISTENCE
**SIDE A:** commits `aba7c81`, `cc691e8`, `3536155` (initial, archive, docstring correction)
**SIDE B:** commit `baf5ec8` (rebuild)
**WHAT CROSSES:** Content. `baf5ec8` deletes `artifact_1.py`, `artifact_2.py`, `artifact_3.py` (1,320 deletions) and adds 18 files / 3,054 insertions, including the whole of C2–C7. [OBSERVED]
**CONTRACT:** C19 asserts the source artifacts are preserved verbatim; after this commit, the only surviving verbatim copy is inside C20. [OBSERVED]
**ENFORCEMENT:** Git history retains the deleted blobs; C20 retains the source conversation including all three code blocks in context, and C19 states it is the complete source document copied unmodified. [DOCUMENTED — `PROVENANCE.md`, "Extraction: what was stripped"]
**LOCATION:** Commit `baf5ec8`; `TRANSCRIPT.md`
**ORIGIN:** DOCUMENTED for C8/C9 only — the commit message reads "Rebuild as installable package; fix adapter sync/async bug and chain-verification bug," and `gsa_adapter.py:1-39` details both fixes. NO EVIDENCE for the addition of C2–C7, which the message does not mention.
**DEPENDS ON:** none
**FAILURE MODE:** If C20 were lost or C19 revised, the chain from the reconstructed modules back to their source would break; C19 itself flags that the artifacts do not execute and that git history reflects archival date rather than development chronology.
**CONFIDENCE:** high

---

**SEAM ID:** S38
**NAME:** Test coverage boundary
**TYPE:** OTHER — a verification boundary separating what is exercised by tests from what is not. Secondary: none
**SIDE A:** C11
**SIDE B:** C8, C9, C10 (covered) / C1–C7 (not covered)
**WHAT CROSSES:** Four test functions. Imports are exclusively `sage_k.gsa_adapter`, `sage_k.graph_extractor`, `sage_k.kernel`. Nothing from C2–C7 is imported or executed. [OBSERVED]
**CONTRACT:** NO EVIDENCE
**ENFORCEMENT:** Test collection only. Related and adjacent: C4 sets `__test__ = False` on both `TestRun` and `TestHarness` with the comment "Not a pytest test class despite the name," which is a deliberate exclusion from collection — a name-collision boundary between the domain vocabulary and the test framework's. [OBSERVED — `harness.py:94-95`, `176-177`]
**LOCATION:** `tests/test_sanity.py:1-46`; `sage_k/harness.py:94-95`, `176-177`
**ORIGIN:** DOCUMENTED for the `__test__` exclusion (inline comment). NO EVIDENCE for the coverage split.
**DEPENDS ON:** S1, S2
**FAILURE MODE:** C2–C7 comprise roughly 1,700 lines and every hash-binding, approval-gate, and seal mechanism in S3, S4, S5, S6, S9, S10, S12, S13, S15, S16, S20 — none of which is exercised by any test in the repo. `test_adapter_wraps_async_kernel` and `test_adapter_wraps_sync_extractor` are the only tests covering the S22 chain-verification fix the commit message names.
**CONFIDENCE:** high — verified by reading and by running the suite (4 passed).

---

**SEAM ID:** S39
**NAME:** Executable entry points
**TYPE:** CONTROL — where execution may begin. Secondary: none
**SIDE A:** C12, C13, C14
**SIDE B:** C8, C9, C10
**WHAT CROSSES:** Process invocation; hand-constructed seed envelopes; printed output. [OBSERVED]
**CONTRACT:** Each demo must seed `gsa_chain_history` and compute `gsa_interlock_hash` the same way the adapter would, or S22 rejects the envelope. [DOCUMENTED — inline comment at `run_wrapped_kernel_demo.py:34-35`]
**ENFORCEMENT:** `if __name__ == "__main__":` guards. C13 and C14 each construct an envelope, call `compute_state_signature("GENESIS_HASH_STUB_A01", 0, envelope)`, then `replace()` the header mapping with the corrected hash — the same three-step dance duplicated in C11's `_seeded_envelope` helper. No `[project.scripts]` entry point exists in C15. [OBSERVED]
**LOCATION:** `examples/run_kernel_stress_test.py:32-33`; `examples/run_wrapped_kernel_demo.py:34-48`; `examples/run_graph_extractor_demo.py:36-58`; `tests/test_sanity.py:22-30`
**ORIGIN:** DOCUMENTED — each example's docstring states which artifact function it was reconstructed from (`dual_phase_stress_test`, `main_test_harness`).
**DEPENDS ON:** S22, S23
**FAILURE MODE:** There is no entry point of any kind for C2–C7 — no script, no CLI, no `[project.scripts]`, no example. That subsystem is reachable only as a library import.
**CONFIDENCE:** high

---

## PHASE 3: COVERAGE REPORT

### Components with no seams found

None. Every one of the 30 components appears on at least one side of at least one seam. C17 (`.gitignore`) appears only as enforcement evidence within S30 rather than as a seam side; that is a real finding, not an unexamined one — its only load-bearing line is the `fortress_audit.log` exclusion.

### Components examined but thin

- **C20 (`TRANSCRIPT.md`)** was read selectively, not line by line: 1,352 lines, targeted by grep for structural terms (`interlock`, `universal_foundation`, `Lego`, `deep_freeze`, `Protocol`, `Sentinel`, `regulation`, `ambiguity zone`). The reads confirm the wrapper template's origin (S22, S24, S25) and confirm zero coverage of C2–C7. A full line-by-line read could surface additional documented origins for C8's guardrail thresholds (S27, S28, S29), which are currently NO EVIDENCE.
- **C22 (`fortress_audit.log`)** exists only as generated output; the version inspected was produced by this analysis's own test run, not committed.

### Parts of the system I could not access or read

- **The deleted artifacts as standalone files.** `artifact_1.py`, `artifact_2.py`, `artifact_3.py` were removed at `baf5ec8`. Their content survives inside C20 and in git history, but I read them through C20's quoting rather than as files. C19 states all three fail to parse (`SyntaxError`), so their internal seams could not be verified by execution.
- **C25 (`Resolver`) and C24 (`ModelClient`) production implementations.** Neither exists in this repo. Everything about S7 and S8 beyond the Protocol shape and the calling convention is unverifiable here.
- **`sealed_channel`, `twin_client`, and "cassettes"**, referenced by `generator.py:28` and `scenarios.py:35` as existing "elsewhere in this codebase." Grep confirms none is defined in this repo. Whatever seams connect C2–C7 to those components are outside what I can read.
- **`universal_foundation.deep_freeze_structure_function`**, imported by the original artifacts per C20 and absent from this repo; replaced by `_local_deep_freeze` (S21).

### Seams I suspect exist but could not confirm

- **A persistence seam for `TestRun` and `DriftReport`.** Both expose `to_dict()` and both are consumed by `RealignmentTrail` and `calibration_suggestion` as historical sequences, which implies storage across months and years. No save/load path for either exists in the repo. Whether that seam lives in an untracked caller or does not exist is undetermined.
- **A seam between C2–C7 and the "Sentinel" system itself.** C25's Protocol is the only visible edge. Whether C2–C7 were extracted from a larger codebase containing that system, and what else crossed that boundary, is not determinable from this tree.
- **An audit-log reader/verifier for C22.** S30's HMAC implies one exists somewhere; nothing in this repo reads the file, and the canonicalization asymmetry means the verification procedure is not recoverable from the writer alone without care.
- **A regulation/interpretation store.** `InterpretationContext` carries `regulation_text` and `chosen_interpretation` as plain strings supplied by a caller, and `interpretation_version` is threaded through C4, C5, and C6 as a bare string. Whatever produces and versions those strings sits outside this tree.

---

## PHASE 4: SPECULATIVE SECTION (QUARANTINED)

*Everything below is INFERRED by definition. Nothing here is a finding and nothing here may be cited as one.*

Boundaries that could exist here and do not:

1. **No seam gates the `situation` dict's contents before it reaches the resolver.** Underscore-prefixed model commentary keys travel with the facts (S5).
2. **No shared result-vocabulary boundary between C4 and C5.** The four result strings are duplicated as literals rather than imported (S11).
3. **No enforcement boundary on `interpretation_version`.** It is carried everywhere and compared nowhere (S17).
4. **No seam separates a never-sealed record from a tampered one.** `verify()` returns `False` for both (S15).
5. **No boundary reconciles C15 and C16.** Nothing detects that they disagree (S35).
6. **No namespace or packaging boundary separates the two module clusters.** They are held apart only by the absence of imports (S2).
7. **No transaction or atomicity boundary on `ScenarioLibrary.save`.** A concurrent or interrupted write has no seam protecting it (S20).
8. **No seam gates whether a `RealignmentRecord` may be sealed without drift evidence.** `drift=None` is constructible, sealable, and renderable (S14).

---

*End of inventory. 30 components, 39 seams.*
