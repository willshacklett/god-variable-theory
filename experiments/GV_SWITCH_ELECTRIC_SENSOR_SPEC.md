# GV Switch Prototype #1 — Fast Electrical Transient Sensor

Protocol family: **GV-SWITCH**

Phase: **0 — Known-channel validation**

Prototype ID: **E1**

Status: **Pre-build engineering specification**

Purpose:

> Build a fast, repeatable electrical transient sensor that can characterize ordinary electromagnetic pickup from the trigger apparatus and support timing-system calibration.

This sensor is not a GV detector.

---

## 1. Physical Quantity

The sensor measures:

- transient voltage
- capacitive pickup
- local electric-field coupling

The output is an electrical waveform suitable for oscilloscope acquisition.

---

## 2. Why This Sensor Comes First

A switching event naturally produces electrical and electromagnetic transients.

Therefore the first prototype should characterize the most obvious conventional coupling mechanism before any anomalous interpretation is considered.

Advantages:

- simple to build
- inexpensive
- fast response
- easy to shield
- easy to rotate
- easy to calibrate
- directly compatible with high-speed oscilloscopes

---

## 3. Functional Architecture

Conceptual signal chain:

\[
\text{field/transient}
\rightarrow
\text{pickup element}
\rightarrow
\text{termination}
\rightarrow
\text{coax}
\rightarrow
\text{oscilloscope}
\]

The initial prototype should avoid unnecessary active amplification.

Passive architecture is preferred first because it reduces:

- amplifier latency
- amplifier saturation
- power-supply coupling
- additional timing uncertainty

---

## 4. Pickup Element

Initial concept:

> Small conductive pickup plate or short monopole probe connected through controlled impedance to the acquisition system.

Candidate geometries:

- flat copper plate
- small metal disk
- short monopole
- PCB copper pad

Geometry must be documented.

Required metadata:

- dimensions
- material
- orientation
- height above reference surface
- distance from trigger
- cable connection point

---

## 5. Initial Preferred Geometry

Prototype E1-A:

- flat copper pickup plate
- approximate area: 25 to 100 square centimeters
- rigid nonconductive mount
- BNC or SMA output
- short 50-ohm coax cable
- oscilloscope input terminated at 50 ohms where appropriate

Final dimensions should remain fixed once calibration begins.

---

## 6. Bandwidth Goal

Initial desired system bandwidth:

\[
\ge 500\ \mathrm{MHz}
\]

Preferred:

\[
\ge 1\ \mathrm{GHz}
\]

This is a system requirement, not merely a sensor-element requirement.

The effective bandwidth includes:

- pickup element
- connector
- cable
- termination
- oscilloscope
- probe interface

---

## 7. Rise-Time Relationship

Approximate relationship:

\[
t_r \approx \frac{0.35}{BW}
\]

For:

\[
BW=500\ \mathrm{MHz}
\]

approximate rise time:

\[
t_r \approx 0.7\ \mathrm{ns}
\]

For:

\[
BW=1\ \mathrm{GHz}
\]

approximate rise time:

\[
t_r \approx 0.35\ \mathrm{ns}
\]

These values are idealized and must not be treated as measured performance.

---

## 8. Timing Requirement

Prototype goal:

- repeatable trigger-relative timing
- measured timing jitter
- stable channel latency

Target:

\[
\sigma_t \le 1\ \mathrm{ns}
\]

Preferred:

\[
\sigma_t \le 0.5\ \mathrm{ns}
\]

The sensor cannot be considered suitable for c-like timing work until actual jitter is measured.

---

## 9. Calibration Stimulus

Primary calibration stimulus:

> Known fast electrical pulse applied to a nearby calibration conductor or plate.

Calibration should verify:

- waveform polarity
- amplitude response
- threshold stability
- timing repeatability
- distance response
- orientation response

---

## 10. Direct Injection Calibration

The acquisition chain must also support direct electrical injection.

Purpose:

- measure cable delay
- measure oscilloscope channel skew
- measure trigger-to-channel latency
- separate sensor behavior from acquisition behavior

Direct injection should bypass the pickup geometry.

---

## 11. Trigger Reference

Every calibration trial must include an independent trigger-reference channel.

Record:

- trigger edge time
- sensor waveform
- sensor threshold-crossing time
- sensor peak amplitude
- cable ID
- sensor orientation
- source configuration

---

## 12. Shielding Test

Minimum conditions:

1. unshielded
2. partial conductive shielding
3. strong conductive shielding

Expected conventional behavior:

> Electrical pickup should decrease or otherwise change systematically with effective shielding.

If shielding has no measurable effect, the setup must be investigated before proceeding.

---

## 13. Orientation Test

Test at minimum:

- 0 degrees
- 90 degrees
- 180 degrees

Record:

- peak amplitude
- integrated waveform energy
- first threshold time
- waveform correlation

Orientation dependence supports an ordinary field-coupling explanation.

---

