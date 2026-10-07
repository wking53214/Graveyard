# Burial: CCC's unused record types

**Repo:** `wking53214/CCC`
**Source commit:** `85bbc4e` (main, 2026-10-06), the last state that had them
**Removal commit:** `8d8312d` (branch `claude/bury-unused-record-types`)
**Date:** 2026-10-06
**Decision:** William N. King

## What was removed

| Piece | Module | What it did |
|---|---|---|
| Turning points | `inflection.py` | A machine flags a possible change of direction; a human rates its significance |
| Threads and branches | `threads.py`, `branches.py` | Named lines of reasoning, with deferred side branches |
| Simulations | `simulation.py` | Stores a modeled trajectory with its assumptions and limitations; blocks it from becoming history |
| Official terms | `canonicalization.py` | Proposed vocabulary that only a human can make canonical |
| The "42" dialogue loop | `dialogue.py`, plus `CCCSystem.record_dialogue_conclusion` | Runs confirm / refine / "42" rounds with a human and records the conclusion |

Also removed with them: their model classes, store collections, the
constitutional rules `CCC-INFLECTION-001`, `CCC-THREAD-001`,
`CCC-SIMULATION-001` and `CCC-CANON-001`, the CNS connector's four transitions
for them (`canonicalize`, `deprecate_term`, `supersede_term`,
`resolve_inflection`), and their tests.

## Why

CCC's one job is remembering claims over time so a machine cannot rewrite what a
human thought. These five follow CCC's rule (a machine proposes, a human
settles), so they were not off-mission. They were unused, and nothing required
them:

- **No users.** Not one call in any non-archived repo in the account, nor in
  innovation_os (where CCC began). Measured 2026-10-06 by scanning every
  repository's code for these operations; the only CCC operations anything
  calls are `ingest`, `record_external_finding`, `save` and the Triad-42 handoff.
- **Not required by the constitution.** Traced against *The Constitution of
  ≡TACK*, Version 4.0, status **Developed Candidate** (not ratified). No article
  requires CCC to hold turning points, threads or branches, simulations, official
  terms, or a dialogue loop. Article XI §4 permits AI simulation; it does not
  require storing it. Article XXX concerns copies of AI systems, not branches of
  reasoning.

**Kept in CCC on the same trace:** conflicts (Articles XLV, LVI: conflicts are
identified, preserved and recorded until legitimately resolved) and human
resolution of open questions (Article II §4, Article XLVI: unresolved matters
are marked and escalated to a human). Discoveries and road signs stay because
CCC's own repeat-sighting guard uses them.

**Revive one if** the ratified constitution, when it exists, turns out to
require it, or a real consumer appears.

## What's here

- `ccc/`: the six removed modules, verbatim from `85bbc4e`.
- `tests/`: `test_dialogue.py` and `test_dialogue_conclusion.py` verbatim, and
  `test_constitution_removed.py` holding the four tests taken out of
  `tests/test_constitution.py` (they use that file's fixtures).
- `removal.patch`: the complete change to CCC's `ccc/` and `tests/`
  directories, including the edits to shared files (facade, models, store,
  rules, connector, harness, tests).

## Compatibility left behind in CCC

- State files that hold the buried sections still load. The sections are kept as
  read and written back unchanged (`ccc.store.RETIRED_SECTIONS`). Verified by
  saving a file with the old code, filled with every buried type, and
  round-tripping it through the new code: identical.
- Artifacts keep their `thread_id` and `branch_id` fields as plain labels.
- Harness checks H13, H14, H17, H18, H33, H40, H41 and H42 report `RETIRED`.
  Their numbers stay reserved so a revival restores them in place.

## Bringing it back

From a CCC checkout at the removal commit, or later if nothing has since
conflicted:

    git apply -R /path/to/Graveyard/ccc/2026-10-06-unused-record-types/removal.patch

Verified: on the removal commit this restores CCC exactly, with its full
suite passing (808 passed, 1 xfailed with CNS installed). To revive one piece
only, copy its module from `ccc/` and take the matching hunks from the patch.
Then put back its paragraph in CCC's README.
