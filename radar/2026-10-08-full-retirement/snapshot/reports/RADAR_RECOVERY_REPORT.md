# RADAR — RECOVERY REPORT

Categories are kept strictly separate. Nothing moves from INFERRED to RECOVERED
without proof, and nothing was generated to fill a gap.

---

## EXECUTED

Commands actually run, 2026-09-17:

1. Scan of `~/.copilot/session-state/*/events.jsonl` for tool calls whose
   arguments reference `/tmp/RADAR` or `RADAR`; extraction of the matching
   `tool.execution_complete` payloads by `toolCallId` **prefix** (the id in
   `assistant.message` is truncated for display).
2. `grep` of `~/.grok/sessions/` for the RADAR repo-inventory entry and the
   GitHub API probe result.
3. `git log --all --oneline` on `~/EDDP` and `~/Data_files`;
   `git cat-file -t 6dd34d3`; `git ls-tree -r 6dd34d3`.
4. `git show 6dd34d3:<file>` for each of the five `eddp-*.py` files.
5. `git show f0b70d6:gsa_universal_interlock_wrapper.py` in `~/GSA-815`.
6. `git log --all --name-only` on `~/EDDP` for the two flattened files.
7. Byte-substring containment test of all six recovered files against
   `~/Downloads/RADAR.txt`, read as **raw bytes**.
8. Turn-marker mapping of `RADAR.txt` (10 turns located by byte offset).
9. `sha256sum` on every recovered file; `cmp` against the STRIDE workspace.
10. Execution of each recovered `.py` once, unmodified, with `python3`.
11. Search of `~/.claude/projects/**` and `~/.grok/**` for RADAR's
    `PROVENANCE.md` contents — **no hit** (the only match was this session's own
    transcript).

Nothing outside `~/RADAR_RECONSTRUCTION/` was created, modified or deleted.

---

## INSPECTED

- `~/.copilot/session-state/1036da72-8122-4d5d-ae75-b6b0cd863296/events.jsonl`
- `~/.grok/sessions/%2Fhome%2Fwking53214/01a02609-…/chat_history.jsonl`
- `~/Downloads/RADAR.txt` — 114,452 bytes (114,455 with BOM), 2,010 CRLF lines
- `~/EDDP` git object database (commit `6dd34d3` and successors)
- `~/Data_files` git object database (same commit present)
- `~/GSA-815` git object database (commit `f0b70d6`)
- `~/STRIDE_RECONSTRUCTION/recovered_repo/` (for the cross-repo hash comparison)
- `~/.claude/projects/*/*.jsonl` and `*/tool-results/*.txt`

---

## RECOVERED

**All six code files, byte-exact, from git blobs — with independent
cross-validation.**

| file (as renamed) | was | bytes | git blob | offset in RADAR.txt | on execution |
|---|---|---:|---|---:|---|
| `eddp-pipeline-core-simple.py` | artifact_1 | 1,174 | `a8ad5a7f…` | 149 | runs, no output |
| `eddp-core-engine-v1.py` | artifact_2 | 10,662 | `22f07960…` | 2,927 | runs, 62 lines |
| `eddp-core-engine-v2-refined.py` | artifact_3 | 14,576 | `b03f0250…` | 19,213 | runs, 58 lines |
| `eddp-comprehensive-synthesized.py` | artifact_4 | 14,751 | `e1573491…` | 34,293 | runs, 58 lines |
| `eddp-wrapped-final.py` | artifact_5 | 5,376 | `4a68b434…` | 90,849 | SyntaxError |
| `gsa_universal_interlock_wrapper.py` | (not renamed) | 18,179 | from GSA-815 `f0b70d6` | 72,631 | runs, no output |

Two independent evidence paths agree for every file: a git blob from the
repository the content was moved into, **and** an exact byte-substring match
inside the archived source transcript. 6/6 on both.

**Complete commit history** — all four hashes with messages and times
(`d5e52dd`, `681fed6`, `93cd72e`, `e07c430`).

**The archived directory listing** — 8 entries, captured 2026-08-17T22:04:03Z.

**`TRANSCRIPT.md`** — recovered as its verbatim source, `~/Downloads/RADAR.txt`.

**The naming sequence** — the three candidate acronyms and the user's selection,
verbatim from the transcript.

---

## RECOMPOSED

`recovered_repo/` holds 7 files: the six code artifacts under the names they
carried after commit `681fed6`, plus the transcript source. No file was
assembled from fragments; each is a single byte-exact blob or a single verbatim
copy. No directories were created — the evidence shows a flat root.

---

## INFERRED

1. That `~/Downloads/RADAR.txt` is the material behind the committed
   `TRANSCRIPT.md`. Basis: it is the archive's own stated input pattern, it
   carries the repo's exact title, and it contains all six artifacts as exact
   byte substrings. **Byte-identity to the committed file is not proven** — no
   PROVENANCE.md counts exist to check.
2. That `d5e52dd` is the archival commit that created the repo. Basis: its
   message matches the archival pattern and the stale clone sits at it with the
   full 8-entry file set.
