# GV Fluid Instability Benchmark — F2b Preregistration

## Purpose

F2b is a corrective follow-up to F2.

F2 was BENCHMARK INVALID because only 33.3% of active trajectories reached the predefined physical event, below the preregistered minimum of 70%.

F2b changes only physical-regime parameters intended to increase active event incidence.

No detector definition, GV weighting, calibration rule, false-positive target, or success criterion is changed.

---

## Governing System

F2b uses the same two-dimensional forced incompressible Navier-Stokes system in vorticity form as F2:

\[
\partial_t\omega
+
\mathbf{u}\cdot\nabla\omega
=
\nu\nabla^2\omega
+
g(x,y,t).
\]

The computational domain remains:

\[
[0,2\pi)^2
\]

with periodic boundary conditions.

The numerical method remains:

- pseudo-spectral vorticity formulation
- Fourier streamfunction recovery
- spectral derivatives
- 2/3 de-aliasing
- RK4 integration
- zero-mean vorticity enforcement

---

## Initial Condition

The periodic double shear layer is unchanged:

\[
u(y)=
\begin{cases}
U_0\tanh\left(\frac{y-\pi/2}{\delta}\right),
& y\le\pi,\\
U_0\tanh\left(\frac{3\pi/2-y}{\delta}\right),
& y>\pi.
\end{cases}
\]

with:

\[
U_0=1.0
\]

and:

\[
\delta=0.20.
\]

The transverse perturbation remains:

\[
v(x,y)
=
\epsilon\sin(x+\phi)
\]

with:

\[
\epsilon=0.05
\]

and:

\[
\phi\sim U(0,2\pi).
\]

---

## Corrective Physical-Regime Changes

Only the following F2 physical parameters are changed.

### Simulation horizon

F2:

\[
T=1.50
\]

F2b:

\[
T=2.00.
\]

### Forcing amplitude

F2:

\[
F=1.50
\]

F2b:

\[
F=2.00.
\]

### Active viscosity

F2:

\[
\nu_a\sim U(0.008,0.012)
\]

F2b:

\[
\nu_a\sim U(0.004,0.008).
\]

Control viscosity remains unchanged:

\[
\nu_c\sim U(0.080,0.120).
\]

Forcing onset remains:

\[
t_{\rm on}=0.25.
\]

Forcing ramp duration remains:

\[
0.25.
\]

---

## Numerical Parameters

Grid remains:

\[
64\times64.
\]

Integrator time step remains:

\[
dt=0.005.
\]

F2b diagnostic samples:

\[
201.
\]

Control trajectories:

\[
N_c=60.
\]

Active trajectories:

\[
N_a=60.
\]

---

## Physical Event

The event definition remains unchanged.

Control trajectories alone determine:

\[
Z_{\rm crit}
=
Q_{0.95}
\left(
\max_t Z_c(t)
\right)
\]

and:

\[
S_{\rm crit}
=
Q_{0.95}
\left(
\max_t S_{\max,c}(t)
\right).
\]

An active event occurs at the first sampled time when both:

\[
Z>Z_{\rm crit}
\]

and:

\[
S_{\max}>S_{\rm crit}.
\]

Active data are not used to set physical-event thresholds.

---

## Frozen Baselines

The following F2 detectors remain unchanged:

1. maximum vorticity
2. enstrophy
3. maximum strain
4. kinetic energy
5. palinstrophy
6. dissipation proxy

---

## Frozen GV Metric

The equal-weight composite remains:

\[
GV
=
\sum_{i=1}^{6}
z(\log(1+B_i)).
\]

Normalization statistics are obtained only from controls.

No component weights may be changed.

---

## Noise Conditions

The same observational noise conditions are retained:

- 0%
- 1%
- 5%
- 10%

Physical event times remain based on noiseless simulations.

---

## Calibration

Every detector is independently calibrated using controls only.

Target trajectory-level false-positive rate:

\[
5\%.
\]

---

## Validity Requirements

F2b is BENCHMARK INVALID if:

1. the numerical solver becomes non-finite,
2. control physical-event rate exceeds 10%,
3. active physical-event rate is below 70%,
4. GV alarms at \(t=0\) in more than 10% of active trajectories,
5. control-only calibration is violated.

---

## Warning Lead Time

For detector \(D\):

\[
L_D
=
t_{\rm event}
-
t_{\rm alarm,D}.
\]

Only alarms before the physical event count.

---

## Primary Comparison

\[
\Delta L
=
L_{GV}
-
\max(
L_{B_1},
L_{B_2},
L_{B_3},
L_{B_4},
L_{B_5},
L_{B_6}
).
\]

---

## Support Criterion

F2b is SUPPORTIVE only if:

1. the benchmark passes all validity requirements,
2. GV satisfies the matched false-positive requirement,
3. GV warns before the physical event,
4. GV median warning lead time exceeds every individual baseline,
5. median paired \(\Delta L>0\),
6. the advantage remains positive at 10% observational noise.

A tie is NOT SUPPORTIVE.

---

## Interpretation

Passing F2b would not prove GV or establish a new law of physics.

The strongest permitted statement would be:

> The preregistered GV composite provided earlier warning than the tested individual observables in the valid F2b two-dimensional flow benchmark.

A negative result means the frozen GV composite did not provide additional warning value.

---

## Research Record

- F0 — NOT SUPPORTIVE
- F1 — NOT SUPPORTIVE; confounded
- F1b — NOT SUPPORTIVE; valid
- F2 — BENCHMARK INVALID
- F2b — current corrective benchmark
- F3 — future 3-D Navier-Stokes candidate-data benchmark

No F2b result existed when this preregistration was written.
