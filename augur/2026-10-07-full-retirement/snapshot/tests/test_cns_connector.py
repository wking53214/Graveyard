"""The connected half: what AUGUR's screen becomes when CNS is installed.

Skipped when CNS is absent. The independence half, which must hold in both
environments, is in ``test_cns_independence.py`` and never skips.

These tests are pytest-style (fixtures, parametrize). Run them with ``pytest``;
``python -m unittest discover`` runs only the original AUGUR tests, and this
module is merely reported as skipped under it when CNS is absent.
"""

from __future__ import annotations

import inspect
import math
import os
import random
import sys
import unittest
from decimal import Decimal

import pytest

try:
    cns_gate = pytest.importorskip(
        "cns.gate", reason="cns not installed; run in an environment with augur[cns]"
    )
except pytest.skip.Exception as skipped:
    # pytest's Skipped is a BaseException that `python -m unittest discover`
    # (the runner tests/test_augur.py documents) reports as an import error.
    # SkipTest is a skip to both runners.
    raise unittest.SkipTest(str(skipped)) from None

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import augur.kernel as kernel  # noqa: E402
from augur import SimulationConfig, run_simulation  # noqa: E402
from augur import cns_connector  # noqa: E402
from augur.cns_connector import (  # noqa: E402
    CnsGate,
    cns_available,
    cns_chain,
    scenario_digest,
    screen_to_cns,
    to_cns_result,
)

# A hard scenario far from its target, so a seeded run can land in any regime.
HARD = dict(initial_state=-500.0, initial_target=1000.0, shifted_target=2000.0)
HARD_NOISE = 30.0

#: (config, noise_scale, native regime). The regime is asserted against the
#: real run below, so these labels cannot drift from the kernel unnoticed.
STABLE_CFG = SimulationConfig(seed=42)
UNSTABLE_CFG = SimulationConfig(seed=0, **HARD)
CRITICAL_CFG = SimulationConfig(seed=3, **HARD)
SAMPLES = (
    (STABLE_CFG, 4.0),
    (SimulationConfig(seed=7, total_steps=25), 4.0),
    (SimulationConfig(seed=10, **HARD), HARD_NOISE),
    (UNSTABLE_CFG, HARD_NOISE),
    (SimulationConfig(seed=4, **HARD), HARD_NOISE),
    (CRITICAL_CFG, HARD_NOISE),
    (SimulationConfig(seed=12, **HARD), HARD_NOISE),
    (SimulationConfig(seed=0, total_steps=12), 25.0),
    (SimulationConfig(seed=3, total_steps=12), 25.0),
)


@pytest.fixture(autouse=True)
def _audit_log_in_tmp(tmp_path, monkeypatch):
    """Every step of a run appends to an audit log; keep it out of the tree."""
    monkeypatch.setattr(kernel, "_AUDIT_LOG_PATH", str(tmp_path / "audit.log"))


def _native(cfg, noise):
    return run_simulation(cfg, noise_scale=noise, record_history=False)


def _result(regime, cfg=STABLE_CFG, *, distortion=0.0, final_state=100.0):
    """What run_simulation returns, as far as the connector reads it."""
    return {
        "regime": regime,
        "distortion": distortion,
        "final_state": final_state,
        "config": cfg.as_dict(),
    }


def _translate(result, cfg=STABLE_CFG, noise=4.0, **kwargs):
    return to_cns_result(result, cfg, noise_scale=noise, **kwargs)


# ---------------------------------------------------------------------------
# The mapping
# ---------------------------------------------------------------------------


def test_cns_is_seen_as_available():
    assert cns_available() is True


def test_the_samples_really_cover_every_regime_the_kernel_reports():
    assert {_native(c, n)["regime"] for c, n in SAMPLES} == {
        "STABLE",
        "UNSTABLE",
        "CRITICAL",
    }


def test_the_regime_vocabulary_matches_the_kernel():
    seen = {
        kernel.RegimeEngine.classify(volatility, distortion)
        for volatility in (0.0, 5.0, 10.5, 15.0, 25.0)
        for distortion in (0.0, 0.2, 0.4, 0.5, 0.7, 0.9)
    }
    assert seen == {cns_connector.STABLE, *cns_connector.REFUSING_REGIMES}


def test_the_default_noise_scale_is_run_simulations_own():
    default = inspect.signature(run_simulation).parameters["noise_scale"].default
    assert cns_connector.DEFAULT_NOISE_SCALE == default


def test_a_stable_result_maps_to_pass_at_the_alpha_end():
    verdict = _translate(_result("STABLE"))
    assert verdict.outcome is cns_gate.GateOutcome.PASS
    assert verdict.position is cns_gate.GatePosition.ALPHA
    assert verdict.gate == "augur_screen"
    assert not verdict.blocking()


