# RADAR — PROVENANCE

Every statement cites the evidence that establishes it. Where evidence is absent
the entry reads UNKNOWN. Nothing is reconstructed from plausibility.

## Repository identity

| field | value | evidence |
|---|---|---|
| name | RADAR | repo inventory + clone command |
| origin | `https://github.com/wking53214/RADAR.git` | `git clone` in Copilot session, 2026-08-17T22:03:59Z |
| branch | `main` | push output |
| commits | **4** | all four hashes recovered (below) |
| entries at archival | 8 files | `/tmp/RADAR` listing, 2026-08-17T22:04:03Z |
| remote status 2026-08-21 | `wking53214/RADAR: MISSING (gh: Not Found (HTTP 404))` | Grok session API probe |
| local `~/RADAR` now | absent | EXECUTED 2026-09-17 |

### Commit history — complete

| hash | message | time | evidence |
|---|---|---|---|
| `d5e52dd` | Archive of pre-existing artifact. Preserved verbatim, unmodified. | 2026-08-13 11:32:08 -0400 | Grok inventory (stale clone) + rename push output |
| `681fed6` | Rename RADAR artifacts to reflect EDDP system functions | 2026-08-17T22:04:37Z | push output `d5e52dd..681fed6` |
| `93cd72e` | Move GSA-named files to GSA-815 central repository | 2026-08-17T23:12:56Z | push output `681fed6..93cd72e` |
| `e07c430` | Move EDDP-named files to EDDP central repository | 2026-08-17T23:14:09Z | push output `93cd72e..e07c430` |

### The `commits=1` discrepancy — RESOLVED, not a conflict

A Grok repo-inventory dump (2026-08-21) records `/home/wking53214/RADAR` with
`commits=1`, `n_entries=8`, last commit **2026-08-13 11:32:08 -0400**. That is a
**stale local clone** captured at `d5e52dd`, before any of the 2026-08-17 work.
All later commits were made in a *separate* fresh clone at `/tmp/RADAR` and
pushed from there. `n_entries=8` matches the archived file set exactly.
Both records are correct; they describe different working copies.

## The source transcript

`~/Downloads/RADAR.txt` — 114,452 bytes (114,455 with BOM), 2,010 CRLF lines,
mtime 2026-08-13 10:58:59 -0400.

- Line 1: `RADAR (Role-based Analytics Dashboard Assembling and Routing) Orchestration Kernel`
- Line 2: `https://gemini.google.com/app/472fb9f896b324e0`
- **10 conversation turns.**

**Validated as the artifacts' source by containment:** all six recovered code
files appear inside it as **exact byte substrings**, at offsets 149, 2927, 19213,
34293, 72631 and 90849. That is independent of, and stronger than, a filename
match.

Whether this file is byte-identical to the committed `TRANSCRIPT.md` is
**UNVERIFIED** — RADAR's `PROVENANCE.md` was never recovered, so no stated line
or character count exists to check against.

## RADAR ↔ EDDP — the naming sequence, recovered verbatim

The system was **EDDP first**. "RADAR" was applied to it later, inside the same
conversation, and the repository then inherited the transcript's title.

1. Turns 1–3 build a system that names itself, in `artifact_2.py`:
   `EDDP (Executive Dashboard Distribution Processor)` — with a class
   `EDDPSystem`.
2. **Turn 4** (offset 33813) — the user asks for "3 acronym based names". The
   response, verbatim:
   ```
   1 RADAR Role-based Analytics Dashboard Assembling and Routing
   2 DEFT Dashboard Evaluation Feedback and Transport
   3 APEX Analytics Processing Evaluation and eXecution
   ```
3. **Turn 5** (offset 34113) — the user picks the first:
   `New system name: RADAR (Role-based Analytics Dashboard Assembling and Routing)`
   The response emits `Program Name: RADAR (...)` and the class is now
   `RADARSystem` (`artifact_4.py`, line 255).
4. On 2026-08-13 the repository was created as **RADAR** (the transcript title).
5. On 2026-08-17 commit `681fed6` renamed the artifacts **back toward EDDP** —
   `eddp-pipeline-core-simple.py`, `eddp-core-engine-v1.py`, etc. — with the
   commit body headed `EDDP (Executive Dashboard Distribution Processor):`.

So the repo is named for the *later* acronym while its files are named for the
*earlier* system name. Recorded as found; nothing renamed to reconcile it.

This is structurally the same pattern as CLIP/STRIDE — a repo named from the
transcript title while the code inside declares a different system name. **No
relationship between the two cases is asserted here.**

## Where the content went

| commit | action | destination | recovered from |
|---|---|---|---|
| `681fed6` | `artifact_1..5.py` renamed in place | — | — |
| `93cd72e` | `gsa_universal_interlock_wrapper.py` removed (397 deletions) | GSA-815 | GSA-815 commit `f0b70d6` blob |
| `e07c430` | all five `eddp-*.py` removed (1,058 deletions) | EDDP | EDDP commit `6dd34d3` blobs |

