# GV Fluid Instability Benchmark — F1 Preregistration

## Purpose

F1 tests whether a preregistered GV-style spatial constraint-strain metric provides earlier warning of gradient catastrophe in a nonlinear distributed system than conventional field observables.

F0 did not support the preregistered GV metric.

F1 is a distinct test and will not modify or reinterpret F0.

---

## System

We use the one-dimensional inviscid Burgers equation:

\[
u_t + u u_x = 0
\]

with periodic boundary conditions.

For smooth initial data \(u_0(x)\), characteristics satisfy:

\[
x = \xi + t u_0(\xi)
\]

and shock formation occurs when characteristics intersect.

The analytic shock time is:

\[
t_* =
-\frac{1}{\min_x u_0'(x)}
\]

when:

\[
\min_x u_0'(x) < 0.
\]

For the reference family:

\[
u_0(x)=A\sin(x),
\]

the shock time is:

\[
t_*=\frac{1}{A}.
\]

---

## Primary Question

At a matched 5% trajectory-level false-positive rate, does the preregistered GV spatial-strain metric provide greater median warning lead time before \(t_*\) than every individual conventional baseline?

---

## Conventional Baselines

The following quantities will be evaluated independently.

### B1 — Maximum gradient

\[
B_1(t)=\max_x |u_x|
\]

### B2 — Maximum curvature

\[
B_2(t)=\max_x |u_{xx}|
\]

### B3 — Total variation

\[
B_3(t)=
\int |u_x|\,dx
\]

### B4 — Gradient energy

\[
B_4(t)=
\int u_x^2\,dx
\]

### B5 — Maximum local compression

\[
B_5(t)=
-\min_x u_x
\]

---

## GV Candidate Metric

The F1 GV metric is fixed before evaluation as:

\[
GV_{F1}(t)
=
z(\log(1+B_1))
+
z(\log(1+B_2))
+
z(\log(1+B_3))
+
z(\log(1+B_4))
+
z(\log(1+B_5)).
\]

Normalization statistics are estimated using control trajectories only.

All five components receive equal weight.

No weights may be tuned after test results are observed.

---

## Controls

Controls use the same Burgers dynamics but initial amplitudes whose analytic shock times occur beyond the observation horizon.

Control family:

\[
u_0(x)=A\sin(x)
\]

with:

\[
A \in [0.10,0.40].
\]

Observation horizon:

\[
T=1.
\]

Therefore:

\[
t_*=\frac1A \geq 2.5,
\]

and no control trajectory should form a shock during the observation window.

---

## Test Trajectories

Primary test amplitudes:

\[
A \in [1.0,2.0].
\]

Therefore:

\[
t_* \in [0.5,1.0].
\]

Simulation data will stop before the analytic shock time to avoid interpreting post-shock numerical regularization as precursor information.

---

## Noise Conditions

The preregistered observational noise levels are:

- 0%
- 1%
- 5%
- 10%

Noise is added to the observed field before diagnostic quantities are calculated.

---

## Threshold Calibration

Every detector is calibrated independently using control trajectories only.

Target trajectory-level false-positive rate:

\[
5\%.
\]

For each detector, an alarm threshold is based on the distribution of the maximum detector value observed over each control trajectory.

Test trajectories are not used during threshold calibration.

---

## Alarm Time

For detector \(D\):

\[
t_{\text{alarm},D}
=
\min
\{t:D(t)>\theta_D\}.
\]

Warning lead time is:

\[
L_D=t_*-t_{\text{alarm},D}.
\]

---

## Primary Comparison

Let:

\[
L_{\text{best baseline}}
=
\max(
L_{B_1},
L_{B_2},
L_{B_3},
L_{B_4},
L_{B_5}
).
\]

Then:

\[
\Delta L
=
L_{GV}
-
L_{\text{best baseline}}.
\]

Positive \(\Delta L\) favors GV.

---

## Success Criterion

F1 is supportive only if, at every preregistered noise level:

1. GV remains within the allowed matched false-positive tolerance.
2. GV detects the approaching shock on the test trajectories.
3. GV has greater median warning lead time than every individual baseline.
4. Median:

\[
\Delta L>0.
\]

5. The advantage does not disappear under the preregistered 10% noise condition.

All conditions must be satisfied.

---

## Failure Criterion

F1 is NOT SUPPORTIVE if any required condition fails.

A tie with the strongest baseline is not considered supportive.

No GV weights, thresholds, components, noise conditions, or success criteria may be altered after results are viewed.

---

## Interpretation

Passing F1 would not establish GV as a physical law.

The strongest permitted statement would be:

> The preregistered GV F1 composite provided earlier warning than the tested individual conventional observables for the tested Burgers shock-formation benchmark.

Failure means that this preregistered GV formulation did not demonstrate additional predictive value on F1.

---

## Progression

- F0 — analytic one-variable blow-up: completed, NOT SUPPORTIVE
- F1 — 1-D Burgers gradient catastrophe: current
- F2 — richer fluid instability simulation
- F3 — three-dimensional Navier-Stokes candidate trajectory/data

Progression does not erase negative results from earlier phases.
