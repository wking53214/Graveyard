# ANVIL

Single-file deterministic, hash-chained **governance kernel** (execution lineage, module registry, DAG, audit/telemetry). Header still reads `GSA Governance Adapter v2.1` — same code, pre-ANVIL name.

## 1. Pipeline Position & Role

**CUSTODY primitive / execution lineage.** Optional. **Not integrated** into any live orchestrator. Complements, and does not replace, a separate output-integrity ledger and a separate Postgres ledger service.

## 2. Full System Scope & Architectural Depth

`ANVIL.py` (~2716 lines) is the product: ten labeled sections (1A–10) sharing one import block.

- Immutable data handling, deterministic identifiers
- Canonical serialization + SHA-256 integrity signatures
- Envelopes, execution state, audit events
- Module registry + DI execution runtime
- DAG lineage + named integrity checkpoints
- Audit ledger, telemetry, event bus, health
- `GsaKernel` entry point

v2.1 vs v2.0: collapsed duplicate `__future__` imports (v2.0 **could not compile**), fixed `ConfigurationException.code` swallowed by an unclosed docstring, Black format. Fail-closed execution is **opt-in**.

`anvil_validation_harness.py` exercises behavior. Importing `ANVIL.py` produces no output.

## 3. What It Does NOT Do / Non-Goals

- Not the live orchestrator or Postgres custody.
- Does not issue human authorization.
- Does not replace other governance components (different question: lineage vs epistemic conservation).
- Not a multi-file package. No `src/` layout.

## 4. Brutally Honest Current Status & Gaps

| Gap | Detail |
|---|---|
| Not wired | The live orchestrator does not import ANVIL. Dual custody with the orchestrator's own ledger and the Postgres ledger service. |
| Single file | 2.7k-line God object. Testable via harness, hostile to incremental review. |
| Opt-in fail-closed | Default is not "refuse undeclared execution". |
| No KMS | SHA-256 integrity, not authenticity. |
| Name collisions | `GsaUniversalAdapter` appears in multiple historical repos. This file is not what they import. |

CI: `.github/workflows/tests.yml`. Stdlib. Python 3.11+.

## 5. Core Invariants & Guarantees

Deterministic records; hash-chained lineage; tamper-evident *if* you recompute; inspectable history. No authenticity, no durable multi-process consensus.

## 6. Inputs, Outputs & Type Contracts

`GsaKernel.execute(...)` over registered modules. Envelope + execution-state dataclasses inside `ANVIL.py`. Canonical serialization before SHA-256.

## 7. Stack Integration Topology

```text
orchestrator execution ledger     ← LIVE (JSONL)
Postgres ledger service           ← LIVE (when infra up)
ANVIL GsaKernel                   ← NOT IMPORTED
output-text hash-chain ledger     ← output-text seal, different layer
```

Apache-2.0.
