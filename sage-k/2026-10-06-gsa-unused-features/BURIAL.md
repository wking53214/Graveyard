# Burial: three unused GSA adapter features

**Removed from:** `wking53214/sage-k`, file `sage_k/gsa_adapter.py`
**Source commit:** `52a08cd` (sage-k `main`, 2026-10-03), the last version that contained them
**Date:** 2026-10-06

## What was buried

1. **Checkpoint / re-entry anchors.** A pipeline could mark a step as a saved
   checkpoint and later resume from it, with the adapter checking the resumed
   state matched what was saved. Seam S24 in sage-k's `docs/SEAM_INVENTORY.md`.
2. **Fork / join branch merging.** A pipeline could split into branches and merge
   them back at a named module, folding every branch's hash into the merged step.
   Seam S25.
3. **`GsaTemporalDoorwayGate`.** A gate that held an envelope until a rotating,
   time-based hash matched a target, or timed out. Seam S26.

## Why

None of the three was ever used. Nothing in sage-k set the headers that switch
on the first two, and the gate class was never created anywhere. They made the
adapter look like it did more than it does. The tamper-evident hash chain, which
is the part that actually works, stays in sage-k unchanged.

## What's here

- `gsa_adapter_before_removal.py`: the complete file exactly as it stood at
  `52a08cd`. The features are woven into the adapter's main routine, so the whole
  file is kept rather than fragments that would not make sense on their own.
  - Re-entry: `gsa_reentry_target_id`, `gsa_set_static_anchor_id`, `gsa_static_anchors`
  - Fork/join: `gsa_graph_forks`, `gsa_branch_hash_*`, the `extra_anchors` merge path
  - Gate: the `GsaTemporalDoorwayGate` class at the bottom of the file

## Bringing it back

The hash format was not changed by the removal, so any of these can be restored
without breaking existing chains. Before reviving one, give it a real caller and a
test. Known weaknesses recorded in the seam inventory:

- Re-entry and fork/join failures surface as a status string, not a stop. The
  caller has to check for them.
- The gate is a polling loop inside the same process, not a real security
  boundary, and it starts a background task that nothing shuts down by default.
