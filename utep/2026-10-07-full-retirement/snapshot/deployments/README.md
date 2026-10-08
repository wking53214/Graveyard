# Deployments

One kernel, one artifact per platform. Each file is ready to paste into the
field named in its header.

| File | Platform | Field | Source variant |
|---|---|---|---|
| `gemini_personal_intelligence.txt` | Gemini | Personal Intelligence | `variants/field_verified.txt` (verbatim) |
| `chatgpt_custom_instructions.md` | ChatGPT | Custom Instructions, or a Custom GPT system prompt | Kernel v2.0 |
| `claude_project_instructions.md` | Claude | Project Instructions | Kernel v2.0 |
| `CLAUDE.md` | Claude Code | repository root | Kernel v2.0 + coding module |
| `.cursorrules` | Cursor | workspace rules | Kernel v2.0 + coding module |
| `copilot-instructions.md` | GitHub Copilot | `.github/copilot-instructions.md` | Kernel v2.0 + coding module |

## Platform capability, from the archive

| Platform | Persistent behavior instructions |
|---|---|
| ChatGPT | Yes. Memory plus Custom Instructions, plus system prompts for a Custom GPT. |
| Gemini | Yes. Personal Intelligence. Tight acceptance boundary, see `docs/FIELD_NOTES.md`. |
| Claude | Partial. Project Instructions, or a system prompt via API. |
| Claude Code | Yes. `CLAUDE.md` at repository root. |
| Cursor | Yes. Workspace rules / `.cursorrules`. |
| GitHub Copilot | Partial. Repository instruction files. |

## Sizing

The archive's guidance on persistent instruction length:

- **250 to 400 words**: ideal for most platforms.
- **500 to 700 words**: workable where instruction space is generous.
- **1,000+ words**: diminishing returns unless building a specialized agent.

Kernel v2.0 is 446 words. The Gemini deployment is 205. Neither is an accident.

## Rule

Do not paste the full kernel into a platform's always-on field and also load
domain modules. That is the monolith UTEP exists to break up. The always-on
layer carries behavior and preferences. Specialists carry expertise.
