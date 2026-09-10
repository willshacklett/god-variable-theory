# GV Fluid Instability Benchmark — F2 Pre-Implementation Amendment

## Status

This amendment is recorded before the F2 implementation is executed and before any F2 benchmark result is viewed.

The original F2 preregistration remains unchanged in the research record.

Two physical/numerical issues were identified during implementation review.

---

## Correction 1 — Periodic Shear Layer

The original preregistration described a single hyperbolic-tangent shear layer on a doubly periodic domain.

A single tanh profile is not periodic across the y boundary.

F2 will therefore use a periodic double shear layer.

The base x-velocity is:

\[
u(y)=
\begin{cases}
U_0\tanh\left(\frac{y-\pi/2}{\delta}\right),
& y\le\pi,\\
U_0\tanh\left(\frac{3\pi/2-y}{\delta}\right),
& y>\pi.
\end{cases}
\]

A weak periodic transverse perturbation is added:

\[
v(x,y)
=
\epsilon\sin(x+\phi).
\]

The phase:

\[
\phi\sim U(0,2\pi)
\]

is randomized independently for each trajectory.

---

## Correction 2 — Enstrophy Event

For unforced two-dimensional incompressible Navier-Stokes flow,

\[
\frac{d}{dt}
\left(
\frac12\int\omega^2\,dA
\right)
=
-\nu
\int|\nabla\omega|^2\,dA
\le 0.
\]

Therefore an event defined by spontaneous growth of total enstrophy would be inappropriate for the originally specified unforced system.

F2 will instead use a common delayed periodic forcing term.

The governing equation becomes:

\[
\partial_t\omega
+
\mathbf{u}\cdot\nabla\omega
=
\nu\nabla^2\omega
+
g(x,y,t).
\]

For:

\[
t<t_{\rm on},
\]

\[
g=0.
\]

For:

\[
t\ge t_{\rm on},
\]

a smooth ramp is applied:

\[
g(x,y,t)
=
r(t)F\cos(2y),
\]

where

\[
r(t)
=
\min
\left(
1,
\frac{t-t_{\rm on}}{0.25}
\right).
\]

The same forcing is applied to control and active populations.

---

## Fixed Parameters

The following implementation values are fixed before F2 results are viewed:

\[
U_0=1.0
\]

\[
\delta=0.20
\]

\[
\epsilon=0.05
\]

\[
t_{\rm on}=0.25
\]

\[
F=1.5
\]

Domain:

\[
[0,2\pi)^2
\]

Grid:

\[
64\times64
\]

Simulation horizon:

\[
T=1.50
\]

Integrator time step:

\[
dt=0.005
\]

Saved diagnostic samples:

\[
151
\]

Control trajectories:

\[
N_c=60
\]

Active trajectories:

\[
N_a=60
\]

---

## Viscosity Populations

Controls:

\[
\nu_c\sim U(0.080,0.120)
\]

Active trajectories:

\[
\nu_a\sim U(0.008,0.012)
\]

The initial-condition family and forcing protocol are otherwise identical.

---

## Event Thresholds

Physical event thresholds are derived exclusively from noiseless control trajectories.

Let:

\[
Z(t)=\frac12\int\omega^2\,dA
\]

and

\[
S_{\max}(t)
=
\max\sqrt{2S_{ij}S_{ij}}.
\]

Define:

\[
Z_{\rm crit}
=
Q_{0.95}
\left(
\max_t Z_c(t)
\right)
\]

and

\[
S_{\rm crit}
=
Q_{0.95}
\left(
\max_t S_{\max,c}(t)
\right).
\]

An active physical event occurs at the first sampled time at which:

\[
Z(t)>Z_{\rm crit}
\]

and

\[
S_{\max}(t)>S_{\rm crit}.
\]

Active trajectories are never used to select these thresholds.

---

## Numerical Method

The implementation will use a pseudo-spectral vorticity solver with:

- Fourier recovery of streamfunction
- spectral spatial derivatives
- 2/3 de-aliasing of nonlinear terms
- fourth-order Runge-Kutta integration
- zero-mean vorticity mode enforcement

---

## Detector Definitions

The original F2 detector definitions remain unchanged:

- maximum vorticity
- enstrophy
- maximum strain
- kinetic energy
- palinstrophy
- dissipation proxy
- equal-weight GV composite

No detector weight will be fitted using active trajectories.

---

## Noise Conditions

The preregistered observational noise conditions remain:

- 0%
- 1%
- 5%
- 10%

Noise affects detector observations only.

Physical event times are always determined from the noiseless state.

---

## Additional Validity Requirements

The implementation will report BENCHMARK INVALID if:

- the numerical solver becomes non-finite,
- more than 10% of control trajectories meet the physical event definition,
- fewer than 70% of active trajectories reach the physical event,
- GV alarms at \(t=0\) in more than 10% of active trajectories,
- or control-only calibration is violated.

---

## Success Criterion

The original F2 success criterion remains unchanged.

GV must beat every individual conventional baseline at matched false-positive rate and retain a positive median paired lead-time advantage through the 10% noise condition.

A tie remains NOT SUPPORTIVE.

No F2 result existed when this amendment was written.
