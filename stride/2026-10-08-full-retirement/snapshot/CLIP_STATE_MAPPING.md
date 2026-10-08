# The two states of one repository

CLIP and STRIDE are **the same repository** at two points in time. It was named
CLIP on GitHub and later renamed to STRIDE. This directory merges the earlier
state into the same repo as the later one so the whole history sits in one place.

## What changed between them: filenames, and nothing else

Commit `56dd695` renamed all six files at once, at 100% similarity. Verified
here by SHA-256 — **every pair is byte-identical**:

| CLIP state (`919a740`) | STRIDE state (post-`56dd695`) | bytes | sha256 |
|---|---|---:|---|
| `artifact_1.py` | `clip-original-multi-module-source.py` | 117,211 | `5d6f4d1be4fed3791b052539…` |
| `artifact_2.py` | `stride-synthesized-unified.py` | 25,106 | `3e128f87f77c4671fe3c2850…` |
| `artifact_3.py` | `stride-formatted-audited.py` | 31,970 | `f2c9e112e48119fc8856a664…` |
| `artifact_4.py` | `stride-wrapped-final.py` | 6,994 | `d47f0902f6a833185cc27b65…` |
| `artifact_5.py` | `ast-graph-extractor-source.py` | 5,376 | `a7026823c9a985cb7ff3d90a…` |
| `artifact_6.py` | `stride-ast-extractor-wrapped.py` | 6,579 | `fb1bc4b02d60d6af5cce9473…` |

The files in `recovered_repo_clip_state_919a740/` are therefore **not different
versions** of the files in `recovered_repo/`. They are the same bytes under the
names they carried before the rename. The filename→content mapping is itself the
historical fact being preserved.

## Why the earlier state is worth keeping separately

1. **It is the only state where `PROVENANCE.md` and the filenames agree.** That
   document describes `artifact_1.py` … `artifact_6.py` 23 times and never once
   uses a `stride-*` name. Read against `recovered_repo/`, it appears to
   describe files that aren't there.
2. **It is more completely recovered.** 8 of 8 entries, versus 6 of 7 for the
   later state, whose `README.md` (added in the fourth commit) is unrecoverable.
3. **It contains two files the later repository no longer had.** Commit
   `a9aef1b` removed `artifact_5`/`artifact_6`'s renamed forms, moving them to an
   AST repo and later ATS. The six-file state existed only between `919a740` and
   `a9aef1b`.

## Commit sequence

```
919a740  Archive of pre-existing artifact. Preserved verbatim, unmodified.
56dd695  Rename CLIP artifacts to reflect system functions       2026-08-17T22:02:46Z
a9aef1b  Move AST-named files to AST central repository          2026-08-17T23:19:40Z
UNKNOWN  Add README documenting rename from CLIP, cross-link to CITADEL   2026-08-19
```

None of these commits is recovered as a commit. The hashes and messages come from
`git push` output captured in a session log; the file contents come from the
archived source transcript. This repository's own history begins in 2026-09-17.

