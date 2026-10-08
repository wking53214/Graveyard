"""
LatentPayload v2 modifications

Blue design v2 diff showing changes from v1 only, adding step_index for hash integrity.

Source: source: 3
Extracted verbatim from artifact_1.json (code_modules[].body) - not repaired.
"""

@@ Fields @@
 friction_count: int = 0
+ step_index: int = 0 # monotone step counter -> hash changes every call, non-saturating

@@ update_after_step, first line of body @@
 resolved = bool(getattr(caller_dynamic, "resolved", False))
+ self.step_index += 1 # a step genuinely elapsed: real state change, unbounded int, encoders never read it
