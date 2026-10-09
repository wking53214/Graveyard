"""
EDDP (Executive Dashboard Distribution Processor)
Fully Integrated Enterprise Kernel & Evaluation Reference Implementation
"""

from __future__ import annotations
import os
import time
import json
import hashlib
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Callable, Optional


# ============================================================
# CRYPTOGRAPHIC & STATE UTILITIES
# ============================================================

def stable_hash(obj: Dict[str, Any]) -> str:
   """Generates a stable SHA-256 hash from a dictionary for deterministic tracking."""
   blob = json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
   return hashlib.sha256(blob).hexdigest()


# ============================================================
# DATA CONTRACTS (TYPED COMPONENT BOUNDARIES)
# ============================================================

@dataclass
class Payload:
   dataset_id: str
   timestamp: float
   kpis: Dict[str, Any]
   dimensions: Dict[str, Any] = field(default_factory=dict)
   role_context: str = "guest"
   metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationResult:
   layer: str
   score: float
   notes: str = ""


@dataclass
class BenchmarkResult:
   overall_score: float
   breakdown: Dict[str, float]
   integrity_hash: str


@dataclass
class DeliveryEvent:
   timestamp: float
   recipients: List[str]
   channel: str
   dashboard: Dict[str, Any]
   status: str


# ============================================================
# UNIQUE COMPONENTS
# ============================================================

class ECPValidator:
   """Upstream verification engine trusted to map raw payloads into typed structures."""
   REQUIRED_FIELDS = {"dataset_id", "timestamp", "kpis", "role_context"}

   def validate(self, payload: Dict[str, Any]) -> Payload:
       missing = self.REQUIRED_FIELDS - set(payload.keys())
       if missing:
           raise ValueError(f"Invalid payload missing required keys: {missing}")

       return Payload(
           dataset_id=payload["dataset_id"],
           timestamp=payload["timestamp"],
           kpis=payload["kpis"],
           dimensions=payload.get("dimensions", {}),
           role_context=payload["role_context"],
           metadata=payload.get("metadata", {})
       )


class EvaluationLayer:
   """A pluggable, isolated logic checkpoint applied against dataset metrics."""
   def __init__(self, name: str, fn: Callable[[Payload], float]):
       self.name = name
       self.fn = fn

   def evaluate(self, payload: Payload) -> EvaluationResult:
       try:
           score = self.fn(payload)
       except Exception as e:
           score = 0.0
           return EvaluationResult(layer=self.name, score=score, notes=f"Error during evaluation: {str(e)}")
       
       return EvaluationResult(
           layer=self.name,
           score=score,
           notes=f"Evaluated successfully by {self.name}"
       )


class EvaluationEngine:
   """Orchestrates sequential iteration across all registered evaluation sub-layers."""
   def __init__(self, layers: List[EvaluationLayer]):
       self.layers = layers

   def run(self, payload: Payload) -> List[EvaluationResult]:
       return [layer.evaluate(payload) for layer in self.layers]


class BenchmarkScorer:
   """Computes mathematical composites and seals states with structural hashes."""
   def score(self, results: List[EvaluationResult], payload: Payload) -> BenchmarkResult:
       breakdown = {r.layer: r.score for r in results}
       overall = sum(breakdown.values()) / max(len(breakdown), 1)

       # Uses native 'asdict' to elegantly deep-serialize dataclasses without string errors
       integrity_hash = stable_hash({
           "payload": asdict(payload),
           "breakdown": breakdown,
           "overall": overall
       })

       return BenchmarkResult(
           overall_score=overall,
           breakdown=breakdown,
           integrity_hash=integrity_hash
       )


class RoleRouter:
   """Maps configured enterprise access lists statically or at dynamic runtimes."""
   def route(self, role_map: Dict[str, List[str]], role: str) -> List[str]:
       return role_map.get(role, [])


class Renderer:
   """Assembles layout presentations by decoupling configuration data from KPIs."""
   def render(self, template: Dict[str, Any], payload: Payload, benchmark: Optional[BenchmarkResult] = None) -> Dict[str, Any]:
       rendered = {
           "title": template.get("title"),
           "sections": template.get("sections"),
           "kpis": payload.kpis,
           "role": payload.role_context,
           "timestamp": payload.timestamp
       }
       if benchmark:
           rendered["benchmark_score"] = benchmark.overall_score
           rendered["benchmark_breakdown"] = benchmark.breakdown
           rendered["integrity_hash"] = benchmark.integrity_hash
           
       return rendered


