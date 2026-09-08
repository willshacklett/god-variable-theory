"""
GV Switch EM-isolation test.

Purpose:
Separate an ordinary electromagnetic propagation mechanism from a hypothetical
non-EM spatial propagation mechanism.

This synthetic test varies EM-specific controls:
- shielding
- source power
- antenna orientation
- modulation state

A known EM signal should respond to these manipulations.
A hypothetical non-EM candidate should remain approximately stable.

Synthetic methodology only. This is not evidence for GV.
"""

from dataclasses import dataclass
from collections import Counter
import random
import statistics
import math

C = 299_792_458.0
TRIALS = 5000
RUNS_PER_STATE = 12


@dataclass
class Detector:
    name: str
    distance_m: float


@dataclass
class EMState:
    name: str
    shielding: float
    source_power: float
    orientation_factor: float
    modulation_on: bool


@dataclass
class Measurement:
    detector_name: str
    distance_m: float
    state_name: str
    arrival_s: float
    amplitude: float


def simulate_measurement(
    detector,
    state,
    model,
    rng,
):
    timing_noise = rng.gauss(0.0, 2e-10)
    amplitude_noise = rng.gauss(0.0, 0.01)

    propagation_time = (
        detector.distance_m / C
        + timing_noise
    )

    if model == "em":
        modulation_factor = (
            1.0 if state.modulation_on else 0.05
        )

        amplitude = (
            state.source_power
            * state.orientation_factor
            * modulation_factor
            * (1.0 - state.shielding)
            + amplitude_noise
        )

        # Strong shielding or modulation-off may suppress detection.
        if amplitude <= 0.05:
            return None

        return Measurement(
            detector_name=detector.name,
            distance_m=detector.distance_m,
            state_name=state.name,
            arrival_s=propagation_time,
            amplitude=amplitude,
        )

    if model == "gv":
        # Hypothetical non-EM candidate:
        # stable against EM-specific controls.
        amplitude = (
            1.0
            + amplitude_noise
        )

        return Measurement(
            detector_name=detector.name,
            distance_m=detector.distance_m,
            state_name=state.name,
            arrival_s=propagation_time,
            amplitude=amplitude,
        )

    raise ValueError(
        "model must be 'em' or 'gv'"
    )


def run_state(
    detectors,
    state,
    model,
    seed,
):
    rng = random.Random(seed)
    measurements = []

    for run_index in range(RUNS_PER_STATE):
        for detector in detectors:
            m = simulate_measurement(
                detector,
                state,
                model,
                rng,
            )

            if m is not None:
                measurements.append(m)

    return measurements


def mean_amplitude(measurements):
    if not measurements:
        return 0.0

    return statistics.mean(
        m.amplitude
        for m in measurements
    )


def detection_fraction(
    measurements,
    detectors,
):
    expected = (
        len(detectors)
        * RUNS_PER_STATE
    )

    if expected == 0:
        return 0.0

    return len(measurements) / expected


def fit_velocity(measurements):
    if len(measurements) < 4:
        return None

    xs = [
        m.arrival_s
        for m in measurements
    ]

    ys = [
        m.distance_m
        for m in measurements
    ]

    x_mean = statistics.mean(xs)
    y_mean = statistics.mean(ys)

    denominator = sum(
        (x - x_mean) ** 2
        for x in xs
    )

    if denominator == 0:
        return None

    slope = sum(
        (x - x_mean)
        * (y - y_mean)
        for x, y in zip(xs, ys)
    ) / denominator

    return slope


