# Burial: TBCA, retired in full

**Repo:** `wking53214/TBCA` (archived on GitHub before burial)
**Snapshot commit:** `2fb37da43486afb9fd7110c791ff2e7ff19f7f48` (default branch), the last live state
**Date:** 2026-10-08
**Decision:** William N. King

## Why

TBCA is a single archived conversation turn: a one-word prompt, followed by one
AI response, which is a script that generates a Word document. The document is a
theoretical whitepaper on "Transparent Binary Constraint Architecture." The paper
makes no empirical claims. It is a one-off artifact, not a working component, and
nothing in the stack imports or runs it.

The concept it describes (a minimal, transparent yes-or-no check at every module
boundary) appears in other stack docs, including the CNS evidence docs and the
observe-perceive architecture notes. The live stack implements that idea through
its gate code, not through this repo.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Source transcript | `snapshot/TRANSCRIPT.md` |
| Whitepaper generator script | `snapshot/generate.js` and `snapshot/src/` |
| Provenance and decomposition notes | `snapshot/PROVENANCE.md` |
| Concept in stack docs | CNS evidence docs and observe-perceive architecture notes (not code) |

## What's here

- `snapshot/`: every tracked file at the snapshot commit, exactly as it was.
- `tbca-full-history.bundle`: complete history (3 commits).

## Known issues at time of burial

- The producing AI tool is not recorded. Origin date is unknown (see PROVENANCE).
- The paper is marked as having an incomplete prior-art review.

## Bringing it back

- Whole repo with history: `git clone tbca-full-history.bundle tbca`
- Files only: copy `snapshot/`.
