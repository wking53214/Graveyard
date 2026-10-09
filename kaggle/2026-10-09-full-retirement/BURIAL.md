# Burial: KAGGLE, retired in full

**Repo:** `wking53214/kaggle` (private at burial)
**Snapshot commit:** `8158c0a` (main), the last live state
**Date:** 2026-10-09
**Decision:** William N. King

## Why

KAGGLE is an archived Google Gemini conversation, 30 turns, about an image-texture classifier for
the FREUID 2026 IJCAI-ECAI Kaggle competition. It is an ordinary data-science working session, not
governance code. Nothing in the local stack uses its techniques (Sobel variance, Local Binary Pattern,
GLCM features into LightGBM). The only mention found is a chat transcript in the GEMS repo.

## Usefulness review (before burial)

- Searched the local repos for the feature techniques and the competition name. Only a GEMS chat
  transcript mentions them. No code to port.
- The artifacts are notebook fragments. Most need packages that are not in the stack (pandas,
  scikit-image, lightgbm, kagglehub, google.colab). Nothing was ported.
- The value of the repo is the record itself. The full transcript and the provenance write-up are kept intact.

## Where each part lives now

| Part | Where it lives now |
|---|---|
| Full 30-turn transcript | `snapshot/TRANSCRIPT.md` (verbatim, unredacted; PROVENANCE.md says no personal data was found) |
| Source provenance, per-file run results, noticed defects | `snapshot/PROVENANCE.md` |
| 14 extracted code fragments and the JSON payload | `snapshot/artifact_*.py`, `snapshot/artifact_13.json`, `snapshot/artifact_*.txt` |

## What's here

- `snapshot/`: all 21 tracked files at `8158c0a`, including LICENSE (Apache-2.0).
- `kaggle-full-history.bundle`: complete history (7 commits) plus the six pull-request refs. Verified with `git bundle verify`.

## Known issues at time of burial

Recorded in full in `snapshot/PROVENANCE.md` and `snapshot/README.md`. Summary:

- Most fragments do not run on their own. They expect notebook state or packages not installed here.
- `artifact_15.py` has a syntax error (`for root, , files in ...`). It came from turn 11 and survived two reconstruction passes.
- `artifact_13.json` is invalid JSON. An unescaped `b""` sits inside a `"body"` value.
- `artifact_4.py` contains a Jupyter shell command (`!rm -rf`) that fails outside a notebook.
- The repo name is "KAGGLE", but the source file was `GLCM.txt`.

## Bringing it back

- Whole repo with history: `git clone kaggle-full-history.bundle kaggle`
- Files only: copy `snapshot/`.
