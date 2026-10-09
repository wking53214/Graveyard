"""The eight-module assessment/dispatch pipeline.

Two properties get disproportionate attention here because both were defects
once: that _gaps_headers writes MERGE rather than overwrite (upstream stages
record evidence into those blocks before this pipeline runs), and that the
integrity hash is a function of the data rather than of the moment.
"""

import json

import pytest

from metric_assessment_telemetry_dispatch_adapter import (
    AggregatedMetricScorer,
    BoundaryValidationFilter,
    CoreDataPipelineOrchestrator,
    DestinationTargetRouter,
    MessageDispatcher,
    ParallelEvaluationEngine,
    PresentationRenderer,
    TransactionAuditLedger,
    compute_stable_hash,
)


def valid_data(**overrides):
    data = {
        "source_id": "source-device-id-001",
        "timestamp": 1_700_000_000.0,
        "metrics": {"primary_metric_a": 120000, "secondary_metric_b": 3400},
        "attributes": {},
        "execution_context": "standard_evaluation_profile",
        "metadata": {},
    }
    data.update(overrides)
    return data


def empty_headers():
    return {"metadata": {}, "risk_metrics": {}, "structural_indices": {}}


class TestStableHash:
    def test_is_deterministic(self):
        assert compute_stable_hash({"a": 1}) == compute_stable_hash({"a": 1})

    def test_is_independent_of_key_order(self):
        assert compute_stable_hash({"a": 1, "b": 2}) == compute_stable_hash(
            {"b": 2, "a": 1}
        )

    def test_distinguishes_different_content(self):
        assert compute_stable_hash({"a": 1}) != compute_stable_hash({"a": 2})

    def test_is_a_sha256_hex_digest(self):
        digest = compute_stable_hash({"a": 1})
        assert len(digest) == 64
        int(digest, 16)


class TestBoundaryValidation:
    @pytest.mark.parametrize(
        "missing", sorted(BoundaryValidationFilter.MANDATORY_FIELDS)
    )
    def test_each_mandatory_field_is_actually_required(self, missing):
        data = valid_data()
        del data[missing]
        with pytest.raises(ValueError) as raised:
            BoundaryValidationFilter().process({"data": data})
        assert missing in str(raised.value)

    def test_optional_fields_default_rather_than_fail(self):
        data = valid_data()
        del data["attributes"]
        del data["metadata"]
        out = BoundaryValidationFilter().process({"data": data})
        assert out["validated_data"]["attributes"] == {}
        assert out["validated_data"]["metadata"] == {}

    def test_validated_data_carries_the_input_through(self):
        out = BoundaryValidationFilter().process({"data": valid_data()})
        assert out["validated_data"]["source_id"] == "source-device-id-001"
        assert out["validated_data"]["metrics"] == {
            "primary_metric_a": 120000,
            "secondary_metric_b": 3400,
        }

    def test_header_writes_merge_and_do_not_discard_upstream_evidence(self):
        """This module ran first in the standalone pipeline, where assignment
        and merge were indistinguishable. Under eddp_pipeline the guardrail and
        authentication stages have already written here, and assignment
        destroyed their evidence."""
        payload = {
            "data": valid_data(),
            "_gaps_headers": {
                "metadata": {},
                "risk_metrics": {
                    "deadman_triggered": False,
                    "ingestion_authenticated": True,
                },
                "structural_indices": {"upstream": "kept"},
            },
        }
        out = BoundaryValidationFilter().process(payload)
        risk = out["_gaps_headers"]["risk_metrics"]
        structural = out["_gaps_headers"]["structural_indices"]

        assert risk["deadman_triggered"] is False
        assert risk["ingestion_authenticated"] is True
        assert risk["boundary_violation_score"] == 0.0
        assert structural["upstream"] == "kept"
        assert structural["schema_validated"] is True

    def test_works_on_an_empty_header_block(self):
        out = BoundaryValidationFilter().process({"data": valid_data()})
        assert out["_gaps_headers"]["structural_indices"]["schema_validated"] is True


