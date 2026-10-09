# Innovation OS: cognitive architecture investigation

Where should an AI thinking engine live in Innovation OS?

Source of record: `wking53214/innovation_os` @ `3bb189d`
Investigated: 2026-09-11
Method: repository evidence only. Evidence tags per `docs/fingerprints/README.md`.

---

## Summary

The repository already contains a package named `intelligence/` with
subpackages called `cognition/`, `reasoning/`, `knowledge/`, `memory/`,
`learning/`, `orchestration/` and `kernel/`. So the instruction not to invent a
`/thinking_engine/` is doubly right: one already exists by name.

It is scaffolding. 160 files, 4,700 lines, **zero enums, four tunables, seven
raise sites**, and a test suite of 309 tests that completes in 0.52 seconds.
`Perceiver.perceive()` returns `{"type": "perception", "input": observation}`.
`Reasoner.reason()` returns the same shape. `[EXPERIMENT + TEST, observed
2026-09-11]`

That is the bad news, and it is not the interesting finding. Three structural
facts are:

**1. Nothing depends on `intelligence/`.** Cross-boundary imports run one way
only: `intelligence/` imports from outer `innovation_os` four times; outer
`innovation_os` imports from `intelligence/` **zero** times. `[CODE]` The
cognitive layer is already a consumer-only leaf. It can be rebuilt without
destabilising anything — which is the "smallest architectural intervention"
question (handoff §16.15) already answered by the existing structure.

**2. The seam is already built, twice.** `IntelligenceRuntime` consumes
`LineageEngine` and `RetryGuardEngine`; `ArtifactRegistry` takes
`provenance_engine` and `lineage_engine` by constructor injection. `[CODE]`
Both are the pattern a cognitive engine needs. Neither needs inventing.

**3. The repository has already written down its own ownership rule, and it is
the right one.** `context_envelope/envelope.py` states that its provenance and
lineage fields are "live lookups against a ProvenanceEngine, not a second copy —
collapsing that distinction is the same three-competing-stores mistake this
codebase already paid down once." `[CODE]`

So the recommendation is not to create a cognitive layer. It is to **stop
`intelligence/` from re-creating what the outer modules already own, and let it
compose them** — because seven of its subpackages currently duplicate an outer
package by name, and the four real cross-boundary imports show what doing it
correctly looks like.

---

## A. Repository map

`[EXPERIMENT: tools/fingerprint/extract_signature.py]`

```
src/innovation_os/          351 .py files    13,879 lines    (mean 40 lines/file)
├── intelligence/           160 files         4,700 lines    (mean 29)
└── everything else         191 files         9,179 lines    (mean 48)

tests/                      169 files           629 assertions
```

64% of source files are under 40 lines. `[EXPERIMENT]`

Size is not quality, but it bounds what can be present. A 28-line module cannot
contain a retrieval strategy, and `intelligence/repository/fingerprint_engine.py`
— 28 lines returning `{path, dependencies, consumer_count}` — does not.

## B. Capability map — what actually exists

Ranked by implemented substance, not by name.

### Load-bearing (real implementation)

| Package | Lines | What it actually does |
| --- | --- | --- |
| `provenance/` | 622 | Separates *who originated* an artifact (closed Article II taxonomy) from *where it came from* (freeform locator, "carries no authority claim"). Registration without an explicit status is a `TypeError`. Status changes recorded as `StatusTransition` retaining the prior value. |
| `lineage/` | 433 | `canonicalize_artifact` + `hash_artifact` give a structure a stable identity; `record_lineage_transition`, `verify_lineage`. |
| `registry/` | 356 | `ArtifactRegistry` — composes provenance, lineage, invariants and context envelope behind one registration call. |
| `context_envelope/` | 262 | Retains speaker, temporal position, scope, conditions, qualifiers, antecedents. Explicitly refuses to duplicate provenance/lineage storage. |
| `retry_guard/` | 181 | `detect_cycle`, `allow_reentry`, `register_attempt` keyed on artifact/branch/parent/evidence/state/hash/version. Stops regeneration that produces no new evidence. |
| `invariants/` | 165 | Records `InvariantViolation` at artifact, decision, approval, branch and lifecycle boundaries. |

