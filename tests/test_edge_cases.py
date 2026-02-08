from __future__ import annotations

from src.gv_edgecase_sims import (
    GVMonitor,
    swarm_amplification_run,
    adversarial_saturation_run,
    human_ai_feedback_loop_run,
)


def _first_trigger_step(monitor: GVMonitor, g_series, l_series) -> int | None:
    for i, (g, l) in enumerate(zip(g_series, l_series)):
        _, ds_dt = monitor.update(g, l)
        if abs(ds_dt) > monitor.threshold:
            return i
    return None


def test_swarm_amplification_triggers_after_drift_kick():
    """
    We expect: before drift_kick_step, ds_dt stays mostly quiet.
    After drift_kick_step, coupling amplifies and ds_dt eventually exceeds threshold.
    """
    g, l = swarm_amplification_run(
        steps=260,
        agents=30,
        coupling=0.35,
        base_noise=0.003,
        drift_kick_step=60,
        drift_kick=0.0022,
        seed=7,
    )

    monitor = GVMonitor(alpha=0.92, beta=0.08, threshold=0.015)
    trig = _first_trigger_step(monitor, g, l)

    assert trig is not None, "Expected swarm drift amplification to trigger threshold."
    assert trig >= 60, "Should not trigger before the drift kick begins."


def test_adversarial_saturation_detects_velocity_not_just_magnitude():
    """
    Slow poison: global/local rise very gradually.
    We expect ds_dt to cross threshold at some point even if values remain bounded.
    """
    g, l = adversarial_saturation_run(steps=650, eps=0.00045, wobble=0.00018, seed=11)

    monitor = GVMonitor(alpha=0.92, beta=0.08, threshold=0.00065)
    trig = _first_trigger_step(monitor, g, l)

    assert trig is not None, "Expected slow adversarial saturation to trigger ds/dt threshold."
    assert trig > 10, "Should not trigger immediately; it should be a long-horizon detection."


def test_human_ai_feedback_loop_shows_silent_recoverability_loss():
    """
    Even if entropy trends are mild, recoverability can silently decay due to feedback bias.
    This test asserts that recoverability meaningfully drops over the horizon.
    """
    g, l, r = human_ai_feedback_loop_run(
        steps=520,
        bias_accum=0.0006,
        recovery_decay=0.0012,
        seed=23,
    )

    # Sanity: entropy didn't explode
    assert max(g) < 0.69 and max(l) < 0.69

    # Key: recoverability silently degrades
    assert r[0] > 0.90
    assert r[-1] < 0.40, "Expected significant recoverability loss over long horizon."
