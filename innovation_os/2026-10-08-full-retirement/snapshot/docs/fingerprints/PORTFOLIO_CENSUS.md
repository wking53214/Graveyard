# Portfolio structural census

Mechanical measurement of every repository reachable in this session.
Run 2026-09-12 with `tools/fingerprint/extract_signature.py`.

No judgement here beyond what the numbers support. Cards under `cards/` carry
the interpretation.

---

## Coverage

24 of 39 repositories cloned and measured. **1,334 Python files, 229,489
lines.** The 15 not measured are listed at the end.

## The table

| Repository | Files | Lines | Classes | Enums | Tunables | Raises | Lines/raise | Parse err |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| observe | 187 | 67,016 | 649 | 51 | 38 | 282 | 237 | 0 |
| sentinel_os | 169 | 49,123 | 270 | 6 | 17 | 292 | 168 | 0 |
| innovation_os | 524 | 22,086 | 350 | 3 | 6 | 23 | **960** | 0 |
| observe-perceive | 79 | 20,615 | 260 | 6 | 15 | 53 | 388 | 0 |
| gsa-815 | 53 | 14,716 | 131 | 13 | 11 | 64 | 229 | 0 |
| herald | 26 | 10,070 | 26 | 2 | 3 | 53 | 190 | 0 |
| ccc | 41 | 8,232 | 63 | 14 | 9 | 69 | 119 | 0 |
| touchstone | 32 | 5,510 | 141 | 3 | 46 | 46 | 119 | **10** |
| ats | 9 | 4,587 | 77 | 4 | 15 | 5 | 917 | 0 |
| conservation_kernel | 33 | 4,375 | 29 | 12 | 0 | 81 | **54** | 0 |
| triad-42 | 20 | 4,296 | 38 | 15 | 3 | 64 | 67 | 0 |
| anvil | 2 | 3,493 | 66 | 2 | 1 | 17 | 205 | 0 |
| gems | 42 | 3,013 | 59 | 8 | 0 | 50 | 60 | 0 |
| gsa-master-kernel | 15 | 2,486 | 111 | 0 | 21 | 16 | 155 | **6** |
| cns | 14 | 1,774 | 20 | 6 | 0 | 5 | 354 | 0 |
| eddp | 6 | 1,591 | 43 | 2 | 0 | 11 | 144 | 0 |
| citadel | 4 | 1,340 | 20 | 5 | 0 | 0 | — | 0 |
| augur | 5 | 1,316 | 23 | 0 | 19 | 7 | 188 | 0 |
| fortress-kernel | 4 | 1,264 | 26 | 2 | 20 | 4 | 316 | 0 |
| synapsis | 31 | 1,262 | 30 | 0 | 0 | **1** | **1,262** | 0 |
| tie | 30 | 660 | 13 | 4 | 0 | 5 | 132 | 0 |
| governance_gateway | 6 | 617 | 7 | 3 | 0 | 12 | 51 | 0 |
| vanguard | 2 | 47 | 1 | 0 | 0 | 0 | — | 1 |
| tbca | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |

**Lines per raise** measures how often code refuses. It separates systems that
*decide* from systems that *record*, and it is the most useful single maturity
signal in this portfolio. Low is dense; high is sparse.

---

## Findings

### 1. URE's source exists, in TOUCHSTONE

All eight of the handoff's URE marker symbols — `SystemResilienceConfig`,
`SystemRegimeClassifier`, `IntegratedResilienceOrchestrator`,
`TelemetryIngestionPipeline`, `StabilityMonitor`,
`RegimeClassificationProfile`, `DiagnosticEvaluationSummary`,
`calculate_shannon_entropy`, `clamp_value` — resolve to `touchstone` and
**nothing else**. `[EXPERIMENT]`

This resolves `UNRESOLVED.md` U-1 and produced a correction to `cards/OBSERVE.md`.
See `cards/URE.md`.

### 2. TOUCHSTONE is the preserved-source corpus, and it is a deliberate instrument

TOUCHSTONE is not a system. Its README calls it "a specimen corpus", built
because "every verification claim in this ecosystem is currently calibrated
against material its own author invented ... That is circular, and it is the
deepest weakness in the platform: not that the verifiers are wrong, but that
nothing can show whether they are right." `[CODE]`

Its `MANIFEST.md` records, per specimen, what the file **is**, what it
**proves**, and **what the correct answer is** — plus a note that every
"Faithful" verdict it inherited from an earlier README "had never been checked"
until a measurement pass on 2026-09-07 corrected the corpus.

This matters for this archive directly. TOUCHSTONE already does, with stated
falsifiable answers, the job of grading a verifier against material it did not
author. Any fingerprint classifier built here should be scored against it
rather than against examples written alongside it.

Its 46 tunables in 5,510 lines is the highest density in the portfolio, which
is what a corpus of preserved control-variable specimens should look like.

### 3. Flattened sources are a portfolio-wide format, not a TOUCHSTONE quirk

16 files across three repositories are **flattened**: an entire module
collapsed onto one line by a copy-paste through a chat interface. They report 0
lines to `wc -l` while carrying 2–33 KB. `[EXPERIMENT]`

