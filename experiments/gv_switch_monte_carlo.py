"""
Monte Carlo calibration for the GV Switch falsification framework.

Measures how often the classifier produces each verdict under:
- null noise
- known EM-like coupling
- hypothetical c-speed channel
- hypothetical sub-light channel

This is still synthetic calibration, not evidence for GV.
"""

from collections import Counter
from statistics import mean
from gv_switch_falsification import (
    Detector,
    simulate_trial,
    classify,
)

TRIALS = 5000


def run_scenario(
    title,
    model,
    fraction_c=1.0,
    trials=TRIALS,
):
    detectors = [
        Detector("D1", 10.0),
        Detector("D2", 50.0),
        Detector("D3", 100.0),
        Detector("D4", 250.0),
        Detector("D5", 500.0),
        Detector("D6", 1000.0),
    ]

    verdicts = Counter()
    velocity_fractions = []

    for seed in range(trials):
        observations = simulate_trial(
            detectors=detectors,
            model=model,
            signal_velocity_fraction_c=fraction_c,
            seed=seed,
        )

        result = classify(observations)

        verdicts[result.verdict] += 1

        if result.fraction_of_c is not None:
            velocity_fractions.append(result.fraction_of_c)

    print(f"\n=== {title} ===")
    print(f"Trials: {trials}")

    for verdict, count in sorted(verdicts.items()):
        print(
            f"{verdict:30s} "
            f"{count:6d} "
            f"{count / trials:8.4%}"
        )

    if velocity_fractions:
        print(
            "Mean recovered fraction of c: "
            f"{mean(velocity_fractions):.9f}"
        )

    return verdicts


if __name__ == "__main__":
    null_results = run_scenario(
        "NULL MODEL",
        "null",
    )

    em_results = run_scenario(
        "KNOWN EM-LIKE CHANNEL",
        "known_em",
    )

    c_results = run_scenario(
        "HYPOTHETICAL CHANNEL AT c",
        "c",
        1.0,
    )

    sub_c_results = run_scenario(
        "HYPOTHETICAL CHANNEL AT 0.90c",
        "sub_c",
        0.90,
    )

    null_candidates = null_results.get(
        "ANOMALOUS CHANNEL CANDIDATE", 0
    )

    c_candidates = c_results.get(
        "ANOMALOUS CHANNEL CANDIDATE", 0
    )

    sub_c_candidates = sub_c_results.get(
        "ANOMALOUS CHANNEL CANDIDATE", 0
    )

    fpr = null_candidates / TRIALS
    tpr_c = c_candidates / TRIALS
    tpr_sub_c = sub_c_candidates / TRIALS

    print("\n=== CALIBRATION SUMMARY ===")
    print(f"False-positive rate under null: {fpr:.4%}")
    print(f"Detection power at c:          {tpr_c:.4%}")
    print(f"Detection power at 0.90c:      {tpr_sub_c:.4%}")

    if fpr <= 0.01:
        print("Null FPR target <= 1%: PASS")
    else:
        print("Null FPR target <= 1%: FAIL")
