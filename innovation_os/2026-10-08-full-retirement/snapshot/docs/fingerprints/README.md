# Code identity fingerprints

## What this directory is

A fingerprint is a claim about what a system **is**, derived from what its code
**does**, written down in a fixed shape so that claims about different systems
can be compared to each other and to a historical concept.

The archive exists to serve a specific downstream job. Historical ChatGPT and
Claude conversations in this portfolio contain years of evolving discussion in
which names changed, architectures merged and split, and the same acronym meant
different things in different months. Classifying an extracted historical
concept against "which system does this belong to?" cannot be done by keyword
match, because the keywords moved. It needs a stable, code-grounded description
of each system's actual behaviour to compare against. That is what a fingerprint
card is.

## The two halves, kept apart on purpose

**The mechanical half** is `tools/fingerprint/extract_signature.py`. It reads a
source tree's AST without importing or executing anything and emits JSON: class
and enum names, enum members, literal constants, the subset of constants whose
names mark them as tunables, numeric keyword defaults, raised exception types,
imported packages, cryptographic primitive hits, and state-machine vocabulary.
It makes no judgement about any of it. Running it twice on the same tree gives
the same answer.

**The interpretive half** is a card under `cards/`. A human or an agent reads
the mechanical output plus the code it points at and writes down what the system
actually is. This half is arguable, and it is where every mistake will live.

These are kept separate because merging them is the failure mode. Once a
generated description and a hand-written judgement occupy the same field,
nobody can tell which parts were checked and which parts were asserted, and the
archive degrades into the thing it was built to replace.

## The naming trap

Class names in this portfolio are not reliable evidence of behaviour, and the
portfolio already knows it. Two examples, both from code in `sentinel_os`, both
documented by the owner rather than discovered here:

- `sage_k/kernel.py` defines `WorldModel` and `Policy` and its source artifacts
  described "Echo State Network reservoirs" and "Lyapunov Stability Engines".
  The module docstring states plainly that there is no ESN reservoir and no
  Lyapunov exponent calculation in the file: it is tanh-based linear layers and
  a rolling standard deviation used as a volatility proxy.
- `sage_k/gsa_adapter.py` is named and was described as a "cryptographic
  interlock". Its docstring states that it is a deterministic SHA-256 hash chain
  over JSON for tamper-evidence and ordering, with no confidentiality property
  and no key management.

So a fingerprint must separate two things that look identical from the outside:

- **architectural identity** — the shape of the thing, what it is organised to do
- **implementation maturity** — how much of that is actually built

A card that says "predictive ML regime classifier" about a function that returns
a fixed distribution keyed off one input variable is not a fingerprint. It is a
sales sheet, and it will not survive anyone reading the file.

## Evidence classes

Every substantive claim on a card carries one of these tags. A claim with no tag
is a defect.

| Tag | Means |
| --- | --- |
| `[CODE]` | Read directly from source in a named file at a named commit. |
| `[TEST]` | A test exists **and its result was observed in this session**. |
| `[EXPERIMENT]` | Something was run and its output recorded. |
| `[REPOSITORY HISTORY]` | From commit history, branches, or tags. |
| `[EXTERNAL SOURCE]` | From a document, conversation, or handoff, not verified against code. |
| `[INFERENCE]` | A conclusion drawn from evidence, with the evidence named. |
| `[HYPOTHESIS]` | A candidate explanation with insufficient evidence. |
| `[UNKNOWN]` | Not established. This is a legitimate final answer. |

Two distinctions that are easy to lose and expensive to lose:

**A test that exists is not a test that passed.** `[TEST]` requires an observed
result. "The repo has a test suite" is `[CODE]`.

**A conversation is evidence of thought, not of implementation.** "We should add
X" is a proposal. "I built X" is a claim. Neither is `[CODE]`. Where repository
evidence is available it outranks both, and where it contradicts them the
contradiction is the finding and belongs on the card.

## Cross-system reality

A concept does not have to belong to exactly one system, and forcing it to is
how the archive starts lying. The supported classifications are:

- **Single-system** — the concept belongs to one system.
- **Multi-system composition** — e.g. `URE + SYNAPSIS`.
- **Cross-system integration** — e.g. `GSA -> URE`, where one feeds the other.
- **Shared infrastructure** — serves several systems, owned by none.
- **`UNKNOWN / UNCLASSIFIED`** — insufficient evidence.

Systems that share concepts, algorithms, vocabulary, or dependencies still get
separate cards. Collapsing two cards because the systems look similar destroys
exactly the distinction the archive exists to preserve. `OBSERVE` and the
handoff's description of `URE` both center on an `OperationalRegime` enum; they
are still two systems, and the overlap is recorded as an overlap rather than
resolved by merging them.

## Using it

```bash
python tools/fingerprint/extract_signature.py <path-to-source> > signature.json
```

Then read `signature.json` alongside the code it points at, and write a card
following `FINGERPRINT_SCHEMA.md`. Register the card in `MASTER_ARCHIVE.md`.

## The standard the archive is held to

The purpose is not to produce a plausible account of the portfolio. It is to
reconstruct the architecture accurately enough that the resulting map survives
someone hostile reading the code to check. When the evidence does not reach,
the correct entry is `UNKNOWN`.
