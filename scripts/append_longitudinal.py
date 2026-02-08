#!/usr/bin/env python3
from __future__ import annotations

import csv
import os
from datetime import datetime, timezone


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def read_csv(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def append_rows(path: str, rows: list[dict]) -> None:
    if not rows:
        return

    # Build union header (robust to new columns later)
    existing_rows: list[dict] = []
    if os.path.exists(path):
        existing_rows = read_csv(path)

    fieldnames = sorted({k for r in (existing_rows + rows) for k in r.keys()})

    # Rewrite whole file (simple + safe)
    ensure_dir(os.path.dirname(path))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in existing_rows:
            w.writerow(r)
        for r in rows:
            w.writerow(r)


def main() -> None:
    metrics_dir = os.environ.get("GV_CI_METRICS_DIR", "artifacts/ci_metrics")
    summary_in = os.path.join(metrics_dir, "summary.csv")

    if not os.path.exists(summary_in):
        raise SystemExit(f"Missing {summary_in}. Run collect_ci_metrics.py first.")

    # GitHub-provided metadata (works in Actions; harmless locally)
    sha = os.environ.get("GITHUB_SHA", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    run_number = os.environ.get("GITHUB_RUN_NUMBER", "")
    ref_name = os.environ.get("GITHUB_REF_NAME", "")
    created_utc = datetime.now(timezone.utc).isoformat()

    rows = read_csv(summary_in)

    # Stamp each scenario row with run metadata
    stamped: list[dict] = []
    for r in rows:
        r2 = dict(r)
        r2["run_created_utc"] = created_utc
        r2["run_id"] = run_id
        r2["run_number"] = run_number
        r2["git_sha"] = sha
        r2["ref_name"] = ref_name
        stamped.append(r2)

    out_path = "data/longitudinal/summary_history.csv"
    append_rows(out_path, stamped)
    print(f"✅ Appended {len(stamped)} rows to {out_path}")


if __name__ == "__main__":
    main()
