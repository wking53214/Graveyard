"""
test_harness_approves_valid_safe_decision

Test verifying harness approves valid safe decision.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def test_harness_approves_valid_safe_decision():
 print("
[TEST] harness: valid safe=true -> approved, not blocked")
 payload = {
 "safe": True, "risk_level": "low", "reasoning": "ok",
 "recommendations": [], "confidence": 0.9,
 }
 h = _harness()
 h.claude_decider = _decider_with(_returns(json.dumps(payload)))
 h.twilio_parser.parse_call_log = lambda rec: _high_friction_journey()
 result = h.process_call({"sid": "CATEST03", "status": "completed",
 "duration": 350, "from": "+1111", "to": "+billing"})
 assert result["governance_approved"] is True
 assert result["governance_blocked"] is False
 assert result["claude_safe"] is True
 print(" PASSED")
 return True
