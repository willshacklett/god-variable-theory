"""
Constraint Information Audit

Research questions
------------------
1. Can a constraint wave transmit measurable information?
2. Can an adaptive constraint medium retain measurable information
   after the wave has passed?

A binary symbol is encoded in pulse amplitude:

    bit 0 -> low-amplitude pulse
    bit 1 -> high-amplitude pulse

Information is measured using Shannon mutual information.

Two media are compared:

1. Passive medium:
   The pulse propagates, but the medium does not change.

2. Adaptive medium:
   Strong strain reduces recoverability, leaving a persistent trace.

This uses established information theory and nonlinear dynamics.
It does not establish new mathematics or a new physical field.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log2, sqrt
from random import Random


@dataclass(frozen=True)
class Trial:
    sent: int
    received_wave: int
    received_memory: int
    wave_signal: float
    memory_signal: float


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


def initial_pulse(
    size: int,
    center: int,
    width: float,
    amplitude: float,
    shift: float,
) -> tuple[list[float], list[float]]:
    current = gaussian(
        size=size,
        center=center,
        width=width,
        amplitude=amplitude,
    )

    previous = gaussian(
        size=size,
        center=center - shift,
        width=width,
        amplitude=amplitude,
    )

    return previous, current


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

    for index in range(1, size - 1):
        local_recovery = recoverability[index]

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
            current[index - 1]
            - 2.0 * current[index]
            + current[index + 1]
        )

        velocity = (
            current[index]
            - previous[index]
        )

        next_state[index] = (
            2.0 * current[index]
            - previous[index]
            + local_speed**2 * laplacian
            - local_damping * velocity
        )

        if adaptive:
            strain = abs(current[index])

            damage = 0.0

            if strain > 0.42:
                damage = (
                    0.020
                    * (strain - 0.42)
                )

            next_recoverability[index] -= damage

            next_recoverability[index] += (
                0.0025
                * (1.0 - next_recoverability[index])
            )

            next_recoverability[index] = max(
                0.35,
                min(
                    1.0,
                    next_recoverability[index],
                ),
            )

    return next_state, next_recoverability


def mutual_information(
    pairs: list[tuple[int, int]],
) -> float:
    joint_counts = [
        [0, 0],
        [0, 0],
    ]

    sent_counts = [0, 0]
    received_counts = [0, 0]

    for sent, received in pairs:
        joint_counts[sent][received] += 1
        sent_counts[sent] += 1
        received_counts[received] += 1

    total = len(pairs)
    information = 0.0

    for sent in (0, 1):
        for received in (0, 1):
            count = joint_counts[sent][received]

            if count == 0:
                continue

            joint_probability = count / total
            sent_probability = (
                sent_counts[sent] / total
            )
            received_probability = (
                received_counts[received] / total
            )

            information += (
                joint_probability
                * log2(
                    joint_probability
                    / (
                        sent_probability
                        * received_probability
                    )
                )
            )

    return information


def accuracy(
    pairs: list[tuple[int, int]],
) -> float:
    correct = sum(
        sent == received
        for sent, received in pairs
    )

    return correct / len(pairs)


def run_trial(
    bit: int,
    adaptive: bool,
    noise: float,
    random_generator: Random,
) -> Trial:
    size = 161
    source = 30
    receiver = 128
    steps = 190

    amplitude = (
        0.86
        if bit == 1
        else 0.30
    )

    previous, current = initial_pulse(
        size=size,
        center=source,
        width=3.2,
        amplitude=amplitude,
        shift=0.62,
    )

    recoverability = [1.0] * size

    wave_signal = 0.0

    for step in range(steps):
        if 105 <= step <= 175:
            wave_signal = max(
                wave_signal,
                abs(current[receiver]),
            )

        (
            next_state,
            next_recoverability,
        ) = evolve(
            previous=previous,
            current=current,
            recoverability=recoverability,
            base_speed=0.62,
            base_damping=0.018,
            adaptive=adaptive,
        )

        previous, current = (
            current,
            next_state,
        )

        recoverability = next_recoverability

    wave_signal += random_generator.gauss(
        0.0,
        noise,
    )

    memory_window = recoverability[
        source - 6 : source + 7
    ]

    memory_signal = (
        1.0
        - sum(memory_window)
        / len(memory_window)
    )

    memory_signal += random_generator.gauss(
        0.0,
        noise * 0.18,
    )

    received_wave = int(
        wave_signal >= 0.16
    )

    received_memory = int(
        memory_signal >= 0.010
    )

    return Trial(
        sent=bit,
        received_wave=received_wave,
        received_memory=received_memory,
        wave_signal=wave_signal,
        memory_signal=memory_signal,
    )


def run_channel(
    adaptive: bool,
    trials: int = 400,
    noise: float = 0.018,
) -> dict[str, float]:
    seed = (
        7321
        if adaptive
        else 1732
    )

    random_generator = Random(seed)
    results = []

    for index in range(trials):
        bit = index % 2

        results.append(
            run_trial(
                bit=bit,
                adaptive=adaptive,
                noise=noise,
                random_generator=random_generator,
            )
        )

    wave_pairs = [
        (
            trial.sent,
            trial.received_wave,
        )
        for trial in results
    ]

    memory_pairs = [
        (
            trial.sent,
            trial.received_memory,
        )
        for trial in results
    ]

    bit_zero_results = [
        trial
        for trial in results
        if trial.sent == 0
    ]

    bit_one_results = [
        trial
        for trial in results
        if trial.sent == 1
    ]

    return {
        "wave_accuracy": accuracy(
            wave_pairs
        ),
        "wave_information": mutual_information(
            wave_pairs
        ),
        "memory_accuracy": accuracy(
            memory_pairs
        ),
        "memory_information": mutual_information(
            memory_pairs
        ),
        "zero_wave_mean": sum(
            trial.wave_signal
            for trial in bit_zero_results
        )
        / len(bit_zero_results),
        "one_wave_mean": sum(
            trial.wave_signal
            for trial in bit_one_results
        )
        / len(bit_one_results),
        "zero_memory_mean": sum(
            trial.memory_signal
            for trial in bit_zero_results
        )
        / len(bit_zero_results),
        "one_memory_mean": sum(
            trial.memory_signal
            for trial in bit_one_results
        )
        / len(bit_one_results),
    }


def print_report(
    label: str,
    result: dict[str, float],
) -> None:
    print()
    print(label)
    print("-" * len(label))

    print(
        "Wave signal, bit 0 mean     : "
        f"{result['zero_wave_mean']:.5f}"
    )

    print(
        "Wave signal, bit 1 mean     : "
        f"{result['one_wave_mean']:.5f}"
    )

    print(
        "Wave decoding accuracy      : "
        f"{result['wave_accuracy']:.3f}"
    )

    print(
        "Wave mutual information     : "
        f"{result['wave_information']:.3f} bits"
    )

    print()

    print(
        "Memory signal, bit 0 mean   : "
        f"{result['zero_memory_mean']:.5f}"
    )

    print(
        "Memory signal, bit 1 mean   : "
        f"{result['one_memory_mean']:.5f}"
    )

    print(
        "Memory decoding accuracy    : "
        f"{result['memory_accuracy']:.3f}"
    )

    print(
        "Memory mutual information   : "
        f"{result['memory_information']:.3f} bits"
    )


def main() -> None:
    print("GV Constraint Information Audit")
    print("===============================")
    print("Input entropy                  : 1.000 bit")

    passive = run_channel(
        adaptive=False
    )

    adaptive = run_channel(
        adaptive=True
    )

    print_report(
        "PASSIVE MEDIUM",
        passive,
    )

    print_report(
        "ADAPTIVE MEDIUM",
        adaptive,
    )

    assert (
        passive["wave_information"]
        > 0.70
    )

    assert (
        adaptive["wave_information"]
        > 0.70
    )

    assert (
        passive["memory_information"]
        < 0.05
    )

    assert (
        adaptive["memory_information"]
        > 0.40
    )

    print()
    print("RESULT")
    print("------")

    print(
        "Both media transmit information "
        "in the propagating wave."
    )

    print(
        "Only the adaptive medium retains "
        "decodable information after passage."
    )

    print()
    print("INTERPRETATION")
    print("--------------")

    print(
        "The wave carries information through "
        "distinguishable state differences."
    )

    print(
        "The adaptive medium stores information "
        "through persistent recovery changes."
    )

    print()
    print("MATHEMATICAL STATUS")
    print("-------------------")

    print(
        "This result uses Shannon information "
        "and nonlinear dynamical systems."
    )

    print(
        "It does not require new mathematics."
    )

    print()
    print("NEXT QUESTION")
    print("-------------")

    print(
        "How long does the stored information "
        "survive, and what erases it?"
    )


if __name__ == "__main__":
    main()
