"""
GV Switch falsification framework.

This is not evidence for GV.
It is a preregistered-style simulation for deciding whether an observed
timing pattern is better explained by known channels, noise, or an
additional propagating channel.
"""

from dataclasses import dataclass
from typing import List, Optional
import math
import random
import statistics

C = 299_792_458.0


@dataclass
class Detector:
    name: str
    distance_m: float


@dataclass
class Observation:
    detector: str
    distance_m: float
    measured_arrival_s: Optional[float]
    control_arrival_s: Optional[float]
    detected: bool


@dataclass
class Classification:
    verdict: str
    estimated_velocity_m_s: Optional[float]
    fraction_of_c: Optional[float]
    residual_rms_s: Optional[float]
    control_match_fraction: float
    detection_fraction: float
    reason: str


def linear_velocity_estimate(observations: List[Observation]) -> Optional[float]:
    usable = [
        o for o in observations
        if o.detected
        and o.measured_arrival_s is not None
        and o.measured_arrival_s > 0
    ]

    if len(usable) < 3:
        return None

    xs = [o.measured_arrival_s for o in usable]
    ys = [o.distance_m for o in usable]

    x_mean = statistics.mean(xs)
    y_mean = statistics.mean(ys)

    numerator = sum(
        (x - x_mean) * (y - y_mean)
        for x, y in zip(xs, ys)
    )
    denominator = sum((x - x_mean) ** 2 for x in xs)

    if denominator == 0:
        return None

    return numerator / denominator


def residual_rms(
    observations: List[Observation],
    velocity_m_s: float,
) -> Optional[float]:
    usable = [
        o for o in observations
        if o.detected and o.measured_arrival_s is not None
    ]

    if not usable:
        return None

    residuals = []

    for o in usable:
        predicted = o.distance_m / velocity_m_s
        residuals.append(o.measured_arrival_s - predicted)

    return math.sqrt(
        sum(r * r for r in residuals) / len(residuals)
    )


def simulate_trial(
    detectors: List[Detector],
    model: str,
    signal_velocity_fraction_c: float = 1.0,
    timing_noise_s: float = 2e-10,
    detection_probability: float = 0.98,
    false_positive_probability: float = 0.01,
    control_match_probability: float = 0.0,
    seed: int = 42,
) -> List[Observation]:
    rng = random.Random(seed)
    observations = []

    for detector in detectors:
        measured = None
        control = None
        detected = False

        if model == "null":
            if rng.random() < false_positive_probability:
                detected = True
                measured = rng.uniform(0.0, 5e-6)

        elif model in {"c", "sub_c", "known_em"}:
            if model == "c":
                velocity = C
            elif model == "sub_c":
                velocity = C * signal_velocity_fraction_c
            else:
                velocity = C

            if rng.random() < detection_probability:
                detected = True
                true_arrival = detector.distance_m / velocity
                measured = true_arrival + rng.gauss(0.0, timing_noise_s)

                if model == "known_em":
                    control = measured + rng.gauss(0.0, timing_noise_s)

                elif rng.random() < control_match_probability:
                    control = measured + rng.gauss(0.0, timing_noise_s)

        else:
            raise ValueError(
                "model must be one of: null, c, sub_c, known_em"
            )

        observations.append(
            Observation(
                detector=detector.name,
                distance_m=detector.distance_m,
                measured_arrival_s=measured,
                control_arrival_s=control,
                detected=detected,
            )
        )

    return observations


