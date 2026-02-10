"""
gv_entropy_observer.py

Passive entropy observer for detecting low-amplitude,
long-horizon drift that may not trigger primary thresholds.

This observer:
- Does NOT affect dynamics
- Does NOT enforce policy
- Only measures and reports
"""

from dataclasses import dataclass
from collections import deque
import math


@dataclass
class EntropyState:
    window_size: int = 50
    epsilon: float = 1e-9


class GVEntropyObserver:
    def __init__(self, config: EntropyState | None = None):
        self.config = config or EntropyState()
        self.history = deque(maxlen=self.config.window_size)

    def update(self, gv_value: float) -> float:
        """
        Update entropy observer with current GV or strain signal.
        Returns normalized entropy estimate.
        """

        self.history.append(abs(gv_value))

        if len(self.history) < 5:
            return 0.0

        mean = sum(self.history) / len(self.history)
        variance = sum((x - mean) ** 2 for x in self.history) / len(self.history)

        # Shannon-like proxy (continuous)
        entropy = 0.5 * math.log(2 * math.pi * math.e * (variance + self.config.epsilon))

        return max(entropy, 0.0)
