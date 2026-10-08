"""
EmpiricalValidationFilter

Checks for the presence of causal connectives or numeric metrics.

Source: [source: 1]
Extracted verbatim from artifact_8.json (code_modules[].body) - not repaired.
"""

class EmpiricalValidationFilter:
 @staticmethod
 def is_clean(text: str) -> bool:
 has_causality = bool(LINGUISTIC_PATTERNS["causal_connectives"].search(text))
 has_metrics = bool(LINGUISTIC_PATTERNS["numeric_metrics"].search(text))
 return has_causality or has_metrics