def test_a_pass_says_it_is_an_absence_of_objection_and_not_an_approval():
    verdict = _translate(_result("STABLE"))
    assert "absence of objection" in verdict.reason
    assert "not evidence that acting is safe" in verdict.reason
    assert "cannot approve" in verdict.reason


def test_a_pass_says_that_only_the_last_step_was_judged():
    """AUGUR reports the regime at the last step, and a run is usually worse
    than that earlier, so the verdict a consumer reads must say so."""
    reason = _translate(_result("STABLE")).reason
    assert "Only the last step is judged" in reason
    assert "earlier steps of the run may have been UNSTABLE or CRITICAL" in reason


@pytest.mark.parametrize("regime", ["UNSTABLE", "CRITICAL"])
def test_a_predicted_instability_maps_to_terminal_breach(regime):
    verdict = _translate(_result(regime, UNSTABLE_CFG, distortion=0.7), UNSTABLE_CFG)
    assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH
    assert verdict.position is cns_gate.GatePosition.ALPHA
    assert verdict.blocking()
    assert regime in verdict.reason
    assert "sufficient reason not to proceed" in verdict.reason


@pytest.mark.parametrize(
    "regime",
    ["stable", "Stable", "STABLE ", " STABLE", "", None, 0, 1, True, [], {}, "UNKNOWN",
     "DIVERGENT", "CHAOTIC", "GOVERNED", "NOMINAL"],
)
def test_nothing_but_the_exact_string_stable_is_ever_a_pass(regime):
    verdict = _translate(_result(regime))
    assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH
    assert verdict.blocking()
    assert "not a pass" in verdict.reason


class _ElementwiseLike:
    """Stands in for a one-element numpy array: == and != answer something that
    is falsy both ways, so a plain comparison cannot tell it from STABLE."""

    def __eq__(self, other):
        return [False]

    def __ne__(self, other):
        return [False]

    __hash__ = None


class _RaisesOnCompare:
    """Stands in for a two-element numpy array, whose truth value is an error."""

    def __eq__(self, other):
        raise ValueError("the truth value of an array is ambiguous")

    __ne__ = __eq__
    __hash__ = None


@pytest.mark.parametrize("regime", [_ElementwiseLike(), _RaisesOnCompare()])
def test_a_regime_that_is_not_a_str_is_refused_however_it_compares(regime):
    verdict = _translate(_result(regime))
    assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH
    assert "not a pass" in verdict.reason


def test_a_numpy_array_regime_is_refused_not_passed_and_not_an_error():
    np = pytest.importorskip("numpy")
    for regime in (np.array(["STABLE"]), np.array(["STABLE", "STABLE"]), np.str_("STABLE")):
        verdict = _translate(_result(regime))
        assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH, regime


def test_a_str_subclass_is_not_the_exact_string_stable():
    class Sneaky(str):
        def __ne__(self, other):
            return False

    verdict = _translate(_result(Sneaky("anything")))
    assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH


def test_a_result_with_no_regime_is_not_a_pass():
    no_regime = {k: v for k, v in _result("STABLE").items() if k != "regime"}
    assert _translate(no_regime).outcome is cns_gate.GateOutcome.TERMINAL_BREACH
    only_config = {"config": STABLE_CFG.as_dict()}
    assert _translate(only_config).outcome is cns_gate.GateOutcome.TERMINAL_BREACH


@pytest.mark.parametrize(
    "overrides",
    [
        {"distortion": float("nan")},
        {"distortion": float("inf")},
        {"final_state": float("nan")},
        {"final_state": float("-inf")},
        {"distortion": None},
        {"final_state": "100"},
        {"distortion": True},
    ],
)
def test_a_stable_regime_over_non_finite_numbers_is_not_a_pass(overrides):
    """RegimeEngine.classify compares with >, so NaN falls through to STABLE."""
    assert kernel.RegimeEngine.classify(float("nan"), float("nan")) == "STABLE"
    verdict = _translate(_result("STABLE", **overrides))
    assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH


def test_the_stable_distortion_bound_is_the_kernels_own():
    """STABLE_MAX_DISTORTION is mirrored from RegimeEngine.classify; if the
    kernel moves its threshold this fails instead of the connector drifting."""
    top = cns_connector.STABLE_MAX_DISTORTION
    assert kernel.RegimeEngine.classify(0.0, top) == "STABLE"
    assert kernel.RegimeEngine.classify(0.0, math.nextafter(top, 1.0)) != "STABLE"


@pytest.mark.parametrize("distortion", [0.0, 0.2, 0.35])
def test_a_stable_result_inside_the_stable_distortion_range_passes(distortion):
    verdict = _translate(_result("STABLE", distortion=distortion))
    assert verdict.outcome is cns_gate.GateOutcome.PASS


