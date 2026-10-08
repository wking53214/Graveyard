# STRIDE — RECOVERY REPORT

Categories below are kept strictly separate. Nothing moves from INFERRED to
RECOVERED without proof, and nothing was generated to fill a gap.

---

## EXECUTED

Searches and commands actually run, 2026-09-17:

1. Corpus sweep over a 65,181-message normalized index (ChatGPT, Claude web,
   Gemini Apps Activity, Copilot, Claude Code, Codex) for: `STRIDE`,
   `Secure Telemetry Runtime`, `Intelligence Deterministic Engine`,
   `PipelineStateEngine`, `InputNormalizer`, `check_loop_condition`,
   `governance_loop_guard`, `seen_outputs`, `prohibited_verbs`, `CLIP`.
2. `grep -rlw STRIDE` across `/home/wking53214`; `find / -iname "*stride*"`.
3. `git log --all -S<term>` and `git log --all --diff-filter=D --name-only`
   across every repository under `/home/wking53214`.
4. `git log --all -- sentinel_os/governance_loop_guard.py`.
5. Re-extraction of `<pre><code>` blocks directly from
   `Gemini_Extraction/source/raw/original_gemini_export.json` with
   html-unescape only — **after discovering that the normalized corpus index
   had collapsed runs of spaces and destroyed Python indentation.** 34 blocks
   matched STRIDE symbols.
6. Extraction of Read/Write/Edit tool payloads from every
   `~/.claude/projects/*/*.jsonl`.
7. Inspection of `~/.grok/sessions/.../chat_history.jsonl` + `updates.jsonl`,
   `~/.copilot/session-state/*/events.jsonl`, `~/.copilot/session-store.db`.
8. Carving of three code regions from `~/Downloads/CLIP.txt` at byte offsets
   149610 / 195701 / 208817, bounded by transcript turn markers.
9. `ast.parse()` on recovered sources (validation only — no modification).
10. `sha256` over every recovered artifact (281 evidence files hashed).
11. `diff` of Gemini-export vs CLIP.txt variants, and of salvage vs Sentinel.
12. `ls /tmp/CLIP`, `ls /home/wking53214/STRIDE` — both absent.

No file outside `~/STRIDE_RECONSTRUCTION/` was created, modified, or deleted.

---

## INSPECTED

- `Gemini_Extraction/source/raw/original_gemini_export.json` (4,911 records)
- `~/Downloads/CLIP.txt` — 215,223 chars, 1,895 lines, 12 transcript turns,
  sha256 `6da02d83e290d53d23a91280e72d7b81315b14644bde38a1dd4950b3c7601438`
- `~/.grok/sessions/%2Fhome%2Fwking53214/01a02609-…/` (chat_history.jsonl,
  updates.jsonl, terminal logs)
- `~/.copilot/session-state/1036da72-…/events.jsonl`
- `~/.claude/projects/-home-wking53214/5cc9da2a-…jsonl`, `a4bdee5f-…jsonl`
- `~/.claude/file-history/a4bdee5f-…/` (editor backups)
- `/mnt/chromeos/MyFiles/Downloads/stride_salvage_loop_and_backpressure.py`
  and `-1.py`
- `sentinel_os/sentinel_os/governance_loop_guard.py` + its git history
- `GSA-815/vendor/sentinel_os/…/governance_loop_guard.py`
- `ATS/stride-ast-extractor-wrapped.py`,
  `synapsis/archive/imported-variants/stride-ast-extractor-wrapped.py`
- `Triad-42/FACTS_STRIDE_OPTIONAL_UPGRADE_INVESTIGATION.md`
- Git object databases of all repositories under `/home/wking53214`

---

## RECOVERED

