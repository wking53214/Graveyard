# Burial: AC-HCCSE, retired in full

**Repo:** `wking53214/AC-HCCSE` (public at burial)
**Snapshot commit:** `b3cac9e` (main, 2026-10-07), the last live state
**Date:** 2026-10-10
**Decision:** William N. King

## Why

AC-HCCSE (Anti-Cog / Human-Centered Customer Service Engine) was a September 2026 reconstruction of
one 187-line Gemini artifact (activity record of 2026-06-22). The original repo was lost. It scores
finished customer calls for friction, groups them for review, and picks who handles the next call.
It is plain standard-library Python, nothing in the stack imports it, and the pieces worth keeping
already exist elsewhere in the stack or sit outside the stack's scope. Nothing needed porting.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Friction score (duration divided by a 300 s baseline, plus 0.5 per transfer; ALPHA below 1.2, BETA below 3.0, GAMMA above) | Not ported. The 300 s baseline and the "put signals on one dimensionless scale" idea also appear in the friction engine ported from ICEBURG to GSA-815 (`Latent/ivr_friction_engine.py`). The call-level score itself has no consumer. |
| Batch review and directive (one GAMMA escalates, BETA needs three) | Not ported. Kept here as a worked example of an asymmetric escalation rule. |
| "No evidence is not a clean bill of health" (empty batch reports `empty`) | Already a stack principle. sage-k and sentinel_os interpretation reports say it in the same words ("This is not a pass. The zone has no evidence behind it."). |
| Allocation (continuity 0.7 against capacity 0.3, ties broken on id) | Not ported. Deciding which agent takes the next call is ACD work, which GSA-815 and ICEBURG both put outside the IVR boundary. No home exists for it. Kept here. |
| Reproducible review sampler (private RNG, seeded) | Not ported. GSA-815 already seeds its own generators the same way. |
| Orchestration, records, demo, 22 tests | Not ported. Kept here as the record. |
| `PROVENANCE.md`, `RECONSTRUCTION.md` | Kept in `snapshot/`. The record of where the code came from and the seven fixes made to the recovered artifact (fake `confidence_value` removed, magic numbers made config, and so on). |

## Usefulness review (before burial)

- Read in full: README, PROVENANCE, RECONSTRUCTION, all six modules, tests, demo, CI.
- Searched every local repo for any import or use of its classes (`RecordEvaluator`,
  `ResourceAllocator`, `ReviewGroup`, `DataSampler`, `OrchestrationSystem`). None outside this repo and
  the Graveyard.
- Checked for overlapping concepts in GSA-815 and sentinel_os (continuity routing, transfer counts,
  empty-batch status, sampling). Only the three overlaps in the table were found.
- Ran the 22 tests and the demo on the final commit: all pass.
- Nothing ported.

## What's here

- `snapshot/`: every tracked file at `b3cac9e`, 18 files. CI is kept as `_github_disabled/` so it never runs here.
- `ac-hccse-full-history.bundle`: complete history (3 commits) plus pull ref #1. Verified with
  `git bundle verify`, and a clone of it matches the snapshot.

## Known issues at time of burial

Recorded so a revival starts from the truth:

- It is a reconstruction of one Gemini record, not the original repo. The original's other artifacts
  and its transcript are gone; six of the nine archived artifacts did not run.
- The scoring constants (300 s baseline, 0.5 per transfer, cut points 1.2 and 3.0, weights 0.7 and 0.3)
  come from the recovered artifact. No real call data backs them.
- The score sees only duration and transfer count. It says nothing about outcome, so a long call that
  fully resolved the problem scores the same as a long call that did not.
- Routing weights make continuity beat capacity, so a customer's previous agent keeps getting the work
  however busy they are. The code does not cap that.
- A local `ac_hccse.egg-info` directory existed in the working copy. It was ignored by git and is not in the snapshot.

## Bringing it back

- Whole repo with history: `git clone ac-hccse-full-history.bundle AC-HCCSE`
- Files only: copy `snapshot/` and rename `_github_disabled` back to `.github`.
- `pip install -e .` then `python3 -m pytest tests/ -q`.
