# UTEP

**Universal Token Efficiency Protocol / Kernel**

A portable behavioral layer for AI systems. It governs *how* a model operates,
not *what* it accomplishes: maximize useful output per token while preserving
correctness, safety, and task completion.

This repository is a reconstruction. UTEP was designed, revised, and deployed
across the author's AI conversation history in August 2026, but existed only
as text pasted into platform fields and quoted back across conversations. It
never had a repository. This is that repository, rebuilt from the archived
source. See [PROVENANCE.md](PROVENANCE.md) for what is verbatim and what is
reconstructed.

---

## The idea

Most attempts at a persistent AI instruction end up as one large block mixing
behavior, formatting, domain rules, and workflow routing. The archive names
the failure mode: **instruction competition**. Everything sits at the same
priority, so conflicts get resolved arbitrarily.

UTEP separates the block into layers with a defined precedence:

```
  kernel          universal behavior, always loaded
    -> standards  absolute formatting rules
    -> core       the kernel's own subsystems
    -> modules    domain expertise, loaded when relevant
    -> gems       specialist roles, invoked deliberately
    -> task       the request
```

A lower layer may specialize a higher one. It may never violate it.

## The governing axiom

> Every action must measurably advance the user's objective.
> Every token must justify its existence.

And the sentence that keeps it honest:

> When brevity conflicts with correctness, choose correctness.

## Quick start

**One instruction field.** Copy the file for your platform from
`deployments/` and paste it in. Done.

| Platform | File |
|---|---|
| ChatGPT | `deployments/chatgpt_custom_instructions.md` |
| Claude | `deployments/claude_project_instructions.md` |
| Claude Code | `deployments/CLAUDE.md` |
| Cursor | `deployments/.cursorrules` |
| GitHub Copilot | `deployments/copilot-instructions.md` |
| Gemini | `deployments/gemini_personal_intelligence.txt` |

**Multiple memory slots.** Deploy `memories/` in numbered order. The first
three carry most of the value.

**Full framework.** Kernel in the always-on field, gems for specialist roles,
domain modules inside the gems that need them. See
[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## Layout

```
kernel/      the canonical kernel, all three archived versions
standards/   punctuation, style consistency, module collaboration
core/        scheduler, context, communication, execution, safety
modules/     coding, research, writing, planning, architecture
gems/        seven specialist role briefs
memories/    the six-memory deployment array
variants/    the compression ladder, including what was field-verified
deployments/ one ready-to-paste file per platform
docs/        architecture, evolution, deployment, field notes
tools/       utep_lint.py
```

## Versions

| Version | Words | Status |
|---|---|---|
| `kernel/UTEP_PROTOCOL_v1.0.md` | 779 | Original. Complete and too long. |
| `kernel/UTEP_KERNEL_v1.0.md` | 563 | The kernel reframe. Introduced inheritance. |
| `kernel/UTEP_KERNEL_v2.0.md` | 446 | **Canonical.** Orthogonal: every rule has one responsibility. |

v2.0 is shorter than v1.0 and loses nothing, because what it cut was
duplication. That is the whole design thesis in one diff.

## The field finding

A 96-word version of this kernel was rejected by Gemini's Personal
Intelligence field. A 205-word version was accepted.

Length was not the constraint. The rejected variants declare a governing
system ("operate as a universal efficiency layer", "when instructions
compete, prioritize"). The accepted ones describe desired behavior in plain
terms.

**Practical rule:** in a consumer preference field, write preferences, not
architecture. Save kernel framing for developer surfaces. The full evidence,
including the additive ceiling that forced the six-memory split, is in
[docs/FIELD_NOTES.md](docs/FIELD_NOTES.md).

## Lint

```bash
python tools/utep_lint.py
```

Checks the repository against its own rules: em dash compliance, per-layer
word budgets, and layer discipline. It currently reports one warning, on
`UTEP_PROTOCOL_v1.0.md` for exceeding the kernel word target. That is
accurate, and it is why v2.0 exists.

An error exits non-zero; a warning does not. CI runs the same command on every
push and pull request, so an em dash or a file over its layer's hard word limit
fails the build. See [.github/workflows/lint.yml](.github/workflows/lint.yml).
