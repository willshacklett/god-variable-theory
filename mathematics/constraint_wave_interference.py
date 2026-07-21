"""
Constraint Wave Interference Experiment

Research question
-----------------
When two constraint-pressure waves collide, do they merely superimpose,
or can their overlap alter the recoverability of the medium?

Two models are compared:

1. Passive medium:
   Standard damped-wave propagation.

2. Adaptive medium:
   Strong local strain reduces recoverability. Reduced recoverability
   lowers propagation speed and increases damping.

This uses established nonlinear wave and adaptive-medium mathematics.
It does not establish a new field or new mathematics.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, sqrt


@dataclass(frozen=True)
class RunResult:
    collision_peak: float
    final_energy: float
    minimum_recoverability: float
    final_recoverability: float
    left_probe_peak: float
    right_probe_peak: float


def gaussian(
    size: int,
    center: float,
    width: float,
    amplitude: float,
) -> list[float]:
    return [
        amplitude
        * exp(-((index - center) ** 2) / (2.0 * width**2))
        for index in range(size)
    ]


def combine(
    first: list[float],
    second: list[float],
) -> list[float]:
    return [
        a + b
        for a, b in zip(first, second)
    ]


def initial_states(
    size: int,
    left_center: int,
    right_center: int,
    width: float,
    amplitude: float,
    shift: float,
) -> tuple[list[float], list[float]]:
    current = combine(
        gaussian(size, left_center, width, amplitude),
        gaussian(size, right_center, width, amplitude),
    )

    previous = combine(
        gaussian(
            size,
            left_center - shift,
            width,
            amplitude,
        ),
        gaussian(
            size,
            right_center + shift,
            width,
            amplitude,
        ),
    )

    return previous, current


def wave_energy(
    previous: list[float],
    current: list[float],
    base_speed: float,
) -> float:
    kinetic = sum(
        (current[i] - previous[i]) ** 2
        for i in range(len(current))
    )

    gradient = sum(
        (current[i + 1] - current[i]) ** 2
        for i in range(len(current) - 1)
    )

    return (
        0.5 * kinetic
        + 0.5 * base_speed**2 * gradient
    )


def evolve(
    previous: list[float],
    current: list[float],
    recoverability: list[float],
    base_speed: float,
    base_damping: float,
    adaptive: bool,
) -> tuple[list[float], list[float]]:
    size = len(current)
    next_state = [0.0] * size
    next_recoverability = recoverability.copy()

    for i in range(1, size - 1):
        local_recovery = recoverability[i]

        if adaptive:
            local_speed = (
                base_speed * sqrt(local_recovery)
            )

            local_damping = (
                base_damping
                + 0.18 * (1.0 - local_recovery)
            )
        else:
            local_speed = base_speed
            local_damping = base_damping

        laplacian = (
            current[i - 1]
            - 2.0 * current[i]
            + current[i + 1]
        )

        velocity = current[i] - previous[i]

        next_state[i] = (
            2.0 * current[i]
            - previous[i]
            + local_speed**2 * laplacian
            - local_damping * velocity
        )

        if adaptive:
            strain = abs(current[i])

            if strain > 0.72:
                damage = 0.045 * (strain - 0.72)
                next_recoverability[i] -= damage

            recovery = (
                0.006
                * (1.0 - next_recoverability[i])
            )

            next_recoverability[i] += recovery
            next_recoverability[i] = max(
                0.35,
                min(1.0, next_recoverability[i]),
            )

    return next_state, next_recoverability


def render(
    field: list[float],
    recoverability: list[float],
) -> str:
    symbols = " .:-=+*#%@"
    peak = max(abs(value) for value in field) or 1.0
    output = []

    for value, recovery in zip(field, recoverability):
        magnitude = abs(value) / peak
        weighted = magnitude * recovery

        index = round(
            min(1.0, weighted)
            * (len(symbols) - 1)
        )

        output.append(symbols[index])

    return "".join(output)


def run(adaptive: bool) -> RunResult:
    size = 121
    center = size // 2
    steps = 92

    base_speed = 0.62
    base_damping = 0.018

    previous, current = initial_states(
        size=size,
        left_center=32,
        right_center=88,
        width=3.2,
        amplitude=0.72,
        shift=0.62,
    )

    recoverability = [1.0] * size

    collision_peak = 0.0
    left_probe_peak = 0.0
    right_probe_peak = 0.0
    minimum_recoverability = 1.0

    left_probe = center - 22
    right_probe = center + 22

    label = "ADAPTIVE" if adaptive else "PASSIVE"

    print()
    print(f"{label} MEDIUM")
    print("-" * (len(label) + 7))

    for step in range(steps + 1):
        collision_peak = max(
            collision_peak,
            abs(current[center]),
        )

        left_probe_peak = max(
            left_probe_peak,
            abs(current[left_probe]),
        )

        right_probe_peak = max(
            right_probe_peak,
            abs(current[right_probe]),
        )

        minimum_recoverability = min(
            minimum_recoverability,
            min(recoverability),
        )

        if step in {0, 16, 32, 44, 56, 72, 92}:
            print(
                f"step {step:02d} "
                f"|{render(current, recoverability)}|"
            )

        if step == steps:
            break

        next_state, next_recoverability = evolve(
            previous=previous,
            current=current,
            recoverability=recoverability,
            base_speed=base_speed,
            base_damping=base_damping,
            adaptive=adaptive,
        )

        previous, current = current, next_state
        recoverability = next_recoverability

    return RunResult(
        collision_peak=collision_peak,
        final_energy=wave_energy(
            previous,
            current,
            base_speed,
        ),
        minimum_recoverability=minimum_recoverability,
        final_recoverability=min(recoverability),
        left_probe_peak=left_probe_peak,
        right_probe_peak=right_probe_peak,
    )


def main() -> None:
    print("GV Constraint-Wave Interference")
    print("===============================")

    passive = run(adaptive=False)
    adaptive = run(adaptive=True)

    assert passive.minimum_recoverability == 1.0
    assert adaptive.minimum_recoverability < 1.0
    assert adaptive.final_energy < passive.final_energy

    print()
    print("COMPARISON")
    print("----------")
    print(
        f"Passive collision peak       : "
        f"{passive.collision_peak:.4f}"
    )
    print(
        f"Adaptive collision peak      : "
        f"{adaptive.collision_peak:.4f}"
    )
    print()
    print(
        f"Passive final energy         : "
        f"{passive.final_energy:.6f}"
    )
    print(
        f"Adaptive final energy        : "
        f"{adaptive.final_energy:.6f}"
    )
    print()
    print(
        f"Passive minimum recovery     : "
        f"{passive.minimum_recoverability:.4f}"
    )
    print(
        f"Adaptive minimum recovery    : "
        f"{adaptive.minimum_recoverability:.4f}"
    )
    print(
        f"Adaptive final recovery      : "
        f"{adaptive.final_recoverability:.4f}"
    )
    print()

    print("RESULT:")
    print(
        "In the passive model, the waves interfered without "
        "changing the medium."
    )
    print(
        "In the adaptive model, collision strain reduced local "
        "recoverability and altered later propagation."
    )
    print()

    print("MATHEMATICAL STATUS:")
    print(
        "This is a nonlinear adaptive-medium model built with "
        "existing mathematics."
    )
    print(
        "The distinctive GV hypothesis is not wave interference "
        "itself, but constraint-dependent modification of the "
        "rules governing future propagation."
    )
    print()

    print("NEXT QUESTION:")
    print(
        "Can the recoverability rule be derived from a conservation "
        "or optimization principle instead of being inserted by hand?"
    )


if __name__ == "__main__":
    main()
