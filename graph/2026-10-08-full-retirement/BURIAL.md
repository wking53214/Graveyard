# Burial: GRAPH, retired in full

**Repo:** `wking53214/graph` (its live README now says retired)
**Snapshot commit:** `e2a0e39` (main), the last live state before retirement
**Date:** 2026-10-08
**Decision:** William N. King

## Why

GRAPH was a consolidation workspace, not a product. Its own README says the name is provisional "because there is no graph." It holds three unrelated programs in one folder: envelope adapters (`from-facts/`), a seven-layer governance paste (`gaps-kernel/`), and an AST extractor that imports a private CNS module and cannot run publicly (`from-code/`). Nothing in the stack imports it. It is marked "safe to archive" in its own README.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Hash-chained governance with tamper checks and chain errors (the GRAPH concept in memory) | PERCEIVE `src/perceive/kernel.py` (`ChainIntegrityError`) |
| AST graph extractor | `sentinel_os/sage_k/graph_extractor.py`, and `ecology/corpus/StaticCode_Intelligence_Graph_Kernel_V1.py` |
| Envelope and interlock adapter (`GsaUniversalAdapter`) | Many variants: TOUCHSTONE specimens, `GSA-815/cassettes/`, `ecology/corpus/gsa_governance_adapter.py`. Not a single canonical copy |
| Seven-layer governance paste (`gaps-kernel`) | Not located elsewhere in the local copies checked. Kept only in `snapshot/` |
| Everything else | Preserved in `snapshot/` |

## What's here

- `snapshot/`: every tracked file at `e2a0e39`, exactly as it was (12 files).
- `graph-full-history.bundle`: complete history (19 commits on main).

## Known issues at time of burial

- The name "GRAPH" is provisional, and the repo contains no graph. Do not treat it as the GRAPH governance system described in memory. That system is in PERCEIVE.
- The repo had no LICENSE or NOTICE file, though its README says Apache-2.0. The tombstone adds both.
- The flattened `gaps_multilayer_governance_source.py` cannot be parsed. Two methods were never recovered.
- A cached-signature function is decorated with a cache that cannot hash its input, so calling it raises `TypeError`. Documented, not fixed.
- The L6 seal uses a random nonce and a timestamp, so it is not replay-stable.
- The "interlock" is an unkeyed SHA-256 chain with a fixed genesis parent. It stamps labels such as `USER_ORIGIN_VERIFIED`; it does not verify anything.
- The AST extractor imports the private `cns.graph` module. It cannot run from the public repo.
- CNS evidence records (`CNS/docs/evidence/COLLISIONS.md`, `CNS_MAP.md`) cite this repo's file paths. The records are still accurate for the snapshot, but the paths now point to a buried repo.

## Bringing it back

- Whole repo with history: `git clone graph-full-history.bundle graph`
- Files only: copy `snapshot/`.