class Distributor:
   """Dispatches dashboard assets and saves serialized tracking rows cleanly to a JSONL audit log."""
   def __init__(self, log_path: str = "logs/delivery_log.jsonl"):
       self.log_path = log_path
       log_dir = os.path.dirname(self.log_path)
       if log_dir:
           os.makedirs(log_dir, exist_ok=True)

   def deliver(self, recipients: List[str], dashboard: Dict[str, Any], channel: str) -> DeliveryEvent:
       event = DeliveryEvent(
           timestamp=time.time(),
           recipients=recipients,
           channel=channel,
           dashboard=dashboard,
           status="DELIVERED"
       )

       # Encodes directly via json.dumps to fully adhere to the JSON Lines format specification
       with open(self.log_path, "a", encoding="utf-8") as f:
           f.write(json.dumps(asdict(event)) + "\n")

       return event


class FeedbackLoop:
   """Maintains an execution log history to dynamically evaluate pipeline novelty metrics."""
   def __init__(self):
       self.history: List[Dict[str, Any]] = []

   def record(self, payload: Payload, benchmark: BenchmarkResult, delivery: DeliveryEvent):
       event = {
           "payload_hash": stable_hash(asdict(payload)),
           "benchmark_hash": benchmark.integrity_hash,
           "delivery_status": delivery.status,
           "timestamp": time.time()
       }
       self.history.append(event)

   def integrity_check(self) -> float:
       if not self.history:
           return 1.0

       unique_payloads = len({h["payload_hash"] for h in self.history})
       total = len(self.history)
       return unique_payloads / total


# ============================================================
# MASTER ORCHESTRATION PIPELINE KERNEL
# ============================================================

class EDDPSystem:
   def __init__(
       self,
       validator: ECPValidator,
       evaluator: EvaluationEngine,
       scorer: BenchmarkScorer,
       router: RoleRouter,
       renderer: Renderer,
       distributor: Distributor,
       feedback: FeedbackLoop
   ):
       self.validator = validator
       self.evaluator = evaluator
       self.scorer = scorer
       self.router = router
       self.renderer = renderer
       self.distributor = distributor
       self.feedback = feedback
       self.delivery_log: List[DeliveryEvent] = []  # Local internal session state capture

   def execute(self, raw_payload: Dict[str, Any], template: Dict[str, Any], role_map: Dict[str, List[str]], role: str, channel: str = "email") -> Dict[str, Any]:
       # 1. Validation Contract Processing
       payload = self.validator.validate(raw_payload)

       # 2. Rule Evaluation
       eval_results = self.evaluator.run(payload)

       # 3. Benchmark Scoring & Hash Signing
       benchmark = self.scorer.score(eval_results, payload)

       # 4. Target Recipient Routing
       recipients = self.router.route(role_map, role)

       # 5. Composite Presentation Rendering
       dashboard = self.renderer.render(template, payload, benchmark)

       # 6. Output Delivery & Persistent JSONL Logging
       delivery = self.distributor.deliver(recipients, dashboard, channel)

       # 7. Internal Session Storage & Global Pipeline Novelty Audit
       self.delivery_log.append(delivery)
       self.feedback.record(payload, benchmark, delivery)

       return {
           "dashboard": dashboard,
           "delivery": asdict(delivery),
           "benchmark": asdict(benchmark),
           "integrity": self.feedback.integrity_check()
       }


# ============================================================
# REFERENCE TEST BENCH PIPELINE RUN
# ============================================================

def custom_revenue_stability(payload: Payload) -> float:
   return min(payload.kpis.get("revenue", 0) / 100000, 1.0)


def custom_operational_health(payload: Payload) -> float:
   return min(payload.kpis.get("calls", 0) / 5000, 1.0)


if __name__ == "__main__":
   # Sample Mock Dynamic Core Data Source
   mock_payload = {
       "dataset_id": "ds-prod-887",
       "timestamp": time.time(),
       "kpis": {"revenue": 125000, "calls": 3800},
       "role_context": "executive"
   }

   # Configuration Template Map Specs
   mock_template = {
       "title": "Executive Dashboard",
       "sections": ["Revenue Summary", "Operational KPIs", "Risk Indicators"]
   }

   # Access Role Bindings Map
   mock_roles = {
       "executive": ["ceo@company.com", "cfo@company.com"],
       "operations": ["coo@company.com"]
   }

   # Initializing Integrated Cluster Ecosystem
   eddp_kernel = EDDPSystem(
       validator=ECPValidator(),
       evaluator=EvaluationEngine([
           EvaluationLayer("revenue_stability", custom_revenue_stability),
           EvaluationLayer("operational_health", custom_operational_health)
       ]),
       scorer=BenchmarkScorer(),
       router=RoleRouter(),
       renderer=Renderer(),
       distributor=Distributor(log_path="logs/production_deliveries.jsonl"),
       feedback=FeedbackLoop()
   )

   # Process Master Orchestration Pipeline
   pipeline_output = eddp_kernel.execute(
       raw_payload=mock_payload,
       template=mock_template,
       role_map=mock_roles,
       role="executive",
       channel="email"
   )

   print("\n=== SYSTEM EXECUTION PIPELINE COMPLETE ===")
   print(json.dumps(pipeline_output, indent=2, default=str))