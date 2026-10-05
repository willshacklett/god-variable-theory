# GV Fluid Instability Benchmark - F2b Results

## Outcome

**NOT SUPPORTIVE**

This is a new computational run on 2026-10-05, not a recovered historical result.
The frozen script and [preregistration](GV_FLUID_F2B_PREREGISTRATION.md) at
`e5711b10fbce7f4949e62ee31db0c2216e19652a` were not modified.
Python 3.11.16; NumPy 2.4.6; Debian Linux; seed 20260910.

Reproduce from the repository root:

```bash
python experiments/gv_fluid_f2b_2d_test.py
```

The script prints to stdout and does not save raw trajectories. Its banner and
per-noise verdict labels still say F2; the filename, parameters, and final
`OVERALL F2b` line identify this corrective experiment. That historical cosmetic
defect is left intact to avoid altering the tested code.

## Implemented Validity Checks

- Grid 64 x 64; dt 0.005; horizon 2.00; 201 diagnostic samples.
- Solver finite: true. This is the code's finite-value check, not a convergence study.
- Control physical events: 0/60; active physical events: 60/60.
- Thresholds: enstrophy 74.670857, maximum strain 5.018401.
- GV initial-time alarm rate: 0 at all four noise levels.
- GV trajectory-level control false-positive rate: 0.050 at each noise level.

## Results

| Noise | GV pre-event detections | GV median lead | Maximum-vorticity detection / lead | Maximum-strain detection / lead | Median paired delta L |
| --- | --- | --- | --- | --- | --- |
| 0% | 5/60 | 0.010000 | 60/60 / 0.640000 | 60/60 / 0.635000 | -0.760000 |
| 1% | 1/60 | 0.010000 | 60/60 / 0.625000 | 60/60 / 0.625000 | -0.740000 |
| 5% | 0/60 | undefined | 60/60 / 0.565000 | 60/60 / 0.595000 | undefined |
| 10% | 0/60 | undefined | 60/60 / 0.610000 | 60/60 / 0.560000 | undefined |

Lead times are simulation-time units. Medians exclude missed alarms in the existing
implementation; they must be read with detection fractions. Paired delta uses the
best available baseline on each paired trajectory, not subtraction of population
medians. Undefined values are not zero or positive evidence.

The script reports palinstrophy as the largest conditional median at 1%, 5%, and
10% noise (1.450000, 1.410000, 1.435000), but it detects only 3/60, 1/60, and
4/60 events respectively. At zero noise its empirical FPR is 0, not 5%.
Conditional medians alone therefore do not rank general baseline quality.

## Interpretation and Limitations

The frozen composite does not beat simpler baselines and fails the preregistered
support criterion at every noise level. The corrected regime resolves F2's low
event-incidence failure, but does not rescue this GV formulation. No weights,
thresholds, or success criteria were changed.

This is simulated ordinary fluid dynamics, not physical replication or evidence
for a new mechanism. Controls are reused for fitting and empirical calibration,
not independent held-out FPR validation. A finite solver is not proof of numerical
accuracy; grid/time-step convergence and independent statistical review remain
needed. The historical F2 verdict remains INVALID.