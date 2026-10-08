# Burial: ARCHIVE, retired in full

**Repo:** `wking53214/archive` (its live README now says retired)
**Snapshot commit:** `dcc6a54` (main), the last live state before retirement
**Date:** 2026-10-08
**Decision:** William N. King

## Why

ARCHIVE holds eight JSON payloads from one Gemini conversation, plus extracted Python from them and the transcript. Every payload is a request to write an architecture report, and every response in the conversation is prose. The only code is fragments embedded in the JSON. Nothing in the stack imports it.

## Usefulness review (run before burial)

Each idea was checked against the live stack. Result: nothing ported.

| Idea in ARCHIVE | Finding |
|---|---|
| Personal pronoun, speculative language, and empirical-validation filters (`report_8`) | Already live in ZTGKT (`ztgkt/filters.py`). The README's "not present anywhere else" note is out of date. ZTS covers pronouns and hedging (gates G6 and G3). |
| Empirical-validation rule: a claim needs a cause or a number | The cause half is already a flag in ZTS (causality). Requiring a number too would flag most sentences, so it was not ported. Revisit only as a deliberate design choice. |
| Execution pacer | Covered by DIT's governor, ZTS's Kinetic Governor, and ZTGKT's throttle. |
| Text and tone normalizers | Covered by ZTS's Logic Cornerstone normalization. |
| Clinical signal validator | Domain-specific. Lives in ZTGKT `domain.py`. OBSERVE covers the clinical work. |
| UGPIS integration controller (`report_8`) | Its integration map is in ZTGKT `docs/INTEGRATION.md` and `reference/`. |
| Harness and governance decider tests (`report_9`) | Older snapshot. The live `GovernanceDecider` and governance harness in sentinel_os have their own tests. |
| PULSEARM pipeline and Fortress (`report_2`) | Cannot run. Its dependencies (Kalman filter, temporal engine, calibration layer, artifact suppressor) are not defined anywhere in the stack. Fortress moved to its own repo. |
| Latent payload diffs (`report_1`) | Historical design notes. The live `LatentPayload` is in OBSERVE. |
| Omega, GSA equilibrium, and sycophancy-filter narrative (`report_2`, `report_3`) | Narrative material, not design. Names do not appear anywhere in the stack. |
| Meta-OS menu config (`report_5`) | Not code. No destination. |

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Linguistic filters | ZTGKT `ztgkt/filters.py`, ZTS |
| Pacing | DIT, ZTS, ZTGKT |
| Clinical validation | ZTGKT `domain.py`, OBSERVE |
| UGPIS integration map | ZTGKT `docs/INTEGRATION.md` |
| Harness and decider | sentinel_os (live) |
| Payloads, transcript, extracted code, and provenance | Only in this burial (`snapshot/`) |

## What's here

- `snapshot/`: every tracked file at `dcc6a54`, exactly as it was (56 files: eight JSON payloads, the extracted `.py` files, the transcript, the provenance file, and the README).
- `archive-full-history.bundle`: complete history (6 commits on main).

## Known issues at time of burial

- Seven of the eight JSON payloads are not valid JSON. The embedded code has unescaped quotes. Only `artifact_5.json` and `artifact_7.json` parse. Nothing was repaired.
- Indentation was flattened in every payload, and doubled characters were collapsed (for example `__init__` became `init`). These cannot be reversed mechanically.
- The payloads name some real-looking source files (`claude_governance_api.py`, `production_harness.py`, `test_governor_failclosed.py`, and an ICD codes CSV). They were not verified.
- The README's "not present anywhere else" note for the report_8 filters was wrong at burial time. ZTGKT has them.

## Bringing it back

- Whole repo with history: `git clone archive-full-history.bundle archive`
- Files only: copy `snapshot/`.
