import numpy as np

SEED = 20260910
RNG = np.random.default_rng(SEED)

TARGET_FPR = 0.05

N_CONTROLS = 300
N_TESTS = 300

N_X = 512
N_T = 220

CONTROL_T_END = 1.0
CUTOFF_FRACTION = 0.98

NOISE_LEVELS = [0.00, 0.01, 0.05, 0.10]

TWO_PI = 2.0 * np.pi
DX = TWO_PI / N_X
XGRID = np.linspace(0.0, TWO_PI, N_X, endpoint=False)

EPS = 1e-12

DETECTORS = [
    "GV",
    "B1_max_gradient",
    "B2_max_curvature",
    "B3_total_variation",
    "B4_gradient_energy",
    "B5_max_compression",
]


def solve_characteristics(A, t):
    """
    Exact pre-shock solution of:

        u_t + u u_x = 0
        u(x,0) = A sin(x)

    Characteristics satisfy:

        x = xi + t A sin(xi)

    Before shock formation the mapping xi -> x is one-to-one,
    so Newton iteration recovers xi for each Eulerian grid point.
    """

    xi = XGRID.copy()

    for _ in range(15):
        f = xi + t * A * np.sin(xi) - XGRID
        fp = 1.0 + t * A * np.cos(xi)

        step = f / fp
        xi -= step

        if np.max(np.abs(step)) < 1e-12:
            break

    return A * np.sin(xi)


def add_noise(u, noise_fraction):
    if noise_fraction == 0.0:
        return u.copy()

    scale = noise_fraction * max(np.std(u), EPS)

    return u + RNG.normal(
        0.0,
        scale,
        size=u.shape
    )


def spatial_derivatives(u):
    """
    Periodic centered finite differences.
    """

    ux = (
        np.roll(u, -1)
        - np.roll(u, 1)
    ) / (2.0 * DX)

    uxx = (
        np.roll(u, -1)
        - 2.0 * u
        + np.roll(u, 1)
    ) / (DX ** 2)

    return ux, uxx


def conventional_metrics(u):
    ux, uxx = spatial_derivatives(u)

    B1 = np.max(np.abs(ux))

    B2 = np.max(np.abs(uxx))

    B3 = np.sum(np.abs(ux)) * DX

    B4 = np.sum(ux ** 2) * DX

    B5 = -np.min(ux)

    return np.array(
        [B1, B2, B3, B4, B5],
        dtype=float
    )


def trajectory(A, noise_fraction, control):
    """
    Returns:
        times
        conventional metric matrix [time, 5]
        analytic shock time
    """

    t_star = 1.0 / A

    if control:
        t_end = CONTROL_T_END
    else:
        t_end = CUTOFF_FRACTION * t_star

    times = np.linspace(
        0.0,
        t_end,
        N_T
    )

    rows = []

    for t in times:
        u = solve_characteristics(A, t)

        observed = add_noise(
            u,
            noise_fraction
        )

        rows.append(
            conventional_metrics(observed)
        )

    return (
        times,
        np.vstack(rows),
        t_star
    )


def log_features(metric_matrix):
    return np.log1p(
        np.maximum(metric_matrix, 0.0)
    )


def build_control_set(noise_fraction):
    trajectories = []

    pooled = []

    for _ in range(N_CONTROLS):

        A = RNG.uniform(0.10, 0.40)

        times, metrics, t_star = trajectory(
            A,
            noise_fraction,
            control=True
        )

        logs = log_features(metrics)

        pooled.append(logs)

        trajectories.append(
            (times, metrics, logs)
        )

    pooled = np.vstack(pooled)

    mu = np.mean(pooled, axis=0)

    sigma = np.std(pooled, axis=0)

    sigma = np.where(
        sigma < EPS,
        1.0,
        sigma
    )

    return trajectories, mu, sigma


def detector_scores(metrics, logs, mu, sigma):

    z = (logs - mu) / sigma

    gv = np.sum(z, axis=1)

    return {
        "GV": gv,

        "B1_max_gradient":
            metrics[:, 0],

        "B2_max_curvature":
            metrics[:, 1],

        "B3_total_variation":
            metrics[:, 2],

        "B4_gradient_energy":
            metrics[:, 3],

        "B5_max_compression":
            metrics[:, 4],
    }


def calibrate_thresholds(
    control_trajectories,
    mu,
    sigma
):
    maxima = {
        name: []
        for name in DETECTORS
    }

    for times, metrics, logs in control_trajectories:

        scores = detector_scores(
            metrics,
            logs,
            mu,
            sigma
        )

        for name in DETECTORS:
            maxima[name].append(
                np.max(scores[name])
            )

    thresholds = {}

    for name in DETECTORS:

        thresholds[name] = np.quantile(
            np.asarray(maxima[name]),
            1.0 - TARGET_FPR
        )

    return thresholds, maxima


def observed_control_fpr(
    maxima,
    thresholds
):

    return {
        name:
        float(
            np.mean(
                np.asarray(maxima[name])
                > thresholds[name]
            )
        )
        for name in DETECTORS
    }


def first_alarm_time(
    times,
    score,
    threshold
):

    idx = np.flatnonzero(
        score > threshold
    )

    if len(idx) == 0:
        return None

    return float(times[idx[0]])


