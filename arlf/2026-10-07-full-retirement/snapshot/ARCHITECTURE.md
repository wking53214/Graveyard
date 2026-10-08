# REPOSITORY ARCHITECTURE

Immutable Gemini activity export → ARLF-bearing record set (46 records) → verbatim excerpts →
evidence ledger → entity, terminology, chronology and lineage datasets → reconstructed
specification → adversarial record → reports.

## Derivation chain

```
gemini_extraction:source/raw/original_gemini_export.json   (immutable, 4,911 records)
        │
        ├── grep ARLF (case-sensitive) ──► 46 unique activity records
        │
        ├── source/excerpts/RAW-*.txt          verbatim, grade A, 16 substantive records
        ├── evidence/evidence_ledger.jsonl     one row per ARLF-bearing record
        ├── evidence/source_records.jsonl      compact index with phase assignment
        │
        ├── entities/entities.jsonl            framework, components, review bodies
        ├── entities/terminology.jsonl         acronym expansions and coined terms
        ├── chronology/events.jsonl            21 dated lifecycle events
        ├── lineage/{nodes,edges}.jsonl        ancestry and succession graph
        │
        ├── spec/                              RECONSTRUCTION, canonical architectural reading
        ├── spec/variant/                      RECONSTRUCTION, the purged affective branch
        ├── adversarial/                       HISTORICAL_STATEMENT, largely verbatim
        └── reports/                           conclusions, graded

proposals/                                     NEW WORK -- derives from nothing above
        ├── RLCF_SPECIFICATION.md              PROPOSAL, no grade
        ├── AUTHORITY_GAP_RESOLUTION.md        PROPOSAL, no grade
        └── reference/                         runnable, 64 tests
```

## Layer rules

- **Source layer** is never edited. This repository holds no raw export; it points at the
  immutable copy in the Gemini extraction archive by record index.
- **Excerpt layer** is verbatim with whitespace normalization only. HTML entities present in the
  source (`&quot;`, `&amp;`, `&lt;`) are preserved as found inside code blocks.
- **Dataset layer** is derived mechanically and regenerable. Each file validates against its
  schema in `schemas/`.
- **Prose layer** (`spec/`, `adversarial/`, `reports/`) is human-readable synthesis. Every
  non-obvious statement carries an evidence ID. Where the layer states something the source does
  not, it says so explicitly.
- **Reading split.** `spec/` reconstructs the canonical architectural reading of ARLF; `spec/variant/`
  reconstructs the affective branch that was condemned and purged. The split is editorial and is argued
  in `NOMENCLATURE.md`. Both are held at the same evidence grade; neither is deleted in favor of the
  other.
- **Proposal layer.** `proposals/` sits outside the derivation chain entirely. It is original design
  work written after the archive, it carries `PROPOSAL` status and no evidence grade, and it never
  amends the reconstruction. Where a proposal addresses a recorded gap, the archive keeps recording the
  gap and adds a pointer. Nothing in `proposals/` may be cited as evidence about what ARLF was.

## Phase partition

The 46 records partition into seven phases, recorded in the `phase` field of every ledger row:

| Phase | Records | Window |
|---|---|---|
| `P1_GENESIS` | 3 | 2026-04-08 02:03 - 02:17 |
| `P2_SPECIFICATION` | 1 | 2026-04-08 02:35 |
| `P3_ADVERSARIAL_REVIEW` | 6 | 2026-04-08 03:13 - 04:00 |
| `P4_INCINERATION` | 4 | 2026-04-08 04:23 - 04:27 |
| `P5_MANIFEST_AUDIT` | 4 | 2026-04-11 |
| `P6_SECULARIZATION_PEAK` | 24 | 2026-04-14 - 2026-04-25 |
| `P7_RETROSPECTIVE` | 4 | 2026-05-29 - 2026-06-04 |

The specification phase contains exactly one record. The framework's entire canonical text was
produced in a single generation cycle, thirty-eight minutes before it went to review.
