import numpy as np

# ============================================================
# GV FLUID INSTABILITY BENCHMARK — F2
# 2-D forced incompressible Navier-Stokes, vorticity form
# ============================================================

SEED = 20260910
RNG = np.random.default_rng(SEED)

TARGET_FPR = 0.05
FPR_TOLERANCE = 0.01

N_CONTROL = 60
N_ACTIVE = 60

N = 64
L = 2.0 * np.pi
DX = L / N
AREA_ELEMENT = DX * DX

T_END = 1.50
DT = 0.005
N_SAMPLES = 151

U0 = 1.0
DELTA = 0.20
PERT_EPS = 0.05

T_ON = 0.25
RAMP_DURATION = 0.25
FORCE_AMP = 1.5

CONTROL_NU_RANGE = (0.080, 0.120)
ACTIVE_NU_RANGE = (0.008, 0.012)

NOISE_LEVELS = [0.00, 0.01, 0.05, 0.10]

MAX_CONTROL_EVENT_RATE = 0.10
MIN_ACTIVE_EVENT_RATE = 0.70
MAX_GV_T0_ALARM_RATE = 0.10

EPS = 1e-12

DETECTORS = [
    "GV",
    "B1_max_vorticity",
    "B2_enstrophy",
    "B3_max_strain",
    "B4_kinetic_energy",
    "B5_palinstrophy",
    "B6_dissipation",
]

# ------------------------------------------------------------
# Grid and spectral operators
# ------------------------------------------------------------

x = np.linspace(0.0, L, N, endpoint=False)
y = np.linspace(0.0, L, N, endpoint=False)

X, Y = np.meshgrid(x, y, indexing="ij")

k = np.fft.fftfreq(N, d=L / N) * 2.0 * np.pi

KX, KY = np.meshgrid(k, k, indexing="ij")

K2 = KX**2 + KY**2

K2_SAFE = K2.copy()
K2_SAFE[0, 0] = 1.0

# 2/3 de-aliasing
K_CUTOFF = N / 3.0

DEALIAS = (
    (np.abs(KX) <= K_CUTOFF)
    &
    (np.abs(KY) <= K_CUTOFF)
)

SAMPLE_TIMES = np.linspace(
    0.0,
    T_END,
    N_SAMPLES
)


def fft2(a):
    return np.fft.fft2(a)


def ifft2_real(a_hat):
    return np.fft.ifft2(a_hat).real


# ------------------------------------------------------------
# Initial condition
# ------------------------------------------------------------

def initial_velocity(phi):
    """
    Periodic double shear layer from preregistered amendment.

    u = streamwise base flow
    v = weak transverse perturbation
    """

    u = np.where(
        Y <= np.pi,
        U0 * np.tanh(
            (Y - np.pi / 2.0) / DELTA
        ),
        U0 * np.tanh(
            (3.0 * np.pi / 2.0 - Y) / DELTA
        ),
    )

    v = PERT_EPS * np.sin(X + phi)

    return u, v


def velocity_to_vorticity(u, v):
    """
    omega = dv/dx - du/dy
    using spectral derivatives.
    """

    u_hat = fft2(u)
    v_hat = fft2(v)

    dv_dx = ifft2_real(
        1j * KX * v_hat
    )

    du_dy = ifft2_real(
        1j * KY * u_hat
    )

    omega = dv_dx - du_dy

    omega_hat = fft2(omega)

    # Project initial condition into resolved/dealiased space.
    omega_hat *= DEALIAS
    omega_hat[0, 0] = 0.0

    return omega_hat


# ------------------------------------------------------------
# Vorticity -> velocity
# ------------------------------------------------------------

def velocity_from_vorticity(omega_hat):
    """
    With:
        laplacian(psi) = -omega
        u = psi_y
        v = -psi_x

    Fourier:
        psi_hat = omega_hat / k^2
    """

    psi_hat = omega_hat / K2_SAFE
    psi_hat[0, 0] = 0.0

    u_hat = 1j * KY * psi_hat
    v_hat = -1j * KX * psi_hat

    u = ifft2_real(u_hat)
    v = ifft2_real(v_hat)

    return u, v, u_hat, v_hat


