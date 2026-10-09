# Burial: HTTP (Hyper Truth Testing Protocol), retired in full

**Repo:** `wking53214/http` (public at burial, Apache-2.0)
**Snapshot commit:** `2cfb08a` (main), the last live state
**Date:** 2026-10-09
**Decision:** William N. King

## Why

HTTP is a 7-layer adversarial validation harness: 70 seeded mutations run through 7 inspection
layers, for 490 evaluations. It was reconstructed from old chat archives, and its PROVENANCE.md
says so. Nothing in STACK imports it. Its purpose overlaps with ZTS, the live project for filtering
language-model output, which is a separate repo and stays active.

## Usefulness review (before burial)

- Searched every local clone for imports or references to the package and the protocol name.
  Nothing outside this repo imports it.
- The protocol's write-up lives in the WhitePapers repo (`papers/lean-review/HTTP.md`). That paper
  stays in WhitePapers, per the rule that whitepaper material does not go to the Graveyard.
- The filtration layers overlap in purpose with `wking53214/zts`. ZTS is the live successor for
  that job. Nothing was ported.
- The repo's own tests pass (102 passed, 0 failed) at burial. That shows the code runs. It does not
  show the reconstruction matches the original sessions beyond what PROVENANCE.md claims.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Source, tests, CI config, licence | `snapshot/` (22 tracked files at `2cfb08a`) |
| Reconstruction record (what was recovered verbatim and what was rebuilt) | `snapshot/PROVENANCE.md` |
| Protocol write-up | WhitePapers repo, `papers/lean-review/HTTP.md` (not moved) |
| Live filtration successor | `wking53214/zts` (active, not part of this burial) |

## What's here

- `snapshot/`: all 22 tracked files at `2cfb08a`, including LICENSE (Apache-2.0) and NOTICE.
- `http-full-history.bundle`: complete history (one commit on main). Verified with
  `git bundle verify`, which reports a complete history. The repo had no pull-request refs.

## Known issues at time of burial

- The code was rebuilt from conversation archives. PROVENANCE.md records which parts were recovered
  verbatim and which were reconstructed. Treat the reconstructed parts as a best rebuild, not as the
  original.
- No live consumer in STACK.

## Bringing it back

- Whole repo with history: `git clone http-full-history.bundle http`
- Files only: copy `snapshot/`.
