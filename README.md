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
