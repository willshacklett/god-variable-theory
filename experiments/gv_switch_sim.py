"""
Toy simulation for the GV Switch Hypothesis.

This does not simulate real GV physics.
It only provides a timing framework for comparing hypothetical
propagation models against a null model.
"""

from dataclasses import dataclass
from typing import List
import random

C = 299_792_458.0  # m/s


@dataclass
class Detector:
    name: str
    distance_m: float


@dataclass
class Arrival:
    detector: str
    distance_m: float
    true_arrival_s: float | None
    measured_arrival_s: float | None


def simulate_arrivals(
    detectors: List[Detector],
    mode: str = "c",
    velocity_fraction_c: float = 1.0,
    timing_noise_s: float = 0.0,
    detection_probability: float = 1.0,
    seed: int = 42,
) -> List[Arrival]:
    rng = random.Random(seed)
    results = []

    for detector in detectors:
        if mode == "null":
            results.append(
                Arrival(
                    detector=detector.name,
                    distance_m=detector.distance_m,
                    true_arrival_s=None,
                    measured_arrival_s=None,
                )
            )
            continue

        if mode == "c":
            velocity = C
        elif mode == "sub_c":
            if not 0 < velocity_fraction_c < 1:
                raise ValueError(
                    "velocity_fraction_c must be between 0 and 1 for sub_c mode"
                )
            velocity = C * velocity_fraction_c
        else:
            raise ValueError("mode must be one of: null, c, sub_c")

        true_arrival = detector.distance_m / velocity

        if rng.random() > detection_probability:
            measured = None
        else:
            measured = true_arrival + rng.gauss(0.0, timing_noise_s)

        results.append(
            Arrival(
                detector=detector.name,
                distance_m=detector.distance_m,
                true_arrival_s=true_arrival,
                measured_arrival_s=measured,
            )
        )

    return results


def estimate_velocity(arrivals: List[Arrival]) -> float | None:
    usable = [
        a for a in arrivals
        if a.measured_arrival_s is not None and a.measured_arrival_s > 0
    ]

    if len(usable) < 2:
        return None

    xs = [a.measured_arrival_s for a in usable]
    ys = [a.distance_m for a in usable]

    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)

    numerator = sum(
        (x - x_mean) * (y - y_mean)
        for x, y in zip(xs, ys)
    )
    denominator = sum(
        (x - x_mean) ** 2
        for x in xs
    )

    if denominator == 0:
        return None

    return numerator / denominator


def print_run(title: str, arrivals: List[Arrival]) -> None:
    print(f"\n=== {title} ===")

    for a in arrivals:
        if a.measured_arrival_s is None:
            print(
                f"{a.detector:10s}  "
                f"{a.distance_m:10.2f} m   no detection"
            )
        else:
            print(
                f"{a.detector:10s}  "
                f"{a.distance_m:10.2f} m   "
                f"{a.measured_arrival_s:.12e} s"
            )

    v = estimate_velocity(arrivals)

    if v is None:
        print("Estimated propagation velocity: unavailable")
    else:
        print(f"Estimated propagation velocity: {v:.6e} m/s")
        print(f"Fraction of c: {v / C:.9f}")


if __name__ == "__main__":
    detectors = [
        Detector("D1", 1.0),
        Detector("D2", 10.0),
        Detector("D3", 100.0),
        Detector("D4", 1000.0),
    ]

    null_case = simulate_arrivals(
        detectors,
        mode="null",
    )

    c_case = simulate_arrivals(
        detectors,
        mode="c",
        timing_noise_s=1e-10,
    )

    sub_c_case = simulate_arrivals(
        detectors,
        mode="sub_c",
        velocity_fraction_c=0.90,
        timing_noise_s=1e-10,
    )

    print_run("NULL MODEL", null_case)
    print_run("MASSLESS-LIKE MODEL: v = c", c_case)
    print_run("SUB-LIGHT MODEL: v = 0.90c", sub_c_case)
