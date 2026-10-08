"""
PersonalPronounFilter

Checks for the absence of first-person tokens.

Source: [source: 1]
Extracted verbatim from artifact_8.json (code_modules[].body) - not repaired.
"""

class PersonalPronounFilter:
 @staticmethod
 def is_clean(text: str) -> bool:
 return not bool(LINGUISTIC_PATTERNS["first_person_tokens"].search(text))
