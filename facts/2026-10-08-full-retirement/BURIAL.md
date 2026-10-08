# Burial: FACTS, retired in full

**Repo:** `wking53214/FACTS` (its live README now says retired)
**Snapshot commit:** `5f7573a` (main), the last live state before retirement
**Date:** 2026-10-08
**Decision:** William N. King

## Why

FACTS is a reconstruction, not an original repo. Its own README says the original commits (`e40f60d`, `edcb397`, and two more) do not exist here, and the repo was created empty on 2026-09-17. The code inside is a forensic recovery of a Gemini transcript. That code calls itself GRAPH, and its envelope adapter is the same lineage as the `from-facts/` folder already buried in the GRAPH burial. Nothing in the stack imports it.

## Usefulness review (run before burial)

Each idea was checked against GRAPH's buried copies and the live stack. Result: nothing was ported. The one mechanism that looked new (pre-hook and post-hook chains on the adapter) is already in GRAPH's `from-facts/` copies, so it was not new.

| Idea in FACTS | Finding |
|---|---|
| Pre-hook and post-hook chains on the envelope adapter | Already in GRAPH `from-facts/`, buried 2026-10-08. Not ported. Hooks run before and after governance and can rewrite headers, so a port would need a design that keeps governance first. |
| Interlock hash (`gsa_interlock_hash`) | Unkeyed SHA-256 chain with a fixed genesis parent. It stamps labels such as "verified" and verifies nothing. Keyed, hash-chained ledgers exist in DIT and PERCEIVE. |
| Cached signature provider | Wrapped in an LRU cache over a frozen dataclass that holds dicts, so calling it raises `TypeError`. Not usable. |
| Crypto engine, module registry, state integrity, universal wrapper | Variants of the same envelope and interlock design. Most do not parse. No new logic found. |
| The eight artifacts not present in GRAPH | Same design in different pastes. Kept in `snapshot/` for the record. |

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Envelope adapter and hooks | GRAPH burial, `from-facts/` (buried) |
| Hash-chained governance with tamper checks | PERCEIVE `src/perceive/kernel.py` |
| Everything else | Preserved in `snapshot/` |

## What's here

- `snapshot/`: every tracked file at `5f7573a`, exactly as it was (25 files, including the 14 recovered artifacts, evidence records, and manifests).
- `facts-full-history.bundle`: complete history (1 commit). The original commits named above are not in this repo, so the bundle does not contain them either.

## Known issues at time of burial

- Nine of the 14 recovered artifacts do not parse. Three are flattened single-line pastes. Six have real line structure and still fail. Nothing was corrected or completed, so the breakage is the evidence.
- `PROVENANCE.md` was never recovered. No surviving session opened it, so there is no stated behavior table to check against. Validation rests on git blobs and transcript containment.
- `graph-state-integrity.py` (artifact 13) is byte-identical to a file in the CLIP/STRIDE and RADAR repos. The same flattened paste appears in three separate Gemini conversations.
- Name mismatch: the repo is named FACTS, the code calls itself GRAPH, and the transcript is titled "FACTS (Forensic Audit & Clinical Transformation System)". Recorded, not reconciled.
- The repo had no LICENSE or NOTICE file. The tombstone adds both.

## Bringing it back

- Whole repo with history: `git clone facts-full-history.bundle facts`
- Files only: copy `snapshot/`.
