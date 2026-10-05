from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SWITCH = {
    "clock": "KNOWN CLOCK/TIMING CHANNEL",
    "em": "KNOWN EM CHANNEL",
    "mechanical": "KNOWN ENVIRONMENTAL CHANNEL",
    "acoustic": "KNOWN ENVIRONMENTAL CHANNEL",
    "thermal": "KNOWN ENVIRONMENTAL CHANNEL",
    "gv": "UNEXPLAINED PROPAGATION CANDIDATE",
}
SMOKE = [
    ("switch_timing", "experiments/gv_switch_sim.py", "SUB-LIGHT MODEL"),
    ("switch_master", "experiments/gv_switch_master_protocol.py", "Protocol scenario score: 6/6"),
    ("ci_metrics", "scripts/collect_ci_metrics.py", "summary.csv"),
    ("ci_plots", "scripts/plot_ci_metrics.py", "recoverability_over_time.png"),
]
BENCHMARKS = [
    ("F0", "experiments/gv_fluid_instability_test.py", "NOT SUPPORTIVE"),
    ("F1", "experiments/gv_fluid_f1_burgers_test.py", "NOT SUPPORTIVE"),
    ("F1b", "experiments/gv_fluid_f1b_forced_burgers_test.py", "NOT SUPPORTIVE"),
    ("F2", "experiments/gv_fluid_f2_2d_test.py", "BENCHMARK INVALID"),
    ("F2b", "experiments/gv_fluid_f2b_2d_test.py", "OVERALL F2b: PREREGISTERED SUCCESS CRITERION NOT MET"),
]


def check_smoke_outputs(out_dir: Path) -> None:
    audit = json.loads((out_dir / "gv_switch_protocol_audit.json").read_text())
    observed = {item["model"]: item["final_verdict"] for item in audit["results"]}
    if len(audit["results"]) != 6 or observed != EXPECTED_SWITCH:
        raise RuntimeError("Synthetic switch classifications do not match the six frozen expectations")
    for filename, expected_rows in {
        "summary.csv": 3, "swarm_amplification.csv": 260,
        "adversarial_saturation.csv": 650, "human_ai_feedback_loop.csv": 520,
    }.items():
        with (out_dir / "ci_metrics" / filename).open(newline="") as handle:
            rows = list(csv.DictReader(handle))
        if len(rows) != expected_rows:
            raise RuntimeError(f"Unexpected row count for {filename}: {len(rows)}")
    for filename in ["recoverability_vs_cum_abs_dgv.png", "recoverability_over_time.png"]:
        image = out_dir / "ci_metrics" / "plots" / filename
        if not image.is_file() or image.stat().st_size < 1000:
            raise RuntimeError(f"Missing or empty plot: {filename}")


def run(mode: str) -> int:
    out_dir = ROOT / "artifacts" / "research" / mode
    out_dir.mkdir(parents=True, exist_ok=True)
    cases = SMOKE if mode == "smoke" else BENCHMARKS if mode == "benchmarks" else [
        ("legacy_cosmology", "gv_simulation.py", "not physical evidence for GV"),
    ]
    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"
    env["PYTHONPATH"] = str(ROOT)
    env["GV_CI_METRICS_DIR"] = str(out_dir / "ci_metrics")
    source_files = [*ROOT.glob("*.py"), *(ROOT / "experiments").glob("*.py"),
                    *(ROOT / "src").glob("*.py"), *(ROOT / "scripts").glob("*.py")]
    manifest = {
        "mode": mode,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "warning": "Computational reproduction only; negative results are not execution failures.",
        "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "tracked_changes": subprocess.check_output(["git", "diff", "HEAD", "--name-only"], cwd=ROOT, text=True).splitlines(),
        "source_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(source_files)},
        "python": sys.version,
        "platform": platform.platform(),
        "packages": {name: importlib.metadata.version(name) for name in ["numpy", "scipy", "matplotlib", "pytest", "requests", "networkx"]},
        "runs": [],
    }
    for name, relative_path, expected in cases:
        script = ROOT / relative_path
        command = [sys.executable, str(script)]
        completed = subprocess.run(command, cwd=out_dir, env=env, text=True, capture_output=True)
        (out_dir / f"{name}.stdout.txt").write_text(completed.stdout)
        (out_dir / f"{name}.stderr.txt").write_text(completed.stderr)
        passed = completed.returncode == 0 and expected in completed.stdout
        manifest["runs"].append({
            "name": name, "script": relative_path, "command": command,
            "sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "returncode": completed.returncode, "expected_output": expected, "passed": passed,
        })
        print(f"{'PASS' if passed else 'FAIL'} {name}; output: {out_dir / (name + '.stdout.txt')}", flush=True)
    if mode == "smoke" and all(item["passed"] for item in manifest["runs"]):
        try:
            check_smoke_outputs(out_dir)
            manifest["artifact_checks"] = "PASS: 6 scenario verdicts, 4 CSV row counts, 2 nonempty plots"
        except (OSError, ValueError, KeyError, RuntimeError) as error:
            manifest["artifact_checks"] = f"FAIL: {error}"
    (out_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    success = all(item["passed"] for item in manifest["runs"])
    if mode == "smoke":
        success = success and manifest.get("artifact_checks", "FAIL").startswith("PASS")
    print(f"{'PASS' if success else 'FAIL'} {mode}: {len(cases)} commands; manifest: {out_dir / 'run_manifest.json'}")
    return 0 if success else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Reproduce computational research without overwriting historical evidence")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--smoke", action="store_true")
    group.add_argument("--benchmarks", action="store_true")
    group.add_argument("--legacy", action="store_true")
    args = parser.parse_args()
    return run("smoke" if args.smoke else "benchmarks" if args.benchmarks else "legacy")


if __name__ == "__main__":
    raise SystemExit(main())