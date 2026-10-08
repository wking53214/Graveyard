"""
DynamicState modifications

Companion diff for Domain/CallerState.py adding required properties.

Source: source: 3
Extracted verbatim from artifact_1.json (code_modules[].body) - not repaired.
"""

@dataclass
class DynamicState:
 perceived_wait: float = 0.0
 frustration: float = 0.0
+ friction_event: int = 0 # adverse navigation events this step (Simulator writes)
+ actual_wait: float = 0.0 # normalized elapsed queue wait this step
+ expected_wait: float = 0.0 # caller's expected wait
+ resolved: bool = False # reached correct agent this step
