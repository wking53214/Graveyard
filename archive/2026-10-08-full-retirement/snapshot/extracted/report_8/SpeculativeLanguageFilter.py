"""
SpeculativeLanguageFilter

Checks for the absence of hedging or speculative tokens.

Source: [source: 1]
Extracted verbatim from artifact_8.json (code_modules[].body) - not repaired.
"""

class SpeculativeLanguageFilter:
 @staticmethod
 def is_clean(text: str) -> bool:
 return not bool(LINGUISTIC_PATTERNS["hedging_tokens"].search(text))
