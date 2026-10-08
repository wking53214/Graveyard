# Architecture

## The layer stack

```
  kernel/         universal behavior, always loaded, never overridden
      |
  standards/      absolute formatting rules, attach to the kernel
      |
  core/           the kernel's own subsystems
      |
  modules/        domain expertise, loaded when relevant
      |
  gems/           specialist roles, invoked deliberately
      |
  task            the request
```

Each layer may specialize the one above it. No layer may violate it. When
instructions conflict, the higher layer wins.

## Why layers at all

The framework exists because a single monolithic instruction block fails in a
specific way. The archive names it **instruction competition**: when a
governance rule, a formatting preference, and a workflow router all sit at the
same priority, the model has no basis for resolving a conflict between them,
so it resolves it arbitrarily.

Layering supplies the missing basis. Two rules in conflict are resolved by
which layer they came from.

## The design principle

Stated in the archive while revising v1.0 into v2.0:

> Every rule should have exactly one responsibility, with no overlap. That
> reduces ambiguity and makes the behavior easier for different LLMs to apply
> consistently.

Orthogonality is why v2.0 is shorter than v1.0 without losing anything. What
it cut was duplication.

The same principle reappears at deployment scale in `memories/`: six focused
blocks rather than one combined block, for the same reason.

## What goes where

| Layer | Answers | Size | Changes |
|---|---|---|---|
| kernel | How should the system behave, always? | 300 to 500 words | Rarely |
| standards | What formatting is non-negotiable? | Under 200 words each | Rarely |
| core | How does the kernel allocate effort, context, output? | Under 500 words each | Rarely |
| modules | How should it behave in this domain? | Under 500 words each | Per domain |
| gems | Who is doing this work? | Under 400 words each | Per role |
| task | What is being asked? | Any | Every request |

The test for placement: if a rule only applies sometimes, it is not kernel. If
a rule applies to a role rather than a domain, it is a gem, not a module.

## The inheritance contract

A lower layer may:

- specialize a kernel rule for its domain
- add rules the kernel does not address
- narrow a kernel permission

A lower layer may not:

- restate a kernel rule (`tools/utep_lint.py` warns on this)
- contradict a kernel rule
- reorder the priority hierarchy in `core/safety.md`

Restating is worth catching even though it is harmless in isolation. Two
copies of a rule drift, and once they drift the conflict is silent.

## Composition

Loading the kernel plus a coding module plus an engineering gem should produce
one coherent instruction set, not three overlapping ones. That works only if
each layer stays inside its remit, which is what the collaboration principle
in `standards/module_collaboration_principle.md` enforces across gem
boundaries: preserve objectives, constraints, decisions, assumptions, and
unresolved questions so the next specialist continues rather than restarts.

Without it, the archive notes a specific failure: one specialist "starts
improvising outside its responsibility".
