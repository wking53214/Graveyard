"""
Tests for AUGUR.

Run with:  python -m unittest discover -s tests -v
"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from augur import Augur, SimulationConfig, run_simulation  # noqa: E402
from augur.__main__ import main  # noqa: E402


class TestSimulationConfig(unittest.TestCase):
    def test_defaults_reproduce_original_scenario(self):
        cfg = SimulationConfig()
        self.assertEqual(cfg.initial_state, 60.0)
        self.assertEqual(cfg.initial_target, 100.0)
        self.assertEqual(cfg.shifted_target, 140.0)
        self.assertEqual(cfg.target_shift_step, 30)
        self.assertEqual(cfg.total_steps, 60)
        self.assertEqual(cfg.state_decay, 0.99)

    def test_default_config_is_valid(self):
        SimulationConfig().validate()

    def test_rejects_zero_steps(self):
        with self.assertRaises(ValueError):
            SimulationConfig(total_steps=0).validate()

    def test_rejects_decay_above_one(self):
        with self.assertRaises(ValueError):
            SimulationConfig(state_decay=1.5).validate()

    def test_rejects_decay_of_zero(self):
        with self.assertRaises(ValueError):
            SimulationConfig(state_decay=0.0).validate()

    def test_rejects_volatility_window_too_small(self):
        with self.assertRaises(ValueError):
            SimulationConfig(volatility_window=1).validate()

    def test_rejects_shift_step_outside_run(self):
        with self.assertRaises(ValueError):
            SimulationConfig(total_steps=10, target_shift_step=50).validate()

    def test_none_shift_step_is_allowed(self):
        SimulationConfig(target_shift_step=None).validate()

    def test_as_dict_round_trips(self):
        cfg = SimulationConfig(seed=5, total_steps=12)
        restored = SimulationConfig(**cfg.as_dict())
        self.assertEqual(restored.as_dict(), cfg.as_dict())


class TestDeterminism(unittest.TestCase):
    def test_same_seed_gives_same_result(self):
        a = run_simulation(SimulationConfig(seed=42), record_history=False)
        b = run_simulation(SimulationConfig(seed=42), record_history=False)
        self.assertEqual(a["final_state"], b["final_state"])

    def test_different_seeds_diverge(self):
        a = run_simulation(SimulationConfig(seed=42), record_history=False)
        b = run_simulation(SimulationConfig(seed=7), record_history=False)
        self.assertNotEqual(a["final_state"], b["final_state"])

    def test_history_is_reproducible(self):
        a = run_simulation(SimulationConfig(seed=3, total_steps=15))
        b = run_simulation(SimulationConfig(seed=3, total_steps=15))
        self.assertEqual(
            [r["state"] for r in a["history"]],
            [r["state"] for r in b["history"]],
        )


class TestResultShape(unittest.TestCase):
    def setUp(self):
        self.result = run_simulation(SimulationConfig(seed=1, total_steps=10))

    def test_reports_every_expected_field(self):
        for key in ("final_state", "regime", "distortion", "target",
                    "final_error", "steps_run", "config", "history"):
            self.assertIn(key, self.result)

    def test_history_length_matches_steps(self):
        self.assertEqual(len(self.result["history"]), 10)
        self.assertEqual(self.result["steps_run"], 10)

    def test_history_rows_are_complete(self):
        for key in ("step", "state", "target", "regime", "distortion",
                    "volatility", "agent_index", "action_delta", "frozen"):
            self.assertIn(key, self.result["history"][0])

    def test_history_can_be_suppressed(self):
        quiet = run_simulation(SimulationConfig(seed=1, total_steps=10),
                               record_history=False)
        self.assertEqual(quiet["history"], [])

    def test_result_is_json_serialisable(self):
        json.dumps(self.result)

    def test_final_error_matches_state_and_target(self):
        expected = abs(self.result["target"] - self.result["final_state"])
        self.assertAlmostEqual(self.result["final_error"], expected, places=9)

    def test_regime_is_a_known_value(self):
        self.assertIn(self.result["regime"], {"STABLE", "UNSTABLE", "CRITICAL"})


class TestScenarioBehaviour(unittest.TestCase):
    def test_target_shifts_at_the_configured_step(self):
        cfg = SimulationConfig(seed=1, total_steps=20, target_shift_step=10,
                               initial_target=100.0, shifted_target=200.0)
        history = run_simulation(cfg)["history"]
        self.assertEqual(history[9]["target"], 100.0)
        self.assertEqual(history[10]["target"], 200.0)

    def test_target_holds_when_shift_disabled(self):
        cfg = SimulationConfig(seed=1, total_steps=20, target_shift_step=None,
                               initial_target=100.0)
        targets = {r["target"] for r in run_simulation(cfg)["history"]}
        self.assertEqual(targets, {100.0})

    def test_custom_starting_point_is_respected(self):
        cfg = SimulationConfig(seed=1, total_steps=5, initial_state=0.0,
                               initial_target=50.0, target_shift_step=None)
        result = run_simulation(cfg)
        self.assertEqual(result["config"]["initial_state"], 0.0)
        self.assertNotEqual(result["final_state"], 0.0)

    def test_zero_noise_is_accepted(self):
        result = run_simulation(SimulationConfig(seed=1, total_steps=5),
                                noise_scale=0.0, record_history=False)
        self.assertIsInstance(result["final_state"], float)


class TestFortressDirectUse(unittest.TestCase):
    def test_kernel_can_be_driven_directly(self):
        kernel = Augur(operational_seed=11)
        result = kernel.run_cycle(config=SimulationConfig(total_steps=8))
        self.assertEqual(result["steps_run"], 8)

    def test_run_cycle_defaults_to_original_scenario(self):
        result = Augur(operational_seed=11).run_cycle(record_history=False)
        self.assertEqual(result["steps_run"], 60)
        self.assertEqual(result["target"], 140.0)


class TestCommandLine(unittest.TestCase):
    def test_default_run_succeeds(self):
        self.assertEqual(main(["--seed", "42"]), 0)

    def test_json_format_succeeds(self):
        self.assertEqual(main(["--seed", "42", "--steps", "3",
                               "--format", "json"]), 0)

    def test_table_format_succeeds(self):
        self.assertEqual(main(["--seed", "42", "--steps", "3",
                               "--format", "table"]), 0)

    def test_short_run_does_not_trip_the_default_shift(self):
        self.assertEqual(main(["--seed", "42", "--steps", "5"]), 0)

    def test_explicitly_impossible_shift_is_rejected(self):
        self.assertEqual(main(["--steps", "10", "--shift-step", "99"]), 2)

    def test_zero_steps_is_rejected(self):
        self.assertEqual(main(["--steps", "0"]), 2)

    def test_missing_config_file_is_reported(self):
        self.assertEqual(main(["--config", "/nonexistent/path.json"]), 2)

    def test_config_file_is_loaded(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump({"total_steps": 7, "target_shift_step": None, "seed": 2}, handle)
            path = handle.name
        try:
            self.assertEqual(main(["--config", path, "--format", "json",
                                   "--output", path + ".out"]), 0)
            with open(path + ".out") as out:
                self.assertEqual(json.load(out)["steps_run"], 7)
        finally:
            os.unlink(path)
            if os.path.exists(path + ".out"):
                os.unlink(path + ".out")

    def test_command_line_overrides_config_file(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump({"total_steps": 7, "target_shift_step": None}, handle)
            path = handle.name
        try:
            out = path + ".out"
            self.assertEqual(main(["--config", path, "--steps", "9",
                                   "--format", "json", "--output", out]), 0)
            with open(out) as handle2:
                self.assertEqual(json.load(handle2)["steps_run"], 9)
        finally:
            os.unlink(path)
            if os.path.exists(path + ".out"):
                os.unlink(path + ".out")


if __name__ == "__main__":
    unittest.main()
