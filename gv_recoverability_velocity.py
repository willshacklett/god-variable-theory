"""
gv_recoverability_velocity.py

Tracks the rate of change of recoverability over time.
This detects erosion of recovery capacity before collapse.

Observer only — no policy, no enforcement.
"""

from collections import deque
from dataclasses import dataclass


@dataclass
class RecoverabilityVelocityConfig:
    window: int = 10
    min_points: int = 3


class GVRecoverabilityVelocity:
    def __init__(self, config: RecoverabilityVelocityConfig | None = None):
        self.config = config or RecoverabilityVelocityConfig()
        self.history = deque(maxlen=self.config.window)

    def update(self, recoverability: float) -> float:
        """
        Returns average delta recoverability per step.
        Negative values indicate loss of recovery capacity.
        """

        self.history.append(recoverability)

        if len(self.history) < self.config.min_points:
            return 0.0

        deltas = [
            self.history[i] - self.history[i - 1]
            for i in range(1, len(self.history))
        ]

        return sum(deltas) / len(deltas)