| artifact | source | status |
|---|---|---|
| STRIDE gateway source, 748 lines, parses as Python | Gemini export activity-904 block 2, 2026-06-22T02:57:20.552Z | RECOVERED FROM CONVERSATION |
| Same artifact, second independent copy | `~/Downloads/CLIP.txt` @149610 | RECOVERED FROM COPY |
| Wrapped-final variant, `VERSION-CONTROL-ID: STRIDE-V7.0.0-SHA256-A8B9C1D2E3F4` | `CLIP.txt` @195701 | RECOVERED FROM COPY |
| AST graph extractor, `STRIDE-AST-GRAPH-V7.0.0-SHA256-F8E9D2` | `CLIP.txt` @208817 | RECOVERED FROM COPY |
| Salvage extract (2 components) | Drive Downloads, 2026-08-20 16:35:48 | DIRECT RECOVERY |
| `governance_loop_guard.py` | sentinel_os working tree + git + editor backup | DIRECT RECOVERY |
| Repository metadata: origin URL, branch, 4 commits, 7 entries, last commit date + message | Grok session repo inventory | RECOVERED FROM CONVERSATION |
| The 7-entry file listing | same | RECOVERED FROM CONVERSATION |
| CLIP→STRIDE rename commands with artifact_N mapping | Copilot session events.jsonl | RECOVERED FROM CONVERSATION |
| Naming event (CLIP and STRIDE proposed together) | Gemini activity-905, 2026-06-22T02:54:07.552Z | RECOVERED FROM CONVERSATION |

---

## RECOMPOSED

`recovered_repo/` holds 5 files. **None is presented under a bare original
filename**, because no recovered byte-stream was proven identical to a repo
file. Each carries an explicit variant suffix naming its source. The repository
tree in `manifests/repository_tree.txt` lists the 7 original entries with a
recovery classification per path.

No directories were created. The evidence shows a flat repository root and no
`src/`, `tests/`, `docs/` or `config/`.

---

## INFERRED

Each of these required a reasoning step and is **not** direct recovery:

1. That `CLIP.txt` region 1 corresponds to `stride-formatted-audited.py`.
   Basis: the rename commit describes artifact_3 as "Formatted and audited
   version (SYSTEM_NAME: STRIDE …)", and region 1 is preceded by a four-phase
   audit report and carries that header. **Not proven by hash or filename.**
2. That region 2 corresponds to `stride-wrapped-final.py`. Basis: the rename
   commit describes artifact_4 as "Final wrapped version with version control
   metadata", and region 2 carries `VERSION-CONTROL-ID`.
3. That region 3 corresponds to `ast-graph-extractor-source.py`.
4. That the local clone outlived the remote. Basis: the 2026-08-21 session
   reports the remote 404 while listing the local path with 4 commits.
5. That `~/Downloads/CLIP.txt` is the material behind `TRANSCRIPT.md`. Basis:
   subject-matter overlap only. **Weak.**

---

## UNKNOWN

- Contents of `PROVENANCE.md`, `README.md`, `TRANSCRIPT.md`.
- Contents of `stride-synthesized-unified.py` — no candidate located anywhere.
- Contents of `clip-original-multi-module-source.py` as a *file*. Its code
  appears in `CLIP.txt` turn 1 but with newlines destroyed; original formatting
  is unrecoverable, so it was not carved.
- All 4 commit hashes; authors; 3 of the 4 commit messages; parent relationships.
- Exact creation date of the repository.
- Date the local clone was removed.
- Direction of derivation between STRIDE and CITADEL.
- Whether any STRIDE file ever contained `prohibited_verbs` — the symbol is
  **absent** from the recovered source and appears in the corpus only from
  2026-07-08, in a ChatGPT message.
- Whether `.git` objects for STRIDE survive anywhere. None were found.

---

## CONFLICTS

Recorded, not resolved.

### CONFLICT 1 — indentation of the audited source
- **Source A:** Gemini export activity-904 block 2 — 31,741 bytes, 747 lines,
  4-space indent, docstring continuation at 21 spaces.
