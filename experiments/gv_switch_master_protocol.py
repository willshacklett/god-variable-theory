"""
GV Switch master preregistration runner.

Purpose:
Combine the validated synthetic exclusion gates into one auditable protocol.

This runner does NOT identify GV.
It only asks whether a candidate survives modeled alternatives:

1. clock / timing artifact
2. electromagnetic channel
3. mechanical / acoustic / thermal channel

Final synthetic outcomes:

- NULL SURVIVES
- KNOWN CLOCK/TIMING CHANNEL
- KNOWN EM CHANNEL
- KNOWN ENVIRONMENTAL CHANNEL
- UNEXPLAINED PROPAGATION CANDIDATE

Synthetic methodology only. This is not evidence for GV.
"""

from dataclasses import dataclass
from typing import Dict, List
import json
import time

from gv_switch_clock_crosscheck import (
    Detector as ClockDetector,
    Clock,
    classify_trial as classify_clock_trial,
)

from gv_switch_em_isolation import (
    Detector as EMDetector,
    EMState,
    classify_trial as classify_em_trial,
)

from gv_switch_environment_isolation import (
    Detector as EnvDetector,
    EnvState,
    classify_trial as classify_env_trial,
)


PROTOCOL_VERSION = "GV-SWITCH-PRE-REG-0.1"


@dataclass
class GateResult:
    gate: str
    verdict: str
    passed: bool
    interpretation: str


@dataclass
class ProtocolResult:
    protocol_version: str
    model: str
    seed: int
    final_verdict: str
    gates: List[GateResult]


def clock_setup():
    detectors = [
        ClockDetector("D1", 10.0),
        ClockDetector("D2", 50.0),
        ClockDetector("D3", 100.0),
        ClockDetector("D4", 250.0),
        ClockDetector("D5", 500.0),
        ClockDetector("D6", 1000.0),
    ]

    clocks = [
        Clock("C1", 3e-9, 1.1e-9),
        Clock("C2", -2e-9, 2.5e-9),
        Clock("C3", 7e-9, 1.8e-9),
        Clock("C4", -5e-9, 2.2e-9),
        Clock("C5", 1e-9, 1.4e-9),
        Clock("C6", -7e-9, 2.8e-9),
    ]

    return detectors, clocks


