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
| 2026-10-07 | content-pipeline | **Entire repo retired** (snapshot + full git history, incl. readable-copy branch) | Flattened AI design that cannot run; ~40 undefined names, 18 found elsewhere in the stack, 2 never defined; every job it attempts is done better in the stack |
| 2026-10-07 | UTEP | **Entire repo retired** (snapshot + full git history) | Text instructions reconstructed from one conversation; not code, nothing in the stack depends on it |
| 2026-10-07 | ARLF | **Entire repo retired** (snapshot + full git history) | Reference governance package, never run, never imported; two ideas ported to DGK and ZTS, the rest duplicates existing stack mechanisms |
| 2026-10-07 | Augur | **Entire repo retired** (snapshot + full git history) | Veto-only simulation screen; kernel duplicates sage-k; predictive controller is a mock-based prototype with no tests; observe-perceive pins two commits, which remain reachable |
| 2026-10-08 | stride | **Entire repo retired** (snapshot + full git history) | Reconstruction superseded by DIT and ZTS; its only unique piece, the analytics layer, relabels the policy score and was not ported |
| 2026-10-08 | citadel | **Entire repo retired** (snapshot + full git history) | Its two unique ideas (outcome without a cause, passive voice) ported to ZTS as flags; its rewrites were rejected (one invents a cause). Lineage copies remain in ecology, TOUCHSTONE, DIT, and GSA |
| 2026-10-08 | graph | **Entire repo retired** (snapshot + full git history) | Consolidation workspace with a provisional name and no graph in it; nothing imports it. The GRAPH governance concept lives in PERCEIVE, which is untouched |
| 2026-10-08 | FACTS | **Entire repo retired** (snapshot + full git history) | Reconstruction of a Gemini transcript whose code is GRAPH's `from-facts/` lineage, already buried; nine of 14 artifacts do not parse; nothing ported |
| 2026-10-08 | clip | **Entire repo retired** (snapshot + full git history) | Earlier name of STRIDE; its six code files are byte-identical to copies in the STRIDE burial. Only the design record (PROVENANCE, transcript) is unique here; nothing ported |
