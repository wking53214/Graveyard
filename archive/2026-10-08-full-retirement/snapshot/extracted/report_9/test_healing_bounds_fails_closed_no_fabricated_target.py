"""
test_healing_bounds_fails_closed_no_fabricated_target

Test verifying decide_healing_bounds fails closed.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def test_healing_bounds_fails_closed_no_fabricated_target():
 print("
[TEST] decide_healing_bounds: garbage -> should_heal False, no target")
 d = _decider_with(_returns("nope"))
 decision = d.decide_healing_bounds("billing_queue", 100.0, 50.0, 1.0)
 assert decision["should_heal"] is False, "was fail-OPEN (True) before the fix"
 assert decision["target_wait"] is None, "must not fabricate a heal target"
 assert decision["governed"] is False
 print(" PASSED")
 return True
