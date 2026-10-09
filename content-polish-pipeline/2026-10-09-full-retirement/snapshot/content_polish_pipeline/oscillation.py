"""
Oscillation detector: identifies repeated normalized generator outputs.

Tracks a bounded history of normalized outputs and signals when an exact
normalized recurrence is observed. Used as a non-authoritative diagnostic
signal in the validation pipeline.

This detector is deterministic, cheap, local, and has no governance authority.
It reports but does not execute governance actions.
"""

from collections import deque


class OscillationDetector:
    """
    Detect repeated normalized outputs within a bounded history.

    This detector maintains a sliding window of observed normalized outputs.
    When a repeated output is observed, it signals oscillation detected.

    Args:
        max_history: Maximum number of normalized outputs to retain in history.
            Default 32. Once the limit is reached, the oldest observation
            is discarded when a new one is added.

    Attributes:
        history: Deque of observed normalized outputs (newest at right).
    """

    def __init__(self, max_history: int = 32):
        """Initialize the detector with a bounded history."""
        if max_history < 1:
            raise ValueError(f"max_history must be >= 1, got {max_history}")
        self.history = deque(maxlen=max_history)

    def observe(self, text: str) -> bool:
        """
        Observe a text output and check if it repeats earlier history.

        Normalizes the text (strip whitespace, lowercase) before comparison.
        The normalized form is added to the history after the check.

        Args:
            text: Raw output text to observe.

        Returns:
            True if the normalized text was already in history (oscillation
            detected). False if it is a new observation.

        Example:
            >>> detector = OscillationDetector()
            >>> detector.observe("Candidate accepted")  # False (first time)
            False
            >>> detector.observe("Candidate accepted")  # True (seen before)
            True
            >>> detector.observe(" CANDIDATE ACCEPTED ")  # True (normalized)
            True
        """
        normalized = text.strip().lower()
        repeated = normalized in self.history
        self.history.append(normalized)
        return repeated

    def reset(self):
        """Clear all history. Use to start a new observation session."""
        self.history.clear()

    def get_history(self) -> list[str]:
        """Return a snapshot of current history (newest at end)."""
        return list(self.history)
