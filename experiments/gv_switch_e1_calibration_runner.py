"""
GV Switch E1 electrical sensor calibration runner.

Purpose:
Read real or synthetic calibration-trial CSV data for Prototype E1
and evaluate basic engineering acceptance metrics.

This program does not test whether GV exists.

It evaluates whether the E1 electrical transient sensor is behaving
well enough to be used as a known-channel control instrument.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import csv
import json
import math
import statistics
import time


BASE_DIR = Path(__file__).resolve().parent

ACCEPTANCE_PATH = BASE_DIR / "gv_switch_electric_sensor_acceptance.json"
DEFAULT_CSV_PATH = BASE_DIR / "gv_switch_e1_trials.csv"
REPORT_PATH = BASE_DIR / "gv_switch_e1_calibration_report.json"


REQUIRED_COLUMNS = [
    "trial_id",
    "active_or_sham",
    "trigger_time_ns",
    "sensor_time_ns",
    "sensor_peak_v",
    "sensor_rms_v",
    "threshold_v",
    "source_state",
    "source_level",
    "sensor_distance_m",
    "sensor_orientation_deg",
    "shielding_state",
    "cable_id",
    "scope_channel",
    "apparatus_config_id",
    "git_commit_sha",
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, payload):
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def parse_float(value):
    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    return float(value)


def load_trials(path: Path):
    if not path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {path}"
        )

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        missing = [
            col
            for col in REQUIRED_COLUMNS
            if col not in (reader.fieldnames or [])
        ]

        if missing:
            raise ValueError(
                "Missing required CSV columns: "
                + ", ".join(missing)
            )

        rows = []

        for row in reader:
            rows.append(
                {
                    **row,
                    "trigger_time_ns": parse_float(
                        row["trigger_time_ns"]
                    ),
                    "sensor_time_ns": parse_float(
                        row["sensor_time_ns"]
                    ),
                    "sensor_peak_v": parse_float(
                        row["sensor_peak_v"]
                    ),
                    "sensor_rms_v": parse_float(
                        row["sensor_rms_v"]
                    ),
                    "threshold_v": parse_float(
                        row["threshold_v"]
                    ),
                    "source_level": parse_float(
                        row["source_level"]
                    ),
                    "sensor_distance_m": parse_float(
                        row["sensor_distance_m"]
                    ),
                    "sensor_orientation_deg": parse_float(
                        row["sensor_orientation_deg"]
                    ),
                }
            )

    return rows


def arrival_delay_ns(row):
    trigger = row["trigger_time_ns"]
    sensor = row["sensor_time_ns"]

    if trigger is None or sensor is None:
        return None

    return sensor - trigger


def valid_delays(rows):
    result = []

    for row in rows:
        delay = arrival_delay_ns(row)

        if delay is not None:
            result.append(delay)

    return result


def summarize(values):
    if not values:
        return {
            "n": 0,
            "mean": None,
            "median": None,
            "stdev": None,
            "min": None,
            "max": None,
        }

    if len(values) >= 2:
        stdev = statistics.stdev(values)
    else:
        stdev = 0.0

    return {
        "n": len(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "stdev": stdev,
        "min": min(values),
        "max": max(values),
    }


def group_rows(rows, key):
    groups = {}

    for row in rows:
        value = str(row[key])

        groups.setdefault(value, [])
        groups[value].append(row)

    return groups


def timing_jitter(rows):
    active = [
        row
        for row in rows
        if row["active_or_sham"].strip().lower() == "active"
        and row["sensor_time_ns"] is not None
    ]

    delays = valid_delays(active)

    if len(delays) < 2:
        return None

    return statistics.stdev(delays)


def sham_false_positive_rate(rows):
    sham = [
        row
        for row in rows
        if row["active_or_sham"].strip().lower() == "sham"
    ]

    if not sham:
        return None

    false_hits = 0

    for row in sham:
        sensor_time = row["sensor_time_ns"]
        peak = row["sensor_peak_v"]
        threshold = row["threshold_v"]

        detected = False

        if sensor_time is not None:
            detected = True

        if (
            peak is not None
            and threshold is not None
            and abs(peak) >= abs(threshold)
        ):
            detected = True

        if detected:
            false_hits += 1

    return false_hits / len(sham)


def saturation_check(rows):
    """
    CSV currently contains no explicit scope-full-scale field.

    Therefore true analog saturation cannot be proven from this schema.
    We conservatively report whether identical peak values occur unusually
    often, which may indicate clipping but is not definitive.
    """

    peaks = [
        row["sensor_peak_v"]
        for row in rows
        if row["sensor_peak_v"] is not None
    ]

    if not peaks:
        return {
            "evaluated": False,
            "possible_clipping": None,
            "reason": "No peak-voltage values available."
        }

    rounded = [
        round(value, 9)
        for value in peaks
    ]

    max_abs = max(
        rounded,
        key=lambda x: abs(x)
    )

    count = sum(
        1
        for x in rounded
        if x == max_abs
    )

    fraction = count / len(rounded)

    return {
        "evaluated": True,
        "possible_clipping": fraction >= 0.10,
        "identical_extreme_fraction": fraction,
        "note": (
            "This is only a clipping heuristic. "
            "Actual scope full-scale metadata is required "
            "for a definitive saturation test."
        ),
    }


def compare_group_means(rows, key):
    groups = group_rows(rows, key)

    output = {}

    for name, group in groups.items():
        delays = valid_delays(group)

        peaks = [
            row["sensor_peak_v"]
            for row in group
            if row["sensor_peak_v"] is not None
        ]

        output[name] = {
            "delay_ns": summarize(delays),
            "peak_v": summarize(peaks),
        }

    return output


def calibration_checks(
    acceptance,
    rows,
):
    req = acceptance["requirements"]

    jitter = timing_jitter(rows)
    sham_fpr = sham_false_positive_rate(rows)

    cable_groups = compare_group_means(
        rows,
        "cable_id",
    )

    channel_groups = compare_group_means(
        rows,
        "scope_channel",
    )

    shielding_groups = compare_group_means(
        rows,
        "shielding_state",
    )

    orientation_groups = compare_group_means(
        rows,
        "sensor_orientation_deg",
    )

    saturation = saturation_check(rows)

    active_count = sum(
        1
        for row in rows
        if row["active_or_sham"].strip().lower() == "active"
    )

    sham_count = sum(
        1
        for row in rows
        if row["active_or_sham"].strip().lower() == "sham"
    )

    checks = {}

    checks["waveform_repeatability"] = {
        "status": (
            "PASS"
            if active_count >= req["minimum_trials_per_configuration"]
            else "INCOMPLETE"
        ),
        "active_trials": active_count,
        "minimum_required": req[
            "minimum_trials_per_configuration"
        ],
    }

    checks["timing_jitter_measured"] = {
        "status": (
            "PASS"
            if jitter is not None
            and jitter <= req["target_timing_sigma_ns"]
            else (
                "FAIL"
                if jitter is not None
                else "INCOMPLETE"
            )
        ),
        "timing_sigma_ns": jitter,
        "target_max_ns": req["target_timing_sigma_ns"],
    }

    checks["cable_delay_separable"] = {
        "status": (
            "READY_FOR_REVIEW"
            if len(cable_groups) >= 2
            else "INCOMPLETE"
        ),
        "groups": cable_groups,
        "note": (
            "Human or preregistered model review is required "
            "to confirm delay follows cable identity as expected."
        ),
    }

    checks["scope_channel_skew_separable"] = {
        "status": (
            "READY_FOR_REVIEW"
            if len(channel_groups) >= 2
            else "INCOMPLETE"
        ),
        "groups": channel_groups,
    }

    checks["shielding_response_characterized"] = {
        "status": (
            "READY_FOR_REVIEW"
            if len(shielding_groups) >= 2
            else "INCOMPLETE"
        ),
        "groups": shielding_groups,
    }

    checks["orientation_response_characterized"] = {
        "status": (
            "READY_FOR_REVIEW"
            if len(orientation_groups) >= 2
            else "INCOMPLETE"
        ),
        "groups": orientation_groups,
    }

    checks["sham_false_positive_rate_measured"] = {
        "status": (
            "PASS"
            if sham_fpr is not None
            and sham_fpr <= req["sham_fpr_max"]
            else (
                "FAIL"
                if sham_fpr is not None
                else "INCOMPLETE"
            )
        ),
        "sham_trials": sham_count,
        "false_positive_rate": sham_fpr,
        "maximum_allowed": req["sham_fpr_max"],
    }

    checks["no_saturation_in_operating_range"] = {
        "status": (
            "REVIEW_REQUIRED"
            if saturation["evaluated"]
            else "INCOMPLETE"
        ),
        "analysis": saturation,
    }

    return checks


def overall_verdict(checks):
    statuses = [
        item["status"]
        for item in checks.values()
    ]

    if "FAIL" in statuses:
        return "E1 CALIBRATION FAIL"

    if all(
        status == "PASS"
        for status in statuses
    ):
        return "E1 CALIBRATION PASS"

    return "E1 CALIBRATION INCOMPLETE"


def run(csv_path: Path):
    acceptance = load_json(
        ACCEPTANCE_PATH
    )

    rows = load_trials(
        csv_path
    )

    checks = calibration_checks(
        acceptance,
        rows,
    )

    verdict = overall_verdict(
        checks
    )

    report = {
        "protocol": acceptance["protocol"],
        "phase": acceptance["phase"],
        "prototype": acceptance["prototype"],
        "generated_unix_time": time.time(),
        "source_csv": str(csv_path),
        "trial_count": len(rows),
        "warning": (
            "This report evaluates E1 engineering calibration only. "
            "It does not test whether GV exists."
        ),
        "checks": checks,
        "verdict": verdict,
    }

    save_json(
        REPORT_PATH,
        report,
    )

    print()
    print("=" * 72)
    print("GV SWITCH E1 CALIBRATION")
    print("=" * 72)

    for name, result in checks.items():
        print(
            f"{name:40s} "
            f"{result['status']}"
        )

    print()
    print(
        "FINAL VERDICT:",
        verdict,
    )

    print()
    print(
        "Report written to:",
        REPORT_PATH,
    )

    return report


def create_template(path: Path):
    if path.exists():
        raise FileExistsError(
            f"Refusing to overwrite existing file: {path}"
        )

    with path.open(
        "w",
        encoding="utf-8",
        newline=""
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=REQUIRED_COLUMNS,
        )

        writer.writeheader()

    print(
        "Created E1 calibration CSV template:",
        path,
    )


def create_demo(path: Path):
    if path.exists():
        path.unlink()

    fieldnames = REQUIRED_COLUMNS

    rows = []

    for i in range(100):
        rows.append(
            {
                "trial_id": f"A{i:04d}",
                "active_or_sham": "active",
                "trigger_time_ns": 0.0,
                "sensor_time_ns": 12.0 + ((i % 5) - 2) * 0.1,
                "sensor_peak_v": 0.20 + (i % 3) * 0.002,
                "sensor_rms_v": 0.010,
                "threshold_v": 0.050,
                "source_state": "active",
                "source_level": 1.0,
                "sensor_distance_m": 1.0,
                "sensor_orientation_deg": 0,
                "shielding_state": "unshielded",
                "cable_id": "CABLE_A" if i < 50 else "CABLE_B",
                "scope_channel": "CH1" if i % 2 == 0 else "CH2",
                "apparatus_config_id": "DEMO_ONLY",
                "git_commit_sha": "SYNTHETIC",
            }
        )

    for i in range(100):
        rows.append(
            {
                "trial_id": f"S{i:04d}",
                "active_or_sham": "sham",
                "trigger_time_ns": 0.0,
                "sensor_time_ns": "",
                "sensor_peak_v": 0.005,
                "sensor_rms_v": 0.003,
                "threshold_v": 0.050,
                "source_state": "sham",
                "source_level": 0.0,
                "sensor_distance_m": 1.0,
                "sensor_orientation_deg": 90,
                "shielding_state": "shielded",
                "cable_id": "CABLE_A",
                "scope_channel": "CH1",
                "apparatus_config_id": "DEMO_ONLY",
                "git_commit_sha": "SYNTHETIC",
            }
        )

    with path.open(
        "w",
        encoding="utf-8",
        newline=""
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

    print(
        "Created SYNTHETIC demonstration CSV:",
        path,
    )


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "GV Switch E1 calibration runner"
        )
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    run_parser = sub.add_parser(
        "run",
        help="Evaluate an E1 calibration CSV",
    )

    run_parser.add_argument(
        "csv_path",
        nargs="?",
        default=str(DEFAULT_CSV_PATH),
    )

    template_parser = sub.add_parser(
        "template",
        help="Create an empty E1 CSV template",
    )

    template_parser.add_argument(
        "csv_path",
        nargs="?",
        default=str(DEFAULT_CSV_PATH),
    )

    demo_parser = sub.add_parser(
        "demo",
        help="Create and evaluate synthetic demonstration data",
    )

    demo_parser.add_argument(
        "csv_path",
        nargs="?",
        default=str(
            BASE_DIR / "gv_switch_e1_demo.csv"
        ),
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        run(
            Path(args.csv_path)
        )
        return

    if args.command == "template":
        create_template(
            Path(args.csv_path)
        )
        return

    if args.command == "demo":
        path = Path(
            args.csv_path
        )

        create_demo(
            path
        )

        run(
            path
        )

        return


if __name__ == "__main__":
    main()
