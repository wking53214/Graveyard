# Source Provenance

This repository contains **no raw source data**. The raw export is immutable and lives in the Gemini
archive. Everything here points at it by record index.

## Authoritative source

| | |
|---|---|
| Repository | `wking53214/Gemini_Extraction` |
| File | `source/raw/original_gemini_export.json` |
| Records | 4,911 activity records |
| Normalized projection | `gemini_extraction:source/normalized/messages.jsonl` |
| Status | Immutable |

Identical content also appears in `wking53214/Gemini_History` at
`Takeout/My Activity/Gemini Apps/myactivity.json`. Case-sensitive `ARLF` occurrence counts match
between the two files, so they are treated as one source.

## Addressing

Evidence IDs are `ARLF-NNNNN`, where `NNNNN` is the zero-padded `message_index` / `record_index` in
the export. To resolve `ARLF-03342`:

```
gemini_extraction:source/raw/original_gemini_export.json[3342]
gemini_extraction:source/normalized/messages.jsonl#message_index=3342
```

## Coverage

| | Count |
|---|---|
| ARLF-bearing unique activity records | 46 |
| Records with verbatim excerpts here | 16 |
| Raw `ARLF` occurrences, Gemini_Extraction | 423 |
| Raw `ARLF` occurrences, Gemini_History | 111 |
| Raw `ARLF` occurrences, ChatGPT / Claude / Copilot archives | 0 |

The raw occurrence count exceeds the record count because the extraction repository's derived ledgers
(evidence, provenance, chronology, VSA investigation) each carry copies of the same records.

## Excerpts

`source/excerpts/RAW-NNNNN.txt` holds the 16 substantive records verbatim, with whitespace normalized
and nothing else altered. HTML entities present in the source (`&quot;`, `&amp;`, `&lt;`) are preserved
as found, particularly inside code blocks. Each file carries a header with its evidence ID, record
index, timestamp, source location, grade and provenance status.

| Excerpt | Subject |
|---|---|
| `RAW-03350` | Naming collision - the packaging-industry reading |
| `RAW-03349` | Scope correction; ARLF, the Jester and RLCF named |
| `RAW-03342` | *Birth and Structure of ARLF* - the canonical specification |
| `RAW-03333` | Six-domain adversarial review |
| `RAW-03332` | Burn-down and the four Hard Gates |
| `RAW-03331` | Bias audit |
| `RAW-03330` | Scope verification |
| `RAW-03329` | Full-architecture exposure |
| `RAW-03327` | Structural Diamonds |
| `RAW-03325` | External Council registry and Glass Wall Protocol |
| `RAW-03324` | The Black Paper |
| `RAW-03323` | Black Paper, code-box reissue |
| `RAW-03322` | Black Paper archival disposition |
| `RAW-02105` | Nomenclature freeze; permanent designations |
| `RAW-02104` | **Peak** - authoritative GSA terminology |
| `RAW-01575` | White Paper v1.0 summary; 7-Layer stack and Ghost Problems |

The remaining 30 records are indexed in `evidence/evidence_ledger.jsonl` and
`evidence/source_records.jsonl` without excerpts; they are passing references rather than substantive
ARLF content.

## Regenerating the datasets

Every JSONL file in `evidence/`, `entities/`, `chronology/` and `lineage/` derives mechanically from
the source by case-sensitive `ARLF` search, deduplication on `message_index`, and phase assignment by
timestamp. Each validates against its schema in `schemas/`.
