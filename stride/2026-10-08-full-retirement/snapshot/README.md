# ⚠ THIS IS A RECONSTRUCTION — NOT THE ORIGINAL STRIDE REPOSITORY

Pushed 2026-09-17. Read this before treating anything here as original history.

## What this repository is

A forensic reconstruction of the **deleted** `wking53214/STRIDE` repository,
assembled from local evidence on 2026-09-17.

## What it is not

- **It is not the original repository.** The original was deleted from GitHub on
  2026-08-20. Its four commits — `919a740`, `56dd695`, `a9aef1b`, and a fourth
  whose hash is UNKNOWN — do **not** exist here. This repo's history begins with
  the reconstruction commit.
- **This GitHub repository is not the original one either.** The repo now at
  `github.com/wking53214/STRIDE` was created **2026-09-11T23:13:56Z**, weeks
  after the original was deleted, and was empty until this push. It reuses the
  name only.
- The original repository was itself **renamed from CLIP**. The original
  `github.com/wking53214/CLIP` was deleted along with it. A repo at that name
  now exists again, created 2026-09-17 to hold the same reconstruction — it is
  not the original either, and its content is merged into this repository (see
  below).

## Both states of the repository are here

This repository was named **CLIP** before it was renamed to **STRIDE** — one
repository, two names, not a lineage. Both states are preserved:

- `recovered_repo/` — the later state, files named `stride-*` / `clip-original-*`
- `recovered_repo_clip_state_919a740/` — the earlier state, files named
  `artifact_1.py` … `artifact_6.py`

**The two sets are byte-identical**; only the filenames differ. See
`CLIP_STATE_MAPPING.md` for the pair-by-pair SHA-256 proof and why the earlier
state is kept separately (it is the only state in which `PROVENANCE.md` and the
filenames agree, and it is the more completely recovered of the two — 8 of 8
entries against 6 of 7).

## What was actually recovered

All six code artifacts, **byte-exact**, validated three independent ways against
the repository's own `PROVENANCE.md`:

| file (as renamed) | was | bytes | PROVENANCE | lines | PROVENANCE | behaviour |
|---|---|---:|---:|---:|---:|---|
| `clip-original-multi-module-source.py` | artifact_1 | 117,211 | 117,211 | 0 | 0 | SyntaxError ✓ |
| `stride-synthesized-unified.py` | artifact_2 | 25,106 | 25,106 | 705 | 705 | runs, output ✓ |
| `stride-formatted-audited.py` | artifact_3 | 31,970 | 31,970 | 746 | 746 | runs, output ✓ |
| `stride-wrapped-final.py` | artifact_4 | 6,994 | 6,994 | 151 | 151 | no output ✓ |
| `ast-graph-extractor-source.py` | artifact_5 | 5,376 | 5,376 | 0 | 0 | SyntaxError ✓ |
| `stride-ast-extractor-wrapped.py` | artifact_6 | 6,579 | 6,579 | 187 | 187 | no output ✓ |

**6/6 on bytes, 6/6 on lines, 6/6 on execution behaviour.**

Also recovered: `PROVENANCE.md` (81 of 82 lines, from a viewer render captured
before the rename), and `TRANSCRIPT.md` via its verbatim source — 1,894 CRLF
lines, exactly the count PROVENANCE.md states.

**Not recovered: `README.md`.** It was added in the fourth commit
(2026-08-19 04:59:31 -0400), after every surviving observation of the repository.
The file you are reading now is a reconstruction notice written in 2026-09-17,
**not** that README.

**Of the 7 archived entries: 6 recovered, 1 unrecovered.**
Verdict: **FULL RECONSTRUCTION SUPPORTED BY EVIDENCE for the six code artifacts,
PROVENANCE.md and TRANSCRIPT.md; PARTIAL at the repository level.**

## Preserved as-found, deliberately

- `artifact_1` and `artifact_5` are **flattened single-line pastes** with zero
  line breaks and do not parse. Not reformatted.
- `stride-ast-extractor-wrapped.py` carries a `SYSTEM_NAME: STRIDE` header that a
  2026-08-19 session determined was **applied in error**. Preserved as found.
- The `_v1` suffix on `GSA_Universal_Interlock_Wrapper_v1.py` (in the wider
  ecosystem) is misleading — it post-dates a `-v7` file. Noted, not corrected.
- CRLF line endings are preserved.
- `evidence/superseded_variants/` holds a Gemini-export variant of
  `artifact_3` that differs from the committed file only in indentation. It is
  **not** the repository file; kept because discarding a conflicting source would
  destroy evidence.

## Salvage chain

`stride-formatted-audited.py` → a salvage extract (2026-08-20, two components) →
`sentinel_os/governance_loop_guard.py` (2026-08-21, one component). The Sentinel
copy is **not** byte-identical to the salvage. The salvage claims its components
are "verbatim from the original"; compared against the recovered committed file
they are not — an unresolved conflict documented in the report.

## Layout

```
recovered_repo/                       the later state: stride-* / clip-original-* names
recovered_repo_clip_state_919a740/    the earlier CLIP state: artifact_1-6.py
CLIP_STATE_MAPPING.md                 SHA-256 proof that the two are the same bytes
evidence/         extracted code blocks, session payloads, superseded variants
manifests/        repository_tree.txt (+ _clip_state), file_manifest.json (+ _clip_state),
                  carve_validation.json
provenance/       STRIDE_PROVENANCE.md — full chain including the CLIP rename
reports/          STRIDE_RECOVERY_REPORT.md (with second-pass addendum),
                  STRIDE_CODE_INVENTORY.md
diffs/            variant and salvage diffs
```

Every recovered file carries a SHA-256 in `manifests/file_manifest.json`.
Nothing in `recovered_repo/` was written, reformatted, corrected or completed.
