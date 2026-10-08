"""
_raises

Client stub raising a transport error.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def _raises(exc):
 """Client stub that raises a transport error."""
 def _create(args, kwargs):
 raise exc
 return _create
