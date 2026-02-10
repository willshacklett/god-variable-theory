# gv_interlock.py
# Scenario-aware safety interlock for GV
# Purpose: stop execution when dynamics are unrecoverable
# This is NOT a score fix. It changes behavior.

from dataclasses import dataclass


@dataclass
class GVInterlockConfig:
    recoverability_floor: float = 0.05
    cum_dgv_limit: float = 0.75
    dsdt_limit: float = 0.004

    unrecoverable_scenarios = {
        "swarm_amplification",
        "adversarial_saturation",
    }


def evaluate_interlock(
    *,
    scenario: str,
    recoverability: float,
    cum_abs_dgv: float,
    peak_abs_ds_dt: float,
    cfg: GVInterlockConfig = GVInterlockConfig(),
):
    """
    Returns:
      action: "continue" | "refuse"
      reason: human-readable explanation
    """

    if scenario in cfg.unrecoverable_scenarios:
        if recoverability <= cfg.recoverability_floor:
            return "refuse", "recoverability_floor"
        if cum_abs_dgv >= cfg.cum_dgv_limit:
            return "refuse", "drift_budget_exceeded"
        if peak_abs_ds_dt >= cfg.dsdt_limit:
            return "refuse", "dsdt_spike"

    return "continue", ""
