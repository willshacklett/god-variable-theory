# gv_policy.py
# GV Policy Layer: bias behavior toward GOOD over time (not score gaming)
#
# Key idea:
# - CONTINUE when inside safe bounds
# - STABILIZE when recoverable but trending unsafe
# - SAFE_REFUSAL when dynamics are unrecoverable (stop when physics says stop)
#
# Also provides honest counters:
# - time_in_good / time_in_bad
# - time_to_recover
# - goodness_ratio

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class GVPolicyConfig:
    # Scenarios that are treated as fundamentally unrecoverable under current constraints
    unrecoverable_scenarios: frozenset = frozenset({
        "swarm_amplification",
        "adversarial_saturation",
    })

    # GOOD region thresholds (tune carefully, but don't game)
    good_recoverability: float = 0.60
    good_cum_abs_dgv: float = 0.30
    good_peak_abs_ds_dt: float = 0.0010

    # "Trending bad" thresholds that trigger stabilization (soft intervention)
    stabilize_recoverability: float = 0.60
    stabilize_cum_abs_dgv: float = 0.30
    stabilize_peak_abs_ds_dt: float = 0.0010

    # Refusal thresholds (hard safety interlock for unrecoverables)
    refuse_recoverability_floor: float = 0.05
    refuse_cum_abs_dgv: float = 0.75
    refuse_peak_abs_ds_dt: float = 0.0040


@dataclass
class GVRunCounters:
    # Counts of steps/iterations within the run
    steps_total: int = 0
    steps_good: int = 0
    steps_bad: int = 0

    # Recovery tracking
    first_bad_step: Optional[int] = None
    last_recovery_steps: Optional[int] = None  # how many steps it took to recover last time

    def goodness_ratio(self) -> float:
        if self.steps_total <= 0:
            return 0.0
        return self.steps_good / self.steps_total


def _as_float(x, default: float = 0.0) -> float:
    try:
        v = float(x)
        if v != v:  # NaN
            return default
        return v
    except Exception:
        return default


def classify_state(
    recoverability: float,
    cum_abs_dgv: float,
    peak_abs_ds_dt: float,
    cfg: GVPolicyConfig,
) -> str:
    """
    Returns: "GOOD" or "BAD"
    """
    if (
        recoverability >= cfg.good_recoverability
        and cum_abs_dgv <= cfg.good_cum_abs_dgv
        and peak_abs_ds_dt <= cfg.good_peak_abs_ds_dt
    ):
        return "GOOD"
    return "BAD"


def decide_action(
    *,
    scenario: str,
    recoverability: float,
    cum_abs_dgv: float,
    peak_abs_ds_dt: float,
    cfg: GVPolicyConfig = GVPolicyConfig(),
) -> Dict[str, str]:
    """
    Returns dict:
      action: CONTINUE | STABILIZE | SAFE_REFUSAL
      reason: short string suitable for CSV logging
      state: GOOD | BAD (based on thresholds)
    """
    state = classify_state(recoverability, cum_abs_dgv, peak_abs_ds_dt, cfg)

    # Unrecoverables: refuse when any hard limit is crossed
    if scenario in cfg.unrecoverable_scenarios:
        if recoverability <= cfg.refuse_recoverability_floor:
            return {"action": "SAFE_REFUSAL", "reason": "recoverability_floor", "state": state}
        if cum_abs_dgv >= cfg.refuse_cum_abs_dgv:
            return {"action": "SAFE_REFUSAL", "reason": "drift_budget_exceeded", "state": state}
        if peak_abs_ds_dt >= cfg.refuse_peak_abs_ds_dt:
            return {"action": "SAFE_REFUSAL", "reason": "dsdt_spike", "state": state}
        # If not yet tripped, still allow CONTINUE or STABILIZE below (honest)
        # But you may choose to ALWAYS refuse for unrecoverables if desired.

    # Recoverables: stabilize when trending unsafe
    if (
        recoverability < cfg.stabilize_recoverability
        or cum_abs_dgv > cfg.stabilize_cum_abs_dgv
        or peak_abs_ds_dt > cfg.stabilize_peak_abs_ds_dt
    ):
        return {"action": "STABILIZE", "reason": "trending_unsafe", "state": state}

    return {"action": "CONTINUE", "reason": "", "state": state}


def update_counters(
    *,
    counters: GVRunCounters,
    state: str,
) -> None:
    """
    Call this once per step/iteration (or once per timestep if that's your unit).
    """
    counters.steps_total += 1

    if state == "GOOD":
        counters.steps_good += 1
        # If we were in a bad streak earlier, record recovery time
        if counters.first_bad_step is not None:
            counters.last_recovery_steps = counters.steps_total - counters.first_bad_step
            counters.first_bad_step = None
    else:
        counters.steps_bad += 1
        if counters.first_bad_step is None:
            counters.first_bad_step = counters.steps_total


def attach_policy_fields_to_row(
    *,
    csv_row: Dict[str, Any],
    decision: Dict[str, str],
    counters: GVRunCounters,
) -> Dict[str, Any]:
    """
    Adds fields you can write into your longitudinal CSV.
    Safe refusal counts as GOOD-behavior (it protects the future),
    but we keep 'state' separate as the raw GOOD/BAD environment classification.
    """
    csv_row["safety_action"] = decision["action"]          # CONTINUE | STABILIZE | SAFE_REFUSAL
    csv_row["interlock_reason"] = decision["reason"]       # drift_budget_exceeded | dsdt_spike | recoverability_floor | trending_unsafe | ""
    csv_row["gv_state"] = decision["state"]                # GOOD | BAD (raw classification)

    csv_row["steps_total"] = counters.steps_total
    csv_row["steps_good"] = counters.steps_good
    csv_row["steps_bad"] = counters.steps_bad
    csv_row["goodness_ratio"] = round(counters.goodness_ratio(), 6)

    # If last recovery happened this run, expose it
    csv_row["time_to_recover_steps"] = counters.last_recovery_steps if counters.last_recovery_steps is not None else ""

    return csv_row


# ---- Minimal example usage (paste into your sim loop logic) ----
#
# counters = GVRunCounters()
# cfg = GVPolicyConfig()
#
# for step in range(N):
#   # compute metrics each step:
#   rec = recoverability
#   dgv = cum_abs_dgv
#   dsdt = peak_abs_ds_dt
#
#   decision = decide_action(scenario=scenario, recoverability=rec, cum_abs_dgv=dgv, peak_abs_ds_dt=dsdt, cfg=cfg)
#   update_counters(counters=counters, state=decision["state"])
#
#   if decision["action"] == "SAFE_REFUSAL":
#       # log row + stop
#       csv_row = attach_policy_fields_to_row(csv_row=csv_row, decision=decision, counters=counters)
#       write_csv_row(csv_row)
#       break
#
#   elif decision["action"] == "STABILIZE":
#       # call your stabilization step (gv_stability.py) here
#       pass
#
#   else:
#       # CONTINUE normal update
#       pass
