"""Optional connector to CNS (``cns.gate``).

AUGUR is independent. It has no runtime dependency, imports nothing from CNS
when it loads, and its whole suite passes with CNS absent. This module is the
one place that knows CNS exists, and it asks for CNS only when one of its
functions is called. Without CNS installed those calls raise
:class:`CnsNotInstalled` with the install command; nothing else in AUGUR is
affected.

What connecting means
---------------------
AUGUR's own verdict is the ``regime`` of a seeded simulation (``STABLE``,
``UNSTABLE`` or ``CRITICAL``), taken at the last step of the run. CNS's shared
gate contract is ``cns.gate.GateResult`` (``gate``, ``position``, ``outcome``,
``reason``, ``subject``, ``subject_digest``). This module translates one into
the other without changing either, so a consumer that speaks CNS can put
AUGUR's screen in a :class:`cns.gate.GateChain` and resolve it alongside gates
from other repositories.

The mapping, and why
--------------------
=========================  ================================================
AUGUR                      CNS
=========================  ================================================
where it judges            ``ALPHA``. AUGUR is a pre-execution screen: a
                           refusal means the action never starts. It has no
                           outcome end, and this connector does not invent
                           one.
regime ``STABLE``          ``PASS``, which here means only that AUGUR raised
                           no objection. The README is explicit: absence of
                           veto is not authorization, and AUGUR may never
                           approve. ``cns.gate.resolve`` reads PASS the same
                           way ("nothing objected"), and the reason says so.
regime ``UNSTABLE``        ``TERMINAL_BREACH``. A predicted instability is
regime ``CRITICAL``        sufficient reason not to proceed, AUGUR models no
                           repair or re-attempt, and re-running a simulation
                           until it looks favourable would turn a veto into
                           an approval by repetition.
a scenario that cannot     ``RETRY``, before anything runs, with a reason
be screened                that says what to change. That is a scenario the
                           repo's own ``SimulationConfig.validate`` rejects
                           (in its own words), or one this connector will not
                           judge because the verdict could not be reproduced
                           from it: a number that is not finite, a field of
                           the wrong type, an unset seed, or a seed outside
                           ``0`` to ``2**32 - 1`` (NumPy refuses those, so
                           the same scenario would decide differently with
                           and without it). RETRY is the contract's
                           "re-render with an instructional delta", and a
                           corrected scenario is a different scenario with
                           its own digest, not a repetition.
the simulation errors      ``TERMINAL_BREACH``. A scenario that passed the
                           checks above still failed while running (an
                           extreme noise scale overflows, for one). No
                           verdict was reached and nothing in AUGUR says
                           what to change.
unknown or missing         ``TERMINAL_BREACH``. Only the exact ``str``
regime, or ``STABLE``      ``"STABLE"``, over a distortion from ``0`` to
over numbers it cannot     ``0.35`` and a finite final state, is ever a
have                       pass. (``RegimeEngine.classify`` compares with
                           ``>``, so a NaN would otherwise fall through to
                           ``STABLE``, and ``STABLE`` is defined as a
                           distortion of at most ``0.35``.)
judged content             ``subject`` (a non-empty label, default
                           ``"scenario"``) and ``subject_digest``, which is
                           ``cns.gate.subject_digest`` over
                           ``{"config": SimulationConfig.as_dict(),
                           "noise_scale": noise_scale}``.
=========================  ================================================

Two things about the judged content. First, ``noise_scale`` is a run
parameter that is not part of ``SimulationConfig`` but changes the result, so
it is bound too. Second, a real scenario can hold NaN or infinite floats (the
command line parses ``--initial-state nan``), which ``subject_digest``
refuses. Those values are bound as the tagged mapping
``{"non_finite_float": "nan"}``, which cannot collide with any float or
string, so a refused NaN scenario still carries a verdict bound to it. Any
other value outside ``str``, ``int``, ``float``, ``bool`` and ``None`` is
outside ``SimulationConfig``'s declared types (NumPy's integer scalars and
``float32`` are not ``int`` or ``float``: pass ``int(x)`` or ``float(x)``), and
an integer of more than 4300 digits cannot be rendered; ``subject_digest``
raises ``TypeError`` or ``ValueError`` for these, before anything runs, and
that is left to propagate.

The digest is tamper-evidence, not tamper-proofing (``cns.gate`` says the same
of itself). A verdict moved onto another scenario fails
``GateResult.binds``; nothing stops one being rebuilt with a different digest,
and someone who recomputes the digest is not detected.

What running it does
--------------------
:func:`screen_to_cns` runs the real simulation, so it has the repo's own side
effects, which a host should expect. It reseeds the process-global ``random``
(and NumPy, if installed) generators, so a host that had seeded its own does
not continue its sequence. It sets ``AUGUR_RUN_ID`` in ``os.environ``. And it
appends one HMAC-signed audit line per step (60 by default) to the audit log,
``augur_audit.log`` in the working directory unless ``AUGUR_AUDIT_LOG`` says
otherwise. None of that is new, and none of it is changed here.

Limits, stated rather than hidden
---------------------------------
The repo's ``regime`` is the regime at the *last step* of the run, and a
``PASS`` here says no more than that. A run that was ``UNSTABLE`` or
``CRITICAL`` for much of its length and ended ``STABLE`` reports ``STABLE``,
and this is the usual case, not a corner. Measured on this repo with seeds 0
to 199 on the default scenario: at noise scale 4.0 all 200 runs spent steps
in ``UNSTABLE`` or ``CRITICAL`` and all 200 ended ``STABLE``; at noise scale
12.0, 153 of 200 ended ``STABLE`` and every one of those 153 had spent steps
outside ``STABLE``. The connector follows the repo's verdict and does not
tighten it: whether ``run_cycle`` should report the worst regime is the
repo owner's decision, not a translator's, and the PASS reason says that only
the last step was judged.

A verdict can be reproduced from the bound scenario only if the scenario fixes
the seed, which is why an unset or unusable seed is refused (``RETRY``)
instead of screened. Re-running an unseeded scenario until it passes would be
approval by repetition.

:func:`to_cns_result` takes a result the caller already has. The result
records its scenario but not its ``noise_scale``, so ``noise_scale`` is
required and is bound as stated; nothing can check it. A result that records
a different scenario than the one named is refused with ``ValueError``.
:func:`screen_to_cns` runs the scenario itself and takes nobody's word.

Because AUGUR has only the precondition end, ``cns_chain(...).complete()`` is
``False`` by design. A consumer that wants a complete chain supplies the
``omega`` end from a repository that has one.

Install with the extra: ``pip install 'augur[cns]'``.
"""

