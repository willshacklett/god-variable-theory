"""
GV Predictive Value Audit — Pure Python

Research question
-----------------
Does the GV recoverability state improve prediction of future dynamics
beyond information already contained in the observable wave state?

Three regression models are compared:

1. BASELINE
   Uses observable wave variables only.

2. GV
   Adds recoverability and recoverability interactions.

3. SHUFFLED CONTROL
   Uses shuffled recoverability values.

This version uses no external dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from random import Random


@dataclass(frozen=True)
class Metrics:
    mse: float
    mae: float
    r_squared: float


@dataclass(frozen=True)
class ModelResult:
    name: str
    metrics: Metrics
    coefficients: list[float]


def generate_sample(
    random_generator: Random,
) -> tuple[list[float], float, float]:
    current = random_generator.uniform(-1.0, 1.0)
    velocity = random_generator.uniform(-0.35, 0.35)
    previous = current - velocity

    left = current + random_generator.uniform(-0.55, 0.55)
    right = current + random_generator.uniform(-0.55, 0.55)

    recoverability = random_generator.uniform(0.35, 1.0)

    curvature = left - 2.0 * current + right

    local_speed = 0.62 * sqrt(recoverability)

    local_damping = (
        0.018
        + 0.18 * (1.0 - recoverability)
    )

    next_amplitude = (
        2.0 * current
        - previous
        + local_speed**2 * curvature
        - local_damping * velocity
    )

    next_amplitude += random_generator.gauss(
        0.0,
        0.012,
    )

    baseline_features = [
        current,
        previous,
        left,
        right,
        velocity,
        curvature,
    ]

    return (
        baseline_features,
        recoverability,
        next_amplitude,
    )


def create_dataset(
    sample_count: int,
    seed: int,
) -> tuple[
    list[list[float]],
    list[float],
    list[float],
]:
    random_generator = Random(seed)

    baseline_rows = []
    recoverability_values = []
    targets = []

    for _ in range(sample_count):
        baseline, recovery, target = generate_sample(
            random_generator
        )

        baseline_rows.append(baseline)
        recoverability_values.append(recovery)
        targets.append(target)

    return (
        baseline_rows,
        recoverability_values,
        targets,
    )


def build_gv_features(
    baseline_features: list[list[float]],
    recoverability: list[float],
) -> list[list[float]]:
    rows = []

    for baseline, recovery in zip(
        baseline_features,
        recoverability,
    ):
        velocity = baseline[4]
        curvature = baseline[5]

        rows.append(
            baseline
            + [
                recovery,
                recovery * curvature,
                recovery * velocity,
            ]
        )

    return rows


def column_means(
    matrix: list[list[float]],
) -> list[float]:
    row_count = len(matrix)
    column_count = len(matrix[0])

    return [
        sum(row[column] for row in matrix) / row_count
        for column in range(column_count)
    ]


def column_standard_deviations(
    matrix: list[list[float]],
    means: list[float],
) -> list[float]:
    row_count = len(matrix)
    column_count = len(matrix[0])

    deviations = []

    for column in range(column_count):
        variance = (
            sum(
                (
                    row[column]
                    - means[column]
                )
                ** 2
                for row in matrix
            )
            / row_count
        )

        deviation = sqrt(variance)

        if deviation < 1e-12:
            deviation = 1.0

        deviations.append(deviation)

    return deviations


def standardize(
    matrix: list[list[float]],
    means: list[float],
    deviations: list[float],
) -> list[list[float]]:
    return [
        [
            (
                value
                - means[column]
            )
            / deviations[column]
            for column, value in enumerate(row)
        ]
        for row in matrix
    ]


def transpose(
    matrix: list[list[float]],
) -> list[list[float]]:
    return [
        list(column)
        for column in zip(*matrix)
    ]


def matrix_multiply(
    first: list[list[float]],
    second: list[list[float]],
) -> list[list[float]]:
    second_transposed = transpose(second)

    return [
        [
            sum(a * b for a, b in zip(row, column))
            for column in second_transposed
        ]
        for row in first
    ]


def matrix_vector_multiply(
    matrix: list[list[float]],
    vector: list[float],
) -> list[float]:
    return [
        sum(value * coefficient for value, coefficient in zip(row, vector))
        for row in matrix
    ]


def solve_linear_system(
    matrix: list[list[float]],
    vector: list[float],
) -> list[float]:
    size = len(vector)

    augmented = [
        matrix[row][:]
        + [vector[row]]
        for row in range(size)
    ]

    for pivot in range(size):
        pivot_row = max(
            range(pivot, size),
            key=lambda row: abs(
                augmented[row][pivot]
            ),
        )

        if abs(augmented[pivot_row][pivot]) < 1e-12:
            raise ValueError(
                "Regression system is singular."
            )

        augmented[pivot], augmented[pivot_row] = (
            augmented[pivot_row],
            augmented[pivot],
        )

        pivot_value = augmented[pivot][pivot]

        augmented[pivot] = [
            value / pivot_value
            for value in augmented[pivot]
        ]

        for row in range(size):
            if row == pivot:
                continue

            factor = augmented[row][pivot]

            augmented[row] = [
                current - factor * pivot_value_row
                for current, pivot_value_row in zip(
                    augmented[row],
                    augmented[pivot],
                )
            ]

    return [
        augmented[row][-1]
        for row in range(size)
    ]


def add_intercept(
    features: list[list[float]],
) -> list[list[float]]:
    return [
        [1.0] + row
        for row in features
    ]


def fit_ridge_regression(
    features: list[list[float]],
    targets: list[float],
    penalty: float = 1e-8,
) -> list[float]:
    design = add_intercept(features)
    design_transposed = transpose(design)

    gram = matrix_multiply(
        design_transposed,
        design,
    )

    target_vector = matrix_vector_multiply(
        design_transposed,
        targets,
    )

    for index in range(1, len(gram)):
        gram[index][index] += penalty

    return solve_linear_system(
        gram,
        target_vector,
    )


def predict(
    features: list[list[float]],
    coefficients: list[float],
) -> list[float]:
    design = add_intercept(features)

    return matrix_vector_multiply(
        design,
        coefficients,
    )


def evaluate(
    truth: list[float],
    predictions: list[float],
) -> Metrics:
    errors = [
        actual - predicted
        for actual, predicted in zip(
            truth,
            predictions,
        )
    ]

    mse = sum(
        error**2
        for error in errors
    ) / len(errors)

    mae = sum(
        abs(error)
        for error in errors
    ) / len(errors)

    truth_mean = sum(truth) / len(truth)

    residual_sum = sum(
        error**2
        for error in errors
    )

    total_sum = sum(
        (
            actual - truth_mean
        )
        ** 2
        for actual in truth
    )

    r_squared = (
        1.0
        - residual_sum / total_sum
    )

    return Metrics(
        mse=mse,
        mae=mae,
        r_squared=r_squared,
    )


def run_model(
    name: str,
    train_features: list[list[float]],
    test_features: list[list[float]],
    train_targets: list[float],
    test_targets: list[float],
) -> ModelResult:
    means = column_means(
        train_features
    )

    deviations = column_standard_deviations(
        train_features,
        means,
    )

    standardized_train = standardize(
        train_features,
        means,
        deviations,
    )

    standardized_test = standardize(
        test_features,
        means,
        deviations,
    )

    coefficients = fit_ridge_regression(
        standardized_train,
        train_targets,
    )

    predictions = predict(
        standardized_test,
        coefficients,
    )

    return ModelResult(
        name=name,
        metrics=evaluate(
            test_targets,
            predictions,
        ),
        coefficients=coefficients,
    )


def improvement_percent(
    baseline_value: float,
    improved_value: float,
) -> float:
    return (
        (
            baseline_value
            - improved_value
        )
        / baseline_value
        * 100.0
    )


def print_result(
    result: ModelResult,
) -> None:
    print(
        f"{result.name:<20}"
        f"{result.metrics.mse:>14.8f}"
        f"{result.metrics.mae:>14.8f}"
        f"{result.metrics.r_squared:>12.6f}"
    )


def main() -> None:
    print("GV Predictive Value Audit")
    print("=========================")

    sample_count = 12000

    (
        baseline_features,
        recoverability,
        targets,
    ) = create_dataset(
        sample_count=sample_count,
        seed=20260720,
    )

    split_index = int(
        sample_count * 0.75
    )

    train_baseline = baseline_features[
        :split_index
    ]

    test_baseline = baseline_features[
        split_index:
    ]

    train_recoverability = recoverability[
        :split_index
    ]

    test_recoverability = recoverability[
        split_index:
    ]

    train_targets = targets[
        :split_index
    ]

    test_targets = targets[
        split_index:
    ]

    train_gv = build_gv_features(
        train_baseline,
        train_recoverability,
    )

    test_gv = build_gv_features(
        test_baseline,
        test_recoverability,
    )

    shuffle_generator = Random(7319)

    shuffled_train_recoverability = (
        train_recoverability[:]
    )

    shuffled_test_recoverability = (
        test_recoverability[:]
    )

    shuffle_generator.shuffle(
        shuffled_train_recoverability
    )

    shuffle_generator.shuffle(
        shuffled_test_recoverability
    )

    train_shuffled = build_gv_features(
        train_baseline,
        shuffled_train_recoverability,
    )

    test_shuffled = build_gv_features(
        test_baseline,
        shuffled_test_recoverability,
    )

    baseline_result = run_model(
        name="BASELINE",
        train_features=train_baseline,
        test_features=test_baseline,
        train_targets=train_targets,
        test_targets=test_targets,
    )

    gv_result = run_model(
        name="GV",
        train_features=train_gv,
        test_features=test_gv,
        train_targets=train_targets,
        test_targets=test_targets,
    )

    shuffled_result = run_model(
        name="SHUFFLED CONTROL",
        train_features=train_shuffled,
        test_features=test_shuffled,
        train_targets=train_targets,
        test_targets=test_targets,
    )

    print()
    print(
        f"Training samples       : {split_index}"
    )

    print(
        "Testing samples        : "
        f"{sample_count - split_index}"
    )

    print()
    print("PREDICTION RESULTS")
    print("------------------")
    print(
        f"{'model':<20}"
        f"{'MSE':>14}"
        f"{'MAE':>14}"
        f"{'R^2':>12}"
    )

    print_result(baseline_result)
    print_result(gv_result)
    print_result(shuffled_result)

    mse_improvement = improvement_percent(
        baseline_result.metrics.mse,
        gv_result.metrics.mse,
    )

    mae_improvement = improvement_percent(
        baseline_result.metrics.mae,
        gv_result.metrics.mae,
    )

    shuffled_mse_change = improvement_percent(
        baseline_result.metrics.mse,
        shuffled_result.metrics.mse,
    )

    print()
    print("GV PREDICTIVE GAIN")
    print("------------------")

    print(
        "MSE reduction using GV        : "
        f"{mse_improvement:.2f}%"
    )

    print(
        "MAE reduction using GV        : "
        f"{mae_improvement:.2f}%"
    )

    print(
        "MSE change with shuffled GV   : "
        f"{shuffled_mse_change:.2f}%"
    )

    assert (
        gv_result.metrics.mse
        < baseline_result.metrics.mse * 0.25
    )

    assert (
        gv_result.metrics.mse
        < shuffled_result.metrics.mse * 0.25
    )

    assert (
        abs(
            shuffled_result.metrics.mse
            - baseline_result.metrics.mse
        )
        / baseline_result.metrics.mse
        < 0.08
    )

    print()
    print("RESULT")
    print("------")

    print(
        "True recoverability substantially improved "
        "prediction of the next wave state."
    )

    print(
        "Shuffled recoverability did not produce "
        "the same improvement."
    )

    print()
    print("CRITICAL LIMITATION")
    print("-------------------")

    print(
        "The simulator was explicitly defined so "
        "recoverability affects future motion."
    )

    print(
        "This validates predictive value inside "
        "the synthetic GV model only."
    )

    print()
    print("NEXT TEST")
    print("---------")

    print(
        "Infer recoverability from observable history "
        "and test on genuinely held-out sequences."
    )


if __name__ == "__main__":
    main()
