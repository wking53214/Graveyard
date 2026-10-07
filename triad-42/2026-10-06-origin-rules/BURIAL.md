# Burial: Triad-42's own origin rules

**Removed from:** `wking53214/Triad-42`
**Source commit:** `ab5521c` (main, 2026-09-17), the last version that contained them
**Date:** 2026-10-06
**Decision:** William N. King

## What was buried

Triad-42 2.2.0 carried a complete second copy of the origin rulebook that CCC
(the Cognitive Continuity Constitution) also implements:

- **Chain A origin labels** (`Origin`): six categories, five of them with the
  same names CCC uses.
- **Chain B support links** with stated reasons and cycle prevention.
- **Human-root requirement**: FACT only when a support chain reaches
  human-originated material.
- **Fact promotion and relabel** through a recorded human `Authorization`.
- **Erasure with cascade**: removing a root downgrades whatever rested on it;
  `zombie_check()` found facts left without a human root.

## Why

Reviewed from a governance standpoint:

- **Separation of duties.** A review tool that can certify facts is the
  authority creep the framework exists to prevent. The Triad proposes; it
  should never ratify.
- **One rulebook.** Two independent copies of the same rules drift; a fix in one
  never reaches the other. CCC now owns them alone.
- **No shadow records.** A Triad-side store that outlived the session could keep
  a copy of something a human erased in CCC.

## What replaced it in Triad-42 3.0.0

- Labeled items are immutable. There is no relabel and no authorization type.
- Everything the Triad produces is advisory; its outputs are never FACT.
- The candidate store is session working memory only.
- `triad42.ccc_handoff.hand_off` records session output into CCC, always as a
  machine (MODEL) actor, including what was not shown to the human, never twice,
  and it raises rather than silently skipping when CCC is absent.
- Where Triad output feeds a governed decision inside ≡TACK, the rule is "no CCC
  record, no use", enforced at the integration point (CNS), not inside Triad-42.

## What's here

- `removed/`: files deleted outright, verbatim at `ab5521c`:
  `provenance.py` (418 lines), `test_provenance.py` (41 tests),
  `example_provenance.py`.
- `before_change/`: the full pre-change versions of the files that were edited
  rather than deleted (`epistemic.py` held `Authorization` and `relabel`;
  `review.py`, `telemetry.py` and `__init__.py` wired the provenance graph in).

## Bringing it back

Do not restore this into Triad-42 as a second rulebook. If a capability here is
missing from CCC, port it into CCC, which is the single owner. CCC already has
provenance categories, human-only promotion, erasure with tombstones, and
retrieval of what was not surfaced; compare against it first.
