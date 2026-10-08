"""
Salvaged from the STRIDE repo (stride-formatted-audited.py) before its
deletion, 2026-08-20. This is NOT CITADEL-related logic - it doesn't belong
merged into citadel.py. Kept separate because it doesn't yet have a
confirmed home in any existing repo (checked: not present in ANVIL,
Conservation_Kernel, GSA-GATEWAY, or sentinel_os's own resilience code as
of this sweep). Flagging that gap rather than guessing a destination.

Everything else in STRIDE (the linguistic gates, the DOIS/anomaly scoring
stack, the GsaUniversalAdapter hash wrapper) was judged not salvageable:
either strictly inferior to CITADEL's own recovered source, uncalibrated
duplicate territory sentinel_os/GSA-815 already cover with real tests, or
in GsaUniversalAdapter's case, actively misrepresenting what it does
(claims cryptographic tamper-evidence via HMAC while never using the hmac
import it declares).

Two pieces held up under scrutiny and are reproduced here verbatim from
the original (renamed only where the original names were STRIDE-specific
branding with no functional meaning):
"""

import hashlib
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Optional


# =====================================================================
# 1. OUTPUT LOOP DETECTION / RETRY LIFECYCLE
# Real, self-contained, working. Detects an LLM repeating itself and
# manages a bounded retry budget before failing closed.
# =====================================================================

@dataclass
class EngineState:
    seen_outputs: Deque[str] = field(default_factory=lambda: deque(maxlen=1000))
    last_output_hash: Optional[str] = None
    last_timestamp: Optional[float] = None
    retry_counter: int = 0


class PipelineStateEngine:
    """Monitors output history to detect generation loops and manage
    a bounded retry lifecycle. Original name kept - it's descriptive,
    not branding."""

    def __init__(self, max_retries: int = 5, max_history: int = 1000):
        self.state = EngineState(seen_outputs=deque(maxlen=max_history))
        self.max_retries = max_retries

    def evaluate_integrity(self, output: str) -> bool:
        if not output or not output.strip():
            return False
        return True

    def check_loop_condition(self, output: str) -> bool:
        return output in self.state.seen_outputs

    def record_state(self, output: str) -> None:
        self.state.seen_outputs.append(output)
        self.state.last_output_hash = self._compute_hash(output)
        self.state.last_timestamp = time.time()

    def check_retry_capacity(self) -> bool:
        return self.state.retry_counter < self.max_retries

    def increment_retry(self) -> None:
        self.state.retry_counter += 1

    def clear_retry_state(self) -> None:
        self.state.retry_counter = 0

    def _compute_hash(self, payload: str) -> str:
        return hashlib.sha256(payload.encode()).hexdigest()

    def process_lifecycle(self, output: str) -> str:
        """Returns one of: BLOCKED_LOOP, RETRY, SYSTEM_ERROR, ACCEPTED."""
        if self.check_loop_condition(output):
            return "BLOCKED_LOOP"
        if not self.evaluate_integrity(output):
            if self.check_retry_capacity():
                self.increment_retry()
                return "RETRY"
            return "SYSTEM_ERROR"
        self.record_state(output)
        self.clear_retry_state()
        return "ACCEPTED"


# =====================================================================
# 2. QUEUE-DEPTH BACKPRESSURE
# Real backpressure (checks actual queue occupancy), unlike the
# decorative "sleep proportional to word count" TrafficGovernor/
# KineticGovernor duplicate found elsewhere in STRIDE, which was NOT
# salvaged - it doesn't measure anything about real system load.
# =====================================================================

def determine_backpressure_delay(
    current_queue_depth: int,
    max_queue_size: int,
    high_watermark: float = 0.85,
) -> float:
    """Returns a delay signal (0.0 = no delay needed) once queue
    occupancy crosses the high-watermark fraction of capacity.
    Caller decides what to do with the signal (sleep, reject, log)."""
    if max_queue_size <= 0:
        raise ValueError("max_queue_size must be positive")
    occupancy = current_queue_depth / max_queue_size
    if occupancy <= high_watermark:
        return 0.0
    # scales 0.0 -> 1.0 as occupancy goes from the watermark to full
    overage = (occupancy - high_watermark) / (1.0 - high_watermark)
    return round(max(0.0, min(overage, 1.0)), 4)


if __name__ == "__main__":
    engine = PipelineStateEngine(max_retries=2)
    print(engine.process_lifecycle("hello"))      # ACCEPTED
    print(engine.process_lifecycle("hello"))       # BLOCKED_LOOP
    print(engine.process_lifecycle(""))            # RETRY
    print(engine.process_lifecycle(""))             # RETRY
    print(engine.process_lifecycle(""))             # SYSTEM_ERROR (budget spent)

    print(determine_backpressure_delay(80, 100))    # 0.0, under watermark
    print(determine_backpressure_delay(95, 100))    # partial delay signal
    print(determine_backpressure_delay(100, 100))   # 1.0, at capacity