def em_setup():
    detectors = [
        EMDetector("D1", 10.0),
        EMDetector("D2", 50.0),
        EMDetector("D3", 100.0),
        EMDetector("D4", 250.0),
        EMDetector("D5", 500.0),
        EMDetector("D6", 1000.0),
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

    return detectors, states


def env_setup():
    detectors = [
        EnvDetector("D1", 10.0),
        EnvDetector("D2", 50.0),
        EnvDetector("D3", 100.0),
        EnvDetector("D4", 250.0),
        EnvDetector("D5", 500.0),
        EnvDetector("D6", 1000.0),
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

    return detectors, states


def run_clock_gate(model: str, seed: int) -> GateResult:
    detectors, clocks = clock_setup()

    if model == "clock":
        mapped_model = "clock"
    elif model == "em":
        mapped_model = "em"
    else:
        mapped_model = "gv"

    verdict = classify_clock_trial(
        detectors,
        clocks,
        mapped_model,
        seed,
    )

    passed = (
        verdict
        == "CLOCK-CROSSCHECK SURVIVING CANDIDATE"
    )

    return GateResult(
        gate="CLOCK CROSSCHECK",
        verdict=verdict,
        passed=passed,
        interpretation=(
            "Pass means the synthetic timing law remains spatial "
            "across clock reassignment."
            if passed
            else "Fail means clock/timing behavior explains or disrupts the signal."
        ),
    )


def run_em_gate(model: str, seed: int) -> GateResult:
    detectors, states = em_setup()

    mapped_model = "em" if model == "em" else "gv"

    verdict = classify_em_trial(
        detectors,
        states,
        mapped_model,
        seed,
    )

    passed = (
        verdict
        == "EM-ISOLATION SURVIVING CANDIDATE"
    )

    return GateResult(
        gate="EM ISOLATION",
        verdict=verdict,
        passed=passed,
        interpretation=(
            "Pass means the synthetic candidate does not track "
            "the modeled EM manipulations."
            if passed
            else "Fail means the modeled EM channel explains the response."
        ),
    )


def run_environment_gate(
    model: str,
    seed: int,
) -> GateResult:
    detectors, states = env_setup()

    if model == "mechanical":
        mapped_model = "mechanical"
    elif model == "acoustic":
        mapped_model = "acoustic"
    elif model == "thermal":
        mapped_model = "thermal"
    else:
        mapped_model = "gv"

    verdict = classify_env_trial(
        detectors,
        states,
        mapped_model,
        seed,
    )

    passed = (
        verdict
        == "ENVIRONMENT-ISOLATION SURVIVING CANDIDATE"
    )

    return GateResult(
        gate="ENVIRONMENT ISOLATION",
        verdict=verdict,
        passed=passed,
        interpretation=(
            "Pass means the synthetic candidate does not track "
            "the modeled mechanical, acoustic, or thermal controls."
            if passed
            else "Fail means a modeled environmental channel explains the response."
        ),
    )


def derive_final_verdict(
    model: str,
    gates: List[GateResult],
) -> str:
    clock_gate, em_gate, env_gate = gates

    if not clock_gate.passed:
        return "KNOWN CLOCK/TIMING CHANNEL"

    if not em_gate.passed:
        return "KNOWN EM CHANNEL"

    if not env_gate.passed:
        return "KNOWN ENVIRONMENTAL CHANNEL"

    return "UNEXPLAINED PROPAGATION CANDIDATE"


def run_protocol(
    model: str,
    seed: int,
) -> ProtocolResult:
    gates = []

    clock_result = run_clock_gate(
        model,
        seed,
    )
    gates.append(clock_result)

    if not clock_result.passed:
        return ProtocolResult(
            protocol_version=PROTOCOL_VERSION,
            model=model,
            seed=seed,
            final_verdict="KNOWN CLOCK/TIMING CHANNEL",
            gates=gates,
        )

    em_result = run_em_gate(
        model,
        seed + 10000,
    )
    gates.append(em_result)

    if not em_result.passed:
        return ProtocolResult(
            protocol_version=PROTOCOL_VERSION,
            model=model,
            seed=seed,
            final_verdict="KNOWN EM CHANNEL",
            gates=gates,
        )

    env_result = run_environment_gate(
        model,
        seed + 20000,
    )
    gates.append(env_result)

    final_verdict = derive_final_verdict(
        model,
        gates,
    )

    return ProtocolResult(
        protocol_version=PROTOCOL_VERSION,
        model=model,
        seed=seed,
        final_verdict=final_verdict,
        gates=gates,
    )


def print_result(result: ProtocolResult):
    print("\n" + "=" * 72)
    print(
        f"MODEL: {result.model.upper()}"
    )
    print(
        f"PROTOCOL: {result.protocol_version}"
    )
    print(
        f"SEED: {result.seed}"
    )
    print("=" * 72)

    for gate in result.gates:
        status = (
            "PASS"
            if gate.passed
            else "FAIL"
        )

        print(
            f"\n[{status}] {gate.gate}"
        )
        print(
            f"Verdict: {gate.verdict}"
        )
        print(
            f"Interpretation: {gate.interpretation}"
        )

    print(
        "\nFINAL SYNTHETIC VERDICT:"
    )
    print(
        result.final_verdict
    )


def save_audit(
    results: List[ProtocolResult],
):
    payload = {
        "protocol_version": PROTOCOL_VERSION,
        "generated_unix_time": time.time(),
        "warning": (
            "Synthetic methodology only. "
            "This file is not evidence for GV."
        ),
        "results": [
            {
                "model": result.model,
                "seed": result.seed,
                "final_verdict": result.final_verdict,
                "gates": [
                    {
                        "gate": gate.gate,
                        "verdict": gate.verdict,
                        "passed": gate.passed,
                        "interpretation": gate.interpretation,
                    }
                    for gate in result.gates
                ],
            }
            for result in results
        ],
    }

    path = "gv_switch_protocol_audit.json"

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            payload,
            f,
            indent=2,
        )

    print(
        f"\nAudit written to experiments/{path}"
    )


if __name__ == "__main__":
    scenarios = [
        ("clock", 101),
        ("em", 102),
        ("mechanical", 103),
        ("acoustic", 104),
        ("thermal", 105),
        ("gv", 106),
    ]

    results = []

    for model, seed in scenarios:
        result = run_protocol(
            model,
            seed,
        )

        results.append(result)

        print_result(
            result
        )

    save_audit(
        results
    )

    print(
        "\n" + "=" * 72
    )
    print(
        "EXPECTED SYNTHETIC BEHAVIOR"
    )
    print(
        "=" * 72
    )

    expected = {
        "clock": "KNOWN CLOCK/TIMING CHANNEL",
        "em": "KNOWN EM CHANNEL",
        "mechanical": "KNOWN ENVIRONMENTAL CHANNEL",
        "acoustic": "KNOWN ENVIRONMENTAL CHANNEL",
        "thermal": "KNOWN ENVIRONMENTAL CHANNEL",
        "gv": "UNEXPLAINED PROPAGATION CANDIDATE",
    }

    passed = 0

    for result in results:
        target = expected[result.model]

        ok = (
            result.final_verdict
            == target
        )

        if ok:
            passed += 1

        marker = (
            "PASS"
            if ok
            else "FAIL"
        )

        print(
            f"{marker:4s} "
            f"{result.model:12s} "
            f"expected={target} "
            f"got={result.final_verdict}"
        )

    print(
        f"\nProtocol scenario score: "
        f"{passed}/{len(results)}"
    )

    if passed == len(results):
        print(
            "MASTER SYNTHETIC PROTOCOL: PASS"
        )
    else:
        print(
            "MASTER SYNTHETIC PROTOCOL: FAIL"
        )
