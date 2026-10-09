# Unresolved questions

Open items the archive must not silently resolve. Each names what would settle
it. `UNKNOWN` is the current answer to all of them.

---

## U-1. RESOLVED (2026-09-12) — URE is a superseded member of a four-way resilience-engine family

**Was** `UNKNOWN`. **Now** `[CODE]`.

URE's source is `touchstone/specimens/superseded/ure-universal-resilience-engine-flattened.py`
(11,273 bytes, flattened to one line, does not parse). The portfolio census
found all eight handoff marker symbols resolving to `touchstone` and nowhere
else.

Resolution, with the evidence in `cards/URE.md` §9:

- **URE and SRE are the same system renamed.** All ten classes map 1:1; nine of
  nine telemetry fields correspond, one (`processing_latency`) identically.
- **The family is URE / SRE / SOLVAR `LyapunovStabilityModule` / GOV4
  `RegimeClassifier`**, sharing the weighted-squared-deviation energy formula
  and the constants 1e-4 and 1e-2. `resilience_stability_kernel.py`, built
  2026-09-03 as the de-duplicated implementation, states it outright: "That
  isn't coincidence - it's the same design, copy-pasted and reskinned per
  source repo."
- **OBSERVE is not in this family.** No drift energy, no shared constants, no
  shared threshold names, one generic shared regime member. The earlier
  inference in `cards/OBSERVE.md` leaned the other way and has been corrected
  in place.
- **URE is superseded and unconsumed.** Nothing imports it, by an explicit
  decision recorded in `resilience_stability_kernel.py`'s header: its regime
  classifier "is hardcoded rather than derived from its inputs ... so it isn't
  a source of real logic to share".

The discriminator that settled it was the one named here in advance: shared
threshold *values* and field vocabulary, not shared structure. Structure alone
had pointed at OBSERVE, and was wrong.

**Still open** — which of URE and SRE came first. Both are flattened specimens
with no commit dates of their own. `UNKNOWN`.

---

## U-2. Which of the two OBSERVE copies is canonical?

**Status** `UNKNOWN` — `[CODE]` establishes they differ; nothing establishes which leads.

| | `observe/observe_consolidated.py` | `observe/sentinel_os/observe_consolidated.py` |
| --- | --- | --- |
| Lines | 1,510 | 1,408 |
| Imports | stdlib only | + `kalman_trajectory`, `threading` |
| Hoisted constants | 8 named tunables | 4 |
| `REGIME_DISTRIBUTION_BANDS` | present | absent from extracted constants |

The root copy has the more developed calibration surface; the `sentinel_os/`
copy has the Kalman trajectory dependency. Neither is a superset.

**To settle** — commit history on both paths, or an explicit declaration.

---

## U-3. `GSA.py` and `GSA_Governance_Operating_Core_Enterprise.py` are duplicates

**Status** `[CODE]` — established, needs a decision, not more evidence.

Both in `observe/sentinel_os/`. 4,986 and 4,988 lines. `diff` output is **7
lines total**: one added `replace,` import and a trailing-newline difference.
Identical enums (12), identical classes (45).

Roughly 5,000 lines of governance core exist twice with no functional
divergence. Which name is canonical is a naming decision for the owner.

---

## U-4. The handoff's OBSERVE fingerprint does not match OBSERVE's code

**Status** `[CODE]` — established. See `cards/OBSERVE.md` §9.

Of nine remembered markers, six are present (some under different names), one is
partial, and two — HMAC-SHA256 pseudonymization and exponential decay weighting
— are absent from OBSERVE and live in other modules
(`sentinel_os/compliance_exporters.py`, `sentinel_os/observe_perceive_core.py`).
Governance approval gates belong to PERCEIVE, not OBSERVE.

This is the archive's justification, demonstrated on its own source material: a
fingerprint held in memory accretes capabilities from neighbouring systems.

---

## U-5. `conservation_kernel` is an unvendored external dependency

**Status** `[CODE]` — established. Source now available (census, 2026-09-12).

`sentinel_os/conservation/boundary.py` and `judgment.py` import
`conservation_kernel` at module level. The package is not vendored into
`sentinel_os`; it lives in `wking53214/Conservation_Kernel`, now cloned and
measured: 33 files, 4,375 lines, 12 enums, 81 raise sites — **one raise per 54
lines, the densest fail-closed code in the portfolio**, three times denser than
`sentinel_os` itself. Whether installing it makes the boundary executable is
untested. `[EXPERIMENT]`

Consequence: `sentinel_os`'s conservation boundary — the fail-closed choke point
that `governance_harness._write_decision` calls before any durable write —
cannot execute from a clone. The repository's own README states this and
records the measurement: 968 tests collected, 658 passing without Postgres and
the other undeclared dependencies, 228 skipped, 39 failed, 38 errored, measured
2026-09-09 at `5341e3d`. `[REPOSITORY HISTORY]`

---

## U-6. 24 of 39 repositories measured; 4 carded

**Status** partially closed by the census (`PORTFOLIO_CENSUS.md`, 2026-09-12).

24 repositories are now cloned and structurally measured. Measurement is not a
card: it establishes scale, density and duplication, not what a system *is*.

Unmeasured: `CODE`, `GRAPH`, `KAGGLE`, `Ecology`, `Resume_OS`,
`content-polish-pipeline`, `ghost_tools`, and the seven history corpora.

No system should be described, classified, or reasoned about from its name or
its line count alone. `synapsis` is the cautionary case: named in the handoff as
a major system and in Innovation OS's integration contract as a future
connection, it measures 1,262 lines with zero enums, zero tunables and one raise
site. That is a size fact. What SYNAPSIS *is* remains `UNKNOWN` until someone
reads it.

---

## U-8. 35 files share a path across `observe` and `sentinel_os` with diverged content

**Status** `[CODE]` — established 2026-09-12.

`observe/sentinel_os/` is a near-copy of the `sentinel_os` repository: 95 paths
exist in both, 60 byte-identical, **35 diverged**. 81 files exist only in the
`observe` copy, 68 only in `sentinel_os`.

Two copies of the same module, at the same path, with different content and no
declared canonical side. This is the highest-risk duplication found: unlike
U-3, the copies are not identical, so a reader cannot assume either is current.

Portfolio-wide, 97 byte-identical files ≥2 KB span more than one repository,
totalling 912,610 redundant bytes.

**To settle** — a declaration of which repository owns each diverged module, or
commit history on both paths.

---

## U-9. 16 flattened sources cannot have produced any result attributed to them

**Status** `[CODE]` — established 2026-09-12.

Flattened files — an entire module on one line, line breaks destroyed by a
copy-paste through a chat interface — exist in `touchstone` (10),
`gsa-master-kernel` (5) and `vanguard` (1). Each raises `SyntaxError` on
import.

In TOUCHSTONE this is deliberate and catalogued. In `gsa-master-kernel` it is
not obviously so: five files named `artifact_1.py` … `artifact_14.py`, matching
TOUCHSTONE's `reference/` naming, sit in a repository that is not a specimen
corpus.

**To settle** — whether `gsa-master-kernel`'s flattened artifacts are preserved
specimens or unrepaired damage.

---

## U-7. Innovation OS's declared integrations do not exist

**Status** `[CODE]` — established.

`docs/architecture/intelligence_v2/api/integration_contract.md` lists "Future
connections: Sentinel OS, Synapsis, Governance systems, Simulation systems,
Deployment runtime". The document labels them future, correctly. No import of
any of them exists in `src/`.

Recorded so that a later reader does not mistake the contract document for a
description of built integration.
