# GV Switch E1 Bench Assembly and Wiring Specification

Protocol family: **GV-SWITCH**

Phase: **0 — Known-channel validation**

Prototype: **E1 — Fast Electrical Transient Sensor**

Status: **Pre-assembly engineering specification**

Purpose:

> Define the physical construction, wiring, channel assignments, calibration paths, and first bench procedure for the E1 electrical transient sensor.

E1 is not a GV detector.

Its job is to make ordinary electrical and electromagnetic coupling measurable before any unexplained-signal experiment is attempted.

---

## 1. Safety Boundary

Initial E1 development must use only:

- low-voltage sources
- low-energy pulses
- isolated bench supplies where practical
- ordinary laboratory signal levels

No high-voltage discharge is required.

No mains switching is required.

No exposed hazardous-energy circuit is required.

The goal is timing quality, not source intensity.

---

## 2. E1 System Overview

The basic bench architecture is:

\[
\text{Pulse Source}
\rightarrow
\text{Trigger Reference}
\]

and independently:

\[
\text{Pulse Source}
\rightarrow
\text{Known EM Transient}
\rightarrow
\text{E1 Pickup}
\rightarrow
\text{Coax}
\rightarrow
\text{Oscilloscope}
\]

The trigger reference establishes:

\[
t_0
\]

The E1 channel establishes:

\[
t_{E1}
\]

The basic measured delay is:

\[
\Delta t = t_{E1} - t_0
\]

---

## 3. First Bench Goal

The first physical milestone is not propagation measurement.

It is:

> Generate a repeatable low-voltage transient and observe a repeatable E1 response on a second oscilloscope channel.

Success requires:

- clean trigger edge
- visible E1 waveform
- repeatable polarity
- repeatable timing
- no clipping
- identifiable baseline noise

---

## 4. Initial Channel Assignment

For a two-channel prototype bench:

### Oscilloscope CH1

Purpose:

`TRIGGER_REFERENCE`

Input:

Direct electrical reference from the pulse/trigger source.

### Oscilloscope CH2

Purpose:

`E1_SENSOR`

Input:

Output of the passive E1 pickup sensor.

---

## 5. Expanded Channel Assignment

If four or more channels are available:

### CH1

`TRIGGER_REFERENCE`

### CH2

`E1_SENSOR`

### CH3

`DIRECT_INJECTION_REFERENCE`

### CH4

`SECONDARY_EM_MONITOR`

Future channels may include:

- magnetic pickup
- photodiode
- additional E1 sensor

---

## 6. E1 Pickup Construction

Prototype designation:

`E1-A`

Initial pickup geometry:

- flat conductive plate
- copper preferred
- approximate active area between 25 and 100 square centimeters
- rigid nonconductive support
- direct connection to coax center conductor
- coax shield connected to defined reference/shield structure

The exact dimensions must be recorded before calibration.

---

## 7. Recommended Starting Geometry

Initial engineering target:

- square copper plate
- approximately 5 cm × 5 cm
- rigid plastic or wood support
- short connection from plate to BNC or SMA connector
- no active amplifier

Approximate active area:

\[
25\ \mathrm{cm^2}
\]

This dimension is not physically privileged.

It is simply a reproducible starting geometry.

---

## 8. Passive-First Rule

E1-A should initially contain no amplifier.

Reason:

An active amplifier introduces additional:

- propagation delay
- phase response
- saturation behavior
- power-supply coupling
- noise
- timing jitter

If passive sensitivity later proves inadequate, an active E1-B version may be developed separately.

Do not modify E1-A after confirmatory calibration begins.

---

## 9. Connector Standard

Preferred detector connector:

- BNC for robust bench work

Alternative:

- SMA for compact high-frequency construction

The same connector family should be used consistently within each calibrated configuration.

Adapter chains should be minimized.

Every adapter used must be documented.

---

## 10. Cable Standard

Initial signal cable:

- 50-ohm coaxial cable

Requirements:

- unique cable ID
- measured length
- measured propagation delay
- documented connector type

Example IDs:

- CABLE_A
- CABLE_B
- TRIGGER_REF_A

Do not identify cables only as "short" or "long."

---

## 11. Oscilloscope Termination

Where supported and appropriate, the high-speed signal path should use:

\[
50\ \Omega
\]

termination.

The selected termination must be documented for every channel.

Do not mix:

- 1 megaohm input
- 50-ohm input

without recording the configuration.

Termination changes can alter both waveform amplitude and timing.

---

## 12. Trigger Source

Preferred initial source:

> Low-voltage pulse generator or logic-controlled transistor switching a small known load.

Required outputs:

1. physical source event
2. electrical trigger/reference edge

The reference edge must be directly observable on CH1.

---

## 13. Source Geometry

