"""
Command-line interface for AUGUR.

    python -m augur                          run the default scenario
    python -m augur --seed 42 --steps 120    reproducible longer run
    python -m augur --format json            machine-readable output
    python -m augur --format table           per-step trace
    python -m augur --config run.json        load a saved scenario

Exit codes: 0 on success, 2 on an invalid scenario, 1 on an unexpected error.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict

from .kernel import SimulationConfig, run_simulation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="augur",
        description="Run a AUGUR closed-loop behavioural simulation.",
    )

    scenario = parser.add_argument_group("scenario")
    scenario.add_argument("--initial-state", type=float, default=None,
                          help="starting value of the tracked measure (default 60.0)")
    scenario.add_argument("--target", type=float, default=None,
                          help="target value to steer toward (default 100.0)")
    scenario.add_argument("--shifted-target", type=float, default=None,
                          help="target after the shift step (default 140.0)")
    scenario.add_argument("--shift-step", type=int, default=None,
                          help="step at which the target changes (default 30)")
    scenario.add_argument("--no-shift", action="store_true",
                          help="hold the target constant for the whole run")
    scenario.add_argument("--steps", type=int, default=None,
                          help="number of steps to simulate (default 60)")
    scenario.add_argument("--decay", type=float, default=None,
                          help="per-step decay applied to the state (default 0.99)")
    scenario.add_argument("--volatility-window", type=int, default=None,
                          help="how many recent steps feed the volatility measure (default 10)")

    run = parser.add_argument_group("run")
    run.add_argument("--seed", type=int, default=None,
                     help="seed for reproducible runs; omit for a random run")
    run.add_argument("--noise", type=float, default=4.0,
                     help="scale of random disturbance per step (default 4.0)")
    run.add_argument("--config", type=str, default=None,
                     help="path to a JSON file of scenario settings")

    out = parser.add_argument_group("output")
    out.add_argument("--format", choices=["summary", "json", "table"], default="summary",
                     help="summary (default), json, or a per-step table")
    out.add_argument("--output", type=str, default=None,
                     help="write results to this file instead of the screen")

    return parser


def config_from_args(args: argparse.Namespace) -> SimulationConfig:
    """Builds a config from file defaults, then command-line overrides."""
    values: Dict[str, Any] = {}

    if args.config:
        with open(args.config) as handle:
            values.update(json.load(handle))

    overrides = {
        "initial_state": args.initial_state,
        "initial_target": args.target,
        "shifted_target": args.shifted_target,
        "target_shift_step": args.shift_step,
        "total_steps": args.steps,
        "state_decay": args.decay,
        "volatility_window": args.volatility_window,
        "seed": args.seed,
    }
    values.update({k: v for k, v in overrides.items() if v is not None})

    if args.no_shift:
        values["target_shift_step"] = None

    return SimulationConfig(**values)


def render_summary(result: Dict[str, Any]) -> str:
    cfg = result["config"]
    seed = cfg["seed"] if cfg["seed"] is not None else "none (run is not reproducible)"
    return "\n".join([
        "AUGUR simulation complete",
        "",
        f"  steps run      {result['steps_run']}",
        f"  seed           {seed}",
        f"  final state    {result['final_state']:.4f}",
        f"  target         {result['target']:.4f}",
        f"  final error    {result['final_error']:.4f}",
        f"  regime         {result['regime']}",
        f"  distortion     {result['distortion']:.4f}",
    ])


def render_table(result: Dict[str, Any]) -> str:
    if not result["history"]:
        return "No history recorded."

    header = (
        f"{'step':>5} {'state':>10} {'target':>9} {'delta':>9} "
        f"{'volatility':>11} {'agent':>6} {'regime':>9} {'frozen':>7}"
    )
    lines = [header, "-" * len(header)]
    for row in result["history"]:
        lines.append(
            f"{row['step']:>5} {row['state']:>10.3f} {row['target']:>9.2f} "
            f"{row['action_delta']:>9.3f} {row['volatility']:>11.4f} "
            f"{row['agent_index']:>6} {row['regime']:>9} "
            f"{'yes' if row['frozen'] else 'no':>7}"
        )
    lines.append("")
    lines.append(render_summary(result))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        config = config_from_args(args)
        config.validate()
    except (ValueError, TypeError) as problem:
        print(f"Invalid scenario: {problem}", file=sys.stderr)
        return 2
    except OSError as problem:
        print(f"Could not read config file: {problem}", file=sys.stderr)
        return 2

    want_history = args.format in ("json", "table")
    result = run_simulation(config, noise_scale=args.noise, record_history=want_history)

    if args.format == "json":
        rendered = json.dumps(result, indent=2)
    elif args.format == "table":
        rendered = render_table(result)
    else:
        rendered = render_summary(result)

    if args.output:
        with open(args.output, "w") as handle:
            handle.write(rendered + "\n")
        print(f"Wrote results to {args.output}")
    else:
        print(rendered)

    return 0


if __name__ == "__main__":
    sys.exit(main())
