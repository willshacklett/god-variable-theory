import numpy as np

SEED = 20260910
RNG = np.random.default_rng(SEED)

TARGET_FPR = 0.05
FPR_TOLERANCE = 0.01
MAX_PRE_ONSET_ACTIVE_ALARM_RATE = 0.10
MIN_ACTIVE_EVENT_FRACTION = 0.80

N_CONTROLS = 160
N_ACTIVE = 160
N_X = 96
N_SAMPLES = 181

DOMAIN = 2.0 * np.pi
DX = DOMAIN / N_X
X = np.linspace(0.0, DOMAIN, N_X, endpoint=False)

NU = 0.10
K_FORCE = 2.0
T_ON = 0.25
RAMP_DURATION = 0.20
T_END = 1.20
DT = 0.002
C_CRIT = 4.0

NOISE_LEVELS = [0.00, 0.01, 0.05, 0.10]
EPS = 1e-12

DETECTORS = [
    "GV",
    "B1_max_gradient",
    "B2_max_curvature",
    "B3_total_variation",
    "B4_gradient_energy",
    "B5_max_compression",
]


def initial_condition(A, phi):
    return A * np.sin(X) + 0.15 * A * np.sin(2.0 * X + phi)


def derivatives(u):
    ux = (np.roll(u, -1) - np.roll(u, 1)) / (2.0 * DX)
    uxx = (np.roll(u, -1) - 2.0 * u + np.roll(u, 1)) / (DX * DX)
    return ux, uxx


def forcing(t, active):
    if not active or t < T_ON:
        return np.zeros_like(X)

    ramp = min(1.0, (t - T_ON) / RAMP_DURATION)
    return ramp * K_FORCE * np.sin(X)


def rhs(u, t, active):
    ux, uxx = derivatives(u)
    return -u * ux + NU * uxx + forcing(t, active)


def rk4_step(u, t, dt, active):
    k1 = rhs(u, t, active)
    k2 = rhs(u + 0.5 * dt * k1, t + 0.5 * dt, active)
    k3 = rhs(u + 0.5 * dt * k2, t + 0.5 * dt, active)
    k4 = rhs(u + dt * k3, t + dt, active)

    return u + (dt / 6.0) * (
        k1 + 2.0 * k2 + 2.0 * k3 + k4
    )


def compression(u):
    ux, _ = derivatives(u)
    return -float(np.min(ux))


def simulate(A, phi, active):
    sample_times = np.linspace(0.0, T_END, N_SAMPLES)
    fields = np.empty((N_SAMPLES, N_X), dtype=float)

    u = initial_condition(A, phi)
    t = 0.0
    event_time = None
    sample_idx = 0
    finite = True

    fields[0] = u
    sample_idx = 1

    if compression(u) >= C_CRIT:
        event_time = 0.0

    n_steps = int(np.ceil(T_END / DT))

    for _ in range(n_steps):
        if t >= T_END - EPS:
            break

        h = min(DT, T_END - t)

        u_prev = u.copy()
        t_prev = t
        c_prev = compression(u_prev)

        u = rk4_step(u, t, h, active)
        t += h

        if not np.all(np.isfinite(u)):
            finite = False
            break

        c_now = compression(u)

        if event_time is None and c_prev < C_CRIT <= c_now:
            frac = (C_CRIT - c_prev) / max(c_now - c_prev, EPS)
            event_time = t_prev + frac * h

        while (
            sample_idx < N_SAMPLES
            and sample_times[sample_idx] <= t + EPS
        ):
            target = sample_times[sample_idx]
            alpha = np.clip((target - t_prev) / h, 0.0, 1.0)

            fields[sample_idx] = (
                (1.0 - alpha) * u_prev
                + alpha * u
            )

            sample_idx += 1

    if finite and sample_idx < N_SAMPLES:
        fields[sample_idx:] = u

    return {
        "A": A,
        "phi": phi,
        "active": active,
        "times": sample_times,
        "fields": fields,
        "event_time": event_time,
        "finite": finite,
    }


