# Execution side effects — NOT part of the RADAR repository

`production_deliveries.jsonl` was **not** recovered. It was created on
2026-09-17 by the reconstruction process running the recovered files once,
unmodified, to observe their behaviour.

Three of the recovered artifacts — `eddp-core-engine-v1.py`,
`eddp-core-engine-v2-refined.py` and `eddp-comprehensive-synthesized.py` —
append to `logs/production_deliveries.jsonl` when executed.

It was committed to `logs/` in the first push (commit `025fd97`) by mistake,
where it read as though it were a recovered artifact. It is moved here, and
labelled, rather than deleted: the fact that these files write to disk on import
is itself a property of the recovered software worth recording.

The timestamps and "DELIVERED" statuses inside it are from the 2026-09-17
validation run. They are not historical.