@pytest.mark.parametrize(
    "distortion", [0.36, math.nextafter(0.35, 1.0), 0.65, 0.8, 0.95, 5.0, -0.01, -1.0]
)
def test_a_stable_label_over_a_distortion_stable_cannot_have_is_not_a_pass(distortion):
    """STABLE means distortion 0 to 0.35. A label over 0.95 or -1.0 is not the
    result of the simulation, and a distortion over 0.8 is a veto elsewhere."""
    verdict = _translate(_result("STABLE", distortion=distortion))
    assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH
    assert "outside what STABLE allows" in verdict.reason


def test_a_stable_result_missing_its_numbers_is_not_a_pass():
    assert _translate({"regime": "STABLE", "config": STABLE_CFG.as_dict()}).blocking()


def test_a_reason_is_built_even_from_a_malformed_result():
    result = _result("UNSTABLE", UNSTABLE_CFG)
    result["distortion"] = "high"
    verdict = _translate(result, UNSTABLE_CFG)
    assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH
    assert "'high'" in verdict.reason


def test_a_non_mapping_result_is_a_type_error():
    with pytest.raises(TypeError):
        _translate("STABLE")


# ---------------------------------------------------------------------------
# A result is only ever read against the scenario it records
# ---------------------------------------------------------------------------

OTHER_CFG = SimulationConfig(seed=0, initial_state=-500.0, initial_target=1000.0, shifted_target=2000.0)


def test_noise_scale_is_required_because_a_result_does_not_record_it():
    param = inspect.signature(to_cns_result).parameters["noise_scale"]
    assert param.default is inspect.Parameter.empty
    assert param.kind is inspect.Parameter.KEYWORD_ONLY
    assert "noise_scale" not in _native(STABLE_CFG, 4.0)
    with pytest.raises(TypeError):
        to_cns_result(_native(STABLE_CFG, 4.0), STABLE_CFG)


def test_a_result_is_refused_for_a_scenario_it_was_not_produced_from():
    """A STABLE result for one scenario must not become a PASS on another, even
    one AUGUR itself would refuse (screen_to_cns gives TERMINAL_BREACH for it)."""
    stable = _native(STABLE_CFG, 4.0)
    assert stable["regime"] == "STABLE"
    assert screen_to_cns(OTHER_CFG, noise_scale=HARD_NOISE).blocking()
    with pytest.raises(ValueError, match="does not record this scenario"):
        to_cns_result(stable, OTHER_CFG, noise_scale=HARD_NOISE)
    # The same result still translates for the scenario it records.
    assert to_cns_result(stable, STABLE_CFG, noise_scale=4.0).outcome is cns_gate.GateOutcome.PASS


@pytest.mark.parametrize(
    "change",
    [
        {"seed": 43},
        {"initial_state": 61.0},
        {"initial_target": 101.0},
        {"shifted_target": 141.0},
        {"total_steps": 61},
        {"state_decay": 0.98},
        {"volatility_window": 11},
        {"target_shift_step": 31},
    ],
)
def test_a_result_is_refused_when_any_field_of_its_scenario_differs(change):
    stable = _native(STABLE_CFG, 4.0)
    other = SimulationConfig(**{**STABLE_CFG.as_dict(), **change})
    with pytest.raises(ValueError):
        to_cns_result(stable, other, noise_scale=4.0)


def test_a_result_is_refused_when_the_scenario_was_edited_after_the_run():
    cfg = SimulationConfig(seed=42)
    stable = _native(cfg, 4.0)
    cfg.initial_state = -500.0
    with pytest.raises(ValueError):
        to_cns_result(stable, cfg, noise_scale=4.0)


@pytest.mark.parametrize("recorded", [None, "config", [], {}, {"seed": 42}])
def test_a_result_that_records_no_usable_scenario_is_refused(recorded):
    result = _result("STABLE")
    if recorded is None:
        del result["config"]
    else:
        result["config"] = recorded
    with pytest.raises(ValueError):
        _translate(result)


def test_a_non_finite_scenario_is_refused_before_its_result_is_compared():
    cfg = SimulationConfig(seed=1, initial_state=float("nan"))
    recorded = {**cfg.as_dict(), "initial_state": float("nan")}  # a different NaN object
    result = {**_result("STABLE", cfg), "config": recorded}
    verdict = to_cns_result(result, cfg, noise_scale=4.0)
    assert verdict.outcome is cns_gate.GateOutcome.RETRY
    assert verdict.binds("scenario", scenario_digest(cfg, 4.0))


def test_an_invalid_scenario_is_refused_whatever_result_comes_with_it():
    """A hand-made result must not give an invalid scenario a pass."""
    cfg = SimulationConfig(seed=1, total_steps=-5)
    forged = {**_result("STABLE", cfg), "config": cfg.as_dict()}
    verdict = to_cns_result(forged, cfg, noise_scale=4.0)
    assert verdict.outcome is cns_gate.GateOutcome.RETRY
    assert "total_steps must be positive" in verdict.reason
    assert verdict.binds("scenario", scenario_digest(cfg, 4.0))
    # And the same for a stable result recorded under some other scenario.
    assert to_cns_result(_native(STABLE_CFG, 4.0), cfg, noise_scale=4.0).blocking()


