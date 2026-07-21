"""
Constraint Memory Persistence and Erasure Audit

Research questions
------------------
1. How long does information remain stored in an adaptive constraint medium?
2. Does ordinary recovery gradually erase stored information?
3. Can a later pulse overwrite an earlier stored bit?
4. Does the final state encode the first bit, the latest bit, or both?

A binary symbol is written through pulse amplitude:

    bit 0 -> low-amplitude pulse
    bit 1 -> high-amplitude pulse

The adaptive medium stores the symbol through a persistent reduction
in local recoverability.

The experiment has two parts:

1. Persistence audit:
   Write one bit, wait for varying durations, then decode the medium.

2. Overwrite audit:
   Write a first bit, wait, write a second bit, then determine whether
   the final medium remembers the first bit or the latest bit.

Information is measured using Shannon mutual information.

This uses established information theory and nonlinear dynamical
systems. It does not establish new mathematics or a new physical field.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log2, sqrt
from random import Random


@dataclass(frozen=True)
class MemoryTrial:
    written_bit: int
    memory_signal: float


@dataclass(frozen=True)
class OverwriteTrial:
    first_bit: int
    second_bit: int
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


def empty_field(
    size: int,
) -> tuple[list[float], list[float]]:
    return [0.0] * size, [0.0] * size


def pulse_amplitude(
    bit: int,
) -> float:
    return 0.86 if bit == 1 else 0.30


def evolve(
    previous: list[float],
    current: list[float],
    recoverability: list[float],
    base_speed: float,
    base_damping: float,
    recovery_rate: float,
) -> tuple[list[float], list[float]]:
    size = len(current)

    next_state = [0.0] * size
    next_recoverability = recoverability.copy()

    for index in range(1, size - 1):
        local_recovery = recoverability[index]

        local_speed = (
            base_speed
            * sqrt(local_recovery)
        )

        local_damping = (
            base_damping
            + 0.18 * (1.0 - local_recovery)
        )

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

        strain = abs(current[index])

        if strain > 0.42:
            damage = (
                0.020
                * (strain - 0.42)
            )

            next_recoverability[index] -= damage

        next_recoverability[index] += (
            recovery_rate
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


def propagate_pulse(
    bit: int,
    recoverability: list[float],
    source: int,
    write_steps: int,
    base_speed: float,
    base_damping: float,
    recovery_rate: float,
) -> list[float]:
    size = len(recoverability)

    previous, current = initial_pulse(
        size=size,
        center=source,
        width=3.2,
        amplitude=pulse_amplitude(bit),
        shift=0.62,
    )

    for _ in range(write_steps):
        next_state, next_recoverability = evolve(
            previous=previous,
            current=current,
            recoverability=recoverability,
            base_speed=base_speed,
            base_damping=base_damping,
            recovery_rate=recovery_rate,
        )

        previous, current = (
            current,
            next_state,
        )

        recoverability = next_recoverability

    return recoverability


def relax_medium(
    recoverability: list[float],
    steps: int,
    base_speed: float,
    base_damping: float,
    recovery_rate: float,
) -> list[float]:
    previous, current = empty_field(
        len(recoverability)
    )

    for _ in range(steps):
        next_state, next_recoverability = evolve(
            previous=previous,
            current=current,
            recoverability=recoverability,
            base_speed=base_speed,
            base_damping=base_damping,
            recovery_rate=recovery_rate,
        )

        previous, current = (
            current,
            next_state,
        )

        recoverability = next_recoverability

    return recoverability


def memory_signal(
    recoverability: list[float],
    source: int,
    radius: int = 6,
) -> float:
    local_window = recoverability[
        source - radius : source + radius + 1
    ]

    return (
        1.0
        - sum(local_window)
        / len(local_window)
    )


def mutual_information(
    pairs: list[tuple[int, int]],
) -> float:
    joint_counts = [
        [0, 0],
        [0, 0],
    ]

    first_counts = [0, 0]
    second_counts = [0, 0]

    for first, second in pairs:
        joint_counts[first][second] += 1
        first_counts[first] += 1
        second_counts[second] += 1

    total = len(pairs)
    information = 0.0

    for first in (0, 1):
        for second in (0, 1):
            count = joint_counts[first][second]

            if count == 0:
                continue

            joint_probability = count / total
            first_probability = (
                first_counts[first] / total
            )
            second_probability = (
                second_counts[second] / total
            )

            information += (
                joint_probability
                * log2(
                    joint_probability
                    / (
                        first_probability
                        * second_probability
                    )
                )
            )

    return information


def accuracy(
    pairs: list[tuple[int, int]],
) -> float:
    return (
        sum(
            first == second
            for first, second in pairs
        )
        / len(pairs)
    )


def calibrated_threshold(
    zero_signals: list[float],
    one_signals: list[float],
) -> float:
    zero_mean = (
        sum(zero_signals)
        / len(zero_signals)
    )

    one_mean = (
        sum(one_signals)
        / len(one_signals)
    )

    return (
        zero_mean + one_mean
    ) / 2.0


def persistence_trials(
    wait_steps: int,
    trial_count: int,
    random_generator: Random,
) -> dict[str, float]:
    size = 181
    source = 38

    write_steps = 115
    base_speed = 0.62
    base_damping = 0.018
    recovery_rate = 0.0025
    measurement_noise = 0.0018

    trials = []

    for index in range(trial_count):
        bit = index % 2
        recoverability = [1.0] * size

        recoverability = propagate_pulse(
            bit=bit,
            recoverability=recoverability,
            source=source,
            write_steps=write_steps,
            base_speed=base_speed,
            base_damping=base_damping,
            recovery_rate=recovery_rate,
        )

        recoverability = relax_medium(
            recoverability=recoverability,
            steps=wait_steps,
            base_speed=base_speed,
            base_damping=base_damping,
            recovery_rate=recovery_rate,
        )

        signal = memory_signal(
            recoverability,
            source,
        )

        signal += random_generator.gauss(
            0.0,
            measurement_noise,
        )

        trials.append(
            MemoryTrial(
                written_bit=bit,
                memory_signal=signal,
            )
        )

    zero_signals = [
        trial.memory_signal
        for trial in trials
        if trial.written_bit == 0
    ]

    one_signals = [
        trial.memory_signal
        for trial in trials
        if trial.written_bit == 1
    ]

    threshold = calibrated_threshold(
        zero_signals,
        one_signals,
    )

    pairs = [
        (
            trial.written_bit,
            int(
                trial.memory_signal
                >= threshold
            ),
        )
        for trial in trials
    ]

    return {
        "zero_mean": (
            sum(zero_signals)
            / len(zero_signals)
        ),
        "one_mean": (
            sum(one_signals)
            / len(one_signals)
        ),
        "threshold": threshold,
        "accuracy": accuracy(pairs),
        "information": mutual_information(pairs),
    }


def overwrite_trials(
    gap_steps: int,
    final_wait_steps: int,
    trial_count: int,
    random_generator: Random,
) -> dict[str, float]:
    size = 181
    source = 38

    write_steps = 115
    base_speed = 0.62
    base_damping = 0.018
    recovery_rate = 0.0025
    measurement_noise = 0.0018

    trials = []

    bit_pairs = [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
    ]

    for index in range(trial_count):
        first_bit, second_bit = bit_pairs[
            index % len(bit_pairs)
        ]

        recoverability = [1.0] * size

        recoverability = propagate_pulse(
            bit=first_bit,
            recoverability=recoverability,
            source=source,
            write_steps=write_steps,
            base_speed=base_speed,
            base_damping=base_damping,
            recovery_rate=recovery_rate,
        )

        recoverability = relax_medium(
            recoverability=recoverability,
            steps=gap_steps,
            base_speed=base_speed,
            base_damping=base_damping,
            recovery_rate=recovery_rate,
        )

        recoverability = propagate_pulse(
            bit=second_bit,
            recoverability=recoverability,
            source=source,
            write_steps=write_steps,
            base_speed=base_speed,
            base_damping=base_damping,
            recovery_rate=recovery_rate,
        )

        recoverability = relax_medium(
            recoverability=recoverability,
            steps=final_wait_steps,
            base_speed=base_speed,
            base_damping=base_damping,
            recovery_rate=recovery_rate,
        )

        signal = memory_signal(
            recoverability,
            source,
        )

        signal += random_generator.gauss(
            0.0,
            measurement_noise,
        )

        trials.append(
            OverwriteTrial(
                first_bit=first_bit,
                second_bit=second_bit,
                memory_signal=signal,
            )
        )

    grouped = {}

    for first_bit, second_bit in bit_pairs:
        signals = [
            trial.memory_signal
            for trial in trials
            if (
                trial.first_bit == first_bit
                and trial.second_bit == second_bit
            )
        ]

        grouped[
            (first_bit, second_bit)
        ] = sum(signals) / len(signals)

    second_zero_signals = [
        trial.memory_signal
        for trial in trials
        if trial.second_bit == 0
    ]

    second_one_signals = [
        trial.memory_signal
        for trial in trials
        if trial.second_bit == 1
    ]

    latest_threshold = calibrated_threshold(
        second_zero_signals,
        second_one_signals,
    )

    latest_pairs = [
        (
            trial.second_bit,
            int(
                trial.memory_signal
                >= latest_threshold
            ),
        )
        for trial in trials
    ]

    first_zero_signals = [
        trial.memory_signal
        for trial in trials
        if trial.first_bit == 0
    ]

    first_one_signals = [
        trial.memory_signal
        for trial in trials
        if trial.first_bit == 1
    ]

    first_threshold = calibrated_threshold(
        first_zero_signals,
        first_one_signals,
    )

    first_pairs = [
        (
            trial.first_bit,
            int(
                trial.memory_signal
                >= first_threshold
            ),
        )
        for trial in trials
    ]

    return {
        "mean_00": grouped[(0, 0)],
        "mean_01": grouped[(0, 1)],
        "mean_10": grouped[(1, 0)],
        "mean_11": grouped[(1, 1)],
        "latest_accuracy": accuracy(
            latest_pairs
        ),
        "latest_information": mutual_information(
            latest_pairs
        ),
        "first_accuracy": accuracy(
            first_pairs
        ),
        "first_information": mutual_information(
            first_pairs
        ),
    }


def print_persistence_report(
    wait_steps: int,
    result: dict[str, float],
) -> None:
    print(
        f"{wait_steps:>5} "
        f"{result['zero_mean']:>12.5f} "
        f"{result['one_mean']:>12.5f} "
        f"{result['accuracy']:>10.3f} "
        f"{result['information']:>12.3f}"
    )


def main() -> None:
    print("GV Constraint Memory Dynamics")
    print("=============================")

    random_generator = Random(90210)

    waiting_periods = [
        0,
        50,
        150,
        300,
        600,
        1000,
    ]

    persistence_results = {}

    print()
    print("PERSISTENCE AUDIT")
    print("-----------------")
    print(
        " wait "
        " bit-0 mean "
        " bit-1 mean "
        " accuracy "
        " information"
    )

    for wait_steps in waiting_periods:
        result = persistence_trials(
            wait_steps=wait_steps,
            trial_count=300,
            random_generator=random_generator,
        )

        persistence_results[
            wait_steps
        ] = result

        print_persistence_report(
            wait_steps,
            result,
        )

    overwrite = overwrite_trials(
        gap_steps=150,
        final_wait_steps=100,
        trial_count=400,
        random_generator=random_generator,
    )

    print()
    print("OVERWRITE AUDIT")
    print("---------------")
    print(
        "Mean final signal after 0 -> 0 : "
        f"{overwrite['mean_00']:.5f}"
    )
    print(
        "Mean final signal after 0 -> 1 : "
        f"{overwrite['mean_01']:.5f}"
    )
    print(
        "Mean final signal after 1 -> 0 : "
        f"{overwrite['mean_10']:.5f}"
    )
    print(
        "Mean final signal after 1 -> 1 : "
        f"{overwrite['mean_11']:.5f}"
    )

    print()
    print(
        "Information about first bit       : "
        f"{overwrite['first_information']:.3f} bits"
    )
    print(
        "Accuracy decoding first bit       : "
        f"{overwrite['first_accuracy']:.3f}"
    )

    print()
    print(
        "Information about latest bit      : "
        f"{overwrite['latest_information']:.3f} bits"
    )
    print(
        "Accuracy decoding latest bit      : "
        f"{overwrite['latest_accuracy']:.3f}"
    )

    initial_information = (
        persistence_results[0]["information"]
    )

    late_information = (
        persistence_results[1000]["information"]
    )

    assert initial_information > 0.90
    assert late_information < initial_information
    assert overwrite["latest_information"] > 0.40

    print()
    print("RESULT")
    print("------")
    print(
        "Stored information decays as recoverability "
        "returns toward its baseline."
    )
    print(
        "A second pulse modifies the existing trace "
        "rather than writing into an empty medium."
    )
    print(
        "The final medium contains measurable information "
        "about the latest input."
    )

    print()
    print("IMPORTANT LIMITATION")
    print("--------------------")
    print(
        "This medium is not yet a clean digital memory cell."
    )
    print(
        "Damage is cumulative, so a low-amplitude pulse cannot "
        "fully restore a state written by a high-amplitude pulse."
    )
    print(
        "True overwrite or erasure would require a reversible "
        "recovery mechanism, not damage alone."
    )

    print()
    print("MATHEMATICAL STATUS")
    print("-------------------")
    print(
        "The experiment uses Shannon information, relaxation "
        "dynamics, hysteresis, and adaptive-medium mathematics."
    )
    print(
        "It does not require new mathematics."
    )

    print()
    print("NEXT QUESTION")
    print("-------------")
    print(
        "Can an opposing constraint operation actively restore "
        "recoverability and create a genuinely rewritable memory?"
    )


if __name__ == "__main__":
    main()
