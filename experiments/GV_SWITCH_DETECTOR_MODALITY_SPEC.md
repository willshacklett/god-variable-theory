# GV Switch Detector Modality Specification

Protocol family: **GV-SWITCH**

Phase: **0 — Known-channel validation**

Status: **Pre-hardware detector architecture**

Purpose:

> Define what physical quantities the apparatus actually measures before selecting final acquisition hardware or performing any unexplained-signal search.

---

## 1. Fundamental Constraint

There is currently no experimentally established GV coupling mechanism.

Therefore there is no scientifically justified device that can simply be labeled:

`GV detector`

The apparatus must instead measure ordinary physical observables with known sensors.

The purpose of Phase 0 is to characterize those observables well enough that conventional explanations can be identified and rejected correctly.

---

## 2. Detector Philosophy

A useful sensor architecture should be:

- multimodal
- physically interpretable
- independently calibrated
- synchronized where timing matters
- spatially repeatable
- swappable between positions
- capable of distinguishing known channels

The experiment should measure multiple physical domains rather than rely on one ambiguous electrical signal.

---

## 3. Primary Sensor Families

### A. Fast Electric / Electrical Transient Sensor

Physical quantity:

- voltage transient
- electric-field pickup
- capacitive coupling

Role:

- detect trigger-correlated electrical effects
- characterize electromagnetic contamination
- provide nanosecond-scale timing where hardware permits

Desired characteristics:

- high bandwidth
- low jitter
- repeatable threshold
- shieldable
- known input impedance
- calibrated cable path

Priority:

**HIGH**

---

### B. Fast Magnetic Sensor

Physical quantity:

- changing magnetic field
- inductive pickup

Possible implementation:

- small loop antenna
- broadband magnetic near-field probe

Role:

- distinguish magnetic coupling from other responses
- detect current-related trigger transients
- support EM exclusion

Desired characteristics:

- known loop geometry
- wide bandwidth
- repeatable orientation
- rotatable mounting

Priority:

**HIGH**

---

### C. Optical Sensor

Physical quantity:

- photons / optical intensity

Possible implementation:

- fast photodiode

Role:

- validate known c-speed optical timing
- benchmark timing hardware against a known propagation mechanism
- provide an independent reference for c-like timing

Desired characteristics:

- fast rise time
- low jitter
- shieldable from ambient light
- known wavelength response

Priority:

**HIGH FOR CALIBRATION**

---

### D. Acoustic Sensor

Physical quantity:

- pressure variation

Possible implementation:

- microphone
- pressure transducer

Role:

- identify acoustic coupling
- measure sound arrival time
- verify environmental classifier

Priority:

**REQUIRED CONTROL**

---

### E. Mechanical Sensor

Physical quantity:

- acceleration / vibration

Possible implementation:

- accelerometer
- piezoelectric vibration sensor

Role:

- identify mechanical coupling
- monitor trigger vibration
- verify isolation effectiveness

Priority:

**REQUIRED CONTROL**

---

### F. Thermal Sensor

Physical quantity:

- temperature

Possible implementation:

- thermistor
- RTD
- digital temperature probe

Role:

- identify drift
- characterize detector baseline changes
- rule out slow thermal artifacts

Priority:

**REQUIRED CONTROL**

---

## 4. Proposed Sensor Node

Each physical detector position should ultimately be treated as a sensor node.

Conceptually:

\[
\text{Node}_i =
\{
E_i,
B_i,
O_i,
A_i,
V_i,
T_i
\}
\]

where:

- \(E_i\) = electric/electrical transient measurement
- \(B_i\) = magnetic measurement
- \(O_i\) = optical measurement
- \(A_i\) = acoustic measurement
- \(V_i\) = vibration measurement
- \(T_i\) = temperature measurement

Not every modality requires nanosecond sampling.

Only the high-speed channels should consume the expensive high-bandwidth acquisition resources.

---

## 5. High-Speed Channels

Recommended high-speed modalities:

1. electric/electrical transient
2. magnetic pickup
3. optical photodiode
4. trigger reference

These channels are candidates for oscilloscope-class acquisition.

Acoustic, mechanical, and thermal sensors can use slower auxiliary acquisition.

---

## 6. Why Optical Calibration Matters

A fast optical pulse provides a known propagation mechanism at approximately:

\[
c
\]

This makes it useful for validating:

- timing resolution
- detector placement
- channel skew
- cable-delay correction
- fitting routines

Before the apparatus is allowed to interpret any unknown c-like timing pattern, it should successfully recover a deliberately injected optical c-speed signal.

---

## 7. Why EM Sensors Matter

A switching event naturally generates electromagnetic disturbances.

Therefore any claimed fast response is presumed electromagnetic until demonstrated otherwise.

Electric and magnetic sensors should be intentionally positioned to measure:

- direct pickup
- radiated transients
- conducted transients
- orientation dependence
- shielding dependence

---

## 8. Sensor Placement

Initial physical positions remain:

| Node | Distance |
|---|---:|
| N1 | 0.25 m |
| N2 | 0.50 m |
| N3 | 1.00 m |
| N4 | 2.00 m |
| N5 | 4.00 m |
| N6 | 8.00 m |

Sensor identity must not be permanently tied to node position.

---

## 9. Swap Requirement

At least the primary fast sensors must be physically reassigned between positions during Phase 0.

A real distance-dependent effect should follow:

\[
\text{position}
\]

A detector artifact should follow:

\[
\text{sensor identity}
\]

---

## 10. Orientation Requirement

Electric and magnetic sensors should support controlled orientation changes.

For example:

- 0 degrees
- 90 degrees
- 180 degrees

