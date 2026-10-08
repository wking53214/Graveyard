"""
_returns

Client stub returning one text block.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def _returns(text):
 """Client stub that returns one text block containing text."""
 def _create(*args, kwargs):
 return _FakeMessage([_FakeBlock(text=text)])
 return _create
