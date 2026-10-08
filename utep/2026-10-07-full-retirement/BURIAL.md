# Burial: UTEP, retired in full

**Repo:** `wking53214/UTEP`
**Snapshot commit:** `7de5308` (main, 2026-09-12), the last live state
**Date:** 2026-10-07
**Decision:** William N. King

## Why

UTEP (Universal Token Efficiency Protocol) is a set of plain-text operating
instructions for AI assistants, not code. It was written in one conversation in
August 2026 and pasted into several AI tools. The repo is a reconstruction of that
text from the author's conversation archive. Nothing in the stack imports or runs
it, and nothing in ZTGKT depends on it.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Source conversation | `ChatGPT_History/transcripts/6a712900-a744-83ea-b6ef-330c9df41e2c.md` (primary artifact, per PROVENANCE) |
| Kernel rules (v1.0, v2.0, protocol) | Preserved in `snapshot/kernel/` |
| Core, modules, standards, variants | Preserved in `snapshot/` |
| Setup files for each AI tool | Preserved in `snapshot/deployments/` |
| Preference memories | Preserved in `snapshot/memories/` |
| Lint tool | `snapshot/tools/utep_lint.py` |

## What's here

- `snapshot/`: every tracked file at `7de5308`, exactly as it was.
- `utep-full-history.bundle`: complete history (4 commits on main).

## Known issues at time of burial

- Only the kernel and standards are described as verbatim. The rest was reconstructed
  from the archive, and PROVENANCE marks which files are which. Read PROVENANCE before
  reusing any reconstructed file.
- The repo's memory files hold personal preference text. Treat them as personal.

## Bringing it back

- Whole repo with history: `git clone utep-full-history.bundle utep`
- Files only: copy `snapshot/`.
