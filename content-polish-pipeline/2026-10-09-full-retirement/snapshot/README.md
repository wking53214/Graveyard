# ContentPolishPipeline

LLM output quality gate: validates generated text against linguistic constraints and retries with recalibration feedback.

## What It Does

Sits between an LLM and a downstream consumer. Calls the LLM, checks output for:
- First-person pronouns (I, we, my, our, etc.)
- Speculative language (might, may, could, probably, etc.)
- Empirical support (metrics, evidence, citations)

If all checks pass, returns the validated text. If not, retries with feedback explaining what to fix.

## Install

```bash
pip install .
```

Installs the `content_polish_pipeline` package (pure standard library; `pytest` is the only optional dependency, for the test suite).

## Usage

```python
import asyncio
from content_polish_pipeline import ContentPolishPipeline

# Define your LLM call
async def my_llm(prompt: str) -> str:
    # Your LLM API call here
    return "Generated text..."

# Create the pipeline
pipeline = ContentPolishPipeline(
    execution_gateway=my_llm,
    max_attempts=5,          # must be >= 1
    signing_key=b"your-secret-key",  # optional; see Design Notes
)

# Run it
result = await pipeline.execute("Write a report on X")

if result["execution_status"] == "SUCCESS":
    print(f"Validated: {result['validated_content']}")
    print(f"Attempts: {result['retry_attempts']}")
    print(f"Time: {result['latency_duration_ms']}ms")
else:
    print(f"Failed after {result['retry_attempts']} attempts")
    print(f"Issues: {result['violations']}")
```

## Result Format

```python
{
    "execution_status": "SUCCESS" | "CRITICAL_FAILURE",
    "validated_content": str | None,  # Only on SUCCESS
    "retry_attempts": int,
    "violations": list[str],  # Constraint violations
    "latency_duration_ms": float,
    "payload_signature": str | None,  # HMAC-SHA384
    "oscillation_detected": bool,  # Repeated normalized outputs detected
}
```

## Filters

Each filter exposes `passes(text) -> bool` and can be used independently.
`True` means the text satisfies that filter. The requirements point in
different directions: the pronoun and speculation filters pass when their
pattern is **absent**, while the empirical filter passes when its pattern
is **present** (no evidence markers = a claim without backing). `is_clean`
is kept as an alias of `passes`.

```python
from content_polish_pipeline.filters import (
    PersonalPronounFilter,
    SpeculativeLanguageFilter,
    EmpiricalValidationFilter,
)

text = "I think this might improve performance."

pronoun_filter = PersonalPronounFilter()
print(pronoun_filter.passes(text))      # False (has "I")
print(pronoun_filter.violations(text))  # ['I']  (unique, sorted)

speculation_filter = SpeculativeLanguageFilter()
print(speculation_filter.passes(text))      # False (has "i think", "might")
print(speculation_filter.violations(text))  # ['i think', 'might']

empirical_filter = EmpiricalValidationFilter()
print(empirical_filter.passes(text))      # False (no evidence markers)
print(empirical_filter.violations(text))  # ['Missing empirical support ...']
```

## Oscillation Detection

The pipeline tracks repeated normalized outputs to prevent infinite loops. The `OscillationDetector` is used internally and exposes its result via the `oscillation_detected` flag in the pipeline result.

```python
from content_polish_pipeline.oscillation import OscillationDetector

detector = OscillationDetector(max_history=32)

# First observation
result = detector.observe("Candidate accepted")
print(result)  # False (first time seen)

# Repeat (exact match)
result = detector.observe("Candidate accepted")
print(result)  # True (already observed)

# Normalized repeat (whitespace + case variations)
result = detector.observe("  CANDIDATE ACCEPTED  ")
print(result)  # True (normalized to same text)

# New observation
result = detector.observe("Candidate rejected")
print(result)  # False (never seen before)

# Reset history
detector.reset()
result = detector.observe("Candidate accepted")
print(result)  # False (history was cleared)

# Get current history snapshot
history = detector.get_history()
print(history)  # ['candidate accepted']
```

**Important:** The `OscillationDetector` is a diagnostic tool only. It reports repeated outputs but does not independently modify them, approve/reject candidates, bypass validation, or alter governance. The pipeline uses it to:
- Prevent infinite loops during retries
- Signal repeated output patterns to the caller
- Facilitate observability and debugging

## Customization

To use different filters or extend behavior:

```python
class MyCustomFilter:
    def passes(self, text: str) -> bool:
        return True  # Your logic

    def violations(self, text: str) -> list[str]:
        return []  # Your violations

# Use it by modifying pipeline.py to add your filter
```

## Design Notes

- **Retry logic:** On failure, provides recalibration feedback explaining what to fix. The LLM sees the original prompt plus feedback.
- **Oscillation detection:** Tracks repeated normalized outputs within a bounded history (default 32) to prevent infinite loops. The `OscillationDetector` observes each output and signals when an exact normalized recurrence is detected. The `oscillation_detected` flag is exposed as a non-authoritative diagnostic signal — it does not independently approve, reject, or modify outputs; it only reports observations to the calling system.
- **Oscillation normalization:** Text is normalized by stripping whitespace and converting to lowercase for comparison. "Candidate accepted", " CANDIDATE ACCEPTED ", and "candidate accepted" are treated as equivalent.
- **Async-first:** All LLM calls are async. Use `asyncio.run()` or integrate into an async context.
- **Deterministic output:** Given a deterministic LLM, the same input prompt produces the same result. Filter `violations()` lists are unique and sorted, so recalibration feedback is stable too.
- **Signature:** `payload_signature` is an HMAC-SHA384 of the validated text. The default `signing_key` is a well-known constant and provides an integrity checksum only — pass your own secret `signing_key` for the signature to be meaningful for authenticity. A warning is logged when the default key is in use.

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE). Copyright 2026 William N. King.

## Version

1.1.0

### Changelog

- **1.2.0** — Refactored duplicate detection into dedicated `OscillationDetector` class with bounded history (default 32). Detector is exposed as a public API via `from content_polish_pipeline import OscillationDetector`. Pipeline result now includes `oscillation_detected` diagnostic signal. Oscillation detection remains non-authoritative; it reports but does not alter governance decisions.
- **1.1.0** — Packaged with `pyproject.toml` (`pip install .`); filters gained `passes()` (`is_clean` kept as alias); `violations()` output now sorted; `max_attempts < 1` raises `ValueError`; duplicate-detection hash switched from MD5 to SHA-256; default signing key now logs a warning.
- **1.0.0** — Initial release.