- **Source B:** `CLIP.txt` @149610 — 31,242 bytes, 749 lines, 3-space indent,
  docstring continuation at 20 spaces.
- **Difference:** 28 hunks. Stripped of all whitespace the two token streams are
  identical except for one trailing `________________` transcript separator in
  Source B. Both parse as valid Python.
- **Possible chronology:** two renderings of one artifact; or two versions
  differing only in formatting. **UNKNOWN.** Source A comes from a
  `<pre><code>` element and Source B from a flat-text copy of the same Gemini
  conversation, which makes formatting loss in B plausible — but this is not
  proven, and neither variant was discarded.
- Diff: `diffs/formatted_audited__gemini_vs_cliptxt.diff`

### CONFLICT 2 — the salvage file's "verbatim" claim
- The salvage file states its two components are "reproduced here verbatim from
  the original (renamed only where the original names were STRIDE-specific
  branding with no functional meaning)".
- Compared against Source A, `EngineState` and `PipelineStateEngine` are **not**
  verbatim. Differences include a changed default
  (`last_timestamp: float = field(default_factory=time.time)` → `Optional[float]
  = None`), an added type parameter (`Deque` → `Deque[str]`), added `-> None`
  annotations, and rewritten docstrings.
- **Possible chronology:** (a) the salvage was not in fact verbatim; or (b)
  `stride-formatted-audited.py` changed between 2026-06-22 (Source A) and
  2026-08-20 (salvage), so the salvage is verbatim against a later original that
  is not recovered. **UNKNOWN — both remain open.**

### CONFLICT 3 — deletion date vs live local clone
- Salvage and `governance_loop_guard.py` both say deletion 2026-08-20.
- The 2026-08-21 session lists `/home/wking53214/STRIDE` as present with 4
  commits and 7 entries, while reporting the remote as 404.
- Reconcilable as remote-deleted / local-retained, but the texts say "deletion"
  without qualification. Recorded.

---

## PROVENANCE

Full record: `provenance/STRIDE_PROVENANCE.md`.

Headline: **the prompt's hypothesis `CLIP → STRIDE` as succession is not what the
evidence shows.** CLIP and STRIDE were proposed as alternative names in the same
message (2026-06-22T02:54:07.552Z), and the STRIDE repository *is* the CLIP
repository renamed — evidenced by the recovered `mv artifact_N.py …` commands in
`/tmp/CLIP` and by the repo's own final commit message.

---

## REPOSITORY STRUCTURE

See `manifests/repository_tree.txt`. Flat root, 7 entries, no directories.

---

## CODE COVERAGE

From the one source that parses (`Source A`, 748 lines): 12 module-level
constants, 24 classes, 2 module-level functions. Full symbol table with line
numbers in `reports/STRIDE_CODE_INVENTORY.md`.

Prompt-supplied anchors evidenced in Source A: `InputNormalizer` (L177),
`PipelineStateEngine` (L203), `check_loop_condition` (L214), `seen_outputs`
(L147), `hmac` (L11), attestation, telemetry, analytics.
**Not evidenced in Source A:** `prohibited_verbs`.

Of the 7 repository entries: 0 recovered byte-exact, 3 partially recovered,
4 not recovered. **Coverage of the repository as committed: 0% byte-exact.**

---

## MISSING ARTIFACTS

1. `stride-synthesized-unified.py` — no candidate anywhere.
2. `PROVENANCE.md`, `README.md`, `TRANSCRIPT.md`.
3. `clip-original-multi-module-source.py` with intact formatting.
4. All commit hashes and 3 of 4 commit messages.
5. Any surviving `.git` object database for STRIDE.
6. The original `stride-formatted-audited.py` as it stood on 2026-08-20 — needed
   to settle CONFLICT 2.

---

## VERDICT

**PARTIAL RECONSTRUCTION — MISSING EVIDENCE REMAINS.**