from __future__ import annotations

import importlib
import math
from types import ModuleType
from typing import Any, Dict, Mapping, Tuple

from .kernel import SimulationConfig, run_simulation

__all__ = [
    "CnsGate",
    "CnsNotInstalled",
    "cns_available",
    "cns_chain",
    "scenario_content",
    "scenario_digest",
    "screen_to_cns",
    "to_cns_result",
]

INSTALL_HINT = "pip install 'augur[cns]'"

#: What ``subject`` is set to when the caller does not name the judged content.
DEFAULT_SUBJECT = "scenario"

#: The name every verdict from this connector carries in ``GateResult.gate``.
GATE_NAME = "augur_screen"

#: ``run_simulation``'s own default, bound into the digest when not overridden.
DEFAULT_NOISE_SCALE = 4.0

#: The regimes ``RegimeEngine.classify`` can return.
STABLE = "STABLE"
REFUSING_REGIMES = ("UNSTABLE", "CRITICAL")

#: ``RegimeEngine.classify`` returns ``STABLE`` only at or below this distortion
#: (and only at or above zero, since a distortion is never negative).
STABLE_MAX_DISTORTION = 0.35

#: Seeds NumPy accepts are ``0 <= seed < 2**32``. Anything else is refused here
#: so that the same bound scenario cannot decide differently with and without it.
SEED_LIMIT = 2**32

_REAL_FIELDS = ("initial_state", "initial_target", "shifted_target", "state_decay")
_INT_FIELDS = ("total_steps", "volatility_window")


class CnsNotInstalled(ImportError):
    """Raised by this module's functions when ``cns`` cannot be imported."""


