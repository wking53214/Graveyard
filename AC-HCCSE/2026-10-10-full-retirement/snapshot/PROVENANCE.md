# Provenance

## Origin

AC-HCCSE was built in a Google Gemini notebook named
`AC-HCCSE (Anti-Cog / Human-Centered Customer Service Engine)`.

The engine itself comes from a single activity record timestamped
`2026-06-22T00:25:59.887Z`, in which Gemini was asked to add a name and
description to the core of the code and reproduce it. That record contains a
complete, coherent, 187-line Python module — the classes this package is built
from, with the same scoring model, the same category boundaries, and the same
0.3/0.7 allocation weights.

**Recovered from:** `Gemini_History/Takeout/My Activity/Gemini Apps/myactivity.json`
(record index 913), and the identical copy in
`Gemini_Extraction/source/raw/original_gemini_export.json`.

## The neutral vocabulary was deliberate

An adjacent record (`2026-06-22T00:12:39.292Z`) captures a refactoring pass
whose Phase 2 required "strict variable neutrality" — identifiers carrying
"non-descriptive terms, domain-specific stylistic naming conventions, or
conceptual branding" were to be rewritten as objective functional terms.

That is why the categories are ALPHA/BETA/GAMMA rather than something
evaluative, and it is why this reconstruction kept them. The neutrality is a
design position, not an accident of generation.

The two records are byte-identical apart from the name-and-description header,
so the June 22 pair represents one settled artifact rather than two drafts.

## What is not from that record

Three other activity records carry the AC-HCCSE notebook tag but are not this
engine:

- `2026-07-04T20:39:22.644Z` — the generic "GSA Universal Cryptographic
  Interlock Wrapper", the same template applied across many unrelated
  codebases in that period. It contains no AC-HCCSE domain logic.
- `2026-07-06T23:13:57.176Z` — an AST graph extractor with colour/animation
  hooks. Unrelated.
- `2026-06-22T03:45:52.680Z` — a refusal, answering a question about whether
  the code was a kernel. No artifact.

None of the three contributed anything to this package.

## Repository history

The original `wking53214/AC-HCCSE` repository held the engine alongside flat
artifact files archived straight from the transcript. An August 2026
inclusion-floor assessment ran them and found three of nine executed.

That repository no longer exists. The GitHub repo of that name is empty, and
its artifacts, provenance notes and transcript are gone. This is a September
2026 reconstruction built from the archive, not a recovery of those files.

## Status in the research corpus

AC-HCCSE previously sat in the cross-tool Gemini arm of an architecture study.
Following the data loss it has been removed from that study set: a
reconstruction cannot carry the evidentiary weight the original artifact would
have, and the corpus has sufficient primary systems without it. This repository
exists to be useful software, and is documented as such.
