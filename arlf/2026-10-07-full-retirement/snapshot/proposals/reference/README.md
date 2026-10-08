# Reference Implementation

`NEW WORK` · standard library only · no dependencies

A runnable implementation of the two proposals in the parent directory. Python
3.11 or later.

```
cd proposals/reference
python3 -m unittest discover -s tests -t .
```

64 tests, all passing. Also runs under `pytest` if preferred.

## Modules

| Module | Role |
|---|---|
| `arlf/resolution.py` | The three terminal verdicts; invariants enforced at construction |
| `arlf/certificate.py` | Non-resolution certificates, cause taxonomy, escalation targets |
| `arlf/substrate.py` | Layer 0 facts and rules; growth only by steward discharge |
| `arlf/gates.py` | Layer 1 epistemic gate, Layer 3 sphere sovereignty, Layer 2 ingestion |
| `arlf/governor.py` | The 0.815 Kinetic Governor: step budget and Liturgical Pause |
| `arlf/rlcf.py` | The Charity Protocol objective and ranking |
| `arlf/pipeline.py` | `admit`, `resolve`, `select` wired together |

## What it demonstrates

The derivation engine is propositional forward chaining, deliberately minimal. The
point is not expressive power; it is that the semantics of both proposals are
concrete enough to test and that their invariants hold:

- Resolution is total over three verdicts and always terminates.
- A claim the substrate cannot settle never comes back as false.
- Divergent substrates terminate with `BUDGET_EXHAUSTED` rather than looping.
- Every `UNDECIDED` carries a cause, a blocking detail, and a discharge condition.
- The substrate never ingests its own conclusions.
- The flattering candidate loses to the useful one at identical structural quality.

## What it is not

Not a production component. Single-process, propositional, no persistence, no
concurrency, and no connection to any model. It implements the decision semantics
described in the proposals and nothing beyond them.

It is also not evidence about ARLF. The archive contains no implementation of any
kind; this one was written in 2026-09 in response to the gaps the archive records.

## Example

```python
from arlf import Substrate, Literal, Rule, resolve, Discharge

s = Substrate(rules=[Rule((Literal("licensed"),), Literal("may_operate"), "r1")])

print(resolve("may_operate", s))
# UNDECIDED [UNDERDETERMINED] a steward settles may_operate directly, or supplies
#                             the missing intermediate rule

print(resolve("solvent", s))
# UNDECIDED [MISSING_AXIOM] a steward supplies an axiom bearing on 'solvent', or a
#                           rule connecting it to existing vocabulary

s.discharge(Discharge(Literal("licensed"), "steward:wking53214", "verified against the register"))

print(resolve("may_operate", s))
# RESOLVED_TRUE <- r1: licensed |- may_operate
```

The two `UNDECIDED` causes differ because `may_operate` appears in the substrate's
vocabulary through the rule while `solvent` appears nowhere. The first needs an
existing premise settled; the second needs new vocabulary. They escalate with
different requests, which is the reason the taxonomy separates them.