def add_observational_noise(fields, noise_fraction, rng):
    if noise_fraction == 0.0:
        return fields.copy()

    out = fields.copy()

    for i, u in enumerate(fields):
        scale = noise_fraction * max(float(np.std(u)), EPS)

        out[i] = u + rng.normal(
            0.0,
            scale,
            size=u.shape
        )

    return out


def conventional_metrics(u):
    ux, uxx = derivatives(u)

    return np.array([
        np.max(np.abs(ux)),
        np.max(np.abs(uxx)),
        np.sum(np.abs(ux)) * DX,
        np.sum(ux ** 2) * DX,
        -np.min(ux),
    ], dtype=float)


def metric_matrix(fields):
    return np.vstack(
        [conventional_metrics(u) for u in fields]
    )


def log_features(metrics):
    return np.log1p(
        np.maximum(metrics, 0.0)
    )


def detector_scores(metrics, mu, sigma):
    logs = log_features(metrics)

    z = (logs - mu) / sigma

    return {
        "GV": np.sum(z, axis=1),
        "B1_max_gradient": metrics[:, 0],
        "B2_max_curvature": metrics[:, 1],
        "B3_total_variation": metrics[:, 2],
        "B4_gradient_energy": metrics[:, 3],
        "B5_max_compression": metrics[:, 4],
    }


def first_alarm_time(
    times,
    scores,
    threshold,
    event_time=None
):
    mask = scores > threshold

    if event_time is not None:
        mask &= times < event_time

    idx = np.flatnonzero(mask)

    if len(idx) == 0:
        return None

    return float(times[idx[0]])


def build_population():
    controls = []
    active = []

    control_params = [
        (
            RNG.uniform(0.60, 1.00),
            RNG.uniform(0.0, 2.0 * np.pi)
        )
        for _ in range(N_CONTROLS)
    ]

    active_params = [
        (
            RNG.uniform(0.60, 1.00),
            RNG.uniform(0.0, 2.0 * np.pi)
        )
        for _ in range(N_ACTIVE)
    ]

    for A, phi in control_params:
        controls.append(
            simulate(A, phi, active=False)
        )

    for A, phi in active_params:
        active.append(
            simulate(A, phi, active=True)
        )

    return controls, active


def prepare_control_calibration(
    controls,
    noise_fraction,
    rng
):
    rows = []
    control_metrics = []

    for tr in controls:
        observed = add_observational_noise(
            tr["fields"],
            noise_fraction,
            rng
        )

        metrics = metric_matrix(observed)

        control_metrics.append(metrics)
        rows.append(log_features(metrics))

    pooled = np.vstack(rows)

    mu = np.mean(pooled, axis=0)
    sigma = np.std(pooled, axis=0)

    sigma = np.where(
        sigma < EPS,
        1.0,
        sigma
    )

    maxima = {
        name: []
        for name in DETECTORS
    }

    for metrics in control_metrics:
        scores = detector_scores(
            metrics,
            mu,
            sigma
        )

        for name in DETECTORS:
            maxima[name].append(
                float(np.max(scores[name]))
            )

    thresholds = {
        name: float(
            np.quantile(
                maxima[name],
                1.0 - TARGET_FPR
            )
        )
        for name in DETECTORS
    }

    fprs = {
        name: float(
            np.mean(
                np.asarray(maxima[name])
                > thresholds[name]
            )
        )
        for name in DETECTORS
    }

    return mu, sigma, thresholds, fprs


