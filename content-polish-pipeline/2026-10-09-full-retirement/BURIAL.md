# Burial: content-polish-pipeline, retired in full

**Repo:** `wking53214/content-polish-pipeline` (public at burial, Apache-2.0)
**Snapshot commit:** `5f1cad8` (main), the last live state
**Date:** 2026-10-09
**Decision:** William N. King

## Why

This is a small LLM output quality gate. It checks generated text for first-person pronouns,
speculative language and missing empirical support, and retries with feedback when a check fails.
It is not a standalone product anymore. Its code was moved into `wking53214/ghost_tools` on
2026-09-09 and runs there as the live gate around the LLM call in `ghost_writer`. This standalone
repo is superseded.

## Usefulness review (before burial)

- Searched every local clone for imports of the package. The only match is in an archived
  snapshot in the Graveyard. No live code imports it.
- The live copy lives in `ghost_tools` at `ghost_writer/polish/`. It has evolved since the move:
  the main pipeline file differs by about 80 lines from this repo's copy. Nothing needs to be
  ported from here.
- The purpose overlaps with `wking53214/zts`, whose README describes removing first-person voice
  and hedging. Nothing was ported from this repo to zts.
- The repo's own 42 tests pass at burial.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Source, tests, license, provenance | `snapshot/` (12 tracked files at `5f1cad8`) |
| Live gate (the working version) | `wking53214/ghost_tools`, `ghost_writer/polish/` (not part of this burial) |
| Source and history of the original zip | `snapshot/PROVENANCE.md` |

## What's here

- `snapshot/`: all 12 tracked files at `5f1cad8`, including LICENSE (Apache-2.0), NOTICE and
  PROVENANCE.md.
- `content-polish-pipeline-full-history.bundle`: complete history (one commit on main). Verified
  with `git bundle verify`, which reports a complete history.

## Known issues at time of burial

PROVENANCE.md records the history in full. The main points:

- The package was assembled from a zip that was made in a Claude sandbox. The archive has no
  transcript, so the prompts behind it are not recorded.
- Its core descends from an earlier Gemini-era design. Git history shows packaging dates, not the
  original development.
- Six issues were fixed on 2026-08-27 (unstable output order, a hardcoded default signing key,
  broken import path, an inverted filter check, weak hash function, and a crash on zero attempts).
- The signature is integrity-only unless the caller supplies a secret key. That is documented in
  the README.
- The current code is in ghost_tools, so fixes made there do not flow back here.

## Bringing it back

- Whole repo with history: `git clone content-polish-pipeline-full-history.bundle content-polish-pipeline`
- Files only: copy `snapshot/`.