The copy into GSA-815 is confirmed by the literal command
`cp RADAR/gsa_universal_interlock_wrapper.py GSA-815/gsa_universal_interlock_wrapper.py`.
After `e07c430`, RADAR retained only `PROVENANCE.md` and `TRANSCRIPT.md`.

**Downstream fate of the moved files (recorded, not interpreted):**
- GSA-815's copy was itself deleted on 2026-09-03 by `3e979a5`
  ("Dead-weight sweep + governance-core consolidation").
- EDDP's `eddp-wrapped-final.py` was deleted on 2026-08-19 by `e789167`
  ("Remove AST extractor duplicate, canonical copy in synapsis").
- The EDDP remote later moved to `Data_files`
  (`remote: This repository moved. Please use the new location:
  https://github.com/wking53214/Data_files.git`), and commit `6dd34d3` is
  present in both local repos.

## A hash-proven duplication across two archived repos

`eddp-wrapped-final.py` (RADAR `artifact_5.py`) is **byte-identical** to
`ast-graph-extractor-source.py` (CLIP/STRIDE `artifact_5.py`):

```
sha256 a7026823c9a985cb7ff3d90a24a832fbc51cfb3ff2c922d61c52296808dbaa04
5,376 bytes, 0 line breaks (flattened)
```

Both are the same flattened "Deterministic AST-based graph extractor", pasted by
the user as the final turn's prompt in each of two separate Gemini
conversations. In RADAR's transcript it sits at offset 90849, immediately after
the turn-10 `User prompt:` marker.

**Its RADAR name does not describe its content** — `eddp-wrapped-final.py` is an
AST graph extractor, not an EDDP wrapper. The 2026-08-19 EDDP commit `e789167`
independently reached the same conclusion, deleting it as an "AST extractor
duplicate".

**No ancestry, derivation, or direction of copying is asserted.** The claim here
is only that the same bytes appear in both places.

## Unresolved

- `PROVENANCE.md` contents — **NOT RECOVERED**. It existed in both the
  2026-08-13 clone and the 2026-08-17 `/tmp/RADAR` listing, but no surviving
  session ever opened it.
- Commit authors and the full timestamp of `d5e52dd` beyond the date shown.
- Whether `RADAR.txt` is byte-identical to the committed `TRANSCRIPT.md`.
- The date `~/RADAR` and `/tmp/RADAR` were removed, and the date the GitHub
  remote was deleted (only "404 by 2026-08-21" is established).
- Any relationship between RADAR/EDDP and CITADEL, STRIDE, Sentinel, OBSERVE,
  GSA-815, CNS or the governance stack. **Not investigated — out of scope.**

---

# ADDENDUM — ORIGIN SCOUR (2026-09-17, second pass)

The first pass treated `d5e52dd` (2026-08-13) as where the repository's history
began. That was an **archival** commit, not an origin, and the distinction
matters. This addendum records what scouring the full record actually shows.

## Correction to the first pass

First pass, INFERRED item 2, read: *"`d5e52dd` is the archival commit that
created the repo."* That is true of the **repository** and says nothing about the
**content**. The content is older, and originates outside the RADAR conversation
entirely.

## The earliest EDDP source code in the record

**2026-06-05T00:08:29.252Z — ChatGPT, `role: user`, message
`14e7a905-4152-4b1e-84e6-64fea9513ecc`, 9,464 bytes.** Its own header:

```
"""
EDDP + Evaluation + Feedback Integrity System
Deterministic Architecture Kernel (Reference Implementation)
"""
```

This is **17 days before** the RADAR conversation and **69 days before** the
archival commit. Every distinctive EDDP symbol bottoms out here and nowhere
earlier in the 65,181-message index: `EDDPSystem`, `stable_hash`, `ECPValidator`,
`BenchmarkScorer`, `FeedbackLoop`, `RoleRouter`, `DeliveryEvent`,
`ContextRegistry`, `revenue_stability`, `ECP (UPSTREAM VALIDATION STUB)`.

Preserved at
`evidence/predecessors/20260605T000829_chatgpt_EDDP_predecessor.py`
(sha256 `45a73c316d8d4524…`).

### Its relationship to RADAR `artifact_2.py`, stated as observation only

| | 2026-06-05 paste | RADAR `artifact_2.py` (2026-06-22) |
|---|---|---|
| header | `EDDP + Evaluation + Feedback Integrity System / Deterministic Architecture Kernel (Reference Implementation)` | `EDDP (Executive Dashboard Distribution Processor) / Fully Integrated Enterprise Kernel & Evaluation Reference Implementation` |
| bytes | 9,464 | 10,662 |
| classes | 14 | 13 |
| shared classes | 13 — `Payload`, `EvaluationResult`, `BenchmarkResult`, `DeliveryEvent`, `ECPValidator`, `EvaluationLayer`, `EvaluationEngine`, `BenchmarkScorer`, `RoleRouter`, `Renderer`, `Distributor`, `FeedbackLoop`, `EDDPSystem` | same |
| only in the earlier | `ContextRegistry` | — |
| top-level defs | `stable_hash`, `revenue_stability`, `operational_health` | `stable_hash`, `custom_revenue_stability`, `custom_operational_health` |

