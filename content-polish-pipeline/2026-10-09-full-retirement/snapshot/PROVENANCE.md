# Provenance

## Source

- Source file: `content-polish-pipeline-v1.zip`, provided by the user from
  their local Downloads folder (`/mnt/chromeos/MyFiles/Downloads/` on this
  Chrome OS machine).
- The zip's internal entries are timestamped **2026-08-26 21:49–21:50**. It
  contains a ready-made Python package, not a chat export — there is no
  transcript, prompt log, or conversation text in the archive.
- Compiled bytecode shipped inside the zip (`__pycache__/pipeline.cpython-312.pyc`)
  carries the embedded `co_filename` `/home/claude/content-polish-pipeline/pipeline.py`.
  The `/home/claude/` path indicates the package was assembled and executed
  in a Claude sandbox environment before being zipped and downloaded. Which
  session produced it, and from what prompts, is not recorded in anything
  included here.
- This repo (`wking53214/content-polish-pipeline`) already existed on GitHub
  with a single commit `088a065 "Initial commit"` holding only a 25-byte
  stub `README.md` (`# content-polish-pipeline`). The package was added on
  top of that stub on **2026-08-27** (commit `fb5e442`). Git history
  reflects the archival/packaging dates, not the code's development history.

## Relationship to earlier archived code

The core of this package — the class `ContentPolishPipeline` plus the three
filter classes `PersonalPronounFilter`, `SpeculativeLanguageFilter`, and
`EmpiricalValidationFilter` — descends from code in the Google Gemini
transcript archived in the user's separate `CODE` repo (visible there in
`content-pipeline-modularized.py`, originally `artifact_2.py`, from a
transcript headed "Code modules,"
`https://gemini.google.com/app/a78e020ee8262a51`).

