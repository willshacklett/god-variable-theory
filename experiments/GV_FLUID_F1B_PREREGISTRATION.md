# GV Fluid Instability Benchmark — F1b Preregistration

## Purpose

F1b is a corrective benchmark motivated by the post-hoc confound identified in F1.

F1 remains NOT SUPPORTIVE and will not be altered.

The purpose of F1b is to test developing instability in a spatially distributed nonlinear system while eliminating the initial-distribution separation between stable and unstable trajectories.

---

## System

We use the one-dimensional forced viscous Burgers equation:

\[
u_t + u u_x = \nu u_{xx} + f(x,t)
\]

on the periodic domain:

\[
x \in [0,2\pi).
\]

Viscosity is fixed before evaluation.

Control and active trajectories use the same initial-condition distribution.

---

## Initial Conditions

Each trajectory begins from:

\[
u(x,0)
=
A\sin(x)
+
0.15A\sin(2x+\phi)
\]

with:

\[
A \sim U(0.60,1.00)
\]

and:

\[
\phi \sim U(0,2\pi).
\]

The same initial-condition distribution is used for controls and active tests.

No class label can therefore be inferred solely from the amplitude range.

---

## Delayed Forcing

Forcing is absent during an initial common evolution period.

For:

\[
t<t_{\text{on}},
\]

both control and active trajectories satisfy:

\[
f(x,t)=0.
\]

The forcing onset is fixed at:

\[
t_{\text{on}}=0.25.
\]

Active trajectories subsequently receive a smooth ramped forcing:

\[
f(x,t)
=
r(t)K\sin(x),
\]

where:

\[
r(t)
=
\min
\left(
1,
\frac{t-t_{\text{on}}}{0.20}
\right)
\]

for \(t\ge t_{\text{on}}\).

Controls continue with:

\[
f(x,t)=0.
\]

Because active and control trajectories are drawn from the same initial-condition distribution and evolve under identical equations before forcing onset, detectors cannot distinguish the two populations from the initial state alone.

---

## Event Definition

F1b evaluates warning of a developing compression event.

The underlying noiseless field defines the event.

Let:

\[
C(t)=-\min_x u_x.
\]

The event occurs at the first time:

\[
C(t)\ge C_{\text{crit}}.
\]

The event threshold will be fixed in the implementation before benchmark results are viewed.

Observational noise does not determine event time.

---

## Conventional Baselines

The following observables are evaluated independently:

### B1 — Maximum gradient

\[
B_1=\max_x|u_x|
\]

### B2 — Maximum curvature

\[
B_2=\max_x|u_{xx}|
\]

### B3 — Total variation

\[
B_3=\int |u_x|dx
\]

### B4 — Gradient energy

\[
B_4=\int u_x^2dx
\]

### B5 — Maximum compression

\[
B_5=-\min_x u_x
\]

---

## GV Candidate

The preregistered F1b candidate metric is:

\[
GV_{F1b}
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

Normalization uses control data only.

All components have equal weight.

No weights will be tuned after viewing active-test results.

---

## Noise Conditions

Observational noise levels are fixed at:

- 0%
- 1%
- 5%
- 10%

Noise is applied to the observed field used by detectors.

The physical event time is always measured from the noiseless simulated field.

---

## Control Calibration

Each detector threshold is calibrated from control trajectories only.

The target trajectory-level false-positive rate is:

\[
5\%.
\]

---

## Warning Lead Time

For each active trajectory that reaches the event:

\[
L_D
=
t_{\text{event}}
-
t_{\text{alarm},D}.
\]

Only alarms occurring before the event contribute positive warning lead time.

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
L_{B_5}
).
\]

Positive values favor GV.

---

## Benchmark Validity Checks

F1b is considered technically valid only if:

1. Control and active initial-condition distributions are generated from the same specified family.
2. Control and active dynamics are identical before forcing onset.
3. Detectors do not systematically alarm before forcing onset solely because of class membership.
4. The numerical solver remains finite and stable before event termination.
5. A sufficient fraction of active trajectories reach the predefined event.

Failure of these conditions is reported as BENCHMARK INVALID rather than interpreted as evidence for or against GV.

---

## Support Criterion

F1b is SUPPORTIVE only if:

1. GV satisfies the matched false-positive requirement.
2. GV detects the event before occurrence.
3. GV median lead time exceeds every individual conventional baseline.
4. Median paired:

\[
\Delta L>0.
\]

5. The advantage remains positive at 10% observational noise.

A tie is NOT SUPPORTIVE.

---

## Interpretation

Passing F1b would not establish GV as a physical law.

The strongest permitted conclusion would be:

> The preregistered GV F1b composite provided earlier warning than the tested individual observables in this forced viscous Burgers benchmark.

Failure would mean that this preregistered GV formulation did not demonstrate added warning value.

---

## Research Record

- F0 — NOT SUPPORTIVE
- F1 — NOT SUPPORTIVE; initial-distribution confound identified
- F1b — paired forced-viscous corrective benchmark
- F2 — future richer fluid instability benchmark
- F3 — future 3-D Navier-Stokes candidate-data benchmark
