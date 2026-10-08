# Burial: STRIDE, retired in full

**Repo:** `wking53214/stride` (its live README now says retired, PR #1)
**Snapshot commit:** `596f81b` (main), the last live state before retirement
**Date:** 2026-10-08
**Decision:** William N. King

## Why

STRIDE is a reconstruction of a deleted gateway, rebuilt from fragments of a pasted conversation. It holds several flattened variants of the same code, plus evidence, manifests, and reports. Nothing in the stack imports it, and every part worth keeping now exists in a better form elsewhere.

The one idea that existed only in STRIDE, the analytics layer (distortion, fragility, stability, confidence), was not ported. Its "repeat contact" input is really message length, so it measures the payload, not customer behavior.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Linguistic gates (first person, hedging, causal claims) | DIT, ZTS, and `sentinel_os/epistemic/dit_gate.py` |
| Constraint-based rewrite loop | DIT `src/dit/injection.py`, ZTS `src/zts/tower.py` |
| Kinetic governor (pacing) | DIT `src/dit/governor.py` |
| Hash-chained ledger | DIT `src/dit/ledger.py` |
| Signed attestation | DIT `src/dit/signing.py` (refuses the hardcoded key) |
| Oscillation / repeat guard | DIT `src/dit/oscillation.py`, `sentinel_os/governance_loop_guard.py` |
| Graph extractor | `sentinel_os/sage_k/graph_extractor.py` |
| Hash-chained interlock wrapper | `sentinel_os/sage_k/gsa_adapter.py` |
| Backpressure | `sentinel_os/backpressure.py` (newer version than STRIDE's) |
| Telemetry dashboard idea | ZTS `feature/telemetry-dashboard` (PR #9), governance_gateway `feature/telemetry-dashboard` (PR #8) |
| Analytics layer (distortion, fragility, stability, confidence) | Not ported. Preserved in `snapshot/` only |
| All variants and evidence | Preserved in `snapshot/` |

## What's here

- `snapshot/`: every tracked file at `596f81b`, exactly as it was.
- `stride-full-history.bundle`: complete history (3 commits on main).

## Known issues at time of burial

- It was reconstructed from fragments. The original repo was deleted, and its 4 original commits are missing.
- The flattened CLIP source does not parse as one program. Several variants disagree on names and details.
- The recovered source contains a hardcoded signing key string from the GSA lineage. Do not reuse it. DIT refuses it on purpose.
- The analytics layer takes proxy inputs, so its outputs should not be used as measurements.
- The duplicate-payload set in the execute path has no size limit.
- The interlock's hash chain uses plain SHA-256 with no secret key, and the verifier checks only the last link. It catches accidental changes, not tampering.
- About 30 repos could not be read, and non-default branches were not checked. The library review was done by name and behavior, not line by line.
- Open PRs that must be merged or closed before this counts as finished: Graveyard #10 (this burial), STRIDE #1 (retirement notice), ZTS #9, and governance_gateway #8.

## Bringing it back

- Whole repo with history: `git clone stride-full-history.bundle stride`
- Files only: copy `snapshot/`.