class TestParallelEvaluation:
    def test_scores_are_the_metrics_scaled_to_their_ceilings(self):
        payload = {"validated_data": valid_data(), "_gaps_headers": empty_headers()}
        out = ParallelEvaluationEngine().process(payload)
        scores = {r["layer_name"]: r["score"] for r in out["evaluation_results"]}

        assert scores["volume_stability_check"] == pytest.approx(1.0)
        assert scores["rate_health_check"] == pytest.approx(0.68)

    def test_scores_are_capped_at_one(self):
        payload = {
            "validated_data": valid_data(
                metrics={"primary_metric_a": 10**9, "secondary_metric_b": 10**9}
            ),
            "_gaps_headers": empty_headers(),
        }
        out = ParallelEvaluationEngine().process(payload)
        assert all(r["score"] == 1.0 for r in out["evaluation_results"])

    def test_absent_metrics_score_zero_rather_than_raising(self):
        payload = {
            "validated_data": valid_data(metrics={}),
            "_gaps_headers": empty_headers(),
        }
        out = ParallelEvaluationEngine().process(payload)
        assert all(r["score"] == 0.0 for r in out["evaluation_results"])

    def test_evaluation_count_is_recorded(self):
        payload = {"validated_data": valid_data(), "_gaps_headers": empty_headers()}
        out = ParallelEvaluationEngine().process(payload)
        assert out["_gaps_headers"]["risk_metrics"]["evaluation_count"] == 2


class TestAggregatedScoring:
    def test_composite_is_the_mean_of_the_layers(self):
        payload = {
            "evaluation_results": [
                {"layer_name": "a", "score": 1.0},
                {"layer_name": "b", "score": 0.0},
            ],
            "_gaps_headers": empty_headers(),
        }
        out = AggregatedMetricScorer().process(payload)
        assert out["metrics_summary"]["composite_score"] == pytest.approx(0.5)

    def test_no_evaluations_scores_zero_rather_than_dividing_by_zero(self):
        out = AggregatedMetricScorer().process(
            {"evaluation_results": [], "_gaps_headers": empty_headers()}
        )
        assert out["metrics_summary"]["composite_score"] == 0.0

    def test_the_integrity_hash_is_a_function_of_the_data_not_the_moment(self):
        """Two runs over identical data must agree, or the hash cannot be used
        to detect alteration."""
        def run():
            return AggregatedMetricScorer().process(
                {
                    "validated_data": valid_data(),
                    "evaluation_results": [{"layer_name": "a", "score": 1.0}],
                    "_gaps_headers": empty_headers(),
                }
            )["metrics_summary"]["state_integrity_hash"]

        assert run() == run()

    def test_altered_data_changes_the_integrity_hash(self):
        def run(source_id):
            return AggregatedMetricScorer().process(
                {
                    "validated_data": valid_data(source_id=source_id),
                    "evaluation_results": [{"layer_name": "a", "score": 1.0}],
                    "_gaps_headers": empty_headers(),
                }
            )["metrics_summary"]["state_integrity_hash"]

        assert run("device-a") != run("device-b")

    def test_the_hash_reaches_the_headers(self):
        out = AggregatedMetricScorer().process(
            {
                "validated_data": valid_data(),
                "evaluation_results": [{"layer_name": "a", "score": 1.0}],
                "_gaps_headers": empty_headers(),
            }
        )
        assert (
            out["_gaps_headers"]["structural_indices"]["state_integrity_hash"]
            == out["metrics_summary"]["state_integrity_hash"]
        )


class TestRouting:
    def test_a_known_context_resolves_to_its_targets(self):
        out = DestinationTargetRouter().process({"validated_data": valid_data()})
        assert out["resolved_targets"] == [
            "endpoint_receiver_01@network.internal",
            "endpoint_receiver_02@network.internal",
        ]

    def test_an_unknown_context_resolves_to_nothing_rather_than_a_default(self):
        """Delivering an unroutable payload to a fallback address would send
        data somewhere nobody asked for."""
        out = DestinationTargetRouter().process(
            {"validated_data": valid_data(execution_context="unregistered_profile")}
        )
        assert out["resolved_targets"] == []

    def test_an_injected_routing_table_replaces_the_default(self):
        router = DestinationTargetRouter({"custom": ["only@example.invalid"]})
        out = router.process(
            {"validated_data": valid_data(execution_context="custom")}
        )
        assert out["resolved_targets"] == ["only@example.invalid"]


