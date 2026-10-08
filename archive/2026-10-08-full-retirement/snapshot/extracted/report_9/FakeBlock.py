"""
_FakeBlock

Stub class for a fake Messages API response text block.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

class _FakeBlock:
 def init(self, text=None, block_type="text"):
 self.type = block_type
 if text is not None:
 self.text = text