3. That `artifact_5.py` was pasted by the user rather than generated. Basis: its
   byte offset (90,849) falls immediately after the turn-10 `User prompt:`
   marker at 90,828.

---

## UNKNOWN

- **`PROVENANCE.md` contents.** It existed in both observations of the repo, but
  no surviving session opened it. This is the one artifact the STRIDE
  reconstruction had and this one does not.
- Commit authors; the time-of-day component of `d5e52dd` beyond `11:32:08 -0400`.
- Whether `RADAR.txt` is byte-identical to the committed `TRANSCRIPT.md`.
- When `~/RADAR`, `/tmp/RADAR` and the GitHub remote were removed (only
  "404 by 2026-08-21" is established).
- Whether a README.md ever existed — none appears in the 8-entry listing, and no
  commit message mentions one.

---

## CONFLICTS

### RESOLVED — `commits=1` vs four commits
The Grok inventory's `commits=1` describes a **stale clone** at `~/RADAR`
captured at `d5e52dd` (2026-08-13), while the later three commits were made in a
separate clone at `/tmp/RADAR` on 2026-08-17. `n_entries=8` matches the archived
file set exactly. Both records are accurate for their own working copy. Not a
contradiction.

### RECORDED — filename does not describe content
`eddp-wrapped-final.py` is an AST graph extractor, not an EDDP wrapper. The name
came from positional renaming (`artifact_5.py` → the fifth EDDP-pattern name).
An independent EDDP commit (`e789167`, 2026-08-19) reached the same conclusion
and deleted it as a duplicate. Recorded; the file is preserved under its
historical name.

### RECORDED — repo name vs system name
The repo is `RADAR`; five of six artifacts were renamed to `eddp-*`; the code
inside declares `EDDP` in early versions and `RADAR` from `artifact_4.py`
onward. Preserved as found.

### NOT A CONFLICT — line-count arithmetic
Commit `e07c430` reports 1,058 deletions; `wc -l` over the five recovered files
gives 1,053. The two flattened files have no trailing newline, which git counts
differently from `wc`. Byte-level identity to the git blobs is exact, so the
files are not in question.

---

## PROVENANCE

Full record: `provenance/RADAR_PROVENANCE.md`.

Headline: **the system was EDDP before it was RADAR.** "RADAR" was one of three
acronyms proposed in turn 4 and chosen by the user in turn 5; the repository
inherited it from the transcript title on 2026-08-13, and on 2026-08-17 the
artifacts were renamed back toward EDDP to match what the code actually declares.

---

## REPOSITORY STRUCTURE

See `manifests/repository_tree.txt`. Flat root, 8 entries, no directories, no
tests, no README.

---

## CODE COVERAGE

Four of six files parse as Python; two (`eddp-pipeline-core-simple.py`,
`eddp-wrapped-final.py`) are flattened single-line pastes with zero line breaks
and are preserved unreformatted. `eddp-pipeline-core-simple.py` executes without
error only because the entire flattened line is a comment.

Symbol tables in `reports/RADAR_CODE_INVENTORY.md`. The EDDP→RADAR rename is
visible in the class names: `EDDPSystem` (artifact_2, line 209) becomes
`RADARSystem` (artifact_4, line 255).

Of the 8 repository entries: **6 recovered byte-exact, 1 recovered as its
verbatim source, 1 not recovered.**

---

## MISSING ARTIFACTS

1. `PROVENANCE.md` — existence verified, contents unrecovered.
2. Proof that `RADAR.txt` equals the committed `TRANSCRIPT.md` byte-for-byte.
3. Commit authorship metadata.
4. Any surviving `.git` object database for RADAR itself (none found; all
   recovery came from the repositories the content was *moved into*).

---

## VERDICT

**PARTIAL RECONSTRUCTION — MISSING EVIDENCE REMAINS.**

All six code artifacts are recovered byte-exact and doubly validated, and the
commit history is complete. `PROVENANCE.md` is not recovered, so 1 of the 8
archived entries is missing and the transcript's byte-identity is unconfirmed.
That is short of full, and is reported as such rather than rounded up.

---

## NEXT RECOVERY TARGET

**RADAR's `PROVENANCE.md`, via the archival session of 2026-08-13 around
11:32 -0400.**

Commit `d5e52dd` created the repo and wrote `PROVENANCE.md` at that moment. The
recovered CLIP/STRIDE `PROVENANCE.md` shows these files were *authored by an
agent* — it contains per-file execution results, character counts and an
"Extraction: what was stripped" section, which means the agent ran the files and
measured them in-session. If RADAR's was written the same way, the full text
will be in whichever session performed the 2026-08-13 archival run, most likely
as a Write/heredoc payload.

That session is the single highest-value target because `PROVENANCE.md` is both
the missing artifact *and* the validation key: its line/character/behaviour table
would confirm byte-identity for `TRANSCRIPT.md` and independently re-verify all
six code files. Search `~/.copilot/session-state/*/events.jsonl` and
`~/.claude/projects/*/*.jsonl` for sessions active on 2026-08-13 between 10:58
(the `RADAR.txt` mtime) and 11:32 (the commit), looking for heredocs or Write
calls whose content begins `# Provenance`.