# ---------------------------------------------------------------------------
# Agreement with the repo's own decision
# ---------------------------------------------------------------------------


def test_the_connector_agrees_with_augurs_own_regime_on_every_sample():
    """The translation must not change what AUGUR decided."""
    for cfg, noise in SAMPLES:
        native = _native(cfg, noise)["regime"]
        verdict = screen_to_cns(cfg, noise_scale=noise)
        outcome = cns_gate.resolve([verdict])
        assert (verdict.outcome is cns_gate.GateOutcome.PASS) is (native == "STABLE"), native
        assert verdict.blocking() is (native in ("UNSTABLE", "CRITICAL")), native
        if native == "STABLE":
            assert outcome is cns_gate.GateOutcome.PASS
        else:
            assert outcome is cns_gate.GateOutcome.TERMINAL_BREACH
        assert native in verdict.reason


def test_translating_a_native_result_gives_the_same_verdict_as_screening():
    for cfg, noise in SAMPLES:
        assert to_cns_result(_native(cfg, noise), cfg, noise_scale=noise) == screen_to_cns(
            cfg, noise_scale=noise
        )


def test_the_connector_leaves_the_native_result_unchanged():
    for cfg, noise in SAMPLES:
        before = _native(cfg, noise)
        screen_to_cns(cfg, noise_scale=noise)
        assert _native(cfg, noise) == before


def test_the_connector_never_overrules_a_real_run_on_a_wider_sweep():
    """The input checks only ever add refusals for scenarios that cannot be
    screened; for a runnable seeded scenario the outcome is AUGUR's own regime,
    including every STABLE the distortion check could have refused."""
    seen = set()
    for noise in (4.0, 12.0, 30.0):
        for extra in ({}, HARD, {"total_steps": 20}):
            for seed in range(0, 70, 3):
                cfg = SimulationConfig(seed=seed, **extra)
                native = _native(cfg, noise)
                verdict = screen_to_cns(cfg, noise_scale=noise)
                seen.add(native["regime"])
                assert (verdict.outcome is cns_gate.GateOutcome.PASS) is (
                    native["regime"] == "STABLE"
                ), (seed, noise, extra)
                assert verdict.blocking() is (native["regime"] != "STABLE")
                assert verdict.outcome is not cns_gate.GateOutcome.RETRY
                if native["regime"] == "STABLE":
                    assert 0.0 <= native["distortion"] <= cns_connector.STABLE_MAX_DISTORTION
    assert seen == {"STABLE", "UNSTABLE", "CRITICAL"}


def test_there_is_no_default_scenario_to_screen():
    """A forgotten scenario must not read as a pass (the default one is not
    even seeded, so it is not screenable)."""
    with pytest.raises(TypeError):
        screen_to_cns()
    for forgotten in (None, {}, "scenario", 42):
        with pytest.raises(TypeError):
            screen_to_cns(forgotten)
    assert screen_to_cns(SimulationConfig()).outcome is cns_gate.GateOutcome.RETRY


def test_the_default_noise_scale_run_is_what_the_default_binds(monkeypatch):
    seen = {}

    def spy(config, noise_scale, record_history):
        seen.update(config=config, noise_scale=noise_scale, record_history=record_history)
        return _result("STABLE")

    monkeypatch.setattr(cns_connector, "run_simulation", spy)
    verdict = screen_to_cns(STABLE_CFG)
    assert seen["noise_scale"] == 4.0
    assert verdict.binds("scenario", scenario_digest(STABLE_CFG))


def test_the_connector_never_adds_an_approval_beyond_no_objection():
    """Whatever a run does, the only non-blocking verdict is PASS for STABLE."""
    for cfg, noise in SAMPLES:
        verdict = screen_to_cns(cfg, noise_scale=noise)
        if not verdict.blocking():
            assert verdict.outcome is cns_gate.GateOutcome.PASS
            assert _native(cfg, noise)["regime"] == "STABLE"


# ---------------------------------------------------------------------------
# Binding to what was judged
# ---------------------------------------------------------------------------


def test_every_verdict_is_bound_to_the_scenario_it_judged():
    verdicts = [screen_to_cns(c, noise_scale=n, subject="plan-1") for c, n in SAMPLES]
    assert cns_gate.unbound(verdicts) == ()
    for (cfg, noise), verdict in zip(SAMPLES, verdicts):
        assert verdict.bound()
        assert verdict.binds("plan-1", scenario_digest(cfg, noise))


