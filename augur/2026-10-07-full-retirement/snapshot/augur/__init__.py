"""
AUGUR

A standalone closed-loop behavioural simulation kernel.

Plainly: a single scalar measure (a KPI) is steered toward a moving target
over a configurable number of steps by one of three fixed-gain controllers,
chosen by a policy that learns from how well each one did. Guardrails clamp
each proposed change and can freeze learning when the system misbehaves.

Library use:

    from augur import run_simulation, SimulationConfig
    result = run_simulation(SimulationConfig(seed=42))
    result["final_state"], result["history"]

Command-line use:

    python -m augur --seed 42 --steps 60 --format table

A note on naming, carried forward from the source material: docstrings in the
original artifacts referenced Echo State Network reservoirs and Lyapunov
stability engines. Neither is implemented. The real mechanisms are tanh-based
linear layers and a rolling standard deviation used as a volatility proxy.
Treat the original naming as marketing, not specification.
"""

from .kernel import (  # noqa: F401
    Augur,
    Payload,
    SimulationConfig,
    audit_append,
    run_simulation,
    safe_stdev,
    set_global_seed,
)

__all__ = [
    "Augur",
    "Payload",
    "SimulationConfig",
    "run_simulation",
    "set_global_seed",
    "safe_stdev",
    "audit_append",
]

__version__ = "1.0.0"