| Repository | Flattened files |
| --- | ---: |
| touchstone | 10 |
| gsa-master-kernel | 5 |
| vanguard | 1 |

A flattened file raises `SyntaxError` on import, so **it cannot have produced
any result attributed to it**. `gsa-master-kernel`'s five are `artifact_1.py`
… `artifact_14.py` — the same naming as TOUCHSTONE's `reference/` artifacts,
suggesting the same preservation practice outside the corpus.

The extractor now recovers structure from flattened files rather than
discarding them; that is how URE was read.

### 4. One file fails silently rather than loudly

`touchstone/specimens/pairs/governance_os_security_source.py` is 11,700 bytes
on a single line **beginning with `#`**. Python reads the whole file as one
comment. It imports cleanly, raises nothing, and defines zero names — an
importability check reports it as healthy. `[EXPERIMENT]`

TOUCHSTONE placed it deliberately, as the specimen that catches a verifier
checking importability instead of content.

The extractor now flags this as `silently_inert`. Across all 24 repositories
and 1,334 files it fires on **exactly that one file** — no false positives.
Reaching that took two corrections: an early version also flagged a config
module assigning a dict, and any docstring-only `__init__.py`.

### 5. Cross-repository duplication is substantial

**97 byte-identical Python files ≥2 KB appear in more than one repository,
totalling 912,610 redundant bytes.** `[EXPERIMENT]`

The largest case is structural: `observe/sentinel_os/` is a near-copy of the
`sentinel_os` repository.

| | |
| --- | ---: |
| `.py` files in `observe/sentinel_os/` | 176 |
| `.py` files in `sentinel_os/sentinel_os/` | 163 |
| Same path in both | 95 |
| Byte-identical | 60 |
| **Same path, diverged content** | **35** |
| Only in the `observe` copy | 81 |
| Only in `sentinel_os` | 68 |

The 35 diverged files are the risk: two copies of the same module, same path,
different content, no declared canonical side. Which repository leads is
`UNKNOWN`.

`gems/transport/gems_transport/` is vendored into
`sentinel_os/conservation/transport/` — but that one is declared, in
`transport/PROVENANCE.md`, and is a correct vendoring rather than a drift.

### 6. SYNAPSIS is nearly empty

31 files, 1,262 lines, **0 enums, 0 tunables, 1 raise site**. `[EXPERIMENT]`

SYNAPSIS is named in the handoff as a major modular system and appears in
Innovation OS's own integration contract as a future connection. The measured
code does not support treating it as an implemented system. What it *is*
remains `UNKNOWN` — this is a size measurement, not a reading of the code.

### 7. Two repositories are effectively empty

- `tbca` — **0 Python files**.
- `vanguard` — 2 files, 47 lines, of which one is flattened. The real
  `vanguard-behavioral-simulation` reconstruction lives in TOUCHSTONE, not
  here.

### 8. Conservation Kernel is the densest fail-closed code in the portfolio

4,375 lines, 81 raise sites, **one raise per 54 lines** — three times denser
than `sentinel_os` and eighteen times denser than `innovation_os`. 12 enums in
33 files. `[EXPERIMENT]`

It is also the unvendored dependency that stops `sentinel_os`'s conservation
boundary executing from a clone (`UNRESOLVED.md` U-5). It is now cloned and
available.

### 9. Innovation OS is the sparsest measured system

**960 lines per raise**, against a portfolio median near 170. Its 524 files and
22,086 lines include this session's own additions and its test suite; the
earlier source-only measurement was 13,879 lines at 694 lines per raise. Either
way it sits at the far end of the distribution. `[EXPERIMENT]`

`ats` at 917 is the only comparable figure, and for a different reason: five of
its nine files carry no tests, and its validation is done with bare `assert`
rather than raises.

### 10. Four regime classifiers, not one

Files matching regime-classifier vocabulary, by repository: `observe` 11,
`touchstone` 8, `observe-perceive` 7, `ats` 2, plus one each in `vanguard`,
`sentinel_os`, `fortress-kernel`, `augur`. `[EXPERIMENT]`

`cards/URE.md` §9 establishes that URE, SRE, SOLVAR's `LyapunovStabilityModule`
and GOV4's `RegimeClassifier` are one design family sharing the
weighted-squared-deviation formula and the 1e-4/1e-2 constants, and that
OBSERVE is **not** in that family despite superficial similarity.

---

## Not yet measured

15 repositories: `CODE`, `GRAPH`, `KAGGLE`, `Ecology`, `Resume_OS`,
`content-polish-pipeline`, `ghost_tools`, `Governance_Gateway` *(measured)*,
and the history corpora — `ChatGPT_History`, `Claude_History`,
`Gemini_History`, `CoPilot_History`, `Gemini_Extraction`, `ARCHIVE`,
`Data_files`.

The history corpora are the extraction *input* for the classifier stage, not
systems to fingerprint. They should be sized before that stage is designed.

## Reproducing

```bash
for d in /path/to/repos/*/; do
  python tools/fingerprint/extract_signature.py "$d" > "census/$(basename $d).json"
done
```
