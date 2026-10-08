# Evolution

UTEP was developed across a single extended session on 2026-08-03 and
2026-08-04, then referenced and refined in later conversations. Six distinct
phases are recoverable from the archive.

## Phase 1: the protocol (779 words)

Begins as **Universal Token Efficiency Protocol v1.0**: a twelve-section
document covering objective focus, proportional reasoning, information
density, context management, clarification policy, adaptive effort, tool
efficiency, communication rules, resource allocation, quality preservation,
response structure, and termination.

Complete, and too long. `kernel/UTEP_PROTOCOL_v1.0.md`.

## Phase 2: kernel, not prompt (563 words)

The reframe that gave the project its shape. Rather than a single large
prompt, a small stable kernel with domain modules inheriting from it:

```
Kernel
  -> Domain Module
    -> Task Instructions
      -> User Request
```

The archive's directory layout for the framework is specified here, and is
what `core/` and `modules/` reconstruct. `kernel/UTEP_KERNEL_v1.0.md`.

## Phase 3: orthogonality (446 words)

The key revision, and the sharpest architectural statement in the archive:

> The biggest improvement isn't making it shorter. It's making it more
> orthogonal. Every rule should have exactly one responsibility, with no
> overlap. That reduces ambiguity and makes the behavior easier for different
> LLMs to apply consistently.

v2.0 is 117 words shorter than v1.0 and loses nothing, because what it cuts is
duplication rather than content. This is the canonical kernel.
`kernel/UTEP_KERNEL_v2.0.md`.

## Phase 4: the compression ladder

An attempt to load the kernel into Gemini's Personal Intelligence field
produced a sequence of progressively stripped variants, each rejected:

| Variant | Words | Removed | Result |
|---|---|---|---|
| `variants/paragraph_362w.txt` | 362 | all markdown structure | rejected |
| `variants/plaintext_314w.txt` | 314 | headings, bullets, arrows | rejected |
| `variants/primitive_96w.txt` | 96 | punctuation, numbering, titles | rejected |
| `variants/minimal_99w.txt` | 99 | kernel framing entirely | **accepted** |
| `variants/field_verified.txt` | 205 | nothing; grown from the accepted form | **accepted** |

The finding is in `docs/FIELD_NOTES.md`. It is not a length limit.

## Phase 5: the split

Rejection forced the question the architecture had been avoiding: what
actually belongs in an always-on layer?

The answer separates **behavior** from **expertise**. The persistent layer
carries how the system communicates. Specialists carry what it knows. From the
archive:

> You would not put your printer driver into the operating system kernel. It
> works, but it makes the whole system heavier and more fragile.

This produced the gem roster in `gems/`.

## Phase 6: the memory array

The final deployment form. Rather than one persistent block, six focused
memories, each with a single responsibility, in priority order:

1. Core Communication Style
2. Technical Discussion Preferences
3. AI Efficiency Behavior
4. Decision and Option Framework
5. Technical Work and Coding Behavior
6. AI Module Collaboration

`memories/`. The archive notes the first three carry most of the value, and
the last three belong in gems if the platform starts rejecting additions.

This is the same orthogonality principle from Phase 3, applied one layer up:
the kernel was made orthogonal internally, then the deployment was made
orthogonal across fields.

## What UTEP replaced

The original configuration was a single block that the archive diagnoses as
trying to be three things at once:

> 1. A governance kernel
> 2. A Gemini operating manual
> 3. A workflow router / command menu
>
> That creates instruction competition.

Everything sat at the same priority: kernel concepts, menu routing, formatting
rules, persona constraints, token optimization, code transportation behavior.
UTEP is the decomposition of that block into layers.
