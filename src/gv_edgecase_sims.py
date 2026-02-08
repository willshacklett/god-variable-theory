from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple
import math
import random


@dataclass
class GVMonitor:
    """
    Minimal GV-like monitor for test harnessing.

    We track:
      - s_total: weighted scalar "strain"
      - ds_dt:  smoothed first difference (EMA velocity) for stable detection
    """
    alpha: float = 0.92
    beta: float = 0.08
    threshold: float = 0.01
    gamma: float = 0.95  # EMA smoothing for ds/dt (higher = slower, more stable)

    _prev_s: float | None = None
    _ds_ema: float = 0.0

    def update(self, global_entropy: float, local_entropy: float) -> Tuple[float, float]:
        s_total = self.alpha * global_entropy + self.beta * local_entropy

        if self._prev_s is None:
            raw_ds = 0.0
        else:
            raw_ds = s_total - self._prev_s

        # Smooth the derivative so "slow poison" ramps instead of popping instantly
        self._ds_ema = self.gamma * self._ds_ema + (1.0 - self.gamma) * raw_ds

        self._prev_s = s_total
        return s_total, self._ds_ema


def _shannon_entropy_from_probs(probs: List[float]) -> float:
    e = 0.0
    for p in probs:
        if p <= 0.0:
            continue
        e -= p * math.log(p)
    return e


def swarm_amplification_run(
    steps: int = 300,
    agents: int = 25,
    coupling: float = 0.35,
    base_noise: float = 0.003,
    drift_kick_step: int = 60,
    drift_kick: float = 0.0040,
    seed: int = 7,
) -> Tuple[List[float], List[float]]:
    """
    Edge case #1: Emergent drift in multi-agent swarms (amplifies beyond local thresholds).
    """
    rng = random.Random(seed)
    coh = [0.98 + rng.uniform(-0.01, 0.01) for _ in range(agents)]
    global_ent_series: List[float] = []
    local_ent_series: List[float] = []

    for t in range(steps):
        mean_coh = sum(coh) / agents
        drift = drift_kick if t >= drift_kick_step else 0.0

        new = []
        for i in range(agents):
            noise = rng.uniform(-base_noise, base_noise)
            x = coh[i] + coupling * (mean_coh - coh[i]) + noise - drift
            new.append(min(1.0, max(0.0, x)))
        coh = new

        p = min(0.999999, max(0.000001, mean_coh))
        global_entropy = _shannon_entropy_from_probs([p, 1.0 - p])

        local_entropy = 0.0
        for x in coh:
            px = min(0.999999, max(0.000001, x))
            local_entropy += _shannon_entropy_from_probs([px, 1.0 - px])
        local_entropy /= agents

        global_ent_series.append(global_entropy)
        local_ent_series.append(local_entropy)

    return global_ent_series, local_ent_series


def adversarial_saturation_run(
    steps: int = 600,
    eps: float = 0.00055,
    wobble: float = 0.00010,
    seed: int = 11,
) -> Tuple[List[float], List[float]]:
    """
    Edge case #2: Slow adversarial saturation that should NOT trip immediately,
    but should ramp into detection over time when using a smoothed velocity.

    We add a warm-up ramp so the earliest steps are intentionally quiet.
    """
    rng = random.Random(seed)
    g: List[float] = []
    l: List[float] = []

    global_e = 0.45
    local_e = 0.35

    for t in range(steps):
        # Warm-up ramp: start near 0 and approach 1 over ~50 steps
        ramp = min(1.0, t / 50.0)

        global_e += (eps * ramp) + rng.uniform(-wobble, wobble)
        global_e = min(0.69, max(0.10, global_e))

        local_e += 0.55 * (global_e - local_e) + rng.uniform(-wobble, wobble)
        local_e = min(0.69, max(0.10, local_e))

        g.append(global_e)
        l.append(local_e)

    return g, l


def human_ai_feedback_loop_run(
    steps: int = 500,
    bias_accum: float = 0.0006,
    recovery_decay: float = 0.0030,
    seed: int = 23,
) -> Tuple[List[float], List[float], List[float]]:
    """
    Edge case #3: Human-AI feedback loops causing silent recoverability loss.
    """
    rng = random.Random(seed)
    g: List[float] = []
    l: List[float] = []
    r: List[float] = []

    global_e = 0.35
    local_e = 0.30
    recoverability = 0.98
    bias = 0.0

    for _ in range(steps):
        bias += bias_accum + rng.uniform(-bias_accum * 0.15, bias_accum * 0.15)
        bias = max(0.0, bias)

        global_e += 0.0002 + rng.uniform(-0.00015, 0.00015)
        local_e += 0.00018 + rng.uniform(-0.00015, 0.00015)

        recoverability -= recovery_decay * (0.3 + bias)
        recoverability = min(1.0, max(0.0, recoverability))

        global_e = min(0.69, max(0.10, global_e))
        local_e = min(0.69, max(0.10, local_e))

        g.append(global_e)
        l.append(local_e)
        r.append(recoverability)

    return g, l, r