def classify(
    observations: List[Observation],
    timing_tolerance_s: float = 1e-9,
    min_detection_fraction: float = 0.75,
    max_control_match_fraction: float = 0.25,
    max_residual_rms_s: float = 5e-9,
) -> Classification:
    total = len(observations)

    detected = [
        o for o in observations
        if o.detected and o.measured_arrival_s is not None
    ]

    detection_fraction = len(detected) / total if total else 0.0

    control_matches = 0

    for o in detected:
        if o.control_arrival_s is None:
            continue

        if abs(o.measured_arrival_s - o.control_arrival_s) <= timing_tolerance_s:
            control_matches += 1

    control_match_fraction = (
        control_matches / len(detected)
        if detected else 0.0
    )

    if detection_fraction < min_detection_fraction:
        return Classification(
            verdict="NULL SURVIVES",
            estimated_velocity_m_s=None,
            fraction_of_c=None,
            residual_rms_s=None,
            control_match_fraction=control_match_fraction,
            detection_fraction=detection_fraction,
            reason="Too few reproducible detections.",
        )

    if control_match_fraction > max_control_match_fraction:
        return Classification(
            verdict="KNOWN CHANNEL LIKELY",
            estimated_velocity_m_s=None,
            fraction_of_c=None,
            residual_rms_s=None,
            control_match_fraction=control_match_fraction,
            detection_fraction=detection_fraction,
            reason="Signal tracks a control channel too closely.",
        )

    velocity = linear_velocity_estimate(observations)

    if velocity is None or velocity <= 0:
        return Classification(
            verdict="NULL SURVIVES",
            estimated_velocity_m_s=None,
            fraction_of_c=None,
            residual_rms_s=None,
            control_match_fraction=control_match_fraction,
            detection_fraction=detection_fraction,
            reason="No stable distance-time propagation law recovered.",
        )

    rms = residual_rms(observations, velocity)

    if rms is None or rms > max_residual_rms_s:
        return Classification(
            verdict="NULL SURVIVES",
            estimated_velocity_m_s=velocity,
            fraction_of_c=velocity / C,
            residual_rms_s=rms,
            control_match_fraction=control_match_fraction,
            detection_fraction=detection_fraction,
            reason="Propagation fit is too poor.",
        )

    return Classification(
        verdict="ANOMALOUS CHANNEL CANDIDATE",
        estimated_velocity_m_s=velocity,
        fraction_of_c=velocity / C,
        residual_rms_s=rms,
        control_match_fraction=control_match_fraction,
        detection_fraction=detection_fraction,
        reason=(
            "Reproducible distance-dependent timing survives "
            "the simulated control-channel checks."
        ),
    )


def print_result(
    title: str,
    observations: List[Observation],
    result: Classification,
) -> None:
    print(f"\n=== {title} ===")

    for o in observations:
        measured = (
            "none"
            if o.measured_arrival_s is None
            else f"{o.measured_arrival_s:.12e}"
        )

        control = (
            "none"
            if o.control_arrival_s is None
            else f"{o.control_arrival_s:.12e}"
        )

        print(
            f"{o.detector:8s} "
            f"{o.distance_m:10.1f} m "
            f"signal={measured:>18s} "
            f"control={control:>18s}"
        )

    print(f"Verdict: {result.verdict}")
    print(f"Detection fraction: {result.detection_fraction:.3f}")
    print(f"Control match fraction: {result.control_match_fraction:.3f}")

    if result.estimated_velocity_m_s is not None:
        print(
            "Estimated velocity: "
            f"{result.estimated_velocity_m_s:.6e} m/s"
        )
        print(f"Fraction of c: {result.fraction_of_c:.9f}")

    if result.residual_rms_s is not None:
        print(f"Residual RMS: {result.residual_rms_s:.6e} s")

    print(f"Reason: {result.reason}")


if __name__ == "__main__":
    detectors = [
        Detector("D1", 10.0),
        Detector("D2", 50.0),
        Detector("D3", 100.0),
        Detector("D4", 250.0),
        Detector("D5", 500.0),
        Detector("D6", 1000.0),
    ]

    scenarios = [
        ("NULL / RANDOM FALSE POSITIVES", "null", 1.0, 101),
        ("KNOWN EM-LIKE CHANNEL", "known_em", 1.0, 102),
        ("HYPOTHETICAL GV AT c", "c", 1.0, 103),
        ("HYPOTHETICAL GV AT 0.90c", "sub_c", 0.90, 104),
    ]

    for title, model, fraction_c, seed in scenarios:
        observations = simulate_trial(
            detectors=detectors,
            model=model,
            signal_velocity_fraction_c=fraction_c,
            seed=seed,
        )

        result = classify(observations)

        print_result(
            title,
            observations,
            result,
        )
