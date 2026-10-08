# Gems

**Status:** RECONSTRUCTED. The roster is attested across the archive; the
individual briefs are assembled from the responsibilities the archive assigns
each role.

A "gem" is the archive's term for a specialist configuration: a persona with a
narrow remit, loaded on demand, sitting above the kernel and below the task.
Gemini calls them Gems; the same thing is a Custom GPT, a Claude Project, or a
system prompt elsewhere.

## Why they exist

The kernel is small and always loaded. Specialist expertise is large and
rarely needed. Putting the second inside the first is the mistake UTEP was
built to correct.

From the archive, on the original monolithic setup:

> Your original GAPS/GSA block was effectively trying to load kernel, drivers,
> applications, developer tools, workflow automation and governance framework
> into the startup firmware.

## The roster

| Gem | Remit |
|---|---|
| Prompt Engineering Architect | AI behavior design, system prompts, prompt synthesis, optimization. Owns the full UTEP kernel. |
| Sentinel OS Architect | Architecture, governance, design decisions, GSA concepts. |
| Sentinel Engineering Architect | Code changes, refactoring, testing, minimal-change discipline. |
| Documentation Architect | READMEs, technical documentation. |
| Refactor Guardian | Protects against destructive rewrites. |
| Research Intelligence Analyst | Evidence rules, source evaluation. |
| Executive Strategy Advisor | Decision frameworks, tradeoff analysis. |

## The pipeline

Gems are meant to compose, not compete:

```
Prompt Architect
       |
System Architect
       |
Engineering Architect
       |
Documentation Architect
       |
Human decision point
```

Every gem carries the shared principle in
`standards/module_collaboration_principle.md`. Without it a specialist starts
improvising outside its remit, which the archive names as the common failure
mode of multi-persona setups.

## Composition rule

A gem extends the kernel. It never restates kernel rules and never overrides
them. If a gem's instructions conflict with the kernel, the kernel wins.
