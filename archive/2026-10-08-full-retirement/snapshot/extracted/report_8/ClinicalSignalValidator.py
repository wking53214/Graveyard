"""
ClinicalSignalValidator

Domain-specific validation ensuring clinical signals possess temporal specificity, numeric values, and clinical context.

Source: [source: 1]
Extracted verbatim from artifact_8.json (code_modules[].body) - not repaired.
"""

class ClinicalSignalValidator:
 """Domain-specific validation for clinical signals. OPPOSITE of linguistic polishing."""
 
 REQUIRED_CLINICAL_MARKERS = {
 "temporal_specificity": re.compile(r"\b(\d{1,2}:\d{2}|hour|minute|second|onset)\b", re.IGNORECASE),
 "numeric_value": re.compile(r"\b\d+(\.\d+)?(?:\s*(?:bpm|mmHg|beats|percent|%|SpO2|O2|sats))\b", re.IGNORECASE),
 "clinical_context": re.compile(r"\b(patient|neonate|infant|pediatric|vital|monitor|alert|abnormal)\b", re.IGNORECASE),
 }
 
 HEDGING_IS_GOOD = re.compile(
 r"\b(may|might|could|possibly|uncertain|unclear|suggest)\b",
 re.IGNORECASE,
 )

 def init(self, profile_name: str = "clinical"):
 self.profile_name = profile_name
 self.validation_log: List[Dict[str, Any]] = []

 def validate_signal(self, signal_text: str) -> Tuple[bool, List[str]]:
 """Check if signal has minimum clinical coherence."""
 failures: List[str] = []
 
 # Clinical signals NEED temporal anchors
 if not self.REQUIRED_CLINICAL_MARKERS["temporal_specificity"].search(signal_text):
 failures.append("Missing temporal specificity (when did this occur?)")
 
 # Clinical signals often need numbers
 if not self.REQUIRED_CLINICAL_MARKERS["numeric_value"].search(signal_text):
 failures.append("Missing quantitative values (vital signs, measurements)")
 
 # Clinical signals must reference the patient/context
 if not self.REQUIRED_CLINICAL_MARKERS["clinical_context"].search(signal_text):
 failures.append("Missing clinical context (what patient/system?)")
 
 is_valid = len(failures) == 0
 
 self.validation_log.append({
 "timestamp": dt.utcnow().isoformat(),
 "signal_sample": signal_text[:100],
 "is_valid": is_valid,
 "failures": failures,
 })
 
 return is_valid, failures
