# Burial: AST, retired in full

**Repo:** `wking53214/AST` (private; its live README now says retired)
**Snapshot commit:** `8450c17` (main), the only commit in the repo's history
**Date:** 2026-10-08
**Decision:** William N. King

## Why

AST is `astgraph`, a pure standard-library Python tool. It extracts a structural graph from Python source (classes, functions, calls, inheritance, imports). Each resolved call is graded: A (same file), B (resolved through an import), or U (unresolvable from syntax). Syntax errors are recorded rather than skipped. Nothing in the stack imports the package.

Its ideas now live in sentinel_os `tools/wiring_verify`, which is the working tool for the same question.

## Usefulness review (run before burial)

Each idea was checked against the live stack. Result: nothing left to port.

| Idea in AST | Finding |
|---|---|
| `self` and `cls` resolve to the enclosing class | Already in wiring_verify (`model.py`, owner-class handling). |
| Resolution runs after the walk, so forward references work | Already in wiring_verify. Symbols are collected across the whole tree before calls are resolved. |
| Graded edges (A, B, U) | Ported in sentinel_os PR #62 (step 3). |
| Parse failures recorded with the file's SHA-256 | Ported in sentinel_os PR #62 (step 2). |
| Parse failures carry a source snippet | Not ported. The SHA-256 names the exact file version, and the file is in the repo. |
| Deterministic, sorted output and content hashes | Ported in sentinel_os PR #62 (steps 1 and 4). |
| External nodes make the outside call surface visible | Not ported. wiring_verify leaves out calls that leave the tree on purpose. Adding them would change every reported count. A future design choice, not a port. |
| CONTAINS, INHERITS, and IMPORTS recorded as edges | Not ported. wiring_verify uses inheritance internally for method lookup. No stack consumer reads these as records. |
| Merging per-unit graphs | Not ported. wiring_verify builds one graph for the whole tree. |
| Corpus finding: 36 of 620 generated blocks did not parse | The figure is in the README. The corpus is not in this repo, so the figure is not verified here. |

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Self and class resolution, two-pass resolution | sentinel_os `tools/wiring_verify` |
| Graded edges, parse-failure records, deterministic output | sentinel_os `tools/wiring_verify` (PR #62) |
| Package source and its 32 tests | Only in this burial (`snapshot/`) |

## What's here

- `snapshot/`: every tracked file at `8450c17`, exactly as it was (9 files: the `astgraph` package, its test file, README, LICENSE, and .gitignore).
- `ast-full-history.bundle`: complete history (1 commit). The bundle verifies.

## Known issues at time of burial

- The package passes its 32 tests at burial time.
- The snapshot's LICENSE is MIT, left as it was, because the snapshot is the record as it was. The live repo's tombstone branch was relicensed to Apache-2.0 on 2026-10-08, per the October 2026 standard for all repos.
- The README's corpus figures (11,540 blocks, 36 of 620 failing) cannot be checked from this burial.

## Bringing it back

- Whole repo with history: `git clone ast-full-history.bundle ast`
- Files only: copy `snapshot/`.
