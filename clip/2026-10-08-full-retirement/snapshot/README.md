# ⚠ RECONSTRUCTION — AND CLIP WAS NEVER A SEPARATE REPOSITORY

Pushed 2026-09-17. Read this before treating anything here as original history.

## The single most important fact

**CLIP and STRIDE are the same repository at two points in time.**

There was one repository. It was named **CLIP** on GitHub, and was later
**renamed to STRIDE**. It was not forked, not copied, not split. Evidence:

- A Copilot session on 2026-08-17 ran
  `git clone https://github.com/wking53214/CLIP.git` into `/tmp/CLIP`.
- Its pushes went to `CLIP.git`: `919a740..56dd695`, then `56dd695..a9aef1b`.
- The repository's own final commit message (2026-08-19) reads
  *"Add README documenting rename from CLIP, cross-link to CITADEL"*.
- `github.com/wking53214/CLIP` now returns **404**.

**This GitHub repository is therefore a new one**, created 2026-09-17 to hold the
reconstruction. No repository called CLIP existed separately from STRIDE, and the
original CLIP/STRIDE repository is deleted. Its commits — `919a740`, `56dd695`,
`a9aef1b`, and a fourth whose hash is UNKNOWN — do not exist here.

## What this repository represents

The state of the repository at commit **`919a740`** —
*"Archive of pre-existing artifact. Preserved verbatim, unmodified."* — i.e.
**before** the 2026-08-17 rename, when the files were still named
`artifact_1.py` … `artifact_6.py`.

That state is worth preserving separately because the repository's own
`PROVENANCE.md` describes the files under those names. It mentions
`artifact_1.py` … `artifact_6.py` 23 times and contains **zero** occurrences of
the later `stride-*` / `clip-original-*` / `ast-graph-*` names. The document and
the filenames only agree in this state.

## Completeness — 8 of 8 entries

The directory listing captured at 2026-08-17T22:02:06Z, immediately before the
rename, shows exactly: `.git`, `PROVENANCE.md`, `TRANSCRIPT.md`,
`artifact_1.py` … `artifact_6.py`. All eight non-`.git` entries are present here.

Every code artifact validated three independent ways against `PROVENANCE.md`:

| file | bytes | stated | CRLF lines | stated | execution behaviour |
|---|---:|---:|---:|---:|---|
| `artifact_1.py` | 117,211 | 117,211 | 0 | 0 | SyntaxError ✓ |
| `artifact_2.py` | 25,106 | 25,106 | 705 | 705 | runs, output ✓ |
| `artifact_3.py` | 31,970 | 31,970 | 746 | 746 | runs, output ✓ |
| `artifact_4.py` | 6,994 | 6,994 | 151 | 151 | no output ✓ |
| `artifact_5.py` | 5,376 | 5,376 | 0 | 0 | SyntaxError ✓ |
| `artifact_6.py` | 6,579 | 6,579 | 187 | 187 | no output ✓ |

**6/6 on bytes, 6/6 on lines, 6/6 on behaviour.**

`PROVENANCE.md` — 81 of 82 lines, from a viewer render captured before the
rename. `TRANSCRIPT.md` — recovered as its verbatim source, 1,894 CRLF lines,
exactly the count `PROVENANCE.md` states.

Note that this state is **more completely recovered than the later STRIDE
state**, which is missing the `README.md` added in the fourth commit.

Verdict: **FULL RECONSTRUCTION SUPPORTED BY EVIDENCE** for the repository as it
stood at `919a740`. The commit history itself is not recovered.

## What the rename did

Commit `56dd695` renamed all six files at once (100% similarity, no content
change):

```
artifact_1.py -> clip-original-multi-module-source.py
artifact_2.py -> stride-synthesized-unified.py
artifact_3.py -> stride-formatted-audited.py
artifact_4.py -> stride-wrapped-final.py
artifact_5.py -> ast-graph-extractor-source.py
artifact_6.py -> stride-ast-extractor-wrapped.py
```

Commit `a9aef1b` then removed `artifact_5`/`artifact_6`'s renamed forms from the
repository entirely (moved to an AST repo, later ATS). So the six-file state
preserved here existed only between `919a740` and `a9aef1b`.

## The naming, from the record

`PROVENANCE.md` states the AI proposed four candidate acronyms — **CLIP, STRIDE,
VITAL, SHIELD** — and that the transcript's own title took the first. It also
records, as a fact worth noting, that none of the three code artifacts carrying a
self-declared system name uses "CLIP": all three say `STRIDE`.

CLIP expands to **C**itadel **L**inguistic **I**ntegrity **P**ipeline; STRIDE to
**S**ecure **T**elemetry **R**untime and **I**ntelligence **D**eterministic
**E**ngine. No relationship to any other system is asserted here.

## Preserved as-found, deliberately

- `artifact_1.py` and `artifact_5.py` are **flattened single-line pastes** with
  zero line breaks and do not parse. `PROVENANCE.md` records this too. Not
  reformatted.
- `artifact_6.py` carries a `SYSTEM_NAME: STRIDE` header that a later session
  determined was applied in error. Preserved as found.
- CRLF line endings preserved throughout.

## Layout

```
recovered_repo/   the 919a740 state: artifact_1-6.py, PROVENANCE.md, TRANSCRIPT.md source
evidence/         the pre-rename directory listing, the PROVENANCE.md viewer render,
                  and the rename commit output
manifests/        file_manifest.json with SHA-256 for every entry
reports/          CLIP_CODE_INVENTORY.md
```

The later state of this same repository is at `github.com/wking53214/STRIDE`.

Nothing in `recovered_repo/` was written, reformatted, corrected or completed.