def classify_trial(
    detectors,
    states,
    model,
    seed,
):
    results = {}

    for index, state in enumerate(states):
        measurements = run_state(
            detectors,
            state,
            model,
            seed + index * 1000,
        )

        results[state.name] = {
            "measurements": measurements,
            "amplitude": mean_amplitude(
                measurements
            ),
            "detection_fraction": detection_fraction(
                measurements,
                detectors,
            ),
            "velocity": fit_velocity(
                measurements
            ),
        }

    baseline = results["baseline"]
    shielded = results["shielded"]
    low_power = results["low_power"]
    rotated = results["rotated"]
    modulation_off = results["modulation_off"]

    if baseline["detection_fraction"] < 0.80:
        return "INSUFFICIENT BASELINE"

    baseline_amp = baseline["amplitude"]

    if baseline_amp <= 0:
        return "INSUFFICIENT BASELINE"

    shield_ratio = (
        shielded["amplitude"]
        / baseline_amp
    )

    power_ratio = (
        low_power["amplitude"]
        / baseline_amp
    )

    rotation_ratio = (
        rotated["amplitude"]
        / baseline_amp
    )

    modulation_ratio = (
        modulation_off["amplitude"]
        / baseline_amp
    )

    shield_detection = (
        shielded["detection_fraction"]
    )

    modulation_detection = (
        modulation_off["detection_fraction"]
    )

    # Strong dependence on EM controls.
    if (
        shield_ratio < 0.50
        or power_ratio < 0.50
        or rotation_ratio < 0.50
        or modulation_ratio < 0.50
        or shield_detection < 0.50
        or modulation_detection < 0.50
    ):
        return "EM CHANNEL LIKELY"

    # Candidate must retain spatial timing around c.
    velocities = [
        item["velocity"]
        for item in results.values()
        if item["velocity"] is not None
    ]

    if len(velocities) < 3:
        return "INSUFFICIENT TIMING"

    fractions = [
        velocity / C
        for velocity in velocities
    ]

    mean_fraction = statistics.mean(
        fractions
    )

    if not 0.95 <= mean_fraction <= 1.05:
        return "NON-C TIMING EFFECT"

    # Candidate amplitude should remain reasonably stable
    # under EM-specific manipulation.
    if (
        shield_ratio >= 0.80
        and power_ratio >= 0.80
        and rotation_ratio >= 0.80
        and modulation_ratio >= 0.80
    ):
        return "EM-ISOLATION SURVIVING CANDIDATE"

    return "AMBIGUOUS"


def run_model(
    detectors,
    states,
    model,
):
    verdicts = Counter()

    for seed in range(TRIALS):
        verdict = classify_trial(
            detectors,
            states,
            model,
            seed,
        )

        verdicts[verdict] += 1

    print(f"\n=== {model.upper()} ===")

    for verdict, count in sorted(
        verdicts.items()
    ):
        print(
            f"{verdict:34s} "
            f"{count:6d} "
            f"{count / TRIALS:8.4%}"
        )

    return verdicts


if __name__ == "__main__":
    detectors = [
        Detector("D1", 10.0),
        Detector("D2", 50.0),
        Detector("D3", 100.0),
        Detector("D4", 250.0),
        Detector("D5", 500.0),
        Detector("D6", 1000.0),
    ]

    states = [
        EMState(
            name="baseline",
            shielding=0.0,
            source_power=1.0,
            orientation_factor=1.0,
            modulation_on=True,
        ),
        EMState(
            name="shielded",
            shielding=0.95,
            source_power=1.0,
            orientation_factor=1.0,
            modulation_on=True,
        ),
        EMState(
            name="low_power",
            shielding=0.0,
            source_power=0.20,
            orientation_factor=1.0,
            modulation_on=True,
        ),
        EMState(
            name="rotated",
            shielding=0.0,
            source_power=1.0,
            orientation_factor=0.20,
            modulation_on=True,
        ),
        EMState(
            name="modulation_off",
            shielding=0.0,
            source_power=1.0,
            orientation_factor=1.0,
            modulation_on=False,
        ),
    ]

    em_results = run_model(
        detectors,
        states,
        "em",
    )

    gv_results = run_model(
        detectors,
        states,
        "gv",
    )

    em_false_candidates = (
        em_results.get(
            "EM-ISOLATION SURVIVING CANDIDATE",
            0,
        )
    )

    gv_candidates = (
        gv_results.get(
            "EM-ISOLATION SURVIVING CANDIDATE",
            0,
        )
    )

    em_fpr = (
        em_false_candidates
        / TRIALS
    )

    gv_power = (
        gv_candidates
        / TRIALS
    )

    print(
        "\n=== EM ISOLATION SUMMARY ==="
    )

    print(
        f"EM false-positive rate: "
        f"{em_fpr:.4%}"
    )

    print(
        f"Hypothetical GV detection power: "
        f"{gv_power:.4%}"
    )

    if (
        em_fpr <= 0.01
        and gv_power >= 0.95
    ):
        print(
            "EM isolation target: PASS"
        )
    else:
        print(
            "EM isolation target: FAIL"
        )

    print(
        "\nInterpretation:"
    )

    print(
        "Passing this synthetic gate means only that "
        "the candidate is not behaving like the modeled EM channel."
    )

    print(
        "It does not identify GV and does not exclude "
        "all possible electromagnetic coupling."
    )
