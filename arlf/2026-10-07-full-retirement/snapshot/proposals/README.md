# Proposals

`NEW WORK` · not sourced from the archive · carries no evidence grade

Everything else in this repository reconstructs what the Gemini corpus says. This
directory does not. It contains original design work addressing the two gaps the
archive records as unresolved, and it is kept separate so that the distinction
between reconstruction and invention stays visible at the directory level.

| Document | Fixes | Archive record of the gap |
|---|---|---|
| `RLCF_SPECIFICATION.md` | RLCF named as a mechanism and never specified | `ARLF-03349`, entity status `NAMED_ONLY` |
| `AUTHORITY_GAP_RESOLUTION.md` | No protocol for a valid unknown; the Loop of the Absurd | `ARLF-01575`, Ghost Problem 2 |
| `reference/` | Runnable implementation of both, with tests | n/a |

## What these are not

**They are not reconstructions.** No record in the 4,911-record corpus contains
any of this content. Nothing here is evidence about what ARLF was, and nothing
here changes the archive's finding that the framework was never implemented.

**They do not close the historical gaps.** `spec/` and `reports/` continue to
record both gaps as open, because they were open. A gap that someone later
proposed a fix for is still a gap in the record. The archive documents 2026; this
directory is a response to it.

**They are not the only possible fixes.** Each document states its design
alternatives and why the chosen one was preferred. Both are arguable.

## Provenance status

Documents here carry `PROPOSAL`. Under `EVIDENCE_POLICY.md` that status takes no
grade: A through U describe what the corpus establishes, and these claims are not
about the corpus. What can be graded is the accuracy of the gap each one
addresses, and those citations are grade A.

## Reference implementation

`reference/` holds a dependency-free Python implementation of both proposals with
64 tests. It exists because a fix for "named but never specified" is not credible
as prose alone. Running it:

```
cd proposals/reference
python3 -m unittest discover -s tests -t .
```

The implementation is a demonstration of semantics, not a production component.
It is propositional, single-process, and deliberately small. What it establishes
is that the two proposals are coherent and that their central invariants hold
under test, including the one that matters most: a claim the substrate cannot
settle never comes back as false.

One note on how it was built. The charity term was first written as a credit
subtracted from the penalty when a candidate handed over a certificate. A test
caught that this can never reward anything, because a candidate already clean on
the other terms sits at zero and subtracting from zero distinguishes nothing. It
was rebuilt as an overclaim penalty on the candidate that withholds the
certificate. That correction is recorded in `RLCF_SPECIFICATION.md` and in the
module docstring, because a design that was wrong once is worth knowing about.
