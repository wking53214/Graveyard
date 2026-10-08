"""
_low_friction_journey

Returns a mock IcebergJourney not requiring governance.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def _low_friction_journey():
 return IcebergJourney(
 caller_id="twilio_LOW",
 timestamp=0,
 journey=["root", "intent_menu", "billing_queue", "agent_a", "exit"],
 wait_times={"intent_menu": 5.0, "queue": 10.0, "agent": 5.0},
 total_duration=60.0,
 resolved=True,
 friction_count=0, # <= 2 -> governance NOT required
 abandonment_reason=None,
 )
