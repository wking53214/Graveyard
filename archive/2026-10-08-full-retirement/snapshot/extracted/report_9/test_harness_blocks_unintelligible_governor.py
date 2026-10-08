"""
test_harness_blocks_unintelligible_governor

Test verifying harness blocks unintelligible governor returns.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def test_harness_blocks_unintelligible_governor():
 print("
[TEST] harness: governor returns garbage -> blocked (Gate 2)")
 h = _harness()
 h.claude_decider = _decider_with(_returns("garbage not json"))
 h.twilio_parser.parse_call_log = lambda rec: _high_friction_journey()
 result = h.process_call({"sid": "CATEST02", "status": "completed",
 "duration": 350, "from": "+1111", "to": "+billing"})
 assert result["governance_approved"] is False
 assert result["governance_blocked"] is True
 assert result["claude_safe"] is False
 print(" PASSED")
 return True
