# STRIDE — CODE INVENTORY

Every symbol below is read out of recovered source with `ast`. Nothing is
listed that was not found in a recovered file.

## Source A — `stride-formatted-audited.py.GEMINI_EXPORT_VARIANT`

- bytes: 31741  lines: 748
- sha256: `5e37d167ac18f10186a4bc74db6bbf4c91c7a74b085e926a7bf22b4a60647ffb`
- origin: Gemini Apps Activity export, activity 904, `<pre><code>` block 2
- timestamp: 2026-06-22T02:57:20.552Z
- recovery status: RECOVERED FROM CONVERSATION
- parses as Python: YES

| kind | name | line | notes |
|---|---|---:|---|
| const | `COMPLIANCE_PATTERNS` | 32 | |
| const | `DEFAULT_TIME_BUDGET_MS` | 55 | |
| const | `MAXIMUM_RISK_THRESHOLD` | 56 | |
| const | `PAYLOAD_LENGTH_THRESHOLD` | 57 | |
| const | `TIME_WINDOW_SECONDS` | 58 | |
| const | `COMPLIANCE_IDENTITY_TOKENS` | 60 | |
| const | `COMPLIANCE_COURTESY_TOKENS` | 61 | |
| const | `WEIGHT_IDENTITY` | 63 | |
| const | `WEIGHT_COURTESY` | 64 | |
| const | `WEIGHT_LONG_PAYLOAD` | 65 | |
| const | `THREAD_WORKER_COUNT` | 67 | |
| const | `MAXIMUM_QUEUE_SIZE` | 68 | |
| class | `OperationalSnapshot` | 75 | — |
| class | `EvaluationMetric` | 90 | — |
| class | `IntelligenceReport` | 97 | — |
| class | `PolicyResult` | 107 | — |
| class | `Telemetry` | 115 | — |
| class | `ExecutionResult` | 123 | — |
| class | `AttestationJob` | 137 | — |
| class | `EngineState` | 145 | — |
| class | `IdentityValidator` | 157 | `validate` |
| class | `HedgingValidator` | 163 | `validate` |
| class | `CausalityValidator` | 169 | `validate` |
| class | `InputNormalizer` | 177 | `normalize` |
| class | `TrafficGovernor` | 184 | `__init__`, `calculate_delay_budget`, `apply_governor_delay` |
| class | `PipelineStateEngine` | 203 | `__init__`, `evaluate_integrity`, `check_loop_condition`, `record_state`, `check_retry_capacity`, `increment_retry`, `clear_retry_state`, `_compute_hash`, `process_lifecycle` |
| class | `DataValidationLayer` | 253 | `validate` |
| class | `AnomalyDetectionEngine` | 270 | `evaluate` |
| class | `VarianceTrackingEngine` | 291 | `evaluate` |
| class | `FragilityAssessmentEngine` | 321 | `evaluate` |
| class | `AnalyticalConsolidationEngine` | 342 | `compute` |
| class | `AnalyticalIntelligenceOrchestrator` | 358 | `__init__`, `compile_analytics` |
| class | `PerformanceDashboard` | 409 | `__init__`, `record_request_metric`, `record_rejection_metric`, `record_latency_metric`, `retrieve_dashboard_snapshot` |
| class | `SecureGatewayRuntime` | 443 | `__init__`, `_generate_token_stream`, `_assess_risk_metrics`, `evaluate_runtime_policy`, `generate_telemetry_profile`, `_processing_worker_loop`, `activate_processing_pool`, `_determine_backpressure_delay`, `_compile_operational_snapshot`, `execute`, `evaluate_policy_rules`, `evaluate_policy_runtime`, `get_dashboard_metrics` |
| def | `simulated_provider_gateway` | 720 | |
| def | `run_system_sandbox` | 726 | |

### Prompt-supplied search anchors — evidenced vs not

| anchor | evidenced in Source A | where |
|---|---|---|
| `InputNormalizer` | YES | class, line 177 |
| `PipelineStateEngine` | YES | class, line 203 |
| `check_loop_condition` | YES | method, line 214 |
| `seen_outputs` | YES | attr, line 147 |
| `prohibited_verbs` | NO | regex key |
| `hmac` | YES | import, line 11 |
| `attestation` | YES | term, line 6 |
| `telemetry` | YES | term, line 127 |
| `analytics` | YES | term, line 370 |
