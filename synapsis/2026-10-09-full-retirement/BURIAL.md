# Burial: Synapsis, retired in full

**Repo:** `wking53214/synapsis` (private at burial, Apache-2.0)
**Snapshot commit:** `a9fa5fe` (Main), the last live state
**Date:** 2026-10-09
**Decision:** William N. King

## Why

Synapsis set out to reconstruct how a complex system arrived at its current state: structure, history, snapshots, timelines, and governance. Its README states that most of that is not built. What exists is a small scanner, basic per-file metrics, a flat JSON store, and a CLI. The README's architecture diagram is a backlog, not a status report. Nothing in the stack uses it, and nothing else in the stack needs what it has.

## Usefulness review (before burial)

- **Imports:** no live code in any local clone imports `synapsis`.
- **Tests:** 50 pass with `src/` on the path. One test file fails to collect unless the package is installed, so a clean CI run would fail. The README's "no tests" line is out of date.
- **Analyzer run:** `analyze` on its own source scanned 25 files and wrote a snapshot. The pipeline works end to end, at small scale.
- **Vendored extractor:** `src/synapsis/analysis/astgraph/` (`extractor.py`, `model.py`) is byte-identical to the AST repo, which is already buried in the Graveyard and ported to sentinel_os `tools/wiring_verify`. Nothing new here.
- **Gitignore helper (not reusable):** `analysis/gitignore.py` does not match Git's rules. Tested against `git check-ignore` on a scratch repo, it got 3 of 6 files wrong. It ignores negated patterns (`!keep.log`), misses anchored patterns (`/build/`), and misses `**/` patterns. Do not port it.
- **Symbol extraction and metrics:** duplicated by `ghost_main_check/ghost_buster` and sentinel `tools/wiring_verify`. Nothing to gain.
- **Snapshot and JSON storage:** flat key-value files with no linkage between snapshots. Sentinel's custody work covers this more rigorously.
- **Walker gap elsewhere (noted, not ported):** sentinel `tools/wiring_verify` and the Gemini `scan.py` walk with `os.walk` and a hard-coded skip list. They do not read `.gitignore`. The fix is to take the file list from Git, not from Synapsis's code. This is the only finding from this review that should go anywhere, and it belongs to sentinel.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Source, tests, config, docs, license, notice | `snapshot/` (63 tracked files at `a9fa5fe`) |
| Full history | `synapsis-full-history.bundle` (31 commits, 5 pull-request refs) |
| Architecture write-up | `snapshot/README.md` (the diagram is a backlog) |
| Walker gap | sentinel_os `tools/wiring_verify` (not yet addressed) |

## What's here

- `snapshot/`: all 63 tracked files at `a9fa5fe`, including LICENSE (Apache-2.0), NOTICE, CHANGELOG, SECURITY, the `config/` folder, and `archive/imported-variants/` (7 extractor variants, not checked against the AST burial).
- `synapsis-full-history.bundle`: complete history. Verified with `git bundle verify`, which reports a complete history. Size is about 15 MB because the history includes an untracked `.venv` that was committed before commit `c9a753f`.

## Checks before publishing

- Secret scan of all commits (AWS keys, private keys, GitHub and OpenAI-style tokens, api_key/secret/token/password assignments): no hits.
- Personal data: the only email addresses are placeholders (`YOUR_EMAIL@example.com`). One file, `config/defaults.yaml.save`, is a nano save header showing a local path that contains the GitHub handle. That handle is already public, so it was left as-is.

## Known issues at time of burial

- Gitignore logic is wrong (see above).
- Test collection fails unless the package is installed.
- The README's "no tests" line is stale.
- Most of the architecture is unbuilt: archaeology, knowledge graphs, timelines, diffing, restoration, search, and governance scorecards.
- The `.venv` committed before `c9a753f` is in history.

## Bringing it back

- Whole repo with history: `git clone synapsis-full-history.bundle synapsis`
- Files only: copy `snapshot/`.
