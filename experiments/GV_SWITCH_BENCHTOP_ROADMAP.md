# GV Switch Benchtop Experimental Roadmap

Protocol family: **GV-SWITCH**

Status: **Pre-hardware design document**

Important:

> This document does not assume that GV exists. It defines what a physical experiment would have to accomplish before an unexplained signal could be treated as scientifically interesting.

---

## 1. Objective

The first physical GV Switch experiment should answer one narrow question:

> Does a deliberately triggered local event produce any reproducible remote response that cannot be accounted for by known electromagnetic, timing, cable, acoustic, mechanical, thermal, or instrumental channels?

The experiment is not intended to demonstrate the origin of the universe, timelessness, or a new force.

It is intended only to search for an unexplained reproducible response.

---

## 2. Experimental Philosophy

The apparatus should be designed so that conventional explanations are easier to detect than a hypothetical GV interpretation.

The experiment must therefore include:

- active controls
- sham triggers
- blinded trials
- randomized configurations
- independent timing
- independent environmental monitoring
- preregistered analysis
- replication

The order is:

\[
\text{trigger}
\rightarrow
\text{detect}
\rightarrow
\text{exclude known channels}
\rightarrow
\text{replicate}
\]

not:

\[
\text{trigger}
\rightarrow
\text{assume GV}
\]

---

## 3. Phase 0 — Instrument Validation

Before searching for anything unexplained, prove that the apparatus can correctly detect known signals.

Required validation signals:

1. electromagnetic pulse
2. acoustic pulse
3. mechanical vibration
4. cable delay
5. clock offset
6. thermal drift

The system should correctly classify these known mechanisms before any GV-style trial is allowed.

Pass requirement:

> 100% of calibration mechanisms must be classified into the correct broad channel family in the reference validation set.

---

## 4. Trigger

The trigger should initially be an ordinary, reproducible switching event.

Examples:

- electrical switch closure
- relay activation
- optical interruption
- capacitor discharge into a contained load
- mechanical contact event

The trigger itself is not assumed to create GV.

Its purpose is to provide a precisely timestamped transition:

\[
t_0
\]

The trigger should generate an independent timing marker recorded by the acquisition system.

---

## 5. Detector Geometry

A benchtop experiment should begin much smaller than the synthetic 1000 m geometry.

Suggested initial physical spacing:

| Detector | Distance |
|---|---:|
| D1 | 0.25 m |
| D2 | 0.50 m |
| D3 | 1.00 m |
| D4 | 2.00 m |
| D5 | 4.00 m |
| D6 | 8.00 m |

The exact geometry must be measured physically and frozen before confirmatory trials.

Later phases may increase baseline distance if timing resolution requires it.

---

## 6. Timing Requirement

At the speed of light:

\[
t=\frac{d}{c}
\]

For 1 meter:

\[
t \approx 3.34\ \mathrm{ns}
\]

For 8 meters:

\[
t \approx 26.7\ \mathrm{ns}
\]

Therefore the apparatus must have timing resolution substantially below the propagation differences being tested.

An initial target should be:

\[
\sigma_t \le 1\ \mathrm{ns}
\]

with tighter timing preferred.

If the hardware cannot independently verify sub-nanosecond to low-nanosecond timing behavior, a c-speed propagation claim is not justified.

---

## 7. Independent Timing

The clock-crosscheck simulation demonstrated that timing artifacts can imitate propagation.

Therefore:

- detectors should not all depend blindly on one unverified timing path
- channel delays must be measured
- cable delays must be calibrated independently
- detector channels must be swapped across physical positions
- timing hardware must be reassigned across repeated runs

A physical propagation law should follow:

\[
\text{physical position}
\]

not:

\[
\text{channel identity}
\]

---

## 8. Cable Control

Cable length must not covary with detector distance.

Bad design:

\[
L_{\text{cable}}\propto d_{\text{detector}}
\]

because cable delay can imitate spatial propagation.

Better design:

- randomized cable lengths
- equalized cable lengths
- optical isolation where appropriate
- measured propagation delay for every cable
- cable assignments swapped among detectors

---

## 9. Electromagnetic Isolation

EM is the most dangerous confound for a c-like signal.

Required controls should include:

### Baseline
Normal apparatus configuration.

### Shielded
Detector or source placed inside appropriate EM shielding.

### Source-power variation
Change electrical power associated with the trigger.

### Modulation control
Change or disable EM-producing trigger components while preserving the logical trigger.

### Orientation test
Change antenna-like geometry or conductor orientation.

### RF monitoring
Record independent broadband RF activity during every trial.

A signal that tracks these manipulations should be classified as:

> `KNOWN EM CHANNEL`

---

## 10. Acoustic Isolation

Required measurements:

- microphone channel
- acoustic damping
- air-path alteration
- reduced-pressure testing if later apparatus permits

An acoustic signal should exhibit timing consistent with approximately:

\[
v_{\text{sound}}\approx343\ \mathrm{m/s}
\]

under ordinary room conditions.

---

## 11. Mechanical Isolation

Required controls:

- accelerometer
- vibration-isolated detector mount
- source isolation
- altered mechanical coupling
- rigid vs decoupled mounting conditions

A signal that follows the mechanical path is not anomalous.

---

## 12. Thermal Isolation

Required logging:

- source temperature
- detector temperature
- ambient temperature
- apparatus temperature

