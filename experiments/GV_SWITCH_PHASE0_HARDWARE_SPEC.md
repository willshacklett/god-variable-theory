# GV Switch Phase 0 Hardware Specification

Protocol family: **GV-SWITCH**

Status: **Hardware validation design**

Purpose:

> Build an apparatus that can correctly detect and classify known timing, cable, electromagnetic, acoustic, mechanical, and thermal artifacts before any unexplained-signal search is attempted.

Phase 0 is not a GV detection experiment.

---

## 1. Phase 0 Objective

The apparatus must demonstrate that it can:

- timestamp a trigger event
- timestamp remote detector responses
- measure channel latency
- detect cable-delay effects
- detect EM coupling
- detect acoustic propagation
- detect mechanical vibration
- detect thermal drift
- distinguish active from sham trials
- preserve an audit trail

The system must fail safely when timing quality is insufficient.

---

## 2. Core Timing Requirement

For light-speed propagation:

\[
t=\frac{d}{c}
\]

At 1 meter:

\[
t \approx 3.34\ \mathrm{ns}
\]

At 8 meters:

\[
t \approx 26.7\ \mathrm{ns}
\]

Initial target:

\[
\sigma_t \le 1\ \mathrm{ns}
\]

Preferred target:

\[
\sigma_t \le 0.5\ \mathrm{ns}
\]

If verified timing uncertainty exceeds the signal delay being tested, no c-like propagation claim is permitted.

---

## 3. Apparatus Architecture

Required subsystems:

1. trigger source
2. trigger timestamp channel
3. six detector channels
4. data acquisition system
5. cable-delay calibration system
6. RF monitor
7. acoustic monitor
8. vibration monitor
9. temperature monitor
10. sham-trigger controller
11. randomized channel assignment record
12. analysis workstation

---

## 4. Trigger Source

Phase 0 should use an ordinary, reproducible switching event.

Candidate mechanisms:

- relay closure
- transistor-switched load
- optical interrupter
- capacitor discharge into a known low-energy load
- pulse generator output

Preferred characteristics:

- low timing jitter
- measurable reference edge
- repeatable for thousands of trials
- sham mode available
- no hazardous energy required

---

## 5. Trigger Timestamp

Required fields:

- trial ID
- trigger timestamp
- active/sham state
- trigger voltage
- trigger current if measured
- control configuration
- randomization seed

The timestamp reference must not depend on the same uncertain path as the detector signal.

---

## 6. Detector Geometry

Initial geometry:

| Detector | Distance |
|---|---:|
| D1 | 0.25 m |
| D2 | 0.50 m |
| D3 | 1.00 m |
| D4 | 2.00 m |
| D5 | 4.00 m |
| D6 | 8.00 m |

Detector identity must remain separable from physical position.

---

## 7. Detector Requirements

Each detector channel should have:

- repeatable threshold behavior
- known latency
- measured timing jitter
- adequate bandwidth
- independent channel ID
- swappable physical assignment

---

## 8. Data Acquisition

DAQ must support:

- synchronized multichannel acquisition
- sub-nanosecond or low-nanosecond timing where feasible
- external trigger input
- waveform or edge-timestamp capture
- deterministic channel labeling
- raw data export

The timing instrument must be independently benchmarked before use.

---

## 9. Cable Calibration

For each cable record:

- cable ID
- cable type
- cable length
- measured propagation delay
- connector type
- channel assignment

Cable delay must be measured rather than inferred only from length.

Phase 0 must include deliberate cable swaps.

---

## 10. RF / Electromagnetic Monitoring

Required controls:

- broadband RF monitoring
- trigger-correlated transient monitoring
- shielding-state record
- altered source power
- altered conductor orientation
- modulation disabled
- source disconnected while logical trial flow remains intact

A response that tracks these controls should be classified as:

`KNOWN EM CHANNEL`

---

## 11. Acoustic Monitoring

Required:

- microphone channel
- trigger-relative timestamp
- amplitude record

Validation:

- inject known acoustic pulse
- recover approximately expected sound propagation
- classify as acoustic

---

## 12. Mechanical Monitoring

Required:

- accelerometer or vibration sensor
- source-side vibration monitoring
- detector-side vibration monitoring where practical

Validation:

- deliberately inject vibration
- vary mounting/isolation
- verify response follows mechanical coupling

---

## 13. Thermal Monitoring

Record:

- ambient temperature
- source temperature
- detector-region temperature

Validation:

- introduce controlled thermal drift
- verify baseline changes are detected
- verify thermal drift is not classified as fast propagation

---

## 14. Sham Trials

Recommended initial split:

\[
50\% \text{ active}
\]

\[
50\% \text{ sham}
\]

A sham trial should preserve:

