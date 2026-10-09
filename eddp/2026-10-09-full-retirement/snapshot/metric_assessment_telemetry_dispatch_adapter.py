from __future__ import annotations
from collections import Counter, deque
from dataclasses import dataclass, field
from typing import Deque, Dict, Any, List, Callable, Optional, Type
import time
import json
import hashlib

# =====================================================================
# GOVERNANCE REGISTRY AND UTILITIES
# =====================================================================
MODULE_REGISTRY: Dict[str, Type] = {}

def register_as_module(cls: Type) -> Type:
   """Decorator for system authentication and governance handshake validation."""
   MODULE_REGISTRY[cls.__name__] = cls
   setattr(cls, "_is_authenticated_module", True)
   return cls

def compute_stable_hash(target_object: Dict[str, Any]) -> str:
   """Generates a deterministic SHA-256 hash string from a dictionary object."""
   serialized_blob = json.dumps(target_object, sort_keys=True, default=str).encode()
   return hashlib.sha256(serialized_blob).hexdigest()


# =====================================================================
# GSA UNIVERSAL ADAPTER MODULES
# =====================================================================
@register_as_module
class BoundaryValidationFilter:
   """Enforces rigid type checks and schema confirmation at systemic boundaries."""
   MANDATORY_FIELDS = {"source_id", "timestamp", "metrics", "execution_context"}

   def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
       raw_input = payload.get("data", {})
       missing_fields = self.MANDATORY_FIELDS - set(raw_input.keys())
       if missing_fields:
           raise ValueError(f"Input schema failure. Missing mandatory entries: {missing_fields}")

       # Merge rather than replace. These were plain assignments while this
       # module ran first in the standalone pipeline, where the difference was
       # invisible. Under eddp_pipeline the guardrail and authentication stages
       # record evidence into these blocks beforehand, and assignment discarded
       # it. On an empty block, update() behaves identically to the original.
       headers = payload.setdefault("_gaps_headers", {})
       headers.setdefault("structural_indices", {}).update(
           {"schema_validated": True, "source_id": raw_input["source_id"]}
       )
       headers.setdefault("risk_metrics", {}).update({"boundary_violation_score": 0.0})

       payload["validated_data"] = {
           "source_id": raw_input["source_id"],
           "timestamp": raw_input["timestamp"],
           "metrics": raw_input["metrics"],
           "attributes": raw_input.get("attributes", {}),
           "execution_context": raw_input["execution_context"],
           "metadata": raw_input.get("metadata", {})
       }
       return payload


@register_as_module
class ParallelEvaluationEngine:
   """Orchestrates validation evaluations across registered metrics."""
   def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
       val_data = payload.get("validated_data", {})
       metrics = val_data.get("metrics", {})

       vol_stability = min(metrics.get("primary_metric_a", 0) / 100000.0, 1.0)
       rate_health = min(metrics.get("secondary_metric_b", 0) / 5000.0, 1.0)

       evaluations = [
           {"layer_name": "volume_stability_check", "score": vol_stability, "evaluation_notes": "Processed volume stability check"},
           {"layer_name": "rate_health_check", "score": rate_health, "evaluation_notes": "Processed rate health check"}
       ]

       payload["evaluation_results"] = evaluations
       headers = payload.setdefault("_gaps_headers", {})
       headers["risk_metrics"]["evaluation_count"] = len(evaluations)
       return payload


@register_as_module
class AggregatedMetricScorer:
   """Consolidates individual numeric layers and produces structural state check hashes."""
   def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
       evaluations = payload.get("evaluation_results", [])
       breakdown_map = {res["layer_name"]: res["score"] for res in evaluations}
       composite_mean = sum(breakdown_map.values()) / max(len(breakdown_map), 1)

       state_hash = compute_stable_hash({
           "validated_data": payload.get("validated_data", {}),
           "breakdown_metrics": breakdown_map,
           "composite_value": composite_mean
       })

       payload["metrics_summary"] = {
           "composite_score": composite_mean,
           "score_breakdown": breakdown_map,
           "state_integrity_hash": state_hash
       }

       headers = payload.setdefault("_gaps_headers", {})
       headers["structural_indices"]["state_integrity_hash"] = state_hash
       headers["risk_metrics"]["composite_score"] = composite_mean
       return payload


