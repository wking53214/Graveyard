# Burial: STRIDE (entire repo retired)

- **Date:** 2026-10-08
- **Source:** github.com/wking53214/stride, branch `main`, commit `596f81b`
- **Contents:** `snapshot/` (the files as they were at that commit) and `stride-full-history.bundle` (complete git history, 3 commits)

## What it was

A reconstruction of the STRIDE gateway, rebuilt from fragments of a pasted conversation. It held several flattened variants of the same code, the recovered evidence, manifests, provenance notes, and reports.

## Why it was retired

It is superseded. Every part worth keeping now lives in a better form elsewhere:

- **DIT:** hardened signing (it refuses the old hardcoded key), a hash-chained ledger, the kinetic governor, an oscillation guard, and the linguistic gates.
- **ZTS:** the gates plus a constraint-based rewrite loop. A telemetry dashboard was added on branch `feature/telemetry-dashboard` (PR #9).
- **sentinel_os:** the graph extractor, the hash-chained adapter, the loop guard, and backpressure.

The one piece that existed only in STRIDE was the analytics layer (distortion, fragility, stability, confidence). It was not ported. Its "repeat contact" input is really message length, so it measures the payload, not customer behavior.

## Warning

The recovered CLIP source contains a hardcoded signing key string from the GSA lineage. Do not reuse it. DIT refuses it on purpose.

## How to bring it back

- Read the files directly from `snapshot/`.
- For full history, clone the bundle: `git clone stride-full-history.bundle <folder>`.
