"""WS3 observe-only guardrail: the refusal, and the observation.

The guardrail's whole value is that it refuses a mutating action BEFORE any
processing occurs. Every test here therefore asserts on the refusal itself --
the exception, the recorded evidence, and the disabled mode -- rather than on
the fact that a function was called.
"""

import pytest

from eddp_telemetry_guardrail import (
    CoreOrchestratorBinder,
    WS3AnalyticsCalculatorModule,
    WS3Mode,
    WS3SafetyGuardModule,
    WS3SignalType,
    WS3TelemetryObserveModule,
    WS3Violation,
)


def _headers(payload):
    return payload["_gaps_headers"]


class TestSafetyGuard:
    def test_observational_action_is_permitted_and_recorded(self):
        guard = WS3SafetyGuardModule()
        out = guard.process({"attempted_action": "observe_telemetry"})

        assert out["halted"] is False
        assert out["mode"] == WS3Mode.OBSERVE_ONLY.value
        assert _headers(out)["risk_metrics"]["deadman_triggered"] is False
        assert _headers(out)["risk_metrics"]["safety_violations"] == 0

    def test_missing_action_defaults_to_observe(self):
        out = WS3SafetyGuardModule().process({})
        assert out["mode"] == WS3Mode.OBSERVE_ONLY.value

    @pytest.mark.parametrize("action", sorted(WS3SafetyGuardModule.FORBIDDEN_ACTIONS))
    def test_every_forbidden_action_raises(self, action):
        with pytest.raises(WS3Violation) as raised:
            WS3SafetyGuardModule().process({"attempted_action": action})
        assert action in str(raised.value)

    def test_forbidden_action_is_detected_as_a_substring(self):
        """'override_policy' must trip the 'override' rule. The guard matches
        on containment, and a rule that only matched whole strings would let
        every decorated variant through."""
        with pytest.raises(WS3Violation):
            WS3SafetyGuardModule().process({"attempted_action": "override_policy"})

    def test_detection_is_case_insensitive(self):
        with pytest.raises(WS3Violation):
            WS3SafetyGuardModule().process({"attempted_action": "ESCALATE_DECISION"})

    def test_violation_records_evidence_before_raising(self):
        """The payload is mutated in place, so the evidence survives the raise.
        Without this the caller catches an exception and has nothing to log."""
        payload = {"attempted_action": "modify"}
        with pytest.raises(WS3Violation):
            WS3SafetyGuardModule().process(payload)

        assert payload["halted"] is True
        assert payload["mode"] == WS3Mode.DISABLED.value
        assert _headers(payload)["risk_metrics"]["deadman_triggered"] is True
        assert _headers(payload)["risk_metrics"]["safety_violations"] == 1

    def test_existing_headers_are_not_replaced(self):
        payload = {
            "attempted_action": "observe",
            "_gaps_headers": {
                "metadata": {"upstream": "kept"},
                "risk_metrics": {},
                "structural_indices": {},
            },
        }
        out = WS3SafetyGuardModule().process(payload)
        assert _headers(out)["metadata"]["upstream"] == "kept"


