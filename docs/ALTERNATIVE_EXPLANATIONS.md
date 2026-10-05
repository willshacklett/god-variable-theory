# Alternative Explanations

Known and ordinary competing explanations come before claim escalation.
Controls must be validated independently; adding a label to a channel does not
exclude a cause. Freeze tolerances and expected responses before looking at data.

| Alternative | Diagnostic / competing test |
| --- | --- |
| Sensor artifacts | Direct calibrated injection, disconnected inputs, sensor substitution, saturation/bandwidth/latency characterization; retain raw waveforms. |
| Clock synchronization | Independent timebase, channel-skew calibration, randomized clock reassignment and per-clock slopes. |
| Cable delay / trigger pickup | Swap cable IDs/lengths independently of physical distance; measure cable delay directly. |
| EM coupling | Verified shielding attenuation, RF logging, power/orientation/modulation intervention and source-disconnected controls. Near-c timing does not exclude EM. |
| Mechanical vibration | Accelerometer monitoring, source/receiver mechanical decoupling and vibration isolation. |
| Acoustic coupling | Microphone logging, acoustic damping and changes in propagation path/pressure where justified. |
| Thermal drift | Temperature logs, warm/cold controls, randomized trial ordering and sufficient equilibration. |
| Feedback/control loops | Same ordinary controller without proposed GV-specific intervention; matched initial conditions, sham and controller-ablation comparisons. |
| Software/event-loop timing | Hardware timestamps versus software logs, injected scheduling load, trigger-path tracing and latency calibration. |
| Sampling artifacts | Anti-alias filtering, multiple declared sample rates, acquisition dead-time checks, discretization/grid/time-step convergence. |
| Thresholds | Freeze control-derived thresholds and apply unchanged to independent tests; publish threshold sensitivity as exploratory. |
| Multiple testing | Declare all endpoints/windows/sensors; correct the complete search family or use independent confirmation. |
| Data leakage | Separate training/calibration/test trajectories and subjects, including normalization; audit target/event labels and future samples. |
| Selection bias | Retain all trials, negative runs, misses and exclusions; randomized assignment and fixed stopping rules. |
| Initial distribution confounding | Overlap initial observable distributions; quantify pre-intervention alarms. F1 is the cautionary example. |
| Ordinary nonlinear dynamics | Compare frozen conventional observables and control models; demonstrate added predictive value rather than merely complicated dynamics. |
| Observer interpretation | Blinded labels, reproducible automated analysis, independent analysts and externally reviewed claim wording. |
| Model misspecification / unknown ordinary causes | Compare plausible known models and uncertainty; maintain an unresolved attribution rather than filling the gap with GV. |

A failure to measure a control signal may reflect insufficient sensitivity, not
absence of the causal pathway. Controls should cover combinations of effects as
well as single causes. Shared generators in synthetic tests can encode a desired
answer; successful simulation gates do not certify real-world exclusions.

Use the [switch protocol](../experiments/GV_SWITCH_PREREGISTRATION.md) for its
frozen modeled gate order and the [falsification rules](FALSIFICATION.md) for
decisions. A residual is only a residual until known explanations are excluded.