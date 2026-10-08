# ARCHIVE

Eight archived "System Architecture and Integration Report" JSON payloads
(`artifact_1.json`...`artifact_9.json`, turn 4 skipped — byte-identical
duplicate of turn 1). See `PROVENANCE.md` for the full source writeup and
`TRANSCRIPT.md` for the original conversation. **Note:** `artifact_N.json`
= turn N verbatim; this doesn't match the "Report N" numbering used in
some prior discussion of this repo's content.

## Two corruptions affect nearly everything in the source JSON

Neither was introduced during extraction — both are baked into the
`artifact_N.json` files themselves:

1. **Indentation was flattened to a uniform single space per line**,
   independent of real nesting depth. Not mechanically repairable —
   reconstructing true indentation would mean guessing at intent.
2. **Every doubled character sequence was collapsed to one**: `__init__`
   → `init`, `from __future__ import` → `from future import`,
   `if __name__ == "__main__"` → `if name == "main"`, `**` (exponent,
   `**kwargs`) → nothing. Confirmed zero `__` or `**` occurrences
   anywhere in the corpus.

## `extracted/`

Real code pulled out of each JSON payload's `code_modules[].body`,
extracted verbatim (not repaired) into individually-named `.py` files
under `extracted/report_N/`. `artifact_5.json` has no `code_modules` — a
"Meta-OS menu config" instead (`report_5/meta_os_menu_config.json`, the
payload itself being the artifact).

19 files that were confirmed duplicative of content already
consolidated elsewhere this week were removed after extraction and
cross-referencing (each check described below) rather than kept as a
third copy:

- **GSA wrapper content** (`gsa_universal_interlock_wrapper.py`,
  `gsa_unified_framework.py`, `PipelineCycleManager`, `GraphExtractor` —
  all from `artifact_2.json`): diffed field-by-field and confirmed
  identical (modulo the corruption above) to
  [GSA-GATEWAY](https://github.com/wking53214/GSA-GATEWAY)'s
  `governance-stack/code-repo-governance-and-gsa-core.py`.
  `GraphExtractor` is the recurring AST tool, already canonical in
  `synapsis`.
- **IVR + content-pipeline content** (`artifact_6.json`,
  `artifact_7.json`, and duplicates of the latter inside
  `artifact_8.json`): same `BaseIVR`/`HomeSecurityIVR`/
  `ContentPolishPipeline`/`SecureDataIngestionPipeline`/
  `CoreDataPipelineOrchestrator` already consolidated into `CODE` and
  `EDDP`.
- **OBSERVE Clinical Engine** (`RiskAdapters`, `RiskAdaptersPhysiological`,
  `BayesianFusion`, `EscalationPolicy`, `ObserveClinicalEngine`, all
  from `artifact_8.json`): diffed `RiskAdapters.bayesian()` line-by-line
  against [observe](https://github.com/wking53214/OBSERVE)'s
  `sentinel_os/observe_consolidated.py` — identical logic, identical
  `# FIX:` comments documenting the same bug-fix history. This snapshot
  matches the *already-integrated, already-bug-fixed* production
  version, not an earlier draft — no real drift found here, unlike the
  report below.

## Moved to FORTRESS

`report_2/Fortress.py` and `report_8/PredictiveStateController.py` moved
to [FORTRESS](https://github.com/wking53214/FORTRESS) once that repo
was created — see its README for the full picture, including a third
variant copied there from `sentinel_os`.

## What's kept, and why

- **`report_1/`** (`Simulator.step invocation`, `LatentPayload v1/v2
  modifications`, `DynamicState modifications`, `Repository_Layout`):
  not runnable code at all — diff/patch-style change descriptions
  (`@@ Fields @@`, `+`-prefixed additions) and a plain directory
  listing. Kept as historical design notes.
- **`report_2/PULSEARMPipeline.py`**: real orchestration logic, but
  references external classes (`ArtifactSuppressor`, `TemporalEngineV3`,
  `KalmanLatentFilter`, `CalibrationLayer`, `ImmutableAuditLog`,
  `DriftDetector`) that aren't defined anywhere in this payload — the
  same names sitting unextracted inside
  `CODE/content-pipeline-user-source.py`'s flattened blob. Can't run
  standalone; not the mocked-stub pattern, just missing dependencies.
  (`report_2/Fortress.py`, same situation, moved to
  [FORTRESS](https://github.com/wking53214/FORTRESS) once that repo
  existed — see below.)
- **`report_2/OmegaEmergencyStasis_Core_Logic_Gates.py`,
  `report_3/*`** (`Omega15Substrate`, `GSASycophancyFilter`,
  `GSAEquilibrium`, `Omega36PneumaticSubstrate`): narrative material,
  not design intent — same standing conclusion as everywhere else this
  content has appeared. Kept, labeled, no engineering effort spent on
  it.
- **`report_5/meta_os_menu_config.json`**: not code, no destination
  proposed.
- **`report_8/PersonalPronounFilter.py`, `SpeculativeLanguageFilter.py`,
  `EmpiricalValidationFilter.py`, `TextNormalizer.py`,
  `ExecutionPacer.py`, `ToneNormalizationPipeline.py`,
  `ClinicalSignalValidator.py`**: checked against CODE, GSA-GATEWAY,
  EDDP, observe, CITADEL, STRIDE — genuinely not present anywhere else.
  Real, standalone content with no confirmed duplicate; no destination
  proposed yet.
- **`report_8/UGPISOmegaController.py`**: the actual integration code
  showing how DIT, OBSERVE, FORTRESS, URE, EDDP, and GSA call into each
  other via a single `process_inbound` method — none of the wired-in
  classes are defined here, this is pure integration architecture. The
  clearest single artifact in this whole sweep answering "how do these
  systems fit together." Deliberately not filed anywhere.
- **`report_9/`** (`ClaudeGovernanceDecider`, `IcebergProductionHarness`,
  full working test suite): real production code, but an **older**
  snapshot with confirmed drift from what's live now in
  [GSA-815](https://github.com/wking53214/GSA-815)/
  [sentinel_os](https://github.com/wking53214/sentinel_os) — the live
  `ClaudeGovernanceDecider` now inherits `__init__`/`safety_check`/
  `get_decision_log` from a `GovernanceDecider` base class
  (`sentinel_os/governance_decider.py`) that didn't exist in this
  snapshot, and live `IcebergProductionHarness` gained cassette/replay
  support (`swap_cassette`, `_assemble_live_episode`) not present here.
  Kept as historical record of the pre-refactor shape — not something
  to overwrite live code with.

No repos were deleted or archived as part of this pass.
