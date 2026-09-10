import numpy as np
from dataclasses import dataclass

SEED = 20260910
RNG = np.random.default_rng(SEED)

TARGET_FPR = 0.05
N_CONTROLS = 500
N_TESTS = 500
N_STEPS = 1500
NOISE_LEVELS = [0.0, 0.01, 0.05, 0.10]

EPS = 1e-12


@dataclass
class Trajectory:
    t: np.ndarray
    x: np.ndarray
    dx: np.ndarray
    ddx: np.ndarray
    blowup_time: float | None


def control_trajectory(x0, t_end=1.0, n=N_STEPS):
    """
    Stable control:
        dx/dt = -x
        x(t) = x0 exp(-t)
    """
    t = np.linspace(0.0, t_end, n)
    x = x0 * np.exp(-t)
    dx = -x
    ddx = x

    return Trajectory(t, x, dx, ddx, None)


def blowup_trajectory(x0, cutoff_fraction=0.98, n=N_STEPS):
    """
    Known finite-time blow-up:
        dx/dt = x^2
        x(t) = x0 / (1 - x0 t)
        t* = 1/x0

    We stop before the singularity to avoid numerical infinity.
    """
    t_star = 1.0 / x0
    t = np.linspace(0.0, cutoff_fraction * t_star, n)

    denom = 1.0 - x0 * t
    x = x0 / denom

    dx = x**2
    ddx = 2.0 * x**3

    return Trajectory(t, x, dx, ddx, t_star)


def noisy_observables(traj, noise_fraction):
    """
    Adds multiplicative Gaussian observational noise independently
    to x, dx, and ddx.
    """
    def add_noise(arr):
        scale = noise_fraction * np.maximum(np.abs(arr), EPS)
        return arr + RNG.normal(0.0, scale, size=arr.shape)

    return (
        add_noise(traj.x),
        add_noise(traj.dx),
        add_noise(traj.ddx),
    )


def features(x, dx, ddx):
    return np.column_stack([
        np.log1p(np.abs(x)),
        np.log1p(np.abs(dx)),
        np.log1p(np.abs(ddx)),
    ])


def fit_control_normalization(control_feature_rows):
    """
    Fit normalization ONLY on control data.
    """
    mu = np.mean(control_feature_rows, axis=0)
    sigma = np.std(control_feature_rows, axis=0)

    sigma = np.where(sigma < EPS, 1.0, sigma)

    return mu, sigma


def detector_scores(x, dx, ddx, mu, sigma):
    f = features(x, dx, ddx)

    z = (f - mu) / sigma

    gv = np.sum(z, axis=1)

    b1 = np.abs(x)
    b2 = np.abs(dx)
    b3 = np.abs(ddx)

    return {
        "GV": gv,
        "|x|": b1,
        "|dx/dt|": b2,
        "|d2x/dt2|": b3,
    }


def calibrate_threshold(scores_by_detector, target_fpr=TARGET_FPR):
    """
    Threshold is chosen so only approximately target_fpr of
    control trajectories ever alarm.

    Calibration is trajectory-level, not timepoint-level.
    """
    thresholds = {}

    for name, trajectory_scores in scores_by_detector.items():
        maxima = np.array([np.max(s) for s in trajectory_scores])

        thresholds[name] = np.quantile(
            maxima,
            1.0 - target_fpr
        )

    return thresholds


def first_alarm_time(t, score, threshold):
    idx = np.flatnonzero(score > threshold)

    if len(idx) == 0:
        return None

    return float(t[idx[0]])


def evaluate_detector(traj, scores, threshold):
    alarm = first_alarm_time(traj.t, scores, threshold)

    if alarm is None:
        return None

    return traj.blowup_time - alarm


