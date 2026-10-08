"""
test_safety_check_fails_closed_on_nonbool_safe

Test verifying 'safe' not being a bool is blocked.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def test_safety_check_fails_closed_on_nonbool_safe():
 print("
[TEST] safety_check: 'safe' not a bool -> blocked (Gate 1)")
 d = _decider_with(_returns(json.dumps({"safe": "yes", "reasoning": "x"})))
 decision = d.safety_check("heal_queue", {"queue": "billing_queue"})
 assert decision["safe"] is False, "non-bool 'safe' is unintelligible for a gate"
 assert decision["governed"] is False
 print(" PASSED")
 return True