def evaluate_active(
    active,
    noise_fraction,
    mu,
    sigma,
    thresholds,
    rng
):
    leads = {
        name: []
        for name in DETECTORS
    }

    pre_onset = {
        name: []
        for name in DETECTORS
    }

    paired_delta = []
    event_count = 0

    for tr in active:
        event_time = tr["event_time"]

        if event_time is None:
            continue

        event_count += 1

        observed = add_observational_noise(
            tr["fields"],
            noise_fraction,
            rng
        )

        metrics = metric_matrix(observed)

        scores = detector_scores(
            metrics,
            mu,
            sigma
        )

        this_leads = {}

        for name in DETECTORS:
            alarm_any = first_alarm_time(
                tr["times"],
                scores[name],
                thresholds[name]
            )

            pre_onset[name].append(
                alarm_any is not None
                and alarm_any < T_ON
            )

            alarm = first_alarm_time(
                tr["times"],
                scores[name],
                thresholds[name],
                event_time=event_time
            )

            lead = (
                np.nan
                if alarm is None
                else event_time - alarm
            )

            leads[name].append(lead)
            this_leads[name] = lead

        gv = this_leads["GV"]

        baselines = [
            this_leads[name]
            for name in DETECTORS
            if name != "GV"
            and not np.isnan(this_leads[name])
        ]

        if not np.isnan(gv) and baselines:
            paired_delta.append(
                gv - max(baselines)
            )
        else:
            paired_delta.append(np.nan)

    return (
        {
            name: np.asarray(vals, dtype=float)
            for name, vals in leads.items()
        },
        {
            name: (
                float(np.mean(vals))
                if vals
                else np.nan
            )
            for name, vals in pre_onset.items()
        },
        np.asarray(
            paired_delta,
            dtype=float
        ),
        event_count / len(active),
    )


def summarize(
    noise_fraction,
    leads,
    pre_onset,
    paired_delta,
    fprs,
    event_fraction,
    solver_ok
):
    print()
    print("=" * 96)
    print(
        f"NOISE FRACTION: "
        f"{noise_fraction:.2%}"
    )
    print("=" * 96)

    medians = {}
    detection_rates = {}

    for name in DETECTORS:
        vals = leads[name]

        valid = vals[
            ~np.isnan(vals)
        ]

        detection = (
            len(valid) / len(vals)
            if len(vals)
            else 0.0
        )

        median = (
            float(np.median(valid))
            if len(valid)
            else np.nan
        )

        medians[name] = median
        detection_rates[name] = detection

        print(
            f"{name:22s} "
            f"FPR={fprs[name]:6.3f} "
            f"PreOnset={pre_onset[name]:6.3f} "
            f"Detection={detection:6.3f} "
            f"MedianLead={median:10.6f}"
        )

    baseline_names = [
        name
        for name in DETECTORS
        if name != "GV"
    ]

    finite_baselines = [
        name
        for name in baseline_names
        if not np.isnan(medians[name])
    ]

    best_name = (
        max(
            finite_baselines,
            key=lambda name: medians[name]
        )
        if finite_baselines
        else None
    )

    best_median = (
        medians[best_name]
        if best_name
        else np.nan
    )

    valid_delta = paired_delta[
        ~np.isnan(paired_delta)
    ]

    median_delta = (
        float(np.median(valid_delta))
        if len(valid_delta)
        else np.nan
    )

    print("-" * 96)
    print(
        f"Active event fraction:       "
        f"{event_fraction:.3f}"
    )
    print(
        f"Best baseline:               "
        f"{best_name}"
    )
    print(
        f"Best baseline median lead:   "
        f"{best_median:.6f}"
    )
    print(
        f"GV median lead:              "
        f"{medians['GV']:.6f}"
    )
    print(
        f"Median paired Delta L:       "
        f"{median_delta:.6f}"
    )

    validity_ok = (
        solver_ok
        and event_fraction >= MIN_ACTIVE_EVENT_FRACTION
        and pre_onset["GV"]
            <= MAX_PRE_ONSET_ACTIVE_ALARM_RATE
    )

    if not validity_ok:
        print(
            "F1b RESULT: "
            "BENCHMARK INVALID"
        )
        return "INVALID"

    fpr_ok = (
        fprs["GV"]
        <= TARGET_FPR + FPR_TOLERANCE
    )

    detects = (
        detection_rates["GV"] > 0.0
    )

    beats_all = (
        not np.isnan(medians["GV"])
        and all(
            medians["GV"] > medians[name]
            for name in finite_baselines
        )
    )

    delta_ok = (
        not np.isnan(median_delta)
        and median_delta > 0.0
    )

    supportive = (
        fpr_ok
        and detects
        and beats_all
        and delta_ok
    )

    print(
        "F1b RESULT:",
        "SUPPORTIVE"
        if supportive
        else "NOT SUPPORTIVE"
    )

    return (
        "SUPPORTIVE"
        if supportive
        else "NOT SUPPORTIVE"
    )


