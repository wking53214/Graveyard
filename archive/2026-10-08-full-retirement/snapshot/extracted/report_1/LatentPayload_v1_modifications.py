"""
LatentPayload v1 modifications

Blue design v1 diff against Latent/LatentPayload.py adding event-driven thresholds and updating to_dict and update_after_step.

Source: source: 3
Extracted verbatim from artifact_1.json (code_modules[].body) - not repaired.
"""

@@ Fields @@
 baseline_frustration: float = 0.1
 escalation_rate: float = 0.05
 menu_compliance: float = 0.7
 navigation_depth_prior: float = 0.4
 fraud_risk: float = 0.1
+ friction_count: int = 0 # running count of adverse events (fork-1 threshold state)
+
+ # deterministic tunables (integer threshold => float-boundary-safe)
+ _TOLERANCE: int = 1
+ _FRICTION_CAP: int = 20
+ _DILATION_K: float = 0.5
+ RELIEF_RATE: float = 0.1

@@ to_dict @@
- return asdict(self)
+ d = asdict(self)
+ return {k: v for k, v in d.items() if not k.startswith("")} # keep constants out of the hash surface

@@ update_after_step @@
- # 1. Frustration update
- caller_dynamic.frustration += self.escalation_rate * (1.0 - self.patience)
- # 2. Trust decay governed by current frustration
- self.trust_scalar = self._clamp(self.trust_scalar - 0.01 * caller_dynamic.frustration)
- # 3. Volatility increase governed by impatience
- self.volatility = self._clamp(self.volatility + 0.005 * (1.0 - self.patience))
- # 4. Memory accumulation
- self.memory_flag = self._clamp(self.memory_flag + 0.01)
+ # read event signals DEFENSIVELY (a bare frustration-only dynamic still works)
+ event = int(getattr(caller_dynamic, "friction_event", 0))
+ actual = float(getattr(caller_dynamic, "actual_wait", 0.0))
+ expected = float(getattr(caller_dynamic, "expected_wait", 0.0))
+ frust_in = float(getattr(caller_dynamic, "frustration", 0.0))
+ resolved = bool(getattr(caller_dynamic, "resolved", False))
+
+ wait_overrun = 1 if actual > expected else 0
+ friction_this_step = event + wait_overrun # integer
+ self.friction_count = min(self.friction_count + friction_this_step, self._FRICTION_CAP)
+ over_tol = max(0, self.friction_count - self._TOLERANCE) # integer, no float boundary
+
+ if friction_this_step > 0:
+ # FORK 1: convex accrual past tolerance; drift ONLY on friction steps
+ d_frust = self.escalation_rate * (1.0 + over_tol) * (1.0 - self.patience)
+ caller_dynamic.frustration = frust_in + d_frust
+ self.trust_scalar = self._clamp(self.trust_scalar - 0.01 * caller_dynamic.frustration)
+ self.volatility = self._clamp(self.volatility + 0.005 * (1.0 + over_tol) * (1.0 - self.patience))
+ self.memory_flag = self._clamp(self.memory_flag + 0.01 * (1.0 + over_tol))
+ elif resolved:
+ # relief: frustration decays toward 0, trust recovers, volatility relaxes, memory PERSISTS
+ caller_dynamic.frustration = max(0.0, frust_in - self._RELIEF_RATE)
+ self.trust_scalar = self._clamp(self.trust_scalar + self._RELIEF_RATE * (1.0 - self.trust_scalar))
+ self.volatility = self._clamp(self.volatility - self._RELIEF_RATE * self.volatility)
+ # else: quiet non-resolved step -> nothing moves -> no saturation
+
+ # FORK 2: frustration distorts perceived_wait; WRITE the previously-dead field
+ caller_dynamic.perceived_wait = self._clamp(actual * (1.0 + self._DILATION_K * caller_dynamic.frustration))
