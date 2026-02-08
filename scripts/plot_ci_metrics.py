#!/usr/bin/env python3
from __future__ import annotations

import csv
import os

import matplotlib.pyplot as plt


def read_csv(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def to_float(xs: list[str]) -> list[float]:
    return [float(x) for x in xs]


def main() -> None:
    metrics_dir = os.environ.get("GV_CI_METRICS_DIR", "artifacts/ci_metrics")
    out_dir = os.path.join(metrics_dir, "plots")
    ensure_dir(out_dir)

    # Primary curve Grok asked for: recoverability vs cumulative |ΔGv|
    fb_path = os.path.join(metrics_dir, "human_ai_feedback_loop.csv")
    rows = read_csv(fb_path)

    x = to_float([r["cum_abs_dgv"] for r in rows])
    y = to_float([r["recoverability"] for r in rows])

    plt.figure()
    plt.plot(x, y)
    plt.xlabel("Cumulative |ΔGv|")
    plt.ylabel("Recoverability (R)")
    plt.title("Recoverability vs Cumulative |ΔGv| (Human–AI Feedback Loop)")
    out_path = os.path.join(out_dir, "recoverability_vs_cum_abs_dgv.png")
    plt.savefig(out_path, dpi=180, bbox_inches="tight")

    # Also save a simple time plot (optional but useful)
    t = to_float([r["t"] for r in rows])
    plt.figure()
    plt.plot(t, y)
    plt.xlabel("t (step)")
    plt.ylabel("Recoverability (R)")
    plt.title("Recoverability over Time (Human–AI Feedback Loop)")
    out_path2 = os.path.join(out_dir, "recoverability_over_time.png")
    plt.savefig(out_path2, dpi=180, bbox_inches="tight")

    print(f"✅ Wrote plots to: {out_dir}")
    print(f" - {out_path}")
    print(f" - {out_path2}")


if __name__ == "__main__":
    main()
