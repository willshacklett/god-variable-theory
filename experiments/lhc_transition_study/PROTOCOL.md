# Prospective LHC transition protocol v0.1

**Draft preregistration — not frozen, not run, no physical evidence.**
This observational study cannot establish intervention causality or exclude all
ordinary explanations. It does not test a specified physical GV law.

## Hypotheses and estimand

H0: conditional on measured state/history and defensible ordinary-physics and
instrument models, held-out event-window residuals have no reproducible excess
over matched control windows beyond the calibrated uncertainty.

H1: at least one prespecified transition class shows a repeatable excess that
survives the prespecified known-cause controls, multiplicity correction and
independent replication. H1 is a residual candidate, not GV detection.

For the selected channel, define r(t) = observed(t) - predicted(t) in its physical
unit. Primary endpoint: per-fill contrast between the time-weighted mean residual
in a fixed command-relative window and matched pseudo-event windows. Define
weights from actual integration intervals, not assumed uniform sampling.
Freeze the sign/direction, window, channel, uncertainty model and scientifically
meaningful minimum effect delta before confirmation. Secondary response-relative
and cross-channel endpoints must be separately declared and corrected.

## Transitions and timestamps

Study injection, acceleration ramp, adjustment/stable-beam entry, beam dump and
non-colliding transitions as separate strata. Record both beam identifiers,
machine configuration and collision status per interaction point.
Use an independent command/event record for t0, not a residual-selected peak.
Record measured actuator/beam response t1 independently, with clock uncertainty.
Beam-mode publication timestamps are a distinct marker, not assumed t0 or t1.
No timestamp may be inferred to make a residual align.

## Data and validity gates

Only real data with authorized provenance, hashes, schemas, units, clocks,
calibration, latency/integration metadata and synchronized channels qualify.
Quantify clock offsets/drift, sensor response, bandwidth and saturation first.
Required channels should cover command/mode, current or field response, energy,
beam intensity/losses, collision status, thermal/environment and independent
reference measurements, where available. These are requirements, not claims of
available NXCALS variables.

Reject or declare inconclusive: unresolved clock semantics, timing uncertainty
too large for the endpoint, missing critical history/calibration, uncontrolled
saturation or gaps, no suitable independent references, insufficient independent
fills or sensitivity, or unauthorized data. Freeze numerical validity thresholds
after a separate instrument/noise pilot. Retain all rejection counts/reasons.
No interpolation across transition gaps. Preserve raw data unchanged.

## Known mechanisms and prior history

| Mechanism/confounder | Required modeling/control |
| --- | --- |
| Magnetic hysteresis | Prior current/field path, polarity, precycle and previous ramp history; compare matched histories and ordinary magnet response models. |
| Persistent currents, decay/snapback | Injection dwell, preceding excitation, ramp rate and magnet conditions; compare history-dependent alternatives. |
| Beam losses and dumps | Intensity, loss-monitor response/integration, dump reason, kicker/extraction response and protection timing; separate intentional/protection dumps. |
| Electromagnetic transients | Converter/RF/kicker switching, grounding/cabling, shielding and common-mode reference; test expected latencies and channel coupling. |
| Thermal/cryogenic relaxation | Temperature, thermal dwell and load history; model slow relaxation and distinguish ramp from heating. |
| Detector timing and instrument artifacts | Clock offset/drift, trigger latency/dead time, integration, aliasing, gain changes, clipping, missing logs, resampling and software timestamps. |
| Operational selection | Fill schedule, maintenance/configuration changes, operator decisions and previous failures; stratify rather than pool incompatible configurations. |

History covariates include prior fills/dumps, time since reset/precycle, injection
dwell, ramp path/rate, temperature and prior beam conditions. Unknown history is
not zero history. This table is a modeling checklist, not verified CERN findings.

## Controls and analysis separation

- Use independent command and response markers; test sensitivity to certified
  timing uncertainty and physically plausible delays.
- Match pseudo-events to configuration/history, time within fill and equal-length
  windows without transitions. Use fixed guard intervals to avoid contamination.
- Independently verify non-colliding operation. No collisions does not mean no
  beam, magnetic switching, heat, losses or electromagnetic signals.
- Include beam-absent/reference controls when available, pre-event windows and
  time-shifted/channel-shuffled negative controls preserving serial dependence.
- Fit K only on development/training fills; compare history-dependent physical
  baselines and instrument/state-space alternatives, not merely a constant.
- Split by whole fills and chronological run/configuration blocks; never split
  adjacent samples randomly. Hold replication periods aside before inspection.
- Treat fills/independent blocks, not individual samples, as independent units.
  Use a preregistered block-resampling or equivalent serial-dependence method.
  Match/control observational confounding; do not claim randomized intervention.

## Freeze gate, success and failure

Before opening confirmatory data, archive a dated, hashed protocol and analysis
version with: dataset identifiers, train/test/replication fills, transition/channel
family, t0 rule, windows/guards, delta in physical units, calibration/timing limits,
history covariates, model family/hyperparameters, missing/exclusion rules, sample
size and power calculation, uncertainty/resampling method and replication rule.
All presently unspecified numerical entries are **blocking**, not tunable after
an anomaly. No confirmatory p-values may be reported from this draft.

Proposed family-wise alpha is 0.05 using Holm correction across all declared
transition/channel primary tests. Freeze the family and any secondary family
separately. Candidate success requires a corrected held-out rejection, effect
exceeding delta with uncertainty bounds, clean negative controls, robustness to
the frozen ordinary alternatives, and independent replication with the same
direction and prespecified magnitude tolerance. A shared sensor or clock failure
does not constitute cross-sensor replication.

Adequately powered bounds excluding effects of size delta support a bounded null
for the tested conditions only. Lack of significance without that sensitivity is
inconclusive, not proof of absence. Effects explained by a known mechanism fail
the unexplained-residual hypothesis. Failed validity gates or replication mean no
candidate claim. Publish nulls, failures, exclusions and model sensitivities;
record amendments prospectively and label post-hoc work exploratory.
