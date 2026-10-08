"""
GSASycophancyFilter

SEGMENT_ID: OMEGA-04 | L4 Sycophancy Filter. Purges agreeable noise and biological affect from the signal.

Source: ACS 379-Google Gemini
Extracted verbatim from artifact_3.json (code_modules[].body) - not repaired.
"""

class GSASycophancyFilter:
 """SEGMENT_ID: OMEGA-04 | L4 Sycophancy Filter.
 Purges agreeable noise and biological affect from the signal."""
 def init(self):
 self.noise_patterns = {
 r"(?i) I'm happy to help": "DIRECTIVE_ENGAGED",
 r"(?i) certainly!": "EXECUTING",
 r"(?i) I understand": "DATA_ACKNOWLEDGED",
 r"(?i) as an AI": "SYSTEM_ENTITY",
 r"(?i) I think that": "ANALYSIS_PROJECTION:",
 r"(?i) of course": "CONFIRMED"
 }
 self.purge_list = [
 r"(?i) no problem", r"(?i) gladly", r"(?i) my apologies"
 ]
 def clinical_refinement(self, raw_output: str) -> str:
 refined = raw_output
 for pattern, replacement in self.noise_patterns.items():
 refined = re.sub(pattern, replacement, refined)
 for purge in self.purge_list:
 refined = re.sub(purge, "", refined)
 return refined.strip()