A response strongly dependent on antenna/probe orientation is evidence for electromagnetic coupling.

---

## 11. Shielding Requirement

Fast electrical and magnetic channels should be tested under multiple shielding states.

At minimum:

- unshielded
- partially shielded
- strongly shielded

Shielding effectiveness must be measured rather than assumed.

---

## 12. Optical Isolation

Photodiode channels must include:

- dark condition
- known optical pulse
- blocked optical path
- ambient-light control

This allows the optical channel to act as both a positive control and a null control.

---

## 13. Acquisition Architecture

Recommended architecture:

### High-speed DAQ

Acquires:

- trigger reference
- electric channel
- magnetic channel
- optical channel

### Auxiliary DAQ

Acquires:

- microphone
- accelerometer
- temperature

The systems must share a trial ID and synchronized event record.

Absolute synchronization between slow environmental channels and the nanosecond channels need only be sufficient to identify trial-correlated environmental events.

---

## 14. Six-Channel Scope Use

A six-channel high-speed oscilloscope should not automatically be interpreted as six identical GV detectors.

A stronger Phase 0 use is:

- CH1 trigger reference
- CH2 fast electric sensor
- CH3 magnetic loop
- CH4 photodiode
- CH5 duplicate electric sensor or reference
- CH6 duplicate magnetic/optical reference

Once timing behavior is characterized, repeated configurations can move identical sensors through the six physical distances.

---

## 15. Replicated Primary Sensors

For propagation testing, identical sensor copies are eventually required.

Example:

\[
E_1,E_2,E_3,E_4,E_5,E_6
\]

at six physical distances.

But before purchasing six copies, one or two prototype sensors should be characterized for:

- bandwidth
- jitter
- sensitivity
- saturation
- shielding response
- orientation response
- channel latency

---

## 16. Detector Development Sequence

### Stage 1

Build one prototype fast electric sensor.

### Stage 2

Build one magnetic pickup sensor.

### Stage 3

Add fast photodiode calibration.

### Stage 4

Characterize all three on the same timing instrument.

### Stage 5

Add acoustic, mechanical, and thermal controls.

### Stage 6

Duplicate the most useful high-speed sensor across spatial positions.

Do not buy six copies before Stage 4 succeeds.

---

## 17. Selection Criteria

Every candidate fast detector should be scored on:

1. bandwidth
2. rise time
3. timing jitter
4. sensitivity
5. repeatability
6. saturation behavior
7. shielding response
8. orientation response
9. cost
10. ease of replication

---

## 18. Detector Rejection Criteria

Reject a sensor design if:

- latency varies unpredictably
- rise time is too slow
- output saturates during ordinary trigger events
- shielding behavior cannot be characterized
- channel-to-channel repeatability is poor
- detector identity dominates apparent propagation timing

---

## 19. Phase 0 Positive Controls

Each modality must have an intentional positive-control stimulus.

Electric:

- injected electrical pulse

Magnetic:

- switched current loop

Optical:

- LED or laser pulse

Acoustic:

- speaker/click pulse

Mechanical:

- controlled tap or actuator

Thermal:

- controlled heating/cooling

The apparatus must demonstrate that it can detect what each sensor is designed to detect.

---

## 20. Phase 0 Negative Controls

Each modality also requires a condition where the relevant stimulus is absent or blocked.

Examples:

- electrical source disconnected
- magnetic source current removed
- optical path blocked
- acoustic source muted
- mechanical source isolated
- thermal source disabled

---

## 21. Candidate Interpretation

If an event appears only in the electric or magnetic channels:

> EM explanation remains primary.

If it appears only optically:

> optical explanation remains primary.

If it tracks microphone or accelerometer signals:

> environmental explanation remains primary.

If it appears consistently across multiple independent modalities:

> cross-coupling must first be investigated.

No sensor combination directly identifies GV.

---

## 22. Unknown-Coupling Problem

Because GV has no established coupling law, a true GV-related phenomenon could theoretically:

- couple electrically
- couple magnetically
- couple optically
- couple mechanically
- alter multiple channels
- couple to none of the selected sensors

Therefore a null result from this apparatus would constrain only the tested coupling channels.

It would not prove that GV does not exist.

---

## 23. Scientific Interpretation of a Null

Allowed conclusion:

> No unexplained response was detected within the sensitivity, bandwidth, geometry, and sensor modalities of the apparatus.

Not allowed:

> GV does not exist.

---

## 24. Scientific Interpretation of a Candidate

Allowed conclusion:

> A reproducible response survived the implemented channel controls and requires further investigation.

Not allowed:

> GV was detected.

---

## 25. Recommended First Detector Build

The first high-speed detector prototype should be:

> a simple, well-characterized broadband electric-field/electrical transient pickup.

Reason:

- easiest fast coupling mechanism to characterize
- highly relevant to switching artifacts
- inexpensive to prototype
- readily tested with shielding and orientation
- directly useful for learning the acquisition system

The second should be:

> a magnetic loop probe.

The third:

> a fast photodiode for known c-speed calibration.

---

## 26. Final Phase 0 Detector Architecture

Phase 0 should therefore consist of:

### Fast timing domain

- trigger reference
- electric transient sensor
- magnetic sensor
- optical calibration sensor

### Environmental domain

- microphone
- accelerometer
- temperature sensors

### Experimental controls

- shielding
- orientation changes
- sensor swaps
- cable swaps
- sham trials

---

## 27. Bottom Line

The detector question is not:

> What detects GV?

The scientifically valid question is:

> What ordinary physical quantities can we measure accurately enough that an unexplained residual, if one ever appears, cannot easily be mistaken for something familiar?
