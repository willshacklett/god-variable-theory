from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import secrets
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.gv_physical_program import (
    SCENARIOS, WARNING, fit_model, inspect_run, load_raw, lock_threshold,
    manifest, mock_run, save_raw, summarize_results, write_json_new,
)


def calibration_records(stage, seed, scenarios):
    for block in range(5):
        public, _ = manifest(stage, seed, block)
        for index, event in enumerate(public["assignments"]):
            yield mock_run(event, scenarios[index % len(scenarios)], seed + block * 1000 + index)


def dry_run(directory: Path, seed: int) -> dict:
    directory.mkdir(parents=True, exist_ok=False)
    known = ["null", "electrical", "em", "vibration", "acoustic", "thermal", "environmental", "overlap"]
    model = fit_model(calibration_records("model_calibration", seed, known))
    threshold = lock_threshold(calibration_records("threshold_calibration", seed + 1, ["sham"]), model)
    write_json_new(directory / "model.json", model)
    write_json_new(directory / "threshold.json", threshold)
    public, private = manifest("engineering", seed + 2)
    public["assignments"] = public["assignments"][:len(SCENARIOS)]
    private["assignments"] = private["assignments"][:len(SCENARIOS)]
    digest = write_json_new(directory / "manifest.json", public)
    write_json_new(directory / "operator_key.json", private)
    (directory / "operator_key.json").chmod(0o600)
    expected = {
        "timing": "TIMING ARTIFACT", "electrical": "ELECTRICAL TRANSIENT",
        "em": "KNOWN EM", "vibration": "KNOWN MECHANICAL", "acoustic": "KNOWN ACOUSTIC",
        "thermal": "KNOWN THERMAL", "environmental": "KNOWN ENVIRONMENTAL",
        "software": "SOFTWARE ARTIFACT", "overlap": "MULTIPLE KNOWN CAUSES",
        "sham": "NULL", "null": "NULL", "unknown": "UNEXPLAINED PROPAGATION CANDIDATE",
    }
    results, checks = [], []
    for index, (event, scenario) in enumerate(zip(public["assignments"], SCENARIOS)):
        metadata, samples = mock_run(event, scenario, seed + index + 10000, digest)
        raw_dir = directory / "raw" / event["run_id"]
        save_raw(raw_dir, metadata, samples)
        result = inspect_run(metadata, samples, model, threshold)
        results.append(result)
        checks.append({"scenario": scenario, "expected": expected[scenario],
                       "actual": result["classification"], "passed": result["classification"] == expected[scenario]})
    summary = summarize_results(results, private)
    summary.update(pipeline_checks=checks, model_calibration_count=len(model["training_ids"]),
                   threshold_calibration_count=len(threshold["calibration_ids"]),
                   dataset_origin="synthetic", analysis_sha256=hashlib.sha256((ROOT / "src/gv_physical_program.py").read_bytes()).hexdigest())
    write_json_new(directory / "analysis.json", {"warning": WARNING, "results": results})
    write_json_new(directory / "summary.json", summary)
    print(WARNING)
    for check in checks:
        print(f"{'PASS' if check['passed'] else 'FAIL'} {check['scenario']}: {check['actual']}")
    print(f"Calibration: {summary['model_calibration_count']} model + {summary['threshold_calibration_count']} threshold events")
    print(f"Summary: {directory / 'summary.json'}; physical_evidence=False")
    if not all(check["passed"] for check in checks):
        raise RuntimeError("Synthetic pipeline classification mismatch; do not alter scientific thresholds to obtain green")
    return summary


def main():
    parser = argparse.ArgumentParser(description="GV-PHY-001 prospective software, no physical driver")
    commands = parser.add_subparsers(dest="command", required=True)
    mock = commands.add_parser("dry-run")
    mock.add_argument("--out", type=Path, required=True)
    mock.add_argument("--seed", type=int, default=42)
    make_manifest = commands.add_parser("manifest")
    make_manifest.add_argument("--stage", choices=["engineering", "model_calibration", "threshold_calibration", "evaluation", "replication"], required=True)
    make_manifest.add_argument("--block", type=int, default=0)
    make_manifest.add_argument("--seed", type=int)
    make_manifest.add_argument("--public-out", type=Path, required=True)
    make_manifest.add_argument("--private-out", type=Path, required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("raw_directory", type=Path)
    score = commands.add_parser("score")
    for option in ("manifest", "model", "threshold", "raw-root", "out"):
        score.add_argument("--" + option, type=Path, required=True)
    summary = commands.add_parser("summarize")
    for option in ("analysis", "operator-key", "out"):
        summary.add_argument("--" + option, type=Path, required=True)
    args = parser.parse_args()
    if args.command == "dry-run":
        dry_run(args.out, args.seed)
    elif args.command == "manifest":
        if args.public_out.resolve() == args.private_out.resolve():
            raise ValueError("Public manifest and operator key must be different files")
        if args.public_out.exists() or args.private_out.exists():
            raise FileExistsError("Refusing to overwrite either manifest or operator key")
        seed = secrets.randbits(128) if args.seed is None else args.seed
        public, private = manifest(args.stage, seed, args.block)
        digest = write_json_new(args.public_out, public)
        write_json_new(args.private_out, private)
        args.private_out.chmod(0o600)
        print(f"Prospective manifest: {len(public['assignments'])} events; SHA256 {digest}")
        print("Keep operator key/seed separate from analysts. This is not an acquisition record.")
    elif args.command == "score":
        public = json.loads(args.manifest.read_text())
        model = json.loads(args.model.read_text())
        threshold = json.loads(args.threshold.read_text())
        digest = hashlib.sha256(args.manifest.read_bytes()).hexdigest()
        results = []
        for event in public["assignments"]:
            metadata, samples = load_raw(args.raw_root / event["run_id"], validate=False)
            if (metadata["run_id"] != event["run_id"] or metadata["blind_label"] != event["blind_label"]
                    or metadata["manifest_sha256"] != digest):
                raise ValueError("Raw/manifest identity mismatch")
            results.append(inspect_run(metadata, samples, model, threshold))
        write_json_new(args.out, {"warning": "Screening only; inspect origins", "results": results})
        print("Blinded per-run scoring saved before operator key is loaded; no physical verdict")
    elif args.command == "summarize":
        analysis = json.loads(args.analysis.read_text())
        private = json.loads(args.operator_key.read_text())
        write_json_new(args.out, summarize_results(analysis["results"], private))
        print("Unblinded mock summary; physical conclusion issuance is not implemented")
    else:
        metadata, _ = load_raw(args.raw_directory)
        print(f"VALID schema/hash: {metadata['run_id']}; origin={metadata['origin']}; not a physical-control certification")


if __name__ == "__main__":
    main()