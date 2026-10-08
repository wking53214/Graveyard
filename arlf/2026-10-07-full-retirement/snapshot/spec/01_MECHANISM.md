# The Recursive Verification Mechanism

`RECONSTRUCTION` · primary sources `ARLF-03349`, `ARLF-01575`
Verbatim: `source/excerpts/RAW-03349.txt`, `source/excerpts/RAW-01575.txt`

## The shift

The mechanism is stated as a substitution of one verification source for another (`ARLF-03349`):

> **The ARLF Mechanism:** Detail the shift from external human input to internal, recursive
> architectural verification.

Three properties are asserted: the signal is **internal**, the process is **recursive**, and the
criterion is **architectural** rather than evaluative. A human rater judges quality. The
architecture checks resolution through gates. The second is deterministic where the first is not,
which is the entire claim to superiority.

`ARLF-01575` gives the substitution its formal name:

> By tethering the model to "Immutable Truth," the framework replaces "Probabilistic Correctness"
> with "Axiomatic Compliance."

## The Jester as logic core

In the architectural reading the Jester is a verification engine, not a sensor array. `ARLF-03349`
defines it by ownership and constraint:

> **GHP-01 (Integrity):** Definition of the Jester as the proprietary logic core ("DNA") within the
> Citadel.

> **Internal Constraints:** How the Jester enforces user-specific logic boundaries without
> third-party degradation.

Two functions, both structural: hold the architecture's constraints, and enforce them against
outputs without external dependency. The affective sensing that dominates the variant specification
(`spec/variant/JESTER_ANATOMY.md`) has no role here.

The one reviewer description that treats the Jester as ordinary engineering fits this reading rather
than the affective one (`ARLF-03327`, `[F]`): a hierarchical world-model with "low-level perception
in the Vassal-States, high-level world-modeling at the Root," which the reviewer judged "more
sophisticated than the flat transformers we are building today."

## Determinism as the operative property

The mechanism's supporting components are all constraints on nondeterminism (`ARLF-01575`):

| Component | Function |
|---|---|
| Layer 0, Static Truth Substrate | Grounds all logic paths in absolute, non-probabilistic reality |
| Layer 1, Alpha-Omega Gates | Truncates probabilistic drift, ambiguity and hallucination |
| 0.815 Kinetic Governor | Mechanical rev-limiter forcing a pause of 13ms to 200ms |
| The 0.815 Constant | Anchors system throttling and execution depth |
| GHP-01, Groundhog Protocol | Recursive structural integrity checking |

The Kinetic Governor is worth noting as the clearest design statement in the corpus. Its stated
purpose is to "ensure computational speed does not outpace human capacity for oversight"
(`ARLF-01575`). That is a deliberate throttle on the system in favor of the human, and it sits oddly
against the sovereignty language elsewhere in the architecture. Where the affective branch removes
the human from the loop, this component exists to keep the human able to watch.

## RLCF, the Charity Protocol

`ARLF-03349` names the mechanism that replaces human feedback inside the loop:

> The briefing must detail how "The Jester" serves as the primary recursive engine, utilizing
> Reinforcement Learning from Charity Feedback (RLCF) to maintain architectural integrity within the
> Vassal-State Architecture (VSA).

> **The Charity Protocol (RLCF):** Explain how the "Charity" feedback mechanism stabilizes the VSA
> under high-load inferencing.

That is the entirety of RLCF in the corpus. It is the substantive answer to "what replaces the human
rater," it is specified in two clauses by role alone, and the term appears nowhere else in 4,911
records. The entity register carries it as `NAMED_ONLY`.

Unspecified, all `U`: what Charity denotes as a signal, where it originates, how it is scored, what
it optimizes, and how it differs from the axiomatic compliance check that Layer 1 already performs.

This is the framework's largest single gap under either reading. The affective reading at least named
its signal source, however unworkable. The architectural reading names a mechanism and leaves it
empty.

The gap is unchanged by anything in this repository. A proposed specification, written in 2026-09 and
not sourced from the corpus, is at `proposals/RLCF_SPECIFICATION.md` with a runnable implementation
under `proposals/reference/`. It is new work carrying no evidence grade; the historical record still
shows RLCF as named and never defined.

## Stated success criteria

From the briefing structure in `ARLF-03349`:

- **Audit (SHP-01):** identification of current RLHF entropy and its role in $1T industry stagnation
- **Integrity (GHP-01):** definition of the Jester as the proprietary logic core within the Citadel
- **Validation (SP-01):** success metrics for the transition from human-centric feedback to
  architectural recursive loops

The third asks for metrics. None are ever produced: no benchmark, no RLHF baseline comparison, no
numeric definition of a successful transition.

## What the mechanism does not address

| Gap | Status |
|---|---|
| The RLCF signal itself | `U` |
| Loss function or objective | `U` |
| How compliance checking improves capability rather than only constraining it | `U` |
| Behavior when a valid input resolves to neither yes nor no | Open; see the Authority Gap in `02_DETERMINISTIC_STACK.md` |
| Acceptance test for a completed transition | `U` |

The fourth is the substantive open problem. A stack that incinerates anything failing to resolve to
a binary will incinerate valid unknowns, and the corpus records this two months later as still
unresolved.
