# Provenance

Everything in this repository traces to the author's own archived AI
conversation history. Nothing was invented to fill a gap. Where the archive
specified a file without writing it, the file is marked RECONSTRUCTED and the
archived specification it derives from is named.

## Source corpus

| Repository | What it holds |
|---|---|
| `wking53214/ChatGPT_History` | ChatGPT exports and transcripts. **Primary source.** |
| `wking53214/Claude_History` | Claude exports, transcripts, derived summaries |
| `wking53214/Gemini_History` | Google Takeout |
| `wking53214/Gemini_Extraction` | normalized message and artifact indexes |
| `wking53214/CoPilot_History` | Copilot transcripts |

The primary artifact is a single extended session:

```
ChatGPT_History/transcripts/6a712900-a744-83ea-b6ef-330c9df41e2c.md
2026-08-03T23:50 to 2026-08-04T02:03
```

UTEP is referenced in later conversations across all five repositories, but
the framework is authored in that one session.

## Classification

### VERBATIM

Reproduced unmodified from the archive, whitespace-trimmed only. No provenance
headers were added to these files so they can be pasted directly into an
instruction field.

| File | Source lines | Words |
|---|---|---|
| `kernel/UTEP_PROTOCOL_v1.0.md` | 1536-1836 | 779 |
| `kernel/UTEP_KERNEL_v1.0.md` | 1941-2147 | 563 |
| `kernel/UTEP_KERNEL_v2.0.md` | 2280-2456 | 446 |
| `variants/plaintext_314w.txt` | 3306-3358 | 314 |
| `variants/primitive_96w.txt` | 3397-3427 | 96 |
| `variants/paragraph_362w.txt` | 3680 | 362 |
| `variants/minimal_99w.txt` | 3716 | 99 |
| `variants/field_verified.txt` | 6126 | 205 |
| `deployments/gemini_personal_intelligence.txt` | 6126 | 205 |
| `standards/punctuation_rule.md` | 5833-5853 | |
| `standards/style_consistency_rule.md` | 5875-5877 | |
| `standards/module_collaboration_principle.md` | 5672 | |
| `memories/*.txt` (all six) | 6353-6404 | 38 to 111 each |

Line numbers refer to the primary transcript above.

`variants/field_verified.txt` is distinguished from the other variants by
being the one the archive records as actually accepted by the target platform.
The user's own words: "This one worked work within its framework."

### RECONSTRUCTED

Not present in the archive as written files. Built to serve a design the
archive specifies.

| Files | Archived basis |
|---|---|
| `core/scheduler.md`, `context.md`, `communication.md`, `execution.md`, `safety.md` | The archive gives this exact file list as the framework's layout, with a one-line purpose for each. Content is assembled from the kernel sections each file is named for. |
| `modules/coding.module.md` | The archive's Refactor Protocol discussion, the "Coding Engineering Standards" draft, Memory 5, and the named token-drain list |
| `modules/research.module.md` | "Research Module: evidence rules, source evaluation" |
| `modules/writing.module.md` | The writing and formatting rules (Memory 4) and the Documentation Architect remit |
| `modules/planning.module.md` | "Strategy Module: decision frameworks" and Memory 3 |
| `modules/architecture.module.md` | The Sentinel OS Architect remit and the layering critique that produced UTEP |
| `gems/*.md` | The roster and per-role remit are attested. The individual briefs are assembled from those remits. |
| `deployments/*` except the Gemini file | The archive's platform-to-field mapping table, filled with Kernel v2.0 content |
| `tools/utep_lint.py` | Written for this reconstruction. Each check derives from a rule the framework states about itself. |
| `docs/*`, `README.md` | Written for this reconstruction. Every quotation is cited to the archive; the analysis is this repository's. |

## Deliberate choices

**The canonical kernel is v2.0, not the longest version.** v1.0 and the
Protocol are preserved but not canonical. The archive is explicit that v2.0
supersedes both on orthogonality grounds, and the word count is a consequence
of that, not the goal.

**Verbatim files carry no provenance header.** A header would be copied along
with the instruction text into whatever field it is pasted into. Provenance
lives in this file instead.

**The Gemini deployment is the field-verified 205-word variant, not the
kernel.** Deploying the kernel there is what the archive shows failing. See
`docs/FIELD_NOTES.md`.

**Rejected variants are kept.** The compression ladder is the evidence for the
field finding. Dropping the failures would leave the conclusion unsupported.

## Not reconstructed

The archive discusses two things this repository does not build:

- **The GAPS / Sentinel OS kernel** that UTEP was extracted from. It is a
  separate system, and the archive's judgment is that mixing it back in is the
  error UTEP corrects. It is referenced in `docs/EVOLUTION.md` as context only.
- **Gem contents beyond their briefs.** Each gem's full instruction set is a
  deployment artifact, not part of the framework.

## Verification

To re-derive the source material:

```bash
grep -rn "UTEP" ~/ChatGPT_History ~/Claude_History ~/Gemini_History
```

The primary transcript is the densest source by a wide margin.
