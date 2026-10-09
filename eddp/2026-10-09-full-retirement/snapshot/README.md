# EDDP

**Evidence and Development Data Preservation** archive plus a **wired fail-closed ingest/assess/dispatch demo**. Not a single production application.

## 1. Pipeline Position & Role

**HISTORICAL / LAB PIPELINE.** Off the live path. Predecessor of observe-only telemetry + fail-closed ingest thinking. GAPS-style `_gaps_headers` later lived in GRAPH.

## 2. Full System Scope & Architectural Depth

Wired contract `.process(payload) -> payload`, `halted` short-circuit:

```
inbound → WS3SafetyGuardModule
       → IngestionAuthenticationModule (HMAC-SHA256)
       → BoundaryValidationFilter → ParallelEvaluationEngine
       → AggregatedMetricScorer → DestinationTargetRouter
       → PresentationRenderer → MessageDispatcher
       → TransactionAuditLedger
```

`FORBIDDEN_ACTIONS` substring match: `modify, write_back, alter_policy, influence, control, override, escalate_decision`. HMAC over canonical JSON; unsigned payloads **signed at ingest**. Secret: ctor / `EDDP_SIGNING_SECRET` / a random per-instance fallback (flagged `placeholder_secret_in_use`), so with no secret configured inbound signatures are rejected and only locally signed envelopes pass. A payload with no ingestion envelope is halted as unauthenticated (`require_envelope=False` reports and continues instead). Scoring: `primary_metric_a/100000`, `secondary_metric_b/5000`. Router defaults to two `@network.internal` fake endpoints. v1/v2 "enterprise kernel" files are reference-only (parse-checked, not behavioral).

~128–154 tests, no third-party deps. CI 3.11/3.12.

## 3. What It Does NOT Do / Non-Goals

Does not talk to a real dashboard, replace OBSERVE, or share a signing secret across processes unless `EDDP_SIGNING_SECRET` is set.

## 4. Brutally Honest Current Status & Gaps

| Gap | Detail |
|---|---|
| `TRANSCRIPT.md` | Advertised in older README; **missing**. Moved to the Gemini_History repo on 2026-09-24: `recovered/eddp-gemini-bc9823e74bfc1124/TRANSCRIPT.md`. |
| Unsigned traffic | An envelope with no signature is still signed at ingest. A payload with no envelope at all is now halted. |
| "Parallel evaluation" | Two sequential scalar ratios. |
| Placeholder HMAC | Removed from the code; still in git history; `.gitleaksignore` dismisses fingerprints. |
| Fake dispatch | Email-like internal endpoints. |

## 5. Core Invariants & Guarantees

True halt on forbidden action (`WS3Violation`), bad HMAC, schema fail, unknown `signal_type` (when observe module on). Handshake `_gaps_authenticated`. Scorer hash unkeyed. Ledger bounded deque.

## 6. Inputs, Outputs & Type Contracts

`WS3Mode{observe_only,disabled}`; `WS3SignalType{capacity,load,accuracy,drift,system_health}`. Envelope `ingestion_envelope.{body_content, metadata_context, cryptographic_signature, signature_origin}`. `UNSIGNED_FIELDS` frozenset. Mandatory assessment: `source_id, timestamp, metrics, execution_context`.

## 7. Stack Integration Topology

```text
EDDP GAPS headers → GRAPH/gaps-kernel (moved)
observe-perceive / sentinel_os  ✗ import
```

**Safe to archive.** Second-most "real" of the historical set because tests bite.

Apache-2.0.
