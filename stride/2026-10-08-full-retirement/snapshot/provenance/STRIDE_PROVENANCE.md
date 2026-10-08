# STRIDE — PROVENANCE

All statements below cite the evidence that establishes them. Where evidence is
absent the entry reads UNKNOWN. Nothing here is reconstructed from plausibility.

## Repository identity

| field | value | evidence |
|---|---|---|
| name | STRIDE | repo inventory dump |
| origin | `https://github.com/wking53214/STRIDE.git` | repo inventory dump |
| local path | `/home/wking53214/STRIDE` | repo inventory dump |
| branch | `main` | repo inventory dump |
| commits | 4 | repo inventory dump |
| entries | 7 | repo inventory dump |
| last commit date | 2026-08-19 04:59:31 -0400 | repo inventory dump |
| last commit message | "Add README documenting rename from CLIP, cross-link to CITADEL" | repo inventory dump |
| commit hashes | **UNKNOWN** | — |
| commit authors | **UNKNOWN** | — |
| first 3 commit messages | **UNKNOWN** | — |
| remote status at 2026-08-21 | `wking53214/STRIDE: MISSING (gh: Not Found (HTTP 404))` | same session, API probe section |
| local clone status now | absent (`ls: cannot access '/home/wking53214/STRIDE'`) | EXECUTED 2026-09-17 |

Evidence file for the above:
`~/.grok/sessions/%2Fhome%2Fwking53214/01a02609-48a6-7e72-b9ff-87cce3e07f90/chat_history.jsonl`
and `updates.jsonl` (same content, two encodings), session mtime 2026-08-21 16:51.

## Earliest evidence

The name STRIDE first appears **2026-06-22T02:54:07.552Z**, Gemini Apps Activity
record `activity-905`, as one of several proposed acronyms — in the **same
message** as CLIP:

> Here are a few descriptive acronym-based names for this unified system: CLIP
> C itadel L inguistic I ntegrity P ipeline … STRIDE S ecure T elemetry R untime
> and I ntelligence D eterministic E ngine

Three minutes later, **2026-06-22T02:57:20.552Z** (`activity-904`), a
`<pre><code>` block carries the header `SYSTEM_NAME: STRIDE` over 748 lines of
Python. That block is the earliest recovered STRIDE source.

## CLIP relationship — ESTABLISHED, and it is a RENAME, not a lineage

The prompt-side hypothesis was `CLIP → STRIDE` as succession. The evidence shows
something different in two independent places:

1. **Sibling naming.** CLIP and STRIDE were proposed together, in one message,
   as alternative names for the same "unified system" (`activity-905`).
2. **Repository rename.** A Copilot session
   (`~/.copilot/session-state/1036da72-8122-4d5d-ae75-b6b0cd863296/events.jsonl`)
   records the actual shell commands run in `/tmp/CLIP`:

   ```
   cd /tmp/CLIP && \
     mv artifact_1.py clip-original-multi-module-source.py && \
     mv artifact_2.py stride-synthesized-unified.py && \
     mv artifact_3.py stride-formatted-audited.py && \
     mv artifact_4.py stride-wrapped-final.py && \
     mv artifact_5.py ast-graph-extractor-source.py && \
     mv artifact_6.py stride-ast-extractor-wrapped.py && \
     git add -A && git commit -m "Rename CLIP artifacts to reflect system functions
   ```

   with the commit body describing each file. The repo's own final commit
   message — "Add README documenting rename from CLIP" — agrees.

**Therefore: the STRIDE repository *is* the CLIP repository, renamed.** Its files
were originally `artifact_1.py` … `artifact_6.py` in `/tmp/CLIP`.
`/tmp/CLIP` no longer exists (EXECUTED 2026-09-17).

## CITADEL relationship — REFERENCED, mechanism partly UNKNOWN

Three distinct pieces of evidence, which are **not** the same claim:

1. The CLIP acronym expands to **C**itadel **L**inguistic **I**ntegrity
   **P**ipeline (`activity-905`).
2. The repo's last commit message says it "cross-link[s] to CITADEL". The README
   that did the cross-linking is **NOT RECOVERED**, so what the cross-link
   asserted is **UNKNOWN**.
3. The recovered `stride-wrapped-final.py` variant's docstring says it
   "integrates the 'Citadel Linguistic Integrity Pipeline' (CLIP) … with a robust
   'Universal Cryptographic Interlock' (the wrapper)".
4. The salvage file states the rest of STRIDE was judged "strictly inferior to
   CITADEL's own recovered source".

No evidence recovered establishes direction of derivation between STRIDE and
CITADEL. **UNKNOWN.**

## Deletion

