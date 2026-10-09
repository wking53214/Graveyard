# Burial: ICEBERG, retired in full

**Repo:** `wking53214/iceberg` (private at burial)
**Snapshot commit:** `eb7d8a4` (main, 2026-10-07), the last live state
**Date:** 2026-10-09
**Decision:** William N. King

## Why

ICEBERG was an older IVR (phone call routing) simulator. Its own README says it is
"not the live runtime," "safe to archive," and that the code does not do what the README claims.
Its successor code lives in gsa-815, and the stack's audit and replay ideas live in sentinel_os.
What remained unique was the recovered raw source in `RECOVERY/`, which is kept here.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Live tree (domain models, latent payload, graph build, governance core) | gsa-815 (same names; contents differ, not diffed line by line) |
| Replay stack (ledger, recorder, snapshot, verifier) | Not ported. Superseded by sentinel_os hash-chained custody (`twin_custody`, `ledger_postgres`, `log_rotation_v1`) and cassette replay. |
| RL engines (PPO, MARL, staffing RL, GPU Bayes) | No equivalent found in the local repos searched. Kept here only. |
| Telemetry aggregator, SDK, API, CLI, registry, dashboard | No equivalent found. Kept here only. |
| `RECOVERY/` (80 pasted source files, prompt and response records, validation reports, gsa_adapter prompts) | Kept here, in `snapshot/RECOVERY/`. This is the valuable part of the repo per its own README. |

## Usefulness review (before burial)

- Checked each live module by name and keyword against the local repos. Nothing was ported.
- The replay stack was read in full and compared with sentinel_os. Sentinel's version is stronger.
- Not worth reviving: the routing fallback, the RL engines that are never called, the mock API,
  and `Main.py`, which imports modules that do not exist.

## What's here

- `snapshot/`: every tracked file at `eb7d8a4`, 203 files, including `RECOVERY/`.
- `iceberg-full-history.bundle`: complete history (7 commits) plus the two pull-request refs
  (#1 and #2, both closed). Verified with `git bundle verify`.

## Known issues at time of burial

Recorded so a revival starts from the truth, not the README:

- Routing is fail-open. When the preferred next node is missing, the simulator silently takes the first
  neighbor instead of failing.
- The RL engines (`staffing_rl`, `rl_ppo`, `rl_marl`) are not called from the simulator step. The
  "staffing optimizer" is a clipped `(load - 0.5)` formula, not reinforcement learning.
- The API returns a mock response that always says `next_node: "exit"`. Its `strict_mode` flag does nothing.
- `Main.py` imports `domain.*` and `dashboard_server`, which do not exist. Tests work around it by
  replacing modules in `sys.modules`.
- README claims a `GovernanceEnvelope` class and a governance envelope. The code has neither.
- The replay ledger is append-only only by convention. Entries are not hash-chained, so edits go undetected.
- The recorder stamps events with wall-clock time. Two identical runs never produce matching snapshots,
  which contradicts the "deterministic" claim.
- Two replay stacks exist (`SDK/Replay.py` and `Replay/`) and were never unified.
- The Simulator docstring says `StaffingRLEngine` was removed on 2026-07-02, but `Engines/staffing_rl.py` still ships.
- `orjson` is declared and unused. The README's Kubernetes and ArgoCD manifests are paper only.
  The image `iceberg-runtime:3.x` it references does not exist.
- Source comments contain Cursor `ca://s?q=` citation links, which point to nothing in this repo.
- `RECOVERY/REPORT.md` records a failed download: `iceberg.zip` in the home directory was the text "Not Found."

## Bringing it back

- Whole repo with history: `git clone iceberg-full-history.bundle iceberg`
- Files only: copy `snapshot/`. For the raw recovered source, start with `snapshot/RECOVERY/README.md`.
