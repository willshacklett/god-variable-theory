# What Has Failed?

Negative results are first-class evidence. **THE GOD VARIABLE HAS NOT BEEN CONFIRMED.**
No formulation gets credit merely for detecting an event that simpler observables
also detect. No post-hoc pattern overrides a frozen success criterion.

## F0: ODE Blow-Up - NOT SUPPORTIVE

- Tested: frozen GV metric on $dx/dt=x^2$, calibrated to 5% trajectory FPR.
- Would support: greater median paired warning lead than every conventional
  baseline, including the declared noisy regime.
- Happened: GV detects events, but lead advantage is zero at 0%, 1%, 5% noise
  and -0.001370 at 10%; $|d^2x/dt^2|$ is as good or better.
- Counts against: the specific additional-warning claim, not a universal theorem
  about every conceivable statistic.
- Learned: an ordinary monotone precursor ($2x^3$) already captures this toy instability.

[Original result](../experiments/GV_FLUID_F0_RESULTS.md).

## F1: Inviscid Burgers - NOT SUPPORTIVE

- Tested: composite warning for analytic shock formation with frozen baselines.
- Would support: positive paired lead advantage at matched control false positives.
- Happened: all median leads tie at every noise level. Control amplitudes
  [0.10,0.40] and active amplitudes [1,2] do not overlap; alarms near the start
  likely measure distribution separation rather than developing precursors.
- Counts against: the preregistered advantage claim. The confound limits the
  strength of a general precursor conclusion; it does not turn a tie into support.
- Learned: overlap initial conditions and separate onset from distribution shift.

[Original result](../experiments/GV_FLUID_F1_RESULTS.md).

## F1b: Forced Viscous Burgers - NOT SUPPORTIVE

- Tested: equal-weight composite under delayed forcing with matched initial families.
- Would support: earlier warning than all baselines in a technically valid benchmark.
- Happened: validity passes, no control events, 160/160 active events. GV paired
  deficits are -0.18, -0.14, -0.066667, -0.04 across the four noise levels.
  Total variation wins at the first three levels; gradient energy at 10%.
- Counts against: the composite's incremental value even after removing F1's confound.
- Learned: combining diagnostics can weaken a strong individual observable;
  shrinking deficit with noise is exploratory, not a positive result.

[Original result](../experiments/GV_FLUID_F1B_RESULTS.md).

## F2: Navier-Stokes - INVALID / INCONCLUSIVE

- Tested: forced 2-D incompressible vorticity dynamics, control-derived event thresholds.
- Would support: first pass all validity gates (including >=70% active events),
  then beat six conventional diagnostics with positive paired lead advantage.
- Happened: solver finite, zero control events, only 20/60 active events (33.3%).
- Counts against: suitability of the selected physical regime as a confirmatory
  benchmark. **It does not count as a valid detector-performance rejection.**
- Learned: freeze a separate corrective regime; do not reinterpret exploratory
  comparisons from the invalid experiment as supportive or NOT SUPPORTIVE.

[Original result](../experiments/GV_FLUID_F2_RESULTS.md).

## F2b: Corrected Navier-Stokes - NOT SUPPORTIVE

- Tested: separately preregistered higher-event regime with unchanged detector rules.
- Would support: pass validity, exceed every baseline's median and retain positive
  paired advantage at all frozen noise levels, including 10%.
- Happened: new 2026-10-05 run passes implemented validity gates with 60/60 events.
  GV warns on 5/60 and 1/60 at 0% and 1%, none at 5% or 10%; vorticity and strain
  warn on all 60 at every level. Paired advantages are negative or undefined.
- Counts against: the frozen composite's warning claim; fixing event incidence did
  not improve its relative performance enough to meet any support criterion.
- Learned: disclose missed events alongside conditional medians. A large median
  among a few baseline detections also does not establish broad reliability.

[New result and numerical limitations](../experiments/GV_FLUID_F2B_RESULTS.md).

## Switch: Failed Identification Methods - NOT SUPPORTIVE

The [original failure notes](../experiments/GV_SWITCH_FAILURE_NOTES.md) preserve:

| Failed approach | What would support it | What happened / why it fails | Lesson |
| --- | --- | --- | --- |
| Naive classifier against random null | Low FPR and high power under realistic conventional alternatives | Easy null looked excellent; its null did not represent instrumental artifacts | Easy-model success cannot establish identification |
| Adversarial null suite | Reject cable and clock artifacts | Both classified anomalous 100%; overall FPR about 33.47% | Distance-time regularity is not distinctive |
| Free linear model comparison | Distinguish physical propagation from clock bias | Unrestricted fit often wins; unexplained rate about 50.98% | Flexibility and nonidentifiability require interventions, not smaller RMS |
| First control matrix | Reject clock as well as cable/noise | Known-mechanism FPR about 21.76% | Direct clock-identity testing is needed |
| First clock correction | Low FPR while retaining injected signal power | FPR=0, TPR=0 | Rejecting everything is not a useful detector |

The corrected synthetic clock slope method is a methodology success, not empirical
GV evidence. EM still survives that gate because EM is a spatial mechanism. Exact
historical reruns are limited by missing superseded implementations/raw trials.

## Unsupported Historical Conclusions

The cosmology/entropy and tether toys lack a locked independent empirical test.
Fitting a known target or imposing damping does not establish constant derivation,
new energy, entropy-law evasion, or eternal behavior. These illustrations are
INVALID / INCONCLUSIVE as evidence, not rebranded positive experiments.

New proposals may be tested, but each failed formulation stays failed. See the
[ledger](EVIDENCE.md) and [anti-goalpost rules](FALSIFICATION.md).