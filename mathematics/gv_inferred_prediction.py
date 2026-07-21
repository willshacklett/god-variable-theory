"""
GV Hidden-State Inference and Prediction Audit

Research question
-----------------
Can a GV recoverability state inferred only from observable history
improve prediction on completely unseen sequences?

The true recoverability state generates the synthetic dynamics but is
hidden from the inferred-GV predictor.

Four models are compared:

1. BASELINE
   Uses only the instantaneous observable wave state.

2. INFERRED GV
   Uses an estimated recoverability state reconstructed from prior
   observed amplitudes.

3. SHUFFLED GV CONTROL
   Uses the inferred recoverability values after their temporal
   association has been destroyed.

4. ORACLE GV
   Uses the simulator's true hidden recoverability state. This is an
   upper-bound reference and is not available to the inferred model.

Inference parameters are chosen using training sequences only.
Testing uses entirely separate held-out sequences.

This uses established state estimation, nonlinear dynamics, regression,
ablation controls, and out-of-sample evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random

from mathematics.gv_predictive_value import (
    build_gv_features,
    improvement_percent,
    run_model,
)


@dataclass(frozen=True)
class Transition:
    baseline: list[float]
    true_recoverability: float
    target: float


@dataclass(frozen=True)
class InferenceParameters:
    threshold: float
    damage_rate: float
    recovery_rate: float


def generate_sequence(
    seed: int,
    steps: int,
) -> list[Transition]:
    random_generator = Random(seed)

    recoverability = 1.0

    previous = random_generator.uniform(
        -0.20,
        0.20,
    )

    current = (
        previous
        + random_generator.uniform(
            -0.05,
            0.05,
        )
    )

    transitions = []

    for _ in range(steps):
        forcing = random_generator.gauss(
            0.0,
            0.22,
        )

        curvature = (
            -0.55 * current
            + forcing
        )

        asymmetry = random_generator.uniform(
            -0.10,
            0.10,
        )

        left = (
            current
            + 0.5 * curvature
            + asymmetry
        )

        right = (
            current
            + 0.5 * curvature
            - asymmetry
        )

        velocity = current - previous

        local_speed_squared = (
            0.62**2
            * recoverability
        )

        local_damping = (
            0.018
            + 0.18
            * (1.0 - recoverability)
        )

        next_amplitude = (
            2.0 * current
            - previous
            + local_speed_squared * curvature
            - local_damping * velocity
        )

        next_amplitude += random_generator.gauss(
            0.0,
            0.012,
        )

        baseline = [
            current,
            previous,
            left,
            right,
            velocity,
            curvature,
        ]

        transitions.append(
            Transition(
                baseline=baseline,
                true_recoverability=recoverability,
                target=next_amplitude,
            )
        )

        strain = abs(current)

        if strain > 0.42:
            recoverability -= (
                0.020
                * (strain - 0.42)
            )

        recoverability += (
            0.0025
            * (1.0 - recoverability)
        )

        recoverability = max(
            0.35,
            min(
                1.0,
                recoverability,
            ),
        )

        previous, current = (
            current,
            next_amplitude,
        )

    return transitions


def generate_sequences(
    count: int,
    steps: int,
    seed: int,
) -> list[list[Transition]]:
    return [
        generate_sequence(
            seed=(
                seed
                + index * 7919
            ),
            steps=steps,
        )
        for index in range(count)
    ]


def infer_recoverability(
    sequence: list[Transition],
    parameters: InferenceParameters,
) -> list[float]:
    """
    Reconstruct recoverability using only prior observed amplitudes.

    No true recoverability values are accessed here.
    """

    inferred = 1.0
    history = []

    for transition in sequence:
        history.append(inferred)

        current = transition.baseline[0]
        strain = abs(current)

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
            * (1.0 - inferred)
        )

        inferred = max(
            0.35,
            min(
                1.0,
                inferred,
            ),
        )

    return history


def inference_prediction(
    transition: Transition,
    inferred_recoverability: float,
) -> float:
    current = transition.baseline[0]
    previous = transition.baseline[1]
    velocity = transition.baseline[4]
    curvature = transition.baseline[5]

    speed_squared = (
        0.62**2
        * inferred_recoverability
    )

    damping = (
        0.018
        + 0.18
        * (
            1.0
            - inferred_recoverability
        )
    )

    return (
        2.0 * current
        - previous
        + speed_squared * curvature
        - damping * velocity
    )


def score_parameters(
    sequences: list[list[Transition]],
    parameters: InferenceParameters,
) -> float:
    squared_error = 0.0
    sample_count = 0

    for sequence in sequences:
        inferred_values = infer_recoverability(
            sequence,
            parameters,
        )

        for transition, inferred in zip(
            sequence,
            inferred_values,
        ):
            prediction = inference_prediction(
                transition,
                inferred,
            )

            error = (
                transition.target
                - prediction
            )

            squared_error += error**2
            sample_count += 1

    return squared_error / sample_count


def select_parameters(
    sequences: list[list[Transition]],
) -> tuple[
    InferenceParameters,
    float,
]:
    thresholds = [
        0.35,
        0.42,
        0.50,
    ]

    damage_rates = [
        0.012,
        0.020,
        0.030,
    ]

    recovery_rates = [
        0.0010,
        0.0025,
        0.0050,
    ]

    best_parameters = None
    best_score = float("inf")

    for threshold in thresholds:
        for damage_rate in damage_rates:
            for recovery_rate in recovery_rates:
                parameters = InferenceParameters(
                    threshold=threshold,
                    damage_rate=damage_rate,
                    recovery_rate=recovery_rate,
                )

                score = score_parameters(
                    sequences,
                    parameters,
                )

                if score < best_score:
                    best_score = score
                    best_parameters = parameters

    if best_parameters is None:
        raise RuntimeError(
            "No inference parameters were selected."
        )

    return (
        best_parameters,
        best_score,
    )


def flatten_sequences(
    sequences: list[list[Transition]],
    parameters: InferenceParameters,
) -> tuple[
    list[list[float]],
    list[float],
    list[float],
    list[float],
]:
    baseline_rows = []
    inferred_values = []
    true_values = []
    targets = []

    for sequence in sequences:
        sequence_inference = infer_recoverability(
            sequence,
            parameters,
        )

        for transition, inferred in zip(
            sequence,
            sequence_inference,
        ):
            baseline_rows.append(
                transition.baseline
            )

            inferred_values.append(
                inferred
            )

            true_values.append(
                transition.true_recoverability
            )

            targets.append(
                transition.target
            )

    return (
        baseline_rows,
        inferred_values,
        true_values,
        targets,
    )


def correlation(
    first: list[float],
    second: list[float],
) -> float:
    first_mean = sum(first) / len(first)
    second_mean = sum(second) / len(second)

    numerator = sum(
        (
            first_value
            - first_mean
        )
        * (
            second_value
            - second_mean
        )
        for first_value, second_value in zip(
            first,
            second,
        )
    )

    first_scale = sum(
        (
            value
            - first_mean
        )
        ** 2
        for value in first
    )

    second_scale = sum(
        (
            value
            - second_mean
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
        f"{name:<22}"
        f"{result.metrics.mse:>14.8f}"
        f"{result.metrics.mae:>14.8f}"
        f"{result.metrics.r_squared:>12.6f}"
    )


def main() -> None:
    print("GV Inferred Prediction Audit")
    print("============================")

    training_sequences = generate_sequences(
        count=50,
        steps=260,
        seed=100,
    )

    testing_sequences = generate_sequences(
        count=20,
        steps=260,
        seed=9000,
    )

    (
        parameters,
        training_inference_mse,
    ) = select_parameters(
        training_sequences
    )

    print()
    print("TRAINING-ONLY STATE INFERENCE")
    print("-----------------------------")
    print(
        "Selected strain threshold  : "
        f"{parameters.threshold:.4f}"
    )
    print(
        "Selected damage rate       : "
        f"{parameters.damage_rate:.4f}"
    )
    print(
        "Selected recovery rate     : "
        f"{parameters.recovery_rate:.4f}"
    )
    print(
        "Training inference MSE     : "
        f"{training_inference_mse:.8f}"
    )

    (
        train_baseline,
        train_inferred,
        train_true,
        train_targets,
    ) = flatten_sequences(
        training_sequences,
        parameters,
    )

    (
        test_baseline,
        test_inferred,
        test_true,
        test_targets,
    ) = flatten_sequences(
        testing_sequences,
        parameters,
    )

    train_inferred_gv = build_gv_features(
        train_baseline,
        train_inferred,
    )

    test_inferred_gv = build_gv_features(
        test_baseline,
        test_inferred,
    )

    train_oracle_gv = build_gv_features(
        train_baseline,
        train_true,
    )

    test_oracle_gv = build_gv_features(
        test_baseline,
        test_true,
    )

    shuffle_generator = Random(8128)

    shuffled_train = train_inferred[:]
    shuffled_test = test_inferred[:]

    shuffle_generator.shuffle(
        shuffled_train
    )

    shuffle_generator.shuffle(
        shuffled_test
    )

    train_shuffled_gv = build_gv_features(
        train_baseline,
        shuffled_train,
    )

    test_shuffled_gv = build_gv_features(
        test_baseline,
        shuffled_test,
    )

    baseline_result = run_model(
        name="BASELINE",
        train_features=train_baseline,
        test_features=test_baseline,
        train_targets=train_targets,
        test_targets=test_targets,
    )

    inferred_result = run_model(
        name="INFERRED GV",
        train_features=train_inferred_gv,
        test_features=test_inferred_gv,
        train_targets=train_targets,
        test_targets=test_targets,
    )

    shuffled_result = run_model(
        name="SHUFFLED GV",
        train_features=train_shuffled_gv,
        test_features=test_shuffled_gv,
        train_targets=train_targets,
        test_targets=test_targets,
    )

    oracle_result = run_model(
        name="ORACLE GV",
        train_features=train_oracle_gv,
        test_features=test_oracle_gv,
        train_targets=train_targets,
        test_targets=test_targets,
    )

    inferred_correlation = correlation(
        test_inferred,
        test_true,
    )

    mse_gain = improvement_percent(
        baseline_result.metrics.mse,
        inferred_result.metrics.mse,
    )

    mae_gain = improvement_percent(
        baseline_result.metrics.mae,
        inferred_result.metrics.mae,
    )

    shuffled_gain = improvement_percent(
        baseline_result.metrics.mse,
        shuffled_result.metrics.mse,
    )

    print()
    print("HELD-OUT SEQUENCE RESULTS")
    print("-------------------------")
    print(
        f"{'model':<22}"
        f"{'MSE':>14}"
        f"{'MAE':>14}"
        f"{'R^2':>12}"
    )

    print_result(
        "BASELINE",
        baseline_result,
    )

    print_result(
        "INFERRED GV",
        inferred_result,
    )

    print_result(
        "SHUFFLED GV",
        shuffled_result,
    )

    print_result(
        "ORACLE GV",
        oracle_result,
    )

    print()
    print("INFERRED GV AUDIT")
    print("-----------------")
    print(
        "Inferred/true state correlation : "
        f"{inferred_correlation:.6f}"
    )
    print(
        "MSE reduction using inferred GV : "
        f"{mse_gain:.2f}%"
    )
    print(
        "MAE reduction using inferred GV : "
        f"{mae_gain:.2f}%"
    )
    print(
        "MSE change using shuffled GV    : "
        f"{shuffled_gain:.2f}%"
    )

    assert inferred_correlation > 0.90

    assert (
        inferred_result.metrics.mse
        < baseline_result.metrics.mse * 0.40
    )

    assert (
        inferred_result.metrics.mse
        < shuffled_result.metrics.mse * 0.40
    )

    assert (
        oracle_result.metrics.mse
        <= inferred_result.metrics.mse * 1.10
    )

    assert (
        abs(
            shuffled_result.metrics.mse
            - baseline_result.metrics.mse
        )
        / baseline_result.metrics.mse
        < 0.10
    )

    print()
    print("RESULT")
    print("------")
    print(
        "Recoverability was hidden from the predictor."
    )
    print(
        "A GV state reconstructed only from observable "
        "history improved prediction on unseen sequences."
    )
    print(
        "Destroying the temporal relationship through "
        "shuffling removed the predictive gain."
    )

    print()
    print("WHAT THIS ESTABLISHES")
    print("---------------------")
    print(
        "Within this synthetic system, observable history "
        "contains enough information to reconstruct the "
        "hidden recoverability state."
    )
    print(
        "That inferred state provides predictive value beyond "
        "the instantaneous wave snapshot."
    )

    print()
    print("CRITICAL LIMITATION")
    print("-------------------")
    print(
        "The hidden dynamics and candidate inference family "
        "were created within the same synthetic framework."
    )
    print(
        "The test demonstrates successful system identification, "
        "not evidence that nature contains a GV field."
    )

    print()
    print("NEXT SCIENTIFIC STEP")
    print("--------------------")
    print(
        "Apply the inference procedure to external data whose "
        "generating equations are unknown."
    )
    print(
        "GV earns empirical status only if its inferred state "
        "improves prediction beyond strong conventional baselines."
    )


if __name__ == "__main__":
    main()
