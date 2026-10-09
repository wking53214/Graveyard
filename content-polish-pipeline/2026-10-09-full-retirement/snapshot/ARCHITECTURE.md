# Architecture

## Design Principles

This repository implements a **stateless, single-execution quality gate** for LLM output validation. The design prioritizes simplicity, clarity, and focus.

### Core Characteristics

- **Stateless**: No persistent state across invocations. Each `execute()` call is independent.
- **Single linear path**: Validation retry loop is straightforward; no branching or multi-path execution.
- **Functional filter interface**: Filters are pure functions with no side effects.
- **Minimal dependencies**: Standard library only.
- **Testable**: All paths covered by unit tests; easy to reason about behavior.

## Security

The repository provides cryptographic signing and integrity protection:

1. **HMAC-SHA384 Signatures** on validated output (`_compute_signature()`)
   - Default key is well-known (integrity only)
   - Pass a secret `signing_key` for authenticity verification
   - Callers are warned when default key is used

2. **SHA-256 Duplicate Detection** to prevent infinite retry loops
   - Tracks hashes of responses within a single execution session
   - Detects when the LLM generates the same invalid response repeatedly

These mechanisms are sufficient for the use case and are already implemented.

## Decision: No Cryptographic Governance Patterns

**Date**: 2026-09-24  
**Status**: Final  
**Decision**: Do not adopt observe-perceive cryptographic governance patterns (state signatures, branch tracking, immutability boundaries, event chaining, invariant monitoring).

### Rationale

An investigation evaluated whether patterns from observe-perceive/Citadel/FORTRESS architectures (compute_state_signature, GsaUniversalAdapter, branch/fork tracking, reentry handling, etc.) would materially benefit this repository.

**Conclusion**: NO.

### Why These Patterns Are Not Applicable

| Pattern | Why Not | Alternative |
|---------|---------|---|
| `compute_state_signature()` | No persistent state or multi-stage lineage | Current HMAC is sufficient |
| Branch/fork tracking | No branching; single linear retry path | Not applicable |
| Universal adapter pattern | Interface already clean; no third-party modules | Current design is sufficient |
| Immutable boundary enforcement | Strings are immutable; no mutable crossings | Already safe |
| Event chaining | No audit/compliance requirement | Logging + HMAC adequate |
| Invariant/drift monitoring | Regex-based filters; no statistical models | Not applicable |

### Cost of Adoption

- **Code**: +300–500 lines of unused complexity
- **Tests**: +10–20 test cases for unneeded features
- **Schema**: Canonicalization rules that constrain future changes
- **Maintenance**: Verification logic, versioning, documentation
- **Benefit**: Zero. No functional improvement.

### Cost of Not Adopting

- **Zero**. The repository already meets all requirements.

## Conclusion

Keep the architecture simple and focused. This is an appropriate case to say **no** to sophisticated patterns that solve problems this repository does not have.

If the repository's scope expands (e.g., persistent audit trails, multi-stage pipelines, multi-branch execution), this decision can be revisited.

---

**Full investigation report**: See branch `claude/observe-perceive-crypto-investigation-5jg06a` for detailed analysis.