class TestPresentation:
    def test_the_template_drives_the_view(self):
        out = PresentationRenderer().process(
            {
                "validated_data": valid_data(),
                "metrics_summary": {"composite_score": 0.84, "score_breakdown": {}},
                "layout_template": {
                    "display_title": "Primary Performance Log Summary",
                    "structural_sections": ["Section A"],
                },
            }
        )
        view = out["rendered_view"]
        assert view["display_title"] == "Primary Performance Log Summary"
        assert view["structural_sections"] == ["Section A"]
        assert view["evaluated_composite_score"] == 0.84

    def test_a_missing_template_falls_back_to_a_declared_default(self):
        out = PresentationRenderer().process({"validated_data": valid_data()})
        assert out["rendered_view"]["display_title"] == "Default Metric Summary"
        assert out["rendered_view"]["structural_sections"] == []


class TestDispatch:
    def test_the_receipt_records_where_the_payload_went(self):
        out = MessageDispatcher().process(
            {
                "resolved_targets": ["a@example.invalid"],
                "rendered_view": {"display_title": "T"},
                "channel_name": "standard_stream",
            }
        )
        receipt = out["dispatch_receipt"]
        assert receipt["destination_targets"] == ["a@example.invalid"]
        assert receipt["delivery_channel"] == "standard_stream"
        assert receipt["dispatch_status"] == "TRANSMISSION_SUCCESSFUL"

    def test_the_channel_defaults_when_unspecified(self):
        out = MessageDispatcher().process({})
        assert out["dispatch_receipt"]["delivery_channel"] == "standard_stream"


class TestAuditLedger:
    def test_identical_payloads_drive_the_uniqueness_ratio_down(self):
        ledger = TransactionAuditLedger()
        payload = {"validated_data": valid_data(), "metrics_summary": {}}

        first = ledger.process(dict(payload))
        assert first["audit_metrics"]["uniqueness_ratio"] == 1.0

        second = ledger.process(dict(payload))
        assert second["audit_metrics"]["uniqueness_ratio"] == pytest.approx(0.5)
        assert second["audit_metrics"]["total_records"] == 2

    def test_distinct_payloads_keep_the_ratio_at_one(self):
        ledger = TransactionAuditLedger()
        ledger.process({"validated_data": valid_data(source_id="a")})
        out = ledger.process({"validated_data": valid_data(source_id="b")})
        assert out["audit_metrics"]["uniqueness_ratio"] == 1.0

    def test_each_ledger_keeps_its_own_history(self):
        TransactionAuditLedger().process({"validated_data": valid_data()})
        fresh = TransactionAuditLedger().process({"validated_data": valid_data()})
        assert fresh["audit_metrics"]["total_records"] == 1