The physical source should be mounted on a stable fixture.

Record:

- source position
- source orientation
- switched conductor geometry
- source voltage
- source current if measured
- pulse duration
- repetition rate

The geometry should remain fixed during a calibration block.

---

## 14. Initial Source-to-Sensor Distance

Begin at:

\[
d = 0.25\ \mathrm{m}
\]

Do not begin at 8 meters.

The initial goal is to obtain a clean, characterized E1 response.

After successful characterization, proceed to:

- 0.50 m
- 1.00 m
- 2.00 m

---

## 15. Bench Layout

Conceptual top view:

    SOURCE / TRIGGER
          |
          |
          |  0.25 m initially
          |
        E1-A
          |
          |
       COAX
          |
          |
      SCOPE CH2

Trigger reference:

    SOURCE TRIGGER OUTPUT
          |
          |
       COAX
          |
          |
      SCOPE CH1

The source and detector geometry must be measured physically.

---

## 16. Direct-Injection Calibration Path

Before using the pickup plate, characterize the acquisition chain directly.

Direct-injection architecture:

    PULSE SOURCE
        |
        +----> CH1 trigger/reference
        |
        +----> calibrated cable ----> CH2

This bypasses the E1 pickup.

Purpose:

- characterize trigger jitter
- characterize cable delay
- characterize channel skew
- verify threshold timing
- measure acquisition repeatability

---

## 17. Direct-Injection Rule

Direct-injection calibration must occur before field-pickup interpretation.

If direct injection cannot achieve stable timing:

> E1 field measurements must not proceed to timing analysis.

---

## 18. Cable Delay Calibration

For each cable:

1. connect pulse source directly
2. record reference edge
3. record arrival edge
4. repeat at least 100 times
5. estimate mean delay
6. estimate delay jitter
7. store cable ID and statistics

Required fields:

- cable_id
- cable_length_m
- mean_delay_ns
- timing_sigma_ns
- connector_configuration

---

## 19. Channel-Skew Calibration

Procedure:

1. send same pulse to CH1 and CH2 through matched or characterized paths
2. collect repeated measurements
3. measure mean channel offset
4. swap physical paths
5. repeat
6. estimate corrected CH1-to-CH2 skew

The measured skew must be stored as calibration metadata.

---

## 20. E1 Signal Connection

E1-A output path:

    PICKUP PLATE
        |
        |
      CONNECTOR
        |
        |
     50-OHM COAX
        |
        |
     SCOPE CH2

Avoid loose jumper wires in the high-speed signal path.

Avoid breadboard signal routing for final timing characterization.

---

## 21. Grounding

The grounding configuration must be deliberate and documented.

Record:

- oscilloscope ground state
- source ground state
- shield connection
- bench earth connection
- any isolation used

Ground loops can produce false transient signals.

A wiring diagram must be updated whenever grounding changes.

---

## 22. Initial Orientation Definition

Define:

`0 degrees`

as the reference orientation where the pickup plate face is directed toward the source.

Define:

`90 degrees`

as plate face rotated perpendicular to the reference orientation.

Define:

`180 degrees`

as reversed reference orientation.

Mark the fixture physically so orientations can be reproduced.

---

## 23. Orientation Fixture

The sensor mount should include physical indexing marks for:

- 0 degrees
- 90 degrees
- 180 degrees

Do not estimate orientation by eye during confirmatory trials.

---

## 24. Distance Fixture

Measure distance from a defined source reference point to a defined E1 reference point.

Example:

Source reference:

> center of switched source element

Sensor reference:

> center of E1 pickup plate

Use the same definition for every trial.

---

## 25. Shielding Fixture

The E1 setup should support three reproducible states:

### UN-SHIELDED

No intentional conductive barrier.

### PARTIAL

Defined conductive barrier between source and sensor.

### STRONG

Sensor placed within or behind a substantially enclosed conductive shield.

The actual attenuation must be measured.

The labels alone do not prove shielding effectiveness.

---

## 26. Shielding Metadata

Record:

- material
- thickness if known
- enclosure dimensions
- openings
- cable entry geometry
- grounding condition

A conductive box with a large uncontrolled cable opening is not automatically a good Faraday enclosure.

---

## 27. Scope Acquisition Settings

Record for every run:

- sample rate
- analog bandwidth
- record length
- vertical scale
- horizontal scale
- trigger level
- trigger mode
- input impedance
- acquisition mode

These settings form part of:

`apparatus_config_id`

---

## 28. Initial Scope Strategy

Begin with a waveform window wide enough to see:

- pre-trigger baseline
- trigger edge
- E1 response
- post-event ringing

Do not zoom immediately to a few nanoseconds and discard the surrounding waveform.

Full context helps expose artifacts.

---

## 29. Raw Waveform Requirement

