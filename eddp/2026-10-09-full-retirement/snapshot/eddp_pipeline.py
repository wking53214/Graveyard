"""
EDDP INTEGRATED PIPELINE

Chains the repository's three previously disconnected working components into a
single ordered execution path:

    1. WS3SafetyGuardModule          (was stranded in _unsorted/, never wired in)
    2. IngestionAuthenticationModule (was in CODE, never wired in)
    3. the eight-module assessment/dispatch pipeline
       (metric_assessment_telemetry_dispatch_adapter, already working standalone)

Ordering rationale, safety-first:

    The guardrail runs before anything else so that a payload attempting a
    mutating action is refused before any processing occurs. Authentication runs
    next so that unverifiable payloads never reach evaluation or dispatch.
    Only then does the existing assessment pipeline run.

All modules share the same .process(payload) -> payload contract and the same
_gaps_headers convention, which is why they compose without adapters.

Fail-closed: once any stage sets payload["halted"], every later stage returns
the payload untouched, and execution_status reports HALTED.
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional

from eddp_ingestion_authentication import IngestionAuthenticationModule
from eddp_telemetry_guardrail import (
    WS3AnalyticsCalculatorModule,
    WS3SafetyGuardModule,
    WS3TelemetryObserveModule,
    WS3Violation,
)
from metric_assessment_telemetry_dispatch_adapter import (
    AggregatedMetricScorer,
    BoundaryValidationFilter,
    DestinationTargetRouter,
    MessageDispatcher,
    ParallelEvaluationEngine,
    PresentationRenderer,
    TransactionAuditLedger,
)


class EDDPPipeline:
    """Sequences the full EDDP execution path with handshake validation."""

    def __init__(
        self,
        cryptographic_secret: Optional[str] = None,
        include_telemetry_analysis: bool = False,
    ):
        self.stages: List[Any] = [
            WS3SafetyGuardModule(),
            IngestionAuthenticationModule(cryptographic_secret),
        ]

        # The WS3 observe/analytics modules read utilization-shaped telemetry,
        # which is a different payload shape from the assessment pipeline's
        # metrics. They are therefore opt-in rather than always-on, so the
        # default path does not silently produce empty analytics.
        if include_telemetry_analysis:
            self.stages.append(WS3TelemetryObserveModule())
            self.stages.append(WS3AnalyticsCalculatorModule())

        self.stages.extend(
            [
                BoundaryValidationFilter(),
                ParallelEvaluationEngine(),
                AggregatedMetricScorer(),
                DestinationTargetRouter(),
                PresentationRenderer(),
                MessageDispatcher(),
                TransactionAuditLedger(),
            ]
        )

    def validate_handshakes(self) -> bool:
        """Confirms every stage is registered and exposes .process().

        Modules carry one of two registration markers depending on which source
        file they came from; both are accepted.
        """
        for stage in self.stages:
            authenticated = getattr(
                stage, "_is_authenticated_module", False
            ) or getattr(stage, "_gaps_authenticated", False)
            if not authenticated:
                raise PermissionError(
                    f"Handshake validation failed for module: "
                    f"{stage.__class__.__name__}"
                )
            if not callable(getattr(stage, "process", None)):
                raise AttributeError(
                    f"Standardized process interface missing in module: "
                    f"{stage.__class__.__name__}"
                )
        return True

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_handshakes()

        payload.setdefault(
            "_gaps_headers",
            {
                "metadata": {
                    "orchestrator": self.__class__.__name__,
                    "init_time": time.time(),
                },
                "risk_metrics": {},
                "structural_indices": {},
            },
        )

        for stage in self.stages:
            if payload.get("halted"):
                break
            try:
                payload = stage.process(payload)
            except WS3Violation as violation:
                payload["halted"] = True
                payload["block_reason"] = str(violation)
                break

        headers = payload["_gaps_headers"]
        clinical_summary = {
            "execution_status": "HALTED" if payload.get("halted") else "COMPLETED",
            "block_reason": payload.get("block_reason"),
            "deadman_triggered": headers["risk_metrics"].get("deadman_triggered"),
            "ingestion_authenticated": headers["risk_metrics"].get(
                "ingestion_authenticated"
            ),
            "signature_origin": headers["metadata"].get("signature_origin"),
            "placeholder_secret_in_use": headers["metadata"].get(
                "placeholder_secret_in_use"
            ),
            "composite_score": payload.get("metrics_summary", {}).get(
                "composite_score"
            ),
            "state_integrity_hash": payload.get("metrics_summary", {}).get(
                "state_integrity_hash"
            ),
            "dispatch_status": payload.get("dispatch_receipt", {}).get(
                "dispatch_status"
            ),
            "gaps_headers": headers,
        }

        payload["clinical_summary"] = json.dumps(
            clinical_summary, indent=2, default=str
        )
        return payload


if __name__ == "__main__":
    pipeline = EDDPPipeline()

    clean_payload = {
        "attempted_action": "observe",
        "ingestion_envelope": {
            "body_content": "Quarterly operational summary for distribution.",
            "metadata_context": {"source": "reporting-service"},
        },
        "data": {
            "source_id": "source-device-id-001",
            "timestamp": time.time(),
            "metrics": {"primary_metric_a": 120000, "secondary_metric_b": 3400},
            "attributes": {},
            "execution_context": "standard_evaluation_profile",
            "metadata": {},
        },
        "layout_template": {
            "display_title": "Primary Performance Log Summary",
            "structural_sections": ["Section A", "Section B", "Section C"],
        },
        "channel_name": "standard_stream",
    }

    print("--- CASE 1: clean payload ---")
    print(pipeline.process(dict(clean_payload))["clinical_summary"])

    print("\n--- CASE 2: payload attempting a mutating action ---")
    blocked = dict(clean_payload)
    blocked["attempted_action"] = "override_policy"
    print(EDDPPipeline().process(blocked)["clinical_summary"])

    print("\n--- CASE 3: payload bearing a forged signature ---")
    forged = dict(clean_payload)
    forged["ingestion_envelope"] = dict(clean_payload["ingestion_envelope"])
    forged["ingestion_envelope"]["cryptographic_signature"] = "0" * 64
    print(EDDPPipeline().process(forged)["clinical_summary"])
