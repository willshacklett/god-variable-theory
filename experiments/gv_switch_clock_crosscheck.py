"""
Corrected clock cross-check for the GV Switch framework.

Question:
Does an apparent propagation slope follow physical distance consistently
across independently reassigned clock channels?

A real spatial signal should produce approximately the same distance/time
slope for every clock.

A clock-generated artifact with clock-specific drift should produce
different slopes for different clocks.

Synthetic methodology only. This is not evidence for GV.
"""

from dataclasses import dataclass
from collections import Counter, defaultdict
import random
import statistics
import math

C = 299_792_458.0
TRIALS = 5000
RUNS_PER_TRIAL = 20


@dataclass
class Detector:
    name: str
    distance_m: float


@dataclass
class Clock:
    name: str
    offset_s: float
    drift_s_per_m: float


@dataclass
class Measurement:
    detector_name: str
    clock_name: str
    distance_m: float
    arrival_s: float


def linear_fit(xs, ys):
    if len(xs) < 3:
        return None, None, None

    x_mean = statistics.mean(xs)
    y_mean = statistics.mean(ys)

    denominator = sum(
        (x - x_mean) ** 2
        for x in xs
    )

    if denominator == 0:
        return None, None, None

    slope = sum(
        (x - x_mean) * (y - y_mean)
        for x, y in zip(xs, ys)
    ) / denominator

    intercept = y_mean - slope * x_mean

    residuals = [
        y - (intercept + slope * x)
        for x, y in zip(xs, ys)
    ]

    rms = math.sqrt(
        sum(r * r for r in residuals)
        / len(residuals)
    )

    return slope, intercept, rms


def simulate_run(
    detectors,
    assignments,
    model,
    seed,
):
    rng = random.Random(seed)

    output = []

    for detector, clock in zip(
        detectors,
        assignments,
    ):
        noise = rng.gauss(0.0, 2e-10)

        if model in {"gv", "em"}:
            arrival = (
                detector.distance_m / C
                + clock.offset_s
                + noise
            )

        elif model == "clock":
            arrival = (
                clock.offset_s
                + detector.distance_m
                * clock.drift_s_per_m
                + noise
            )

        else:
            raise ValueError(
                "model must be gv, em, or clock"
            )

        output.append(
            Measurement(
                detector_name=detector.name,
                clock_name=clock.name,
                distance_m=detector.distance_m,
                arrival_s=arrival,
            )
        )

    return output


def collect_trial(
    detectors,
    clocks,
    model,
    seed,
):
    rng = random.Random(seed)
    measurements = []

    for run_index in range(RUNS_PER_TRIAL):

        assignments = clocks[:]
        rng.shuffle(assignments)

        measurements.extend(
            simulate_run(
                detectors,
                assignments,
                model,
                seed + 1000 + run_index,
            )
        )

    return measurements


def slopes_by_clock(measurements):
    grouped = defaultdict(list)

    for m in measurements:
        grouped[m.clock_name].append(m)

    results = {}

    for clock_name, values in grouped.items():

        xs = [
            m.distance_m
            for m in values
        ]

        ys = [
            m.arrival_s
            for m in values
        ]

        slope, intercept, rms = linear_fit(
            xs,
            ys,
        )

        if slope is not None:
            results[clock_name] = {
                "slope": slope,
                "intercept": intercept,
                "rms": rms,
                "velocity": (
                    1.0 / slope
                    if slope > 0
                    else None
                ),
            }

    return results


def classify_trial(
    detectors,
    clocks,
    model,
    seed,
):
    measurements = collect_trial(
        detectors,
        clocks,
        model,
        seed,
    )

    fits = slopes_by_clock(
        measurements
    )

    if len(fits) < len(clocks):
        return "INSUFFICIENT"

    slopes = [
        result["slope"]
        for result in fits.values()
    ]

    if any(s <= 0 for s in slopes):
        return "CLOCK / TIMING ARTIFACT"

    velocities = [
        1.0 / s
        for s in slopes
    ]

    fractions_c = [
        v / C
        for v in velocities
    ]

    mean_fraction = statistics.mean(
        fractions_c
    )

    slope_cv = (
        statistics.pstdev(slopes)
        / abs(statistics.mean(slopes))
    )

    mean_rms = statistics.mean(
        result["rms"]
        for result in fits.values()
    )

    # Clock-specific drift should make recovered
    # slopes disagree across clock identities.
    if slope_cv > 0.05:
        return "CLOCK ARTIFACT"

    # Candidate spatial law must be approximately c-like
    # in this particular test.
    if not 0.95 <= mean_fraction <= 1.05:
        return "NON-C SPATIAL / TIMING EFFECT"

    if mean_rms > 1e-9:
        return "CLOCK / TIMING ARTIFACT"

    return "CLOCK-CROSSCHECK SURVIVING CANDIDATE"


def run_model(
    detectors,
    clocks,
    model,
):
    verdicts = Counter()

    for seed in range(TRIALS):

        verdict = classify_trial(
            detectors,
            clocks,
            model,
            seed,
        )

        verdicts[verdict] += 1

    print(f"\n=== {model.upper()} ===")

    for verdict, count in sorted(
        verdicts.items()
    ):
        print(
            f"{verdict:38s} "
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

    clocks = [
        Clock("C1", 3e-9, 1.1e-9),
        Clock("C2", -2e-9, 2.5e-9),
        Clock("C3", 7e-9, 1.8e-9),
        Clock("C4", -5e-9, 2.2e-9),
        Clock("C5", 1e-9, 1.4e-9),
        Clock("C6", -7e-9, 2.8e-9),
    ]

    clock_results = run_model(
        detectors,
        clocks,
        "clock",
    )

    em_results = run_model(
        detectors,
        clocks,
        "em",
    )

    gv_results = run_model(
        detectors,
        clocks,
        "gv",
    )

    false_candidates = (
        clock_results.get(
            "CLOCK-CROSSCHECK SURVIVING CANDIDATE",
            0,
        )
    )

    clock_fpr = (
        false_candidates / TRIALS
    )

    em_survival = (
        em_results.get(
            "CLOCK-CROSSCHECK SURVIVING CANDIDATE",
            0,
        )
        / TRIALS
    )

    gv_power = (
        gv_results.get(
            "CLOCK-CROSSCHECK SURVIVING CANDIDATE",
            0,
        )
        / TRIALS
    )

    print(
        "\n=== CLOCK CROSSCHECK SUMMARY ==="
    )

    print(
        f"Clock-artifact false-positive rate: "
        f"{clock_fpr:.4%}"
    )

    print(
        f"EM spatial-signal survival rate:    "
        f"{em_survival:.4%}"
    )

    print(
        f"Hypothetical GV detection power:    "
        f"{gv_power:.4%}"
    )

    if (
        clock_fpr <= 0.01
        and gv_power >= 0.95
    ):
        print(
            "Clock crosscheck target: PASS"
        )
    else:
        print(
            "Clock crosscheck target: FAIL"
        )

    print(
        "\nNOTE: EM and hypothetical GV are "
        "expected to remain degenerate here."
    )

    print(
        "They must be separated by independent "
        "EM shielding/modulation controls."
    )
