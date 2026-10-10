# Burial: innovation_os, retired in full

**Repo:** `wking53214/innovation_os` (private; reduced to a LICENSE and a gravestone by innovation_os PR #3, with archiving on GitHub left to the owner)
**Snapshot commit:** `08470f1` (main), "docs: complete architectural rewrite with transparent gap accounting"
**Branches and tags in the bundle:** `main`, the unmerged `claude/licenses-72o5xt` (`872c4d1`), and 65 tags (v0.1.0, v3.0.0 to v3.0.2, and the intelligence-v* tags)
**Date:** 2026-10-08
**Decision:** William N. King

## What it was

A governed pipeline meant to record the reasoning behind decisions and code, not just the code. It tracked ideas through review, approval and decision, on the principle "AI proposes, systems evaluate, humans authorize".

## Why

Its useful parts were already done better elsewhere in the stack. The Sept 8 audit docs list it as a non-wedge repo marked for archive. The repo was later reopened (the audit docs say archived, and GitHub showed it unarchived at burial; the reason for reopening is not recorded). The live pieces were carried out as listed below, and nothing active depends on it any more.

## Where each part lives now

| Part | Where it lives now | State |
|---|---|---|
| Retry guard | CNS PR #8, `cns_composition/resubmission.py` | Merged. **Called by link** (`admit_session`, link PR #1) |
| Scope part of context envelopes | Conservation_Kernel PR #12 (`Proposition.conditions`, scope-widening approval) | Merged. **No caller yet** |
| Decision records (options, selected, rejected, deferred, assumptions, plus `DEC-TEMPLATE_v1.md`) | CCC PR #24 | Merged. **No caller yet** |
| Two invariants (a rejected record is final; a record can be superseded only once) | CCC PR #25 | Merged |
| Git commit lister | Ecology PR #18 (`commit_loader.py`, `commit_history_v1` index) | Merged |
| Keyword clustering | CCC PR #26 (recurring groups) and observe-perceive PR #34 | Merged. Live now: observe-perceive's CCC pin was bumped after burial (observe-perceive PR #38 and #41) |
| Fingerprint extractor, two parts (numbers set in code with value and line; a cryptography boundary) | ghost_tools PR #85 | Merged. Hashing was left out on purpose |
| Approval adapter | observe-perceive PR #37, renamed `approval_governance_adapter`, neutral origin label | Merged. **No caller yet** |
| Adapter, decision model and translators inside CNS | Removed by CNS PR #9 | Merged |
| DEC-0002 (CCC v1.1 disposition) | CCC PR #23, `decisions/` | Merged |

## Left behind on purpose (only here)

- **Lineage parent binding:** Conservation_Kernel already does it more strictly.
- **Lifecycle table:** partly covered. CCC's provenance module and DGK's ledger check state transitions, but the full table was not found in GSA or ghost_tools. Elegant and TOUCHSTONE are not in the current repo list, so that part of the original claim could not be checked.
- **Significance and the per-item record** from context envelopes.
- **Decision-record predictions and confidence:** the form that writes down a predicted outcome, its risks and a stated confidence before the result is only here. sentinel_os compares predicted and actual waits for recommendations (`recommendation_impact.py`), so predicted outcomes exist in STACK for that one domain, but not as a decision-record field.
- **Replay of recorded decisions:** partly covered. observe-perceive's `governance_chain.py` re-verifies recorded decision chains. The decision-replay module here has no structured reconsideration record.
- **Fingerprint archive** (`docs/fingerprints/`: schema, master archive, unresolved list, four cards, and the Sept 12 portfolio census). It was built to sort old conversations by which system a concept belongs to. The census is a dated measurement and the cards describe other repos as they were then.
- **CEE-0001** (the original "Concept Evolution Engine" conversation), the decision ledger (an example entry only), the `memory/` notes (including "advisory enforcement defaults OFF"), and the architecture survey and inventory dumps.
- **HERALD** was rejected as a home for keyword clustering.

## What's here

- `snapshot/`: every tracked file at `08470f1`. The CI folder is renamed `_github_disabled`, so nothing runs here.
- `innovation_os-full-history.bundle`: full history of all branches and tags (279 commits across all branches and tags). Pull-request refs are not included.

## Known issues at time of burial

- The approval engine accepted an approval with an empty reviewer name. This was never fixed in innovation_os. The observe-perceive seam now treats an approval with no named reviewer as not human review.
- Lineage: `link_parent_artifact` and `link_idea` both make `verify` return False. Found in the October 2026 audit and reproduced on scratch copies. Not fixed here.
- Retry guard: `assess_repetition` builds its check without `retry_count`, while the stored attempt record includes it, so a repeat after the first retry is not detected. The CNS port's note says this is fixed. That fix was not re-tested.
- Several gap checks in the CNS composition tests assert a known gap rather than test a working feature.
- Several carried-out pieces have no caller yet and do nothing until something calls them (see the table).
- The history was scanned for tokens, keys and passwords before this went public, and none were found. Some baseline data holds a local home path; it is harmless.

## Bringing it back

- Whole repo with history: `git clone innovation_os-full-history.bundle innovation_os`, then check out `main` (other branches and tags are inside).
- Files only: copy `snapshot/`. Rename `_github_disabled` back to `.github` to restore CI.
- It needs Python 3.11 or newer. The last recorded run was 245 tests.
- Before reviving, check whether the pieces in the table above already cover what you need.
