# Burial: ZTGKT, retired in full

**Repo:** `wking53214/ZTGKT` (public at burial, Apache-2.0)
**Snapshot commit:** `7dbcf05` (main, 2026-10-07), the last live state
**Date:** 2026-10-10
**Decision:** William N. King

## Why

ZTGKT (Zero-Trust Guardrails & Kinetic Throttle) was a September 2026 reconstruction of a section
that only ever existed inside the single-file UGPIS-Omega system. It is a gate that sits between a
caller and a text generator: three word-list guards, a pacing delay, an HMAC signature, and a retry
loop with feedback. Nothing in the stack imports it. ZTS now does the same work better, and one
small idea with no live equivalent was ported out first.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Domain signal validator, generalized to a caller-supplied marker set (`ztgkt/domain.py`) | **Ported** to OBSERVE as `DomainSignalValidator` in `clinical_signal_validator_adapter.py`, PR #13. OBSERVE already held the clinical-only version with identical rules. |
| Guards: first-person, hedging, unsupported-claim, and the vague-verb normalizer | ZTS (gates, normalizer, causality flag). ZTS is stronger: ZTGKT's unsupported-claim check accepts any digit at all, which its own docs admit. |
| Kinetic Throttle (`throttle.py`) | ZTS `governor.py`, from the same archived constants. |
| HMAC-SHA384 signing (`signing.py`) | ZTS signs its results. |
| Retry loop with feedback, attempt record, duplicate detection (`pipeline.py`) | ZTS `tower.py`, which re-asks only for the gates that failed. |
| Design record (`docs/LINEAGE.md`, `ARCHITECTURE.md`, `INTEGRATION.md`, `KNOWN_GAPS.md`, `PROVENANCE.md`, `reference/`) | Kept here in `snapshot/`. |

## Usefulness review (before burial)

- Read in full: README, PROVENANCE, all four docs, every module, the tests, the two verbatim reference files.
- Searched every local repo for imports of the package. None. Mentions outside this repo are only
  analysis documents and the Graveyard.
- Compared each module with ZTS, OBSERVE, ghost_tools and sentinel_os. Only the generalized domain
  validator had no equivalent.
- Ran the 48 tests on the final commit: all pass once `pytest-asyncio` (declared in the repo's
  dev extras) is installed. Without it, 15 async tests fail.
- **Ported:** the domain validator generalization, with an equivalence check (20,000 random
  signals, identical results and log shape) and 11 tests. Nothing else.

## The lesson worth keeping

The best thing in this repo is a design finding, recorded in `snapshot/docs/LINEAGE.md`:

> A validator that encodes a domain assumption cannot be positioned as universal infrastructure.

The original gate rejected hedging everywhere. That is right for a governance record and wrong for a
clinical signal, where a hedge is calibrated uncertainty and carries information. The fix was to split
one component into two with opposite rules: a polish half (optional, hedging is a defect) and a domain
half (mandatory, hedging is a signal, anchors are required). The same pattern shows up in other repos,
so it is kept here as the record rather than only in a code comment.

LINEAGE.md also records the follow-on problem: four components each answering "is this content
acceptable?" and disagreeing. That arbitration problem was never built here and is a stack-level concern.

## What's here

- `snapshot/`: every tracked file at `7dbcf05`, 30 files. CI is kept as `_github_disabled/` so it never runs here.
- `ztgkt-full-history.bundle`: complete history (13 commits) plus pull refs #1 to #5. Verified with
  `git bundle verify`, and a clone of it matches the snapshot.

## Known issues at time of burial

Recorded so a revival starts from the truth:

- The guards match bare word stems only. "optimize" is caught, "optimized" is not.
- The guards are a formatting policy, not a safety control. Synonyms and homoglyphs pass.
- The unsupported-claim filter accepts any digit, including a list index or a year.
- The throttle's proportional band is narrow: at default settings most real payloads hit the flat 200 ms cap. It also paces one payload and is not a rate limiter.
- The archive's hardcoded HMAC key survives only as `ARCHIVE_DEFAULT_KEY`, for replaying old signatures. Without a key supplied, signing uses a random per-instance key.
- A deterministic generator burns the whole retry budget returning the same rejected text. Duplicate detection reports it but cannot fix it.
- The acronym had four different expansions across the archive. This repo uses the dominant one.
- It is a reconstruction. Everything in `reference/` is verbatim archive text; the package around it, the tests and the docs were written for the reconstruction.

## Bringing it back

- Whole repo with history: `git clone ztgkt-full-history.bundle ZTGKT`
- Files only: copy `snapshot/` and rename `_github_disabled` back to `.github`.
- `pip install -e ".[dev]"` then `python -m pytest -q`.
