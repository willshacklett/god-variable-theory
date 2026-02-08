from __future__ import annotations

import csv
from pathlib import Path


INPUT = Path("data/longitudinal/summary_history.csv")
OUTPUT = Path("data/longitudinal/summary_history_binned.csv")


def classify(row: dict) -> str:
    rec = float(row.get("final_recoverability", "1.0") or 1.0)
    cum = float(row.get("final_cum_abs_dgv", "0.0") or 0.0)
    peak = float(row.get("peak_abs_ds_dt", "0.0") or 0.0)

    if rec < 0.4 and cum < 0.3 and peak < 0.001:
        return "quiet_degradation"

    if rec >= 0.6 and (cum > 0.6 or peak > 0.005):
        return "shock_recoverable"

    if 0.4 <= rec < 0.6:
        return "saturation_drift"

    return "healthy"


def main() -> None:
    if not INPUT.exists():
        raise SystemExit("Missing summary_history.csv")

    rows = []
    with INPUT.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            r = dict(r)
            r["behavior_bin"] = classify(r)
            rows.append(r)

    fieldnames = list(rows[0].keys())

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print(f"✅ Binned {len(rows)} rows → {OUTPUT}")


if __name__ == "__main__":
    main()
