# Master fingerprint archive

Index of code identity fingerprints. One canonical card per system. Cards are
never collapsed because two systems look similar; see `README.md`.

Last updated: 2026-09-12

---

## Fingerprinted

| System | Card | Source of record | Commit | Maturity |
| --- | --- | --- | --- | --- |
| ATS Governor | [`cards/ATS_GOVERNOR.md`](cards/ATS_GOVERNOR.md) | `wking53214/ats` | `48245a9` | Implementation |
| OBSERVE | [`cards/OBSERVE.md`](cards/OBSERVE.md) | `wking53214/observe` | `9138bed` | Implementation |
| Innovation OS | [`cards/INNOVATION_OS.md`](cards/INNOVATION_OS.md) | `wking53214/innovation_os` | `3bb189d` | Skeleton + 4 real packages |
| URE | [`cards/URE.md`](cards/URE.md) | `wking53214/touchstone` | `0db5600` | Superseded specimen, flattened |

## Measured but not yet carded

Structural signatures extracted; a card requires reading the code to card
standard, which has not been done for these.

| System | Path | Files | Lines | Enums | Tunables | Raises | Crypto |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Sentinel OS | `sentinel_os/sentinel_os/` | 163 | 47,204 | 6 | 17 | 291 | cryptography, hkdf, hmac, nonce, secrets, sha256, signing |
| SRE | `touchstone/.../sre_system_resilience_evaluator_adapter.py` | 1 | 570 | 2 | — | — | none |
| SAGE-K | `sentinel_os/sentinel_os/sage_k/` | 14 | 2,851 | 0 | 3 | 15 | hmac, sha256, signing |
| PERCEIVE | `observe/sentinel_os/perceive_consolidated.py` | 1 | 1,172 | 0 | 3 | — | hmac, secrets, sha256, signing |
| GSA Governance Operating Core | `observe/sentinel_os/GSA.py` | 1 | 4,986 | 12 | 0 | — | sha256 |
| GOV4 kernel | `ats/gov4_kernel.py` | 1 | 604 | 2 | 6 | 1 | hmac, sha256 |

`[EXPERIMENT: tools/fingerprint/extract_signature.py]`

### Density comparison

Raise sites per line separates systems that *decide* from systems that
*record*. It remains the most useful single maturity signal found. Full table
in [`PORTFOLIO_CENSUS.md`](PORTFOLIO_CENSUS.md).

| System | Lines | Raises | Lines per raise |
| --- | ---: | ---: | ---: |
| Conservation Kernel | 4,375 | 81 | **54** |
| GEMS | 3,013 | 50 | 60 |
| Triad-42 | 4,296 | 64 | 67 |
| Sentinel OS | 49,123 | 292 | 168 |
| SAGE-K | 2,851 | 15 | 190 |
| OBSERVE | 67,016 | 282 | 237 |
| ATS | 4,587 | 5 | 917 |
| Innovation OS | 22,086 | 23 | **960** |

The two extremes are the finding. Conservation Kernel refuses roughly eighteen
times more often per line than Innovation OS. ATS's figure has a different
cause: it validates with bare `assert`, which `python -O` removes.

---

## Portfolio inventory

39 repositories on the account `[EXTERNAL SOURCE: repository listing]`.
Status is fingerprint status, not code quality. Line counts from
[`PORTFOLIO_CENSUS.md`](PORTFOLIO_CENSUS.md).

### Named in the handoff

| Repository | Handoff system | Lines | Status |
| --- | --- | ---: | --- |
| `ATS` | ATS | 4,587 | **Carded** |
| `OBSERVE` | OBSERVE | 67,016 | **Carded** |
| `innovation_os` | Innovation_OS | 22,086 | **Carded** |
| `TOUCHSTONE` | — (holds URE) | 5,510 | **URE carded**; corpus itself needs an entry |
| `observe-perceive` | OBSERVE / PERCEIVE | 20,615 | Measured |
| `GSA-815` | GSA | 14,716 | Measured |
| `GSA-Master-Kernel` | GSA | 2,486 | Measured; 5 flattened artifacts |
| `synapsis` | SYNAPSIS | 1,262 | Measured; 0 enums, 0 tunables, 1 raise |
| — | LOT | — | **No repository identified.** `UNKNOWN` |

URE's source was located in `TOUCHSTONE` by the census — see `UNRESOLVED.md`
U-1. LOT remains unlocated; no repository name and no code symbol matches it.

