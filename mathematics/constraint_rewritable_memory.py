"""
Constraint Rewritable Memory Audit

Research question
-----------------
Can opposing constraint operations create a genuinely rewritable memory?

The medium has a recoverability state R:

    R = 1.0      unconstrained / logical 0
    R < 1.0      constrained / logical 1

Two signed wave operations are introduced:

    WRITE pulse  -> lowers recoverability
    ERASE pulse  -> restores recoverability

The experiment tests:

    initial 0
    write   1
    erase   0
    rewrite 1

It also measures whether each stage remains decodable under noise.

This uses ordinary adaptive-medium dynamics, relaxation,
threshold decoding, and Shannon information theory.
It does not establish new mathematics or a new physical field.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log2, sqrt
from random import Random


@dataclass(frozen=True)
class Trial:
    expected: int
    signal: float


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
    amplitude: float,
    shift: float = 0.62,
) -> tuple[list[float], list[float]]:
    current = gaussian(
        size=size,
        center=center,
        width=3.2,
        amplitude=amplitude,
    )

    previous = gaussian(
        size=size,
        center=center - shift,
        width=3.2,
        amplitude=amplitude,
    )

    return previous, current


def evolve(
    previous: list[float],
    current: list[float],
    recoverability: list[float],
) -> tuple[list[float], list[float]]:
    size = len(current)

    next_state = [0.0] * size
    next_recovery = recoverability.copy()

    for index in range(1, size - 1):
        recovery = recoverability[index]

        speed = 0.62 * sqrt(recovery)

        damping = (
            0.018
            + 0.18 * (1.0 - recovery)
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
            + speed**2 * laplacian
            - damping * velocity
        )

        local_value = current[index]

        if local_value > 0.42:
            write_strength = (
                0.022
                * (local_value - 0.42)
            )

            next_recovery[index] -= write_strength

        elif local_value < -0.42:
            erase_strength = (
                0.030
                * (abs(local_value) - 0.42)
            )

            next_recovery[index] += erase_strength

        next_recovery[index] += (
            0.0004
            * (1.0 - next_recovery[index])
        )

        next_recovery[index] = max(
            0.35,
            min(1.0, next_recovery[index]),
        )

    return next_state, next_recovery


def apply_operation(
    recoverability: list[float],
    source: int,
    amplitude: float,
    steps: int = 120,
) -> list[float]:
    previous, current = initial_pulse(
        size=len(recoverability),
        center=source,
        amplitude=amplitude,
    )

    for _ in range(steps):
        next_state, next_recovery = evolve(
            previous=previous,
            current=current,
            recoverability=recoverability,
        )

        previous, current = (
            current,
            next_state,
        )

        recoverability = next_recovery

    return recoverability


def memory_signal(
    recoverability: list[float],
    source: int,
    radius: int = 6,
) -> float:
    window = recoverability[
        source - radius : source + radius + 1
    ]

    return (
        1.0
        - sum(window) / len(window)
    )


def mutual_information(
    pairs: list[tuple[int, int]],
) -> float:
    joint = [
        [0, 0],
        [0, 0],
    ]

    expected_counts = [0, 0]
    decoded_counts = [0, 0]

    for expected, decoded in pairs:
        joint[expected][decoded] += 1
        expected_counts[expected] += 1
        decoded_counts[decoded] += 1

    total = len(pairs)
    information = 0.0

    for expected in (0, 1):
        for decoded in (0, 1):
            count = joint[expected][decoded]

            if count == 0:
                continue

            joint_probability = count / total
            expected_probability = (
                expected_counts[expected] / total
            )
            decoded_probability = (
                decoded_counts[decoded] / total
            )

            information += (
                joint_probability
                * log2(
                    joint_probability
                    / (
                        expected_probability
                        * decoded_probability
                    )
                )
            )

    return information


def accuracy(
    pairs: list[tuple[int, int]],
) -> float:
    return (
        sum(
            expected == decoded
            for expected, decoded in pairs
        )
        / len(pairs)
    )


def run_cycle(
    random_generator: Random,
    noise: float,
) -> dict[str, float]:
    size = 181
    source = 38

    recoverability = [1.0] * size

    initial_signal = memory_signal(
        recoverability,
        source,
    )

    recoverability = apply_operation(
        recoverability=recoverability,
        source=source,
        amplitude=0.90,
    )

    written_signal = memory_signal(
        recoverability,
        source,
    )

    recoverability = apply_operation(
        recoverability=recoverability,
        source=source,
        amplitude=-1.10,
    )

    erased_signal = memory_signal(
        recoverability,
        source,
    )

    recoverability = apply_operation(
        recoverability=recoverability,
        source=source,
        amplitude=0.90,
    )

    rewritten_signal = memory_signal(
        recoverability,
        source,
    )

    return {
        "initial": (
            initial_signal
            + random_generator.gauss(0.0, noise)
        ),
        "written": (
            written_signal
            + random_generator.gauss(0.0, noise)
        ),
        "erased": (
            erased_signal
            + random_generator.gauss(0.0, noise)
        ),
        "rewritten": (
            rewritten_signal
            + random_generator.gauss(0.0, noise)
        ),
    }


def main() -> None:
    print("GV Constraint Rewritable Memory")
    print("===============================")

    random_generator = Random(314159)

    trial_count = 400
    noise = 0.0018

    stage_trials = {
        "initial": [],
        "written": [],
        "erased": [],
        "rewritten": [],
    }

    expected_states = {
        "initial": 0,
        "written": 1,
        "erased": 0,
        "rewritten": 1,
    }

    for _ in range(trial_count):
        result = run_cycle(
            random_generator=random_generator,
            noise=noise,
        )

        for stage, signal in result.items():
            stage_trials[stage].append(
                Trial(
                    expected=expected_states[stage],
                    signal=signal,
                )
            )

    zero_signals = (
        [
            trial.signal
            for trial in stage_trials["initial"]
        ]
        + [
            trial.signal
            for trial in stage_trials["erased"]
        ]
    )

    one_signals = (
        [
            trial.signal
            for trial in stage_trials["written"]
        ]
        + [
            trial.signal
            for trial in stage_trials["rewritten"]
        ]
    )

    zero_mean = sum(zero_signals) / len(zero_signals)
    one_mean = sum(one_signals) / len(one_signals)

    threshold = (
        zero_mean + one_mean
    ) / 2.0

    all_pairs = []

    print()
    print("STATE CYCLE")
    print("-----------")
    print(
        " stage       expected   mean signal   accuracy"
    )

    for stage in (
        "initial",
        "written",
        "erased",
        "rewritten",
    ):
        trials = stage_trials[stage]

        pairs = [
            (
                trial.expected,
                int(trial.signal >= threshold),
            )
            for trial in trials
        ]

        all_pairs.extend(pairs)

        mean_signal = (
            sum(trial.signal for trial in trials)
            / len(trials)
        )

        print(
            f" {stage:<11}"
            f"{expected_states[stage]:>8}"
            f"{mean_signal:>14.5f}"
            f"{accuracy(pairs):>11.3f}"
        )

    total_accuracy = accuracy(all_pairs)
    total_information = mutual_information(
        all_pairs
    )

    print()
    print(
        f"Decode threshold             : {threshold:.5f}"
    )
    print(
        f"Overall decoding accuracy    : {total_accuracy:.3f}"
    )
    print(
        f"Overall mutual information   : {total_information:.3f} bits"
    )

    initial_mean = (
        sum(
            trial.signal
            for trial in stage_trials["initial"]
        )
        / trial_count
    )

    written_mean = (
        sum(
            trial.signal
            for trial in stage_trials["written"]
        )
        / trial_count
    )

    erased_mean = (
        sum(
            trial.signal
            for trial in stage_trials["erased"]
        )
        / trial_count
    )

    rewritten_mean = (
        sum(
            trial.signal
            for trial in stage_trials["rewritten"]
        )
        / trial_count
    )

    assert written_mean > initial_mean + 0.01
    assert erased_mean < written_mean * 0.35
    assert rewritten_mean > erased_mean + 0.01
    assert total_information > 0.90

    print()
    print("RESULT")
    print("------")
    print(
        "The positive operation wrote a constrained state."
    )
    print(
        "The opposing operation restored recoverability "
        "and erased the stored state."
    )
    print(
        "A later positive operation successfully wrote "
        "the constrained state again."
    )

    print()
    print("STATE TRANSITION")
    print("----------------")
    print("0 -> 1 -> 0 -> 1")

    print()
    print("INTERPRETATION")
    print("--------------")
    print(
        "The medium now supports operational write, erase, "
        "and rewrite behavior."
    )
    print(
        "The stored bit is represented by a reversible change "
        "in recoverability rather than permanent damage alone."
    )

    print()
    print("IMPORTANT LIMITATION")
    print("--------------------")
    print(
        "The write and erase laws were deliberately defined "
        "through signed pulse responses."
    )
    print(
        "The experiment proves internal coherence, not that "
        "nature implements this mechanism."
    )

    print()
    print("MATHEMATICAL STATUS")
    print("-------------------")
    print(
        "This remains ordinary nonlinear dynamics, hysteresis, "
        "control, and Shannon information theory."
    )
    print(
        "No new mathematics is required."
    )

    print()
    print("NEXT QUESTION")
    print("-------------")
    print(
        "Can multiple neighboring memory cells preserve distinct "
        "bits without cross-talk between constraint waves?"
    )


if __name__ == "__main__":
    main()
