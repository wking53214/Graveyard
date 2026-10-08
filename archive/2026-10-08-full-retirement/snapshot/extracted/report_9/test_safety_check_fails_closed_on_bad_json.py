"""
test_safety_check_fails_closed_on_bad_json

Test verifying non-JSON governor output is blocked.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def test_safety_check_fails_closed_on_bad_json():
 print("
[TEST] safety_check: non-JSON governor output -> blocked")
 d = _decider_with(_returns("this is not json at all"))
 decision = d.safety_check("heal_queue", {"queue": "billing_queue"})
 assert decision["safe"] is False, "parse failure must NOT be safe"
 assert decision["governed"] is False
 assert decision["parse_failed"] is True
 print(" PASSED")
 return True
