# Burial: ANVIL, retired in full

**Repo:** `wking53214/ANVIL` (private at burial)
**Snapshot commit:** `a34e30c` (main), the last live state
**Date:** 2026-10-09
**Decision:** William N. King (A: bury now)

## Why

ANVIL is a single-file governance kernel (`ANVIL.py`, about 2,700 lines) with its own harness and
tests. It was built as an earlier, separate version of ideas that now live in STACK. A usefulness
review of every top-level piece found nothing that needs porting as new code. Each useful idea
already exists elsewhere in STACK, often in a stronger form. Its own kernel also has defects that
would carry into any port.

## Usefulness review (before burial)

A read-only review checked all 67 top-level definitions against every local STACK repo.

| Verdict | Count | Meaning |
|---|---|---|
| Duplicate | 37 | STACK already has it |
| Skip | 21 | Not useful for STACK |
| Hold | 6 | Lineage graph group (DAG, nodes, branches, merge records). No consumer. |
| Done | 3 | Ported or deliberately not ported (see below) |
| Port | 0 | Nothing to bring in as new code |

**Already taken from ANVIL:**
- The per-trace repeat detector, now in sentinel_os `governance_loop_guard.py` (PR #64).
- Named checkpoints, now names on sentinel_os head anchors in `twin_custody.py` (PR #65). The
  in-memory checkpoint registry was deliberately not ported, because it does not survive a restart.

**Stronger versions already in STACK:** the canonical encoder and chain walk in stack-kernel (refuses
floats and duplicate keys), the bounded oscillation guard in dit, the event bus in swizzle, and the
durable audit ledger in sentinel_os.

**The Hold group was not ported.** If a lineage graph is ever needed, it should be designed from a
real consumer, not copied from this file. Its own acyclicity check returns false on valid chains.

## Known defects at time of burial

Recorded so nobody ports them by accident. Items marked "reproduced" were confirmed in a probe.
The rest come from reading the code.

- **High:** a module's returned record is trusted, so it can set its own parent hash, depth and
  governance result (reproduced).
- **High:** a failing module makes the public entry point raise an error instead of returning a
  failure record, so the "fail closed" claim does not hold for those callers (reproduced).
- **High:** disabled modules still run. The kernel ignores the enabled flag (reproduced).
- **High:** the audit trail is never saved. After successful runs the ledger has 0 entries. The
  default audit sink is a no-op, so a missing connection loses audit records silently (reproduced).
- **High:** the default health checks test whether an object exists, which is always true.
- **Medium:** integer key 1 and string key "1" hash the same. Duplicate keys merge silently
  (reproduced).
- **Medium:** naive datetimes hash by the host's time zone, so cross-host verification breaks
  (reproduced).
- **Medium:** tuples inside "frozen" data can still be changed (reproduced).
- **Medium:** some verifiers accept unlinked data or check only that a value is non-empty.
- **Medium:** unbounded memory growth in the DAG, audit list, telemetry list, oscillation sets and
  checkpoints (reproduced).
- **Low:** failure records store full tracebacks, and the oscillation detector prints to stdout.
- **Low:** several interfaces are never used (the failure hook, the event bus, three protocols,
  and the module dependency declarations). They look like features but are not.

## Test status at burial

- `test_anvil.py`: 2 passed. These only check that the code imports.
- `anvil_validation_harness.py`: 27 passed, 5 findings. Of the findings, two are design choices
  (fail-open default, returning versus raising errors), one is a real inconsistency, and two are
  artifacts of how the tests are written. The harness does not cover the failure path through the
  main entry point, where the high-severity defects are.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Full source at the last live state | `snapshot/` (9 tracked files, including LICENSE, NOTICE and CI config) |
| Full history, 27 commits, with pull refs | `anvil-full-history.bundle` |
| Ported ideas | sentinel_os PRs #64 and #65 |

## What's here

- `snapshot/`: all 9 tracked files at `a34e30c`, including LICENSE (Apache-2.0) and NOTICE.
- `anvil-full-history.bundle`: complete history (27 commits) plus pull-request refs. Verified with
  `git bundle verify`, which reports a complete history.

## Bringing it back

- Whole repo with history: `git clone anvil-full-history.bundle anvil`
- Files only: copy `snapshot/`.