def test_a_verdict_does_not_bind_to_a_different_scenario_label_or_noise():
    verdict = screen_to_cns(UNSTABLE_CFG, noise_scale=HARD_NOISE, subject="plan-1")
    digest = scenario_digest(UNSTABLE_CFG, HARD_NOISE)
    assert verdict.binds("plan-1", digest)
    # Transplanted onto a different scenario.
    assert not verdict.binds("plan-1", scenario_digest(STABLE_CFG, HARD_NOISE))
    assert not verdict.binds("plan-1", scenario_digest(SimulationConfig(seed=1, **HARD), HARD_NOISE))
    # The same scenario under a different noise scale is a different judgement.
    assert not verdict.binds("plan-1", scenario_digest(UNSTABLE_CFG, HARD_NOISE + 1.0))
    # A different subject label.
    assert not verdict.binds("plan-2", digest)


def test_every_field_of_the_scenario_changes_the_digest():
    base = SimulationConfig(seed=1, total_steps=40)
    digests = {scenario_digest(base)}
    for change in (
        {"initial_state": 61.0},
        {"initial_target": 101.0},
        {"shifted_target": 141.0},
        {"target_shift_step": 10},
        {"total_steps": 41},
        {"state_decay": 0.98},
        {"volatility_window": 11},
        {"seed": 2},
        {"seed": None},
    ):
        fields = {**base.as_dict(), **change}
        digests.add(scenario_digest(SimulationConfig(**fields)))
    assert len(digests) == 10


def test_the_digest_is_stable_across_calls_and_processes():
    """Pinned: a change to the bound content is a change to the contract."""
    assert scenario_digest(SimulationConfig(seed=42)) == scenario_digest(SimulationConfig(seed=42))
    assert scenario_digest(SimulationConfig(seed=42)) == (
        "ee4cadbf56e5921bb4b5652ab387e20e8cb19d4f05376a5ef4db268cabb3c851"
    )


def test_a_float_subclass_binds_like_the_float_it_is():
    class Wide(float):
        def __repr__(self):
            return f"Wide({float(self)})"

    assert scenario_digest(SimulationConfig(seed=1, initial_state=Wide(60.0))) == (
        scenario_digest(SimulationConfig(seed=1, initial_state=60.0))
    )


# ---------------------------------------------------------------------------
# What the repo refuses or cannot decide is never a pass
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"total_steps": 0}, "total_steps must be positive"),
        ({"total_steps": -5}, "total_steps must be positive"),
        ({"state_decay": 1.5}, "state_decay must be in"),
        ({"state_decay": 0.0}, "state_decay must be in"),
        ({"state_decay": float("nan")}, "state_decay must be in"),
        ({"volatility_window": 1}, "volatility_window must be at least 2"),
        ({"total_steps": 10, "target_shift_step": 50}, "must fall inside the run"),
        ({"total_steps": "60", "target_shift_step": None}, "not supported"),
    ],
)
def test_an_invalid_scenario_is_a_retry_carrying_the_repos_own_reason(kwargs, message):
    cfg = SimulationConfig(seed=1, **kwargs)
    # The repo itself refuses this scenario...
    with pytest.raises((ValueError, TypeError)):
        run_simulation(cfg)
    # ...and the connector reports that refusal, never a pass.
    verdict = screen_to_cns(cfg)
    assert verdict.outcome is cns_gate.GateOutcome.RETRY
    assert verdict.position is cns_gate.GatePosition.ALPHA
    assert verdict.blocking()
    assert message in verdict.reason
    assert verdict.bound()
    assert verdict.binds("scenario", scenario_digest(cfg))


def test_an_invalid_scenario_does_not_run_the_simulation(monkeypatch):
    def boom(*args, **kwargs):
        raise AssertionError("the simulation must not run for an invalid scenario")

    monkeypatch.setattr(cns_connector, "run_simulation", boom)
    assert screen_to_cns(SimulationConfig(total_steps=0)).outcome is cns_gate.GateOutcome.RETRY


def _must_not_run(monkeypatch):
    def boom(*args, **kwargs):
        raise AssertionError("the simulation must not run for a scenario that cannot be screened")

    monkeypatch.setattr(cns_connector, "run_simulation", boom)


