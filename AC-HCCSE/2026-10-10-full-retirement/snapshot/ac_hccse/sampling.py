"""
Sampling for quality review.

Pulling a random subset of interactions for a human to read is the one part of
this system that checks the rest of it. The original used bare `random.sample`,
which makes a review unreproducible: you cannot re-examine the batch somebody
disputed, and you cannot write a test against it.

This version takes an optional seed. Seeded, the same call returns the same
subset forever, which is what an auditable review needs.
"""

from __future__ import annotations

import random
from typing import List, Optional, Sequence

from .records import InteractionRecord

__all__ = ["DataSampler"]


class DataSampler:
    """Draws a subset of interactions, optionally reproducibly."""

    def __init__(self, seed: Optional[int] = None):
        # A private Random instance, not the module-level one, so seeding here
        # cannot perturb anyone else's random stream.
        self._rng = random.Random(seed)

    def extract_subset(
        self, collection: Sequence[InteractionRecord], sample_size: int = 1
    ) -> List[InteractionRecord]:
        if not collection or sample_size <= 0:
            return []
        return self._rng.sample(list(collection), min(sample_size, len(collection)))
