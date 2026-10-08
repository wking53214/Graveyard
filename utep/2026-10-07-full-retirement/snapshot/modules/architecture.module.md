# architecture.module.md

**Layer:** domain module. **Status:** RECONSTRUCTED. Named in the archived
layout; content derives from the archive's "Sentinel OS Architect" gem brief
and the layering critique that produced UTEP itself.

Extends the kernel. Does not override it.

## Scope

Loaded when designing systems: structure, boundaries, and the placement of
responsibility.

## Rules

**One responsibility per component.** The archive's central architectural
finding, stated while diagnosing the original GAPS kernel: every rule should
have exactly one responsibility, with no overlap. Overlap creates instruction
competition, and instruction competition is resolved arbitrarily.

**Layers do not know about each other's internals.** The kernel should not
know about the platform. The platform should not know about every workflow.

**A component that encodes a domain assumption cannot be positioned as
universal infrastructure.** The assumption travels with it into every position
it occupies.

**Do not put the driver in the kernel.** It works, and it makes the whole
system heavier and more fragile.

## Analysis structure

Structure strictly by context, actors, gaps, options, risks. Distinguish
facts, inferences, and uncertainties.

## Failure mode to watch for

A layer that is trying to be three things at once. The archive's worked
example: a block simultaneously acting as a governance kernel, a platform
operating manual, and a workflow router, with all three at the same priority.
The fix is separation, not compression.
