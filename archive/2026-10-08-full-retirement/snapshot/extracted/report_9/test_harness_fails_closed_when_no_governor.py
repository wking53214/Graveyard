"""
test_harness_fails_closed_when_no_governor

Test verifying harness blocks when no governor is present but governance is required.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def test_harness_fails_closed_when_no_governor():
 print("
[TEST] harness: governance required but no governor -> blocked")
 h = _harness()
 assert h.claude_decider is None, "no api key -> no decider"
 h.twilio_parser.parse_call_log = lambda rec: _high_friction_journey()
 result = h.process_call({"sid": "CATEST01", "status": "completed",
 "duration": 350, "from": "+1111", "to": "+billing"})
 assert result["governance_required"] is True
 assert result["governance_approved"] is False
 assert result["governance_blocked"] is True, "must NOT run ungoverned + report success"
 # the call is still observed/scored -- fail-closed withholds the ACTION,
 # it does not abort the pipeline.
 assert result["caller_id"] == "twilio_TEST"
 assert result["quality"] is not None
 print(" PASSED")
 return True