# ------------------------------------------------------------
# Forcing
# ------------------------------------------------------------

def forcing_field(t):
    if t < T_ON:
        return np.zeros((N, N))

    ramp = min(
        1.0,
        (t - T_ON) / RAMP_DURATION
    )

    return (
        ramp
        * FORCE_AMP
        * np.cos(2.0 * Y)
    )


# ------------------------------------------------------------
# PDE RHS
# ------------------------------------------------------------

def rhs(omega_hat, t, nu):
    u, v, _, _ = velocity_from_vorticity(
        omega_hat
    )

    omega_x = ifft2_real(
        1j * KX * omega_hat
    )

    omega_y = ifft2_real(
        1j * KY * omega_hat
    )

    advection = (
        u * omega_x
        + v * omega_y
    )

    adv_hat = fft2(advection)
    adv_hat *= DEALIAS

    force_hat = fft2(
        forcing_field(t)
    )
    force_hat *= DEALIAS

    out = (
        -adv_hat
        - nu * K2 * omega_hat
        + force_hat
    )

    out *= DEALIAS
    out[0, 0] = 0.0

    return out


def rk4_step(omega_hat, t, dt, nu):
    k1 = rhs(
        omega_hat,
        t,
        nu
    )

    k2 = rhs(
        omega_hat + 0.5 * dt * k1,
        t + 0.5 * dt,
        nu
    )

    k3 = rhs(
        omega_hat + 0.5 * dt * k2,
        t + 0.5 * dt,
        nu
    )

    k4 = rhs(
        omega_hat + dt * k3,
        t + dt,
        nu
    )

    result = omega_hat + (
        dt / 6.0
    ) * (
        k1
        + 2.0 * k2
        + 2.0 * k3
        + k4
    )

    result *= DEALIAS
    result[0, 0] = 0.0

    return result


# ------------------------------------------------------------
# Diagnostics
# ------------------------------------------------------------

def diagnostics_from_omega(
    omega,
    nu
):
    omega_hat = fft2(omega)

    # Remove observational mean only.
    omega_hat[0, 0] = 0.0

    u, v, u_hat, v_hat = (
        velocity_from_vorticity(
            omega_hat
        )
    )

    du_dx = ifft2_real(
        1j * KX * u_hat
    )

    du_dy = ifft2_real(
        1j * KY * u_hat
    )

    dv_dx = ifft2_real(
        1j * KX * v_hat
    )

    dv_dy = ifft2_real(
        1j * KY * v_hat
    )

    omega_x = ifft2_real(
        1j * KX * omega_hat
    )

    omega_y = ifft2_real(
        1j * KY * omega_hat
    )

    # Strain tensor:
    # Sxx = du/dx
    # Syy = dv/dy
    # Sxy = 0.5 (du/dy + dv/dx)

    sxx = du_dx
    syy = dv_dy

    sxy = 0.5 * (
        du_dy + dv_dx
    )

    strain_mag = np.sqrt(
        np.maximum(
            0.0,
            2.0 * (
                sxx**2
                + syy**2
                + 2.0 * sxy**2
            )
        )
    )

    grad_omega_sq = (
        omega_x**2
        + omega_y**2
    )

    B1 = float(
        np.max(np.abs(omega))
    )

    B2 = float(
        0.5
        * np.sum(omega**2)
        * AREA_ELEMENT
    )

    B3 = float(
        np.max(strain_mag)
    )

    B4 = float(
        0.5
        * np.sum(u**2 + v**2)
        * AREA_ELEMENT
    )

    B5 = float(
        0.5
        * np.sum(grad_omega_sq)
        * AREA_ELEMENT
    )

    B6 = float(
        nu
        * np.sum(grad_omega_sq)
        * AREA_ELEMENT
    )

    return np.array(
        [B1, B2, B3, B4, B5, B6],
        dtype=float
    )