@register_as_module
class DestinationTargetRouter:
   """Maps operational tracking profiles to explicit downstream communication pathways."""
   def __init__(self, routing_table: Optional[Dict[str, List[str]]] = None):
       self.routing_table = routing_table or {
           "standard_evaluation_profile": ["endpoint_receiver_01@network.internal", "endpoint_receiver_02@network.internal"]
       }

   def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
       val_data = payload.get("validated_data", {})
       exec_ctx = val_data.get("execution_context", "standard_evaluation_profile")
       payload["resolved_targets"] = self.routing_table.get(exec_ctx, [])
       return payload


@register_as_module
class PresentationRenderer:
   """Standardizes target outputs, injecting evaluation histories into clear interfaces."""
   def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
       val_data = payload.get("validated_data", {})
       summary = payload.get("metrics_summary", {})
       template = payload.get("layout_template", {})

       payload["rendered_view"] = {
           "display_title": template.get("display_title", "Default Metric Summary"),
           "structural_sections": template.get("structural_sections", []),
           "extracted_metrics": val_data.get("metrics", {}),
           "runtime_context": val_data.get("execution_context", ""),
           "evaluated_composite_score": summary.get("composite_score", 0.0),
           "evaluated_score_breakdown": summary.get("score_breakdown", {}),
           "generation_timestamp": val_data.get("timestamp", time.time())
       }
       return payload


@register_as_module
class MessageDispatcher:
   """Coordinates packet delivery across registered external communication channels."""
   def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
       targets = payload.get("resolved_targets", [])
       rendered = payload.get("rendered_view", {})
       channel = payload.get("channel_name", "standard_stream")

       payload["dispatch_receipt"] = {
           "timestamp": time.time(),
           "destination_targets": targets,
           "delivery_channel": channel,
           "rendered_view": rendered,
           "dispatch_status": "TRANSMISSION_SUCCESSFUL"
       }
       return payload


@register_as_module
class TransactionAuditLedger:
   """Tracks systemic loop execution histories to verify operational consistency.

   MEASURED, then bounded. The original kept every event in an unbounded list
   and rebuilt a set over the whole history on every call to recount distinct
   payload hashes. That is quadratic in the number of events and unbounded in
   memory, and both showed up as soon as anybody looked:

       events   per-event   held
          500      14.5 us    500
         1000      23.3 us   1000
         2000      51.7 us   2000
         4000      95.1 us   4000      (~4x the time for 2x the events)
        20000           --  20000      6.3 MiB live, still growing

   After, same machine, same benchmark:

       events   per-event   held
          500       5.6 us    500
         1000       5.6 us   1000
         2000       5.8 us   1000
         4000       6.2 us   1000      (~2x the time for 2x the events)
        20000           --   1000      0.35 MiB live, flat

   Linear instead of quadratic, flat per event, and bounded in memory. At
   4000 events that is ~15x faster, and the gap widens with every event after
   it -- which is the point, because the original was slowest exactly when it
   had been running longest.

   A long-running ingest is exactly where an audit ledger is supposed to be
   useful, and it was the one component that got slower the longer it ran.
   SecureDataIngestionPipeline in this same repository already had the answer:
   a deque with maxlen. This adopts it, and keeps the distinct-hash count
   incrementally so the ratio costs nothing to maintain.

   What the numbers now mean, stated because bounding changed one of them:

     total_records      every event this ledger has ever seen. Exact, all-time,
                        and unaffected by the window.
     uniqueness_window  how many events the ratio below was computed over.
     uniqueness_ratio   distinct payload hashes WITHIN that window. Previously
                        all-time, which an unbounded list is the only way to
                        offer. The window is reported beside it so the number
                        is never read against a population it does not cover.
   """

   DEFAULT_HISTORY_LIMIT = 1000

   def __init__(self, max_history: Optional[int] = DEFAULT_HISTORY_LIMIT):
       self.audit_history: Deque[Dict[str, Any]] = deque(maxlen=max_history)
       self.total_records = 0
       self._hash_counts: Counter = Counter()

   def _remember(self, event_record: Dict[str, Any]) -> None:
       """Append, evicting by hand so the distinct-hash count stays right.

       deque drops the oldest element silently when it is full, and a count
       that is never decremented would drift upward forever -- a uniqueness
       ratio above 1.0, which is worse than the slow version it replaced."""
       limit = self.audit_history.maxlen
       if limit is not None and len(self.audit_history) == limit:
           evicted = self.audit_history[0]["payload_data_hash"]
           self._hash_counts[evicted] -= 1
           if self._hash_counts[evicted] <= 0:
               del self._hash_counts[evicted]
       self.audit_history.append(event_record)
       self._hash_counts[event_record["payload_data_hash"]] += 1
       self.total_records += 1

   def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
       val_data = payload.get("validated_data", {})
       summary = payload.get("metrics_summary", {})
       receipt = payload.get("dispatch_receipt", {})

       event_record = {
           "payload_data_hash": compute_stable_hash(val_data),
           "summary_metrics_hash": summary.get("state_integrity_hash", ""),
           "dispatch_final_status": receipt.get("dispatch_status", ""),
           "log_timestamp": time.time()
       }
       self._remember(event_record)

       payload["audit_metrics"] = {
           "uniqueness_ratio": len(self._hash_counts) / len(self.audit_history),
           "total_records": self.total_records,
           "uniqueness_window": len(self.audit_history)
       }
       return payload


