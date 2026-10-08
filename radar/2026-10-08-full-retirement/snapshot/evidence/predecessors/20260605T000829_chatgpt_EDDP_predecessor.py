"""
EDDP + Evaluation + Feedback Integrity System
Deterministic Architecture Kernel (Reference Implementation)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Callable, Optional
import time
import json
import hashlib


# ============================================================
# UTILITIES
# ============================================================

def stable_hash(obj: Dict[str, Any]) -> str:
    blob = json.dumps(obj, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()


# ============================================================
# CORE DATA CONTRACTS
# ============================================================

@dataclass
class Payload:
    dataset_id: str
    timestamp: float
    kpis: Dict[str, Any]
    dimensions: Dict[str, Any]
    role_context: str
    metadata: Dict[str, Any]


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
# ECP (UPSTREAM VALIDATION STUB)
# ============================================================

class ECPValidator:
    """
    Assumed upstream system.
    EDDP trusts this completely.
    """

    REQUIRED_FIELDS = {"dataset_id", "timestamp", "kpis", "role_context"}

    def validate(self, payload: Dict[str, Any]) -> Payload:
        missing = self.REQUIRED_FIELDS - set(payload.keys())
        if missing:
            raise ValueError(f"Invalid payload missing: {missing}")

        return Payload(
            dataset_id=payload["dataset_id"],
            timestamp=payload["timestamp"],
            kpis=payload["kpis"],
            dimensions=payload.get("dimensions", {}),
            role_context=payload["role_context"],
            metadata=payload.get("metadata", {})
        )


# ============================================================
# CONTEXT MODULE SYSTEM
# ============================================================

class ContextRegistry:
    def __init__(self):
        self.contexts: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, context: Dict[str, Any]):
        self.contexts[name] = context

    def get(self, name: str) -> Dict[str, Any]:
        return self.contexts.get(name, {})


# ============================================================
# EVALUATION LAYERS
# ============================================================

class EvaluationLayer:
    def __init__(self, name: str, fn: Callable[[Payload], float]):
        self.name = name
        self.fn = fn

    def evaluate(self, payload: Payload) -> EvaluationResult:
        score = self.fn(payload)
        return EvaluationResult(
            layer=self.name,
            score=score,
            notes=f"Evaluated by {self.name}"
        )


class EvaluationEngine:
    def __init__(self, layers: List[EvaluationLayer]):
        self.layers = layers

    def run(self, payload: Payload) -> List[EvaluationResult]:
        return [layer.evaluate(payload) for layer in self.layers]


# ============================================================
# BENCHMARK SCORING SYSTEM
# ============================================================

class BenchmarkScorer:
    def score(self, results: List[EvaluationResult], payload: Payload) -> BenchmarkResult:
        breakdown = {r.layer: r.score for r in results}
        overall = sum(breakdown.values()) / max(len(breakdown), 1)

        integrity_hash = stable_hash({
            "payload": payload.__dict__,
            "breakdown": breakdown,
            "overall": overall
        })

        return BenchmarkResult(
            overall_score=overall,
            breakdown=breakdown,
            integrity_hash=integrity_hash
        )


# ============================================================
# ROLE ROUTER
# ============================================================

class RoleRouter:
    def __init__(self, role_map: Dict[str, List[str]]):
        self.role_map = role_map

    def route(self, role: str) -> List[str]:
        return self.role_map.get(role, [])


# ============================================================
# TEMPLATE RENDERER
# ============================================================

class Renderer:
    def render(self, template: Dict[str, Any], payload: Payload, benchmark: BenchmarkResult):
        return {
            "title": template.get("title"),
            "sections": template.get("sections"),
            "kpis": payload.kpis,
            "role": payload.role_context,
            "benchmark_score": benchmark.overall_score,
            "benchmark_breakdown": benchmark.breakdown,
            "timestamp": payload.timestamp
        }


# ============================================================
# DISTRIBUTION ENGINE
# ============================================================

class Distributor:
    def deliver(self, recipients: List[str], dashboard: Dict[str, Any], channel: str) -> DeliveryEvent:
        return DeliveryEvent(
            timestamp=time.time(),
            recipients=recipients,
            channel=channel,
            dashboard=dashboard,
            status="DELIVERED"
        )


# ============================================================
# FEEDBACK LOOP INTEGRITY SYSTEM
# ============================================================

class FeedbackLoop:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def record(self, payload: Payload, benchmark: BenchmarkResult, delivery: DeliveryEvent):
        event = {
            "payload_hash": stable_hash(payload.__dict__),
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
# EDDP CORE SYSTEM
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

    def execute(self, raw_payload: Dict[str, Any], template: Dict[str, Any], role: str, channel="email"):
        # 1. validate upstream (ECP boundary)
        payload = self.validator.validate(raw_payload)

        # 2. evaluation layer stack
        eval_results = self.evaluator.run(payload)

        # 3. benchmark scoring
        benchmark = self.scorer.score(eval_results, payload)

        # 4. role routing
        recipients = self.router.route(role)

        # 5. render dashboard
        dashboard = self.renderer.render(template, payload, benchmark)

        # 6. distribute
        delivery = self.distributor.deliver(recipients, dashboard, channel)

        # 7. feedback loop integrity tracking
        self.feedback.record(payload, benchmark, delivery)

        return {
            "dashboard": dashboard,
            "delivery": delivery.__dict__,
            "benchmark": benchmark.__dict__,
            "integrity": self.feedback.integrity_check()
        }


# ============================================================
# EXAMPLE EVALUATION FUNCTIONS
# ============================================================

def revenue_stability(payload: Payload) -> float:
    return min(payload.kpis.get("revenue", 0) / 100000, 1.0)


def operational_health(payload: Payload) -> float:
    return min(payload.kpis.get("calls", 0) / 5000, 1.0)


# ============================================================
# OPTIONAL BOOTSTRAP
# ============================================================

if __name__ == "__main__":

    raw_payload = {
        "dataset_id": "ds-001",
        "timestamp": time.time(),
        "kpis": {"revenue": 120000, "calls": 3400},
        "dimensions": {},
        "role_context": "executive",
        "metadata": {}
    }

    template = {
        "title": "Executive Dashboard",
        "sections": ["Revenue", "Operations", "Risk"]
    }

    role_map = {
        "executive": ["cfo@company.com", "ceo@company.com"]
    }

    system = EDDPSystem(
        validator=ECPValidator(),
        evaluator=EvaluationEngine([
            EvaluationLayer("revenue_stability", revenue_stability),
            EvaluationLayer("operational_health", operational_health)
        ]),
        scorer=BenchmarkScorer(),
        router=RoleRouter(role_map),
        renderer=Renderer(),
        distributor=Distributor(),
        feedback=FeedbackLoop()
    )

    result = system.execute(raw_payload, template, "executive")

    print(json.dumps(result, indent=2, default=str))