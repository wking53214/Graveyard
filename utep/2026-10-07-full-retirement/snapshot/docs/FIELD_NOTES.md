# Field notes

Observations recorded while deploying UTEP to real platform fields. These are
empirical, from the archive, not design intent.

## The Gemini acceptance boundary

Loading the kernel into Gemini's Personal Intelligence field failed
repeatedly. The rejection pattern rules out the obvious explanation.

**What was tried, in order:**

| Attempt | Words | Result |
|---|---|---|
| Kernel v2.0 with markdown | 446 | rejected |
| Same content, one paragraph, no formatting | 362 | rejected |
| Plain text, no headings or bullets | 314 | rejected |
| Primitive: no punctuation, no titles, no numbering | 96 | rejected |
| Plain behavioral description, no kernel framing | 99 | **accepted** |
| The accepted form, grown with targeted additions | 205 | **accepted** |
| The 205-word form plus two more sentences | 223 | rejected |
| A trimmed version of those same additions | 215 | rejected |

**The finding.** A 96-word version was rejected and a 205-word version was
accepted. Length is not the constraint.

The variants that were accepted describe desired behavior in plain terms. The
variants that were rejected declare a governing system: "operate as a
universal efficiency layer", "this kernel defines universal behavior", "when
instructions compete, prioritize". The archive's reading:

> Words like "universal efficiency layer", "instructions compete", and
> "priority" resemble system prompt injection patterns.

**Practical rule.** In a consumer-facing persistent field, write preferences,
not architecture. Say what you want, not what the instruction set *is*. Save
kernel framing for developer surfaces: API system prompts, Project
instructions, `CLAUDE.md`, `.cursorrules`.

**Caveat.** This is behavior observed on one platform on 2026-08-04. Acceptance
boundaries move. Treat it as a testable hypothesis, not a specification.

## The additive ceiling

Once a version was accepted, adding two sentences broke it. Rephrasing those
sentences did not help. The archive's conclusion:

> Gemini Personal Intelligence is accepting your original style, but small
> additions are pushing it over the limit.

This is what drove Phase 6. When one field cannot hold the framework, the
framework splits across several fields rather than compressing further.
Compression had already been shown not to work.

## Format sensitivity is real but secondary

Removing markdown, arrows, and special characters changed nothing on its own.
Worth doing for a plain-text field, but it is not the lever.

## Where the kernel actually fits

From the archive:

> Your original design was actually closer to a system prompt for an AI agent
> framework, not a personal preference layer. Gemini Personal Intelligence is
> better treated like a "BIOS preference profile", not the operating system
> itself.

The full kernel belongs in a custom Gem, an API system prompt, a Claude
Project instruction, a Cursor rule file, or an agent framework. Not in a
consumer preference field.