class TestSignalTypeVocabulary:
    """The enum is a declared vocabulary. These tests pin what it admits."""

    def test_every_member_is_accepted_by_the_observe_module(self):
        for member in WS3SignalType:
            out = WS3TelemetryObserveModule().process({"signal_type": member.value})
            assert out["telemetry_report"]["signal_type"] == member.value

    def test_the_declared_vocabulary_is_exactly_these_five(self):
        """Two assertions, because they catch different edits.

        The value comparison catches a member added with a new value. The
        mapping over __members__ also catches one added as an ALIAS of an
        existing value: iterating an Enum skips aliases, so the value
        comparison cannot see one, and an alias is how a careless edit widens
        a vocabulary that other code dispatches on.

        A note on how this test got here, since the history is misleading.
        ghost_buster --mutate once reported the value comparison alone as a
        vacuous_check -- "the implementation the test names was broken and the
        test did not notice". That was a false positive in the scanner, not a
        weakness in the test: it had mutated the archived copy of this module
        in _archive/, which nothing imports, so no test could have noticed.
        The value comparison was always sound and kills its mutant once the
        scanner mutates the file this test actually imports (ghost_tools
        1.7.9). The mapping assertion is kept anyway, on its own merits: the
        alias gap it closes is real and was found while chasing the false
        report.
        """
        assert {m.value for m in WS3SignalType} == {
            "capacity",
            "load",
            "accuracy",
            "drift",
            "system_health",
        }
        assert {
            name: member.value
            for name, member in WS3SignalType.__members__.items()
        } == {
            "CAPACITY": "capacity",
            "LOAD": "load",
            "ACCURACY": "accuracy",
            "DRIFT": "drift",
            "SYSTEM_HEALTH": "system_health",
        }


    def test_every_member_is_reachable_from_stored_data(self):
        """Each member is produced by coercing the string a stored telemetry
        record carries. Before the vocabulary was enforced, four of the five
        were states the system could name and never enter."""
        for member in WS3SignalType:
            out = WS3TelemetryObserveModule().process({"signal_type": member.value})
            assert (
                WS3SignalType(out["_gaps_headers"]["metadata"]["signal_type"])
                is member
            )

    def test_the_default_signal_type_is_a_declared_member(self):
        out = WS3TelemetryObserveModule().process({})
        assert out["telemetry_report"]["signal_type"] == WS3SignalType.LOAD.value

    @pytest.mark.parametrize(
        "unrecognised", ["utilisation", "LOAD", "", "capacity ", 7, None]
    )
    def test_an_unrecognised_signal_type_halts_rather_than_passing_through(
        self, unrecognised
    ):
        """Accepting an arbitrary string would let a payload claim a state the
        enum does not define, and anything dispatching on it would silently do
        nothing for a value that was merely misspelled upstream."""
        out = WS3TelemetryObserveModule().process({"signal_type": unrecognised})

        assert out["halted"] is True
        assert "telemetry_report" not in out
        assert _headers(out)["risk_metrics"]["signal_type_recognized"] is False

    def test_the_refusal_names_the_vocabulary_it_enforced(self):
        out = WS3TelemetryObserveModule().process({"signal_type": "utilisation"})
        for member in WS3SignalType:
            assert member.value in out["block_reason"]

    def test_a_recognised_signal_type_is_recorded_as_recognised(self):
        out = WS3TelemetryObserveModule().process(
            {"signal_type": WS3SignalType.DRIFT.value}
        )
        assert _headers(out)["risk_metrics"]["signal_type_recognized"] is True
        assert not out.get("halted")

    def test_an_unrecognised_signal_type_stops_downstream_analytics(self):
        """Fail-closed: the halt has to be honoured by the next stage, not just
        recorded by this one."""
        payload = WS3TelemetryObserveModule().process({"signal_type": "utilisation"})
        out = WS3AnalyticsCalculatorModule().process(payload)
        assert "analytics_summary" not in out


class TestTelemetryObserve:
    def test_report_carries_the_observed_signal(self):
        out = WS3TelemetryObserveModule().process(
            {
                "domain": "autonomous_fleet",
                "signal_type": "load",
                "metrics": {"gpu_utilization": 0.72, "sensor_latency_ms": 14.3},
                "notes": ["snapshot"],
            }
        )
        report = out["telemetry_report"]

        assert report["domain"] == "autonomous_fleet"
        assert report["metrics"] == {"gpu_utilization": 0.72, "sensor_latency_ms": 14.3}
        assert report["notes"] == ["snapshot"]
        assert _headers(out)["structural_indices"]["metrics_count"] == 2

    def test_report_copies_rather_than_aliases_the_input(self):
        """A report described as immutable must not share mutable state with
        the payload it was built from."""
        metrics = {"gpu_utilization": 0.5}
        notes = ["first"]
        out = WS3TelemetryObserveModule().process(
            {"metrics": metrics, "notes": notes}
        )

        metrics["gpu_utilization"] = 0.9
        notes.append("second")

        assert out["telemetry_report"]["metrics"] == {"gpu_utilization": 0.5}
        assert out["telemetry_report"]["notes"] == ["first"]

    def test_halted_payload_passes_through_untouched(self):
        out = WS3TelemetryObserveModule().process({"halted": True})
        assert "telemetry_report" not in out


