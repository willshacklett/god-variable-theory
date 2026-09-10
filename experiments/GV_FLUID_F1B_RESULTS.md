# GV Fluid Instability Benchmark — F1b Results

## Outcome

Preregistered result:

**NOT SUPPORTIVE**

The corrective F1b benchmark passed its technical validity checks.

- Solver remained finite and stable.
- Control physical events: 0.
- Active physical events: 160/160.
- Active event fraction: 1.000.
- GV pre-forcing alarm rate remained below the preregistered validity threshold at all noise levels.
- All detectors were calibrated to a 5% trajectory-level control false-positive rate.

## Results

| Noise | GV Median Lead | Best Baseline | Best Baseline Lead | Median Paired Delta L |
|---|---:|---|---:|---:|
| 0% | 0.192609 | Total variation | 0.372861 | -0.180000 |
| 1% | 0.232775 | Total variation | 0.370079 | -0.140000 |
| 5% | 0.287653 | Total variation | 0.358110 | -0.066667 |
| 10% | 0.307900 | Gradient energy | 0.342609 | -0.040000 |

GV detected the developing event on 100% of event-producing active trajectories at all preregistered noise levels.

However, GV did not exceed the strongest individual conventional baseline at any noise level.

Therefore the preregistered F1b success criterion was not met.

## Interpretation

F1b provides a cleaner negative result than F1.

Because active and control trajectories were generated from the same initial-condition family and evolved identically prior to delayed forcing, the initial-distribution confound identified in F1 was removed.

Under these conditions, the preregistered equal-weight GV composite provided warning of the developing compression event, but did not provide additional lead time beyond the strongest conventional observable.

## Post-Hoc Observation

The GV deficit relative to the strongest baseline decreased as observational noise increased:

\[
-0.180000,\;
-0.140000,\;
-0.066667,\;
-0.040000.
\]

This pattern was not part of the preregistered success criterion and is not interpreted as evidence supporting GV.

It may motivate a separately preregistered experiment testing robustness to measurement noise.

No F1b metric, threshold, weighting, event definition, or success criterion will be retroactively modified.

## Research Record

- F0 — NOT SUPPORTIVE
- F1 — NOT SUPPORTIVE; initial-distribution confound identified
- F1b — NOT SUPPORTIVE; technically valid corrective benchmark
- F2 — next richer fluid-instability benchmark
- F3 — future 3-D Navier-Stokes candidate-data benchmark
