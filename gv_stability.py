# gv_stability.py
# Minimal stability layer for GV dynamics:
# - adaptive damping on ds/dt (prevents explosive spikes)
# - adaptive attractor pull-back (re-enters stable basin)
# - hard cap / interlock when "irreversibility" conditions are met
#
# This is NOT score-tuning. This changes internal dynamics so recovery is possible.

from __future__ import annotations
from dataclasses import dataclass
import math


@dataclass
class GVStabilityConfig:
  # Damping: stronger => more suppression of large |ds_dt|
  damping_lambda: float = 30.0

  # Attractor pull: stronger => more "way home"
  attractor_k: float = 0.35

  # Strain threshold where stabilizers begin to engage (0..1 scale typical)
  strain_on: float = 0.55

  # Irreversibility guardrail triggers (truthful interlock)
  # If ds_dt spikes beyond this, we clamp ds_dt_effective to avoid basin escape
  dsdt_hard_cap: float = 0.0030

  # If cum_abs_dgv crosses this, attractor + damping go max effort
  cum_dgv_critical: float = 0.75

  # If recoverability drops below this, treat as emergency stabilization
  recoverability_critical: float = 0.35


def clamp(x: float, lo: float, hi: float) -> float:
  return max(lo, min(hi, x))


def smoothstep(x: float) -> float:
  # 0..1 -> smooth 0..1
  x = clamp(x, 0.0, 1.0)
  return x * x * (3 - 2 * x)


def adaptive_gain(
  strain: float,
  recoverability: float,
  cum_abs_dgv: float,
  cfg: GVStabilityConfig,
) -> float:
  """
  Returns 0..1 "engagement" gain.
  Engages when strain is high, recoverability is low, or cum drift is high.
  """
  s = smoothstep((strain - cfg.strain_on) / max(1e-9, (1.0 - cfg.strain_on)))
  r = smoothstep((cfg.recoverability_critical - recoverability) / max(1e-9, cfg.recoverability_critical))
  d = smoothstep((cum_abs_dgv - cfg.cum_dgv_critical) / max(1e-9, (1.0 - cfg.cum_dgv_critical)))
  # Combine (any of them can engage), but cap to 1
  return clamp(0.55 * s + 0.30 * r + 0.30 * d, 0.0, 1.0)


def damp_ds_dt(ds_dt: float, gain: float, cfg: GVStabilityConfig) -> float:
  """
  Adaptive damping: ds_dt_eff = ds_dt / (1 + λ*gain*|ds_dt|)
  This prevents runaway spikes from ejecting the system from stable basins.
  """
  lam = cfg.damping_lambda * gain
  denom = 1.0 + lam * abs(ds_dt)
  if denom <= 1e-9:
    return 0.0
  ds_eff = ds_dt / denom

  # Hard cap safety (only if we're in emergency gain)
  if gain > 0.65 and abs(ds_eff) > cfg.dsdt_hard_cap:
    ds_eff = math.copysign(cfg.dsdt_hard_cap, ds_eff)
  return ds_eff


def attractor_pull(
  s_total: float,
  s_target: float,
  gain: float,
  cfg: GVStabilityConfig
) -> float:
  """
  Adds a stabilizing pull-back term that guides s_total toward s_target.
  Without this, escaped loops may never re-enter a stable basin.
  """
  k = cfg.attractor_k * gain
  return -k * (s_total - s_target)


def step_stabilized(
  *,
  s_total: float,
  ds_dt: float,
  s_target: float,
  dt: float,
  strain: float,
  recoverability: float,
  cum_abs_dgv: float,
  cfg: GVStabilityConfig = GVStabilityConfig(),
) -> dict:
  """
  Returns a dict with:
    - ds_dt_effective
    - attractor_term
    - s_total_next
    - gain
  """
  gain = adaptive_gain(strain, recoverability, cum_abs_dgv, cfg)
  ds_eff = damp_ds_dt(ds_dt, gain, cfg)
  pull = attractor_pull(s_total, s_target, gain, cfg)

  # New stabilized update:
  s_next = s_total + dt * (ds_eff + pull)

  return {
    "gain": gain,
    "ds_dt_effective": ds_eff,
    "attractor_term": pull,
    "s_total_next": s_next,
  }