#: Scenarios the repo's validate() lets through but a verdict cannot rest on.
#: (kwargs, noise_scale, what the reason must name)
UNSCREENABLE = [
    ({"initial_state": float("nan")}, 4.0, "initial_state must be a finite number"),
    ({"initial_state": float("inf")}, 4.0, "initial_state must be a finite number"),
    ({"initial_state": float("-inf")}, 4.0, "initial_state must be a finite number"),
    ({"initial_target": float("nan")}, 4.0, "initial_target must be a finite number"),
    ({"initial_target": float("inf")}, 4.0, "initial_target must be a finite number"),
    ({"shifted_target": float("nan")}, 4.0, "shifted_target must be a finite number"),
    # Never applied (no shift), but still a NaN in the scenario: refused all the same.
    ({"shifted_target": float("nan"), "target_shift_step": None}, 4.0, "shifted_target"),
    ({"initial_state": 10**400}, 4.0, "initial_state must be a finite number"),
    ({"initial_state": "60"}, 4.0, "initial_state must be a finite number"),
    ({"initial_state": True}, 4.0, "initial_state must be a finite number"),
    ({"total_steps": 60.0}, 4.0, "total_steps must be a whole number"),
    ({"total_steps": True}, 4.0, "total_steps must be a whole number"),
    ({"volatility_window": 10.0}, 4.0, "volatility_window must be a whole number"),
    ({"target_shift_step": 3.0}, 4.0, "target_shift_step must be a whole number or None"),
    ({}, float("nan"), "noise_scale must be a finite number"),
    ({}, float("inf"), "noise_scale must be a finite number"),
    ({}, "4.0", "noise_scale must be a finite number"),
    ({"seed": None}, 4.0, "seed is not set"),
    ({"seed": -1}, 4.0, "seed must be a whole number from 0 to 4294967295"),
    ({"seed": 2**32}, 4.0, "seed must be a whole number from 0 to 4294967295"),
    ({"seed": 2**40}, 4.0, "seed must be a whole number from 0 to 4294967295"),
    ({"seed": 1.5}, 4.0, "seed must be a whole number from 0 to 4294967295"),
    ({"seed": 7.0}, 4.0, "seed must be a whole number from 0 to 4294967295"),
    ({"seed": True}, 4.0, "seed must be a whole number from 0 to 4294967295"),
    ({"seed": "7"}, 4.0, "seed must be a whole number from 0 to 4294967295"),
]


@pytest.mark.parametrize("kwargs, noise, message", UNSCREENABLE)
def test_a_scenario_that_cannot_be_screened_is_a_retry_and_is_not_run(
    kwargs, noise, message, monkeypatch
):
    """The same RETRY the repo's own invalid scenarios get, for the same reason:
    the reason says what to change. Nothing runs, so nothing can pass."""
    cfg = SimulationConfig(**{"seed": 1, **kwargs})
    _must_not_run(monkeypatch)
    verdict = screen_to_cns(cfg, noise_scale=noise)
    assert verdict.outcome is cns_gate.GateOutcome.RETRY
    assert verdict.position is cns_gate.GatePosition.ALPHA
    assert verdict.blocking()
    assert message in verdict.reason
    assert verdict.reason.startswith("refused: this scenario cannot be screened")
    # Still bound to exactly what was refused, NaN and infinity included.
    assert verdict.bound()
    assert verdict.binds("scenario", scenario_digest(cfg, noise))
    # A result for the scenario does not change that.
    assert to_cns_result(_result("STABLE", cfg), cfg, noise_scale=noise) == verdict


def test_the_seed_range_is_the_one_numpy_enforces():
    """The reason a seed outside 0 to 2**32 - 1 is refused: with NumPy installed
    the repo itself fails on it, without NumPy it runs, so the verdict would
    depend on the environment and the digest could not tell."""
    np = pytest.importorskip("numpy")
    for seed in (-1, 2**32, 2**40, 1.5):
        with pytest.raises((ValueError, TypeError)):
            np.random.seed(seed)
    for seed in (0, 1, 2**32 - 1):
        np.random.seed(seed)


@pytest.mark.parametrize("seed", [0, 1, 42, 2**32 - 1])
def test_every_seed_in_range_is_screened_including_zero_and_the_top(seed):
    cfg = SimulationConfig(seed=seed, total_steps=12)
    verdict = screen_to_cns(cfg)
    assert verdict.outcome is not cns_gate.GateOutcome.RETRY
    native = _native(cfg, 4.0)["regime"]
    assert (verdict.outcome is cns_gate.GateOutcome.PASS) is (native == "STABLE")


def test_an_unseeded_run_is_refused_not_screened_by_a_random_draw(monkeypatch):
    """Re-running an unseeded scenario until it passes would be approval by
    repetition, so no draw is allowed to decide: it is RETRY every time."""
    cfg = SimulationConfig(seed=None)
    result = _native(cfg, 4.0)  # a real unseeded run that came out one way or another
    _must_not_run(monkeypatch)
    verdicts = [screen_to_cns(cfg) for _ in range(5)] + [_translate(result, cfg)]
    assert {v.outcome for v in verdicts} == {cns_gate.GateOutcome.RETRY}
    assert all("seed is not set" in v.reason for v in verdicts)
    assert len({v.subject_digest for v in verdicts}) == 1
    assert all(v.binds("scenario", scenario_digest(cfg)) for v in verdicts)


def test_seed_zero_is_a_seed_not_an_unset_one():
    cfg = SimulationConfig(seed=0)
    verdict = screen_to_cns(cfg)
    assert "seed is not set" not in verdict.reason
    assert verdict.outcome is not cns_gate.GateOutcome.RETRY
    assert _translate(_native(cfg, 4.0), cfg).outcome is verdict.outcome