In that earlier version the pipeline used `logging.getLogger("GSA_CORE")`
and a one-line docstring ("Polish output for external communication
(optional routing)."), and the module carried the header
`Module: content_pipelines.py | Version: v1.0.0`. This zip is a
restructured, expanded, documented, and **test-covered** standalone
version of that same design: HMAC signing, duplicate-hash loop detection,
recalibration-feedback retry text, a package `__init__.py`, a `README.md`,
and a `tests.py` are all present here and absent from the `CODE`-repo
original. The transformation from the Gemini original to this package was
not itself captured in any file provided.

## What the zip contained

| File | Lines | Bytes | Kept in repo |
|---|---|---|---|
| `README.md` | 102 | 2,933 | yes (replaced the 25-byte stub) |
| `__init__.py` | 31 | 861 | yes |
| `filters.py` | 65 | 2,565 | yes |
| `pipeline.py` | 191 | 6,964 | yes |
| `tests.py` | 139 | 4,834 | yes |
| `__pycache__/filters.cpython-312.pyc` | — | 4,439 | no |
| `__pycache__/pipeline.cpython-312.pyc` | — | 7,467 | no |

The `__pycache__/` directory (two `.pyc` files, Python 3.12 bytecode) was
build output and was not committed; a `.gitignore` excluding
`__pycache__/`, `*.pyc`, `.pytest_cache/`, and virtualenv directories was
added instead.

**As committed in `fb5e442`, no source file was modified — the five text
files were byte-for-byte as they came out of the zip.** They were later
edited and relocated; see "Post-archival fixes" below.

## Whether the artifacts execute

Yes. As received (commit `fb5e442`), the package ran and its test suite
passed:

```
$ python3 -m pytest tests.py -q
................                                                          [100%]
16 passed in 0.07s
```

All 16 tests passed unmodified on the system `python3` (3.12) with no
third-party dependencies — `pipeline.py` and `filters.py` import only the
standard library (`asyncio`, `hashlib`, `hmac`, `logging`, `time`, `re`).
`pipeline.py` has a `try/except ImportError` around its filter import so it
works both as a package submodule and when run flat from inside the
directory; the as-received `tests.py` used the flat form
(`from filters import ...`, `from pipeline import ...`) and so had to be run
from within the package directory rather than as `python -m` from the
parent. After the post-archival fixes the suite is 23 tests and runs via
plain `python3 -m pytest` from the repo root.

## Tests

The as-received `tests.py` was real, first-party test coverage (16
`unittest` cases across four `TestCase` classes), unlike the AI-chat
archives elsewhere in this collection which generally have none. It covered
each filter individually and four pipeline paths: success on first try,
retry-then-succeed on a pronoun violation, max-attempts exhaustion, and
gateway-exception handling. It did **not** cover the HMAC signature value,
the duplicate-hash loop-break path, or the `_normalize` whitespace
handling.

The post-archival fixes added tests for the behaviors they changed
(`is_clean`/`passes` equivalence, sorted `violations()`, `max_attempts < 1`
rejection, duplicate-generation detection, signature stability). The
`_normalize` whitespace handling is still uncovered.

## Things noticed in the as-received package

*(All six were fixed after archival — see "Post-archival fixes" below.
Kept here verbatim as the record of what was received.)*

- **README "Deterministic output" claim vs. `set()` ordering.** The README's
  Design Notes say "Same input prompt + LLM seed → same result." Both
  `PersonalPronounFilter.violations()` and `SpeculativeLanguageFilter.violations()`
  return `list(set(matches))`, whose element order is not stable across
  runs; the human-readable `violations` strings in the result dict (and in
  the recalibration feedback sent back to the LLM) can therefore vary in
  ordering for the same input. The validated text and its HMAC signature
  are unaffected.
- **Signing key is a hardcoded default.** `signing_key` defaults to
  `b"CONTENTPOLISH_DEFAULT_HMAC_KEY"`. The README presents
  `payload_signature` (HMAC-SHA384) as something to "use for verification";
  it only provides integrity/authenticity if the caller supplies a private
  key, which the README does not mention.
- **Package name vs. directory name.** The README imports
  `from content_polish_pipeline import ContentPolishPipeline` (underscores),
  but the packaged directory — and this repo — is `content-polish-pipeline`
  (hyphens), which is not an importable Python module name. Installing as a
  real package would need packaging metadata (there is no `pyproject.toml`,
  `setup.py`, or `requirements.txt`) or the directory renamed with
  underscores.
- **`EmpiricalValidationFilter` inverts the filter contract.** Its
  `is_clean()` returns `True` when an evidence marker is *present* (the
  other two filters return `True` when their target pattern is *absent*).
  This is intentional and documented in the class docstring, but it means
  "clean" means opposite things depending on the filter.
- **`hashlib.md5`** is used for the duplicate-detection hash. This is a
  non-security use (loop detection), so the weak-hash property does not
  matter here.
- The `CRITICAL_FAILURE`-on-max-attempts branch references `failures` from
  the last loop iteration; it is always bound by then because
  `max_attempts >= 1` is assumed (the constructor does not validate it —
  `max_attempts=0` would raise `UnboundLocalError`).

## Repo actions taken (2026-08-27)

1. Unpacked `content-polish-pipeline-v1.zip`.
2. Added `README.md`, `__init__.py`, `filters.py`, `pipeline.py`,
   `tests.py` to the existing repo; the real `README.md` replaced the stub.
3. Added `.gitignore`; did not commit the zip's `__pycache__/`.
4. Ran `python3 -m pytest tests.py` — 16 passed — then committed
   (`fb5e442`) and pushed to `main`.
5. Added this `PROVENANCE.md` (`02456e5`).

## Post-archival fixes (2026-08-27, commit `33626b0`)

At the user's request, the six items above were fixed. Version bumped
`1.0.0` → `1.1.0`. All changes are in a single commit; 23 tests pass.

| # | As-received issue | Fix |
|---|---|---|
| 1 | `violations()` returned `list(set(...))` (unstable order) vs. README "deterministic output" | `violations()` now returns `sorted(set(...))` in both `PersonalPronounFilter` and `SpeculativeLanguageFilter`; test added |
| 2 | Hardcoded default `signing_key`, undocumented | Constructor logs a `WARNING` when the default key is used; README + docstring state the signature is integrity-only without a caller-supplied secret key |
| 3 | README import `content_polish_pipeline` didn't resolve; no packaging metadata | Modules moved into `content_polish_pipeline/`, tests into `tests/`; `pyproject.toml` added so `pip install .` works and `import content_polish_pipeline` resolves. **This relocates the files listed in "What the zip contained."** Licensed **MIT** at the user's request (`LICENSE` file added, `license = "MIT"` in `pyproject.toml`); the copyright line reads `2026 wking53214` (the GitHub identity — no other name was given). |
| 4 | `EmpiricalValidationFilter.is_clean` inverted vs. the other two filters | All three filters expose `passes()`; `is_clean` kept as an alias; pipeline calls `passes()`; the inversion is documented on the method and in the README |
| 5 | `hashlib.md5` for the duplicate-detection hash | Switched to `hashlib.sha256` (internal only; not part of the result dict) |
| 6 | `max_attempts=0` would raise `UnboundLocalError` deep in `execute()` | Constructor raises `ValueError` for `max_attempts < 1`; test added |

Current layout:

```
content_polish_pipeline/  __init__.py  filters.py  pipeline.py
tests/                     test_pipeline.py
pyproject.toml  README.md  PROVENANCE.md  .gitignore
```

## Retired into ghost_tools (2026-09-09 onwards)

This repo is no longer developed as a standalone package. Its code now
lives inside `wking53214/ghost_tools` (originally v0.6.0, now v1.0.5 as of
2026-09-18), where it is the quality gate wrapped around `ghost_writer/correct.py`'s LLM call, the one place in `ghost_writer` that generates new text rather than templating a human's
own decision. It is not a new ghost_tools command, and `report.py` there
is not gated.

### Initial vendoring (2026-09-09)

What moved, from commit `44bf225abd819008f898510c37ea5b432cb44532`
(v1.1.0, the last state of `main`):

| Here | There |
|---|---|
| `content_polish_pipeline/filters.py` | `ghost_writer/polish/filters.py` |
| `content_polish_pipeline/pipeline.py` | `ghost_writer/polish/pipeline.py` |
| `content_polish_pipeline/__init__.py` | `ghost_writer/polish/__init__.py` (rewritten, same exports) |
| `tests/test_pipeline.py` (23 tests) | `Tests/test_polish.py` |
| `LICENSE` (MIT) | `ghost_writer/polish/LICENSE` |

Vendored, not depended on: ghost_tools declares no dependencies. The copy
differs from the files here in an unused `import asyncio` removed
(ghost_tools runs `ruff check` as a CI gate), the standalone
`try/except ImportError` import fallback replaced by the relative import,
and the logger renamed to `ghost_writer.polish`. ghost_tools'
`PROVENANCE.md` records the same table from the receiving side.

How it is used there: `correct.py` runs the pipeline around its one model
call. The pronoun and speculation filters check both the proposed
replacement and the reasoning; the empirical filter checks the reasoning
only (a minimal doc replacement is not an empirical claim). Three attempts
by default. `README.md` and the `## Usage` example above describe the
standalone package as it was and are left as the record of it.

### Post-vendoring addition: `oscillation.py` (2026-09-09)

After the repo was archived, a code audit found an unmerged branch
(`claude/ats-oscillation-detection-qs1k74`, commit `b0740bf3d827a30c339c5f54e1a14432548d2689`, dated 2026-08-30)
that refactored the duplicate-detection logic into a reusable `OscillationDetector` class. This class
replaced the inline `historical_hashes` set that was part of the vendored pipeline.

What was added:

| Source branch | Copied to |
|---|---|
| `content_polish_pipeline/oscillation.py` (from unmerged branch) | `ghost_writer/polish/oscillation.py` |

Changes in the vendored copy:
- Attribution header added
- Internal `.strip().lower()` normalization removed (the pipeline already normalizes before duplicate checks; stacking case-insensitive normalization would be a behavior change)
- `deque[str]` type hint added
- Docstring rewritten to explain the deviation

The pipeline was updated to use `OscillationDetector(max_history=32)` in place of the inline
hash set, with the detector reset once per `execute()` call. All result dicts now include an
`oscillation_detected` field. The unmerged branch itself remains archived in this repo's git
history but was never merged.

The repo is kept, archived and read-only, as the record of this lineage.

### Current state

As of 2026-09-18, ghost_tools is at v1.0.5. The vendored polish code has evolved beyond the
v0.6.0 reference point: the pipeline now uses bounded-history oscillation detection instead of
unbounded duplicate tracking, and the integration has grown through several ghost_tools releases
to support broader use cases within the `ghost_writer` module.

### Audit note: unmerged branch `claude/ats-oscillation-detection-qs1k74`

A branch audit after the archival above found a second branch on this
repo, `claude/ats-oscillation-detection-qs1k74`, commit
`b0740bf3d827a30c339c5f54e1a14432548d2689` (2026-08-30). It was never
opened as a pull request and was not part of the retirement above; the
retirement only carried what was on `main`.

That branch refactors the pipeline's inline duplicate-response detection
(an unbounded `set` of response hashes) into a reusable `OscillationDetector`
class with a bounded history, adds 19 tests, and bumps the package to
v1.2.0. It was reviewed, found sound in intent, and adapted -- not merged
wholesale -- into `ghost_writer/polish/oscillation.py` in `ghost_tools`
(v0.6.3). `ghost_tools`' own `PROVENANCE.md` has the full accounting;
summarized here:

- **Adapted:** the `OscillationDetector` class itself, wired into the
  vendored pipeline in place of the inline hash set.
- **Not carried forward:** the class's own `.strip().lower()` normalization
  of its input. The vendored pipeline already normalizes a response before
  any duplicate check sees it; stacking a second, case-insensitive
  normalization on top would silently treat two proposals differing only
  in capitalization as the same output. `ghost_tools`' copy compares
  exactly what it is given.
- **Not carried forward:** this branch's README changes and its
  `content_polish_pipeline/__init__.py` export shape; `ghost_tools`
  documents the detector in its own README and exports it from its own
  `ghost_writer/polish/__init__.py` instead.

The branch itself was archived in this repo's git history as the record of the work it contains,
pending final disposition decision on this archive.