Thermal changes are generally much slower than c-like propagation but may produce detector drift and threshold artifacts.

Temperature must be included as a nuisance variable.

---

## 13. Environmental Monitoring

Every trial should record:

- RF activity
- acoustic level
- vibration
- temperature
- power-supply state
- trigger voltage/current where relevant
- detector supply voltage
- clock synchronization state

No unexplained candidate should be evaluated without its environmental record.

---

## 14. Sham Trials

A substantial fraction of trials must contain no physical activation while the acquisition system behaves identically.

Suggested starting design:

\[
50\% \text{ active}
\]

\[
50\% \text{ sham}
\]

Trial identity should be hidden from the first-pass analysis where possible.

The analysis should not know whether a trigger was real until after candidate extraction.

---

## 15. Randomization

Randomize:

- active vs sham
- detector-channel assignment
- cable assignment
- clock assignment
- control state
- trial order

Randomization seeds should be preserved in the audit record.

---

## 16. Blinding

At least one layer of analysis should be blinded.

Example:

1. acquisition computer records trial data
2. trial labels are replaced with anonymous IDs
3. analysis extracts candidate events
4. labels are revealed only after analysis output is frozen

---

## 17. Primary Endpoint

The primary endpoint should not be signal amplitude.

The first endpoint should be:

> reproducible trigger-locked remote timing structure that scales with physical detector distance and survives preregistered controls.

A simple propagation model is:

\[
t_i=t_0+\frac{d_i}{v}+\epsilon_i
\]

where:

- \(t_i\) = detector arrival time
- \(d_i\) = physical distance
- \(v\) = inferred propagation velocity
- \(\epsilon_i\) = measurement error

---

## 18. Null Hypothesis

Primary null:

\[
H_0:
\text{no independent propagation channel exists}
\]

All observed structure arises from conventional physical or instrumental mechanisms.

The burden is on the candidate signal to defeat the null.

---

## 19. Initial Statistical Target

Synthetic development target:

\[
\mathrm{FPR}\le1\%
\]

A real physical experiment should eventually demand stronger evidence than this.

The initial 1% target is for apparatus-development screening, not discovery.

A discovery-level claim would require substantially stronger statistics, independent replication, and expert review.

---

## 20. Trial Count

Phase 1 should prioritize calibration rather than massive sample size.

Suggested development progression:

### Calibration
100 known-channel trials per mechanism.

### Pilot
500 active/sham trials.

### Confirmatory
Trial count determined prospectively from measured noise and effect-size assumptions.

Do not choose the final sample size after observing whether the result looks favorable.

---

## 21. Required Failure Behavior

The experiment must be capable of saying:

- nothing detected
- detector unstable
- timing insufficient
- EM contamination
- cable artifact
- clock artifact
- acoustic explanation
- mechanical explanation
- thermal explanation
- ambiguous

These are valid scientific outcomes.

---

## 22. Candidate Behavior

Only after all gates pass may the system output:

> `UNEXPLAINED PROPAGATION CANDIDATE`

This phrase means:

> A reproducible signal survived the controls implemented in this experiment.

It does not mean GV.

---

## 23. Replication Ladder

Any unexplained candidate must proceed through:

### Level 1
Repeat on same apparatus.

### Level 2
Rebuild apparatus with replaced detectors, cables, clocks, and trigger hardware.

### Level 3
Independent operator repeats experiment.

### Level 4
Independent laboratory reproduces the effect.

Only after Level 4 should a new-physics interpretation receive serious consideration.

---

## 24. Connection to the Switch Hypothesis

The conceptual GV Switch model is:

\[
\text{latent state}
\rightarrow
\text{activation}
\rightarrow
\text{physical response}
\]

The benchtop experiment cannot test whether a timeless or pre-spacetime state exists.

It can test only whether an activation event produces an unexplained physical response.

That distinction must remain explicit.

---

## 25. First Hardware Milestone

The first hardware milestone is not:

> detect GV.

It is:

> Build a trigger-and-detector apparatus that can correctly identify ordinary EM, acoustic, mechanical, cable, clock, and thermal artifacts under blinded randomized trials.

Only after that milestone is achieved should anomalous-signal searches begin.

---

## 26. Recommended Development Sequence

1. Choose timing hardware.
2. Characterize channel latency.
3. Build trigger timestamping.
4. Build six-detector acquisition.
5. Measure cable delays.
6. Inject known EM pulse.
7. Inject known acoustic pulse.
8. Inject known mechanical pulse.
9. Introduce controlled clock offsets.
10. Introduce thermal drift.
11. Verify classifier behavior.
12. Add randomized sham trials.
13. Freeze analysis.
14. Run blinded pilot.
15. Evaluate null.
16. Replicate any unexplained result.

---

## 27. Success Criterion for Phase 0

Phase 0 succeeds only if:

\[
\text{known mechanisms}
\rightarrow
\text{correct classifications}
\]

with no unexplained candidate intentionally injected.

Only then advance to Phase 1.

---

## 28. Scientific Constraint

The apparatus must be designed such that a null result is useful.

If the experiment is constructed so that every outcome can be interpreted as GV, the experiment is invalid.

---

## 29. Bottom Line

The first real GV Switch experiment should not ask:

> "Can we prove GV?"

It should ask:

> "Can we build an apparatus capable of detecting and eliminating every ordinary explanation we know how to test?"

If the answer becomes yes, then—and only then—an unexplained residual becomes worth investigating.
