"""
GV Switch E1 blocked and balanced trial manifest generator.

Purpose:
Create a balanced Phase 0 trial plan in which every major configuration
is deliberately represented before the order is randomized.

This tool does not analyze results and does not test whether GV exists.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import csv
import hashlib
import itertools
import json
import random
import time


BASE_DIR = Path(__file__).resolve().parent

DEFAULT_MANIFEST = BASE_DIR / "gv_switch_e1_blocked_manifest.csv"
DEFAULT_METADATA = BASE_DIR / "gv_switch_e1_blocked_manifest_metadata.json"


FIELDS = [
    "trial_id",
    "block_id",
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


DISTANCES = [
    0.25,
    0.50,
    1.00,
    2.00,
]

ORIENTATIONS = [
    0,
    90,
    180,
]

SHIELDING_STATES = [
    "unshielded",
    "partial",
    "strong",
]

CABLES = [
    "CABLE_A",
    "CABLE_B",
]

CHANNELS = [
    "CH1",
    "CH2",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def save_json(path: Path, payload):
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def configuration_space():
    return list(
        itertools.product(
            DISTANCES,
            ORIENTATIONS,
            SHIELDING_STATES,
            CABLES,
            CHANNELS,
        )
    )


def build_block(
    block_number: int,
    seed: int,
    apparatus_config_id: str,
):
    rows = []

    configs = configuration_space()

    for index, (
        distance,
        orientation,
        shielding,
        cable,
        channel,
    ) in enumerate(configs, start=1):

        block_id = f"B{block_number:03d}-{index:03d}"

        rows.append(
            {
                "block_id": block_id,
                "active_or_sham": "active",
                "sensor_distance_m": distance,
                "sensor_orientation_deg": orientation,
                "shielding_state": shielding,
                "cable_id": cable,
                "scope_channel": channel,
                "source_level": 1.0,
                "apparatus_config_id": apparatus_config_id,
                "randomization_seed": seed,
            }
        )

        rows.append(
            {
                "block_id": block_id,
                "active_or_sham": "sham",
                "sensor_distance_m": distance,
                "sensor_orientation_deg": orientation,
                "shielding_state": shielding,
                "cable_id": cable,
                "scope_channel": channel,
                "source_level": 0.0,
                "apparatus_config_id": apparatus_config_id,
                "randomization_seed": seed,
            }
        )

    return rows


def generate_manifest(
    output_path: Path,
    metadata_path: Path,
    seed: int,
    repeats: int,
    apparatus_config_id: str,
):
    rng = random.Random(seed)

    all_rows = []

    for block_number in range(
        1,
        repeats + 1,
    ):
        block_rows = build_block(
            block_number=block_number,
            seed=seed,
            apparatus_config_id=apparatus_config_id,
        )

        rng.shuffle(block_rows)

        all_rows.extend(block_rows)

    rng.shuffle(all_rows)

    for trial_number, row in enumerate(
        all_rows,
        start=1,
    ):
        row["trial_id"] = f"E1-{trial_number:05d}"

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
        writer.writerows(all_rows)

    digest = sha256_file(output_path)

    configs_per_block = len(
        configuration_space()
    )

    trials_per_block = configs_per_block * 2

    active = sum(
        1
        for row in all_rows
        if row["active_or_sham"] == "active"
    )

    sham = sum(
        1
        for row in all_rows
        if row["active_or_sham"] == "sham"
    )

    metadata = {
        "protocol": "GV-SWITCH",
        "phase": 0,
        "prototype": "E1",
        "document": "blocked_balanced_trial_manifest",
        "created_unix_time": time.time(),
        "seed": seed,
        "repeats": repeats,
        "configurations_per_block": configs_per_block,
        "trials_per_block": trials_per_block,
        "active_trials": active,
        "sham_trials": sham,
        "total_trials": len(all_rows),
        "apparatus_config_id": apparatus_config_id,
        "manifest_file": str(output_path),
        "manifest_sha256": digest,
        "design": {
            "distances_m": DISTANCES,
            "orientations_deg": ORIENTATIONS,
            "shielding_states": SHIELDING_STATES,
            "cables": CABLES,
            "scope_channels": CHANNELS,
            "paired_active_sham_per_configuration": True,
        },
        "warning": (
            "This file defines a balanced randomized trial plan before "
            "measurement. It contains no hardware results and is not "
            "evidence for GV."
        ),
    }

    save_json(
        metadata_path,
        metadata,
    )

    print()
    print("=" * 72)
    print("GV SWITCH E1 BLOCKED MANIFEST")
    print("=" * 72)
    print("Seed:", seed)
    print("Repeats:", repeats)
    print(
        "Configurations per block:",
        configs_per_block,
    )
    print(
        "Trials per block:",
        trials_per_block,
    )
    print(
        "Active trials:",
        active,
    )
    print(
        "Sham trials:",
        sham,
    )
    print(
        "Total trials:",
        len(all_rows),
    )
    print(
        "Manifest:",
        output_path,
    )
    print(
        "Metadata:",
        metadata_path,
    )
    print(
        "SHA256:",
        digest,
    )
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

    configs = {}

    for row in rows:
        key = (
            row["sensor_distance_m"],
            row["sensor_orientation_deg"],
            row["shielding_state"],
            row["cable_id"],
            row["scope_channel"],
        )

        configs.setdefault(
            key,
            {
                "active": 0,
                "sham": 0,
            },
        )

        configs[key][
            row["active_or_sham"]
        ] += 1

    imbalanced = []

    for key, counts in configs.items():
        if counts["active"] != counts["sham"]:
            imbalanced.append(
                {
                    "configuration": key,
                    "counts": counts,
                }
            )

    print()
    print("=" * 72)
    print("BLOCKED MANIFEST INSPECTION")
    print("=" * 72)

    print(
        "Trials:",
        len(rows),
    )

    print(
        "Active:",
        active,
    )

    print(
        "Sham:",
        sham,
    )

    print(
        "Unique configurations:",
        len(configs),
    )

    print(
        "Imbalanced configurations:",
        len(imbalanced),
    )

    print(
        "SHA256:",
        sha256_file(path),
    )

    if imbalanced:
        print()
        print(
            "WARNING: Some configurations are not balanced."
        )

    else:
        print()
        print(
            "BALANCE CHECK: PASS"
        )

    print()


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Generate blocked and balanced "
            "GV Switch E1 trial manifests."
        )
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    generate = sub.add_parser(
        "generate",
        help="Generate balanced randomized manifest",
    )

    generate.add_argument(
        "--seed",
        type=int,
        required=True,
    )

    generate.add_argument(
        "--repeats",
        type=int,
        default=1,
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
        help="Inspect balance of an existing manifest",
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
            repeats=args.repeats,
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