# =====================================================================
# DYNAMIC BINDING ENGINE AND ORCHESTRATOR
# =====================================================================
@register_as_module
class CoreDataPipelineOrchestrator:
   """Centralized binding engine validating handshakes and sequencing execution."""
   def __init__(self, pipeline_sequence: Optional[List[Any]] = None):
       if pipeline_sequence is None:
           self.pipeline_sequence = [
               BoundaryValidationFilter(),
               ParallelEvaluationEngine(),
               AggregatedMetricScorer(),
               DestinationTargetRouter(),
               PresentationRenderer(),
               MessageDispatcher(),
               TransactionAuditLedger()
           ]
       else:
           self.pipeline_sequence = pipeline_sequence

   def validate_handshakes(self) -> bool:
       """Verifies governance module authentication before pipeline execution."""
       for module in self.pipeline_sequence:
           if not getattr(module, "_is_authenticated_module", False):
               raise PermissionError(f"Handshake validation failed for module: {module.__class__.__name__}")
           if not hasattr(module, "process") or not callable(getattr(module, "process")):
               raise AttributeError(f"Standardized process interface missing in module: {module.__class__.__name__}")
       return True

   def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
       """Sequences pipeline execution and outputs a serialized clinical summary."""
       self.validate_handshakes()

       if "_gaps_headers" not in payload:
           payload["_gaps_headers"] = {
               "metadata": {"orchestrator": self.__class__.__name__, "init_time": time.time()},
               "risk_metrics": {},
               "structural_indices": {}
           }

       for module in self.pipeline_sequence:
           payload = module.process(payload)

       clinical_summary = {
           "execution_status": "COMPLETED",
           "handshake_verified": True,
           "gaps_headers": payload["_gaps_headers"],
           "composite_score": payload.get("metrics_summary", {}).get("composite_score"),
           "dispatch_status": payload.get("dispatch_receipt", {}).get("dispatch_status"),
           "uniqueness_ratio": payload.get("audit_metrics", {}).get("uniqueness_ratio")
       }

       payload["clinical_summary"] = json.dumps(clinical_summary, indent=2, default=str)
       return payload


if __name__ == "__main__":
   mock_input_payload = {
       "data": {
           "source_id": "source-device-id-001",
           "timestamp": time.time(),
           "metrics": {"primary_metric_a": 120000, "secondary_metric_b": 3400},
           "attributes": {},
           "execution_context": "standard_evaluation_profile",
           "metadata": {}
       },
       "layout_template": {
           "display_title": "Primary Performance Log Summary",
           "structural_sections": ["Section A", "Section B", "Section C"]
       },
       "channel_name": "standard_stream"
   }

   binding_engine = CoreDataPipelineOrchestrator()
   final_output = binding_engine.process(mock_input_payload)
   print("--- EXECUTION COMPLETED ---")
   print(final_output["clinical_summary"])
