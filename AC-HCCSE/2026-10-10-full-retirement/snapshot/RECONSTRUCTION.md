# Reconstruction record

The original `wking53214/AC-HCCSE` is gone. This package was rebuilt in
September 2026 from the source conversation preserved in the account's Gemini
archive.

Unlike a strict archival restoration, this rebuild **optimizes for working
software**. The engine was removed from the research study set after the data
loss, so there is no longer a reason to preserve defects for fidelity's sake.
Where the recovered artifact was wrong or untunable, it was fixed, and each
change is listed below.

## Source

One activity record — `2026-06-22T00:25:59.887Z`, 187 lines — containing the
complete engine. It parses and executes as recovered, producing:

```
{'group_id': 'group_omega', 'count_alpha': 1, 'count_beta': 1, 'count_gamma': 1,
 'action_directive': 'Escalate to systemic review assembly'}
{'proc_alpha': 0.15, 'proc_beta': 0.75, 'proc_gamma': 0.09999999999999999}
```

Those numbers are pinned by two fidelity tests. The default configuration must
reproduce them, so the scoring model and the allocation weights cannot drift
without a test failing.

## Structure

The artifact was a single flat module. It is now seven modules along the lines
the original classes already implied — scoring, categories, review,
allocation, sampling, orchestration — with no logic moved between them.

## Changes from the recovered artifact

### 1. `confidence_value` was a lie, and is gone

Every evaluation returned `confidence_value=0.85`, a hardcoded constant. It was
not derived from anything and did not vary between a borderline case and an
obvious one, but it read as a model's stated confidence — the most misleading
kind of defect, because a downstream consumer could reasonably filter on it.

Replaced with `friction_score`, which carries the actual computed score. The
number now means what the field name says.

### 2. Magic numbers became configuration

The baseline duration, the routing weight, both category thresholds, both
allocation weights and both escalation counts were literals inside method
bodies. The scoring model was therefore unstateable without reading the code
and untunable without editing it.

They are now fields on `ScoringConfig`, `AllocationConfig` and
`DirectiveConfig`, with defaults equal to the original values.
`ScoringConfig` also rejects inverted thresholds at construction, which the
original would have accepted while silently making one category unreachable.

### 3. Sampling is reproducible, and no longer disturbs anyone else

`DataSampler` called the module-level `random.sample`. Two consequences: a
review sample could never be reproduced, so a disputed batch could not be
re-examined; and seeding it for a test would have perturbed the global random
stream for the rest of the process.

It now holds a private `random.Random` and takes an optional seed. A test
asserts that using it leaves the global stream untouched.

### 4. Routing now reaches a decision

`calculate_priority` returned a dictionary of scores and nothing selected from
it, so the module scored a routing decision without making one. Added
`select_processor`, which picks the highest score and **breaks ties on
processor id** — otherwise the choice would silently depend on dictionary
insertion order.

### 5. Directives carry a level and a reason

`_determine_directive` returned a bare string. The `AllocationLevel` enum was
defined in the original and never used anywhere — the escalation tiers existed
as a concept with no code path reaching them.

Directives are now a `Directive` object carrying the level, the text and a
stated reason (`"1 record(s) in GAMMA"`), so a batch report says why it
escalated rather than only that it did.

### 6. Records are immutable

`InteractionRecord` and `EvaluatedRecord` are `frozen=True`. An evaluated
record is a finding about a completed interaction; nothing downstream has cause
to edit one, and freezing makes an accidental write an error rather than a
silent rewrite of evidence.

### 7. Smaller corrections

- Unused `Optional` import removed.
- Negative workload counts are clamped to zero. The original's
  `1.0 / (1.0 + load)` would give a processor reporting `-5` a score of
  `-0.25`, and one reporting `-1` a division by zero.
- An empty `sample_size` of zero or less returns `[]` rather than falling
  through to `random.sample`.

## Verification

- 22 tests pass, including the two fidelity tests above.
- The demo runs end to end and reproduces the original scenario's counts,
  scores and directive.
- CI runs the suite and the demo on Python 3.10 through 3.13.

## What is not here

- The original repository's flat `artifact_N.py` files, its `PROVENANCE.md` and
  its `TRANSCRIPT.md`. All are lost; six of the nine archived artifacts did not
  execute in any case.
- The full source conversation. The Gemini export preserves rendered activity
  records, not conversation threading, so only the four tagged records survive
  and only one carries this engine.
