from __future__ import annotations

from src.gv_edgecase_sims import (
    GVMonitor,
    swarm_amplification_run,
    adversarial_saturation_run,
    human_ai_feedback_loop_run,
)


def _first_trigger_step(monitor: GVMonitor, g_series, l_series, min_step: int = 0) -> int | None:
    for i, (g, l) in enumerate(zip(g_series, l_series)):
        _, ds_dt = monitor.update(g, l)
        if i < min_step:
            continue
        if abs(ds_dt) > monitor.threshold:
            return i
    return None


def test_swarm_amplification_triggers_after_drift_kick():
    g, l = swarm_amplification_run(
        steps=260,
        agents=30,
        coupling=0.35,
        base_noise=0.003,
        drift_kick_step=60,
        drift_kick=0.0040,
        seed=7,
    )

    monitor = GVMonitor(alpha=0.92, beta=0.08, gamma=0.95, threshold=0.0025)
    trig = _first_trigger_step(monitor, g, l)

    assert trig is not None, "Expected swarm drift amplification to trigger threshold."
    assert trig >= 60, "Should not trigger before the drift kick begins."


def test_adversarial_saturation_detects_velocity_not_just_magnitude():
    g, l = adversarial_saturation_run(steps=650, eps=0.00055, wobble=0.00010, seed=11)

    monitor = GVMonitor(alpha=0.92, beta=0.08, gamma=0.97, threshold=0.00012)
    trig = _first_trigger_step(monitor, g, l, min_step=25)

    assert trig is not None, "Expected slow adversarial saturation to trigger ds/dt threshold."
    assert trig > 25, "Should not trigger immediately; it should be a long-horizon detection."


def test_human_ai_feedback_loop_shows_silent_recoverability_loss():
    g, l, r = human_ai_feedback_loop_run(
        steps=520,
        bias_accum=0.0006,
        recovery_decay=0.0030,
        seed=23,
    )

    assert max(g) < 0.69 and max(l) < 0.69
    assert r[0] > 0.90
    assert r[-1] < 0.40, "Expected significant recoverability loss over long horizon."
