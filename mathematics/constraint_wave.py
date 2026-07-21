"""
Constraint Wave Experiment

Hypothesis
----------
Constraint pressure may behave as a dynamic field whose disturbances
propagate through neighboring states.

This model uses an established discrete damped wave equation.
It tests mathematical coherence, not the existence of a new physical field.
"""

from __future__ import annotations

from math import exp


def gaussian_pulse(
    size: int,
    center: int,
    width: float,
    amplitude: float,
) -> list[float]:
    return [
        amplitude
        * exp(-((index - center) ** 2) / (2.0 * width**2))
        for index in range(size)
    ]


def evolve(
    previous: list[float],
    current: list[float],
    wave_speed: float,
    damping: float,
) -> list[float]:
    if len(previous) != len(current):
        raise ValueError("wave states must have equal length")

    next_state = [0.0] * len(current)

    for index in range(1, len(current) - 1):
        laplacian = (
            current[index - 1]
            - 2.0 * current[index]
            + current[index + 1]
        )

        velocity = current[index] - previous[index]

        next_state[index] = (
            2.0 * current[index]
            - previous[index]
            + wave_speed**2 * laplacian
            - damping * velocity
        )

    return next_state


def wave_energy(
    previous: list[float],
    current: list[float],
    wave_speed: float,
) -> float:
    kinetic = sum(
        (current[index] - previous[index]) ** 2
        for index in range(len(current))
    )

    gradient = sum(
        (current[index + 1] - current[index]) ** 2
        for index in range(len(current) - 1)
    )

    return 0.5 * kinetic + 0.5 * wave_speed**2 * gradient


def render(state: list[float]) -> str:
    symbols = " .:-=+*#%@"
    peak = max(abs(value) for value in state) or 1.0

    output = []

    for value in state:
        normalized = min(1.0, abs(value) / peak)
        symbol_index = round(
            normalized * (len(symbols) - 1)
        )
        output.append(symbols[symbol_index])

    return "".join(output)


def main() -> None:
    size = 81
    center = size // 2
    steps = 32

    wave_speed = 0.65
    damping = 0.035

    initial = gaussian_pulse(
        size=size,
        center=center,
        width=2.5,
        amplitude=0.9,
    )

    previous = initial.copy()
    current = initial.copy()

    initial_energy = None

    left_probe = center - 12
    right_probe = center + 12

    left_max = abs(current[left_probe])
    right_max = abs(current[right_probe])

    print("GV Constraint Wave Experiment")
    print("-----------------------------")
    print()
    print(f"Field size       : {size}")
    print(f"Wave speed       : {wave_speed}")
    print(f"Damping          : {damping}")
    print(f"Initial center   : {center}")
    print()
    print(f"step 00 |{render(current)}|")

    for step in range(1, steps + 1):
        next_state = evolve(
            previous=previous,
            current=current,
            wave_speed=wave_speed,
            damping=damping,
        )

        previous, current = current, next_state

        energy = wave_energy(
            previous=previous,
            current=current,
            wave_speed=wave_speed,
        )

        if initial_energy is None:
            initial_energy = energy

        left_max = max(
            left_max,
            abs(current[left_probe]),
        )

        right_max = max(
            right_max,
            abs(current[right_probe]),
        )

        if step in {4, 8, 12, 16, 20, 24, 28, 32}:
            print(f"step {step:02d} |{render(current)}|")

    final_energy = wave_energy(
        previous=previous,
        current=current,
        wave_speed=wave_speed,
    )

    assert initial_energy is not None
    assert left_max > 0.05
    assert right_max > 0.05
    assert abs(left_max - right_max) < 0.05
    assert final_energy < initial_energy

    print()
    print("PROPAGATION AUDIT")
    print(f"Left probe maximum   : {left_max:.4f}")
    print(f"Right probe maximum  : {right_max:.4f}")
    print(
        "Symmetric propagation: "
        f"{abs(left_max - right_max) < 0.05}"
    )

    print()
    print("ENERGY AUDIT")
    print(f"Initial wave energy  : {initial_energy:.6f}")
    print(f"Final wave energy    : {final_energy:.6f}")
    print(
        "Energy decreased     : "
        f"{final_energy < initial_energy}"
    )

    print()
    print("RESULT:")
    print(
        "A localized constraint-pressure disturbance propagated "
        "symmetrically through neighboring states."
    )
    print(
        "The measured wave energy decreased under damping."
    )

    print()
    print("MATHEMATICAL STATUS:")
    print(
        "This remains an established damped-wave model."
    )
    print(
        "It shows that a dynamic constraint-pressure interpretation "
        "is coherent, not that a new field has been discovered."
    )

    print()
    print("NEXT TEST:")
    print(
        "Let the local constraint level alter propagation speed, "
        "damping, and recovery."
    )


if __name__ == "__main__":
    main()