class TestAnalyticsCalculator:
    def test_capacity_pressure_is_the_square_of_utilization(self):
        out = WS3AnalyticsCalculatorModule().process(
            {"metrics": {"utilization": 0.5}}
        )
        assert out["analytics_summary"]["capacity_pressure"] == pytest.approx(0.25)

    def test_gpu_utilization_is_the_fallback_key(self):
        out = WS3AnalyticsCalculatorModule().process(
            {"metrics": {"gpu_utilization": 0.4}}
        )
        assert out["analytics_summary"]["capacity_pressure"] == pytest.approx(0.16)

    @pytest.mark.parametrize(
        "utilization,expected", [(-2.0, 0.0), (0.0, 0.0), (1.0, 1.0), (7.5, 1.0)]
    )
    def test_utilization_is_clamped_into_the_unit_interval(self, utilization, expected):
        out = WS3AnalyticsCalculatorModule().process(
            {"metrics": {"utilization": utilization}}
        )
        assert out["analytics_summary"]["capacity_pressure"] == pytest.approx(expected)

    def test_drift_is_relative_to_the_baseline(self):
        out = WS3AnalyticsCalculatorModule().process(
            {"metrics": {"utilization": 0.72}, "baseline": 0.5, "current": 0.72}
        )
        assert out["analytics_summary"]["drift_score"] == pytest.approx(0.44)

    def test_drift_is_zero_when_there_is_no_baseline_to_drift_from(self):
        """Division by a zero baseline is undefined, and reporting a fabricated
        number would be worse than reporting none."""
        out = WS3AnalyticsCalculatorModule().process(
            {"metrics": {"utilization": 0.72}, "baseline": 0.0}
        )
        assert out["analytics_summary"]["drift_score"] == 0.0

    def test_drift_is_unsigned(self):
        below = WS3AnalyticsCalculatorModule().process(
            {"baseline": 1.0, "current": 0.4, "metrics": {}}
        )
        above = WS3AnalyticsCalculatorModule().process(
            {"baseline": 1.0, "current": 1.6, "metrics": {}}
        )
        assert below["analytics_summary"]["drift_score"] == pytest.approx(0.6)
        assert above["analytics_summary"]["drift_score"] == pytest.approx(0.6)

    def test_halted_payload_passes_through_untouched(self):
        out = WS3AnalyticsCalculatorModule().process({"halted": True})
        assert "analytics_summary" not in out


class TestCoreOrchestratorBinder:
    def test_full_observational_cycle_completes(self):
        import json

        result = CoreOrchestratorBinder().process(
            {
                "domain": "autonomous_fleet",
                "signal_type": WS3SignalType.LOAD.value,
                "metrics": {"gpu_utilization": 0.72},
                "attempted_action": "observe_telemetry",
                "baseline": 0.50,
                "current": 0.72,
            }
        )
        summary = json.loads(result["clinical_summary"])

        assert summary["execution_status"] == "COMPLETED"
        assert summary["mode"] == WS3Mode.OBSERVE_ONLY.value
        assert summary["domain"] == "autonomous_fleet"
        assert summary["deadman_triggered"] is False
        assert summary["capacity_pressure"] == pytest.approx(0.5184)

    def test_violation_propagates_out_of_the_binder(self):
        """The binder does not catch WS3Violation. A caller that wants the
        refusal recorded rather than raised must use EDDPPipeline."""
        with pytest.raises(WS3Violation):
            CoreOrchestratorBinder().process({"attempted_action": "control"})

    def test_handshake_validation_passes_for_registered_modules(self):
        assert CoreOrchestratorBinder().validate_handshakes() is True

    def test_handshake_failure_is_raised_not_ignored(self, monkeypatch):
        monkeypatch.setattr(
            WS3SafetyGuardModule, "_gaps_authenticated", False, raising=False
        )
        with pytest.raises(PermissionError):
            CoreOrchestratorBinder().validate_handshakes()
