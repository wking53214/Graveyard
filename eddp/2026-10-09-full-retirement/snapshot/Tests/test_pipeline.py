"""The integrated pipeline, end to end.

The pipeline's stated contract is fail-closed: once any stage sets
payload["halted"], every later stage returns the payload untouched and
execution_status reports HALTED. A pipeline that merely *usually* stops is
worth nothing, so the halting is asserted stage by stage as well as in the
summary.
"""

import json

import pytest

from eddp_pipeline import EDDPPipeline
from eddp_telemetry_guardrail import WS3AnalyticsCalculatorModule, WS3TelemetryObserveModule

SECRET = "test-secret"


def clean_payload(**overrides):
    payload = {
        "attempted_action": "observe",
        "ingestion_envelope": {
            "body_content": "Quarterly operational summary for distribution.",
            "metadata_context": {"source": "reporting-service"},
        },
        "data": {
            "source_id": "source-device-id-001",
            "timestamp": 1_700_000_000.0,
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
    payload.update(overrides)
    return payload


def summary_of(payload):
    return json.loads(payload["clinical_summary"])


class TestStageOrdering:
    def test_the_guardrail_runs_before_authentication(self):
        """Safety-first ordering is the design claim. A payload that is both
        mutating AND forged must be refused for the mutation, because the
        guardrail should never have let it reach the authenticator."""
        payload = clean_payload(attempted_action="override_policy")
        payload["ingestion_envelope"] = dict(payload["ingestion_envelope"])
        payload["ingestion_envelope"]["cryptographic_signature"] = "0" * 64

        summary = summary_of(EDDPPipeline(SECRET).process(payload))
        assert summary["execution_status"] == "HALTED"
        assert "forbidden_action_detected" in summary["block_reason"]
        assert summary["ingestion_authenticated"] is None

    def test_telemetry_stages_are_opt_in(self):
        """They read a different payload shape. Always-on would silently
        produce empty analytics on every assessment run."""
        default = EDDPPipeline(SECRET)
        assert not any(
            isinstance(stage, (WS3TelemetryObserveModule, WS3AnalyticsCalculatorModule))
            for stage in default.stages
        )

        opted_in = EDDPPipeline(SECRET, include_telemetry_analysis=True)
        assert any(
            isinstance(stage, WS3TelemetryObserveModule) for stage in opted_in.stages
        )
        assert any(
            isinstance(stage, WS3AnalyticsCalculatorModule) for stage in opted_in.stages
        )

    def test_handshake_validation_accepts_both_registration_markers(self):
        """Modules come from two source files using two different markers."""
        assert EDDPPipeline(SECRET).validate_handshakes() is True

    def test_an_unregistered_stage_is_refused(self):
        class Unregistered:
            def process(self, payload):
                return payload

        pipeline = EDDPPipeline(SECRET)
        pipeline.stages.append(Unregistered())
        with pytest.raises(PermissionError):
            pipeline.validate_handshakes()


class TestCleanPayload:
    def test_a_clean_payload_completes(self):
        summary = summary_of(EDDPPipeline(SECRET).process(clean_payload()))

        assert summary["execution_status"] == "COMPLETED"
        assert summary["block_reason"] is None
        assert summary["deadman_triggered"] is False
        assert summary["ingestion_authenticated"] is True
        assert summary["signature_origin"] == "signed_at_ingest"
        assert summary["dispatch_status"] == "TRANSMISSION_SUCCESSFUL"

    def test_the_composite_score_reaches_the_summary(self):
        summary = summary_of(EDDPPipeline(SECRET).process(clean_payload()))
        assert summary["composite_score"] == pytest.approx(0.84)

    def test_evidence_from_every_stage_survives_to_the_summary(self):
        """Each stage writes into _gaps_headers. The merge behaviour in the
        assessment stages is what keeps the earlier stages' evidence alive."""
        summary = summary_of(EDDPPipeline(SECRET).process(clean_payload()))
        headers = summary["gaps_headers"]

        assert headers["risk_metrics"]["deadman_triggered"] is False
        assert headers["risk_metrics"]["ingestion_authenticated"] is True
        assert headers["risk_metrics"]["boundary_violation_score"] == 0.0
        assert headers["risk_metrics"]["evaluation_count"] == 2
        assert headers["structural_indices"]["schema_validated"] is True
        assert headers["structural_indices"]["source_id"] == "source-device-id-001"
        assert headers["structural_indices"]["state_integrity_hash"]

    def test_an_inbound_signature_from_the_same_secret_is_verified(self):
        from eddp_ingestion_authentication import SecureDataIngestionPipeline

        payload = clean_payload()
        envelope = dict(payload["ingestion_envelope"])
        envelope["cryptographic_signature"] = SecureDataIngestionPipeline(
            SECRET
        ).generate_payload_signature(envelope)
        payload["ingestion_envelope"] = envelope

        summary = summary_of(EDDPPipeline(SECRET).process(payload))
        assert summary["execution_status"] == "COMPLETED"
        assert summary["signature_origin"] == "verified_inbound"


class TestFailClosed:
    def test_a_mutating_action_is_refused_before_any_processing(self):
        payload = clean_payload(attempted_action="override_policy")
        result = EDDPPipeline(SECRET).process(payload)
        summary = summary_of(result)

        assert summary["execution_status"] == "HALTED"
        assert summary["deadman_triggered"] is True
        assert result.get("validated_data") is None
        assert result.get("dispatch_receipt") is None

    def test_a_forged_signature_is_refused_before_dispatch(self):
        payload = clean_payload()
        payload["ingestion_envelope"] = dict(payload["ingestion_envelope"])
        payload["ingestion_envelope"]["cryptographic_signature"] = "0" * 64

        result = EDDPPipeline(SECRET).process(payload)
        summary = summary_of(result)

        assert summary["execution_status"] == "HALTED"
        assert summary["ingestion_authenticated"] is False
        assert "unauthenticated" in summary["block_reason"]
        assert result.get("dispatch_receipt") is None

    def test_a_signature_from_a_foreign_secret_is_refused(self):
        from eddp_ingestion_authentication import SecureDataIngestionPipeline

        payload = clean_payload()
        envelope = dict(payload["ingestion_envelope"])
        envelope["cryptographic_signature"] = SecureDataIngestionPipeline(
            "a-different-secret"
        ).generate_payload_signature(envelope)
        payload["ingestion_envelope"] = envelope

        summary = summary_of(EDDPPipeline(SECRET).process(payload))
        assert summary["execution_status"] == "HALTED"
        assert summary["ingestion_authenticated"] is False

    def test_a_malformed_envelope_halts_the_run(self):
        payload = clean_payload(ingestion_envelope={"body_content": ""})
        summary = summary_of(EDDPPipeline(SECRET).process(payload))
        assert summary["execution_status"] == "HALTED"
        assert "schema" in summary["block_reason"].lower()

    def test_no_stage_after_the_halt_writes_to_the_payload(self):
        """The contract is that later stages return the payload untouched, not
        merely that the final status says HALTED."""
        payload = clean_payload(attempted_action="escalate_decision")
        result = EDDPPipeline(SECRET).process(payload)

        for produced_downstream in (
            "validated_data",
            "evaluation_results",
            "metrics_summary",
            "resolved_targets",
            "rendered_view",
            "dispatch_receipt",
            "audit_metrics",
        ):
            assert produced_downstream not in result


class TestSecretHandling:
    def test_the_placeholder_secret_is_declared_in_the_summary(self, monkeypatch):
        monkeypatch.delenv("EDDP_SIGNING_SECRET", raising=False)
        summary = summary_of(EDDPPipeline().process(clean_payload()))
        assert summary["placeholder_secret_in_use"] is True

    def test_a_real_secret_clears_the_placeholder_flag(self):
        summary = summary_of(EDDPPipeline(SECRET).process(clean_payload()))
        assert summary["placeholder_secret_in_use"] is False


class TestDeterminism:
    def test_the_integrity_hash_is_stable_across_runs(self):
        """The hash covers validated data and scores, none of which depend on
        when the run happened."""
        first = summary_of(EDDPPipeline(SECRET).process(clean_payload()))
        second = summary_of(EDDPPipeline(SECRET).process(clean_payload()))
        assert first["state_integrity_hash"] == second["state_integrity_hash"]

    def test_different_data_produces_a_different_hash(self):
        baseline = summary_of(EDDPPipeline(SECRET).process(clean_payload()))

        altered = clean_payload()
        altered["data"] = dict(altered["data"])
        altered["data"]["source_id"] = "source-device-id-002"
        changed = summary_of(EDDPPipeline(SECRET).process(altered))

        assert baseline["state_integrity_hash"] != changed["state_integrity_hash"]