@pytest.mark.parametrize("noise", [1e308])
def test_a_scenario_the_simulation_errors_on_is_refused_and_still_bound(noise):
    """What the checks cannot foresee: it passed them, then failed while running."""
    cfg = SimulationConfig(seed=1)
    with pytest.raises(Exception):
        _native(cfg, noise)
    verdict = screen_to_cns(cfg, noise_scale=noise)
    assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH
    assert verdict.blocking()
    assert "did not run to a verdict" in verdict.reason
    assert verdict.bound()
    assert verdict.binds("scenario", scenario_digest(cfg, noise))


def test_non_finite_values_bind_distinctly():
    digests = {
        scenario_digest(SimulationConfig(seed=1, initial_state=v))
        for v in (float("nan"), float("inf"), float("-inf"), 60.0)
    }
    assert len(digests) == 4
    # And a tagged value cannot collide with the string it is rendered from.
    assert scenario_digest(SimulationConfig(seed=1, initial_state=float("nan"))) != (
        scenario_digest(SimulationConfig(seed=1, initial_state="nan"))
    )


def test_a_simulation_that_raises_anything_is_refused_not_passed(monkeypatch):
    for error in (RuntimeError("boom"), ZeroDivisionError("div"), KeyError("k")):
        def fail(*args, _error=error, **kwargs):
            raise _error

        monkeypatch.setattr(cns_connector, "run_simulation", fail)
        verdict = screen_to_cns(STABLE_CFG)
        assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH
        assert type(error).__name__ in verdict.reason
        assert verdict.bound()


def test_a_scenario_cns_cannot_describe_is_refused_before_anything_runs(monkeypatch):
    def boom(*args, **kwargs):
        raise AssertionError("nothing may run for a scenario that cannot be bound")

    monkeypatch.setattr(cns_connector, "run_simulation", boom)
    with pytest.raises(TypeError):
        screen_to_cns(SimulationConfig(seed=b"bytes"))


@pytest.mark.parametrize("subject", ["", " ", "\n\t"])
def test_an_empty_subject_is_refused_rather_than_issuing_an_unbound_verdict(subject, monkeypatch):
    _must_not_run(monkeypatch)
    with pytest.raises(ValueError):
        screen_to_cns(STABLE_CFG, subject=subject)
    with pytest.raises(ValueError):
        _translate(_result("STABLE"), subject=subject)
    with pytest.raises(ValueError):
        CnsGate(subject=subject)
    with pytest.raises(ValueError):
        cns_chain(subject=subject)


@pytest.mark.parametrize("subject", [None, 123, b"plan", ["plan"], 1.5])
def test_a_subject_that_is_not_a_str_is_refused(subject, monkeypatch):
    _must_not_run(monkeypatch)
    with pytest.raises(TypeError):
        screen_to_cns(STABLE_CFG, subject=subject)
    with pytest.raises(TypeError):
        _translate(_result("STABLE"), subject=subject)
    with pytest.raises(TypeError):
        CnsGate(subject=subject)
    with pytest.raises(TypeError):
        cns_chain(subject=subject)


def test_a_named_subject_is_carried_unchanged_and_bound():
    verdict = screen_to_cns(STABLE_CFG, subject="  plan 1  ")
    assert verdict.subject == "  plan 1  "
    assert verdict.bound()


def test_a_scenario_with_an_undigestible_value_raises_before_anything_runs(monkeypatch):
    """Not a fail-open: nothing is returned. numpy ints and floats are not the
    declared types, and an integer of more than 4300 digits cannot be rendered."""
    _must_not_run(monkeypatch)
    for cfg in (
        SimulationConfig(seed=1, initial_state=b"x"),
        SimulationConfig(seed=10**5000),
        SimulationConfig(seed=1, initial_state=Decimal("1.5")),
    ):
        with pytest.raises((TypeError, ValueError)):
            screen_to_cns(cfg)
    with pytest.raises((TypeError, ValueError)):
        screen_to_cns(STABLE_CFG, noise_scale=b"4")


def test_numpy_scalars_that_are_not_int_or_float_raise_and_the_plain_value_works(monkeypatch):
    np = pytest.importorskip("numpy")
    with pytest.raises(TypeError):
        screen_to_cns(STABLE_CFG, noise_scale=np.int64(4))
    with pytest.raises(TypeError):
        screen_to_cns(STABLE_CFG, noise_scale=np.float32(4.0))
    # np.float64 is a float, and the plain value binds identically.
    assert screen_to_cns(STABLE_CFG, noise_scale=np.float64(4.0)) == screen_to_cns(
        STABLE_CFG, noise_scale=4.0
    )
    assert screen_to_cns(STABLE_CFG, noise_scale=float(np.int64(4))).bound()