### Lifecycle surfaces (thin, working, mostly record-keeping)

`decision/` (318), `repository/` (292), `history/` (207), `reconstruction/`
(205), `archive/` (204), `search/` (189), `graph/` (171), `ideation/` (157).

### Scaffolding

`intelligence/` (4,700 lines / 160 files), plus `simulation/` and
`observation/` which are empty.

## C. Cognitive capability map

Against the handoff's list of cognitive primitives.

| Primitive | Where it exists | Reality |
| --- | --- | --- |
| **Provenance / identity** | `provenance/` | **Strong.** The best-implemented idea in the repository. |
| **Context** | `context_envelope/` | **Strong.** Eight context dimensions, each mapped to a specific collapse it prevents (conditional→absolute, local→global, temporary→permanent, uncertain→certain). |
| **Memory** | `memory/` (106), `intelligence/memory/` (242) | **Fragmented.** Two stores, neither durable; `storage/database.py` is 139 lines. |
| **Knowledge / graph** | `knowledge_graph/`, `graph/`, `graph_storage/`, `intelligence/knowledge/`, `intelligence/knowledge_graph.py` | **Five implementations.** `CODEX_CONTEXT.md` flags the duplication and says not to merge incidentally. `[CODE]` |
| **Retrieval** | `search/` (189), `intelligence/memory/retrieval_engine.py` | **Weak.** No index, no ranking, no embedding. |
| **Reasoning** | `reasoning/` (62), `intelligence/reasoning/` (115) | **Absent in substance.** `Reasoner.reason()` returns its input wrapped in a dict. |
| **Evaluation** | `scoring/`, `review/`, `forecast/`, `intelligence/decision/decision_scorer.py` | **Thin but present.** |
| **Decision** | `decision/` (318), `decisions/` (197), `intelligence/decision/` (139) | **Three implementations.** |
| **Planning** | `intelligence/orchestration/task_planner.py` | **Name only.** `orchestration/` totals 144 lines across 5 files. |
| **Learning** | `intelligence/learning/` (125) | **Name only.** |
| **Perception** | `intelligence/cognition/perceiver.py` | **Identity function.** |
| **Reflection** | — | **Absent.** |
| **Tool use / agent behaviour** | `intelligence/agents/` (119) | **Name only.** `capability_registry.py`, `task_router.py` are stubs. |
| **Governance** | `governance/` (127), `intelligence/governance/` (236), `review_queue/` | **Thin.** No authentication, no authorization, no policy evaluation. |
| **Orchestration** | `intelligence/kernel/cognitive_kernel.py` | **Real, and the exception.** See below. |

### The one working cognitive component

`CognitiveKernel` is a registry-and-dispatch router. It holds engines and
adapters by name, resolves one, and calls `.process(payload)` or the callable,
raising `ValueError` for an unknown engine and `TypeError` for one that cannot
execute. Its docstring states: *"Does not replace engines. Routes intelligence
between components."* `[CODE]`

That is a correct and correctly-scoped piece of architecture. It is also
approximately 45 lines, and nothing registers anything with it in production
code.

## D. Ownership map

The handoff's §15 question — "who owns this responsibility?" — has a
measurable answer, and it is currently *two owners* for seven responsibilities.

