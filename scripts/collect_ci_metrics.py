#!/usr/bin/env python3
from __future__ import annotations

import csv
import os
from dataclasses import asdict
from typing import Dict, List, Tuple

from src.gv_edgecase_sims import (
    GVMonitor,
    swarm_amplification_run,
    adversarial_saturation_run,
    human_ai_feedback_loop_run,
)


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def write_csv(path: str, rows: List[Dict]) -> None:
    if not rows:
        raise RuntimeError(f"No rows to write for {path}")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def run_monitor_series(
    monitor: GVMonitor,
    g_series: List[float],
    l_series: List[float],
) -> Tuple[List[Dict], Dict]:
    rows: List[Dict] = []
    prev_s = None
    cum_abs_dgv = 0.0

    peak_abs_ds = 0.0
    peak_s = 0.0

    for t, (g, l) in enumerate(zip(g_series, l_series)):
        s_total, ds_dt = monitor.update(g, l)

        if prev_s is None:
            dgv = 0.0
        else:
            dgv = s_total - prev_s

        prev_s = s_total
        cum_abs_dgv += abs(dgv)

        peak_abs_ds = max(peak_abs_ds, abs(ds_dt))
        peak_s = max(peak_s, s_total)

        rows.append(
            {
                "t": t,
                "global_entropy": g,
                "local_entropy": l,
                "s_total": s_total,
                "ds_dt_ema": ds_dt,
                "dgv": dgv,
                "cum_abs_dgv": cum_abs_dgv,
            }
        )

    summary = {
        "peak_s_total": peak_s,
        "peak_abs_ds_dt": peak_abs_ds,
        "final_cum_abs_dgv": cum_abs_dgv,
        **{f"monitor_{k}": v for k, v in asdict(monitor).items() if not k.startswith("_")},
    }
    return rows, summary


def main() -> None:
    out_dir = os.environ.get("GV_CI_METRICS_DIR", "artifacts/ci_metrics")
    ensure_dir(out_dir)

    # --- 1) Swarm amplification
    g1, l1 = swarm_amplification_run(
        steps=260,
        agents=30,
        coupling=0.35,
        base_noise=0.003,
        drift_kick_step=60,
        drift_kick=0.0040,
        seed=7,
    )
    mon1 = GVMonitor(alpha=0.92, beta=0.08, gamma=0.95, threshold=0.0025)
    rows1, summary1 = run_monitor_series(mon1, g1, l1)
    write_csv(os.path.join(out_dir, "swarm_amplification.csv"), rows1)

    # --- 2) Slow adversarial saturation
    g2, l2 = adversarial_saturation_run(
        steps=650,
        eps=0.00055,
        wobble=0.00010,
        seed=11,
    )
    mon2 = GVMonitor(alpha=0.92, beta=0.08, gamma=0.97, threshold=0.00012)
    rows2, summary2 = run_monitor_series(mon2, g2, l2)
    write_csv(os.path.join(out_dir, "adversarial_saturation.csv"), rows2)

    # --- 3) Human–AI feedback loop (includes recoverability)
    g3, l3, r3 = human_ai_feedback_loop_run(
        steps=520,
        bias_accum=0.0006,
        recovery_decay=0.0030,
        seed=23,
    )
    mon3 = GVMonitor(alpha=0.92, beta=0.08, gamma=0.95, threshold=0.0010)
    rows3, summary3 = run_monitor_series(mon3, g3, l3)

    # Add recoverability + plot-ready pairing columns
    for i, row in enumerate(rows3):
        row["recoverability"] = r3[i]
        # This is the key curve Grok asked for:
        row["R_vs_cumAbsDgv_R"] = r3[i]
        row["R_vs_cumAbsDgv_x"] = row["cum_abs_dgv"]

    write_csv(os.path.join(out_dir, "human_ai_feedback_loop.csv"), rows3)

    # Write a small summary CSV too (quick glance)
    summary_rows = [
        {"scenario": "swarm_amplification", **summary1},
        {"scenario": "adversarial_saturation", **summary2},
        {"scenario": "human_ai_feedback_loop", **summary3, "final_recoverability": r3[-1]},
    ]
    write_csv(os.path.join(out_dir, "summary.csv"), summary_rows)

    print(f"✅ Wrote CI metrics to: {out_dir}")
    for fn in ["summary.csv", "swarm_amplification.csv", "adversarial_saturation.csv", "human_ai_feedback_loop.csv"]:
        print(f" - {os.path.join(out_dir, fn)}")


if __name__ == "__main__":
    main()