class TestAuditLedgerIsBounded:
    """The ledger used to keep every event forever and rebuild a set over the
    whole history on every call: quadratic in time, unbounded in memory, in
    the one component whose job is to keep working during a long run."""

    def _ledger(self, limit=4):
        return TransactionAuditLedger(max_history=limit)

    def _feed(self, ledger, count, *, distinct=True):
        out = None
        for index in range(count):
            source = f"s{index}" if distinct else "same"
            out = ledger.process({"validated_data": valid_data(source_id=source)})
        return out

    def test_retained_history_never_exceeds_the_limit(self):
        ledger = self._ledger(4)
        self._feed(ledger, 50)
        assert len(ledger.audit_history) == 4

    def test_the_distinct_hash_index_is_bounded_too(self):
        """The index is what replaced the per-call rescan. If it grew with the
        stream it would just be the old memory leak wearing a faster hat."""
        ledger = self._ledger(4)
        self._feed(ledger, 50)
        assert len(ledger._hash_counts) <= 4

    def test_total_records_stays_all_time_and_exact(self):
        """Bounding the window must not cost the one number that was never
        approximate."""
        ledger = self._ledger(4)
        out = self._feed(ledger, 50)
        assert out["audit_metrics"]["total_records"] == 50

    def test_the_window_the_ratio_covers_is_reported(self):
        ledger = self._ledger(4)
        out = self._feed(ledger, 50)
        assert out["audit_metrics"]["uniqueness_window"] == 4

    def test_the_window_is_the_stream_until_it_fills(self):
        ledger = self._ledger(4)
        out = self._feed(ledger, 2)
        assert out["audit_metrics"]["uniqueness_window"] == 2
        assert out["audit_metrics"]["total_records"] == 2

    def test_the_ratio_never_exceeds_one_across_eviction(self):
        """The failure mode of an incremental count: deque drops its oldest
        element silently, and a count that is never decremented drifts upward
        forever. A uniqueness ratio above 1.0 is worse than a slow one."""
        ledger = self._ledger(4)
        for index in range(200):
            out = ledger.process({"validated_data": valid_data(source_id=f"s{index}")})
            assert 0.0 < out["audit_metrics"]["uniqueness_ratio"] <= 1.0

    def test_eviction_decrements_rather_than_forgetting(self):
        """Fill the window with one repeated payload, then push distinct ones
        through. The ratio has to climb back to 1.0, which it can only do if
        the evicted duplicates were actually subtracted from the index."""
        ledger = self._ledger(4)
        self._feed(ledger, 4, distinct=False)
        assert ledger.process(
            {"validated_data": valid_data(source_id="same")}
        )["audit_metrics"]["uniqueness_ratio"] == pytest.approx(0.25)

        out = self._feed(ledger, 4)
        assert out["audit_metrics"]["uniqueness_ratio"] == pytest.approx(1.0)
        assert len(ledger._hash_counts) == 4

    def test_the_incremental_ratio_agrees_with_a_full_rescan(self):
        """The property the rewrite has to preserve: for every prefix of the
        stream, the cheap number equals the number the original computed the
        expensive way, over the records actually retained."""
        ledger = self._ledger(5)
        for index in range(60):
            source = f"s{index % 7}"
            out = ledger.process({"validated_data": valid_data(source_id=source)})
            rescanned = len({r["payload_data_hash"] for r in ledger.audit_history})
            assert out["audit_metrics"]["uniqueness_ratio"] == pytest.approx(
                rescanned / len(ledger.audit_history)
            )

    def test_an_unbounded_ledger_is_still_available_and_still_correct(self):
        """The bound is a default, not a decision taken away from the caller.
        max_history=None restores all-time behaviour for anyone who needs it."""
        ledger = TransactionAuditLedger(max_history=None)
        out = self._feed(ledger, 40)
        assert len(ledger.audit_history) == 40
        assert out["audit_metrics"]["uniqueness_window"] == 40
        assert out["audit_metrics"]["uniqueness_ratio"] == pytest.approx(1.0)

    def test_the_default_limit_is_declared_rather_than_buried(self):
        assert TransactionAuditLedger().audit_history.maxlen == \
            TransactionAuditLedger.DEFAULT_HISTORY_LIMIT


class TestOrchestrator:
    def test_the_default_sequence_runs_end_to_end(self):
        out = CoreDataPipelineOrchestrator().process(
            {
                "data": valid_data(),
                "layout_template": {"display_title": "T", "structural_sections": []},
                "channel_name": "standard_stream",
            }
        )
        summary = json.loads(out["clinical_summary"])

        assert summary["execution_status"] == "COMPLETED"
        assert summary["handshake_verified"] is True
        assert summary["composite_score"] == pytest.approx(0.84)
        assert summary["dispatch_status"] == "TRANSMISSION_SUCCESSFUL"
        assert summary["uniqueness_ratio"] == 1.0

    def test_a_schema_failure_propagates_out_of_the_orchestrator(self):
        with pytest.raises(ValueError):
            CoreDataPipelineOrchestrator().process({"data": {}})

    def test_an_unregistered_module_fails_the_handshake(self):
        class Unregistered:
            def process(self, payload):
                return payload

        orchestrator = CoreDataPipelineOrchestrator([Unregistered()])
        with pytest.raises(PermissionError):
            orchestrator.validate_handshakes()

    def test_a_registered_module_without_process_fails_the_handshake(self):
        class NoProcess:
            _is_authenticated_module = True

        orchestrator = CoreDataPipelineOrchestrator([NoProcess()])
        with pytest.raises(AttributeError):
            orchestrator.validate_handshakes()
