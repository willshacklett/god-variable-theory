"""
Constraint-path experiment.

Question:
Can two systems have the same present pressure and the same total historical
pressure, yet different recoverability because the order of exposure differs?

This experiment uses an ordinary nonlinear dynamical system. It is not
presented as new mathematics.
"""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class PathResult:
    history: tuple[float, ...]
    total_pressure: float
    current_pressure: float
    damage: float
    recoverability: float


def simulate_path(
    history: Iterable[float],
    damage_rate: float = 0.55,
    recovery_rate: float = 0.25,
) -> PathResult:
    path = tuple(history)

    if not path:
        raise ValueError("history cannot be empty")

    if any(not 0.0 <= pressure <= 1.0 for pressure in path):
        raise ValueError("pressure values must be between 0 and 1")

    damage = 0.0

    for pressure in path:
        damage_gain = damage_rate * pressure * (1.0 - damage)
        damage += damage_gain

        recovery = recovery_rate * (1.0 - pressure) * damage
        damage = max(0.0, damage - recovery)

    return PathResult(
        history=path,
        total_pressure=sum(path),
        current_pressure=path[-1],
        damage=damage,
        recoverability=1.0 - damage,
    )


def main() -> None:
    early_shock = (
        0.9,
        0.7,
        0.2,
        0.1,
        0.0,
        0.0,
    )

    late_shock = (
        0.1,
        0.0,
        0.2,
        0.9,
        0.7,
        0.0,
    )

    early = simulate_path(early_shock)
    late = simulate_path(late_shock)

    assert early.total_pressure == late.total_pressure
    assert early.current_pressure == late.current_pressure
    assert early.damage != late.damage

    print("GV Path-Dependence Experiment")
    print("-----------------------------")
    print(f"Early-shock path       : {early.history}")
    print(f"Late-shock path        : {late.history}")
    print()
    print(f"Equal total pressure   : {early.total_pressure:.3f}")
    print(f"Equal current pressure : {early.current_pressure:.3f}")
    print()
    print(f"Early-shock damage     : {early.damage:.3f}")
    print(f"Late-shock damage      : {late.damage:.3f}")
    print()
    print(f"Early recoverability   : {early.recoverability:.3f}")
    print(f"Late recoverability    : {late.recoverability:.3f}")
    print()
    print("VERDICT:")
    print("Present pressure and total exposure are insufficient.")
    print("The ordering of constraint exposure changes the outcome.")
    print()
    print("MATHEMATICAL STATUS:")
    print("This is path dependence in an ordinary dynamical system.")
    print("It does not yet require new mathematics.")


if __name__ == "__main__":
    main()