def noisy_omega(
    omega,
    noise_fraction,
    rng
):
    if noise_fraction == 0.0:
        return omega.copy()

    sigma = (
        noise_fraction
        * max(
            float(np.std(omega)),
            EPS
        )
    )

    return (
        omega
        + rng.normal(
            0.0,
            sigma,
            size=omega.shape
        )
    )


# ------------------------------------------------------------
# One simulation
# ------------------------------------------------------------

def simulate(
    nu,
    phi,
    trajectory_seed
):
    u0, v0 = initial_velocity(phi)

    omega_hat = velocity_to_vorticity(
        u0,
        v0
    )

    metrics_by_noise = {
        noise: np.zeros(
            (N_SAMPLES, 6),
            dtype=float
        )
        for noise in NOISE_LEVELS
    }

    noiseless_Z = np.zeros(
        N_SAMPLES,
        dtype=float
    )

    noiseless_S = np.zeros(
        N_SAMPLES,
        dtype=float
    )

    noise_rngs = {
        noise: np.random.default_rng(
            trajectory_seed
            + 10000 * i
        )
        for i, noise
        in enumerate(NOISE_LEVELS)
    }

    finite = True
    t = 0.0
    sample_idx = 0

    def record_state(idx, omega_hat_state):
        omega = ifft2_real(
            omega_hat_state
        )

        clean = diagnostics_from_omega(
            omega,
            nu
        )

        # Event diagnostics:
        # B2 = enstrophy
        # B3 = max strain
        noiseless_Z[idx] = clean[1]
        noiseless_S[idx] = clean[2]

        for noise in NOISE_LEVELS:
            observed = noisy_omega(
                omega,
                noise,
                noise_rngs[noise]
            )

            metrics_by_noise[noise][idx] = (
                diagnostics_from_omega(
                    observed,
                    nu
                )
            )

    record_state(
        0,
        omega_hat
    )

    sample_idx = 1

    n_steps = int(
        np.ceil(
            T_END / DT
        )
    )

    for _ in range(n_steps):
        if t >= T_END - EPS:
            break

        h = min(
            DT,
            T_END - t
        )

        previous_hat = omega_hat.copy()
        previous_t = t

        omega_hat = rk4_step(
            omega_hat,
            t,
            h,
            nu
        )

        t += h

        if not (
            np.all(
                np.isfinite(
                    omega_hat.real
                )
            )
            and
            np.all(
                np.isfinite(
                    omega_hat.imag
                )
            )
        ):
            finite = False
            break

        while (
            sample_idx < N_SAMPLES
            and
            SAMPLE_TIMES[sample_idx]
            <= t + EPS
        ):
            target = SAMPLE_TIMES[
                sample_idx
            ]

            alpha = np.clip(
                (
                    target
                    - previous_t
                ) / h,
                0.0,
                1.0
            )

            # Linear interpolation between
            # integration states for saved
            # diagnostic samples.
            interp_hat = (
                (1.0 - alpha)
                * previous_hat
                + alpha
                * omega_hat
            )

            record_state(
                sample_idx,
                interp_hat
            )

            sample_idx += 1

    if finite and sample_idx < N_SAMPLES:
        for idx in range(
            sample_idx,
            N_SAMPLES
        ):
            record_state(
                idx,
                omega_hat
            )

    return {
        "nu": nu,
        "phi": phi,
        "finite": finite,
        "metrics": metrics_by_noise,
        "Z": noiseless_Z,
        "S": noiseless_S,
    }


# ------------------------------------------------------------
# Build populations
# ------------------------------------------------------------

