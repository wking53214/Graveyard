# ⚠ THIS IS A RECONSTRUCTION — NOT THE ORIGINAL RADAR REPOSITORY

Pushed 2026-09-17. Read this before treating anything here as original history.

## What this repository is

A forensic reconstruction of the **deleted** `wking53214/RADAR` repository,
assembled from local evidence on 2026-09-17.

## What it is not

- **It is not the original repository.** The original was deleted. Its four
  commits — `d5e52dd`, `681fed6`, `93cd72e`, `e07c430` — do **not** exist here.
  The commit history in this repo begins with the reconstruction commit and is
  authored by the reconstruction process, not by the original work.
- **This GitHub repository is not the original one either.** The repo now at
  `github.com/wking53214/RADAR` was created **2026-09-11T23:22:49Z**, weeks after
  the original was deleted, and was empty until this push. It reuses the name
  only.

## What was actually recovered

Six code artifacts, **byte-exact**, each confirmed by two independent paths — a
git blob from the repository the content was moved into, and an exact
byte-substring match inside the archived source transcript.

| file (as renamed by `681fed6`) | was | bytes | git blob | offset in RADAR.txt |
|---|---|---:|---|---:|
| `eddp-pipeline-core-simple.py` | artifact_1 | 1,174 | `a8ad5a7f…` | 149 |
| `eddp-core-engine-v1.py` | artifact_2 | 10,662 | `22f07960…` | 2,927 |
| `eddp-core-engine-v2-refined.py` | artifact_3 | 14,576 | `b03f0250…` | 19,213 |
| `eddp-comprehensive-synthesized.py` | artifact_4 | 14,751 | `e1573491…` | 34,293 |
| `eddp-wrapped-final.py` | artifact_5 | 5,376 | `4a68b434…` | 90,849 |
| `gsa_universal_interlock_wrapper.py` | (not renamed) | 18,179 | GSA-815 `f0b70d6` | 72,631 |

Plus `TRANSCRIPT.md.SOURCE_RADAR_TXT` — the verbatim source transcript, which
contains all six artifacts as exact byte substrings.

**Not recovered: `PROVENANCE.md`.** It existed, but the archival window
(2026-08-13, 10:58→11:32 -0400) falls in a simultaneous coverage gap across every
available record. Marked `FILE EXISTENCE VERIFIED — RAW SOURCE NOT RECOVERED`.

**Of the 8 archived entries: 6 byte-exact, 1 as verbatim source, 1 unrecovered.**
Verdict: **PARTIAL RECONSTRUCTION — MISSING EVIDENCE REMAINS.**

## Two findings that correct the obvious reading

**The system was EDDP before it was RADAR.** "RADAR" was one of three acronyms
(RADAR / DEFT / APEX) proposed 2026-06-22T02:01:30Z and chosen by the account
holder. The repo inherited it from the transcript title; the 2026-08-17 rename
pushed the files back toward EDDP. You can see it in the code — `EDDPSystem`
becomes `RADARSystem`.

**The code predates the RADAR conversation by 17 days.** The earliest EDDP source
in the record is a ChatGPT paste dated 2026-06-05T00:08:29Z, preserved here at
`evidence/predecessors/`. It shares 13 of 14 classes with `artifact_2.py`. Where
*it* came from is UNKNOWN — it was itself a paste, with nothing earlier in any
available corpus. **The archival commit is not the origin.**

## Preserved as-found, deliberately

- `eddp-pipeline-core-simple.py` and `eddp-wrapped-final.py` are **flattened
  single-line pastes** with zero line breaks. Not reformatted.
- `eddp-wrapped-final.py` **does not match its name** — it is an AST graph
  extractor, and is byte-identical (sha256 `a7026823…`) to an artifact in the
  CLIP/STRIDE archive. No ancestry or direction of copying is claimed; only that
  the same bytes appear in both places.
- CRLF line endings are preserved.

## Layout

```
recovered_repo/   the six artifacts + transcript source
evidence/         extracted session payloads; predecessors/ holds the 2026-06-05 version
manifests/        repository_tree.txt, file_manifest.json, carve_validation.json
provenance/       RADAR_PROVENANCE.md — full chain, with the origin-scour addendum
reports/          RADAR_RECOVERY_REPORT.md, RADAR_CODE_INVENTORY.md
diffs/            version diffs + the cross-repo hash note
```

Every recovered file carries a SHA-256 in `manifests/file_manifest.json`.
Nothing in `recovered_repo/` was written, reformatted, corrected or completed.
