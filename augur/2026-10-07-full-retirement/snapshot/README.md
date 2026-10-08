# AUGUR

Optional **pre-execution behavioural simulation screen**. Veto-only: may refuse; may **never** approve. Renamed from FORTRESS (2026-09-07) to avoid collision with [`fortress-kernel`](https://github.com/wking53214/fortress-kernel).

## 1. Pipeline Position & Role

**OPTIONAL SCREEN** on the live path, only when observe-perceive `simulation_screen=True`. Not a standalone product.

```text
… PERCEIVE → [AUGUR veto] → Conservation → Execution …
```

## 2. Full System Scope & Architectural Depth

Closed-loop seeded simulation: controllers + a learning-policy sketch. HMAC audit log of refusals. Package `augur/` (`kernel.py`, `predictive_controller.py`). `_archive/` holds unrepaired prior names (`fortress_orchestrator_incomplete.txt`, `predictive_state_controller_unrepaired.txt`).

34 core tests, numpy. Passes with no sibling present and with `cns` absent.

`python -m unittest discover -s tests` runs those 34 core tests and none of the CNS tests (with `cns` absent it also reports the connected module as one skip). The CNS tests are pytest-style, so run them with `pytest` (`pip install 'augur[dev]'`). With `cns` absent: 45 passed and 1 skipped (the connected module, skipped as a whole). With `cns` installed: 195 passed and 3 skipped (the three checks that need numpy); with numpy as well, 198 passed.

## 3. What It Does NOT Do / Non-Goals

- Cannot approve. Absence of veto is not authorization.
- Not a digital twin of a customer environment.
- Not fortress-kernel (containment/slew), not CCC (recurrence).

## 4. Brutally Honest Current Status & Gaps

Commercial red team: **FEATURE**, crowded category (scenario simulators). Unfrozen 2026-09-11; findings not superseded. Predictive controller recovered from incomplete sources. Uncalibrated simulation constants. Not evidence that "what if" matches production dynamics.

## 5. Core Invariants & Guarantees

Veto-only. Seeded determinism for the shipped tests. HMAC audit of screen outcomes (integrity, not authenticity without key control).

**Audit key.** The log (`augur_audit.log`, or `AUGUR_AUDIT_LOG`) is signed with `AUGUR_AUDIT_KEY`. Set it to a unique secret if the log must be verifiable later. Unset or empty: a random per-process key is used and a `RuntimeWarning` says the log is verifiable only inside that process. With `AUGUR_ENV=production` (exact value), a missing or empty key, or the old public default `development-key`, stops the import with a `RuntimeError`; outside production that literal is accepted with a warning.

## 6. Inputs, Outputs & Type Contracts

Adapter: observe-perceive `augur_screen_adapter.py`. Refusal types live in `augur/kernel.py`. Extra `chain` pin: `augur @ git+…/AUGUR@9e24dab5`.

## 7. Stack Integration Topology

```text
observe-perceive --(opt)--> AUGUR  --veto--> halt
                           --no veto--> Conservation (still required)
fortress-kernel is a different extra (`fortress`)
```

## 8. Connecting to CNS (optional)

AUGUR stands alone: no runtime dependency, and the whole suite passes without
CNS installed. If CNS is present, `augur.cns_connector` expresses the screen's
verdict as a CNS gate result so it can be resolved alongside gates from other
repositories.

```
pip install 'augur[cns]'
```

```python
from augur import SimulationConfig
from augur.cns_connector import screen_to_cns
from cns.gate import resolve

verdict = screen_to_cns(SimulationConfig(seed=42), subject="plan-1")
resolve([verdict])       # PASS, RETRY or TERMINAL_BREACH, fail-closed
```

| AUGUR | CNS |
|---|---|
| where it judges | `ALPHA`: a pre-execution screen, so a refusal means the action never starts. AUGUR has no outcome end and the connector does not invent one, so `cns_chain().complete()` is `False` by design. |
| regime `STABLE` | `PASS`, which means only that AUGUR raised no objection. Absence of veto is not authorization, and AUGUR still cannot approve; the reason says so, and says that only the last step was judged. |
| regime `UNSTABLE` or `CRITICAL` | `TERMINAL_BREACH`. AUGUR models no repair or re-attempt, and re-running a simulation until it looks favourable would turn a veto into an approval by repetition. |
| a scenario that cannot be screened | `RETRY`, before anything runs, with a reason that says what to change. That is a scenario `SimulationConfig.validate` rejects (in the repo's own words), or one the connector will not judge because the verdict could not be reproduced from it: a number that is not finite, a field of the wrong type, an unset seed, or a seed outside `0` to `2**32 - 1`. |
| the simulation errors, an unknown, missing or non-`str` regime, or `STABLE` over numbers it cannot have | `TERMINAL_BREACH`. Only the exact string `STABLE`, over a distortion from `0` to `0.35` and a finite final state, is ever a pass. |
| judged scenario | `subject` label (non-empty) plus a digest of the config and `noise_scale`. A verdict that is moved onto another scenario fails `GateResult.binds`. That is tamper-evidence, not tamper-proofing, as `cns.gate` says of itself: nothing stops a verdict being rebuilt with another digest, and someone who recomputes the digest is not detected. NaN and infinite values, which CNS refuses to digest, are bound as a tagged mapping. |

Limits, stated rather than hidden.

- **A `PASS` judges the last step only, and that is the usual case, not a corner.** The `regime` AUGUR reports is the regime at the last step of the run, so a run that was `UNSTABLE` or `CRITICAL` for much of its length and ended `STABLE` reports `STABLE`. Measured here with seeds 0 to 199 on the default scenario: at noise scale 4.0, all 200 runs spent steps outside `STABLE` and all 200 ended `STABLE`, so all 200 are a `PASS`; at noise scale 12.0, 153 of 200 ended `STABLE` and every one of those 153 had spent steps outside it. The connector follows AUGUR's verdict and does not tighten it. Whether `run_cycle` should report the worst regime instead is a decision for the owner of AUGUR, not for a translator.
- **A verdict is only as reproducible as its seed.** An unset seed is one random draw, and a seed NumPy refuses would give a different answer with and without it, so neither is screened: both are `RETRY`.
- **`to_cns_result` takes a result the caller already has.** The result records its scenario but not its `noise_scale`, so `noise_scale` is required and is bound as stated; nothing can check it. A result that records a different scenario than the one named raises `ValueError`. `screen_to_cns` runs the scenario itself and takes nobody's word.
- **Running it has AUGUR's own side effects.** `screen_to_cns` runs the real simulation. It reseeds the process-global `random` (and NumPy) generators, so a host that seeded its own does not continue its sequence; it sets `AUGUR_RUN_ID` in `os.environ`; and it appends one audit line per step (60 by default) to `augur_audit.log` in the working directory, or to `AUGUR_AUDIT_LOG` if set. A scenario refused with `RETRY` never runs and has none of these effects.

`screen_to_cns` has no default scenario: a forgotten one must not read as a pass. A `subject` that is empty or not a `str` is refused rather than issuing an unbound verdict.

Without CNS installed, the connector's functions raise `CnsNotInstalled` with
the install command. Nothing else in AUGUR changes.

Apache-2.0.