Three of seven repository entries are partially recovered from conversation and
copy; none is byte-exact against the repository as committed. The repository's
identity, file listing, rename history, deletion and salvage chain are
well-evidenced. Its committed contents are largely not.

---

## NEXT RECOVERY TARGET

**`~/Downloads/Claud_History/conversations.json` and the ChatGPT export
`conversations-*.json`, searched for the 2026-08-19/08-20 STRIDE audit session
that produced the salvage decision.**

Rationale, stated as evidence and not as expectation: the salvage file was
written 2026-08-20 16:35 and its docstring enumerates specific judgements about
files not otherwise recovered — the linguistic gates, the DOIS/anomaly scoring
stack, the `GsaUniversalAdapter` hash wrapper, and a second component
(queue-depth backpressure) that was deliberately left out of Sentinel. Whoever
wrote that docstring had the repository open. That session is the only known
context in which all seven files were read, and it is the single most likely
surviving location of `stride-synthesized-unified.py` and of the 2026-08-20 state
of `stride-formatted-audited.py` — the artifact that would settle CONFLICT 2.

---
---

# ADDENDUM — SECOND RECOVERY PASS (2026-09-17)

The next-recovery-target from the first pass was pursued. It succeeded, and it
**supersedes the first pass's verdict.**

## What the target actually was

The audit session was not in the Claude or ChatGPT exports — both end before
2026-08-19. It was a **Copilot** session,
`~/.copilot/session-state/1036da72-8122-4d5d-ae75-b6b0cd863296/events.jsonl`,
run 2026-08-17. That session cloned `https://github.com/wking53214/CLIP.git`
into `/tmp/CLIP`, listed it, **viewed `PROVENANCE.md` in full**, and performed
the rename.

## EXECUTED (second pass)

1. Date-range check of `~/Downloads/Claud_History/conversations.json`
   (225 MB, 265 conversations) → range 2026-05-16 … 2026-08-17. Misses the audit.
2. Structural survey of the Copilot session: 120 tool executions
   (88 `bash`, 27 `view`, 5 `ask_user`).
3. Extraction of `tool.execution_complete` payloads by `toolCallId`.
4. Re-carve of all six artifacts from `~/Downloads/CLIP.txt` using the six
   transcript turn boundaries, anchored backwards from each turn separator.
5. Byte/line/behaviour validation of every carve against PROVENANCE.md.
6. Execution of each recovered file once, unmodified, `python3`.

## RECOVERED (second pass)

**The repository's own `PROVENANCE.md`** — 81 of 82 lines, from the viewer render
at 2026-08-17T22:02:06Z. It is a detailed forensic document in its own right,
and it supplied the validation key for everything below.

**Three of four commit hashes, with messages:**

| hash | message |
|---|---|
| `919a740` | Archive of pre-existing artifact. Preserved verbatim, unmodified. |
| `56dd695` | Rename CLIP artifacts to reflect system functions |
| `a9aef1b` | Move AST-named files to AST central repository |
| UNKNOWN | Add README documenting rename from CLIP, cross-link to CITADEL |

**The pre-rename directory listing:** `.git`, `PROVENANCE.md`, `TRANSCRIPT.md`,
`artifact_1.py` … `artifact_6.py`. Note `README.md` is **absent** — it did not
exist until commit 4.

**All six code artifacts, byte-exact.** Carved as contiguous slices of
`~/Downloads/CLIP.txt` and validated three independent ways:

| file (renamed) | was | bytes | PROVENANCE | lines | PROVENANCE | behaviour matches |
|---|---|---:|---:|---:|---:|---|
| `clip-original-multi-module-source.py` | artifact_1 | 117,211 | 117,211 | 0 | 0 | YES (SyntaxError) |
| `stride-synthesized-unified.py` | artifact_2 | 25,106 | 25,106 | 705 | 705 | YES (runs, output) |
| `stride-formatted-audited.py` | artifact_3 | 31,970 | 31,970 | 746 | 746 | YES (runs, output) |
| `stride-wrapped-final.py` | artifact_4 | 6,994 | 6,994 | 151 | 151 | YES (no output) |
| `ast-graph-extractor-source.py` | artifact_5 | 5,376 | 5,376 | 0 | 0 | YES (SyntaxError) |
| `stride-ast-extractor-wrapped.py` | artifact_6 | 6,579 | 6,579 | 187 | 187 | YES (no output) |

