# GV Fluid Instability Benchmark — F0 Results

## Outcome

Preregistered result:

**NOT SUPPORTIVE**

## Summary

Across 500 stable controls and 500 blow-up trajectories at each noise level, all detectors were calibrated to a 5% trajectory-level false-positive rate.

GV achieved 100% detection, but did not provide greater median warning lead time than the strongest conventional baseline.

### Results

| Noise | GV median lead | Best baseline | Delta L |
|---|---:|---:|---:|
| 0% | 0.778451 | 0.778451 | 0.000000 |
| 1% | 0.787606 | 0.787606 | 0.000000 |
| 5% | 0.780925 | 0.780925 | 0.000000 |
| 10% | 0.778699 | 0.780069 | -0.001370 |

The strongest baseline was consistently:

\[
\left|\frac{d^2x}{dt^2}\right|
\]

## Interpretation

For the system

\[
\frac{dx}{dt}=x^2,
\]

the second derivative is

\[
\frac{d^2x}{dt^2}=2x^3.
\]

This quantity already provides a very strong monotonic precursor to finite-time blow-up.

The preregistered GV metric therefore did not demonstrate additional predictive value in this system.

This result does not validate GV.

It also does not falsify all possible GV formulations.

It falsifies the specific claim that this preregistered GV metric would outperform the tested conventional observables on the F0 benchmark.

## Next Step

Proceed, if scientifically justified, to F1:

**1-D Burgers equation**

The purpose of F1 is to test a system with spatially distributed structure, nonlinear gradient steepening, and richer competing observables.

No F0 thresholds, weights, or success criteria will be retroactively modified.
