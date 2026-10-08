# Burial: WIZZLE, retired in full

**Repo:** `wking53214/wizzle` (private; its live README now says retired once the tombstone merges)
**Snapshot commit:** `8622cbb` (main), the last live state before retirement
**Date:** 2026-10-08
**Decision:** William N. King

## Why

WIZZLE was an experimental "epistemic adversary." It was meant to test whether an autonomous software modifier (its "Ghost") is entitled to the conclusions it draws from repository history. The repo holds a Python package of about 6,900 lines, 114 passing tests, and design notes. Its own STATUS file says Phase 2 is 50% done. Phases 3 and 4 (overclaim detection, minimization, holdout evaluation, the full CLI) were never started. The CLI commands are stubs. Nothing in the stack imports it.

## Usefulness review (run before burial)

Each idea was checked against the live stack. Result: nothing ported. Each idea below was either already in the stack or has no consumer.

| Idea in WIZZLE | Finding |
|---|---|
| Entitlement framing: does the evidence justify the conclusion? | Already in ghost_tools `docs/forensics-limits.md`. That document is WIZZLE's FORENSICS_SCENARIOS argument, kept after its fixture was deleted in ghost_tools 1.9.1. |
| "Evidence that costs nothing to fake does not lower a severity" | Already in ghost_tools CHANGELOG 1.7.8. |
| Intent taxonomy (16 categories) and evidence provenance (7 categories) | Not in ghost_tools. No stack component reads them. Only WIZZLE's epistemic model defines them. |
| Oracle independence: oracles cannot read the conclusion or the ground-truth label | Tested in WIZZLE. Not found by name in ghost_tools. Design record only; no consumer. |
| Contrastive pairs (cases that differ by one fact) | Built as a framework in WIZZLE. Not in ghost_tools. No consumer. |
| Holdout evaluation framework | Planned, not built. Design notes only. |
| Minimization and replay of findings | Planned, not built. Design notes only. |
| Scenario commits (`16e9923`, `3e2ddc3`, `ce544ad`, `a1a1356`) | Named by ghost_tools' fixture as the source of the scenarios. Not present in WIZZLE's own history either. The scenarios can't be rebuilt from this repo. |

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Entitlement argument and "cheap evidence" lesson | ghost_tools `docs/forensics-limits.md`, CHANGELOG 1.7.8 |
| Package, 114 tests, epistemic model, taxonomies, STATUS and design notes | Only in this burial (`snapshot/`) |
| Scenario commits named in the ghost_tools fixture | Not recoverable from any repo here |

## What's here

- `snapshot/`: every tracked file at `8622cbb`, exactly as it was (45 files).
- `wizzle-full-history.bundle`: complete history (23 commits). The bundle verifies.

## Known issues at time of burial

- The README says the CLI is not implemented. STATUS says the CLI has working `inspect` commands. The two documents disagree, and this is not resolved here.
- The `Ghost` in the design documents is not connected to ghost_tools in code. No file imports ghost_tools.
- The scenario commits named in ghost_tools' fixture do not exist in this repo's history.
- The repo has no LICENSE file.

## Bringing it back

- Whole repo with history: `git clone wizzle-full-history.bundle wizzle`
- Files only: copy `snapshot/`.
