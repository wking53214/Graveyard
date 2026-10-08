"""
test_safety_check_fails_closed_on_transport_error

Test verifying client raise is blocked.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def test_safety_check_fails_closed_on_transport_error():
 print("
[TEST] safety_check: client raises -> blocked, error captured")
 d = _decider_with(_raises(RuntimeError("boom")))
 decision = d.safety_check("heal_queue", {"queue": "billing_queue"})
 assert decision["safe"] is False
 assert "transport_error" in decision["reasoning"]
 print(" PASSED")
 return True