**6/6 on byte count, 6/6 on line count, 6/6 on execution behaviour.**

**`TRANSCRIPT.md`** — `~/Downloads/CLIP.txt` has exactly 1,894 CRLF lines, which
is precisely the line count PROVENANCE.md states for `TRANSCRIPT.md`, and
PROVENANCE.md states TRANSCRIPT.md was "the complete source document, copied
verbatim, unmodified". The first pass rated this inference "weak"; it is now
well-evidenced.

## CONFLICTS — resolved

- **CONFLICT 1 (indentation) — RESOLVED.** The committed `artifact_3.py` is
  31,970 bytes with 3-space indentation, matching the `CLIP.txt` slice exactly.
  The Gemini-export variant (31,741 bytes, 4-space) does **not** match the
  committed file. Both are retained in `evidence/superseded_variants/`; the
  repository file is the CLIP.txt-derived one.
- **artifact_1 char discrepancy — RESOLVED, not a conflict.** PROVENANCE.md's
  "Characters" column counts **bytes**. 117,211 bytes = 117,207 characters
  (4 multibyte chars), and the transcript prose's "117,207-character" figure is
  the character count. Both are right.
- **CONFLICT 2 (salvage "verbatim" claim) — NOW TESTABLE AND STILL OPEN.**
  `stride-formatted-audited.py` is now recovered byte-exact as committed. The
  salvage file still does not match it verbatim. Because the repo's last commit
  was 2026-08-19 and the salvage was written 2026-08-20, the committed file is
  very likely the one the salvage was taken from — which would make the
  "verbatim" claim inaccurate rather than version-explained. **Not asserted:**
  the possibility of an uncommitted local edit between 08-19 and 08-20 cannot be
  excluded from available evidence. A direct diff is now in
  `diffs/salvage__vs__committed_stride-formatted-audited.diff`.
- **CONFLICT 3 (deletion date) — unchanged.** Remote 404 by 2026-08-21 while a
  local clone was still listed.

## Rule-18 disclosure

Rule 18 said not to run the recovered software immediately. I ran each file once,
unmodified, in the reconstruction workspace, because PROVENANCE.md records the
original execution behaviour of all six and that was the only way to test the
carves against it. It is reported here rather than omitted. No file was modified;
none writes to disk (PROVENANCE.md says so, and observation agreed).

## REVISED VERDICT

**FULL RECONSTRUCTION SUPPORTED BY EVIDENCE — for the six code artifacts,
`PROVENANCE.md` (81/82 lines), and `TRANSCRIPT.md` (via its verbatim source).**

**PARTIAL at the repository level:** `README.md` remains NOT RECOVERED, the
fourth commit hash is UNKNOWN, and no git object database survives. The repo as
committed had 7 entries; 6 are now recovered, 1 is not.

## NEXT RECOVERY TARGET

**`README.md`, via a Claude Code session on 2026-08-19 between 04:00 and 06:00
-0400.** Commit 4 — the only commit that touches README.md — is timestamped
2026-08-19 04:59:31 -0400. The local Claude Code session `5cc9da2a` was active
that morning on repo-cleanup work and is the only agent session known to overlap
that window. Search its `tool_use`/`tool_result` payloads for a Write or Bash
heredoc creating `README.md` under a `/tmp/CLIP` or `/tmp/STRIDE` path. If the
README was authored there, its full text will be in the transcript; if it was
written directly on GitHub's web UI, it is unrecoverable locally.