def main():
    print(
        "GV FLUID INSTABILITY "
        "BENCHMARK — F1b"
    )

    print(
        "FORCED VISCOUS 1-D BURGERS "
        "— CORRECTIVE BENCHMARK"
    )

    print("-" * 96)

    print(f"Seed: {SEED}")
    print(f"Grid points: {N_X}")
    print(f"nu: {NU}")
    print(f"forcing K: {K_FORCE}")
    print(f"forcing onset: {T_ON}")
    print(
        f"event threshold Ccrit: "
        f"{C_CRIT}"
    )
    print(
        f"simulation horizon: "
        f"{T_END}"
    )
    print(f"integration dt: {DT}")
    print(
        f"control trajectories: "
        f"{N_CONTROLS}"
    )
    print(
        f"active trajectories: "
        f"{N_ACTIVE}"
    )
    print(
        f"target FPR: "
        f"{TARGET_FPR:.2%}"
    )
    print(
        f"minimum event fraction: "
        f"{MIN_ACTIVE_EVENT_FRACTION:.2%}"
    )
    print(
        "maximum allowed GV pre-onset "
        f"alarm rate: "
        f"{MAX_PRE_ONSET_ACTIVE_ALARM_RATE:.2%}"
    )

    controls, active = build_population()

    solver_ok = all(
        tr["finite"]
        for tr in controls + active
    )

    print(
        f"solver finite/stable: "
        f"{solver_ok}"
    )

    print(
        "control physical events: "
        f"{sum(tr['event_time'] is not None for tr in controls)}"
    )

    print(
        "active physical events: "
        f"{sum(tr['event_time'] is not None for tr in active)}"
    )

    outcomes = []

    for noise_index, noise_fraction in enumerate(
        NOISE_LEVELS
    ):
        noise_rng = np.random.default_rng(
            SEED + 1000 + noise_index
        )

        (
            mu,
            sigma,
            thresholds,
            fprs
        ) = prepare_control_calibration(
            controls,
            noise_fraction,
            noise_rng
        )

        (
            leads,
            pre_onset,
            paired_delta,
            event_fraction
        ) = evaluate_active(
            active,
            noise_fraction,
            mu,
            sigma,
            thresholds,
            noise_rng
        )

        outcome = summarize(
            noise_fraction,
            leads,
            pre_onset,
            paired_delta,
            fprs,
            event_fraction,
            solver_ok
        )

        outcomes.append(outcome)

    print()
    print("=" * 96)

    if any(
        outcome == "INVALID"
        for outcome in outcomes
    ):
        print(
            "OVERALL F1b: "
            "BENCHMARK INVALID"
        )

    elif all(
        outcome == "SUPPORTIVE"
        for outcome in outcomes
    ):
        print(
            "OVERALL F1b: SUPPORTIVE "
            "UNDER ALL PREREGISTERED "
            "NOISE CONDITIONS"
        )

    else:
        print(
            "OVERALL F1b: "
            "PREREGISTERED SUCCESS "
            "CRITERION NOT MET"
        )

    print("=" * 96)


if __name__ == "__main__":
    main()
