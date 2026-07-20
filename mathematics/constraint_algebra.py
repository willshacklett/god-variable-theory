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

    def _check_universe(self, other: "Constraint") -> None:
        if self.universe != other.universe:
            raise ValueError("constraints must share a universe")

    def merge(self, other: "Constraint") -> "Constraint":
        self._check_universe(other)

        return Constraint(
            self.universe,
            self.allowed & other.allowed,
        )

    def release(self, other: "Constraint") -> "Constraint":
        self._check_universe(other)

        return Constraint(
            self.universe,
            self.allowed | other.allowed,
        )

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

    operational = Constraint(
        states,
        {"stable", "degraded", "recovering"},
    )

    safe = Constraint(
        states,
        {"stable", "recovering"},
    )

    merged = operational.merge(safe)
    released = operational.release(safe)

    print("GV Constraint Mathematics")
    print("Operational:", sorted(operational.allowed))
    print("Safe       :", sorted(safe.allowed))
    print("Merge      :", sorted(merged.allowed))
    print("Release    :", sorted(released.allowed))
