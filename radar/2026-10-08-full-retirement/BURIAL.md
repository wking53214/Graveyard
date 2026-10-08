# Burial: RADAR, retired in full

**Repo:** `wking53214/radar` (its live README now says retired once the tombstone merges)
**Snapshot commit:** `94017cc` (main), the last live state before retirement
**Date:** 2026-10-08
**Decision:** William N. King

## Why

RADAR was a name given to a system that was EDDP before it was RADAR. The repo is a 2026-09-17 reconstruction of a deleted repo. Its original four commits do not exist here, and the GitHub name now belongs to an empty repo created later. The code it holds is the EDDP lineage. The live `wking53214/EDDP` repo still holds the two main versions byte-for-byte, and its own README calls them reference-only. Nothing in the stack imports RADAR.

## Usefulness review (run before burial)

Each file was checked against the live EDDP repo and the rest of the stack. Result: nothing ported.

| File | Finding |
|---|---|
| `eddp-core-engine-v1.py` | Byte-identical to the copy in live EDDP. Nothing new here. |
| `eddp-core-engine-v2-refined.py` | Byte-identical to the copy in live EDDP. Nothing new here. |
| `eddp-comprehensive-synthesized.py` | Same classes as v2, with the top-level wrapper renamed. Nothing new. Not in live EDDP, so it is kept here. |
| `eddp-pipeline-core-simple.py` | A minimal render, route, and deliver sketch. Covered by the EDDP pipeline. Kept here for the record. |
| `eddp-wrapped-final.py` | An AST graph extractor, byte-identical to the copies in CLIP, STRIDE, and FACTS. Nothing new. |
| `gsa_universal_interlock_wrapper.py` | Its interlock and temporal-gate logic is covered by `sentinel_os/sage_k/gsa_adapter.py`. The original source remains in GSA-815 history. |
| Assessment novelty ratio (`assess_system_novelty`) | Distinct payloads over total runs. A weak repeat signal. DIT's oscillation guard covers repetition. Not ported. |
| Revenue and health reference checks | Hard-coded proxies (revenue divided by 100,000). The same proxy problem noted for the STRIDE analytics layer. Not ported. |
| Predecessor paste (2026-06-05) | Origin unknown. Its evidence is kept here. |

## Where each part lives now

| Part | Where it lives now |
|---|---|
| EDDP v1 and v2 engines | Live `wking53214/EDDP` (identical bytes), reference-only there |
| Interlock wrapper | `sentinel_os/sage_k/gsa_adapter.py`; source in GSA-815 history |
| AST graph extractor | CLIP, STRIDE, and FACTS burials (identical bytes) |
| Synthesized and simple variants, predecessor paste, provenance, and transcript | Only in this burial (`snapshot/`) |

## What's here

- `snapshot/`: every tracked file at `94017cc`, exactly as it was (29 files: six recovered code files, the transcript source, provenance, evidence, manifests, diffs, and reports).
- `radar-full-history.bundle`: complete history (2 commits). The original RADAR commits are not recoverable.

## Known issues at time of burial

- It is a partial reconstruction. The provenance file was never recovered because the archive window falls in a gap across every record.
- Not the original repo. Commits `d5e52dd`, `681fed6`, `93cd72e`, and `e07c430` do not exist here.
- `eddp-pipeline-core-simple.py` and `eddp-wrapped-final.py` are single-line pastes. Nothing was reformatted.
- `eddp-wrapped-final.py` does not match its name. It is an AST graph extractor.
- The 2026-06-05 predecessor paste is the earliest EDDP source on record. Where it came from is unknown.
- The live EDDP repo was read but not changed. This burial does not affect it.

## Bringing it back

- Whole repo with history: `git clone radar-full-history.bundle radar`
- Files only: copy `snapshot/`.
