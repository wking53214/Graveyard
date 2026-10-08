"""
CITADEL v1.1 -- copy 2 of 2

The second of two non-identical drafts of the CITADEL v1.1 enforcement
engine that were pasted concatenated together in a single prompt and
preserved, unedited, as artifact_1.py (see PROVENANCE.md's "Duplication"
section). artifact_1.py itself was NOT modified to produce this file --
it remains the canonical, flattened, single-line archival copy of both
drafts together, exactly as received. This file is a separately-created,
readable reformatting of the SECOND of the two drafts only, split out for
comparison/reference purposes. See citadel_v1.1_copy1.py for the other
draft (the one citadel_v1.2.py was reconstructed from).

Differences from copy 1, preserved exactly rather than corrected:
  - _simplify_passive here vs. _fix_passive in copy 1 (same job, renamed).
  - PENALTIES here vs. PENALTY in copy 1.
  - k/v variable naming in copy 1's _remove_hedging/_remove_identity vs.
    word/replacement here.
  - The causality check is nested as two `if` statements here vs. one
    combined `if X and Y` in copy 1 -- functionally equivalent.
  - A different __main__ example block (uses pprint).

REAL BUG, preserved as found, NOT fixed: _remove_identity below calls
re.sub(pattern, replacement, flags=re.I) with the `text` argument
omitted. re.sub()'s signature requires (pattern, repl, string, ...), so
this raises "TypeError: sub() missing 1 required positional argument:
'string'" the first time rewrite() reaches an IDENTITY violation --
confirmed live before writing this file. Copy 1's equivalent method does
not have this bug.
"""

import re
import time
from enum import Enum
from typing import Dict, List, Any

# ============================================================
# REGEX DETECTION RULES
# ============================================================
REGEX = {
    "identity": re.compile(
        r"\b(i|me|my|mine|myself|we|us|our|ours|ourselves)\b",
        re.I
    ),
    "hedging": re.compile(
        r"\b(may|might|could|seems|generally|potentially|likely|perhaps|probably|i think)\b",
        re.I
    ),
    "passive": re.compile(
        r"\b(am|is|are|was|were|be|been|being)\b\s+\w+(ed|en)\b",
        re.I
    ),
    "metric": re.compile(
        r"\b\d+(\.\d+)?%|\b\d+\b"
    ),
    "causal": re.compile(
        r"\b(because|due to|driven by|resulting from|caused by|therefore|consequently)\b",
        re.I
    ),
    "emdash": re.compile(r"—")
}

# ============================================================
# ENFORCEMENT PROFILES
# ============================================================
PROFILES = {
    "default": {
        "identity": True,
        "hedging": True,
        "passive": False,
        "causality": False,
        "punctuation": True
    },
    "ops": {
        "identity": True,
        "hedging": True,
        "passive": True,
        "causality": True,
        "punctuation": True
    },
    "exec": {
        "identity": True,
        "hedging": True,
        "passive": True,
        "causality": False,
        "punctuation": True
    },
    "legal": {
        "identity": True,
        "hedging": True,
        "passive": True,
        "causality": True,
        "punctuation": True
    }
}

# ============================================================
# CONSTRAINT ENUM
# ============================================================
class Constraint(Enum):
    IDENTITY = "identity"
    HEDGING = "hedging"
    PASSIVE = "passive"
    CAUSALITY = "causality"
    PUNCTUATION = "punctuation"

# ============================================================
# DETECTOR
# ============================================================
class CitadelDetector:
    def detect(self, text: str, profile: Dict[str, bool]) -> List[Dict[str, str]]:
        violations = []
        if profile["identity"] and REGEX["identity"].search(text):
            violations.append({
                "type": Constraint.IDENTITY.value,
                "snippet": self._extract(REGEX["identity"], text)
            })
        if profile["hedging"] and REGEX["hedging"].search(text):
            violations.append({
                "type": Constraint.HEDGING.value,
                "snippet": self._extract(REGEX["hedging"], text)
            })
        if profile["passive"] and REGEX["passive"].search(text):
            violations.append({
                "type": Constraint.PASSIVE.value,
                "snippet": self._extract(REGEX["passive"], text)
            })
        if profile["causality"]:
            if self._needs_causality(text):
                if not (
                    REGEX["causal"].search(text)
                    or REGEX["metric"].search(text)
                ):
                    violations.append({
                        "type": Constraint.CAUSALITY.value,
                        "snippet": "missing causal support"
                    })
        if profile["punctuation"] and REGEX["emdash"].search(text):
            violations.append({
                "type": Constraint.PUNCTUATION.value,
                "snippet": "—"
            })
        return violations

    def _needs_causality(self, text: str) -> bool:
        trigger_words = [
            "increase",
            "decrease",
            "improve",
            "impact",
            "result"
        ]
        return any(word in text.lower() for word in trigger_words)

    def _extract(self, pattern, text):
        match = pattern.search(text)
        return match.group(0) if match else ""

