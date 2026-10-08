"""
test_safety_check_fails_closed_on_empty_content

Test verifying empty/unintelligible response is blocked.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def test_safety_check_fails_closed_on_empty_content():
 print("
[TEST] safety_check: empty/unintelligible response -> blocked")
 d = _decider_with(_returns_empty())
 decision = d.safety_check("heal_queue", {"queue": "billing_queue"})
 assert decision["safe"] is False
 assert decision["governed"] is False
 print(" PASSED")
 return True
