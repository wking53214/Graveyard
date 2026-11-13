# Burial: AUGUR simulation screen, removed from observe-perceive

**Repo:** `wking53214/observe-perceive`
**Removed in:** observe-perceive branch `remove-augur-screen` (stacked on `bump-cns-pin-v4.0.0`), last live commit before removal `eed1514`
**Date:** 2026-11-13
**Decision:** William N. King

## Why

The screen was an optional, veto-only stage that could refuse a request but never approve one. It was
off by default, and the AUGUR repo itself was retired on 2026-10-07 (see `augur/2026-10-07-full-retirement`).
That left observe-perceive carrying a stage whose library is archived and private, which also forced CI to
hold a read token just to install it, and a demo gate and pins nobody would keep alive.

## What's here

| File | What it was |
|---|---|
| `augur_screen_adapter.py` | The adapter the orchestrator loaded when `simulation_screen=True` (354 lines) |
| `test_augur_screen_adapter.py` | Its test file (306 lines) |
| `fixture_augur.py` | The demo fixture that built AUGUR's CNS gate (was `examples/cns_demo/fixture_augur.py`) |
| `removal.patch` | The edits to the files that stayed behind: the orchestrator stage and its two constructor options, `demo_why.py` step 6, the demo and its test, pins, CI key, README and CHANGELOG. Applying it in reverse puts them back |

All three Python files are verbatim copies.

## Also removed (not stored as files)

- `test_a_crashing_screen_refuses_and_says_it_crashed` in `test_chain_failure_paths.py`: a screen that crashes refuses and says it crashed. It is in `removal.patch`.
- Three `.ghost_baseline.json` entries pointing at the two removed Python files.
- The `augur` pin in the `chain` extra of `pyproject.toml` and in `requirements-demo.txt` (commit `1fc76118f75024be5ebebed227c2d9a4530c78b7`).
- The CI step that made a throwaway `AUGUR_AUDIT_KEY` for the demo test.

## What changed in behaviour

- The demo chain went from five gates to four. Scenario S4 used to be refused by AUGUR; it is now refused by ccc.
- `GovernanceOrchestrator` no longer accepts `simulation_screen` or `simulation_seed`, and results no longer carry a `simulation_screen` key.
- `demo_why.py` keeps step 6 ("prediction") as an explicit "no stage" line so the ten-step numbering stays stable.

## Known issues at time of burial

- The adapter needs the AUGUR package, which is archived. The pinned AUGUR commit falls back to a published
  default audit key outside production, with no warning (noted in the AUGUR burial).
- The adapter's import of AUGUR is guarded, but the orchestrator imported the adapter only when asked, so
  restoring it means restoring both halves.

## Bringing it back

1. Copy the three files to their old paths (`fixture_augur.py` goes in `examples/cns_demo/`).
2. In observe-perceive, from the commit that removed them, run `git apply -R removal.patch` (the patch does
   not include the three files or the recorded demo output, which must be regenerated).
3. Restore the AUGUR repo from `augur/2026-10-07-full-retirement` and re-add its pin.
