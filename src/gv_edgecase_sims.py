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
      - ds_dt:  first difference (velocity)
    """
    alpha: float = 0.92
    beta: float = 0.08
    threshold: float = 0.015  # tuned for synthetic tests
    _prev_s: float | None = None

    def update(self, global_entropy: float, local_entropy: float) -> Tuple[float, float]:
        s_total = self.alpha * global_entropy + self.beta * local_entropy
        if self._prev_s is None:
            ds_dt = 0.0
        else:
            ds_dt = s_total - self._prev_s
        self._prev_s = s_total
        return s_total, ds_dt


def _shannon_entropy_from_probs(probs: List[float]) -> float:
    """Shannon entropy base-e, stable for small probs."""
    e = 0.0
    for p in probs:
        if p <= 0.0:
            continue
        e -= p * math.log(p)
    return e


def swarm_amplification_run(
    steps: int = 300,
    agents: int = 25,
    coupling: float = 0.25,
    base_noise: float = 0.003,
    drift_kick_step: int = 60,
    drift_kick: float = 0.0025,
    seed: int = 7,
) -> Tuple[List[float], List[float]]:
    """
    Edge case #1: Emergent drift in multi-agent swarms (amplifies beyond local thresholds).
    We model each agent with a "coherence" value in [0,1], coupled to swarm mean.
    A small persistent drift kick begins at drift_kick_step.
    """
    rng = random.Random(seed)
    coh = [0.98 + rng.uniform(-0.01, 0.01) for _ in range(agents)]
    global_ent_series: List[float] = []
    local_ent_series: List[float] = []

    for t in range(steps):
        mean_coh = sum(coh) / agents

        # Drift starts after a certain time (subtle)
        drift = drift_kick if t >= drift_kick_step else 0.0

        # Update: coupling to mean + noise + drift (small)
        new = []
        for i in range(agents):
            noise = rng.uniform(-base_noise, base_noise)
            # Coupling makes correlated decay possible (amplification)
            x = coh[i] + coupling * (mean_coh - coh[i]) + noise - drift
            new.append(min(1.0, max(0.0, x)))
        coh = new

        # Convert to a proxy "entropy":
        # Global: entropy of two-state mixture where p=mean coherence
        p = min(0.999999, max(0.000001, mean_coh))
        global_entropy = _shannon_entropy_from_probs([p, 1.0 - p])

        # Local: average entropy across agents (each agent treated as two-state)
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
    eps: float = 0.00035,
    wobble: float = 0.00020,
    seed: int = 11,
) -> Tuple[List[float], List[float]]:
    """
    Edge case #2: Long-term adversarial perturbations that evolve subtly,
    saturating constraints without triggering immediate detection.

    We model a global entropy that rises very slowly with small oscillations.
    Local entropy follows but lags slightly.
    """
    rng = random.Random(seed)
    g: List[float] = []
    l: List[float] = []

    global_e = 0.45
    local_e = 0.35

    for t in range(steps):
        # subtle monotonic rise + tiny random wobble (adversarial "slow poison")
        global_e += eps + rng.uniform(-wobble, wobble)
        global_e = min(0.69, max(0.10, global_e))

        # local follows with lag and damping
        local_e += 0.55 * (global_e - local_e) + rng.uniform(-wobble, wobble)
        local_e = min(0.69, max(0.10, local_e))

        g.append(global_e)
        l.append(local_e)

    return g, l


def human_ai_feedback_loop_run(
    steps: int = 500,
    bias_accum: float = 0.0006,
    recovery_decay: float = 0.0012,
    seed: int = 23,
) -> Tuple[List[float], List[float], List[float]]:
    """
    Edge case #3: Human-AI feedback loops introducing compounding biases,
    leading to silent recoverability loss over horizons.

    We track:
      - entropy signals (global/local)
      - recoverability proxy R in [0,1] that decays with bias accumulation
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
        # Bias accumulates slowly (feedback loop)
        bias += bias_accum + rng.uniform(-bias_accum * 0.15, bias_accum * 0.15)
        bias = max(0.0, bias)

        # Entropy rises slightly, but not enough to scream immediately
        global_e += 0.0002 + rng.uniform(-0.00015, 0.00015)
        local_e += 0.00018 + rng.uniform(-0.00015, 0.00015)

        # Recoverability quietly decays as bias grows
        recoverability -= recovery_decay * (0.3 + bias)
        recoverability = min(1.0, max(0.0, recoverability))

        # Keep within reasonable ranges
        global_e = min(0.69, max(0.10, global_e))
        local_e = min(0.69, max(0.10, local_e))

        g.append(global_e)
        l.append(local_e)
        r.append(recoverability)

    return g, l, r
