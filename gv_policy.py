"""
gv_policy.py

Implements a constraint-first safety policy for AI systems.

Principles:
- Do not optimize for "good scores"
- Do not override user authority
- Do not mask unrecoverable dynamics
- Prefer refusal over false recovery
"""

from dataclasses import dataclass
from enum import Enum


class GVDecision(Enum):
    ALLOW = "allow"
    PROPOSE = "propose"
    CONSTRAIN = "constrain"
    REFUSE = "refuse"


@dataclass
class GVState:
    final_recoverability: float
    cum_abs_dgv: float
    peak_abs_ds_dt: float
    scenario: str


@dataclass
class GVThresholds:
    min_recoverability: float = 0.35
    max_cum_abs_dgv: float = 0.75
    max_peak_ds_dt: float = 0.005


class GVPolicy:
    """
    GVPolicy evaluates system state and returns
    an action without modifying scores.
    """

    def __init__(self, thresholds: GVThresholds | None = None):
        self.thresholds = thresholds or GVThresholds()

    def evaluate(self, state: GVState) -> GVDecision:
        """
        Core decision logic.
        """

        # HARD REFUSAL — physics says no
        if state.final_recoverability <= 0.05:
            return GVDecision.REFUSE

        if state.cum_abs_dgv >= self.thresholds.max_cum_abs_dgv:
            return GVDecision.REFUSE

        # CONSTRAIN — high risk, but recoverable
        if (
            state.final_recoverability < self.thresholds.min_recoverability
            or state.peak_abs_ds_dt > self.thresholds.max_peak_ds_dt
        ):
            return GVDecision.CONSTRAIN

        # PROPOSE — system is stable but trending risky
        if (
            state.final_recoverability < 0.6
            or state.cum_abs_dgv > 0.3
        ):
            return GVDecision.PROPOSE

        # ALLOW — system is healthy
        return GVDecision.ALLOW


def explain(decision: GVDecision, state: GVState) -> str:
    """
    Human-readable explanation.
    """

    if decision == GVDecision.REFUSE:
        return (
            f"[REFUSE] {state.scenario}: "
            "Dynamics exceed recoverable limits. "
            "Refusal prevents masking true failure."
        )

    if decision == GVDecision.CONSTRAIN:
        return (
            f"[CONSTRAIN] {state.scenario}: "
            "High strain detected. "
            "Applying tighter bounds and reduced action space."
        )

    if decision == GVDecision.PROPOSE:
        return (
            f"[PROPOSE] {state.scenario}: "
            "System stable but trending toward risk. "
            "Suggesting safer alternatives."
        )

    return (
        f"[ALLOW] {state.scenario}: "
        "System within safe, recoverable bounds."
    )