def _cns_gate() -> ModuleType:
    """Import ``cns.gate`` on demand, or say exactly what is missing."""
    try:
        return importlib.import_module("cns.gate")
    except ImportError as exc:
        raise CnsNotInstalled(
            "augur.cns_connector needs the CNS package (cns.gate), which is "
            f"not installed. Install it with: {INSTALL_HINT}. AUGUR itself "
            "works without it."
        ) from exc


def cns_available() -> bool:
    """Whether the CNS gate contract can be imported in this environment."""
    try:
        _cns_gate()
    except CnsNotInstalled:
        return False
    return True


def _bindable(value: Any) -> Any:
    """``value`` as content ``subject_digest`` accepts.

    A non-finite float is refused by CNS, so it is bound as a tagged mapping
    instead. A float subclass is narrowed to ``float`` so its rendering does
    not depend on the subclass (numpy 2 renders ``np.float64(1.0)``).
    """
    if isinstance(value, float):
        value = float(value)
        if not math.isfinite(value):
            return {"non_finite_float": repr(value)}
    return value


def scenario_content(
    config: SimulationConfig, noise_scale: float = DEFAULT_NOISE_SCALE
) -> Dict[str, Any]:
    """The canonical mapping a verdict on this scenario is bound to."""
    return {
        "config": {k: _bindable(v) for k, v in config.as_dict().items()},
        "noise_scale": _bindable(noise_scale),
    }


def scenario_digest(
    config: SimulationConfig, noise_scale: float = DEFAULT_NOISE_SCALE
) -> str:
    """The digest a bound verdict on this scenario carries.

    Pass it, with the subject label, to ``GateResult.binds`` to check that a
    verdict was issued against exactly this scenario. A verdict moved onto
    another scenario fails that check; it is tamper-evidence, not proof
    against someone who recomputes the digest.
    """
    return _cns_gate().subject_digest(scenario_content(config, noise_scale))


def _finite_number(value: Any) -> bool:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:  # an int too large to be a float is not usable as one
        return False


