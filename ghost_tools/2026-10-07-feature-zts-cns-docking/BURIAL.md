# Burial: ghost_tools branch `feature/zts-cns-docking`

**Repo:** `wking53214/ghost_tools`
**Branch tip:** `6c6bb8e` (2026-10-06), the last state of the branch
**Forked from:** `d14dc1a` (main at v1.7.0, 2026-09-11)
**Date:** 2026-10-07
**Decision:** William N. King

## Why

The branch held refactors only: 15 commits pulling helper functions out of
long ghost_buster functions, plus one later "restore" commit. No features.

It was squash-merged into main as PR #78 on 2026-10-05, while 48 commits
behind main. The squash overwrote newer main code in 8 ghost_buster modules
(boundary, cli, correlate, ledger, mechanical, mutation, secrets, structure)
and attached two `@connector` decorators to helper functions instead of the
correlators. Main went from passing to 70 failing tests.

PR #82 repaired main by restoring those 8 files to `960f24f` (the last
commit before #78). After that, the branch held nothing main needs, and its
tip was worse than main, so it no longer belongs in ghost_tools.

## What's here

- `feature-zts-cns-docking.bundle`: the branch with its complete history
  (88 commits), self-contained. Does not need ghost_tools to restore.
- `branch-changes.patch`: everything the branch changed relative to where it
  forked (`d14dc1a`), readable without git.

## Known issues at time of burial

Recorded so a revival starts from the truth:

- The refactors were written against v1.7.0. Main has since changed the same
  functions heavily, so they cannot be re-applied as-is. Redo them against
  current main, one function at a time, with the mutation suite run after each.
- Commit `b8ed4df` and `d3af337` move `@connector` onto `_build_*` helpers.
  Commit `1662a95` fixes the same mistake for one `@register`, but the two
  connectors were never fixed on this branch.
- The tip (`6c6bb8e`) does not run: `Tests/test_correlate.py` alone shows 33
  failures, because it restores v1.7.3 code onto a v1.7.0 base.
- The name says "CNS docking", but no CNS work is on this branch. The real
  CNS adapter landed on main separately (`2f6b01d`).

## Bringing it back

- With history: `git clone -b feature/zts-cns-docking feature-zts-cns-docking.bundle`
- Or into an existing ghost_tools checkout:
  `git fetch <path>/feature-zts-cns-docking.bundle feature/zts-cns-docking:feature/zts-cns-docking`
