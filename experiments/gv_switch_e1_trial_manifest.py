"""
GV Switch E1 randomized trial manifest generator.

Purpose:
Create a preregistered, randomized trial plan for real Phase 0
electrical-sensor calibration before any measurements are collected.

This tool does not analyze results and does not test whether GV exists.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import csv
import hashlib
import json
import random
import time


BASE_DIR = Path(__file__).resolve().parent

DEFAULT_MANIFEST = BASE_DIR / "gv_switch_e1_trial_manifest.csv"
DEFAULT_METADATA = BASE_DIR / "gv_switch_e1_trial_manifest_metadata.json"


FIELDS = [
    "trial_id",
    "active_or_sham",
    "sensor_distance_m",
    "sensor_orientation_deg",
    "shielding_state",
    "cable_id",
    "scope_channel",
    "source_level",
    "apparatus_config_id",
    "randomization_seed",
]


DEFAULT_DISTANCES = [
    0.25,
    0.50,
    1.00,
    2.00,
]

DEFAULT_ORIENTATIONS = [
    0,
    90,
    180,
]

DEFAULT_SHIELDING = [
    "unshielded",
    "partial",
    "strong",
]

DEFAULT_CABLES = [
    "CABLE_A",
    "CABLE_B",
]

DEFAULT_CHANNELS = [
    "CH1",
    "CH2",
]


def write_json(path: Path, payload):
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def sha256_file(path: Path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def generate_manifest(
    output_path: Path,
    metadata_path: Path,
    seed: int,
    active_trials: int,
    sham_trials: int,
    apparatus_config_id: str,
):
    rng = random.Random(seed)

    trial_states = (
        ["active"] * active_trials
        + ["sham"] * sham_trials
    )

    rng.shuffle(trial_states)

    rows = []

    for index, state in enumerate(
        trial_states,
        start=1,
    ):
        row = {
            "trial_id": f"E1-{index:05d}",
            "active_or_sham": state,
            "sensor_distance_m": rng.choice(
                DEFAULT_DISTANCES
            ),
            "sensor_orientation_deg": rng.choice(
                DEFAULT_ORIENTATIONS
            ),
            "shielding_state": rng.choice(
                DEFAULT_SHIELDING
            ),
            "cable_id": rng.choice(
                DEFAULT_CABLES
            ),
            "scope_channel": rng.choice(
                DEFAULT_CHANNELS
            ),
            "source_level": (
                1.0
                if state == "active"
                else 0.0
            ),
            "apparatus_config_id": apparatus_config_id,
            "randomization_seed": seed,
        }

        rows.append(row)

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=FIELDS,
        )

        writer.writeheader()
        writer.writerows(rows)

    digest = sha256_file(
        output_path
    )

    metadata = {
        "protocol": "GV-SWITCH",
        "phase": 0,
        "prototype": "E1",
        "document": "randomized_trial_manifest",
        "created_unix_time": time.time(),
        "seed": seed,
        "active_trials": active_trials,
        "sham_trials": sham_trials,
        "total_trials": len(rows),
        "apparatus_config_id": apparatus_config_id,
        "manifest_file": str(output_path),
        "manifest_sha256": digest,
        "design": {
            "distances_m": DEFAULT_DISTANCES,
            "orientations_deg": DEFAULT_ORIENTATIONS,
            "shielding_states": DEFAULT_SHIELDING,
            "cables": DEFAULT_CABLES,
            "scope_channels": DEFAULT_CHANNELS,
        },
        "warning": (
            "This file defines trial order before measurement. "
            "It contains no hardware results and is not evidence for GV."
        ),
    }

    write_json(
        metadata_path,
        metadata,
    )

    print()
    print("=" * 72)
    print("GV SWITCH E1 TRIAL MANIFEST")
    print("=" * 72)
    print("Seed:", seed)
    print("Active trials:", active_trials)
    print("Sham trials:", sham_trials)
    print("Total trials:", len(rows))
    print("Manifest:", output_path)
    print("Metadata:", metadata_path)
    print("SHA256:", digest)
    print()


def inspect_manifest(path: Path):
    if not path.exists():
        raise FileNotFoundError(
            f"Manifest not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as f:
        rows = list(
            csv.DictReader(f)
        )

    active = sum(
        1
        for row in rows
        if row["active_or_sham"] == "active"
    )

    sham = sum(
        1
        for row in rows
        if row["active_or_sham"] == "sham"
    )

    print()
    print("=" * 72)
    print("MANIFEST INSPECTION")
    print("=" * 72)
    print("Trials:", len(rows))
    print("Active:", active)
    print("Sham:", sham)
    print("SHA256:", sha256_file(path))
    print()


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Generate randomized GV Switch E1 "
            "hardware trial manifests."
        )
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    generate = sub.add_parser(
        "generate",
        help="Generate randomized trial manifest",
    )

    generate.add_argument(
        "--seed",
        type=int,
        required=True,
    )

    generate.add_argument(
        "--active",
        type=int,
        default=250,
    )

    generate.add_argument(
        "--sham",
        type=int,
        default=250,
    )

    generate.add_argument(
        "--apparatus-config",
        default="E1-PROTOTYPE-001",
    )

    generate.add_argument(
        "--output",
        default=str(DEFAULT_MANIFEST),
    )

    generate.add_argument(
        "--metadata",
        default=str(DEFAULT_METADATA),
    )

    inspect = sub.add_parser(
        "inspect",
        help="Inspect an existing manifest",
    )

    inspect.add_argument(
        "path",
        nargs="?",
        default=str(DEFAULT_MANIFEST),
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "generate":
        generate_manifest(
            output_path=Path(args.output),
            metadata_path=Path(args.metadata),
            seed=args.seed,
            active_trials=args.active,
            sham_trials=args.sham,
            apparatus_config_id=args.apparatus_config,
        )
        return

    if args.command == "inspect":
        inspect_manifest(
            Path(args.path)
        )
        return


if __name__ == "__main__":
    main()