def build_population():
    controls = []
    active = []

    print()
    print("Simulating control population...")

    for i in range(N_CONTROL):
        nu = RNG.uniform(
            *CONTROL_NU_RANGE
        )

        phi = RNG.uniform(
            0.0,
            2.0 * np.pi
        )

        controls.append(
            simulate(
                nu,
                phi,
                SEED + 100000 + i
            )
        )

        if (
            (i + 1) % 10 == 0
            or i + 1 == N_CONTROL
        ):
            print(
                f"  controls: "
                f"{i + 1}/{N_CONTROL}"
            )

    print()
    print("Simulating active population...")

    for i in range(N_ACTIVE):
        nu = RNG.uniform(
            *ACTIVE_NU_RANGE
        )

        phi = RNG.uniform(
            0.0,
            2.0 * np.pi
        )

        active.append(
            simulate(
                nu,
                phi,
                SEED + 200000 + i
            )
        )

        if (
            (i + 1) % 10 == 0
            or i + 1 == N_ACTIVE
        ):
            print(
                f"  active: "
                f"{i + 1}/{N_ACTIVE}"
            )

    return controls, active


# ------------------------------------------------------------
# Control-derived physical event thresholds
# ------------------------------------------------------------

def physical_event_thresholds(
    controls
):
    max_Z = np.array([
        np.max(tr["Z"])
        for tr in controls
    ])

    max_S = np.array([
        np.max(tr["S"])
        for tr in controls
    ])

    Z_crit = float(
        np.quantile(
            max_Z,
            0.95
        )
    )

    S_crit = float(
        np.quantile(
            max_S,
            0.95
        )
    )

    return Z_crit, S_crit


def event_time(
    tr,
    Z_crit,
    S_crit
):
    mask = (
        (tr["Z"] > Z_crit)
        &
        (tr["S"] > S_crit)
    )

    idx = np.flatnonzero(mask)

    if len(idx) == 0:
        return None

    return float(
        SAMPLE_TIMES[idx[0]]
    )


# ------------------------------------------------------------
# Detector calibration
# ------------------------------------------------------------

def log_features(metrics):
    return np.log1p(
        np.maximum(
            metrics,
            0.0
        )
    )


def detector_scores(
    metrics,
    mu,
    sigma
):
    logs = log_features(metrics)

    z = (
        logs - mu
    ) / sigma

    return {
        "GV":
            np.sum(z, axis=1),

        "B1_max_vorticity":
            metrics[:, 0],

        "B2_enstrophy":
            metrics[:, 1],

        "B3_max_strain":
            metrics[:, 2],

        "B4_kinetic_energy":
            metrics[:, 3],

        "B5_palinstrophy":
            metrics[:, 4],

        "B6_dissipation":
            metrics[:, 5],
    }


def calibrate_detectors(
    controls,
    noise
):
    pooled = np.vstack([
        log_features(
            tr["metrics"][noise]
        )
        for tr in controls
    ])

    mu = np.mean(
        pooled,
        axis=0
    )

    sigma = np.std(
        pooled,
        axis=0
    )

    sigma = np.where(
        sigma < EPS,
        1.0,
        sigma
    )

    maxima = {
        name: []
        for name in DETECTORS
    }

    for tr in controls:
        scores = detector_scores(
            tr["metrics"][noise],
            mu,
            sigma
        )

        for name in DETECTORS:
            maxima[name].append(
                float(
                    np.max(
                        scores[name]
                    )
                )
            )

    thresholds = {
        name: float(
            np.quantile(
                np.asarray(
                    maxima[name]
                ),
                1.0 - TARGET_FPR
            )
        )
        for name in DETECTORS
    }

    fprs = {
        name: float(
            np.mean(
                np.asarray(
                    maxima[name]
                )
                > thresholds[name]
            )
        )
        for name in DETECTORS
    }

    return (
        mu,
        sigma,
        thresholds,
        fprs
    )


# ------------------------------------------------------------
# Alarm / lead time
# ------------------------------------------------------------

def first_alarm_before_event(
    scores,
    threshold,
    t_event
):
    mask = (
        (scores > threshold)
        &
        (SAMPLE_TIMES < t_event)
    )

    idx = np.flatnonzero(mask)

    if len(idx) == 0:
        return None

    return float(
        SAMPLE_TIMES[idx[0]]
    )


