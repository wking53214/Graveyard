# innovation_os

Governed **innovation workflow OS** (capture → connect → evaluate → review → approve). Sample application for "AI proposes / systems evaluate / humans authorize." **Not required** on the observe-perceive gate.

## 1. Pipeline Position & Role

**SPECIALIZED INLET / DOMAIN WORKFLOW.** Optional adapter `innovation_governance_adapter.py` in observe-perceive (skip if absent). Commercial: **PRODUCT in a crowded category** (Jira/Productboard/Aha) with **no evidence of differentiation**.

## 2. Full System Scope & Architectural Depth

606 files, **524 `.py`**, `dependencies = []`. What actually executes:

```python
# src/innovation_os/core/pipeline.py
aligned = alignment_score >= 70   # hardcoded, caller-supplied
reviewed = review_complete        # caller boolean
approved = approved               # caller boolean
```

`demos/run_innovation_demo.py` / `run_mvp.sh` print strings back. **No ideation model, no LLM, no evaluator.**

"Intelligence v2": 160 modules under `intelligence/`. `CognitiveKernel` is a registry + `engine.process(payload)` router. Invariants check non-empty ids and SUPERSEDED vs current. Optional SQLite `nodes/relationships`. Living-brain `memory/` is YAML; CODEX: **no runtime query engine**. Duplicate trees (`decision/` vs `decisions/`). Empty root docs: `BRANCHING_MODEL.md`, `CODE_REGISTRY.md`, etc.

## 3. What It Does NOT Do / Non-Goals

Does not generate ideas, call a model, persist a governed decision to sentinel_os, or enforce authorization beyond caller booleans.

## 4. Brutally Honest Current Status & Gaps

Module count ≠ capability. Tests (164 files / ~285 claimed) largely exercise dataclasses in isolation. Fingerprint cards are portfolio census, not runtime. Adapter in the hub is optional theater until this pipeline does work.

## 5. Core Invariants & Guarantees

InvariantEngine records violations in a list (bool + append) — **no SHA chain**. Fail-closed is not the architecture here.

## 6. Inputs, Outputs & Type Contracts

`InnovationPipeline.run(..., alignment_score, review_complete, nature_patterns, solution_id, approved) -> InnovationPipelineResult`.

## 7. Stack Integration Topology

```text
observe-perceive innovation_governance_adapter (opt, skip-if-absent)
sentinel_os ✗   α-ζ-β-δ ✗
```

Apache-2.0.
