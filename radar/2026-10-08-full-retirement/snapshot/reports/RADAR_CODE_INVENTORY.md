# RADAR — CODE INVENTORY

Symbols read out of recovered source with `ast`. Files that do not parse are
reported as not parsing; nothing was reformatted to make them parse.
Execution results were obtained by running each file once, unmodified.

## `eddp-comprehensive-synthesized.py`

- was: `artifact_4.py`
- bytes 14751 · CRLF line breaks 369
- sha256 `ede000dfbdf94d099fe6d85aab4f971a52d9bd9852fc8b10a767585e80fa998b`
- observed on execution: runs, 58 lines of output
- parses as Python: YES

| kind | name | line | methods |
|---|---|---:|---|
| def | `calculate_secure_hash` | 22 | |
| class | `InputPayloadContract` | 40 | — |
| class | `EvaluationLayerResult` | 50 | — |
| class | `BenchmarkCompositeResult` | 57 | — |
| class | `DeliveryTrackingEvent` | 64 | — |
| class | `DataPayloadValidator` | 76 | `process_data_validation` |
| class | `EvaluationProcessingLayer` | 103 | `__init__`, `execute_layer_evaluation` |
| class | `EvaluationOrchestrationEngine` | 127 | `__init__`, `run_all_evaluations` |
| class | `MetricsBenchmarkScorer` | 137 | `calculate_composite_metrics` |
| class | `AccessRoleRouter` | 161 | `resolve_routing_targets` |
| class | `ComponentRenderer` | 168 | `generate_rendered_output` |
| class | `AssetDistributor` | 192 | `__init__`, `execute_delivery_dispatch` |
| class | `PipelineFeedbackSystem` | 221 | `__init__`, `record_execution_state`, `assess_system_novelty` |
| class | `RADARSystem` | 255 | `__init__`, `execute_orchestration_cycle` |
| def | `reference_revenue_stability_check` | 320 | |
| def | `reference_operational_health_check` | 324 | |

## `eddp-core-engine-v1.py`

- was: `artifact_2.py`
- bytes 10662 · CRLF line breaks 316
- sha256 `97f9ae9a9875e72aa232bab5000ac084742e29ba63494ba799113f5ee454846c`
- observed on execution: runs, 62 lines of output
- parses as Python: YES

| kind | name | line | methods |
|---|---|---:|---|
| def | `stable_hash` | 19 | |
| class | `Payload` | 30 | — |
| class | `EvaluationResult` | 40 | — |
| class | `BenchmarkResult` | 47 | — |
| class | `DeliveryEvent` | 54 | — |
| class | `ECPValidator` | 66 | `validate` |
| class | `EvaluationLayer` | 85 | `__init__`, `evaluate` |
| class | `EvaluationEngine` | 105 | `__init__`, `run` |
| class | `BenchmarkScorer` | 114 | `score` |
| class | `RoleRouter` | 134 | `route` |
| class | `Renderer` | 140 | `render` |
| class | `Distributor` | 158 | `__init__`, `deliver` |
| class | `FeedbackLoop` | 182 | `__init__`, `record`, `integrity_check` |
| class | `EDDPSystem` | 209 | `__init__`, `execute` |
| def | `custom_revenue_stability` | 264 | |
| def | `custom_operational_health` | 268 | |

## `eddp-core-engine-v2-refined.py`

- was: `artifact_3.py`
- bytes 14576 · CRLF line breaks 368
- sha256 `df7f91037f7e1a6b584c8db046e1d6140d37d755e7859a4dbdb657052ebf5c18`
- observed on execution: runs, 58 lines of output
- parses as Python: YES

| kind | name | line | methods |
|---|---|---:|---|
| def | `calculate_secure_hash` | 21 | |
| class | `InputPayloadContract` | 39 | — |
| class | `EvaluationLayerResult` | 49 | — |
| class | `BenchmarkCompositeResult` | 56 | — |
| class | `DeliveryTrackingEvent` | 63 | — |
| class | `DataPayloadValidator` | 75 | `process_data_validation` |
| class | `EvaluationProcessingLayer` | 102 | `__init__`, `execute_layer_evaluation` |
| class | `EvaluationOrchestrationEngine` | 126 | `__init__`, `run_all_evaluations` |
| class | `MetricsBenchmarkScorer` | 136 | `calculate_composite_metrics` |
| class | `AccessRoleRouter` | 160 | `resolve_routing_targets` |
| class | `ComponentRenderer` | 167 | `generate_rendered_output` |
| class | `AssetDistributor` | 191 | `__init__`, `execute_delivery_dispatch` |
| class | `PipelineFeedbackSystem` | 220 | `__init__`, `record_execution_state`, `assess_system_novelty` |
| class | `ExecutiveDashboardDistributionProcessor` | 254 | `__init__`, `execute_orchestration_cycle` |
| def | `reference_revenue_stability_check` | 319 | |
| def | `reference_operational_health_check` | 323 | |

## `eddp-pipeline-core-simple.py`

- was: `artifact_1.py`
- bytes 1174 · CRLF line breaks 0
- sha256 `66df1813ace0998b8d9d6334a9c06a616b07d281e27ed04436c92ab323140541`
- observed on execution: runs, no output
- parses as Python: YES

| kind | name | line | methods |
|---|---|---:|---|

## `eddp-wrapped-final.py`

- was: `artifact_5.py`
- bytes 5376 · CRLF line breaks 0
- sha256 `a7026823c9a985cb7ff3d90a24a832fbc51cfb3ff2c922d61c52296808dbaa04`
- observed on execution: SyntaxError
- parses as Python: **NO** — SyntaxError line 1: invalid syntax
- the file contains 0 line breaks: it is a flattened single-line paste. Left exactly as found; not reformatted.

## `gsa_universal_interlock_wrapper.py`

- was: `gsa_universal_interlock_wrapper.py (not renamed)`
- bytes 18179 · CRLF line breaks 396
- sha256 `aba510cc512b4aed074c81606819761a33161d5ba1e2a80ff58d7f78f2c9a4eb`
- observed on execution: runs, no output
- parses as Python: YES

| kind | name | line | methods |
|---|---|---:|---|
| def | `_internal_deep_freeze_structure_function` | 73 | |
| class | `ComposableLegoModule` | 93 | `process_payload` |
| def | `compute_state_signature` | 113 | |
| class | `GsaUniversalAdapter` | 152 | `__init__`, `process_payload` |
| class | `GsaTemporalDoorwayGate` | 295 | `__init__`, `start_gate_engine`, `shutdown_gate_engine`, `_hash_rotation_worker`, `execute_governance_logic` |

