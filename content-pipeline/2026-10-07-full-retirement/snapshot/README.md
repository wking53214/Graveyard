# CODE

## Archived AI Chat Transcript — Content-Polish/IVR Code Paste

This repository preserves a single AI chat transcript (Google Gemini) in which the user pasted a large body of Python source and asked the AI to split it into separate, versioned modules. It is archival material, not an active software project.

**See [`PROVENANCE.md`](./PROVENANCE.md) for the authoritative account of what this repository contains** — source, extraction method, execution status, and everything noticed but deliberately left unfixed. This README summarizes it; PROVENANCE.md is the ground truth if the two ever disagree.

## What's here

| File | What it is |
|---|---|
| `content-pipeline-user-source.py.flattened` | The user's original pasted source, flattened onto one line, with two Kaggle API tokens redacted. It does not parse, so it carries a `.flattened` extension to stop tools reading it as a program (see PROVENANCE.md). |
| `content-pipeline-modularized.txt` | The AI's module-separated response, verbatim except for later, deliberate cross-repo moves (below). Renamed `.txt` because it is not valid Python: it still contains several bare `Module: <name>.py \| Version: v1.0.0` header lines (not comments; the AI included them as plain text), which are Python syntax errors. This is intentional: the archival convention here is to move misplaced content to its correct home, not to repair broken syntax in preserved material. The IVR classes, the caller-state structs, the 7-class Omega cluster, and the `gsa_core_engine.py` residue (six utility functions and six orphan dataclasses) have since been removed from this file (see "Phase 1 consolidation" below); what remains is `ContentPolishPipeline` and the empty `governance_filters.py` header stub. |
| `business-strategy-notes.md` | Turns 2–6 of the transcript (the module summary, "combine into one system" discussion, monetization/first-customer strategy) extracted into readable notes — real strategic thinking that was otherwise buried inside `TRANSCRIPT.md`. |
| `TRANSCRIPT.md` | The complete source transcript, all six turns, with two Kaggle API tokens redacted. |
| `PROVENANCE.md` | Source, extraction method, execution status, and known defects. Read this first. |

## What's no longer here

Two later commits moved classes that didn't belong in this repo to their correct homes, without editing them:

- `SecureDataIngestionPipeline`, `CoreDataPipelineOrchestrator` → `EDDP/content-pipeline-eddp-classes.py`
- `ComplianceFiltrationFilter`, `SystemicTrajectoryRegistry`, `TelemetryDispatchBus`, `EvolutionaryRecursionEngine`, `ConstitutionalGovernorLayer`, `GsaContextEnvelope`, `compute_state_signature`, `GsaStaticAnchorManager`, `GsaUniversalAdapter`, `PipelineCycleManager` → `GSA-GATEWAY/governance-stack/code-repo-governance-and-gsa-core.py`

What was left in place — `ContentPolishPipeline`, the IVR content (`BaseIVR`/`HomeSecurityIVR`/`process_ivr`), the Omega-prefixed classes, `gsa_core_engine.py`'s utility functions and dataclasses, and `telemetry_simulator.py` — wasn't confidently a match for either destination at the time; see the commit message on `5c35a2d` for the specific reasoning per class. Phase 1 (below) has since migrated some of these and dropped the rest.

## Phase 1 consolidation

Phase 1 routed three bodies of code out of this repo into their real homes, each landed unwired and clearly provenance-marked, then removed four `Module:` sections from `content-pipeline-modularized.txt` — the three migrated ones plus `gsa_core_engine.py`, a residue of small utilities and orphan dataclasses that had no destination and is referenced by nothing left in the file. That leaves `content_pipelines.py` (`ContentPolishPipeline`) and the empty `governance_filters.py` header. `content-pipeline-user-source.py.flattened` (the flattened raw paste) was left untouched by this phase, apart from the later token redaction, and still holds every removed section.