### Governance stack

| Repository | Lines | Note |
| --- | ---: | --- |
| `sentinel_os` | 49,123 | Measured. Frozen since 2026-09-08 per its README. |
| `Conservation_Kernel` | 4,375 | Measured. Densest fail-closed code in the portfolio. Unblocks U-5. |
| `GEMS` | 3,013 | Measured. `transport/` vendored into `sentinel_os/conservation/transport/`, declared. |
| `fortress-kernel` | 1,264 | Measured. Related to SAGE-K's `Fortress`. |
| `Governance_Gateway` | 617 | Measured. |

### Measured, unclassified

Scale only. Nothing below has been read, and nothing about what these systems
*are* should be inferred from this table.

| Repository | Lines | Enums | Lines/raise |
| --- | ---: | ---: | ---: |
| `HERALD` | 10,070 | 2 | 190 |
| `CCC` | 8,232 | 14 | 119 |
| `Triad-42` | 4,296 | 15 | 67 |
| `ANVIL` | 3,493 | 2 | 205 |
| `CNS` | 1,774 | 6 | 354 |
| `EDDP` | 1,591 | 2 | 144 |
| `CITADEL` | 1,340 | 5 | — (0 raises) |
| `AUGUR` | 1,316 | 0 | 188 |
| `TIE` | 660 | 4 | 132 |
| `VANGUARD` | 47 | 0 | — (effectively empty) |
| `TBCA` | 0 | — | — (no Python files) |

`CITADEL` also appears as a class-name prefix inside `GSA.py`
(`CitadelDiamondEngine`, `CitadelProcessorEngine`, `CitadelRouterEngine`). That
is a lead, not a finding: whether the repository and the prefix are the same
thing is `UNKNOWN`.

### History corpora — the extraction input

The conversation archives the classifier is ultimately meant to run against
(handoff §10). None cloned or sized. They are input, not systems to fingerprint,
but they should be sized before the extraction stage is designed.

`ChatGPT_History`, `Claude_History`, `Gemini_History`, `CoPilot_History`,
`Gemini_Extraction`, `ARCHIVE`, `Data_files`

### Not measured

`CODE`, `GRAPH`, `KAGGLE`, `Ecology`, `Resume_OS`, `content-polish-pipeline`,
`ghost_tools`

---

## Coverage

- **4 of 39** repositories carded.
- **24 of 39** structurally measured — see [`PORTFOLIO_CENSUS.md`](PORTFOLIO_CENSUS.md).
- **15** unmeasured, of which 7 are conversation corpora rather than systems.

Measurement is not a card. The census establishes scale, density and
duplication; it does not establish what a system is.

The archive is still not sufficient to classify historical concepts. Four cards
cannot anchor a portfolio of this size, and forcing concepts against whichever
systems happen to be carded is the specific failure the evidence discipline
exists to prevent.

**Grading the classifier.** When that stage is built, it should be scored
against `wking53214/touchstone` rather than against examples written alongside
it. TOUCHSTONE is a specimen corpus with per-specimen stated correct answers,
built precisely because "every verification claim in this ecosystem is currently
calibrated against material its own author invented". Using it is the difference
between a classifier that is tested and one that is only demonstrated.

## Next systems, in priority order

Revised after the census.

1. **SRE** (`touchstone/specimens/pairs/sre_system_resilience_evaluator_adapter.py`)
   — 570 lines, verified reconstruction, and the live successor to URE. The
   family's working member and the one URE should be read against.
2. **Conservation Kernel** — densest fail-closed code in the portfolio (one
   raise per 54 lines), supplies the epistemic vocabulary the cognitive
   architecture investigation recommends interoperating with, and unblocks U-5.
3. **observe-perceive** — 20,615 lines, the "governed action gate" and, per
   `sentinel_os`'s README, the first sellable unit of the stack.
4. **GSA family** — `gsa-815` (14,716 lines, 13 enums) and `gsa-master-kernel`
   (2,486 lines, 5 flattened artifacts) alongside the two identical ~5,000-line
   `GSA.py` copies in `observe`. Four GSA-shaped things; the canonical one is
   undetermined.
5. **TOUCHSTONE** — not a system, so not a normal card, but it needs an entry
   describing what the corpus contains and how to score against it.
6. **SYNAPSIS** — still named in Innovation OS's integration contract. Read it
   to establish what it actually is; its 1,262 lines suggest the answer is
   short.
