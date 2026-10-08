"""
_decider_with

Helper to create a ClaudeGovernanceDecider with a mocked create_fn.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def _decider_with(create_fn):
 d = ClaudeGovernanceDecider(api_key="sk-fake-not-used")
 d.client.messages.create = create_fn
 return d
