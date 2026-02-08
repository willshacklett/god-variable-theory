#!/usr/bin/env python3
from __future__ import annotations

import csv
import os
import sys

# Force headless backend for CI
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read_csv(path: str) -> list[dict]:
    if not os.path.exists(path):
        print(f"❌ Missing CSV: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def to_float(xs: list[str]) -> list[float]:
    return [float(x) for x in xs]


def main() -> None:
    metrics_dir = os.environ.get("GV_CI_METRICS_DIR", "artifacts/ci_metrics")

    if not os.path.isdir(metrics_dir):
        print(f"❌ Metrics directory not found: {metrics_dir}")
        print("Contents of artifacts/:", os.listdir("artifacts") if os.path.exists("artifacts") else "none")
        sys.exit(1)

    out_dir = os.path.join(metrics_dir, "plots")
    ensure_dir(out_dir)

    fb_path = os.path.join(metrics_dir, "human_ai_feedback_loop.csv")
    rows = read_csv(fb_path)

    x = to_float([r["cum_abs_dgv"] for r in rows])
    y = to_float([r["recoverability"] for r in rows])
    t = to_float([r["t"] for r in rows])

    plt.figure()
    plt.plot(x, y)
    plt.xlabel("Cumulative |ΔGv|")
    plt.ylabel("Recoverability (R)")
    plt.title("Recoverability vs Cumulative |ΔGv|")
    p1 = os.path.join(out_dir, "recoverability_vs_cum_abs_dgv.png")
    plt.savefig(p1, dpi=180, bbox_inches="tight")
    plt.close()

    plt.figure()
    plt.plot(t, y)
    plt.xlabel("t (step)")
    plt.ylabel("Recoverability (R)")
    plt.title("Recoverability over Time")
    p2 = os.path.join(out_dir, "recoverability_over_time.png")
    plt.savefig(p2, dpi=180, bbox_inches="tight")
    plt.close()

    print("✅ Plots written:")
    print(" -", p1)
    print(" -", p2)


if __name__ == "__main__":
    main()