# ============================================================
# TRANSFORMER
# ============================================================
class CitadelTransformer:
    HEDGE_REPLACEMENTS = {
        "might": "",
        "may": "",
        "could": "",
        "seems": "",
        "probably": "",
        "perhaps": "",
        "likely": "",
        "i think": ""
    }
    IDENTITY_REPLACEMENTS = {
        "i": "",
        "we": "",
        "my": "",
        "our": ""
    }

    def rewrite(self, text: str, violations: List[Dict[str, str]]) -> str:
        updated = text
        for violation in violations:
            if violation["type"] == Constraint.HEDGING.value:
                updated = self._remove_hedging(updated)
            elif violation["type"] == Constraint.IDENTITY.value:
                updated = self._remove_identity(updated)
            elif violation["type"] == Constraint.PASSIVE.value:
                updated = self._simplify_passive(updated)
            elif violation["type"] == Constraint.CAUSALITY.value:
                updated += " due to measurable operational impact."
            elif violation["type"] == Constraint.PUNCTUATION.value:
                updated = self._normalize_punctuation(updated)
        updated = re.sub(r"\s{2,}", " ", updated).strip()
        return updated

    def _remove_hedging(self, text: str) -> str:
        for word, replacement in self.HEDGE_REPLACEMENTS.items():
            text = re.sub(rf"\b{word}\b", replacement, text, flags=re.I)
        return text

    def _remove_identity(self, text: str) -> str:
        for word, replacement in self.IDENTITY_REPLACEMENTS.items():
            # BUG, preserved as found: `text` is missing as the third
            # positional argument to re.sub() here. This raises
            # "TypeError: sub() missing 1 required positional argument:
            # 'string'" the moment this method is reached at runtime.
            # Confirmed live; NOT fixed, per this file's own purpose
            # (faithful separation of the original draft, not correction).
            text = re.sub(rf"\b{word}\b", replacement, flags=re.I)
        return text

    def _simplify_passive(self, text: str) -> str:
        passive_map = {
            "was improved": "improved",
            "is generated": "generates",
            "was completed": "completed"
        }
        for source, target in passive_map.items():
            text = re.sub(source, target, text, flags=re.I)
        return text

    def _normalize_punctuation(self, text: str) -> str:
        return text.replace("—", "–")

# ============================================================
# SCORER
# ============================================================
class CitadelScorer:
    PENALTIES = {
        Constraint.IDENTITY.value: 10,
        Constraint.HEDGING.value: 5,
        Constraint.PASSIVE.value: 5,
        Constraint.CAUSALITY.value: 10,
        Constraint.PUNCTUATION.value: 3
    }

    def score(self, violations: List[Dict[str, str]]) -> int:
        score = 100
        for violation in violations:
            score -= self.PENALTIES.get(violation["type"], 0)
        return max(score, 0)

# ============================================================
# MAIN ENGINE
# ============================================================
class Citadel:
    def __init__(self):
        self.detector = CitadelDetector()
        self.transformer = CitadelTransformer()
        self.scorer = CitadelScorer()

    def enforce(self, text: str, profile: str = "default") -> Dict[str, Any]:
        start = time.time()
        profile_config = PROFILES.get(profile, PROFILES["default"])
        violations = self.detector.detect(text, profile_config)
        original_score = self.scorer.score(violations)
        final_text = self.transformer.rewrite(text, violations)
        latency_ms = round((time.time() - start) * 1000, 2)
        return {
            "original": text,
            "final": final_text,
            "changed": text != final_text,
            "score": original_score,
            "violations": violations,
            "profile_used": profile,
            "latency_ms": latency_ms
        }

# ============================================================
# EXAMPLE USAGE
# ============================================================
if __name__ == "__main__":
    citadel = Citadel()
    sample = "I think this might improve performance — because the workflow was improved."
    result = citadel.enforce(sample, profile="ops")
    from pprint import pprint
    pprint(result)
