# Burial: ARLF, retired in full

**Repo:** `wking53214/ARLF`
**Snapshot commit:** `9d4f818` (main), the last live state
**Date:** 2026-10-07
**Decision:** William N. King

## Why

ARLF is a reference package of governance-resolution ideas (certificates for
unresolved questions, escalation gates, a governor, a pipeline, substrate and
RLCF modules) with four test files. It was never run, and nothing in the stack
imports it. Its useful ideas were reviewed against the stack. Two were ported:

- The "cause" idea (every refusal records why it happened) went into DGK, PR #19.
- A step budget (a hard cap on how many steps a run may take) went into ZTS, PR #8.

The rest was left out on purpose. The certificate, escalation mapping and
discharge concepts overlap with mechanisms already in the stack. The verdict
scheme (answers that are not just yes or no, with a fixed set of outcomes) was
also left out. The stack already has many verdict and status enums, so porting it
would duplicate them.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Refusal-cause idea | DGK `feature/refusal-cause`, PR #19 (open) |
| Step budget idea | ZTS `feature/step-budget`, PR #8 (open) |
| Certificate, gates, governor, pipeline, resolution, substrate, RLCF modules | Preserved in `snapshot/proposals/reference/arlf/` |
| Evidence, chronology, entities, lineage, reports, schemas, spec, adversarial | Preserved in `snapshot/` |

## What's here

- `snapshot/`: every tracked file at `9d4f818`, exactly as it was.
- `arlf-full-history.bundle`: complete history (8 commits on main).

## Known issues at time of burial

- The reference modules were never executed. Their tests were never run.
- Verdict scheme was not ported. Certificate and discharge concepts were only partly ported.
- The two open PRs (DGK #19, ZTS #8) must be merged or closed before the ideas
  count as in the stack.

## Bringing it back

- Whole repo with history: `git clone arlf-full-history.bundle arlf`
- Files only: copy `snapshot/`.
