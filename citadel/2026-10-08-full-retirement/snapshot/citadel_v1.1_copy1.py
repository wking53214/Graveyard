"""
CITADEL v1.1 -- copy 1 of 2

One of two non-identical drafts of the CITADEL v1.1 enforcement engine
that were pasted concatenated together in a single prompt and preserved,
unedited, as artifact_1.py (see PROVENANCE.md's "Duplication" section).
artifact_1.py itself was NOT modified to produce this file -- it remains
the canonical, flattened, single-line archival copy of both drafts
together, exactly as received. This file is a separately-created,
readable reformatting of the FIRST of the two drafts only, split out for
comparison/reference purposes.

citadel_v1.2.py (this repo) was reconstructed from this exact draft --
its own docstring says "copy 1 of 2," and the method name below
(_fix_passive) matches citadel_v1.2.py, distinguishing it from copy 2's
_simplify_passive. See citadel_v1.1_copy2.py for the other draft and its
differences (PENALTY vs. PENALTIES naming, k/v vs. word/replacement
variable naming, a differently-nested causality check, and -- unlike
this copy -- a real bug in _remove_identity: a missing `text` argument
to re.sub() that would raise TypeError at runtime).
"""

import re
import time
from enum import Enum
from typing import Dict, List, Any

# ============================================================
# CITADEL v1.1
# Deterministic LLM Output Enforcement Engine
# ============================================================

# ============================================================
# REGEX DETECTION LAYERS
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
    # PUNCTUATION CONTROL LAYER
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
# CONSTRAINT MODEL
# ============================================================
class Constraint(Enum):
    IDENTITY = "identity"
    HEDGING = "hedging"
    PASSIVE = "passive"
    CAUSALITY = "causality"
    PUNCTUATION = "punctuation"

# ============================================================
# DETECTOR ENGINE
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
        if profile["causality"] and self._needs_causality(text):
            if not (
                REGEX["causal"].search(text)
                or REGEX["metric"].search(text)
            ):
                violations.append({
                    "type": Constraint.CAUSALITY.value,
                    "snippet": "missing causal support"
                })
        # PUNCTUATION ENFORCEMENT
        if profile["punctuation"] and REGEX["emdash"].search(text):
            violations.append({
                "type": Constraint.PUNCTUATION.value,
                "snippet": "emdash detected"
            })
        return violations

    def _needs_causality(self, text: str) -> bool:
        triggers = ["increase", "decrease", "improve", "impact", "result"]
        return any(t in text.lower() for t in triggers)

    def _extract(self, pattern, text):
        m = pattern.search(text)
        return m.group(0) if m else ""

# ============================================================
# TRANSFORMER ENGINE
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
        for v in violations:
            if v["type"] == Constraint.HEDGING.value:
                updated = self._remove_hedging(updated)
            elif v["type"] == Constraint.IDENTITY.value:
                updated = self._remove_identity(updated)
            elif v["type"] == Constraint.PASSIVE.value:
                updated = self._fix_passive(updated)
            elif v["type"] == Constraint.CAUSALITY.value:
                updated += " due to measurable operational impact."
            elif v["type"] == Constraint.PUNCTUATION.value:
                updated = self._normalize_punctuation(updated)
        return re.sub(r"\s{2,}", " ", updated).strip()

    def _remove_hedging(self, text: str) -> str:
        for k, v in self.HEDGE_REPLACEMENTS.items():
            text = re.sub(rf"\b{k}\b", v, text, flags=re.I)
        return text

    def _remove_identity(self, text: str) -> str:
        for k, v in self.IDENTITY_REPLACEMENTS.items():
            text = re.sub(rf"\b{k}\b", v, text, flags=re.I)
        return text

    def _fix_passive(self, text: str) -> str:
        mapping = {
            "was improved": "improved",
            "is generated": "generates",
            "was completed": "completed"
        }
        for a, b in mapping.items():
            text = re.sub(a, b, text, flags=re.I)
        return text

    def _normalize_punctuation(self, text: str) -> str:
        # EN DASH ONLY POLICY
        return text.replace("—", "–")

# ============================================================
# SCORER ENGINE
# ============================================================
class CitadelScorer:
    PENALTY = {
        Constraint.IDENTITY.value: 10,
        Constraint.HEDGING.value: 5,
        Constraint.PASSIVE.value: 5,
        Constraint.CAUSALITY.value: 10,
        Constraint.PUNCTUATION.value: 3
    }

    def score(self, violations: List[Dict[str, str]]) -> int:
        s = 100
        for v in violations:
            s -= self.PENALTY.get(v["type"], 0)
        return max(0, s)

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
        config = PROFILES.get(profile, PROFILES["default"])
        violations = self.detector.detect(text, config)
        score = self.scorer.score(violations)
        final = self.transformer.rewrite(text, violations)
        return {
            "original": text,
            "final": final,
            "changed": text != final,
            "score": score,
            "violations": violations,
            "profile_used": profile,
            "latency_ms": round((time.time() - start) * 1000, 2)
        }

# ============================================================
# EXAMPLE
# ============================================================
if __name__ == "__main__":
    engine = Citadel()
    sample = "I think this might improve performance — because workflow was improved."
    print(engine.enforce(sample, profile="ops"))