def run_test_set(
    noise_fraction,
    mu,
    sigma,
    thresholds
):

    lead_times = {
        name: []
        for name in DETECTORS
    }

    paired_deltas = []

    for _ in range(N_TESTS):

        A = RNG.uniform(
            1.0,
            2.0
        )

        times, metrics, t_star = trajectory(
            A,
            noise_fraction,
            control=False
        )

        logs = log_features(metrics)

        scores = detector_scores(
            metrics,
            logs,
            mu,
            sigma
        )

        this_leads = {}

        for name in DETECTORS:

            alarm = first_alarm_time(
                times,
                scores[name],
                thresholds[name]
            )

            if alarm is None:
                lead = np.nan
            else:
                lead = (
                    t_star - alarm
                )

            lead_times[name].append(lead)

            this_leads[name] = lead

        gv_lead = this_leads["GV"]

        baseline_values = [
            this_leads[name]
            for name in DETECTORS
            if name != "GV"
            and not np.isnan(
                this_leads[name]
            )
        ]

        if (
            not np.isnan(gv_lead)
            and baseline_values
        ):
            paired_deltas.append(
                gv_lead
                - max(baseline_values)
            )
        else:
            paired_deltas.append(
                np.nan
            )

    return (
        {
            name:
            np.asarray(values)
            for name, values
            in lead_times.items()
        },
        np.asarray(paired_deltas)
    )


def summarize(
    noise_fraction,
    leads,
    paired_deltas,
    fprs
):

    print()
    print("=" * 82)

    print(
        f"NOISE FRACTION: "
        f"{noise_fraction:.2%}"
    )

    print("=" * 82)

    medians = {}

    for name in DETECTORS:

        vals = leads[name]

        valid = vals[
            ~np.isnan(vals)
        ]

        detection_rate = (
            len(valid)
            / len(vals)
        )

        median_lead = (
            float(np.median(valid))
            if len(valid)
            else np.nan
        )

        medians[name] = (
            median_lead
        )

        print(
            f"{name:22s} "
            f"FPR={fprs[name]:6.3f} "
            f"Detection={detection_rate:6.3f} "
            f"Median lead={median_lead:10.6f}"
        )

    baseline_names = [
        name
        for name in DETECTORS
        if name != "GV"
    ]

    best_baseline_name = max(
        baseline_names,
        key=lambda name:
        medians[name]
        if not np.isnan(
            medians[name]
        )
        else -np.inf
    )

    best_baseline = medians[
        best_baseline_name
    ]

    gv_median = medians["GV"]

    valid_delta = paired_deltas[
        ~np.isnan(paired_deltas)
    ]

    median_paired_delta = (
        float(
            np.median(valid_delta)
        )
        if len(valid_delta)
        else np.nan
    )

    print("-" * 82)

    print(
        "Best baseline:             "
        f"{best_baseline_name}"
    )

    print(
        "Best baseline median lead: "
        f"{best_baseline:.6f}"
    )

    print(
        "GV median lead:            "
        f"{gv_median:.6f}"
    )

    print(
        "Median paired Delta L:     "
        f"{median_paired_delta:.6f}"
    )

    fpr_ok = (
        fprs["GV"]
        <= TARGET_FPR + 0.01
    )

    detection_ok = (
        np.mean(
            ~np.isnan(
                leads["GV"]
            )
        )
        == 1.0
    )

    beats_all = all(
        gv_median > medians[name]
        for name in baseline_names
    )

    delta_ok = (
        not np.isnan(
            median_paired_delta
        )
        and median_paired_delta > 0.0
    )

    supportive = (
        fpr_ok
        and detection_ok
        and beats_all
        and delta_ok
    )

    print(
        "F1 RESULT:",
        "SUPPORTIVE"
        if supportive
        else "NOT SUPPORTIVE"
    )

    return supportive


def main():

    print(
        "GV FLUID INSTABILITY "
        "BENCHMARK — F1"
    )

    print(
        "1-D INVISCID BURGERS "
        "GRADIENT CATASTROPHE"
    )

    print("-" * 82)

    print(f"Seed: {SEED}")

    print(
        f"Spatial points: {N_X}"
    )

    print(
        f"Time samples: {N_T}"
    )

    print(
        f"Control trajectories: "
        f"{N_CONTROLS}"
    )

    print(
        f"Test trajectories: "
        f"{N_TESTS}"
    )

    print(
        f"Target FPR: "
        f"{TARGET_FPR:.2%}"
    )

    all_supportive = True

    for noise_fraction in NOISE_LEVELS:

        (
            controls,
            mu,
            sigma
        ) = build_control_set(
            noise_fraction
        )

        (
            thresholds,
            maxima
        ) = calibrate_thresholds(
            controls,
            mu,
            sigma
        )

        fprs = observed_control_fpr(
            maxima,
            thresholds
        )

        (
            leads,
            paired_deltas
        ) = run_test_set(
            noise_fraction,
            mu,
            sigma,
            thresholds
        )

        supportive = summarize(
            noise_fraction,
            leads,
            paired_deltas,
            fprs
        )

        all_supportive = (
            all_supportive
            and supportive
        )

    print()
    print("=" * 82)

    if all_supportive:

        print(
            "OVERALL F1: SUPPORTIVE "
            "UNDER ALL PREREGISTERED "
            "NOISE CONDITIONS"
        )

    else:

        print(
            "OVERALL F1: "
            "PREREGISTERED SUCCESS "
            "CRITERION NOT MET"
        )

    print("=" * 82)


if __name__ == "__main__":
    main()
