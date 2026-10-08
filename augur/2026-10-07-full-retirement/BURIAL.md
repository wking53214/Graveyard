# Burial: Augur, retired in full

**Repo:** `wking53214/augur`
**Snapshot commit:** `1fc7611` (main), the last live state
**Date:** 2026-10-07
**Decision:** William N. King

## Why

Augur was an optional, veto-only simulation screen. It could refuse an action but
never approve one. Most of its kernel is the same code as the sage-k kernel, which
is already buried, and its CNS connector matches the connectors in other stack repos.
A full function-by-function review found nothing that would make another live repo
better. The one conditional candidate, a model-driven error term for the fortress
kernel's risk tracking, was not ported. The fortress kernel was instead fixed to use
a seeded random generator (fortress-kernel PR #9).

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Simulation kernel, run loop, shared kernel classes | Buried sage-k copy (`graveyard/sage-k`) and `sentinel_os` |
| Predictive controller (mock-based prototype) | `snapshot/augur/predictive_controller.py` only |
| CNS connector | `snapshot/augur/cns_connector.py`; the same pattern lives in ccc, conservation_kernel, dit, governance_gateway |
| Audit signing | DGK and sage-k audit blocks |
| Tests | `snapshot/tests/` (34 unique Augur tests, plus connector tests) |

## What's here

- `snapshot/`: every tracked file at `1fc7611`, exactly as it was.
- `augur-full-history.bundle`: complete history (20 commits on main, 4 refs).

## Known issues at time of burial

- The predictive controller runs against a mock model. Its constants are uncalibrated,
  and its provenance check is a string comparison, not a cryptographic check, despite
  the docstring. It has no test in any repo.
- observe-perceive pins Augur at `9e24dab` and `7022ead`. Both pinned commits fall back
  to a published default audit key outside production, with no warning. Current Augur
  main fixes this, but observe-perceive's pins do not pick up the fix. Its pins should
  be updated or the fix backported.
- The optional simulation screen in observe-perceive fails at construction if Augur is
  absent. The default path does not use it.

## Keeping the pins reachable

- Branches `pin/9e24dab` and `pin/7022ead` point at the two pinned commits.
- Both commits are ancestors of main, so they remain reachable after the README-only
  retirement branch is merged.

## Bringing it back

- Whole repo with history: `git clone augur-full-history.bundle augur`
- Files only: copy `snapshot/`.