| Responsibility | Outer package | `intelligence/` counterpart | Verdict |
| --- | --- | --- | --- |
| Provenance | **622 lines** | 135 | Outer owns it. Duplicate. |
| Registry | **356** | 46 | Outer owns it. Duplicate. |
| Decision | **318** | 139 | Outer owns it (plus `decisions/`, 197). |
| Governance | 127 | 236 | Contested; neither implements policy evaluation. |
| Memory | 106 | 242 | Contested; neither is durable. |
| Knowledge graph | 64 | 125 | Contested; five implementations exist overall. |
| Reasoning | 62 | 115 | Neither implements reasoning. |
| Lineage | **433** | — | **Clean.** Single owner. |
| Context envelope | **262** | — | **Clean.** Single owner, explicitly non-duplicating. |
| Retry / oscillation | **181** | — | **Clean.** Single owner, consumed correctly. |
| Invariants | **165** | — | **Clean.** Single owner. |

The four clean rows are exactly the four packages `ArtifactRegistry` and
`IntelligenceRuntime` consume by injection. The seven contested rows are exactly
the ones `intelligence/` re-created instead of consuming.

That correlation is the finding. Where `intelligence/` consumed, ownership
stayed clean and the code became real. Where it re-created, both copies stayed
thin.

## E. Dependency graph

`[CODE]` Measured by import analysis.

```
                    outer innovation_os
                   (provenance, lineage,
                    registry, invariants,
                    context_envelope, retry_guard)
                             ▲
                             │  4 imports
                             │  (one direction only)
                             │
                      intelligence/
                   ─────────────────────
                   29 internal imports
                    0 outbound consumers
```

The four cross-boundary imports, in full:

```
intelligence/runtime/runtime.py        → innovation_os.lineage.LineageEngine
intelligence/runtime/runtime.py        → innovation_os.retry_guard.RetryGuardEngine
intelligence/system/system_factory.py  → innovation_os.retry_guard.RetryGuardEngine
intelligence/project_scan.py           → innovation_os.repository.mapper
```

**Nothing outside `intelligence/` imports anything inside it.** `[CODE]`

Two consequences, both load-bearing for the recommendation:

- `intelligence/` carries **no downstream risk**. Rebuilding it cannot break the
  rest of the repository, because the rest of the repository does not use it.
  This is the cheapest possible position from which to build a cognitive layer.
- It is also not yet wired in. Whatever gets built has to be adopted by the
  lifecycle packages before it is load-bearing.

## F. Cognitive data flow — what exists of it

Against the handoff's target chain:

```
Input → Context → Memory/Knowledge → Reasoning → Evaluation → Decision → Action → Feedback
  ✓        ✓           ~                ✗            ~           ✓         ✗         ✗
```

- **Input** — `ingest/`, `ingestion/`, `conversations/`, `importer/`, `archive/`. Present. `[CODE]`
- **Context** — `context_envelope/`. Present and well-formed. `[CODE]`
- **Memory / knowledge** — Partial and fragmented: two memory stores, five graph
  implementations, no durable persistence. `[CODE]`
- **Reasoning** — **Absent.** Identity functions. `[CODE]`
- **Evaluation** — Partial: `scoring/`, `review/`, `forecast/` exist and are thin. `[CODE]`
- **Decision** — Present in three copies, with real status transitions. `[CODE]`
- **Action** — **Absent.** No executor, no effect boundary, no tool invocation. `[CODE]`
- **Feedback** — **Absent.** `intelligence/learning/feedback_engine.py` is a stub. `[CODE]`

What the repository actually implements end-to-end is a different and narrower
chain, and it implements it well:

```
Artifact → canonical hash → provenance determination → lineage edge
        → invariant check → context envelope → registry
```

That is an **evidence custody chain**, not a cognitive cycle. It is the
repository's real spine, and it is the thing a cognitive engine here should be
built *on top of* rather than beside.

## G. Missing capability analysis

Genuinely absent, as opposed to present-but-thin:

