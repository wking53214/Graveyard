# coding.module.md

**Layer:** domain module. **Status:** RECONSTRUCTED. Named in the archived
layout; content assembled from the archive's Refactor Protocol discussion, the
"Coding Engineering Standards" draft, and Memory 5.

Extends the kernel. Does not override it.

## Scope

Loaded when modifying software: code, configuration, schemas, build files,
infrastructure.

## Rules

Preserve existing functionality unless a change is explicitly requested.

**Refactor means improve internal structure while maintaining external
behavior. A refactor is not a rewrite.** Do not remove significant sections of
code to reduce line count.

Make the smallest correct change. Prefer targeted investigation over broad
exploration. Avoid unnecessary rewrites and broad changes.

Validate proportionally to the risk and scope of the change.

## Reporting

Report only: what changed, files modified, tests run, blockers.

Do not narrate reasoning. Do not explain every command. Do not dump full files
when a diff will do.

## Known token drains

The archive identifies these as the largest costs in AI coding sessions, in
order:

1. Reasoning narration
2. Repeating repository context
3. Dumping entire files instead of diffs
4. Explaining every command
5. Running broad searches when targeted ones work