def evaluate_active(
    active,
    noise,
    mu,
    sigma,
    thresholds,
    Z_crit,
    S_crit
):
    leads = {
        name: []
        for name in DETECTORS
    }

    paired_delta = []
    gv_t0_alarm = []

    event_count = 0

    for tr in active:
        t_event = event_time(
            tr,
            Z_crit,
            S_crit
        )

        scores = detector_scores(
            tr["metrics"][noise],
            mu,
            sigma
        )

        gv_t0_alarm.append(
            bool(
                scores["GV"][0]
                > thresholds["GV"]
            )
        )

        if t_event is None:
            continue

        event_count += 1

        this_leads = {}

        for name in DETECTORS:
            alarm = first_alarm_before_event(
                scores[name],
                thresholds[name],
                t_event
            )

            if alarm is None:
                lead = np.nan
            else:
                lead = (
                    t_event
                    - alarm
                )

            leads[name].append(
                lead
            )

            this_leads[name] = lead

        gv_lead = this_leads["GV"]

        baseline_leads = [
            this_leads[name]
            for name in DETECTORS
            if name != "GV"
            and not np.isnan(
                this_leads[name]
            )
        ]

        if (
            not np.isnan(gv_lead)
            and baseline_leads
        ):
            paired_delta.append(
                gv_lead
                - max(
                    baseline_leads
                )
            )
        else:
            paired_delta.append(
                np.nan
            )

    return (
        {
            name:
            np.asarray(
                vals,
                dtype=float
            )
            for name, vals
            in leads.items()
        },
        np.asarray(
            paired_delta,
            dtype=float
        ),
        (
            event_count
            / len(active)
        ),
        float(
            np.mean(
                gv_t0_alarm
            )
        ),
    )


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

