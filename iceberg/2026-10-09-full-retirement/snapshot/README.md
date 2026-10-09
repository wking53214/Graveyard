# ICEBERG

Recovered **queue-era** IVR tree (pre-Correction 1) plus forensic dump under `RECOVERY/`. STACK: predecessor lineage toward sentinel_os / GSA-815. **Not the live runtime.** README claims a complete 3.x platform; code does not.

## 1. Pipeline Position & Role

**HISTORICAL / RECOVERY.** Off the live path. `sentinel_os` still uses `ICEBERG_*` env var *names* (fossils), not this package.

## 2. Full System Scope & Architectural Depth

Live tree: Domain/Engines/Sim/Replay/SDK/API/Admin/CLI/Deploy + Tests. `build_graph()` still emits `{intent}_queue` → `{intent}_agent` → `exit`. `Simulator._next_node` prefers queue then **falls back to first neighbor (fail-open)**. `StaffingRLEngine.compute_deltas` is `(load-0.5)` clipped — **not RL**. PPO/MARL never called from `Simulator.step`. `BayesianIntentEngineGPU` is small real log-space Bayes (torch).

Internal contradiction: Simulator docstring says StaffingRLEngine removed 2026-07-02; `Engines/staffing_rl.py` still ships.

## 3. What It Does NOT Do / Non-Goals

Does not govern, train RL, staff a contact center, serve a real dashboard, or deploy `iceberg-runtime:3.x` (image referenced, missing).

## 4. Brutally Honest Current Status & Gaps

| Claim (README) | Reality |
|---|---|
| PPO+MARL routing | Not wired to Simulator |
| Staffing optimizer | 10-line clip |
| Governance envelope | **No `GovernanceEnvelope` class** |
| Dashboard pages callers/telemetry | Templates: Index, Queues, Replay, rl only |
| API | `MockSimulator` always `next_node: "exit"` |
| `Main.py` | Imports `domain.*` / `dashboard_server` **that do not exist**. Tests shim `sys.modules`. |
| K8s/ArgoCD | Paper manifests |
| Two Replay stacks | `SDK/Replay.py` vs `Replay/` never unified |

This is the stale-docs failure mode ICEBURG's SCORECARD was written to prevent. `orjson` declared, unused. Cursor `ca://s?q=` comments in sources.

## 5. Core Invariants & Guarantees

SHA-256 structural hashes exist. **Routing is fail-open.** API `strict_mode` is a flag on a mock. No `canonical_fields`. No authenticity.

## 6. Inputs, Outputs & Type Contracts

`QueueState{name, active_calls, staffing, target_service_level=0.80, abandonment_rate=0.02}` — post-ACD fields ICEBURG refused. `SimulateRequest{caller_id, intent, emotion, steps}`.

## 7. Stack Integration Topology

```text
ICEBERG (this)  ≠  ICEBURG (honest July kernel)  ≠  GSA-815 iceberg_complete_simulator
RECOVERY/on_disk_copies/ includes later GSA-815 files, not wired
```

**Safe to archive.** Valuable part is `RECOVERY/`.

Apache-2.0.