| Move | From | Landed as | Notes |
|---|---|---|---|
| 1 | `content-pipeline-modularized.txt` — `telemetry_simulator.py` section (`LatentPayload`, `DynamicState`) | `GSA-815 : Latent/ivr_perceived_wait_model.py` | Richer IVR perceived-wait / frustration-escalation model, landed **beside** GSA-815's canonical `Latent/LatentPayload.py` + `Domain/CallerState.py` (not merged, not wired). Classes renamed to avoid reading as competitors. Two source defects **fixed on landing** (`to_dict()` returned `{}` for every field; `update_after_step` mutated its argument — it now returns a new dynamics object and leaves the input alone); fields, math and coefficients otherwise unchanged. |
| 2 | `content-pipeline-modularized.txt` — `ivr_triage.py` section (`BaseIVR`, `HomeSecurityIVR`, `process_ivr`) | `GSA-815 : cassettes/ivr_triage_archival_from_code.py` | Industry IVR triage sketch; no collision with the live `cassettes/ivr_cassette.py`. The `init` vs `__init__` defect in both classes is **preserved, not fixed**, and documented in the landed file. The two divergent `BaseIVR` versions in `content-pipeline-user-source.py.flattened` were reconciled into one (union of `handle_call` + `get_route`, with `.get()` lookups). |
| 3 | `content-pipeline-user-source.py.flattened` (flattened raw paste) — `GraphExtractor`, `extract_graph`, `graph_to_dict`, `Node`/`Edge`/`Graph` | `GRAPH : from-code/ast_graph_extractor.py` | Reconstructed from the single-line source, then extended (William's v1.0.0: an architecture-notes header, frozen `Node`/`Edge`, a `total_row_count` field on `Graph`). Fills a real gap: nothing in GRAPH walked source code. `resolve_attr_chain` records a partial target for calls like `make_factory().build()` — flagged in the apply script. The sibling `DeterministicGraphExtractor` (a two-method stub) was deliberately **not** carried over. |

The destination-side additions were made by `apply_code_to_gsa815_move_v1.sh` and `apply_code_to_graph_move_v1.sh`; the removal here by `apply_code_phase1_trim_v2.sh`. Each change was reviewed as a staged diff before being committed to its own repo.

`ContentPolishPipeline` stays here as the archival copy. Its maintained, packaged reimplementation lives in [`wking53214/content-polish-pipeline`](https://github.com/wking53214/content-polish-pipeline) — that is the version to use; this one is a record of the original AI output.

The Omega cluster was removed as all seven classes together (`Omega15Substrate`, `GSASycophancyFilter`, `GSAEquilibrium`, `Omega36PneumaticSubstrate`, `OmegaEmergencyStasis`, `DataDirective`, `GSAOmegaPoint`) — removing only the name-prefixed ones would have stranded `DataDirective` and `GSAEquilibrium` on deleted dependencies. Unlike Moves 1–3 these classes have no home elsewhere in the ecosystem: they were dropped, not migrated.

The `gsa_core_engine.py` section — `register_as_module`, `gsa_deep_freeze`, `deep_freeze_structure_function`, `set_global_seed`, `safe_stdev`, `audit_append`, a mock `np`, the `Payload`/`Node`/`Edge`/`Graph`/`RiskSignal`/`AuditEntry` dataclasses, and a truncated `@dataclass(frozen=True)` with no class body — was removed on the same "no destination, nothing references it" basis. `5c35a2d` had left it in place for lack of a clean target; the two utilities worth keeping (`register_as_module`, `gsa_deep_freeze`) were reconstructed into GSA-GATEWAY independently, and `Node`/`Edge`/`Graph` are superseded by Move 3's extractor.

Everything removed in this pass remains fully preserved in `content-pipeline-user-source.py.flattened` and `TRANSCRIPT.md`, which it does not touch.

## Status

Nothing in this repository is meant to run as-is. It is a preserved record of one AI chat session's code output. The pieces that belonged elsewhere have been routed to their homes (see "Phase 1 consolidation"); the pieces with no home were dropped from the modularized file but stay fully preserved in `content-pipeline-user-source.py.flattened` and `TRANSCRIPT.md`. What remains in `content-pipeline-modularized.txt` — `ContentPolishPipeline` and the empty `governance_filters.py` header — is kept as the archival record of the AI's output, not as working code. This pass is complete; the repository is a closed archive.

## License

[Apache License 2.0](./LICENSE). The preserved transcript content is AI-generated output reproduced for archival purposes; the license covers this repository's organization, documentation, and any reconstructed material.