---
---

# ADDENDUM — ORIGIN SCOUR + PROVENANCE.md HUNT (2026-09-17, second pass)

Two things were pursued: the next-recovery-target (`PROVENANCE.md`), and a
correction the account holder was right to demand — **do not assume a commit
elsewhere was the repository's origin.**

## EXECUTED (second pass)

1. Corpus sweep for earliest occurrence of 12 EDDP/RADAR markers across the
   65,181-message index.
2. Byte-containment test of the 2026-06-05 ChatGPT paste against `RADAR.txt`.
3. Class/function set comparison between the 2026-06-05 paste and RADAR
   `artifact_2.py`; unified diff written.
4. Timestamp survey of every Copilot, Claude Code and Grok session to find one
   active on 2026-08-13.
5. Hour-by-hour coverage audit of the claude_web export for 2026-08-13.
6. Search of all corpora for the archival commit message string.

## The correction

The first pass recorded `d5e52dd` (2026-08-13) as the commit that created the
repo. That is accurate for the **repository** and says nothing about the
**content** — and reading it as an origin would have been wrong.

**The EDDP code predates the RADAR conversation by 17 days.** Earliest source in
the record: **2026-06-05T00:08:29.252Z**, ChatGPT, `role: user`, 9,464 bytes,
headed `EDDP + Evaluation + Feedback Integrity System / Deterministic
Architecture Kernel (Reference Implementation)`. It shares 13 of its 14 classes
with RADAR `artifact_2.py`; the extra class is `ContextRegistry`, and two
top-level functions were later renamed with a `custom_` prefix.

**And the RADAR conversation did not receive that paste.** `RADAR.txt` contains
neither the 2026-06-05 text nor any occurrence of `ContextRegistry`. Its turn-1
prompt is a 1,174-byte fragment; the full system appears in turn 2's *response*.

Where the 2026-06-05 paste itself came from is **UNKNOWN** — it is a paste, and
nothing earlier exists in any corpus. The earliest `EDDP` token anywhere is
2026-05-16T22:54:45Z, where Claude reviews code the account holder had pasted
from ChatGPT; **that code is not preserved**.

## RECOVERED (second pass)

- The 2026-06-05 predecessor, verbatim
  (`evidence/predecessors/`, sha256 `45a73c316d8d4524…`).
- The RADAR naming event at **2026-06-22T02:01:30Z** — three candidates
  (RADAR / DEFT / APEX), user selects the first.
- A dated adjacency: the CLIP/STRIDE naming occurred **53 minutes later** the
  same night in the same Gemini stream. Recorded; no relationship asserted.

## UNKNOWN — and now evidenced as such

**`PROVENANCE.md` is NOT RECOVERABLE.** The archival window (2026-08-13,
10:58 → 11:32 -0400) falls in a simultaneous coverage gap:

| source | 2026-08-13 coverage | covers the window? |
|---|---|---|
| claude_web export | hours 00–05 and 12–19; **nothing 06:00–12:00** | NO |
| Copilot session-state | earliest session 2026-08-17T17:32Z | NO |
| Claude Code local | earliest session 2026-08-19T08:54Z | NO |
| Grok sessions | earliest 2026-08-21 | NO |

The archival pattern does appear in claude_web at 14:20/14:25/14:27 that day for
*other* repos, placing the work in Claude web — but RADAR's slot is inside the
hole. **FILE EXISTENCE VERIFIED — RAW SOURCE NOT RECOVERED.**

## VERDICT — unchanged

**PARTIAL RECONSTRUCTION — MISSING EVIDENCE REMAINS.**

Six of eight archived entries recovered byte-exact, one recovered as its verbatim
source, one unrecoverable. The second pass did not add recovered repository
files; it corrected the chronology and closed the `PROVENANCE.md` line of inquiry
with an evidenced negative rather than an open question.

## NEXT RECOVERY TARGET

**The pre-2026-06-05 EDDP source, in the ChatGPT account's own conversation
history for 2026-05-16 and earlier.**

The account holder's own statement on 2026-05-16 — *"ChatGPT was my primary
building system… That is where I housed all of the final products"* — and the
same evening's Claude review of pasted EDDP code together establish that EDDP
existed before any surviving artifact of it. The 2026-06-05 paste is the
earliest **preserved** copy, not the earliest copy.

This is the highest-value remaining target because it is the only one that could
push the origin back past the corpus boundary: everything after 2026-06-05 is now
recovered or accounted for. Concretely — search the ChatGPT export
(`ChatGPT_History/data/raw.jsonl`, and the raw `conversations-*.json`) for
conversations dated 2026-04-01 → 2026-06-05 containing `ECPValidator`,
`stable_hash`, `ContextRegistry` or `EDDP`, and check whether any predecessor of
the 9,464-byte paste was itself generated rather than pasted. If every hit is
`role: user`, the origin lies outside the exported record entirely and should be
reported as such rather than pursued further locally.