def build_control_calibration(noise_fraction):
    controls = []

    raw = []

    for _ in range(N_CONTROLS):
        x0 = RNG.uniform(0.25, 2.0)

        traj = control_trajectory(x0)

        x, dx, ddx = noisy_observables(traj, noise_fraction)

        raw.append((traj, x, dx, ddx))

        controls.append(features(x, dx, ddx))

    pooled_features = np.vstack(controls)

    mu, sigma = fit_control_normalization(pooled_features)

    scores_by_detector = {
        "GV": [],
        "|x|": [],
        "|dx/dt|": [],
        "|d2x/dt2|": [],
    }

    for traj, x, dx, ddx in raw:
        scores = detector_scores(x, dx, ddx, mu, sigma)

        for name in scores_by_detector:
            scores_by_detector[name].append(scores[name])

    thresholds = calibrate_threshold(scores_by_detector)

    return mu, sigma, thresholds, scores_by_detector


def observed_control_fpr(scores_by_detector, thresholds):
    fprs = {}

    for name, trajectories in scores_by_detector.items():
        alarms = [
            np.any(scores > thresholds[name])
            for scores in trajectories
        ]

        fprs[name] = float(np.mean(alarms))

    return fprs


def run_test_set(noise_fraction, mu, sigma, thresholds):
    leads = {
        "GV": [],
        "|x|": [],
        "|dx/dt|": [],
        "|d2x/dt2|": [],
    }

    for _ in range(N_TESTS):
        x0 = RNG.uniform(0.5, 2.0)

        traj = blowup_trajectory(x0)

        x, dx, ddx = noisy_observables(
            traj,
            noise_fraction
        )

        scores = detector_scores(
            x,
            dx,
            ddx,
            mu,
            sigma
        )

        for name in leads:
            lead = evaluate_detector(
                traj,
                scores[name],
                thresholds[name]
            )

            leads[name].append(
                np.nan if lead is None else lead
            )

    return {
        name: np.array(values, dtype=float)
        for name, values in leads.items()
    }


def summarize(noise_fraction, leads, fprs):
    print()
    print("=" * 72)
    print(f"NOISE FRACTION: {noise_fraction:.2%}")
    print("=" * 72)

    medians = {}

    for name, values in leads.items():
        valid = values[~np.isnan(values)]

        detection_rate = len(valid) / len(values)

        median_lead = (
            float(np.median(valid))
            if len(valid)
            else np.nan
        )

        medians[name] = median_lead

        print(
            f"{name:12s} "
            f"FPR={fprs[name]:6.3f} "
            f"Detection={detection_rate:6.3f} "
            f"Median lead={median_lead:10.6f}"
        )

    conventional = [
        medians["|x|"],
        medians["|dx/dt|"],
        medians["|d2x/dt2|"],
    ]

    best_baseline = np.nanmax(conventional)

    delta = medians["GV"] - best_baseline

    print("-" * 72)
    print(f"Best baseline median lead: {best_baseline:.6f}")
    print(f"GV median lead:            {medians['GV']:.6f}")
    print(f"Delta L:                   {delta:.6f}")

    passes = (
        fprs["GV"] <= TARGET_FPR + 0.01
        and not np.isnan(medians["GV"])
        and delta > 0.0
    )

    print(
        "F0 RESULT:",
        "SUPPORTIVE" if passes else "NOT SUPPORTIVE"
    )

    return passes, delta


def main():
    print("GV FLUID INSTABILITY BENCHMARK — F0")
    print("-----------------------------------")
    print(f"Seed: {SEED}")
    print(f"Control trajectories: {N_CONTROLS}")
    print(f"Blow-up trajectories: {N_TESTS}")
    print(f"Target FPR: {TARGET_FPR:.2%}")

    all_pass = True

    for noise_fraction in NOISE_LEVELS:
        mu, sigma, thresholds, control_scores = (
            build_control_calibration(noise_fraction)
        )

        fprs = observed_control_fpr(
            control_scores,
            thresholds
        )

        leads = run_test_set(
            noise_fraction,
            mu,
            sigma,
            thresholds
        )

        passes, delta = summarize(
            noise_fraction,
            leads,
            fprs
        )

        all_pass = all_pass and passes

    print()
    print("=" * 72)

    if all_pass:
        print(
            "OVERALL F0: SUPPORTIVE UNDER ALL "
            "PREREGISTERED NOISE CONDITIONS"
        )
    else:
        print(
            "OVERALL F0: PREREGISTERED SUCCESS "
            "CRITERION NOT MET"
        )

    print("=" * 72)


if __name__ == "__main__":
    main()
