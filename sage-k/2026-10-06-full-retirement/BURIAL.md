# Burial: SAGE-K, retired in full

**Repo:** `wking53214/sage-k` (also reached as `SAGE-K`)
**Snapshot commit:** `52a08cd` (main, 2026-10-03), the last live state
**Date:** 2026-10-06
**Decision:** William N. King

## Why

SAGE-K did nothing that is not already done, and done better, elsewhere in ≡TACK.

| Part | Where that job lives now |
|---|---|
| Interpretation loop (scenarios, drift, annual realignment) | `sentinel_os/interpretation/`, a newer copy that also has the cassette resolver seam test. SAGE-K held a stale duplicate. |
| GSA hash-chain wrapper | ANVIL, GRAPH, the GSA gateway audit trail, and the stack's audit layer (Layer 5). |
| Fortress kernel (learning policy under guardrails) | The stack's Kinetic Governor and the trap-to-boundary flywheel, on real execution rather than a toy number. |
| AST call-graph extractor | Not checked against other repos. Small and self-contained; revive from here if a need appears. |

A simulator was considered as SAGE-K's one remaining job and rejected: a
simulator is only worth having when it models something real, Fortress models
a made-up number, and deterministic verification already exists in the stack's
chaos, fire and red-team harnesses.

## What's here

- `snapshot/`: every tracked file at `52a08cd`, exactly as it was. The CI
  workflow folder is renamed `_github_disabled/` so it does not run inside
  Graveyard. The 57 tests pass from this folder as-is.
- `sage-k-full-history.bundle`: the complete git history in one file, including
  the unmerged branch `claude/bury-unused-gsa-features` (PR #3, closed as
  superseded by this burial).

The earlier, narrower burial of three unused GSA features
(`../2026-10-06-gsa-unused-features/`) is kept; it is a subset of this one.

## Known issues at time of burial

Recorded so a revival starts from the truth, not the README:

- GSA reports tampering as a status message and keeps going instead of stopping.
  Wrapping a module it cannot run still produces a valid-looking stamp.
- GSA's chain uses no secret key and travels inside the envelope it protects, so
  a tamperer can recompute it.
- When GSA wraps Fortress, Fortress ignores the envelope's contents and runs its
  own fixed scenario.
- Fortress's word-contradiction guardrail can never fire: the label it inspects is
  hard-coded.
- Constructing a Fortress resets the random number generator for the whole process.
- Fortress's signed audit log has no reader or verifier, and write failures are silent.
- The "Echo State Network" and "Lyapunov" names from the Gemini source describe
  nothing the code does.

## Bringing it back

- Whole repo with history: `git clone sage-k-full-history.bundle sage-k`
- Files only: copy `snapshot/`, then rename `_github_disabled` back to `.github`.
