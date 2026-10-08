# EVIDENCE POLICY

A direct source record is grade **A** only for what that record actually establishes.

| Grade | Meaning |
|---|---|
| A | Direct source record. Establishes that the statement appears in the corpus at a given index and time. |
| B | Derived from source records by stated reasoning, or inferred from a successor specification. |
| C | Weakly supported. Consistent with the corpus but resting on a single ambiguous record. |
| U | Unknown. Recorded as a gap. |

Grades describe what the corpus establishes. Content in `proposals/` is therefore **ungraded**: it is
design work written after the fact and makes no claim about what ARLF was. The citation identifying
the gap each proposal addresses is graded normally, at A. A proposal never upgrades, closes, or
amends a `U`.

## Specific limits observed in this repository

**Specification is not implementation.** Grade A on the *Birth and Structure of ARLF* document
establishes that the document exists and what it says. It establishes nothing about whether the
framework was built, could be built, or was ever executed. The corpus contains no ARLF code, no
loss function, no benchmark, and no run log. `executable_implementation` is
`UNKNOWN_NONE_IN_CORPUS`.

**Retention is not validation.** Grade A on the 2026-04-14 terminology list establishes that ARLF
was a named component of the architecture on that date. It does not establish that the Black
Paper's objections were answered. They were not; no record in the corpus addresses them
technically.

**Simulated critique is grade A as a record, U as a claim about its authors.** That the corpus
contains a critique attributed to a named individual is grade A. That the individual holds that
view is `U` and outside the scope of this archive.

**Two expansions of the acronym coexist, and choosing between them is editorial.** "Affective
Recursive Loop Framework" and "Architectural Recursive Logic Feedback" both appear in grade-A records,
days and weeks apart, without either being retracted. That both appear is grade A. That the
architectural reading is the canonical one is a **determination by this repository**, argued in
`NOMENCLATURE.md` from the review record, the structural seeds, the realized stack and the post-purge
persistence. It is not a source statement and carries no grade. The affective branch is preserved at
equal grade in `spec/variant/` rather than deleted, and the previously selected peak date is retained
in `reports/PEAK_CAPACITY.md` rather than overwritten, so the determination can be reversed against the
same evidence.

**Post-purge persistence of the architectural reading is grade A only for the summary date.**
`ARLF-01575` establishes that on 2026-06-04 a summary of White Paper v1.0 described ARLF as
Architectural Recursive Logic Feedback and its doctrine as current. Whether the white paper itself was
authored before the 2026-05-30 purge is `U`.

**Successor inversion is grade B.** That the Joy Dial and the Layer 5 Sycophancy Filter block what
ARLF was built to do is visible by comparing specifications. That they were built *in response to*
ARLF is not stated in the corpus and is graded B.

**A gap with a proposed fix is still a gap.** `proposals/` addresses the RLCF underspecification and
the Authority Gap. Both remain recorded as open in `spec/` and `reports/`, because both were open in
the period the archive covers. Reading a later fix back into the record would be exactly the
back-projection the opening rule of this policy prohibits.
