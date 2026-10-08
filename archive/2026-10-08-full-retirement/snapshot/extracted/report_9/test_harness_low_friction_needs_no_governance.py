"""
test_harness_low_friction_needs_no_governance

Test verifying harness does not block on low friction.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def test_harness_low_friction_needs_no_governance():
 print("
[TEST] harness: low friction -> governance not required, not blocked")
 h = _harness()
 h.twilio_parser.parse_call_log = lambda rec: _low_friction_journey()
 result = h.process_call({"sid": "CATEST04", "status": "completed",
 "duration": 60, "from": "+1111", "to": "+billing"})
 assert result["governance_required"] is False
 assert result["governance_blocked"] is False
 assert result["claude_safe"] is None
 print(" PASSED")
 return True
