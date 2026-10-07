# Burial: VANGUARD, retired in full

**Repo:** `wking53214/vanguard`
**Snapshot commit:** `8df86a7` (main, 2026-10-07), the last live state
**Date:** 2026-10-07
**Decision:** William N. King

## Why

VANGUARD was a perimeter sketch that never ran. Its two code files are byte-identical
copies of files already in TOUCHSTONE, so the only thing unique to this repo was the
analysis in its README. That analysis is preserved here and in TOUCHSTONE's archive notes.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Behavioral simulation, flattened (one line, 9.9 KB) | TOUCHSTONE `specimens/pairs/vanguard-behavioral-simulation-flattened.py` (identical) |
| Behavioral simulation, readable reconstruction | TOUCHSTONE `specimens/pairs/vanguard-behavioral-simulation.py` (one class renamed) |
| Governance wrapper (45 lines, does not run) | TOUCHSTONE `specimens/superseded/vanguard-unified-governance-wrapper.py` (identical) |
| Contradiction word pairs, velocity limits, +15/-75 bounds | sentinel_os `sage_k/kernel.py` (SAGE-K copy, buried 2026-10-06) |
| Echo state network and Lyapunov stability | Implemented in URE and DGK. VANGUARD only names them. |

## What's here

- `snapshot/`: every tracked file at `8df86a7`, exactly as it was, including both code files.
- `vanguard-full-history.bundle`: complete git history (10 commits) in one file.

## Known issues at time of burial

Recorded so a revival starts from the truth, not the README:

- The audit logger silently drops write errors, so a failed log write goes unnoticed (fail-open).
- The docstring claims echo state networks and Lyapunov stability. The code implements neither.
- The default signing key is public. The fallback value sits in plain sight in the code.
- The wrapper passes a hardcoded keystone string, "Coldfire." The wrapper never runs, so it was
  treated as a placeholder. This was not verified against any real system.
- The wrapper cannot run: it uses names it never defines (PipelineCycleManager, UnifiedSovereignKernel,
  system_logger) and its type hints reference unimported names.
- The same weaknesses appear in SAGE-K (see `sage-k/2026-10-06-full-retirement/BURIAL.md`).
  The live gsa-815 cassette had the same fail-open audit writer and fallback key; that is being fixed
  in a separate PR on gsa-815.

## Bringing it back

- Whole repo with history: `git clone vanguard-full-history.bundle vanguard`
- Files only: copy `snapshot/`.