def _whole_number(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _shown(value: Any) -> str:
    """A number for a reason string; anything else is shown as it is."""
    return f"{value:.3f}" if _finite_number(value) else repr(value)


def _checked_subject(subject: Any) -> str:
    """The label of what was judged, or a refusal to issue an unbound verdict."""
    if not isinstance(subject, str):
        raise TypeError(
            f"subject is the label of what was judged, a str; got {type(subject).__name__}"
        )
    if not subject.strip():
        raise ValueError(
            "subject must name what was judged: an empty label makes the verdict unbound"
        )
    return subject


def _scenario_problem(config: SimulationConfig, noise_scale: Any) -> str | None:
    """Why this scenario cannot be screened, in words that say what to change.

    The repo's own validation speaks first, in its own words. Then what it lets
    through but a verdict cannot rest on: a number that is not finite, a field
    of the wrong type, and a seed that does not fix the run. Only ever refuses.
    """
    try:
        config.validate()
    except (ValueError, TypeError) as exc:
        return str(exc)

    fields = config.as_dict()
    for name in _REAL_FIELDS:
        if not _finite_number(fields[name]):
            return f"{name} must be a finite number; got {fields[name]!r}"
    if not _finite_number(noise_scale):
        return f"noise_scale must be a finite number; got {noise_scale!r}"
    for name in _INT_FIELDS:
        if not _whole_number(fields[name]):
            return f"{name} must be a whole number; got {fields[name]!r}"
    shift = fields["target_shift_step"]
    if shift is not None and not _whole_number(shift):
        return f"target_shift_step must be a whole number or None; got {shift!r}"

    seed = fields["seed"]
    if seed is None:
        return (
            "seed is not set. An unseeded run is one random draw, so its verdict "
            "cannot be reproduced from the scenario it is bound to, and re-running "
            "it until it passes would be approval by repetition. Set an integer seed"
        )
    if not _whole_number(seed) or not 0 <= seed < SEED_LIMIT:
        return (
            f"seed must be a whole number from 0 to {SEED_LIMIT - 1}; got {seed!r}. "
            "NumPy refuses any other seed, so the same scenario would decide "
            "differently with and without it"
        )
    return None


def _judge(gate: ModuleType, result: Mapping[str, Any]) -> Tuple[Any, str]:
    """AUGUR's native verdict as a CNS outcome and a reason."""
    regime = result.get("regime")
    distortion = result.get("distortion")
    numbers = (
        f"final error {_shown(result.get('final_error'))}, "
        f"distortion {_shown(distortion)}"
    )
    detail = f"regime {regime!r}, {numbers}"

    # The exact str, checked by type before anything is compared: an object
    # that overrides == and != (a one-element array does) must not be able to
    # slide past both tests below.
    if type(regime) is not str:
        outcome = gate.GateOutcome.TERMINAL_BREACH
        reason = (
            f"refused: no decision. The result reports {detail}, which is not "
            "a regime AUGUR defines (a str), so it is not a pass."
        )
    elif regime in REFUSING_REGIMES:
        outcome = gate.GateOutcome.TERMINAL_BREACH
        reason = (
            f"refused: the simulation predicts regime {regime} at its last "
            f"step ({numbers}). A predicted instability is sufficient reason "
            "not to proceed, and nothing in AUGUR repairs it."
        )
    elif regime != STABLE:
        outcome = gate.GateOutcome.TERMINAL_BREACH
        reason = (
            f"refused: no decision. The result reports {detail}, which is not "
            "a regime AUGUR defines, so it is not a pass."
        )
    elif not (
        _finite_number(distortion)
        and 0.0 <= distortion <= STABLE_MAX_DISTORTION
        and _finite_number(result.get("final_state"))
    ):
        outcome = gate.GateOutcome.TERMINAL_BREACH
        reason = (
            f"refused: no decision. The result reports {detail} but its "
            "distortion or final state is missing, not finite, or outside what "
            f"STABLE allows (distortion from 0 to {STABLE_MAX_DISTORTION}), so "
            "it is not a pass."
        )
    else:
        outcome = gate.GateOutcome.PASS
        reason = (
            "no objection: the simulation ended in regime STABLE at its last "
            f"step ({numbers}). This is an absence of objection, not "
            "evidence that acting is safe. AUGUR cannot approve. Only the last "
            "step is judged: earlier steps of the run may have been UNSTABLE "
            "or CRITICAL."
        )
    return outcome, reason


def _verdict(
    gate: ModuleType, outcome: Any, reason: str, digest: str, subject: str
) -> Any:
    return gate.GateResult(
        gate=GATE_NAME,
        position=gate.GatePosition.ALPHA,
        outcome=outcome,
        reason=reason,
        subject=subject,
        subject_digest=digest,
    )


def _refusal_for(gate: ModuleType, problem: str, digest: str, subject: str) -> Any:
    return _verdict(
        gate,
        gate.GateOutcome.RETRY,
        f"refused: this scenario cannot be screened: {problem}.",
        digest,
        subject,
    )


def _belongs_to(result: Mapping[str, Any], config: SimulationConfig) -> bool:
    """Whether the result records exactly this scenario.

    A scenario with a non-finite number was refused before this is asked, so a
    NaN never has to be compared with itself here.
    """
    recorded = result.get("config")
    return isinstance(recorded, Mapping) and dict(recorded) == config.as_dict()


def to_cns_result(
    result: Mapping[str, Any],
    config: SimulationConfig,
    *,
    noise_scale: float,
    subject: str = DEFAULT_SUBJECT,
) -> Any:
    """Translate one AUGUR result into a bound ``cns.gate.GateResult``.

    ``result`` is what ``run_simulation`` returned for ``config`` and
    ``noise_scale``, and the verdict is bound to that scenario. The result
    records its config but not its noise scale, so ``noise_scale`` has no
    default: state what the run used. It cannot be checked, so a caller who
    states a different one binds the verdict to a scenario that was not
    judged; use :func:`screen_to_cns`, which runs the scenario itself, when
    nobody's word should be taken.

    Raises ``ValueError`` when ``result`` does not record exactly ``config``,
    because a verdict must not be bound to a scenario AUGUR never judged. A
    scenario that cannot be screened (see :func:`screen_to_cns`) is refused
    with ``RETRY`` from the scenario alone, whatever the result says.
    """
    gate = _cns_gate()
    if not isinstance(result, Mapping):
        raise TypeError(
            f"an AUGUR result is a mapping; got {type(result).__name__}"
        )
    if not isinstance(config, SimulationConfig):
        raise TypeError(
            f"AUGUR's screen judges a SimulationConfig; got {type(config).__name__}"
        )
    subject = _checked_subject(subject)
    digest = scenario_digest(config, noise_scale)

    problem = _scenario_problem(config, noise_scale)
    if problem is not None:
        return _refusal_for(gate, problem, digest, subject)
    if not _belongs_to(result, config):
        raise ValueError(
            "the result does not record this scenario (its config differs from "
            "config.as_dict(), or it records none), so no verdict on this "
            "scenario can be read from it"
        )
    outcome, reason = _judge(gate, result)
    return _verdict(gate, outcome, reason, digest, subject)


def screen_to_cns(
    config: SimulationConfig,
    *,
    noise_scale: float = DEFAULT_NOISE_SCALE,
    subject: str = DEFAULT_SUBJECT,
) -> Any:
    """Run AUGUR's screen over ``config`` and return its CNS verdict.

    Same simulation as :func:`augur.run_simulation`, same ``regime``; only the
    representation differs. Combine the result with ``cns.gate.resolve``.

    ``config`` is required: there is no default scenario, because a forgotten
    one must not read as a pass. A scenario that cannot be screened is refused
    with ``RETRY`` before anything runs (see the module docstring). Running it
    reseeds the global ``random`` and NumPy generators, sets ``AUGUR_RUN_ID``
    and appends to the audit log; those are the repo's own effects.
    """
    gate = _cns_gate()
    if not isinstance(config, SimulationConfig):
        raise TypeError(
            f"AUGUR's screen judges a SimulationConfig; got {type(config).__name__}"
        )
    subject = _checked_subject(subject)
    # Bind first: a scenario CNS cannot describe is refused before anything runs.
    digest = scenario_digest(config, noise_scale)

    problem = _scenario_problem(config, noise_scale)
    if problem is not None:
        return _refusal_for(gate, problem, digest, subject)

    try:
        result = run_simulation(config, noise_scale=noise_scale, record_history=False)
    except Exception as exc:  # no verdict was reached, and that must never read as a pass
        return _verdict(
            gate,
            gate.GateOutcome.TERMINAL_BREACH,
            "refused: the simulation did not run to a verdict: "
            f"{type(exc).__name__}: {exc}",
            digest,
            subject,
        )

    outcome, reason = _judge(gate, result)
    return _verdict(gate, outcome, reason, digest, subject)


class CnsGate:
    """AUGUR's screen as a gate that satisfies ``cns.gate.Gate``.

    ``check`` takes a :class:`~augur.SimulationConfig`, runs the simulation
    unchanged, and returns its verdict as a bound ``cns.gate.GateResult`` at
    the ``ALPHA`` end. ``noise_scale`` is fixed per gate because it changes the
    result and is bound into every verdict.
    """

    def __init__(
        self,
        *,
        noise_scale: float = DEFAULT_NOISE_SCALE,
        subject: str = DEFAULT_SUBJECT,
    ) -> None:
        _cns_gate()  # fail here, at construction, not on first use
        self._noise_scale = noise_scale
        self._subject = _checked_subject(subject)

    @property
    def name(self) -> str:
        return GATE_NAME

    @property
    def position(self) -> Any:
        return _cns_gate().GatePosition.ALPHA

    def check(self, candidate: object) -> Any:
        if not isinstance(candidate, SimulationConfig):
            raise TypeError(
                "AUGUR's screen judges a SimulationConfig; "
                f"got {type(candidate).__name__}"
            )
        return screen_to_cns(
            candidate, noise_scale=self._noise_scale, subject=self._subject
        )


def cns_chain(
    *,
    noise_scale: float = DEFAULT_NOISE_SCALE,
    subject: str = DEFAULT_SUBJECT,
) -> Any:
    """A ``cns.gate.GateChain`` holding AUGUR's screen in the ``alpha`` slot.

    ``omega`` stays empty: AUGUR has no outcome end.
    """
    gate = _cns_gate()
    return gate.GateChain(alpha=(CnsGate(noise_scale=noise_scale, subject=subject),))
