from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Hashable, Iterable

State = Hashable


@dataclass(frozen=True)
class Constraint:
    universe: FrozenSet[State]
    allowed: FrozenSet[State]

    def __init__(
        self,
        universe: Iterable[State],
        allowed: Iterable[State],
    ) -> None:
        universe_set = frozenset(universe)
        allowed_set = frozenset(allowed)

        if not universe_set:
            raise ValueError("universe cannot be empty")

        if not allowed_set.issubset(universe_set):
            raise ValueError(
                "allowed states must belong to the universe"
            )

        object.__setattr__(self, "universe", universe_set)
        object.__setattr__(self, "allowed", allowed_set)

    @property
    def viable(self) -> bool:
        return bool(self.allowed)

    @property
    def capacity(self) -> float:
        return len(self.allowed) / len(self.universe)

    @property
    def pressure(self) -> float:
        return 1.0 - self.capacity


if __name__ == "__main__":
    states = {
        "stable",
        "degraded",
        "recovering",
        "failed",
    }

    system = Constraint(
        states,
        {
            "stable",
            "degraded",
            "recovering",
        },
    )

    print("GV Constraint Mathematics")
    print(f"Viable   : {system.viable}")
    print(f"Capacity : {system.capacity:.3f}")
    print(f"Pressure : {system.pressure:.3f}")