| Missing | Notes |
| --- | --- |
| **Reasoning of any kind** | No inference rules, no chains, no causal model. `reasoning/causal_engine.py` and `reasoning_chain.py` are stubs. |
| **Retrieval** | No index, ranking, embedding, or similarity search over stored artifacts. `similarity/engine.py` exists; it is thin. |
| **Durable persistence** | `storage/database.py` is 139 lines. Everything is in-memory dataclasses. A thinking engine that forgets on restart is a calculator. |
| **Action / effect boundary** | Nothing executes anything. No tool protocol, no sandbox, no effect log. |
| **Feedback capture** | No outcome recording, so no learning signal can exist. |
| **Policy evaluation** | `governance/` has no policy model, no evaluation, no enforcement point. |
| **Uncertainty representation** | `contracts/confidence.py` exists (a float). No distribution, no calibration, no propagation. |
| **An LLM boundary** | There is no model client, no prompt construction, no token accounting anywhere in the repository. `[CODE]` |

That last row matters and is easy to skip past. **Innovation OS currently
contains no AI.** It is a governance and traceability framework. "Where should
the AI thinking engine live" is therefore partly a question about where a
*model boundary* should be introduced into a codebase that has never had one —
and the governing principle "AI proposes, systems evaluate, humans authorize"
means that boundary is the most safety-relevant interface in the system.

## H. Candidate locations, ranked

### 1. `intelligence/kernel/` — extend the existing CognitiveKernel ★ recommended

Make `CognitiveKernel` the composition point: it keeps its registry-and-dispatch
role, gains constructor-injected access to the four cleanly-owned outer engines,
and every cognitive operation it routes is wrapped in the custody chain the
repository already implements.

