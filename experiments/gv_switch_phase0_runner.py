"""
GV Switch Phase 0 acceptance runner.

Purpose:
Track hardware-validation results against the machine-readable
Phase 0 acceptance specification.

This runner does not test whether GV exists.

Phase 0 answers only:

Can the apparatus correctly identify known injected artifacts
and satisfy the preregistered hardware-validation requirements?
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import json
import time


BASE_DIR = Path(__file__).resolve().parent

SPEC_PATH = BASE_DIR / "gv_switch_phase0_acceptance.json"
STATE_PATH = BASE_DIR / "gv_switch_phase0_results.json"
AUDIT_PATH = BASE_DIR / "gv_switch_phase0_audit.json"


@dataclass
class TestResult:
    id: str
    name: str
    status: str
    measured_value: Optional[float] = None
    units: Optional[str] = None
    expected_classification: Optional[str] = None
    observed_classification: Optional[str] = None
    notes: str = ""
    updated_unix_time: Optional[float] = None


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, payload):
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def load_spec():
    if not SPEC_PATH.exists():
        raise FileNotFoundError(
            f"Missing acceptance specification: {SPEC_PATH}"
        )

    return load_json(SPEC_PATH)


def empty_state(spec):
    tests = {}

    for item in spec["required_tests"]:
        tests[item["id"]] = asdict(
            TestResult(
                id=item["id"],
                name=item["name"],
                status="NOT_RUN",
            )
        )

    return {
        "protocol": spec["protocol"],
        "phase": spec["phase"],
        "status": "INCOMPLETE",
        "created_unix_time": time.time(),
        "updated_unix_time": time.time(),
        "tests": tests,
    }


def load_state(spec):
    if not STATE_PATH.exists():
        state = empty_state(spec)
        save_json(STATE_PATH, state)
        return state

    return load_json(STATE_PATH)


def required_ids(spec):
    return [
        item["id"]
        for item in spec["required_tests"]
        if item.get("required", False)
    ]


def evaluate_test(test):
    if test["status"] != "PASS":
        return False

    expected = test.get("expected_classification")
    observed = test.get("observed_classification")

    if expected is not None:
        if observed != expected:
            return False

    if observed == "UNEXPLAINED PROPAGATION CANDIDATE":
        return False

    return True


def evaluate_phase0(spec, state):
    required = required_ids(spec)

    passed = 0
    failed = 0
    not_run = 0

    details = []

    for test_id in required:
        test = state["tests"][test_id]

        valid_pass = evaluate_test(test)

        if valid_pass:
            passed += 1
            outcome = "PASS"
        elif test["status"] == "NOT_RUN":
            not_run += 1
            outcome = "NOT_RUN"
        else:
            failed += 1
            outcome = "FAIL"

        details.append(
            {
                "id": test_id,
                "name": test["name"],
                "outcome": outcome,
                "status": test["status"],
                "expected_classification": test.get(
                    "expected_classification"
                ),
                "observed_classification": test.get(
                    "observed_classification"
                ),
            }
        )

    required_passes = spec["pass_rule"]["required_passes"]

    phase0_pass = (
        passed == required_passes
        and failed == 0
        and not_run == 0
    )

    if phase0_pass:
        verdict = "PHASE 0 PASS"
        phase1_allowed = True
    elif failed > 0:
        verdict = "PHASE 0 FAIL"
        phase1_allowed = False
    else:
        verdict = "PHASE 0 INCOMPLETE"
        phase1_allowed = False

    return {
        "verdict": verdict,
        "phase1_allowed": phase1_allowed,
        "passed": passed,
        "failed": failed,
        "not_run": not_run,
        "required": len(required),
        "details": details,
    }


def update_test(
    spec,
    state,
    test_id,
    status,
    measured_value=None,
    units=None,
    expected_classification=None,
    observed_classification=None,
    notes="",
):
    if test_id not in state["tests"]:
        raise ValueError(
            f"Unknown test ID: {test_id}"
        )

    if status not in {
        "PASS",
        "FAIL",
        "NOT_RUN",
    }:
        raise ValueError(
            "status must be PASS, FAIL, or NOT_RUN"
        )

    test = state["tests"][test_id]

    test["status"] = status
    test["measured_value"] = measured_value
    test["units"] = units
    test["expected_classification"] = (
        expected_classification
    )
    test["observed_classification"] = (
        observed_classification
    )
    test["notes"] = notes
    test["updated_unix_time"] = time.time()

    state["updated_unix_time"] = time.time()

    evaluation = evaluate_phase0(
        spec,
        state,
    )

    state["status"] = evaluation["verdict"]

    save_json(
        STATE_PATH,
        state,
    )

    write_audit(
        spec,
        state,
        evaluation,
    )

    return evaluation


def write_audit(
    spec,
    state,
    evaluation,
):
    payload = {
        "protocol": spec["protocol"],
        "phase": spec["phase"],
        "generated_unix_time": time.time(),
        "warning": (
            "Phase 0 validates known-channel classification "
            "and apparatus performance. It is not a GV detection test."
        ),
        "acceptance_spec": spec,
        "state": state,
        "evaluation": evaluation,
    }

    save_json(
        AUDIT_PATH,
        payload,
    )


def print_summary(
    spec,
    state,
):
    evaluation = evaluate_phase0(
        spec,
        state,
    )

    print()
    print("=" * 72)
    print("GV SWITCH PHASE 0 ACCEPTANCE")
    print("=" * 72)

    for detail in evaluation["details"]:
        print(
            f'{detail["id"]}  '
            f'{detail["name"]:24s} '
            f'{detail["outcome"]}'
        )

        expected = detail.get(
            "expected_classification"
        )
        observed = detail.get(
            "observed_classification"
        )

        if expected is not None:
            print(
                f"   expected: {expected}"
            )

        if observed is not None:
            print(
                f"   observed: {observed}"
            )

    print()
    print(
        f'Passed:  {evaluation["passed"]}'
    )
    print(
        f'Failed:  {evaluation["failed"]}'
    )
    print(
        f'Not run: {evaluation["not_run"]}'
    )
    print(
        f'Required: {evaluation["required"]}'
    )

    print()
    print(
        f'FINAL VERDICT: {evaluation["verdict"]}'
    )

    print(
        "PHASE 1 ALLOWED: "
        + (
            "YES"
            if evaluation["phase1_allowed"]
            else "NO"
        )
    )

    print()

    return evaluation


def demo(spec):
    state = empty_state(spec)

    examples = {
        "A": {
            "status": "PASS",
            "measured_value": 0.42,
            "units": "ns",
            "notes": "Synthetic demonstration trigger jitter.",
        },
        "B": {
            "status": "PASS",
            "expected_classification": "CABLE ARTIFACT",
            "observed_classification": "CABLE ARTIFACT",
        },
        "C": {
            "status": "PASS",
            "expected_classification": "KNOWN EM CHANNEL",
            "observed_classification": "KNOWN EM CHANNEL",
        },
        "D": {
            "status": "PASS",
            "expected_classification": "ACOUSTIC CHANNEL LIKELY",
            "observed_classification": "ACOUSTIC CHANNEL LIKELY",
        },
        "E": {
            "status": "PASS",
            "expected_classification": "MECHANICAL CHANNEL LIKELY",
            "observed_classification": "MECHANICAL CHANNEL LIKELY",
        },
        "F": {
            "status": "PASS",
            "expected_classification": "CLOCK ARTIFACT",
            "observed_classification": "CLOCK ARTIFACT",
        },
        "G": {
            "status": "PASS",
            "expected_classification": "THERMAL CHANNEL LIKELY",
            "observed_classification": "THERMAL CHANNEL LIKELY",
        },
    }

    for test_id, values in examples.items():
        test = state["tests"][test_id]

        for key, value in values.items():
            test[key] = value

        test["updated_unix_time"] = time.time()

    state["updated_unix_time"] = time.time()

    evaluation = evaluate_phase0(
        spec,
        state,
    )

    state["status"] = evaluation["verdict"]

    save_json(
        STATE_PATH,
        state,
    )

    write_audit(
        spec,
        state,
        evaluation,
    )

    print(
        "Synthetic Phase 0 demonstration loaded."
    )

    print_summary(
        spec,
        state,
    )


def reset(spec):
    state = empty_state(spec)

    save_json(
        STATE_PATH,
        state,
    )

    evaluation = evaluate_phase0(
        spec,
        state,
    )

    write_audit(
        spec,
        state,
        evaluation,
    )

    print(
        "Phase 0 state reset to NOT_RUN."
    )


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "GV Switch Phase 0 acceptance runner"
        )
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    sub.add_parser(
        "status",
        help="Show Phase 0 acceptance status",
    )

    sub.add_parser(
        "demo",
        help=(
            "Load a synthetic 7/7 demonstration. "
            "This is not hardware data."
        ),
    )

    sub.add_parser(
        "reset",
        help="Reset all Phase 0 tests to NOT_RUN",
    )

    record = sub.add_parser(
        "record",
        help="Record one test result",
    )

    record.add_argument(
        "test_id",
        choices=[
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
        ],
    )

    record.add_argument(
        "status",
        choices=[
            "PASS",
            "FAIL",
            "NOT_RUN",
        ],
    )

    record.add_argument(
        "--measured-value",
        type=float,
        default=None,
    )

    record.add_argument(
        "--units",
        default=None,
    )

    record.add_argument(
        "--expected",
        default=None,
    )

    record.add_argument(
        "--observed",
        default=None,
    )

    record.add_argument(
        "--notes",
        default="",
    )

    return parser


def main():
    spec = load_spec()

    parser = build_parser()
    args = parser.parse_args()

    state = load_state(spec)

    if args.command == "status":
        print_summary(
            spec,
            state,
        )
        return

    if args.command == "demo":
        demo(spec)
        return

    if args.command == "reset":
        reset(spec)
        return

    if args.command == "record":
        evaluation = update_test(
            spec=spec,
            state=state,
            test_id=args.test_id,
            status=args.status,
            measured_value=args.measured_value,
            units=args.units,
            expected_classification=args.expected,
            observed_classification=args.observed,
            notes=args.notes,
        )

        print(
            f"Recorded test {args.test_id}: "
            f"{args.status}"
        )

        print_summary(
            spec,
            load_state(spec),
        )

        if (
            args.observed
            == "UNEXPLAINED PROPAGATION CANDIDATE"
        ):
            print(
                "WARNING: A known injected Phase 0 mechanism "
                "was classified as unexplained."
            )
            print(
                "Phase 1 must remain blocked."
            )

        return


if __name__ == "__main__":
    main()
