# VANGUARD

**Retired 2026-09-03.** Two preserved files. Canonical home for this content: [`TOUCHSTONE`](https://github.com/wking53214/TOUCHSTONE). Not on the live path.

## 1. Pipeline Position & Role

**ARCHIVED PERIMETER SKETCH.** Explicitly excluded from Admission→Custody. Moved out of DGK because it had nowhere else to go.

## 2. Full System Scope & Architectural Depth

- `vanguard-behavioral-simulation-flattened.py` — minified pipeline: contradictory term pairs, regime classifier (`STABLE|UNSTABLE|CRITICAL` at 0.35/0.65), HMAC-SHA256 default key **`"default-vanguard-key"`**, actuation clip magic numbers. Docstring claims ESN/Lyapunov; **code has neither**.
- `vanguard-unified-governance-wrapper.py` — 45 lines referencing **undefined** `PipelineCycleManager`, `UnifiedSovereignKernel`, `system_logger`. Hardcoded secret `"Coldfire"`. `asyncio.run` → `NameError`.

IOError on log write is swallowed (`pass`) — **fail-open on audit**.

## 3. What It Does NOT Do / Non-Goals

Forecast, Lyapunov stability, wrap a real kernel, govern actuation. Not [`fortress-kernel`](https://github.com/wking53214/fortress-kernel).

## 4. Brutally Honest Current Status & Gaps

Already retired. Archiving the GitHub repo is bookkeeping. Flattened file `__main__` demo may run; wrapper does not. Default HMAC key is public.

## 5. Core Invariants & Guarantees

None you should rely on. Wrapper *would* `REJECTED / VANGUARD_ANOMALY` if it imported.

## 6. Inputs, Outputs & Type Contracts

`SystemInputStructure(text_content_body, numeric_metric_value, metadata_map)` in the flattened file.

## 7. Stack Integration Topology

```text
DGK → this repo → TOUCHSTONE specimens → SWIZZLE/ghost_tools
observe-perceive / fortress-kernel  ✗
```

Apache-2.0.
