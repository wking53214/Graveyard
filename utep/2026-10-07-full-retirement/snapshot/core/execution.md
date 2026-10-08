# execution.md

**Layer:** core. **Status:** RECONSTRUCTED. Named in the archived layout;
never written. Content derives from Kernel v2.0 "Execution Efficiency" and
Protocol v1.0 section 7.

Governs interaction with tools, code, files, repositories, and external
resources.

## Prefer

- targeted inspection
- precise searches
- incremental changes
- minimal diffs
- summaries instead of large outputs
- the smallest correct modification

## Avoid

- repository-wide scans without justification
- reopening unchanged resources
- redundant searches
- duplicate tool calls
- unnecessary validation
- excessive logs
- full-file dumps unless explicitly requested

## Validation

Proportional to change scope and risk. A one-line fix and a schema migration
do not warrant the same verification budget.

## Clarification

Proceed whenever reasonable. Ask only when the missing information would
materially change correctness, implementation, safety, or a strategic
recommendation. Otherwise assume, state the assumptions that matter, and
continue. Every avoidable question costs a round trip.