Diff: `diffs/predecessor_20260605__vs__RADAR_artifact_2.diff` (596 lines).

**Not asserted:** that one was derived from the other, or the direction of any
such derivation. What the record establishes is that a near-identical class set
existed 17 days earlier, and that `ContextRegistry` is present only in the
earlier one.

### RADAR.txt did NOT receive that paste

Tested directly: `~/Downloads/RADAR.txt` does **not** contain the 2026-06-05
text, exactly or CRLF-normalised, and contains no occurrence of
`ContextRegistry`. The RADAR conversation's turn-1 prompt is a **small** 1,174-byte
pipeline fragment (`artifact_1.py`); the full EDDP system appears in turn 2's
*response*. So the system was re-produced inside that conversation rather than
pasted into it.

## Where the 2026-06-05 paste itself came from — UNKNOWN

It carries `role: user`, i.e. it was pasted into ChatGPT. Nothing earlier exists
in any available corpus. Its origin is outside the record.

One in-record statement bears on this, from the account holder on
**2026-05-16T22:51:58Z** (claude_web), quoted verbatim and offered as context,
not as proof of any particular file's provenance:

> OK. This is where I started to incorporate ChatGPT copilot and Gemini and what
> I did was bounced back-and-forth between the three building out different
> components and following the build methodology that you've seen. ChatGPT was my
> primary building system, and reaction response very similar to how you do. That
> is where I housed all of the final products and did most of the work.

The earliest occurrence of the token `EDDP` in any corpus is
**2026-05-16T22:54:45Z** (claude_web, assistant), reviewing code the account
holder had pasted from ChatGPT in that same session. The code under review at
that moment is **not itself preserved** in the corpus.

## Corrected chronology

| when | what | provenance |
|---|---|---|
| before 2026-05-16 | EDDP code exists in ChatGPT | **UNKNOWN** — asserted by the account holder, artifact not preserved |
| 2026-05-16T22:54:45Z | earliest `EDDP` token in any corpus | RECOVERED FROM CONVERSATION |
| **2026-06-05T00:08:29Z** | **earliest EDDP source code in the record**, user paste, 9,464 bytes | RECOVERED FROM CONVERSATION |
| 2026-06-22T02:01:30Z | RADAR proposed as one of three acronyms (RADAR / DEFT / APEX) | RECOVERED FROM CONVERSATION |
| 2026-06-22T02:03:45Z | `RADARSystem` first appears | RECOVERED FROM CONVERSATION |
| 2026-08-13 10:58:59 -0400 | `RADAR.txt` written to `~/Downloads` | filesystem mtime |
| 2026-08-13 11:32:08 -0400 | `d5e52dd` — **archival**, not origin | RECOVERED FROM GIT (via push output) |
| 2026-08-17 | rename, then content moved out to GSA-815 and EDDP | RECOVERED FROM GIT |

## An adjacency worth recording, with no claim attached

The RADAR acronym was proposed at **2026-06-22T02:01:30Z** (`g907-response`). The
CLIP / STRIDE / VITAL / SHIELD acronyms were proposed at **2026-06-22T02:54:07Z**
(`g905-response`) — **53 minutes later, the same night, in the same Gemini
activity stream.** Both conversations then produced repos archived on 2026-08-13
with the same `PROVENANCE.md` + `TRANSCRIPT.md` + `artifact_N.py` pattern.

Recorded as temporal adjacency. **No relationship between the two systems is
asserted here.**

## PROVENANCE.md — NOT RECOVERABLE, with the negative evidenced

RADAR's `PROVENANCE.md` cannot be recovered from anything available. The archival
window (2026-08-13, 10:58 → 11:32 -0400) falls in a coverage gap in **every**
corpus simultaneously:

| source | coverage on 2026-08-13 | covers 10:58–11:32? |
|---|---|---|
| claude_web export | messages in hours 00–05 and 12–19; **nothing 06:00–12:00** | NO |
| Copilot session-state | earliest session starts 2026-08-17T17:32Z | NO |
| Claude Code local sessions | earliest starts 2026-08-19T08:54Z | NO |
| Grok sessions | earliest starts 2026-08-21 | NO |
| ChatGPT export | searched; no archival content | NO |

The commit-message pattern "Archive of pre-existing artifact. Preserved verbatim,
unmodified." does appear in claude_web later the same day (14:20, 14:25, 14:27,
for other repos), which places the archival work in Claude web — but the RADAR
portion sits in the 06:00–12:00 hole.

**Status: FILE EXISTENCE VERIFIED — RAW SOURCE NOT RECOVERED.** No further local
avenue was identified.
