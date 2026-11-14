# Burial: ARLF, retired in full

**Repo:** `wking53214/ARLF`
**Snapshot commit:** `9d4f818` (main), the last live state
**Date:** 2026-10-07
**Decision:** William N. King

## Why

ARLF is a reference package of governance-resolution ideas (certificates for
unresolved questions, escalation gates, a governor, a pipeline, substrate and
RLCF modules) with four test files. It was never run, and nothing in the stack
imports it. Its useful ideas were reviewed against the stack. Two were ported:

- The "cause" idea (every refusal records why it happened) went into DGK, PR #19.
- A step budget (a hard cap on how many steps a run may take) went into ZTS, PR #8.

The rest was left out on purpose. The certificate, escalation mapping and
discharge concepts overlap with mechanisms already in the stack. The verdict
scheme (answers that are not just yes or no, with a fixed set of outcomes) was
also left out. The stack already has many verdict and status enums, so porting it
would duplicate them.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Refusal-cause idea | DGK `feature/refusal-cause`, PR #19 (open) |
| Step budget idea | ZTS `feature/step-budget`, PR #8 (open) |
| Certificate, gates, governor, pipeline, resolution, substrate, RLCF modules | Preserved in `snapshot/proposals/reference/arlf/` |
| Evidence, chronology, entities, lineage, reports, schemas, spec, adversarial | Preserved in `snapshot/` |

## What's here

- `snapshot/`: every tracked file at `9d4f818`, exactly as it was, except for the one redaction recorded below.
- `arlf-full-history.bundle`: complete history (8 commits on main).

## Known issues at time of burial

- The reference modules were never executed. Their tests were never run.
- Verdict scheme was not ported. Certificate and discharge concepts were only partly ported.
- The two open PRs (DGK #19, ZTS #8) must be merged or closed before the ideas
  count as in the stack.

## Redaction (2026-11-13)

One personal sentence was removed from this public copy. It was a quoted prompt from the source
conversation (record 2117) that named a family member and a location. It appeared in two files:
`snapshot/evidence/source_records.jsonl` (the `prompt` field) and `snapshot/evidence/evidence_ledger.jsonl`
(the `claim` field). Each now holds a redaction marker in its place. Nothing else in either file changed,
and both still parse line by line as JSON. The `chars` and `record_chars` numbers still describe the
original record, so they no longer match the shortened text.

The full history bundle (`arlf-full-history.bundle`) was not changed and still contains the original
sentence in its older commits. The same text exists in the private `Gemini_Extraction` repo. Rewriting the
bundle is a separate decision for the owner.

## Bringing it back

- Whole repo with history: `git clone arlf-full-history.bundle arlf`
- Files only: copy `snapshot/`.
