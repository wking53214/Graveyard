# Burial: ICEBURG, retired in full

**Repo:** `wking53214/ICEBURG` (public at burial)
**Snapshot commit:** `3cc5752` (main, 2026-10-07), the last live state
**Date:** 2026-10-10
**Decision:** William N. King

## Why

ICEBURG was a reconstruction of the early-July 2026 IVR (phone call routing) simulation kernel,
rebuilt on 2026-09-11 from archive references. Its own README marks it "off the live path" and
"historical lineage." It is the ancestor of sentinel_os (by rename), and the live kernel and live
IVR app are sentinel_os and GSA-815. Nothing imports it. One component had no live equivalent and
was ported out first; everything else is either already live or kept here as the record.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Latent friction engine (`Latent/LatentPayload.py`) | **Ported** to GSA-815 as `Latent/ivr_friction_engine.py` (`IvrFrictionEngine`), PR #19. GSA-815 held only an older, unwired, weaker copy. |
| Stimulus derivation (`derive_stimuli`) | Already live in GSA-815, identical. Not ported. |
| Simulator (fails closed on undeclared branches), journey-based `Build_Graph` | GSA-815 has the same names. Live copies are queue-era (see below). Kept here as the corrected reference. |
| Path congestion, integration loop (tick: advance, group, aggregate and triage, sweep) | Not ported. No live consumer; the tick design is recorded in `snapshot/ARCHITECTURE.md`. |
| Telemetry (append-only, structural and content hashes), cluster runner | Not ported. Hash-chained custody in sentinel_os is stronger. Kept here only. |
| RL stubs (`rl_ppo`, `rl_marl`) | Deterministic and untrained by design (weights from `RandomState(815)`). Not ported. |
| Calibration harness (`Training/Modules/calibrate_expected_wait.py`) | Kept here only. The latent constants it would tune remain uncalibrated. |
| `Intent`, `Emotion`, `CallerState`, `IngestAdapter`, `TwilioSyntheticLogGenerator` (stub bodies on purpose) | GSA-815 has live equivalents. Not ported. |
| `QueueStress.py` | Superseded in its own README; nothing imports it. |
| Four locked corrections and the ACD-door boundary | Recorded in `snapshot/ARCHITECTURE.md`, `PROVENANCE.md`, `SCORECARD.md`. Kept here as the record. |

## Usefulness review (before burial)

Read in full: README, ARCHITECTURE, PROVENANCE, SCORECARD, every module, and the latent tests.
Each module was compared with the live GSA-815 and sentinel_os code by name and by reading.

- **Ported:** the friction engine. Improvements over GSA-815's older parked model: friction and
  resolution can both apply in one step (the old `elif` made relief never fire), accrual grows past
  a tolerance, relief is capped within a step and bounded above baseline, waits are normalized
  against a 300 s reference, `memory_flag` and `peak_frustration` never decay, and two labelled
  hashes separate "a step elapsed" from "something real happened."
- **Check on the port:** the new engine matches the original over 61,273 steps in 2,000 randomized
  trials with no mismatches and no mutation of its argument. 23 tests ship with it.
- **Not ported:** everything else in the table above, with the reason given per row.

## Cross-stack findings (found during the review, not fixed here)

- GSA-815 still carries queue-era code (`{q}_queue` nodes, `QueueState`,
  `queue_staffing_bayes_integration`). ICEBURG's Corrections 1 and 2 declare queue state
  epistemically unavailable to the IVR. Worth a deliberate decision in GSA-815.
- GSA-815's live `_update_queue` fails open with a "missing" status, where ICEBURG's Simulator fails closed.
- observe-perceive still pins buried AUGUR commits (they remain reachable in the AUGUR burial).
- The ported friction constants are uncalibrated (the earlier AUC 0.73 finding stands).

## What's here

- `snapshot/`: every tracked file at `3cc5752`, 39 files.
- `iceburg-full-history.bundle`: complete history (9 commits) plus the three pull-request refs
  (#1, #2, #3). Verified with `git bundle verify`.
- ICEBURG had no CI folder, so none was renamed.

## Known issues at time of burial

Recorded so a revival starts from the truth, not the README:

- PPO and MARL store `lr`, `gamma` and `eps_clip` but never train. They are stubs, not learning.
- The latent constants (`_FRICTION_CAP=20`, path-congestion weights, and others) have no real call data behind them.
- `reset_for_new_call` and `load_from_dict` are unwired, because the replay layer was never recovered.
- Modules reach each other through `sys.path.insert` hacks into Aggregation and Latent.
- Not recovered, and listed absent rather than stubbed: live calls, Twilio, staffing, ACD, replay, API, GPU Bayes, k8s, training, real data.
- About 72% of the 2,031 engine lines are verbatim recovered; the rest is reconstruction.

## Bringing it back

- Whole repo with history: `git clone iceburg-full-history.bundle ICEBURG`
- Files only: copy `snapshot/`. Run `python3 run_worked_example.py` for the worked example (needs numpy).
