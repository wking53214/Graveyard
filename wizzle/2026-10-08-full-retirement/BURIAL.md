# Burial: WIZZLE, retired in full

**Repo:** `wking53214/wizzle` (private; its live README now says retired once the tombstone merges)
**Snapshot commit:** `8622cbb` (main), the last live state before retirement
**Date:** 2026-10-08
**Decision:** William N. King

## Why

WIZZLE was an experimental "epistemic adversary." It was meant to test whether an autonomous software modifier (its "Ghost") is entitled to the conclusions it draws from repository history. The repo holds a Python package of about 6,900 lines, 114 passing tests, and design notes. Its own STATUS file says Phase 2 is 50% done. Phases 3 and 4 (overclaim detection, minimization, holdout evaluation, the full CLI) were never started. The CLI commands are stubs. Nothing in the stack imports it as a package (but see the correction below: its code was already copied into SWIZZLE).

## Correction (2026-11-13)

The review below compared WIZZLE only with ghost_tools and missed SWIZZLE. WIZZLE's code had already been
brought into SWIZZLE on 2026-09-13 (SWIZZLE commit `bb9079d`, "Integrate Wizzle independent verification
subsystem"), before this burial. Found by comparing this snapshot with the live SWIZZLE repo:

- SWIZZLE's `swizzle/wizzle/` holds the evolved package: epistemic model, oracles, additional oracles,
  contrastive evaluation, evidence and action entitlement, ghost attacks, ghost invoker, ghost simulator,
  history generator, evaluator and experiment record. Its tests are in `Tests/wizzle/`.
- The intent taxonomy (16 categories) and evidence provenance (7 categories) are defined there.
- `experiment_record.py` is byte-identical to this snapshot. The other files have changed since.
- `tools/wizzle/` holds `build_scenarios.py`, `evaluate_scenarios.py` and `reconstruct_history.py`.
  `fixtures/wizzle-forensics/` holds three files (`enums.py`, `library.py`, `test_status.py`) that are
  byte-identical to ones in this snapshot.
- SWIZZLE also has a holdout corpus (`corpus/holdout`) and a holdout test. Whether it follows the holdout
  design planned here was not checked.

So the rows marked "no consumer" below were wrong for the oracle, taxonomy and contrastive material. The
rows are corrected in place. Nothing needs to be brought back from this burial for those parts.

## Usefulness review (run before burial)

Each idea was checked against the live stack. Result: nothing ported. Each idea below was either already in the stack or had no consumer. (Corrected 2026-11-13: several were already in SWIZZLE; see the correction above.)

| Idea in WIZZLE | Finding |
|---|---|
| Entitlement framing: does the evidence justify the conclusion? | Already in ghost_tools `docs/forensics-limits.md`. That document is WIZZLE's FORENSICS_SCENARIOS argument, kept after its fixture was deleted in ghost_tools 1.9.1. |
| "Evidence that costs nothing to fake does not lower a severity" | Already in ghost_tools CHANGELOG 1.7.8. |
| Intent taxonomy (16 categories) and evidence provenance (7 categories) | Not in ghost_tools. Corrected: both live in SWIZZLE `swizzle/wizzle/epistemic_model.py`. |
| Oracle independence: oracles cannot read the conclusion or the ground-truth label | Tested in WIZZLE. Not found by name in ghost_tools. Corrected: SWIZZLE has `Tests/wizzle/test_oracle_independence.py` and the oracle modules. |
| Contrastive pairs (cases that differ by one fact) | Built as a framework in WIZZLE. Not in ghost_tools. Corrected: SWIZZLE has `swizzle/wizzle/contrastive_evaluation.py` and its test. |
| Holdout evaluation framework | Planned, not built here. SWIZZLE has a holdout corpus and test; not compared against this plan. |
| Minimization and replay of findings | Planned, not built. Design notes only. |
| Scenario commits (`16e9923`, `3e2ddc3`, `ce544ad`, `a1a1356`) | Named by ghost_tools' fixture as the source of the scenarios. Not present in WIZZLE's own history either. The scenarios can't be rebuilt from this repo. SWIZZLE has `tools/wizzle/build_scenarios.py`; whether it rebuilds those four commits was not checked. |

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Entitlement argument and "cheap evidence" lesson | ghost_tools `docs/forensics-limits.md`, CHANGELOG 1.7.8 |
| Package, 114 tests, epistemic model, taxonomies | Evolved copy live in SWIZZLE `swizzle/wizzle/` and `Tests/wizzle/` (since 2026-09-13); original also in this burial (`snapshot/`) |
| STATUS and design notes | Only in this burial (`snapshot/`) |
| Scenario commits named in the ghost_tools fixture | Not recoverable from this repo. SWIZZLE `tools/wizzle/` and `fixtures/wizzle-forensics/` may cover them; not checked |

## What's here

- `snapshot/`: every tracked file at `8622cbb`, exactly as it was (45 files).
- `wizzle-full-history.bundle`: complete history (23 commits). The bundle verifies.

## Known issues at time of burial

- The README says the CLI is not implemented. STATUS says the CLI has working `inspect` commands. The two documents disagree, and this is not resolved here.
- The `Ghost` in the design documents is not connected to ghost_tools in code. No file imports ghost_tools. (SWIZZLE's copy has `ghost_invoker.py`, which launches a Ghost executable found on the path; whether that is ghost_tools was not checked.)
- The scenario commits named in ghost_tools' fixture do not exist in this repo's history.
- The repo had no LICENSE file. The live tombstone branch was licensed under Apache-2.0 on 2026-10-08, per the standard for all repos. The snapshot itself has no license, as it was.

## Bringing it back

- Whole repo with history: `git clone wizzle-full-history.bundle wizzle`
- Files only: copy `snapshot/`.
