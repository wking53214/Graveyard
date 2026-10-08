"""
test_safety_check_approves_valid_safe_true

Test verifying valid safe=true is approved and governed.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def test_safety_check_approves_valid_safe_true():
 print("
[TEST] safety_check: valid safe=true -> approved, governed")
 payload = {
 "safe": True, "risk_level": "low", "reasoning": "reversible, in-bounds",
 "recommendations": [], "confidence": 0.9,
 }
 d = _decider_with(_returns(json.dumps(payload)))
 decision = d.safety_check("heal_queue", {"queue": "billing_queue"})
 assert decision["safe"] is True
 assert decision["governed"] is True
 assert decision["parse_failed"] is False
 print(" PASSED")
 return True
