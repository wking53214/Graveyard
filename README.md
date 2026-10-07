# Graveyard

Anything stripped out of a repository because it doesn't belong there gets
buried here instead of deleted. The live repo stays honest about what it
actually does, and nothing is lost.

## Layout

One folder per source repo, then one folder per burial:

```
<repo>/<YYYY-MM-DD>-<what-was-removed>/
  BURIAL.md      what was removed, why, where it came from, how to bring it back
  <files>        the removed material, verbatim

A whole retired repo is stored as `snapshot/` (files as they were) plus a git
bundle (complete history). CI folders are renamed so they never run here.
```

## Burials

| Date | Repo | What | Why |
|---|---|---|---|
| 2026-10-06 | sage-k | GSA checkpoint/re-entry, fork/join merging, temporal doorway gate | Written but never used anywhere in the repo |
| 2026-10-06 | sage-k | **Entire repo retired** (snapshot + full git history) | Every part already done better elsewhere in ≡TACK |
| 2026-10-06 | Triad-42 | Its own origin rules: provenance graph, fact promotion, relabel, erasure cascade | Second copy of CCC's rulebook; a reviewer must not certify facts |
| 2026-10-06 | ccc | Turning points, threads/branches, simulations, official terms, the "42" dialogue loop | Used nowhere in ≡TACK; no article of Constitution v4.0 (candidate) requires CCC to hold them |
| 2026-10-07 | ghost_tools | Branch `feature/zts-cns-docking` (full history bundle + patch) | Stale refactor branch whose squash-merge (#78) broke main; repaired by #82, nothing left to keep |
| 2026-10-07 | vanguard | **Entire repo retired** (snapshot + full git history) | Code byte-identical to copies in TOUCHSTONE; README analysis kept here as the record |
