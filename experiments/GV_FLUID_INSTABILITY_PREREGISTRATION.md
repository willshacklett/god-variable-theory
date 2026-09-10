# GV Fluid Instability Test — Preregistration

## Purpose

Test whether a pre-specified GV-style constraint-strain metric provides earlier warning of an approaching mathematical instability than conventional observables alone.

This experiment is not evidence that GV is a new physical law.

It is a falsification-oriented benchmark.

## Research Question

At a matched false-positive rate, does a GV-style constraint-strain metric detect an approaching instability earlier than conventional measures?

## Phase F0 — Known Blow-Up ODE

We begin with the equation:

\[
\frac{dx}{dt}=x^2
\]

For initial condition \(x(0)=x_0>0\), the analytic solution is:

\[
x(t)=\frac{x_0}{1-x_0 t}
\]

with finite-time blow-up at:

\[
t_*=\frac{1}{x_0}
\]

This system is chosen because the instability time is known exactly.

## Signals

The following conventional signals will be evaluated:

1. State magnitude

\[
B_1(t)=|x(t)|
\]

2. First derivative magnitude

\[
B_2(t)=\left|\frac{dx}{dt}\right|
\]

3. Second derivative magnitude

\[
B_3(t)=\left|\frac{d^2x}{dt^2}\right|
\]

The GV candidate metric is defined before examining benchmark results as:

\[
GV(t)=
z(\log(1+|x|))
+
z(\log(1+|\dot{x}|))
+
z(\log(1+|\ddot{x}|))
\]

where \(z\) denotes normalization using statistics obtained only from non-blow-up control trajectories.

No component weights will be tuned after viewing test outcomes.

## Controls

Control trajectories use:

\[
\frac{dx}{dt}=-x
\]

which decay toward zero and do not blow up.

Control initial conditions and noise realizations will be used to calibrate thresholds.

## Threshold Calibration

For each detector:

- GV
- \(|x|\)
- \(|dx/dt|\)
- \(|d^2x/dt^2|\)

the alarm threshold will be selected using control data only.

Target false-positive rate:

\[
5\%
\]

Thresholds will not be altered after evaluation on blow-up trajectories.

## Primary Outcome

For every detector that alarms before \(t_*\), calculate:

\[
L=t_* - t_{\text{alarm}}
\]

where \(L\) is warning lead time.

Primary comparison:

\[
\Delta L =
L_{GV} -
\max(L_{B_1},L_{B_2},L_{B_3})
\]

A positive value favors GV.

## Success Criterion

Phase F0 is considered supportive only if:

1. GV respects the matched false-positive rate.
2. GV alarms before blow-up.
3. GV provides greater median lead time than every individual baseline across the preregistered test set.
4. The advantage survives added observational noise.

Passing F0 does not validate GV.

It permits progression to F1.

## Failure Criterion

GV fails F0 if:

- it exceeds the allowed false-positive rate,
- fails to warn before blow-up,
- does not outperform the best conventional observable,
- or loses its apparent advantage under modest noise.

Negative results will be retained.

## Planned Progression

- F0 — analytic blow-up ODE
- F1 — 1-D viscous/inviscid Burgers equation
- F2 — controlled fluid instability simulation
- F3 — 3-D Navier-Stokes trajectory or independently published candidate blow-up data

Later phases proceed only if earlier tests justify them.

## Interpretation Rule

The strongest permitted conclusion from F0 is:

> The preregistered GV candidate metric provided earlier warning than the tested individual conventional observables under the tested conditions.

The following conclusion is not permitted:

> GV has been proven.