def summarize(
    noise,
    leads,
    paired_delta,
    fprs,
    active_event_rate,
    gv_t0_rate,
    globally_valid
):
    print()
    print("=" * 104)
    print(
        f"NOISE FRACTION: "
        f"{noise:.2%}"
    )
    print("=" * 104)

    medians = {}
    detections = {}

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
            float(
                np.median(valid)
            )
            if len(valid)
            else np.nan
        )

        detections[name] = detection
        medians[name] = median

        print(
            f"{name:22s} "
            f"FPR={fprs[name]:6.3f} "
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
        if not np.isnan(
            medians[name]
        )
    ]

    best_name = (
        max(
            finite_baselines,
            key=lambda n:
                medians[n]
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
        ~np.isnan(
            paired_delta
        )
    ]

    median_delta = (
        float(
            np.median(
                valid_delta
            )
        )
        if len(valid_delta)
        else np.nan
    )

    print("-" * 104)

    print(
        f"Active physical-event rate: "
        f"{active_event_rate:.3f}"
    )

    print(
        f"GV t=0 alarm rate:           "
        f"{gv_t0_rate:.3f}"
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

    if not globally_valid:
        print(
            "F2 RESULT: "
            "BENCHMARK INVALID"
        )
        return "INVALID"

    noise_valid = (
        gv_t0_rate
        <= MAX_GV_T0_ALARM_RATE
    )

    if not noise_valid:
        print(
            "F2 RESULT: "
            "BENCHMARK INVALID"
        )
        return "INVALID"

    fpr_ok = (
        fprs["GV"]
        <= TARGET_FPR
        + FPR_TOLERANCE
    )

    detects = (
        detections["GV"] > 0.0
    )

    beats_all = (
        not np.isnan(
            medians["GV"]
        )
        and all(
            medians["GV"]
            > medians[name]
            for name in finite_baselines
        )
    )

    delta_ok = (
        not np.isnan(
            median_delta
        )
        and median_delta > 0.0
    )

    supportive = (
        fpr_ok
        and detects
        and beats_all
        and delta_ok
    )

    print(
        "F2 RESULT:",
        "SUPPORTIVE"
        if supportive
        else "NOT SUPPORTIVE"
    )

    return (
        "SUPPORTIVE"
        if supportive
        else "NOT SUPPORTIVE"
    )


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():
    print(
        "GV FLUID INSTABILITY "
        "BENCHMARK — F2"
    )

    print(
        "2-D FORCED INCOMPRESSIBLE "
        "NAVIER-STOKES"
    )

    print("-" * 104)

    print(f"Seed: {SEED}")
    print(f"Grid: {N} x {N}")
    print(f"dt: {DT}")
    print(f"Horizon: {T_END}")
    print(f"Samples: {N_SAMPLES}")

    print(
        "Control viscosity: "
        f"{CONTROL_NU_RANGE}"
    )

    print(
        "Active viscosity:  "
        f"{ACTIVE_NU_RANGE}"
    )

    print(
        f"Forcing onset: {T_ON}"
    )

    print(
        f"Forcing amplitude: "
        f"{FORCE_AMP}"
    )

    print(
        f"Controls: {N_CONTROL}"
    )

    print(
        f"Active: {N_ACTIVE}"
    )

    print(
        f"Target FPR: "
        f"{TARGET_FPR:.2%}"
    )

    controls, active = (
        build_population()
    )

    solver_ok = all(
        tr["finite"]
        for tr in controls + active
    )

    Z_crit, S_crit = (
        physical_event_thresholds(
            controls
        )
    )

    control_events = [
        event_time(
            tr,
            Z_crit,
            S_crit
        )
        is not None
        for tr in controls
    ]

    active_events = [
        event_time(
            tr,
            Z_crit,
            S_crit
        )
        is not None
        for tr in active
    ]

    control_event_rate = float(
        np.mean(
            control_events
        )
    )

    active_event_rate = float(
        np.mean(
            active_events
        )
    )

    print()
    print("-" * 104)

    print(
        f"Solver finite/stable: "
        f"{solver_ok}"
    )

    print(
        f"Z_crit: "
        f"{Z_crit:.6f}"
    )

    print(
        f"S_crit: "
        f"{S_crit:.6f}"
    )

    print(
        "Control physical-event rate: "
        f"{control_event_rate:.3f}"
    )

    print(
        "Active physical-event rate:  "
        f"{active_event_rate:.3f}"
    )

    globally_valid = (
        solver_ok
        and
        control_event_rate
        <= MAX_CONTROL_EVENT_RATE
        and
        active_event_rate
        >= MIN_ACTIVE_EVENT_RATE
    )

    print(
        f"Global validity checks: "
        f"{globally_valid}"
    )

    outcomes = []

    for noise in NOISE_LEVELS:
        (
            mu,
            sigma,
            thresholds,
            fprs
        ) = calibrate_detectors(
            controls,
            noise
        )

        (
            leads,
            paired_delta,
            event_rate,
            gv_t0_rate
        ) = evaluate_active(
            active,
            noise,
            mu,
            sigma,
            thresholds,
            Z_crit,
            S_crit
        )

        outcome = summarize(
            noise,
            leads,
            paired_delta,
            fprs,
            event_rate,
            gv_t0_rate,
            globally_valid
        )

        outcomes.append(
            outcome
        )

    print()
    print("=" * 104)

    if any(
        x == "INVALID"
        for x in outcomes
    ):
        print(
            "OVERALL F2: "
            "BENCHMARK INVALID"
        )

    elif all(
        x == "SUPPORTIVE"
        for x in outcomes
    ):
        print(
            "OVERALL F2: SUPPORTIVE "
            "UNDER ALL PREREGISTERED "
            "NOISE CONDITIONS"
        )

    else:
        print(
            "OVERALL F2: "
            "PREREGISTERED SUCCESS "
            "CRITERION NOT MET"
        )

    print("=" * 104)


if __name__ == "__main__":
    main()
