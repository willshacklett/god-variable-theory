"""
GV Hostile Prediction Gauntlet

Research question
-----------------
Can an inferred GV-style constraint state improve genuinely
out-of-sample prediction when the hidden world does not use the
same equations assumed by the GV inference model?

The synthetic world is intentionally hostile:

1. Hidden damage is nonlinear and asymmetric.
2. Recovery rate changes during the sequence.
3. Observations contain measurement noise.
4. Some observations are missing.
5. GV does not receive the true hidden state.
6. GV does not receive the true hidden-state update law.
7. Testing occurs in a later regime with stronger forcing.

Models compared
---------------
1. SNAPSHOT BASELINE
   Instantaneous observable wave variables only.

2. AUTOREGRESSIVE HISTORY
   Snapshot plus recent observed amplitudes.

3. EXPONENTIAL MEMORY
   Snapshot plus a generic exponentially weighted strain history.

4. INFERRED GV
   Snapshot plus an inferred bounded recoverability state.

5. SHUFFLED GV CONTROL
   Same features as inferred GV, but temporal association is destroyed.

6. ORACLE
   Snapshot plus the true hidden state. This is an unavailable
   upper-bound reference.

This is still a synthetic experiment using established mathematics.
It does not demonstrate that GV exists in nature.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import tanh
from random import Random

from mathematics.gv_predictive_value import (
    improvement_percent,
    run_model,
)


@dataclass(frozen=True)
class Observation:
    true_current: float
    observed_current: float
    observed_previous: float
    observed_left: float
    observed_right: float
    observed_velocity: float
    observed_curvature: float
    hidden_recoverability: float
    target: float


@dataclass(frozen=True)
class GVParameters:
    threshold: float
    damage_rate: float
    recovery_rate: float


@dataclass(frozen=True)
class MemoryParameters:
    decay: float


def clamp(
    value: float,
    lower: float,
    upper: float,
) -> float:
    return max(
        lower,
        min(upper, value),
    )


def interpolate_missing(
    values: list[float | None],
) -> list[float]:
    filled: list[float] = []

    last_valid = 0.0

    for value in values:
        if value is None:
            filled.append(last_valid)
        else:
            last_valid = value
            filled.append(value)

    first_valid = next(
        (
            value
            for value in values
            if value is not None
        ),
        0.0,
    )

    for index, value in enumerate(values):
        if value is None and index == 0:
            filled[index] = first_valid
        elif value is not None:
            break

    return filled


def hidden_damage(
    strain: float,
    velocity: float,
    forcing: float,
) -> float:
    """
    Hostile nonlinear law.

    This is deliberately different from the simple linear GV
    inference family used later.
    """

    excess = max(
        0.0,
        strain - 0.38,
    )

    nonlinear_damage = (
        0.014 * excess
        + 0.030 * excess**2
    )

    velocity_damage = (
        0.006
        * max(
            0.0,
            abs(velocity) - 0.16,
        )
    )

    forcing_damage = (
        0.004
        * max(
            0.0,
            abs(forcing) - 0.25,
        )
    )

    return (
        nonlinear_damage
        + velocity_damage
        + forcing_damage
    )


def hidden_recovery_rate(
    step: int,
    total_steps: int,
    recoverability: float,
) -> float:
    regime_fraction = (
        step / max(1, total_steps - 1)
    )

    if regime_fraction < 0.55:
        base_rate = 0.0032
    else:
        base_rate = 0.0013

    state_modifier = (
        0.55
        + 0.45 * recoverability
    )

    return base_rate * state_modifier


def generate_sequence(
    seed: int,
    steps: int,
    hostile_test_regime: bool,
) -> list[Observation]:
    random_generator = Random(seed)

    true_previous = random_generator.uniform(
        -0.12,
        0.12,
    )

    true_current = (
        true_previous
        + random_generator.uniform(
            -0.04,
            0.04,
        )
    )

    hidden_recoverability = 1.0

    raw_current_observations: list[
        float | None
    ] = []

    raw_left_observations: list[
        float | None
    ] = []

    raw_right_observations: list[
        float | None
    ] = []

    true_rows: list[
        tuple[
            float,
            float,
            float,
            float,
            float,
            float,
            float,
        ]
    ] = []

    for step in range(steps):
        regime_fraction = (
            step / max(1, steps - 1)
        )

        if hostile_test_regime:
            forcing_scale = (
                0.23
                if regime_fraction < 0.45
                else 0.36
            )
        else:
            forcing_scale = (
                0.20
                if regime_fraction < 0.55
                else 0.27
            )

        forcing = random_generator.gauss(
            0.0,
            forcing_scale,
        )

        restoring_force = (
            -0.48 * tanh(1.35 * true_current)
        )

        curvature = (
            restoring_force
            + forcing
        )

        asymmetry = random_generator.uniform(
            -0.11,
            0.11,
        )

        true_left = (
            true_current
            + 0.5 * curvature
            + asymmetry
        )

        true_right = (
            true_current
            + 0.5 * curvature
            - asymmetry
        )

        true_velocity = (
            true_current
            - true_previous
        )

        speed_squared = (
            0.62**2
            * (
                0.18
                + 0.82
                * hidden_recoverability**1.35
            )
        )

        damping = (
            0.016
            + 0.24
            * (
                1.0
                - hidden_recoverability
            )
            ** 1.20
        )

        nonlinear_drag = (
            0.020
            * true_velocity
            * abs(true_velocity)
        )

        next_amplitude = (
            2.0 * true_current
            - true_previous
            + speed_squared * curvature
            - damping * true_velocity
            - nonlinear_drag
        )

        next_amplitude += random_generator.gauss(
            0.0,
            0.014,
        )

        true_rows.append(
            (
                true_current,
                true_previous,
                true_left,
                true_right,
                hidden_recoverability,
                next_amplitude,
                forcing,
            )
        )

        observation_noise = (
            0.024
            if hostile_test_regime
            else 0.020
        )

        missing_probability = (
            0.10
            if hostile_test_regime
            else 0.07
        )

        observed_current: float | None = (
            true_current
            + random_generator.gauss(
                0.0,
                observation_noise,
            )
        )

        observed_left: float | None = (
            true_left
            + random_generator.gauss(
                0.0,
                observation_noise,
            )
        )

        observed_right: float | None = (
            true_right
            + random_generator.gauss(
                0.0,
                observation_noise,
            )
        )

        if (
            random_generator.random()
            < missing_probability
        ):
            observed_current = None

        if (
            random_generator.random()
            < missing_probability
        ):
            observed_left = None

        if (
            random_generator.random()
            < missing_probability
        ):
            observed_right = None

        raw_current_observations.append(
            observed_current
        )

        raw_left_observations.append(
            observed_left
        )

        raw_right_observations.append(
            observed_right
        )

        damage = hidden_damage(
            strain=abs(true_current),
            velocity=true_velocity,
            forcing=forcing,
        )

        hidden_recoverability -= damage

        recovery_rate = hidden_recovery_rate(
            step=step,
            total_steps=steps,
            recoverability=hidden_recoverability,
        )

        hidden_recoverability += (
            recovery_rate
            * (
                1.0
                - hidden_recoverability
            )
        )

        hidden_recoverability = clamp(
            hidden_recoverability,
            0.28,
            1.0,
        )

        true_previous, true_current = (
            true_current,
            next_amplitude,
        )

    filled_current = interpolate_missing(
        raw_current_observations
    )

    filled_left = interpolate_missing(
        raw_left_observations
    )

    filled_right = interpolate_missing(
        raw_right_observations
    )

    observations = []

    for index, true_row in enumerate(
        true_rows
    ):
        (
            true_current,
            _true_previous,
            _true_left,
            _true_right,
            hidden_recoverability,
            target,
            _forcing,
        ) = true_row

        observed_current = (
            filled_current[index]
        )

        if index == 0:
            observed_previous = (
                observed_current
            )
        else:
            observed_previous = (
                filled_current[index - 1]
            )

        observed_left = filled_left[index]
        observed_right = filled_right[index]

        observed_velocity = (
            observed_current
            - observed_previous
        )

        observed_curvature = (
            observed_left
            - 2.0 * observed_current
            + observed_right
        )

        observations.append(
            Observation(
                true_current=true_current,
                observed_current=observed_current,
                observed_previous=observed_previous,
                observed_left=observed_left,
                observed_right=observed_right,
                observed_velocity=observed_velocity,
                observed_curvature=observed_curvature,
                hidden_recoverability=hidden_recoverability,
                target=target,
            )
        )

    return observations


def generate_sequences(
    count: int,
    steps: int,
    seed: int,
    hostile_test_regime: bool,
) -> list[list[Observation]]:
    return [
        generate_sequence(
            seed=(
                seed
                + index * 7919
            ),
            steps=steps,
            hostile_test_regime=hostile_test_regime,
        )
        for index in range(count)
    ]


def infer_gv_state(
    sequence: list[Observation],
    parameters: GVParameters,
) -> list[float]:
    inferred = 1.0
    values = []

    for observation in sequence:
        values.append(inferred)

        strain = abs(
            observation.observed_current
        )

        if strain > parameters.threshold:
            inferred -= (
                parameters.damage_rate
                * (
                    strain
                    - parameters.threshold
                )
            )

        inferred += (
            parameters.recovery_rate
            * (
                1.0 - inferred
            )
        )

        inferred = clamp(
            inferred,
            0.28,
            1.0,
        )

    return values


def infer_exponential_memory(
    sequence: list[Observation],
    parameters: MemoryParameters,
) -> list[float]:
    memory = 0.0
    values = []

    for observation in sequence:
        strain = abs(
            observation.observed_current
        )

        memory = (
            parameters.decay * memory
            + (
                1.0
                - parameters.decay
            )
            * strain
        )

        values.append(memory)

    return values


def baseline_features(
    observation: Observation,
) -> list[float]:
    return [
        observation.observed_current,
        observation.observed_previous,
        observation.observed_left,
        observation.observed_right,
        observation.observed_velocity,
        observation.observed_curvature,
    ]


def autoregressive_features(
    sequence: list[Observation],
    index: int,
    lags: int = 6,
) -> list[float]:
    row = baseline_features(
        sequence[index]
    )

    for lag in range(1, lags + 1):
        history_index = max(
            0,
            index - lag,
        )

        row.append(
            sequence[
                history_index
            ].observed_current
        )

    return row


def state_augmented_features(
    observation: Observation,
    state: float,
) -> list[float]:
    row = baseline_features(
        observation
    )

    return row + [
        state,
        state
        * observation.observed_curvature,
        state
        * observation.observed_velocity,
    ]


def flatten_baseline(
    sequences: list[list[Observation]],
) -> tuple[
    list[list[float]],
    list[float],
]:
    features = []
    targets = []

    for sequence in sequences:
        for observation in sequence:
            features.append(
                baseline_features(
                    observation
                )
            )

            targets.append(
                observation.target
            )

    return features, targets


def flatten_autoregressive(
    sequences: list[list[Observation]],
) -> tuple[
    list[list[float]],
    list[float],
]:
    features = []
    targets = []

    for sequence in sequences:
        for index, observation in enumerate(
            sequence
        ):
            features.append(
                autoregressive_features(
                    sequence,
                    index,
                )
            )

            targets.append(
                observation.target
            )

    return features, targets


def flatten_gv(
    sequences: list[list[Observation]],
    parameters: GVParameters,
) -> tuple[
    list[list[float]],
    list[float],
    list[float],
]:
    features = []
    states = []
    targets = []

    for sequence in sequences:
        inferred = infer_gv_state(
            sequence,
            parameters,
        )

        for observation, state in zip(
            sequence,
            inferred,
        ):
            features.append(
                state_augmented_features(
                    observation,
                    state,
                )
            )

            states.append(state)
            targets.append(
                observation.target
            )

    return features, states, targets


def flatten_exponential_memory(
    sequences: list[list[Observation]],
    parameters: MemoryParameters,
) -> tuple[
    list[list[float]],
    list[float],
]:
    features = []
    targets = []

    for sequence in sequences:
        memory_values = (
            infer_exponential_memory(
                sequence,
                parameters,
            )
        )

        for observation, memory in zip(
            sequence,
            memory_values,
        ):
            features.append(
                state_augmented_features(
                    observation,
                    memory,
                )
            )

            targets.append(
                observation.target
            )

    return features, targets


def flatten_oracle(
    sequences: list[list[Observation]],
) -> tuple[
    list[list[float]],
    list[float],
    list[float],
]:
    features = []
    states = []
    targets = []

    for sequence in sequences:
        for observation in sequence:
            state = (
                observation
                .hidden_recoverability
            )

            features.append(
                state_augmented_features(
                    observation,
                    state,
                )
            )

            states.append(state)

            targets.append(
                observation.target
            )

    return features, states, targets


def evaluate_gv_parameters(
    training_sequences: list[
        list[Observation]
    ],
    validation_sequences: list[
        list[Observation]
    ],
    parameters: GVParameters,
) -> float:
    train_baseline, train_targets = (
        flatten_baseline(
            training_sequences
        )
    )

    test_baseline, test_targets = (
        flatten_baseline(
            validation_sequences
        )
    )

    train_features, _, _ = flatten_gv(
        training_sequences,
        parameters,
    )

    test_features, _, _ = flatten_gv(
        validation_sequences,
        parameters,
    )

    result = run_model(
        name="GV SEARCH",
        train_features=train_features,
        test_features=test_features,
        train_targets=train_targets,
        test_targets=test_targets,
    )

    baseline = run_model(
        name="BASELINE SEARCH",
        train_features=train_baseline,
        test_features=test_baseline,
        train_targets=train_targets,
        test_targets=test_targets,
    )

    return (
        result.metrics.mse
        / baseline.metrics.mse
    )


def select_gv_parameters(
    training_sequences: list[
        list[Observation]
    ],
    validation_sequences: list[
        list[Observation]
    ],
) -> tuple[
    GVParameters,
    float,
]:
    thresholds = [
        0.30,
        0.40,
        0.50,
        0.60,
    ]

    damage_rates = [
        0.006,
        0.012,
        0.020,
        0.032,
    ]

    recovery_rates = [
        0.0008,
        0.0018,
        0.0035,
        0.0060,
    ]

    best_parameters = None
    best_ratio = float("inf")

    for threshold in thresholds:
        for damage_rate in damage_rates:
            for recovery_rate in recovery_rates:
                parameters = GVParameters(
                    threshold=threshold,
                    damage_rate=damage_rate,
                    recovery_rate=recovery_rate,
                )

                score = evaluate_gv_parameters(
                    training_sequences,
                    validation_sequences,
                    parameters,
                )

                if score < best_ratio:
                    best_ratio = score
                    best_parameters = parameters

    if best_parameters is None:
        raise RuntimeError(
            "GV parameter search failed."
        )

    return best_parameters, best_ratio


def select_memory_parameters(
    training_sequences: list[
        list[Observation]
    ],
    validation_sequences: list[
        list[Observation]
    ],
) -> tuple[
    MemoryParameters,
    float,
]:
    train_baseline, train_targets = (
        flatten_baseline(
            training_sequences
        )
    )

    test_baseline, test_targets = (
        flatten_baseline(
            validation_sequences
        )
    )

    baseline = run_model(
        name="BASELINE SEARCH",
        train_features=train_baseline,
        test_features=test_baseline,
        train_targets=train_targets,
        test_targets=test_targets,
    )

    best_parameters = None
    best_ratio = float("inf")

    for decay in (
        0.70,
        0.82,
        0.90,
        0.95,
        0.98,
        0.995,
    ):
        parameters = MemoryParameters(
            decay=decay
        )

        train_features, _ = (
            flatten_exponential_memory(
                training_sequences,
                parameters,
            )
        )

        test_features, _ = (
            flatten_exponential_memory(
                validation_sequences,
                parameters,
            )
        )

        result = run_model(
            name="MEMORY SEARCH",
            train_features=train_features,
            test_features=test_features,
            train_targets=train_targets,
            test_targets=test_targets,
        )

        ratio = (
            result.metrics.mse
            / baseline.metrics.mse
        )

        if ratio < best_ratio:
            best_ratio = ratio
            best_parameters = parameters

    if best_parameters is None:
        raise RuntimeError(
            "Memory parameter search failed."
        )

    return best_parameters, best_ratio


def correlation(
    first: list[float],
    second: list[float],
) -> float:
    first_mean = (
        sum(first) / len(first)
    )

    second_mean = (
        sum(second) / len(second)
    )

    numerator = sum(
        (
            first_value - first_mean
        )
        * (
            second_value - second_mean
        )
        for first_value, second_value in zip(
            first,
            second,
        )
    )

    first_scale = sum(
        (
            value - first_mean
        )
        ** 2
        for value in first
    )

    second_scale = sum(
        (
            value - second_mean
        )
        ** 2
        for value in second
    )

    denominator = (
        first_scale
        * second_scale
    ) ** 0.5

    if denominator < 1e-12:
        return 0.0

    return numerator / denominator


def print_result(
    name: str,
    result,
) -> None:
    print(
        f"{name:<24}"
        f"{result.metrics.mse:>14.8f}"
        f"{result.metrics.mae:>14.8f}"
        f"{result.metrics.r_squared:>12.6f}"
    )


def main() -> None:
    print("GV Hostile Prediction Gauntlet")
    print("==============================")

    all_training_sequences = (
        generate_sequences(
            count=54,
            steps=300,
            seed=100,
            hostile_test_regime=False,
        )
    )

    tuning_sequences = (
        all_training_sequences[:42]
    )

    validation_sequences = (
        all_training_sequences[42:]
    )

    testing_sequences = generate_sequences(
        count=22,
        steps=340,
        seed=50000,
        hostile_test_regime=True,
    )

    (
        selected_gv,
        gv_validation_ratio,
    ) = select_gv_parameters(
        tuning_sequences,
        validation_sequences,
    )

    (
        selected_memory,
        memory_validation_ratio,
    ) = select_memory_parameters(
        tuning_sequences,
        validation_sequences,
    )

    print()
    print("TRAINING-ONLY MODEL SELECTION")
    print("-----------------------------")
    print(
        "GV threshold               : "
        f"{selected_gv.threshold:.4f}"
    )
    print(
        "GV damage rate             : "
        f"{selected_gv.damage_rate:.4f}"
    )
    print(
        "GV recovery rate           : "
        f"{selected_gv.recovery_rate:.4f}"
    )
    print(
        "GV validation MSE ratio    : "
        f"{gv_validation_ratio:.4f}"
    )
    print(
        "Memory decay               : "
        f"{selected_memory.decay:.4f}"
    )
    print(
        "Memory validation MSE ratio: "
        f"{memory_validation_ratio:.4f}"
    )

    train_baseline, train_targets = (
        flatten_baseline(
            all_training_sequences
        )
    )

    test_baseline, test_targets = (
        flatten_baseline(
            testing_sequences
        )
    )

    (
        train_autoregressive,
        _,
    ) = flatten_autoregressive(
        all_training_sequences
    )

    (
        test_autoregressive,
        _,
    ) = flatten_autoregressive(
        testing_sequences
    )

    (
        train_memory,
        _,
    ) = flatten_exponential_memory(
        all_training_sequences,
        selected_memory,
    )

    (
        test_memory,
        _,
    ) = flatten_exponential_memory(
        testing_sequences,
        selected_memory,
    )

    (
        train_gv,
        train_gv_states,
        _,
    ) = flatten_gv(
        all_training_sequences,
        selected_gv,
    )

    (
        test_gv,
        test_gv_states,
        _,
    ) = flatten_gv(
        testing_sequences,
        selected_gv,
    )

    (
        train_oracle,
        train_true_states,
        _,
    ) = flatten_oracle(
        all_training_sequences
    )

    (
        test_oracle,
        test_true_states,
        _,
    ) = flatten_oracle(
        testing_sequences
    )

    shuffle_generator = Random(81173)

    shuffled_train_states = (
        train_gv_states[:]
    )

    shuffled_test_states = (
        test_gv_states[:]
    )

    shuffle_generator.shuffle(
        shuffled_train_states
    )

    shuffle_generator.shuffle(
        shuffled_test_states
    )

    train_shuffled = []

    for baseline, state in zip(
        train_baseline,
        shuffled_train_states,
    ):
        train_shuffled.append(
            baseline + [
                state,
                state * baseline[5],
                state * baseline[4],
            ]
        )

    test_shuffled = []

    for baseline, state in zip(
        test_baseline,
        shuffled_test_states,
    ):
        test_shuffled.append(
            baseline + [
                state,
                state * baseline[5],
                state * baseline[4],
            ]
        )

    baseline_result = run_model(
        name="SNAPSHOT",
        train_features=train_baseline,
        test_features=test_baseline,
        train_targets=train_targets,
        test_targets=test_targets,
    )

    autoregressive_result = run_model(
        name="AUTOREGRESSIVE",
        train_features=train_autoregressive,
        test_features=test_autoregressive,
        train_targets=train_targets,
        test_targets=test_targets,
    )

    memory_result = run_model(
        name="EXPONENTIAL MEMORY",
        train_features=train_memory,
        test_features=test_memory,
        train_targets=train_targets,
        test_targets=test_targets,
    )

    gv_result = run_model(
        name="INFERRED GV",
        train_features=train_gv,
        test_features=test_gv,
        train_targets=train_targets,
        test_targets=test_targets,
    )

    shuffled_result = run_model(
        name="SHUFFLED GV",
        train_features=train_shuffled,
        test_features=test_shuffled,
        train_targets=train_targets,
        test_targets=test_targets,
    )

    oracle_result = run_model(
        name="ORACLE",
        train_features=train_oracle,
        test_features=test_oracle,
        train_targets=train_targets,
        test_targets=test_targets,
    )

    gv_state_correlation = correlation(
        test_gv_states,
        test_true_states,
    )

    gv_gain = improvement_percent(
        baseline_result.metrics.mse,
        gv_result.metrics.mse,
    )

    autoregressive_gain = improvement_percent(
        baseline_result.metrics.mse,
        autoregressive_result.metrics.mse,
    )

    memory_gain = improvement_percent(
        baseline_result.metrics.mse,
        memory_result.metrics.mse,
    )

    shuffled_gain = improvement_percent(
        baseline_result.metrics.mse,
        shuffled_result.metrics.mse,
    )

    oracle_gap = improvement_percent(
        gv_result.metrics.mse,
        oracle_result.metrics.mse,
    )

    print()
    print("HOSTILE HELD-OUT RESULTS")
    print("------------------------")
    print(
        f"{'model':<24}"
        f"{'MSE':>14}"
        f"{'MAE':>14}"
        f"{'R^2':>12}"
    )

    print_result(
        "SNAPSHOT BASELINE",
        baseline_result,
    )

    print_result(
        "AUTOREGRESSIVE",
        autoregressive_result,
    )

    print_result(
        "EXPONENTIAL MEMORY",
        memory_result,
    )

    print_result(
        "INFERRED GV",
        gv_result,
    )

    print_result(
        "SHUFFLED GV",
        shuffled_result,
    )

    print_result(
        "ORACLE",
        oracle_result,
    )

    print()
    print("GAUNTLET AUDIT")
    print("--------------")
    print(
        "Inferred/true state correlation : "
        f"{gv_state_correlation:.6f}"
    )
    print(
        "Autoregressive MSE reduction    : "
        f"{autoregressive_gain:.2f}%"
    )
    print(
        "Exponential-memory reduction    : "
        f"{memory_gain:.2f}%"
    )
    print(
        "Inferred-GV MSE reduction       : "
        f"{gv_gain:.2f}%"
    )
    print(
        "Shuffled-GV MSE change          : "
        f"{shuffled_gain:.2f}%"
    )
    print(
        "Remaining improvement to oracle : "
        f"{oracle_gap:.2f}%"
    )

    assert (
        abs(shuffled_gain)
        < 8.0
    )

    assert (
        gv_result.metrics.mse
        < baseline_result.metrics.mse
    )

    print()
    print("VERDICT")
    print("-------")

    strongest_conventional = min(
        autoregressive_result.metrics.mse,
        memory_result.metrics.mse,
    )

    if (
        gv_result.metrics.mse
        < strongest_conventional
    ):
        print(
            "GV survived this hostile synthetic test."
        )
        print(
            "Its inferred bounded state outperformed "
            "the tested conventional history baselines."
        )
    else:
        print(
            "GV did not beat the strongest conventional "
            "history baseline."
        )
        print(
            "The simpler model is preferred for this test."
        )

    print()
    print("HONEST INTERPRETATION")
    print("---------------------")
    print(
        "The hidden world used nonlinear damage, variable "
        "recovery, noisy observations, missing values, and "
        "a shifted future regime."
    )
    print(
        "The inferred GV model was intentionally misspecified."
    )
    print(
        "Any predictive gain therefore reflects approximate "
        "state tracking rather than recovery of the exact law."
    )

    print()
    print("SCIENTIFIC LIMITATION")
    print("---------------------")
    print(
        "This remains synthetic data generated by a world that "
        "contains a hidden recoverability variable."
    )
    print(
        "Success would justify external testing, not establish "
        "GV as a natural law."
    )

    print()
    print("NEXT STEP")
    print("---------")
    print(
        "Run this same model-comparison protocol on an external "
        "dataset with unknown generating equations."
    )


if __name__ == "__main__":
    main()
