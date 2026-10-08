# ⚠ THIS IS A RECONSTRUCTION — NOT THE ORIGINAL FACTS REPOSITORY

Pushed 2026-09-17.

## What this is

A forensic reconstruction of the deleted `wking53214/FACTS` repository. The
original's commits — `e40f60d`, `edcb397`, and two more — do **not** exist here.
The repo now at this name was created 2026-09-17T11:44:33Z and was empty until
this push; it reuses the name only.

## What FACTS actually was

An archived Gemini transcript (`https://gemini.google.com/app/d23849459aff7505`),
titled **"FACTS (Forensic Audit & Clinical Transformation System) Deterministic
Kernl"** — the typo is in the source and is preserved.

The code inside does not call itself FACTS. It calls itself **GRAPH —
Governance, Routing, and Anchor Processing Hierarchy** — across 14 artifacts
spanning versions v2.1 to v2.3, implementing (per the rename commit's own words)
"rotational temporal interlock and SHA-256 historical data integrity".

This repo-name / system-name mismatch is the same pattern seen in CLIP→STRIDE
and RADAR→EDDP. Recorded, not reconciled.

## Recovery: 16 of 17 entries

All 14 code artifacts recovered, each confirmed as an **exact byte substring of
the source transcript**. Twelve also came from an independent git blob
(`GRAPH@e1bd68e`), giving two agreeing paths; the remaining two exist in **no
local git history at all** and were recoverable only from the transcript.

| was | renamed to | bytes | CRLF lines | parses | source |
|---|---|---:|---:|:--:|---|
| artifact_1 | `graph-v2.1-flattened-base.py` | 3,273 | 0 | YES | git blob + transcript |
| artifact_2 | `graph-v2.1-indexed-audited.py` | 5,878 | 123 | NO | git blob + transcript |
| artifact_3 | `graph-v2.3-dual-extract-combined.py` | 5,569 | 0 | YES | git blob + transcript |
| artifact_4 | `graph-v2.3-indexed-driver.py` | 7,972 | 159 | NO | git blob + transcript |
| artifact_5 | `graph-v2.3-driver-enabled.py` | 3,284 | 0 | NO | git blob + transcript |
| artifact_6 | `graph-v2.1-user-ai-modules.py` | 4,974 | 113 | YES | git blob + transcript |
| artifact_7 | `graph-v2.3-extraction-logic.py` | 4,837 | 95 | NO | git blob + transcript |
| artifact_8 | `graph-v2.3-synthesis-payload.py` | 5,377 | 0 | NO | git blob + transcript |
| artifact_9 | `graph-adapter-hooks.py` | 711 | 22 | YES | git blob + transcript |
| artifact_10 | `graph-cryptographic-engine.py` | 7,089 | 137 | NO | git blob + transcript |
| artifact_11 | `graph-context-envelope.py` | 6,948 | 0 | YES | git blob + transcript |
| artifact_12 | `graph-module-registry.py` | 7,276 | 145 | NO | git blob + transcript |
| artifact_13 | `graph-state-integrity.py` | 5,376 | 0 | NO | **transcript only** |
| artifact_14 | `graph-universal-wrapper-final.py` | 9,930 | 215 | NO | **transcript only** |

**Not recovered: `PROVENANCE.md`.** It existed in the 2026-08-17 `/tmp/FACTS`
listing, but no surviving session ever opened it. Unlike the STRIDE
reconstruction, there is therefore **no stated line/character/behaviour table to
validate against** — validation here rests on git blobs and transcript
containment instead.

## What the parse results actually show

Nine of fourteen do not parse, and the reason is not uniform:

- **3 are flattened single-line pastes** (0 line breaks) — `artifact_5`,
  `artifact_8`, `artifact_13`.
- **6 have real line structure and still fail** — `artifact_2`, `artifact_4`,
  `artifact_7`, `artifact_10`, `artifact_12`, `artifact_14`. These were broken
  **as transcribed**, not merely flattened.
- 5 parse cleanly, 3 of which are flattened but still valid.

Nothing was reformatted, corrected or completed. The breakage is the evidence.

## A file that appears in three separate repositories

`artifact_13` (`graph-state-integrity.py`) is **byte-identical** to
`artifact_5` of CLIP/STRIDE and `artifact_5` of RADAR:

```
sha256 a7026823c9a985cb7ff3d90a24a832fbc51cfb3ff2c922d61c52296808dbaa04
5,376 bytes, 0 line breaks
```

The same flattened "Deterministic AST-based graph extractor", pasted as a late
turn into **three separate Gemini conversations**. Its FACTS name
(`graph-state-integrity.py`) does not describe it, exactly as its RADAR name
(`eddp-wrapped-final.py`) did not.

No ancestry or direction of copying is asserted — only that the same bytes
appear in all three.

## Layout

```
recovered_repo/   the 14 artifacts + transcript source
evidence/         Copilot session payloads: the /tmp/FACTS listing, the rename
manifests/        repository_tree.txt, file_manifest.json (SHA-256 for every entry)
```
