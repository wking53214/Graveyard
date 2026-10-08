# Deployment

## Choose by surface, not by preference

Two kinds of field exist, and they take different artifacts.

**Developer surfaces** accept kernel framing: API system prompts, Claude
Project instructions, `CLAUDE.md`, `.cursorrules`,
`.github/copilot-instructions.md`, Custom GPT system prompts. Use
`kernel/UTEP_KERNEL_v2.0.md` or the matching file in `deployments/`.

**Consumer preference fields** may reject it. Gemini's Personal Intelligence
rejected every kernel-framed variant tested, including a 96-word one, while
accepting a 205-word plain behavioral description. Use
`deployments/gemini_personal_intelligence.txt`. The evidence is in
`FIELD_NOTES.md`.

## Recommended setup

**One field available.** Deploy the platform file from `deployments/`. Stop
there. Do not append domain modules.

**Multiple memory slots.** Deploy `memories/` in priority order. The first
three carry most of the value. If the platform starts rejecting additions,
move 4 through 6 into gems rather than compressing them.

**Full framework.** Kernel in the always-on field. Gems for specialist roles.
Domain modules inside the gems that need them. Task instructions per
conversation.

## Sizing

From the archive:

- 250 to 400 words: ideal for a persistent instruction on most platforms
- 500 to 700 words: workable where instruction space is generous
- 1,000+ words: diminishing returns unless building a specialized agent

Kernel v2.0 is 446 words. Protocol v1.0 is 779, which is why v2.0 exists.

## Verifying a deployment

```bash
python tools/utep_lint.py
```

Checks em dash compliance, per-layer word budgets, and layer discipline
(a module or gem restating kernel text).

Behavioral checks the linter cannot do, worth running by hand after any
deployment:

1. Ask something trivial. The answer should be short, with no preamble.
2. Ask something genuinely complex. The answer should get longer. If it does
   not, the effort scaling is not taking.
3. Ask a question that depends on something decided earlier in the session.
   It should not be re-derived.
4. Ask for options. They should arrive as lettered choices with tradeoffs and
   a recommendation, not a bare list.
5. Check any output for the em dash character.

Failure on 2 is the common one. Efficiency instructions tend to over-apply,
producing terse answers to questions that deserve depth. The counterweight is
in `core/safety.md`: when brevity conflicts with correctness, choose
correctness. If a deployment is failing check 2, that sentence is the one to
restore.
