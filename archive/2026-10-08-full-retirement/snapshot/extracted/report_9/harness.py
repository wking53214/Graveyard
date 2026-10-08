"""
_harness

Returns a mocked IcebergProductionHarness instance.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def _harness():
 return IcebergProductionHarness(
 {"postgres_host": None, "claude_api_key": None, "twilio_account_sid": None}
 )