- Salvage file docstring (written 2026-08-20 16:35:48 -0400):
  "Salvaged from the STRIDE repo (stride-formatted-audited.py) before its
  deletion, 2026-08-20."
- `governance_loop_guard.py` docstring: "before its deletion **from GitHub**,
  2026-08-20."
- Corroboration: the 2026-08-21 API probe returns 404 for the remote.
- **Apparent conflict, resolved by distinguishing remote from local:** the same
  2026-08-21 session that reports the remote as 404 *also* lists
  `/home/wking53214/STRIDE` with 4 commits and 7 entries. The local clone
  therefore still existed on 2026-08-21 after the remote was deleted. The local
  clone's subsequent removal date is **UNKNOWN**.

## Salvage chain — STRIDE → Sentinel

| step | artifact | time | sha256 | status |
|---|---|---|---|---|
| origin | `STRIDE/stride-formatted-audited.py` | — | — | **NOT RECOVERED as a file** |
| salvage | `~/Downloads/stride_salvage_loop_and_backpressure.py` | 2026-08-20 16:35:48 -0400 | `2da62963…cab485` | DIRECT RECOVERY |
| duplicate | `…/stride_salvage_loop_and_backpressure-1.py` | 2026-08-21 10:18:34 -0400 | `2da62963…cab485` | byte-identical to the above |
| destination | `sentinel_os/sentinel_os/governance_loop_guard.py` | 2026-08-21 10:48:29 -0400 | `2fd50fe2…4572ed` | DIRECT RECOVERY |
| editor backup | `.claude/file-history/a4bdee5f…/8a769391c65d676f@v2` | 2026-08-21 10:52:13 | `2fd50fe2…4572ed` | byte-identical to destination |
| vendored copy | `GSA-815/vendor/sentinel_os/…/governance_loop_guard.py` | — | — | present |
| git | commit `91755bef6069674fabf386d54f142fa8c2c3eaa6`, 2026-08-21T10:51:12-04:00, "Wire governor loop detection into production_harness.py's Claude call" | | | sole commit touching this path |

**The Sentinel copy is NOT byte-identical to the salvage file** (3,708 vs 5,242
bytes). Diff: `diffs/salvage__vs__sentinel_governance_loop_guard.diff`.

What changed, per the recovered text itself: the salvage file carried **two**
pieces — (1) output-loop detection / bounded retry lifecycle, (2) queue-depth
backpressure. `governance_loop_guard.py` brought in **only the first**, and says
so explicitly: the second "has no identified use site yet and was left out rather
than added speculatively". The Sentinel file also gained a new docstring
section comparing itself to `circuit_breaker.py`.

**Neither file is the original STRIDE file.** The salvage file states it renamed
things "where the original names were STRIDE-specific branding". Provenance stops
at the salvage; the original is not recoverable from it.

## What the salvage file records about the rest of STRIDE

Quoted verbatim, as a historical judgement recorded at the time — not adopted
here as a finding:

> Everything else in STRIDE (the linguistic gates, the DOIS/anomaly scoring
> stack, the GsaUniversalAdapter hash wrapper) was judged not salvageable:
> either strictly inferior to CITADEL's own recovered source, uncalibrated
> duplicate territory sentinel_os/GSA-815 already cover with real tests, or
> in GsaUniversalAdapter's case, actively misrepresenting what it does
> (claims cryptographic tamper-evidence via HMAC while never using the hmac
> import it declares).

## Explicitly excluded from STRIDE

`stride-ast-extractor-wrapped.py` (in `ATS/` and `synapsis/`) carries a
`SYSTEM_NAME: STRIDE` header, but a session on 2026-08-19 recorded that this was
an error:

> 3:SYSTEM_NAME: STRIDE. That is incorrect — STRIDE is a real, separate gateway
> system (see the STRIDE repo, formerly CLIP). The STRIDE label was attached
> [in error]

It is therefore **not** treated as STRIDE source here, though it descends from
`/tmp/CLIP`'s `artifact_6.py` and was moved out of the repo before the final
7-entry listing.

## Unresolved provenance

- Which recovered code region corresponds to which of the 4 original `.py` files
  is **INFERRED from descriptions**, not proven by hash or filename.
- Commit hashes, authors, and 3 of 4 commit messages: **UNKNOWN**.
- `PROVENANCE.md`, `README.md`, `TRANSCRIPT.md` contents: **UNKNOWN**.
- Whether `~/Downloads/CLIP.txt` *is* `TRANSCRIPT.md`: **UNKNOWN**. It is a
  Gemini conversation export (`https://gemini.google.com/app/7a0bcc5ecb8f6d62`)
  covering the same development, which makes it a candidate, nothing more.
