# Burial: CLIP, retired in full

**Repo:** `wking53214/clip` (its live README now says retired)
**Snapshot commit:** `176e9da` (main), the reconstruction commit. It holds the CLIP state at `919a740`
**Date:** 2026-10-08
**Decision:** William N. King

## Why

CLIP was never a separate repository. It was the original name of the repo that became STRIDE, renamed on 2026-08-17. The original repo was deleted, and this repo is a 2026-09-17 reconstruction of its earlier state (`919a740`, before the rename). Nothing in the stack imports it.

The six code files in this state are byte-identical to the copies already buried in the STRIDE burial (`stride/2026-10-08-full-retirement/snapshot/recovered_repo_clip_state_919a740/`). So the code adds nothing new. What is unique here is the design record: `PROVENANCE.md` and the transcript source.

## Usefulness review (run before burial)

Each idea was checked against the STRIDE review and the live stack. Result: nothing ported.

| Idea in CLIP | Finding |
|---|---|
| Identity, hedging, and causality validators | Covered by ZTS (gates G6, G3, and causality flags) and DIT |
| Input normalizer | Covered by ZTS's Logic Cornerstone normalization |
| Loop and repeat detection (pipeline state engine) | Covered by DIT's oscillation guard |
| Traffic governor (pacing) | Covered by DIT's governor and ZTS's Kinetic Governor |
| Hash-chained state records | Covered by DIT's ledger. Keyed fingerprints are in ZTS |
| Backpressure and performance dashboard | Covered by ZTS and governance_gateway telemetry dashboards |
| Anomaly, variance, fragility, and consolidation analytics | Not ported. Same reasoning as the STRIDE review: the inputs are proxies (message length, not customer behavior), so the outputs are not measurements |
| Signed attestation | Not ported. The code carries a hardcoded signing key from the GSA lineage. DIT refuses that key on purpose |
| Simulated gateway and sandbox runner | Test scaffolding only. Nothing to keep |
| `PROVENANCE.md` and transcript source | Record of design history, not code. Kept here in full |

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Linguistic gates and rewrite loop | ZTS, DIT |
| Loop guard, pacing, ledger, signing | DIT (`src/dit/`) |
| Telemetry dashboard | ZTS and governance_gateway telemetry PRs |
| Analytics layer | Not ported. Preserved in `snapshot/` and in the STRIDE burial |
| Code artifacts (all six) | STRIDE burial, `recovered_repo_clip_state_919a740/` (identical bytes) |
| Design record (`PROVENANCE.md`, transcript) | Only in this burial, `snapshot/recovered_repo/` |

## What's here

- `snapshot/`: every tracked file at `176e9da`, exactly as it was (15 files: six code artifacts, `PROVENANCE.md`, the transcript source, evidence, manifests, and the code inventory report).
- `clip-full-history.bundle`: complete history of this repo (1 commit). The original CLIP commits are not recoverable.

## Known issues at time of burial

- The original CLIP commits (`919a740`, `56dd695`, `a9aef1b`, and one unknown hash) do not exist here. The record is the reconstruction.
- `artifact_1.py` and `artifact_5.py` are single-line pastes and do not parse. Nothing was reformatted.
- `artifact_6.py` carries a `SYSTEM_NAME: STRIDE` header that a later session determined was applied in error. Preserved as found.
- `artifact_5.py` is byte-identical to a file in the FACTS and RADAR repos. It is the same flattened paste from three separate conversations.
- The code contains a hardcoded signing key string from the GSA lineage. Do not reuse it.
- The reconstruction README expands CLIP as "Citadel Linguistic Integrity Pipeline", but the code's own headers say STRIDE. Recorded, not reconciled.

## Bringing it back

- Whole repo with history: `git clone clip-full-history.bundle clip`
- Files only: copy `snapshot/`.
- The later STRIDE state, with its history, is in the STRIDE burial.
