# CITADEL

Archived **single-turn AI transcript** plus recovered `CITADEL v1.1` deterministic LLM-output enforcement engine (regex: first-person, hedging, passive, em-dashes, scoring/rewrite). Successor concept: [`DIT`](https://github.com/wking53214/DIT). **Not the live path.**

## 1. Pipeline Position & Role

**HISTORICAL / LINGUISTIC SPECIMEN.** Parallel ancestor of DIT "linguistic interceptors". STRIDE consumed this and was **deleted**; v1.2 salvages `prohibited_verbs` from it.

## 2. Full System Scope & Architectural Depth

| File | What | Runs? |
|---|---|---|
| `artifact_1.py` | Concatenated paste, one flattened line | No (`SyntaxError`) |
| `artifact_1.recovered.py` | Same SHA | No |
| `citadel_v1.1_copy1.py` | Readable first draft | Yes |
| `citadel_v1.1_copy2.py` | Second draft | Import ok; `__main__` `TypeError` in `re.sub` (left unfixed) |
| `citadel_v1.2.py` | + `prohibited_verbs` (`improve|optimize|enhance|…`) on `ops`/`exec` | Yes |

`CitadelDetector` / `CitadelTransformer` / `CitadelScorer` / `Citadel`. Profiles `default|ops|exec|legal`. No tests. Stdlib `re`.

## 3. What It Does NOT Do / Non-Goals

Governance, provenance, execution control, fail-closed decisions. First-person pronouns are not a governance kernel.

## 4. Brutally Honest Current Status & Gaps

No hash, no halt, no package. Transcript in `TRANSCRIPT.md`. Kept as a general-purpose archive (unlike VANGUARD, which folded into TOUCHSTONE).

## 5. Core Invariants & Guarantees

None at the custody layer. Style gate only.

## 6. Inputs, Outputs & Type Contracts

`Constraint` enum; `PROFILES` booleans; rewrite string out.

## 7. Stack Integration Topology

```text
CITADEL regex  →  DIT tower (live output integrity)
STRIDE (deleted) consumed v1.1
observe-perceive ✗
```

**Safe to archive** as specimens; DIT is the living descendant.

Apache-2.0.
