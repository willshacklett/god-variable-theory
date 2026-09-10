# GV Fluid Instability Benchmark — F2 Preregistration

## Purpose

F2 tests whether a preregistered GV-style composite metric provides earlier warning of a developing two-dimensional fluid instability than conventional single-observable diagnostics.

F0 and F1b produced NOT SUPPORTIVE outcomes.
F1 was NOT SUPPORTIVE with a benchmark confound.

F2 is a materially different benchmark and does not modify prior outcomes.

---

## System

We use the two-dimensional incompressible Navier-Stokes equations in vorticity form on a periodic domain:

\[
\partial_t \omega + \mathbf{u}\cdot\nabla\omega
=
\nu\nabla^2\omega
\]

with

\[
\omega = \partial_x v - \partial_y u
\]

and incompressibility:

\[
\nabla\cdot\mathbf{u}=0.
\]

Velocity is recovered from a streamfunction \(\psi\):

\[
\nabla^2\psi=-\omega
\]

with

\[
u=\partial_y\psi,
\qquad
v=-\partial_x\psi.
\]

---

## Domain

The computational domain is:

\[
(x,y)\in[0,2\pi)\times[0,2\pi)
\]

with periodic boundary conditions.

---

## Initial Condition

The initial velocity field is a perturbed shear layer.

A base flow is defined as:

\[
u(y)=U_0\tanh\left(\frac{y-\pi}{\delta}\right)
\]

with a weak perturbation added through the streamfunction.

The perturbation phase is randomized across trajectories.

Active and control trajectories use the same perturbation family.

---

## Control and Active Populations

Controls and active trajectories are drawn from overlapping initial-condition distributions.

Controls use a viscosity range chosen to suppress rapid roll-up during the observation window.

Active trajectories use a lower-viscosity range chosen to permit a Kelvin-Helmholtz-like transition during the observation window.

The parameter ranges will be fixed in the implementation before active-test results are viewed.

---

## Event Definition

The physical event is defined using the noiseless simulation state.

Let enstrophy be:

\[
Z(t)
=
\frac12\int \omega^2\,dA.
\]

Let maximum strain magnitude be:

\[
S_{\max}(t)
=
\max_{x,y}
\sqrt{
2S_{ij}S_{ij}
}.
\]

The event occurs when both:

\[
Z(t)\ge Z_{\text{crit}}
\]

and

\[
S_{\max}(t)\ge S_{\text{crit}}
\]

for the first time.

The event thresholds are fixed in the implementation before benchmark outcomes are viewed.

---

## Conventional Baselines

The following detectors are evaluated independently.

### B1 — Maximum vorticity

\[
B_1(t)=\max|\omega|
\]

### B2 — Enstrophy

\[
B_2(t)=\frac12\int\omega^2\,dA
\]

### B3 — Maximum strain

\[
B_3(t)=S_{\max}(t)
\]

### B4 — Kinetic energy

\[
B_4(t)
=
\frac12
\int
|\mathbf{u}|^2
\,dA
\]

### B5 — Palinstrophy

\[
B_5(t)
=
\frac12
\int
|\nabla\omega|^2
\,dA
\]

### B6 — Dissipation proxy

\[
B_6(t)
=
\nu
\int
|\nabla\omega|^2
\,dA
\]

---

## GV Candidate Metric

The preregistered F2 candidate is:

\[
GV_{F2}
=
\sum_{i=1}^{6}
z\left(
\log(1+B_i)
\right).
\]

Normalization statistics are estimated from control trajectories only.

All six components receive equal weight.

No weights may be tuned after active-test results are viewed.

---

## Noise Conditions

The observational noise levels are:

- 0%
- 1%
- 5%
- 10%

Noise is added to the observed vorticity field used by detectors.

The physical event time is determined only from the noiseless simulation.

---

## Threshold Calibration

Every detector threshold is calibrated using controls only.

Target trajectory-level false-positive rate:

\[
5\%.
\]

---

## Warning Lead Time

For each event-producing active trajectory:

\[
L_D
=
t_{\text{event}}
-
t_{\text{alarm},D}.
\]

Only alarms occurring before the physical event count as warning.

---

## Primary Comparison

For each trajectory:

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

Positive values favor GV.

---

## Benchmark Validity Requirements

F2 is technically valid only if:

1. Numerical integration remains finite and stable.
2. Control trajectories have a low physical-event rate.
3. A sufficient fraction of active trajectories reach the event.
4. GV does not systematically alarm before the two populations dynamically diverge.
5. Thresholds are calibrated from controls only.
6. No detector definition is changed after viewing active outcomes.

If these conditions fail, the result is BENCHMARK INVALID.

---

## Support Criterion

F2 is SUPPORTIVE only if:

1. GV satisfies the matched false-positive requirement.
2. GV detects the event prior to occurrence.
3. GV median warning lead time exceeds every individual conventional baseline.
4. Median paired:

\[
\Delta L>0.
\]

5. The advantage remains positive at 10% noise.

A tie is NOT SUPPORTIVE.

---

## Interpretation

Passing F2 would not establish GV as a law of physics.

The strongest permitted conclusion would be:

> The preregistered GV F2 composite provided earlier warning than the tested individual observables in this two-dimensional fluid-instability benchmark.

A negative result means this preregistered composite did not provide additional warning value.

---

## Research Record

- F0 — NOT SUPPORTIVE
- F1 — NOT SUPPORTIVE; benchmark confound identified
- F1b — NOT SUPPORTIVE; technically valid
- F2 — current two-dimensional fluid-instability benchmark
- F3 — future three-dimensional Navier-Stokes candidate-data benchmark