- software path
- timing record
- analysis path
- trial metadata

while omitting the physical activation.

---

## 15. Randomization

Randomize:

- active/sham state
- detector/channel assignment
- cable assignment
- timing-channel assignment
- control-state order

Store all randomization seeds.

---

## 16. Phase 0 Calibration Experiments

### Test A — Trigger Repeatability

Measure trigger jitter.

Target:

\[
\sigma_{trigger}\le1\ \mathrm{ns}
\]

### Test B — Cable Delay

Inject known electrical edge through different cable paths.

Required:

- measured delay follows cable path
- cable swap moves the delay with the cable
- classifier identifies cable artifact

### Test C — EM Pulse

Inject controlled EM coupling.

Required:

- shielding changes response
- source-power changes response
- orientation/control state changes response
- classifier identifies EM channel

### Test D — Acoustic Pulse

Inject known sound.

Required approximate behavior:

\[
v \approx 343\ \mathrm{m/s}
\]

Classifier must identify acoustic channel.

### Test E — Mechanical Pulse

Inject controlled vibration.

Classifier must identify mechanical channel.

### Test F — Clock / Timing Bias

Introduce controlled offset or timing skew.

Required:

- apparent signal follows timing-channel identity
- channel reassignment exposes artifact
- classifier rejects it

### Test G — Thermal Drift

Introduce controlled temperature change.

Required:

- drift is detected
- drift is not interpreted as c-like propagation

---

## 17. Phase 0 Acceptance Criteria

Required score:

\[
7/7
\]

Required tests:

1. trigger repeatability
2. cable delay
3. electromagnetic
4. acoustic
5. mechanical
6. clock/timing
7. thermal

No known injected mechanism may be classified as:

`UNEXPLAINED PROPAGATION CANDIDATE`

---

## 18. Failure Conditions

Phase 0 fails if:

- timing precision is inadequate
- channel latency cannot be calibrated
- cable artifacts survive as candidates
- clock artifacts survive as candidates
- EM artifacts survive as candidates
- environmental artifacts survive as candidates
- sham trials produce unexplained trigger-locked structure
- raw data cannot be reproduced from the audit record

---

## 19. Budget Tiers

### Tier 1 — Proof of Measurement

Purpose:

Validate basic timing and known-channel classification.

Likely components:

- oscilloscope
- simple pulse source
- detector channels
- microphone
- accelerometer
- temperature sensors
- RF probe
- shielded cables
- basic shielding

This level may not support a credible sub-nanosecond propagation claim.

### Tier 2 — Serious Timing Bench

Purpose:

Sub-nanosecond to low-nanosecond characterization.

Likely components:

- high-bandwidth oscilloscope or TDC
- calibrated pulse source
- characterized cables
- stable reference clock
- improved shielding
- quality probes
- deterministic trigger hardware

### Tier 3 — Replication Grade

Purpose:

Independent scientific replication.

Likely additions:

- metrology-grade timing hardware
- redundant sensors
- controlled environment
- independent time reference
- documented calibration
- external replication

---

## 20. Recommended Purchase Order

1. timing instrument
2. pulse/trigger source
3. cable calibration accessories
4. detector channels
5. RF monitor
6. microphone
7. accelerometer
8. temperature logging
9. shielding
10. isolation hardware

Timing hardware comes first because it determines what propagation scale can actually be measured.

---

## 21. Software Deliverables

Phase 0 should produce:

- raw waveform/timestamp data
- calibration metadata
- randomized trial manifest
- environmental log
- classification result
- protocol audit JSON

Every output should include:

- protocol version
- apparatus configuration ID
- trial ID
- timestamp
- software commit SHA

---

## 22. Data Format

Recommended per-trial structure:

    {
      "trial_id": "000001",
      "active": true,
      "trigger_time_ns": 0.0,
      "detectors": {
        "D1": null,
        "D2": null,
        "D3": null,
        "D4": null,
        "D5": null,
        "D6": null
      },
      "rf": {},
      "acoustic": {},
      "vibration": {},
      "thermal": {},
      "cable_map": {},
      "channel_map": {},
      "random_seed": 0
    }

---

## 23. First Physical Milestone

The first milestone is:

> Demonstrate that the apparatus can correctly identify every known injected artifact under blinded and randomized conditions.

It is not:

> Search for GV.

---

## 24. Phase 1 Entry Gate

Do not begin unexplained-signal trials until:

- Phase 0 passes
- hardware configuration is documented
- timing uncertainty is measured
- analysis code is frozen
- calibration data are archived
- sham behavior is characterized

---

## 25. Bottom Line

Phase 0 asks:

> Can the apparatus tell us when we are fooling ourselves?

Only after that answer is convincingly yes should the apparatus be used to ask whether anything unexplained remains.
