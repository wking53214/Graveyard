"""
_high_friction_journey

Returns a mock IcebergJourney requiring governance.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def _high_friction_journey():
 return IcebergJourney(
 caller_id="twilio_TEST",
 timestamp=0,
 journey=["root", "intent_menu", "billing_queue", "agent_a", "exit"],
 wait_times={"intent_menu": 10.0, "queue": 60.0, "agent": 40.0},
 total_duration=350.0,
 resolved=True,
 friction_count=5, # > 2 -> governance REQUIRED
 abandonment_reason=None,
 )
