# Burial: content-pipeline, retired in full

**Repo:** `wking53214/content-pipeline` (formerly `wking53214/code`)
**Snapshot commit:** `03f282e` (main, 2026-10-07), the last live state
**Readable copy branch:** `unflatten-content-pipeline` at `12bba72`, included in the bundle
**Date:** 2026-10-07
**Decision:** William N. King

## Why

The repo held one pasted file: a 66 KB single-line flattening of an AI-generated
"content pipeline" design, mixing several unrelated versions. It does not run. About
40 names it uses are never defined in the file. Of those, 18 are defined elsewhere in
the stack (see the map in the branch's notes file), and 2 (`SystemStateV5`,
`ControlSystemV5`) are never defined anywhere the search reached. The stack already
does every job the file attempts, in better form.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Signing and payload verification | ztgkt `signing.py`, `pipeline.py` (real keys, typed results) |
| Ingestion validation and audit | sentinel_os `event_v1.py`, sage_k `kernel.py` (persisted, HMAC-signed audit) |
| Stop switch (killswitch) | sentinel_os `circuit_breaker.py` (blocks calls when open) |
| Text filters and sycophancy gate | ztgkt `filters.py`, http `zts.py` (G5 gate rejects rather than rewrites) |
| Graph extractor | sentinel_os `sage_k/graph_extractor.py` (call-chain fix on branch `fix/graph-call-chain-none`) |
| IVR routing and latent wait model | gsa-815 cassettes and `Latent/` |
| Missing-name map (18 of 20 found) | `unflatten-content-pipeline` branch, `content-pipeline-user-source.readable-NOTES.md` |
| Readable reconstruction, pasted-residue file | `unflatten-content-pipeline` branch (in the bundle) |
| Business strategy notes (extracted from the transcript) | `snapshot/business-strategy-notes.md` (this burial, verbatim) |

## What's here

- `snapshot/`: every tracked file at `03f282e`, exactly as it was, including the flattened source.
- `content-pipeline-full-history.bundle`: complete history of all branches (27 commits on main, plus the readable-copy branch).

## Known issues at time of burial

Recorded so a revival starts from the truth, not the design notes:

- **Cannot run.** About 40 names are used and not defined. Two are defined nowhere.
- **Original defects.** Two strings are broken across lines. Six function or class bodies are empty (comment-only or docstring-only). One import sits in the middle of the file, where Python does not allow it. Shell and pip commands were pasted into the code.
- **Audit trail records nothing.** The audit function is an empty stub.
- **Circular signature check.** It signs a payload, then verifies the signature it just made, so the check always passes.
- **Hard-coded signing key.** The source contains a key literal. Its value is not recorded here. Treat it as burned, and never reuse it.
- **Call-chain bug.** The graph extractor reported a fake call for chains like `f().g`. Fixed in sentinel_os, not here.

## Bringing it back

- Whole repo with history: `git clone content-pipeline-full-history.bundle content-pipeline` (then check out `unflatten-content-pipeline` for the readable copy).
- Files only: copy `snapshot/`.
