"""
GV Switch environmental-isolation test.

Purpose:
Separate modeled mechanical, acoustic, and thermal channels from a hypothetical
non-EM spatial propagation candidate.

Synthetic controls:
- vibration isolation
- acoustic damping
- temperature change
- air vs reduced-pressure condition

Synthetic methodology only. This is not evidence for GV.
"""

from dataclasses import dataclass
from collections import Counter
import random
import statistics

C = 299_792_458.0
SOUND_AIR = 343.0
TRIALS = 5000
RUNS_PER_STATE = 12


@dataclass
class Detector:
    name: str
    distance_m: float


@dataclass
class EnvState:
    name: str
    vibration_factor: float
    acoustic_factor: float
    temperature_c: float
    pressure_factor: float


@dataclass
class Measurement:
    detector_name: str
    distance_m: float
    state_name: str
    arrival_s: float
    amplitude: float


def sound_speed(temp_c):
    return 331.3 + 0.606 * temp_c


def simulate_measurement(
    detector,
    state,
    model,
    rng,
):
    timing_noise = rng.gauss(0.0, 2e-10)
    amplitude_noise = rng.gauss(0.0, 0.01)

    if model == "gv":
        return Measurement(
            detector_name=detector.name,
            distance_m=detector.distance_m,
            state_name=state.name,
            arrival_s=(
                detector.distance_m / C
                + timing_noise
            ),
            amplitude=1.0 + amplitude_noise,
        )

    if model == "acoustic":
        v_sound = (
            sound_speed(state.temperature_c)
            * max(state.pressure_factor, 0.05)
        )

        amplitude = (
            state.acoustic_factor
            * state.pressure_factor
            + amplitude_noise
        )

        if amplitude <= 0.05:
            return None

        return Measurement(
            detector_name=detector.name,
            distance_m=detector.distance_m,
            state_name=state.name,
            arrival_s=(
                detector.distance_m / v_sound
                + rng.gauss(0.0, 1e-5)
            ),
            amplitude=amplitude,
        )

    if model == "mechanical":
        mechanical_speed = 5000.0

        amplitude = (
            state.vibration_factor
            + amplitude_noise
        )

        if amplitude <= 0.05:
            return None

        return Measurement(
            detector_name=detector.name,
            distance_m=detector.distance_m,
            state_name=state.name,
            arrival_s=(
                detector.distance_m / mechanical_speed
                + rng.gauss(0.0, 1e-6)
            ),
            amplitude=amplitude,
        )

    if model == "thermal":
        thermal_delay_per_m = (
            1e-3
            * (293.15 / (273.15 + state.temperature_c))
        )

        amplitude = (
            1.0
            + 0.02 * (state.temperature_c - 20.0)
            + amplitude_noise
        )

        return Measurement(
            detector_name=detector.name,
            distance_m=detector.distance_m,
            state_name=state.name,
            arrival_s=(
                detector.distance_m
                * thermal_delay_per_m
                + rng.gauss(0.0, 1e-4)
            ),
            amplitude=amplitude,
        )

    raise ValueError(
        "model must be gv, acoustic, mechanical, or thermal"
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
    expected = len(detectors) * RUNS_PER_STATE

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
        (x - x_mean) * (y - y_mean)
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
    vibration_isolated = results["vibration_isolated"]
    acoustic_damped = results["acoustic_damped"]
    cold = results["cold"]
    warm = results["warm"]
    reduced_pressure = results["reduced_pressure"]

    if baseline["detection_fraction"] < 0.80:
        return "INSUFFICIENT BASELINE"

    baseline_amp = baseline["amplitude"]

    if baseline_amp <= 0:
        return "INSUFFICIENT BASELINE"

    vib_ratio = (
        vibration_isolated["amplitude"]
        / baseline_amp
    )

    acoustic_ratio = (
        acoustic_damped["amplitude"]
        / baseline_amp
    )

    pressure_ratio = (
        reduced_pressure["amplitude"]
        / baseline_amp
    )

    cold_ratio = (
        cold["amplitude"]
        / baseline_amp
    )

    warm_ratio = (
        warm["amplitude"]
        / baseline_amp
    )

    # Channel-specific suppression checks
    if (
        vib_ratio < 0.50
        or vibration_isolated["detection_fraction"] < 0.50
    ):
        return "MECHANICAL CHANNEL LIKELY"

    if (
        acoustic_ratio < 0.50
        or pressure_ratio < 0.50
        or acoustic_damped["detection_fraction"] < 0.50
        or reduced_pressure["detection_fraction"] < 0.50
    ):
        return "ACOUSTIC CHANNEL LIKELY"

    # Thermal signals should vary substantially with temperature
    if (
        abs(cold_ratio - warm_ratio) > 0.20
    ):
        return "THERMAL CHANNEL LIKELY"

    velocities = [
        item["velocity"]
        for item in results.values()
        if item["velocity"] is not None
    ]

    if len(velocities) < 4:
        return "INSUFFICIENT TIMING"

    fractions = [
        velocity / C
        for velocity in velocities
    ]

    mean_fraction = statistics.mean(
        fractions
    )

    # Candidate here is constrained to the c-like branch
    if not 0.95 <= mean_fraction <= 1.05:
        return "NON-C ENVIRONMENTAL EFFECT"

    # Candidate should remain stable across environmental controls
    if (
        vib_ratio >= 0.80
        and acoustic_ratio >= 0.80
        and pressure_ratio >= 0.80
        and abs(cold_ratio - warm_ratio) <= 0.10
    ):
        return "ENVIRONMENT-ISOLATION SURVIVING CANDIDATE"

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
            f"{verdict:40s} "
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
        EnvState(
            name="baseline",
            vibration_factor=1.0,
            acoustic_factor=1.0,
            temperature_c=20.0,
            pressure_factor=1.0,
        ),
        EnvState(
            name="vibration_isolated",
            vibration_factor=0.10,
            acoustic_factor=1.0,
            temperature_c=20.0,
            pressure_factor=1.0,
        ),
        EnvState(
            name="acoustic_damped",
            vibration_factor=1.0,
            acoustic_factor=0.10,
            temperature_c=20.0,
            pressure_factor=1.0,
        ),
        EnvState(
            name="cold",
            vibration_factor=1.0,
            acoustic_factor=1.0,
            temperature_c=0.0,
            pressure_factor=1.0,
        ),
        EnvState(
            name="warm",
            vibration_factor=1.0,
            acoustic_factor=1.0,
            temperature_c=40.0,
            pressure_factor=1.0,
        ),
        EnvState(
            name="reduced_pressure",
            vibration_factor=1.0,
            acoustic_factor=1.0,
            temperature_c=20.0,
            pressure_factor=0.10,
        ),
    ]

    models = [
        "mechanical",
        "acoustic",
        "thermal",
        "gv",
    ]

    false_candidates = 0
    known_trials = 0
    gv_power = 0.0

    for model in models:
        verdicts = run_model(
            detectors,
            states,
            model,
        )

        if model == "gv":
            gv_power = (
                verdicts.get(
                    "ENVIRONMENT-ISOLATION SURVIVING CANDIDATE",
                    0,
                )
                / TRIALS
            )
        else:
            false_candidates += verdicts.get(
                "ENVIRONMENT-ISOLATION SURVIVING CANDIDATE",
                0,
            )

            known_trials += TRIALS

    fpr = (
        false_candidates / known_trials
        if known_trials
        else 0.0
    )

    print(
        "\n=== ENVIRONMENT ISOLATION SUMMARY ==="
    )

    print(
        f"Known environmental false-positive rate: "
        f"{fpr:.4%}"
    )

    print(
        f"Hypothetical GV detection power: "
        f"{gv_power:.4%}"
    )

    if (
        fpr <= 0.01
        and gv_power >= 0.95
    ):
        print(
            "Environment isolation target: PASS"
        )
    else:
        print(
            "Environment isolation target: FAIL"
        )

    print(
        "\nInterpretation:"
    )

    print(
        "Passing means only that the candidate does not behave like "
        "the modeled mechanical, acoustic, or thermal channels."
    )

    print(
        "It does not identify GV and does not exclude every possible "
        "environmental coupling mechanism."
    )