## 14. Distance Sweep

Initial distances:

- 0.25 m
- 0.50 m
- 1.00 m
- 2.00 m

Do not begin with the full 8-meter layout.

First prove that the prototype behaves predictably over a smaller bench geometry.

---

## 15. Cable Swap Test

Use at least two cables with separately measured delay.

Procedure:

1. place sensor at fixed position
2. measure with cable A
3. measure with cable B
4. correct using measured cable delay
5. verify recovered sensor timing remains stable

If apparent propagation follows cable identity, the system fails calibration.

---

## 16. Channel Swap Test

Acquire the same sensor through multiple oscilloscope channels.

Purpose:

- measure channel-to-channel skew
- identify channel-specific latency
- verify timing correction

Required result:

> Corrected timing should not depend materially on oscilloscope channel identity.

---

## 17. Repeated-Trial Requirement

Minimum early characterization:

\[
N=100
\]

trials per configuration.

Preferred before Phase 0 acceptance:

\[
N\ge500
\]

per major condition.

Report:

- mean arrival time
- standard deviation
- median
- interquartile range
- amplitude distribution
- missed-detection rate

---

## 18. Threshold Definition

Do not tune threshold independently after viewing each condition.

Threshold method must be frozen.

Candidate methods:

- fixed voltage threshold
- fixed fraction of calibration amplitude
- matched-filter timing
- waveform cross-correlation

Initial simple method:

> Fixed threshold determined from calibration data and then held constant during blinded trials.

---

## 19. Saturation Test

The sensor must be tested at multiple source strengths.

Reject the configuration if:

- oscilloscope clips
- waveform shape changes due to overload
- arrival time shifts with saturation
- recovery behavior contaminates later trials

---

## 20. Noise Characterization

Measure with:

- trigger system completely idle
- logical sham trigger
- active trigger
- source disconnected
- source powered but not switched

Record baseline:

- RMS noise
- peak noise
- false threshold crossings
- spectrum where practical

---

## 21. Sham Requirement

During sham trials:

- software trigger flow remains intact
- trial IDs continue normally
- sensor acquisition still occurs
- physical source event is omitted

The sensor must not show reproducible trigger-locked responses during sham trials beyond the preregistered false-positive limit.

---

## 22. Positive Control

Positive control:

> Deliberate nearby electrical transient.

Expected classification:

`KNOWN EM CHANNEL`

If the apparatus cannot reliably detect its own positive control, the sensor is not ready.

---

## 23. Negative Control

Negative controls include:

- source disconnected
- source disabled
- shielded source
- blocked coupling geometry
- sham trigger

Expected:

> No stable propagation candidate.

---

## 24. Prototype Acceptance Metrics

E1 passes initial characterization only if:

1. waveform is repeatable
2. timing jitter is measured
3. cable delay is separable
4. channel skew is separable
5. shielding changes response
6. orientation changes response where expected
7. sham false-positive rate remains acceptable
8. no saturation occurs in selected operating range

---

## 25. Initial Acceptance Target

For prototype characterization:

\[
\sigma_t \le 1\ \mathrm{ns}
\]

and:

\[
\mathrm{FPR}_{sham}\le1\%
\]

These are engineering screening criteria.

They are not discovery thresholds.

---

## 26. Data Fields

Every E1 trial should record:

- trial_id
- active_or_sham
- trigger_time_ns
- sensor_time_ns
- sensor_peak_v
- sensor_rms_v
- threshold_v
- source_state
- source_level
- sensor_distance_m
- sensor_orientation_deg
- shielding_state
- cable_id
- scope_channel
- apparatus_config_id
- git_commit_sha

---

## 27. File Output

Recommended raw format:

- CSV for timing summary
- binary or native waveform file for raw capture
- JSON metadata per run

Never retain only derived timing values.

Raw waveforms should be archived.

---

## 28. Prototype Build Sequence

Stage E1.1:

- build passive pickup
- verify waveform visibility

Stage E1.2:

- direct-injection cable calibration

Stage E1.3:

- repeated trigger measurement

Stage E1.4:

- shielding test

Stage E1.5:

- orientation test

Stage E1.6:

- cable swap

Stage E1.7:

- channel swap

Stage E1.8:

- sham randomized trials

Only then consider duplicating the sensor.

---

## 29. Safety

Use only low-voltage, low-energy trigger systems during initial development.

No high-voltage discharge is required for Phase 0.

The experiment should prefer measurement quality over source intensity.

---

## 30. Scientific Interpretation

If E1 responds:

> An electrical/electromagnetic coupling path has been detected.

If E1 does not respond:

> No electrical transient was detected within the bandwidth and sensitivity of E1.

Neither result says anything directly about whether GV exists.

---

## 31. Bottom Line

Prototype E1 exists to make ordinary electrical coupling visible, measurable, and falsifiable.

Before searching for anything unexplained, the apparatus must become very good at detecting the things most likely to fool it.
