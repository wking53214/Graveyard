# Provenance

## Source

- Source file: `Citadel_02.txt`, provided by the user from their local `Downloads` folder.
- Producing AI tool: the transcript's first line states a Google Gemini URL — `https://gemini.google.com/app/bdfb714c5ff685ed` — under the heading "Citadel LLM Enforcement Engine Audit." No specific Gemini model version/name is stated anywhere in the transcript body.
- Origin date: **recoverable, in part.** The AI's response opens with a literal date/time stamp, `2026-06-18 4:15pm`, as the first line after the `Response:` label. This is taken exactly as it appears in the source and is not independently verified.
- This repo was created on 2026-08-13 from a pre-existing artifact. Git history reflects the archival date, not the artifact's development history. No development chronology is available.

## What the transcript contains

This is a single-turn conversation. The user pastes a Python module — `CITADEL v1.1`, described in its own header comment as a "Deterministic LLM Output Enforcement Engine" (regex-based detection of first-person pronouns, hedging language, passive voice, and em-dashes, with a scoring/rewriting pipeline) — and the AI's reply is a structured "🛡️ Systemic Analysis" audit of the code, in prose only, with no new code produced.

Notably, the user's single pasted block actually contains **two versions of the same module concatenated back to back** — the AI's own response explicitly remarks on this: "wam: Audit of CITADEL v1.1 Deterministic LLM Output Enforcement Engine initiated. Duplicated code block detected and consolidated." The two copies are similar but **not identical** (different internal variable names — e.g. `_fix_passive` vs. `_simplify_passive`, `PENALTY` vs. `PENALTIES`, `k, v` vs. `word, replacement` — and slightly different code structure in a few places, such as how `causality` gating is nested). Both copies were preserved together as they were pasted, in a single file, rather than being split apart — see "Extraction: what was stripped" and "Duplication" below.

| File | Turn | Source | Contents |
|---|---|---|---|
| `artifact_1.py` | 1 (prompt) | User-pasted | The full pasted content: two similar-but-not-identical implementations of the `CITADEL v1.1` enforcement engine (`REGEX`, `PROFILES`, `Constraint`, `CitadelDetector`, `CitadelTransformer`, `CitadelScorer`, `Citadel`), concatenated in the order pasted. |

The AI's response contains no code and was not extracted as a separate artifact; it is preserved in full inside `TRANSCRIPT.md`.

`artifact_1.py` does not state its own filename inside its own text (only a version/system header comment, `# CITADEL v1.1`), so it is named per the fallback rule.

**Note on scope:** a second, related file (`CITADEL-01.txt`) exists in the user's `Downloads` folder and was intended, per the user's request, to share this repository ("the house repo for the two files"). At the user's explicit direction, given the sensitive personal nature of that second transcript's content, it was **not** included in this archive. This repository currently contains only `Citadel_02.txt`.

## Whether the artifact executes

`artifact_1.py` was run once, unmodified, with `python3` (system interpreter). It does not run: `SyntaxError: invalid syntax`. Like the raw code pastes seen in the user's other archived transcripts, the entire file has no internal line breaks — it is a single unbroken line of text, spanning both concatenated copies of the module.

## Line and file counts

- `artifact_1.py`: 0 lines (no newline characters), 15,933 characters.
- `TRANSCRIPT.md`: 19 lines (identical line count to the source `.txt` file).
- At original archival this repo held 3 files (`artifact_1.py`,
  `TRANSCRIPT.md`, `PROVENANCE.md`). See "Later additions" below for the
  files added afterward.

## Later additions (post-archival, 2026-08-21)

Three readable files were added after the archive was created. They do not
change the archival record above; `artifact_1.py` remains the canonical
flattened copy.

- `citadel_v1.1_copy1.py`, `citadel_v1.1_copy2.py` — the two concatenated
  drafts inside `artifact_1.py`, split apart and given conventional line
  breaks/indentation, unedited otherwise. `copy1` runs; `copy2` imports but
  its `__main__` demo raises `TypeError` in `re.sub` — a defect present in
  the flattened original, deliberately not fixed.
- `citadel_v1.2.py` — v1.1 with one additional constraint (`prohibited_verbs`)
  salvaged from the now-deleted STRIDE repository. Runs.
- `README.md` and `LICENSE` (Apache-2.0) were also added.

## Tests

No tests exist. The source transcript contains no test files, no test framework references, and no `assert`-based test code — only an `if __name__ == "__main__":` demonstration block (present, in slightly different form, in each of the two concatenated copies within `artifact_1.py`).

## Extraction: what was stripped

Only transport-layer wrapper text was removed; the code itself was copied byte-for-byte from the source `.txt` file (verified against exact character offsets, preserving original CRLF line endings):

- The literal labels `User prompt:` and `Response:` (including the `2026-06-18 4:15pm` date/time line that follows `Response:`) that the transcript export prepends to the turn.
- No markdown code fences (```` ``` ````) were present in the source file — there was nothing of that kind to strip.
- The AI's "🛡️ Systemic Analysis" response (a prose audit, not code) was not extracted; it is preserved in full inside `TRANSCRIPT.md`.
- Nothing was stripped from the `.txt` file to build `TRANSCRIPT.md` — that file is the complete source document, copied verbatim, unmodified.

## Duplication

The user's single prompt contains two concatenated implementations of the same module, both preserved as instructed: the two copies were **compared and found not to be identical** (different lengths — 7,880 vs. 8,035 characters — and different internal naming/structure in several places, listed in "What the transcript contains" above). Per the rule to keep differing copies rather than choosing between them, both were kept together in `artifact_1.py`, exactly as the user pasted them, rather than being split into two separate files or having one discarded.

## Things noticed but not fixed

- `artifact_1.py` has no recoverable line/indentation structure in the source transcript; it was left as a single flattened line (containing both concatenated copies) rather than being reformatted into conventionally indented Python.
- The two concatenated copies were not merged, reconciled, or deduplicated into a single canonical version, even though they implement near-identical logic. Both are preserved exactly as pasted.