# ---------------------------------------------------------------------------
# Running it has the repo's own side effects, which the docs state
# ---------------------------------------------------------------------------


def test_screening_reseeds_the_global_generators_sets_the_run_id_and_appends_to_the_audit_log(
    monkeypatch,
):
    """The module docstring says so (README section 8 is pinned in
    test_cns_independence.py); if the repo stops doing this, or the docs stop
    saying it, this is where it shows."""
    monkeypatch.setenv("AUGUR_RUN_ID", "host's own value")
    random.seed(2024)
    expected_next = random.random()
    random.seed(2024)
    screen_to_cns(STABLE_CFG)
    assert random.random() != expected_next  # the host's sequence was clobbered
    assert os.environ["AUGUR_RUN_ID"] != "host's own value"
    with open(kernel._AUDIT_LOG_PATH) as log:
        assert len(log.readlines()) == STABLE_CFG.total_steps
    doc = cns_connector.__doc__
    for stated in ("reseeds", "AUGUR_RUN_ID", "audit", "augur_audit.log"):
        assert stated in doc


def test_a_scenario_that_cannot_be_screened_has_none_of_those_effects(monkeypatch):
    monkeypatch.setenv("AUGUR_RUN_ID", "host's own value")
    random.seed(2024)
    expected_next = random.random()
    random.seed(2024)
    screen_to_cns(SimulationConfig(seed=None))
    screen_to_cns(SimulationConfig(seed=1, total_steps=0))
    assert random.random() == expected_next
    assert os.environ["AUGUR_RUN_ID"] == "host's own value"
    assert not os.path.exists(kernel._AUDIT_LOG_PATH)


# ---------------------------------------------------------------------------
# The Gate protocol and the chain
# ---------------------------------------------------------------------------


def test_a_cns_gate_satisfies_the_cns_gate_protocol():
    gate = CnsGate()
    assert isinstance(gate, cns_gate.Gate)
    assert gate.name == "augur_screen"
    assert gate.position is cns_gate.GatePosition.ALPHA


def test_a_cns_gate_judges_the_same_way_as_the_screen_it_wraps():
    gate = CnsGate(noise_scale=HARD_NOISE, subject="plan-9")
    for cfg, noise in SAMPLES:
        if noise == HARD_NOISE:
            assert gate.check(cfg) == screen_to_cns(cfg, noise_scale=HARD_NOISE, subject="plan-9")


def test_a_cns_gate_binds_its_noise_scale_into_every_verdict():
    quiet = CnsGate(noise_scale=4.0).check(STABLE_CFG)
    loud = CnsGate(noise_scale=HARD_NOISE).check(STABLE_CFG)
    assert quiet.subject_digest != loud.subject_digest


@pytest.mark.parametrize(
    "candidate", [None, "scenario", b"bytes", 42, {"seed": 1}, _result("STABLE")]
)
def test_a_cns_gate_refuses_a_candidate_that_is_not_a_scenario(candidate):
    with pytest.raises(TypeError):
        CnsGate().check(candidate)


def test_the_chain_is_precondition_only_and_says_so():
    chain = cns_chain()
    assert chain.misplaced() == ()
    assert len(chain.alpha) == 1
    assert chain.omega == ()
    assert chain.complete() is False  # AUGUR has no outcome end


def test_the_chain_runs_through_cns_resolution_fail_closed():
    (gate,) = cns_chain(noise_scale=HARD_NOISE).alpha
    assert cns_gate.resolve([gate.check(UNSTABLE_CFG)]) is cns_gate.GateOutcome.TERMINAL_BREACH
    assert cns_gate.resolve([gate.check(CRITICAL_CFG)]) is cns_gate.GateOutcome.TERMINAL_BREACH
    (quiet,) = cns_chain().alpha
    assert cns_gate.resolve([quiet.check(STABLE_CFG)]) is cns_gate.GateOutcome.PASS


def test_a_pass_from_augur_does_not_outvote_another_gates_objection():
    """PASS is no objection, so anything else that objects still decides."""
    pass_verdict = screen_to_cns(STABLE_CFG)
    objection = cns_gate.GateResult(
        gate="elsewhere",
        position=cns_gate.GatePosition.OMEGA,
        outcome=cns_gate.GateOutcome.RETRY,
    )
    assert cns_gate.resolve([pass_verdict, objection]) is cns_gate.GateOutcome.RETRY
    assert cns_gate.resolve([objection, pass_verdict]) is cns_gate.GateOutcome.RETRY


def test_the_bound_content_uses_only_types_cns_accepts():
    for cfg, noise in SAMPLES:
        content = cns_connector.scenario_content(cfg, noise)
        assert cns_gate.subject_digest(content) == scenario_digest(cfg, noise)
        assert all(not (isinstance(v, float) and not math.isfinite(v)) for v in content["config"].values())