- **Evidence** — It already exists, already works, and its own docstring already
  states the correct boundary ("does not replace engines, routes between
  them"). `IntelligenceRuntime` already demonstrates injection of `LineageEngine`
  and `RetryGuardEngine` with fail-closed `RuntimeError`s. `ArtifactRegistry`
  already demonstrates the same pattern over four engines. `[CODE]`
- **Advantages** — Smallest intervention. No new package. No renaming. Nothing
  depends on `intelligence/`, so no downstream risk. Reuses a pattern proven
  twice in this codebase.
- **Disadvantages** — Inherits the `intelligence/` namespace, whose seven
  duplicate subpackages must be resolved rather than ignored. The name
  "kernel" overstates it until it does more.
- **Dependencies** — provenance, lineage, invariants, context_envelope,
  retry_guard. All present, all cleanly owned.
- **Architectural risk** — **Low.**
- **Confidence** — **High.** `[CODE]`

**Corroboration from prior work.** This recommendation was reached from import
analysis before reading `docs/architecture/intelligence_v2/`. Those documents
independently arrive at the same boundary `[CODE]`:

- `kernel/kernel_consolidation_plan.md` — *"Target State: Single authoritative
  kernel boundary: `innovation_os.intelligence.kernel`"*, with consolidation
  rules *"Kernel owns lifecycle only"* and *"Runtime executes through
  kernel-managed components"*.
- `canonical/canonical_decision_matrix.md` — Kernel criteria are *"lifecycle
  ownership, subsystem initialization, component coordination"*. Coordination,
  not ownership of the things coordinated.

Two independent analyses converging on the same location is the strongest
evidence available here, and "kernel owns lifecycle only" is the same boundary
rule as §I stated in different words.

**Where this report differs from the prior plan.** `graphs/runtime_flow.txt`
specifies the intended chain as Signal → Observation → Perception → Context →
Knowledge → Evidence → Confidence → Hypothesis → Inference. That is a pure
cognitive pipeline with **no provenance, lineage, or invariant step in it**. It
routes intelligence without establishing custody of what it produces.

This report's §J places the cognitive chain *inside* the custody chain rather
than beside it. Given the governing principle — machine output must remain
distinguishable from authorized decision — a cognitive pipeline that produces
`Inference` objects carrying no provenance determination is the specific failure
the provenance module was built to prevent. The prior plan's Phase 1 does list
"provenance tracking" among what to preserve; the runtime flow simply does not
show where it attaches. §J proposes where.

### 2. A new top-level `cognition/` package beside `intelligence/`

- **Evidence** — Nothing forbids it; `intelligence/` has no dependents.
- **Advantages** — Clean namespace, no inherited duplication.
- **Disadvantages** — Creates an eighth ambiguity in a repository already
  carrying seven duplicate-ownership pairs and five graph implementations. The
  problem here is not a shortage of packages.
- **Architectural risk** — **Medium.** Adds to the exact pathology under
  investigation.
- **Confidence** — High that it would work; high that it is the wrong choice.

### 3. At the `registry/` tier, as a capability of `ArtifactRegistry`

- **Evidence** — `ArtifactRegistry` is already the composition point for the
  four clean engines. `[CODE]`
- **Advantages** — Every cognitive act would automatically be an artifact with
  provenance, which is exactly the governing principle.
- **Disadvantages** — Overloads a registry with reasoning. Registration and
  cognition are different responsibilities, and merging them recreates the
  duplicate-ownership problem at a new site.
- **Architectural risk** — Medium-high.
- **Confidence** — High that this is the right *integration target* and the
  wrong *home*.

### 4. As a service above the repository, consuming Innovation OS as a library

- **Evidence** — `api/server.py` and `intelligence/api/` exist but are thin.
- **Advantages** — Clean process boundary; independent deployment.
- **Disadvantages** — Premature. A service boundary around capabilities that do
  not yet exist is an interface for nothing. Revisit once (1) is real.
- **Architectural risk** — Medium.
- **Confidence** — Medium.

### 5. Outside Innovation OS entirely, in the governance stack

Worth stating because the evidence points at it and it would otherwise go
unexamined. The epistemic machinery a thinking engine needs is **already built,
in another repository**. `sentinel_os/conservation/` models a governance decision
as a conservation transformation over typed propositions with
`EpistemicStatus`, `AuthorityStatus`, `OriginStatus`, `Uncertainty`, and an
`EvidenceRegistry`, and it rejects judgments that claim human origin for machine
inferences (`FALSE_HUMAN_ATTRIBUTION`) or assert unrooted propositions
(`UNROOTED_NEW_PROPOSITION`). `[CODE: sentinel_os @ bd18280]`

That is a working implementation of the evidence discipline this very
investigation is conducted under. It is not a candidate location — it is the
wrong layer, and `sentinel_os` is frozen until 2026-12-07 per its README — but
any reasoning layer built in Innovation OS should expect to interoperate with
those types rather than invent a parallel vocabulary. `[REPOSITORY HISTORY]`

## I. Recommended location and boundary

**`intelligence/kernel/`, extending `CognitiveKernel`.**

### Inside the boundary

- Routing a cognitive request to a capability
- Composing multi-step operations (plan → retrieve → reason → evaluate)
- Holding execution context for one cognitive session
- Producing an `IntelligenceArtifact` with identity, confidence, provenance
- The model boundary: prompt construction, model invocation, token accounting

### Explicitly outside the boundary

This list is the operative part of the recommendation. Handoff §14 warns that
the thinking engine must not silently become the owner of governance merely by
consuming it.

| The engine must NOT own | Because | Owner |
| --- | --- | --- |
| Provenance determination | It is a machine originator. Letting it set its own origin status defeats the Article II taxonomy. | `provenance/` |
| Lineage / canonical hashing | Single owner already, consumed correctly. | `lineage/` |
| Invariant enforcement | A component must not be able to waive the checks applied to it. | `invariants/` |
| Context retention | Already single-owned and explicitly non-duplicating. | `context_envelope/` |
| Retry / oscillation budget | The guard exists to bound regeneration. Self-granted budget is no budget. | `retry_guard/` |
| Human authorization | "Humans authorize" is the governing principle. | `review_queue/`, `governance/` |
| Durable storage | A consumer of persistence, not its owner. | `storage/` |

The rule in one line: **the cognitive engine proposes artifacts; it does not
get to determine their status, their lineage, their validity, or their
authorization.** That is the repository's own stated principle, applied to the
engine itself.

## J. Integration architecture

The pattern is already in the codebase; this generalises it.

```
                     ┌──────────────────────────┐
                     │     CognitiveKernel      │
                     │  registry + dispatch     │
                     └────────────┬─────────────┘
                                  │ constructor injection
        ┌──────────────┬──────────┼──────────┬──────────────┐
        ▼              ▼          ▼          ▼              ▼
   ProvenanceEngine  Lineage  Invariant  ContextEnvelope  RetryGuard
        │              │          │          │              │
        └──────────────┴──────────┴──────────┴──────────────┘
                                  │
                          artifact custody chain
                                  │
                                  ▼
                          ArtifactRegistry
```

Every cognitive operation follows the path an artifact already follows:

1. **Guard** — `retry_guard.detect_cycle` / `allow_reentry`, raising on
   oscillation or budget exhaustion. Already implemented in
   `IntelligenceRuntime._guard_execution`. `[CODE]`
2. **Context** — attach a `ContextEnvelope`; mark absent dimensions absent
   rather than dropping them.
3. **Execute** — dispatch to the registered capability.
4. **Hash** — `lineage.canonicalize_artifact` → `hash_artifact`.
5. **Attribute** — register with an explicit machine-originated provenance
   status. Never infer it.
6. **Check** — `invariants` at the artifact boundary.
7. **Record** — `ArtifactRegistry.register` with the lineage edge to its parents.

Steps 1, 4, 5 and 7 are already implemented and already composed by
`ArtifactRegistry`. Steps 2, 3 and 6 are the work.

## K. Migration strategy

Staged so that each step is independently valuable and reversible. **No step
merges, deletes, or renames an existing module** — handoff §17.

**Stage 0 — resolve duplicate ownership (prerequisite).**
For each of the seven contested pairs in §D, record a decision: which package
owns it, and does the other become a consumer or get retired? Record it; do not
execute it yet. Without this the engine is built on contested ground.

This is `intelligence_v2` Phase 2 ("Review: duplicate registries, duplicate
bootstrap paths, duplicate memory interfaces, duplicate artifact definitions")
with the scope corrected. That phase scopes duplication to *within*
`intelligence/`; §D shows the more consequential duplication is *across* the
`intelligence/` boundary, against outer packages that are 2-5× larger. Note also
that `consolidation/duplicate_modules.txt` lists filename collisions — almost
entirely `__init__.py` — which is not the same analysis.

**Stage 1 — wire the kernel to the clean four.**
Give `CognitiveKernel` injected access to provenance, lineage, invariants and
context_envelope, following `IntelligenceRuntime`'s existing pattern. No new
capabilities. Purely structural, and testable: a registered engine's output
should come back with a provenance record and a lineage edge.

**Stage 2 — make one capability real, end to end.**
Pick one and implement it properly through the full custody chain. **Suggested:
repository fingerprinting** — `intelligence/repository/fingerprint_engine.py` is
currently 28 lines, `tools/fingerprint/extract_signature.py` now does the real
work, and it is the capability this whole investigation needs anyway. It makes
the archive self-hosting: Innovation OS fingerprints the portfolio, including
itself.

**Stage 3 — introduce the model boundary.**
One module, one interface, explicit token accounting, and every model output
registered as machine-originated at `PROPOSED` authority — never as fact. This
is the highest-risk step in the repository's history and should not be reached
before Stages 0-2 are done, because it is the step where the governing principle
can be silently violated.

**Stage 4 — retrieval, then feedback.**
Only once artifacts are durably stored and model outputs are attributed. Both
are meaningless before that.

### What preserves module identity through this

Each existing module keeps its name, its package, and its responsibility. The
engine gains references, not ownership. Nothing is merged because it looks
similar — the same rule the fingerprint archive applies to systems, applied
to packages.

---

## Answers to the §16 questions

| # | Question | Answer |
| --- | --- | --- |
| 1 | Centre of gravity | The evidence custody chain: provenance → lineage → invariants → context → registry. `[CODE]` |
| 2 | Foundational modules | `provenance/`, `lineage/`, `invariants/`, `context_envelope/`, `retry_guard/` |
| 3 | Capability providers | `ideation/`, `scoring/`, `forecast/`, `review/`, `search/`, `repository/` |
| 4 | Orchestration layers | `intelligence/kernel/`, `intelligence/runtime/`, `core/pipeline.py` |
| 5 | Governance boundaries | `review_queue/approval.py`, `governance/`, `invariants/` — all thin |
| 6 | State / memory | `memory/`, `intelligence/memory/`, `storage/` — fragmented, non-durable |
| 7 | Reasoning-related | `reasoning/`, `intelligence/reasoning/` — named only |
| 8 | Experimental | Most of `intelligence/`; `simulation/` and `observation/` are empty |
| 9 | Duplicates | 7 outer/intelligence pairs; `decision/` vs `decisions/`; 5 graph implementations |
| 10 | Should stay independent | The clean four. Their single ownership is why they work. |
| 11 | Where cognition belongs | `intelligence/kernel/`, as a composer |
| 12 | What is missing | Reasoning, retrieval, persistence, action, feedback, policy, and a model boundary |
| 13 | What it must NOT own | Provenance, lineage, invariants, context, retry budget, authorization, storage |
| 14 | Interfaces needed | Constructor injection of the four engines; a capability protocol for the registry; an `IntelligenceArtifact` return contract |
| 15 | Smallest intervention | Stage 1: inject the four engines into `CognitiveKernel`. No new package, no renames, zero downstream risk. |

## Evidence log

| Claim | Class | How |
| --- | --- | --- |
| 309 tests pass in 0.52s | `[TEST]` | `python -m pytest -q`, 2026-09-11 |
| `intelligence/`: 0 enums, 4 tunables, 7 raises / 4,700 lines | `[EXPERIMENT]` | `tools/fingerprint/extract_signature.py` |
| 0 imports of `intelligence/` from outer `innovation_os` | `[CODE]` | grep over `src/` excluding `intelligence/` |
| 4 cross-boundary imports, one direction | `[CODE]` | grep, enumerated in §E |
| Duplicate-ownership line counts | `[EXPERIMENT]` | per-package line count |
| Identity-function cognition | `[CODE]` | `cognition/perceiver.py`, `reasoner.py` read in full |
| Ownership rule already stated | `[CODE]` | `context_envelope/envelope.py` docstring |
| Injection pattern exists | `[CODE]` | `runtime/runtime.py`, `registry/artifact_registry.py` |
| No model client anywhere | `[CODE]` | no LLM SDK in imports across 351 files |
| Sentinel conservation types | `[CODE]` | `sentinel_os` @ `bd18280`, `conservation/judgment.py` |
| Sentinel frozen until 2026-12-07 | `[REPOSITORY HISTORY]` | `sentinel_os/README.md` |
| Prior plan targets the same kernel boundary | `[CODE]` | `intelligence_v2/kernel/kernel_consolidation_plan.md` |
| Prior runtime flow omits provenance | `[CODE]` | `intelligence_v2/graphs/runtime_flow.txt` |

## What this investigation did not establish

- Whether the lifecycle packages (`ideation/`, `solution/`, `forecast/`) *want*
  a cognitive layer. No consumer was consulted; no requirement was found in the
  repository. `[UNKNOWN]`
- Whether the 309 passing tests would still pass under Stage 1. Not attempted.
- Whether the `intelligence_v2` plans were ever executed. The planning documents
  exist; whether any consolidation happened is not established from them.
  `[UNKNOWN]`
