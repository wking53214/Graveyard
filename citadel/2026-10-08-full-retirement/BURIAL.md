# Burial: CITADEL, retired in full

**Repo:** `wking53214/citadel` (its live README now says retired)
**Snapshot commit:** `d5f67a2` (main), the last live state before retirement
**Date:** 2026-10-08
**Decision:** William N. King

## Why

CITADEL is a regex-based enforcement script for LLM output (first-person pronouns, hedging, passive voice, causal claims, em dashes), kept as a transcript plus three versions of its code. Its working rules now live in ZTS, which runs them with tests, profiles, and a scoring system. Before burial, every idea was checked against the whole stack. Two ideas were not already running in ZTS, and both were ported as review flags. The rest was either covered or wrong to port.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Outcome words with no stated cause | ZTS `src/zts/causality.py` (flag only), PR #10 |
| Passive voice | ZTS `src/zts/passive.py` (flag only, ops/exec/legal), PR #11 |
| First-person pronouns | ZTS gate PPA (same pattern) |
| Hedging words | ZTS gate SBF (superset of CITADEL's list) |
| Em dash to en dash | ZTS punctuation rule (same behavior) |
| Profiles (default, ops, exec, legal) | ZTS `src/zts/profiles.py` |
| Scoring (100 minus penalties) | ZTS `sieve.py` scoring, own weights |
| Verb normalization | ZTS `normalizer.py` (utilize to use, leverage to apply) |

## Not ported, on purpose

- **Causality rewrite** that appends "due to measurable operational impact." It invents a cause. Do not reuse it.
- **Passive rewrite**: three hard-coded phrase swaps. Brittle and can change meaning.
- **Prohibited verbs rewrite** (v1.2): replaces improve, optimize, enhance, enable, support, and strengthen with "use." "Improve performance" becomes "use performance."
- **Transformer's second regex pass**, duplicate copies, and the Gemini audit's performance notes.

## What's here

- `snapshot/`: every tracked file at `d5f67a2`, exactly as it was (11 files).
- `citadel-full-history.bundle`: complete history (11 commits on main).

## Copies that remain elsewhere in the stack

This burial covers the CITADEL repo only. The same lineage exists in other live or archived repos, and those were NOT buried by this action:

- `ecology/corpus`: about eight CITADEL-named files (a governance engine with telemetry and correction routing, a security core, a router, and others). Not reviewed in depth.
- `TOUCHSTONE/specimens`: archived copies of citadel v1.2, including the fabricated-causality line.
- `DIT/legacy`: `gsa_v13_citadel_processor.py` (the CLIP / CitadelProcessor engine).
- `GSA/archive`: CITADEL Diamond references and the CITADEL_COLLAPSE test strings.
- "Citadel" is also a live intent-check gate name in PERCEIVE and observe-perceive. That is a different component and is not affected.

## Known issues at time of burial

- `artifact_1.py` does not run (`SyntaxError`): it is the flattened paste with both copies on one line.
- `citadel_v1.1_copy2.py` imports, but its demo raises a `TypeError` in `re.sub`. Left unfixed on purpose.
- No tests exist.
- The Gemini transcript's date (2026-06-18) is taken from the source and was not verified.
- The repo's own README and STACK.md still describe it as the "governed-action" stack role. That text is historical.

## Bringing it back

- Whole repo with history: `git clone citadel-full-history.bundle citadel`
- Files only: copy `snapshot/`.
