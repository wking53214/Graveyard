# Provenance

Where each part of this repository came from. Every claim below is tied to the
archive record that supports it. Claims that could not be corroborated are
marked as such rather than smoothed over.

## Subsystem B — kernel, adapter, extractor

**Origin:** a single Google Gemini chat, conducted in a Gemini notebook named
`SAGE-K (Streaming Adaptive Governance & Ensemble Kernel)`.

The chat's closing turn asked Gemini to scan the whole thread and synthesize the
most current refactored version of the code as one file. It produced a
consolidated module it labelled:

```
GSA UNIVERSAL CRYPTOGRAPHIC INTERLOCK WRAPPER ENGINE WITH INTEGRATED S.A.G.E.-K.
Version-Control-ID: [SHA256-PLACEHOLDER-V7.0.0-PROD-UNIFIED-INTERLOCK]
```

That module is preserved verbatim in `docs/GEMINI_SOURCE_RECORD.md`. It
describes itself as two layers — a governance wrapper enforcing SHA-256 chain
anchors and temporal handshakes, and a simulation kernel inside it modelling
queue dynamics through "Echo State Network" projections and "Lyapunov
Stability" metrics. The second description does not survive contact with the
code; see the note in `README.md`.

**Evidence:** Gemini Apps Activity record timestamped `2026-07-04T20:27:43.223Z`,
present in the account's Takeout export at
`Gemini_History/Takeout/My Activity/Gemini Apps/myactivity.json` (record index
219) and in the identical copy at
`Gemini_Extraction/source/raw/original_gemini_export.json`.

**Repository history:** the chat was exported using Gemini's full-transcript
download rather than re-prompted, and filed as the first of a planned pass over
unused Gemini-built projects. The initial commit contained five files: three
flattened code artifacts (`artifact_1.py`, `artifact_2.py`, `artifact_3.py`), a
`PROVENANCE.md`, and a 1,352-line verbatim `TRANSCRIPT.md`.

**None of the three artifacts executed.** `artifact_1.py` was pasted without
real line breaks. `artifact_2.py` does not parse at all — it has an odd number
of triple-quote docstring delimiters and raises `SyntaxError` on import, which
means the "Verification completed successfully" output claimed in the transcript
was never actually produced by running the code. `artifact_3.py` carried a
near-duplicate of `artifact_2.py`'s adapter with one behavioural divergence.

On 2026-08-14 a rebuild commit (`baf5ec8`, *"Rebuild as installable package; fix
adapter sync/async bug and chain-verification bug"*) deleted all three artifacts
and replaced them with the `sage_k` package. The two bugs it names are described
in `RECONSTRUCTION.md`.

## Subsystem A — interpretation

**Origin:** built 2026-08-06 as a standalone package named `interpretation`,
designed as the interpretation-drift layer for the Sentinel governance system.
Its `Resolver` protocol is the seam where Sentinel would be plugged in; no
Sentinel implementation is included here, and none ever was.

It was later merged into `sage_k/` as a second module cluster, and its facade
became the package's `__init__.py`.

**Evidence:** the module sources were recovered from the authoring conversation
in the Claude archive (`Claude_History`, conversation `39aecf97`, 2026-08-06).
Module line counts match the independent seam analysis of the original
repository exactly for `scenarios.py` (266), `drift.py` (303),
`realignment.py` (370), `report.py` (302) and `__init__.py` (90).

**Undocumented in the original.** The seam analysis in `docs/SEAM_INVENTORY.md`
recorded that the original repository contained no comment, doc, or commit
message explaining where this cluster came from or why it shipped alongside the
kernel. Its `PROVENANCE.md` described only the three broken artifacts and still
claimed "5 total files in this repo" after the package had been added. That gap
is the reason this file exists in its current form.

## Relationship between the two subsystems

They share nothing. Zero imports in either direction, zero shared symbols, zero
shared vocabulary. Nothing but the absence of an import edge holds them apart —
no packaging or namespace mechanism enforces it, and nothing would report a
future edge being added. This is catalogued as seam **S2**.

## Assessment on the record

On 2026-08-14, SAGE-K was evaluated against a minimum-substance rule for
archived Gemini transcripts — an archive counts only if it produced something
real, a working artifact or a documented design decision, rather than a
conversation that fizzled. Six candidates were checked. SAGE-K passed as the
strongest of the set: its three archived artifacts all failed to execute, but
the same-week rebuild was independently re-verified to import cleanly, produce
real example output, and pass its test suite.

## Reconstruction

The original repository is gone. This copy was rebuilt from the archives in
September 2026. `RECONSTRUCTION.md` documents the method, the verification, and
every known divergence from the original.