For each real trial, preserve the raw waveform if the instrument permits.

Do not retain only:

- threshold time
- peak amplitude
- fitted delay

Derived values can be recalculated.

Discarded raw waveforms cannot.

---

## 30. First Power-On Procedure

Step 1:

Inspect all wiring with source power off.

Step 2:

Verify scope input termination.

Step 3:

Connect trigger reference to CH1.

Step 4:

Leave E1 disconnected.

Step 5:

Generate low-amplitude pulse.

Step 6:

Confirm clean CH1 waveform.

Step 7:

Stop source.

Step 8:

Connect E1 to CH2.

Step 9:

Place E1 at 0.25 m.

Step 10:

Resume low-amplitude pulses.

Step 11:

Observe CH2 for trigger-correlated response.

---

## 31. Initial E1 Observation

If CH2 responds, record:

- polarity
- peak voltage
- approximate delay
- waveform shape
- ringing
- baseline noise

Do not immediately interpret delay as propagation time.

The observed delay includes:

\[
\text{source latency}
+
\text{sensor response}
+
\text{cable delay}
+
\text{channel skew}
+
\text{threshold method}
\]

---

## 32. Initial Noise Run

With the source idle, collect:

\[
N \ge 100
\]

acquisitions.

Measure:

- RMS baseline
- maximum spontaneous excursion
- false threshold crossings

This establishes the electrical noise floor.

---

## 33. Sham Run

Run the acquisition logic without a physical source event.

Collect at least:

\[
N \ge 100
\]

early sham trials.

The confirmatory blocked design comes later.

---

## 34. Active Calibration Run

At fixed geometry:

- 0.25 m
- 0 degrees
- unshielded
- CABLE_A
- CH2

collect:

\[
N \ge 100
\]

active pulses.

Compute:

- mean arrival delay
- timing sigma
- mean peak voltage
- peak-voltage sigma
- detection rate

---

## 35. Immediate Acceptance Question

Before changing geometry ask:

> Is the E1 response repeatable enough to characterize?

If no:

- troubleshoot source
- troubleshoot cable
- troubleshoot grounding
- troubleshoot scope settings
- troubleshoot pickup geometry

Do not proceed by increasing complexity.

---

## 36. First Shielding Test

Once baseline repeatability is established:

1. collect unshielded condition
2. install partial shielding
3. repeat
4. install strong shielding
5. repeat

Compare:

- peak amplitude
- integrated waveform energy
- waveform correlation
- timing

A meaningful shielding dependence supports an ordinary EM interpretation.

---

## 37. First Orientation Test

At fixed distance and source strength:

1. 0 degrees
2. 90 degrees
3. 180 degrees

Repeat measurements.

Orientation-dependent amplitude is expected for many ordinary coupling geometries.

---

## 38. Cable Swap Test

At fixed physical geometry:

1. run CABLE_A
2. run CABLE_B
3. apply measured cable corrections
4. compare corrected timing

Corrected sensor timing should not follow cable identity.

---

## 39. Scope Channel Swap

At fixed geometry:

1. E1 on CH2
2. move E1 to another characterized channel
3. preserve cable if possible
4. apply channel-skew correction
5. compare result

Corrected timing should not follow channel identity.

---

## 40. Apparatus Configuration ID

Initial suggested ID:

`E1-PROTOTYPE-001`

Any material change requires a new configuration ID.

Examples:

- different pickup dimensions
- different termination
- different connector topology
- added amplifier
- changed source circuit
- changed grounding architecture

---

## 41. E1-A Freeze Point

Once E1-A passes preliminary characterization, freeze:

- pickup geometry
- connector
- cable class
- termination
- fixture
- grounding plan

Do not modify these inside a confirmatory run.

---

## 42. Expected Phase 0 Result

E1 is expected to detect ordinary trigger-generated electrical or electromagnetic transients.

That is a successful result.

A strong E1 response is not anomalous.

The better E1 becomes at exposing conventional coupling, the more useful it becomes as a control instrument.

---

## 43. Failure Is Useful

If E1 reveals that apparent fast signals are ordinary EM pickup:

> The experiment has worked.

Phase 0 is designed to discover ways the apparatus can fool us.

---

## 44. No Unknown Search Yet

Do not conduct an unexplained-propagation search using E1-A until:

- direct injection is characterized
- timing jitter is measured
- cable delays are measured
- channel skew is measured
- shielding behavior is measured
- orientation behavior is measured
- sham behavior is measured
- saturation is excluded

---

## 45. Bottom Line

The first real E1 experiment is deliberately mundane:

> Make a small known electrical transient, measure it reliably, and learn exactly how every part of the apparatus changes what we see.

Only after the instrument can explain ordinary signals should it be trusted with extraordinary ones.
