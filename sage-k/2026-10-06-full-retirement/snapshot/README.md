# SAGE-K

**S.A.G.E.-K. — Streaming Adaptive Governance & Ensemble Kernel.**

This repository is a reconstruction of SAGE-K at its most developed historical
state, rebuilt from conversation archives after the original repository was
lost. See `RECONSTRUCTION.md` for the evidence trail, what was recovered from
where, and every point where this copy knowingly differs from the original.

The repo holds two subsystems that share a package but not a single line of
code. That separation is real, it was in the original, and it is load-bearing
for understanding what you are looking at.

---

## Subsystem A — interpretation (`sage_k/__init__.py` surface)

How a governance system keeps applying the reading it was given.

Regulations are not black and white. Where one is genuinely open, a business
picks a reading. This subsystem is what makes that reading auditable: it probes
the decision system with concrete situations every month and reports whether
the answers still match what Legal locked in.

The loop:

1. A model writes candidate scenarios on the boundaries of declared ambiguity
   zones — `generator.py`
2. Legal approves or rejects each one, and in approving it **locks** the correct
   answer. Nothing runs unapproved — `scenarios.py`
3. Monthly, approved scenarios are posed to the system and every outcome is
   recorded, including refusals — `harness.py`
4. Results are grouped by zone and compared against tolerances the business
   set, so drift is localized rather than vague — `drift.py`
5. Annually, humans decide whether the reading still holds, and the decision is
   sealed with its evidence — `realignment.py`
6. Everything renders as documents people can read — `report.py`

The load-bearing constraint: **AI generates and humans decide.** A model
suggestion is never an authoritative answer, and no scenario is ever scored
against a machine-supplied expectation.

Properties the test suite actually pins down, each one a way the subsystem
could quietly stop being trustworthy:

- an unapproved scenario running
- an approved scenario being edited after the fact
- a model's opinion becoming the graded answer
- refusals inflating or deflating the score
- an empty zone reporting perfect health
- a sealed annual record being altered after sign-off
- multi-year slippage hiding inside individually acceptable years

Run it end to end, no network and no database:

```bash
PYTHONPATH=. python3 -m sage_k.demo
```

That walks five years of one regulation, which is where multi-year slippage
becomes visible — the part that is hard to see from a single month's output.

## Subsystem B — kernel, adapter, extractor

Three components archived from a single Gemini chat transcript (see
`PROVENANCE.md` and `docs/GEMINI_SOURCE_RECORD.md`). None of the original
artifacts ran as-is. This restructures the same logic into importable modules,
with the defects fixed and documented.

**`sage_k/kernel.py` — S.A.G.E.-K. / "Fortress"**
A closed-loop toy simulation: a scalar KPI is nudged from 60 toward a target
(100, then 140 halfway through) over 60 steps, by one of three fixed-gain
linear controllers chosen by a softmax policy. Guardrail classes
(`IntegrityLayer`, `InvariantMonitor`, `DriftMonitor`, `MandateLayer`) clamp
actions and can freeze the policy if the state misbehaves.

Despite the original docstring naming ("Echo State Network reservoirs,"
"Lyapunov Stability Engines"), there is no ESN and no Lyapunov exponent
calculation anywhere in the code — just `tanh`-based linear layers and a
rolling standard deviation used as a volatility proxy. Read the class names as
labels, not as a spec.

**`sage_k/gsa_adapter.py` — the "GSA" wrapper**
A generic adapter that wraps any module exposing `execute_governance_logic` /
`execute_governance_module` and chains a deterministic SHA-256 hash over each
step's JSON-serialized state. This is integrity and ordering tamper-evidence,
**not encryption** — it has no confidentiality property and manages no keys.
"Cryptographic interlock" is marketing language for a hash chain.

**`sage_k/graph_extractor.py` — AST call-graph extractor**
Unrelated to the kernel (a second, separate snippet from the same chat). Walks
a Python source string with the stdlib `ast` module and records
module/function/class/import nodes and `CALL` edges by name. Straightforward
and does what it says; call resolution is name-based rather than type-aware.

---

## Running it

No third-party runtime dependencies; standard library only. NumPy is used
opportunistically for seeding if present, but is never required. `pytest` is
needed only to run the tests.

```bash
pip install -e .          # or just add this directory to PYTHONPATH

python3 -m sage_k.demo                          # interpretation loop, 5 years
python3 examples/run_kernel_stress_test.py      # kernel alone, 20 runs
python3 examples/run_wrapped_kernel_demo.py     # kernel through the GSA adapter
python3 examples/run_graph_extractor_demo.py    # AST extractor, direct + wrapped

python3 -m pytest tests/ -q                     # 57 tests
```

`examples/run_kernel_stress_test.py` is the reproducibility check. It is seeded
and must print exactly:

```
=== DUAL PHASE RESULTS ===
GREEN : 20
YELLOW: 0
RED   : 0
```

That is the same output recorded against the original repository, and it is how
this reconstruction was verified behaviourally rather than just structurally.

## Layout

```
sage_k/
  __init__.py          package facade (exports subsystem A only -- see note)
  scenarios.py         Scenario, lifecycle, hash binding, ScenarioLibrary
  generator.py         ScenarioGenerator, ModelClient protocol, StubModelClient
  harness.py           TestHarness, TestRun, ScenarioResult, Resolver protocol
  drift.py             DriftAnalyzer, ZoneDrift, ToleranceConfig, calibration
  realignment.py       RealignmentRecord, RealignmentTrail, Approver, events
  report.py            monthly_drift_report, annual_realignment_report
  demo.py              full five-year interpretation walkthrough
  kernel.py            Fortress / S.A.G.E.-K. simulation
  gsa_adapter.py       envelope, hash chain, adapter, temporal doorway gate
  graph_extractor.py   AST call-graph extractor (independent of kernel.py)
examples/
  run_kernel_stress_test.py
  run_wrapped_kernel_demo.py
  run_graph_extractor_demo.py
tests/
  test_sanity.py           subsystem B: 4 tests
  test_interpretation.py   subsystem A: 39 governance-property tests
  test_audit_key.py        subsystem B: 14 audit-key tests (key source, production gate, warnings)
docs/
  SEAM_INVENTORY.md        39-seam boundary analysis of the original repo
  GEMINI_SOURCE_RECORD.md  recovered Gemini source record for subsystem B
PROVENANCE.md              where each part came from
RECONSTRUCTION.md          how this copy was rebuilt, and its known divergences
```

**Note on the package facade.** `import sage_k` exposes subsystem A only;
`kernel`, `gsa_adapter` and `graph_extractor` must be imported as submodules
(`from sage_k.kernel import Fortress`). This is faithful to the original and is
catalogued as seam **S1** in `docs/SEAM_INVENTORY.md`, which found no evidence
that the exclusion was intentional. It was left as-found rather than silently
changed; `RECONSTRUCTION.md` explains the reasoning.
