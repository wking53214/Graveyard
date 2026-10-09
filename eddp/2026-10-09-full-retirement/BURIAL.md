# Burial: EDDP, retired in full

**Repo:** `wking53214/eddp` (private at burial, Apache-2.0)
**Snapshot commit:** `04e9048` (main), the last live state
**Date:** 2026-10-09
**Decision:** William N. King

## Why

EDDP is a lab pipeline: it chains an ingestion authentication module (keyed HMAC-SHA256), a telemetry guardrail, and a dispatch adapter. Its README marks it as historical and off the live path. It was the predecessor of the observe-only telemetry and fail-closed ingest work now carried in other repos. The repo is retired in full.

## Usefulness review (before burial)

- Searched every local clone for imports of its modules. The only match is inside an archived snapshot in the Graveyard. No live code imports EDDP.
- The repo's own test suite passes at burial: 165 passed, 0 failed (main `04e9048`).
- The telemetry guardrail and ingestion authentication were let go. The `authorized_by` HMAC attestation idea was carried into `sentinel_os` (see `APPLY_authorized_by_attestation.md` there). Nothing else was ported.
- **Not included:** an uncommitted local reorganization of the repo on the owner's machine (applied around 2026-08-26, never committed or pushed). That work exists only on that machine and is not part of this burial.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Source, tests, license, notice, provenance, scanner records | `snapshot/` (27 tracked files at `04e9048`) |
| Full history | `eddp-full-history.bundle` (scrubbed copy, see below) |
| `authorized_by` attestation idea | `wking53214/sentinel_os`, `APPLY_authorized_by_attestation.md` |
| Uncommitted local reorganization | Owner's machine only. Not captured here |

## What's here

- `snapshot/`: all 27 tracked files at `04e9048`, including LICENSE (Apache-2.0), NOTICE, PROVENANCE.md, `_archive/`, the scanner state files (`.ghost_*.json`), `.gitleaksignore`, and `.github/workflows/` (nested, so it does not run from this location).
- `eddp-full-history.bundle`: 34 commits plus 2 pull-request refs. Verified with `git bundle verify`, which reports a complete history.

## Change to the history (read this before using the bundle)

The bundle is **not** a byte-exact copy of the private repo's history.

- Commit `1905e0d` (2026-09-24) replaced a development placeholder signing secret, which the older commits still contained.
- Before publishing, that placeholder string was replaced in every commit of the bundle copy with `dev-placeholder-redacted`. No commit in the bundle contains the original string. No backup refs remain.
- Because of this, commit hashes in the bundle differ from the private repo. The bundle's `main` is `a54b7e7`. Its tree is identical to the original `04e9048` tree, so the snapshot and the current code are unchanged.
- The private repo itself was not modified.

## Known issues at time of burial

- Lab pipeline with no live consumer.
- The original code relied on a fixed development placeholder secret. That was replaced with a random per-instance fallback on 2026-09-24. With no secret configured, inbound signatures are rejected.
- The history was rewritten on 2026-09-24 to remove conversation transcripts. The removal is recorded in commit `430f738`.
- Two email addresses in the engine files (`ceo@company.com`, `enterprise.org` addresses) are placeholders, not real contacts.
- The `.ghost_*.json` files are scanner records (tool metadata and commit hashes), not personal data.

## Bringing it back

- Whole repo with history: `git clone eddp-full-history.bundle eddp`
- Files only: copy `snapshot/`.
