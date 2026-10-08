# Burial: gsa-governance-core, retired in full

**Repo:** `wking53214/gsa-governance-core` (its live README now says retired once the tombstone merges)
**Snapshot commit:** `ff6a883` (main), the last live state before retirement
**Date:** 2026-10-08
**Decision:** William N. King

## Why

This repo holds one file: a self-contained "Governance Operating Core" reference runtime, about 5,000 lines with no dependencies. Its own README says it was never deployed, never sat on a live request path, and is not an audit trail. The production governance it was meant to illustrate runs in sentinel_os. Nothing in the stack imports it.

## Usefulness review (run before burial)

Each layer was checked against the live stack. Result: nothing ported.

| Idea in the core | Finding |
|---|---|
| Circuit breaker | Live in sentinel_os (`circuit_breaker.py`, tested). |
| Rate limiting | Live in sentinel_os (`api_key_auth.py`) and GSA gateway. |
| Identity, citadel routing and diamond engines, kernel registry, provenance, sanitizer, policy rules | Same names in the GSA copies and sentinel_os lineage. The core's versions are the same design, already covered. |
| Immutable audit ledger | Not ported. The README says it is an in-memory dict that does not persist, and it does not link one entry to the next. The live ledgers are DIT and PERCEIVE. |
| Module attestation and cryptographic sealing | Not ported. The README says `verified=True` is set unconditionally, and the seal is not a signature. |
| Human approval workflow | Not ported. It waits 10 ms and then approves. A stub, not a control. |
| Runtime health monitor, adaptive threshold controller, adaptive queue controller | Not ported. No live equivalent under these names, but the implementations are unverified and their values are fixed starting points. Revisit only as a fresh design. |

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Circuit breaker and rate limiting | sentinel_os |
| Ledger and signing | DIT and PERCEIVE |
| Full runtime and its gaps | Only in this burial (`snapshot/`) |

## What's here

- `snapshot/`: every tracked file at `ff6a883`, exactly as it was (6 files: the runtime, its test harness, README, PROVENANCE, LICENSE, and .gitignore).
- `gsa-governance-core-full-history.bundle`: complete history (1 commit).

## Known issues at time of burial

- The README lists nine demonstrated flaws. The test harness is meant to fail (exit 1) and show them.
- The audit ledger is in memory and does not persist. The README says it is not an audit trail.
- Module attestation records `verified=True` without checking anything.
- The human approval step auto-approves.
- Other copies of this file exist in older working copies (GSA and sentinel_os). They differ from this one, and this one is the canonical copy according to PROVENANCE.

## Bringing it back

- Whole repo with history: `git clone gsa-governance-core-full-history.bundle gsa-governance-core`
- Files only: copy `snapshot/`.
