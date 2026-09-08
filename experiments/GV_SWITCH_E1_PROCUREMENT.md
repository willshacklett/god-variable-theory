# GV Switch E1 Procurement Sheet

Prototype: **E1-A**

Phase: **0 — Known-channel validation**

Status: **Pre-purchase**

Purpose:

> Identify the minimum hardware needed to assemble and characterize the first E1 electrical transient sensor without prematurely buying expensive instrumentation.

---

## 1. Purchase Philosophy

Buy in layers.

Do not start with the expensive oscilloscope.

First purchase the inexpensive parts required to build:

- the passive E1 pickup
- the trigger/reference path
- the cable system
- the mechanical fixture
- the shielding controls

Then choose the high-speed acquisition hardware once the final channel and bandwidth requirements are fixed.

---

## 2. Buy Now — Low-Cost E1 Parts

### Pickup Material

Required:

- copper sheet or copper-clad PCB material

Target size:

- enough material to fabricate multiple 5 cm × 5 cm plates

Purpose:

- E1-A pickup plate
- spare prototype
- shielding experiments

Estimated planning cost:

\[
\$10-\$30
\]

---

## 3. Connectors

Preferred:

- panel-mount BNC female connectors

Quantity:

- 4 to 8

Purpose:

- E1 pickup
- fixture connections
- direct-injection path
- spare calibration ports

Estimated planning cost:

\[
\$15-\$40
\]

---

## 4. Coaxial Cable

Preferred:

- 50-ohm coax

Required:

- at least two separately identifiable sensor cables
- one trigger-reference cable
- one spare

Suggested initial lengths:

- 0.5 m
- 1.0 m
- 2.0 m
- spare/custom

All cables must receive unique IDs.

Estimated planning cost:

\[
\$30-\$100
\]

---

## 5. Terminators and Adapters

Required:

- 50-ohm BNC terminators
- BNC T adapters if needed
- BNC gender adapters only where necessary

Avoid excessive adapter chains.

Estimated planning cost:

\[
\$20-\$60
\]

---

## 6. Nonconductive Sensor Mount

Possible materials:

- acrylic
- PVC
- wood
- 3D-printed plastic

Required features:

- stable sensor position
- orientation indexing
- adjustable height
- reproducible distance placement

Estimated planning cost:

\[
\$10-\$50
\]

---

## 7. Orientation Fixture

Required positions:

- 0 degrees
- 90 degrees
- 180 degrees

Possible implementation:

- marked rotating plate
- indexed bracket
- simple detent fixture

Estimated planning cost:

\[
\$10-\$40
\]

---

## 8. Distance Measurement

Required:

- tape measure or steel rule
- fixed reference marks

Preferred:

- rigid measurement line or rail

Initial positions:

- 0.25 m
- 0.50 m
- 1.00 m
- 2.00 m

Estimated planning cost:

\[
\$10-\$50
\]

---

## 9. Shielding Materials

Useful initial materials:

- aluminum sheet
- copper foil
- conductive mesh
- metal enclosure
- ferrites

Purpose:

- unshielded control
- partial shielding
- strong shielding

Estimated planning cost:

\[
\$30-\$150
\]

---

## 10. Low-Voltage Trigger Source

Preferred initial options:

- function/pulse generator
- low-voltage MOSFET switching circuit
- microcontroller-controlled logic pulse

Initial development does not require high voltage.

Planning budget:

\[
\$50-\$500
\]

depending on whether a dedicated bench generator is purchased.

---

## 11. Bench Power Supply

Optional if the pulse source provides everything required.

If needed:

- regulated low-voltage DC bench supply

Planning budget:

\[
\$50-\$200
\]

---

## 12. Basic Hand Tools

Useful:

- soldering iron
- solder
- wire cutters
- small drill
- multimeter
- heat-shrink tubing
- cable labels
- ruler/caliper

Only purchase missing items.

---

## 13. Labeling

Required:

- cable labels
- sensor ID labels
- configuration labels

Examples:

- E1-A
- CABLE_A
- CABLE_B
- TRIGGER_REF_A

The experiment should never rely on memory for component identity.

---

## 14. Hold Off — Oscilloscope

Do not purchase the serious oscilloscope yet.

Final choice depends on:

- synchronized channel count
- bandwidth
- sample rate
- channel skew
- trigger jitter
- timebase accuracy
- API support
- cost

Current serious direction remains:

> synchronized multi-GSa/s acquisition

---

## 15. Hold Off — Six Sensor Copies

Do not build six identical E1 sensors yet.

Build and characterize:

- E1-A first

Only duplicate after verifying:

- bandwidth
- sensitivity
- timing jitter
- repeatability
- shielding response
- orientation response

---

## 16. Hold Off — Amplifiers

Do not buy RF amplifiers for E1-A.

The initial design is passive.

An amplified E1-B should be treated as a separate prototype because amplification changes:

- latency
- phase
- noise
- gain
- saturation behavior

---

## 17. Hold Off — Exotic Sensors

Do not purchase:

- unusual field sensors
- quantum sensors
- exotic detector materials
- speculative "scalar" detectors

There is no established GV coupling mechanism that justifies those purchases.

---

## 18. Initial Shopping List

Minimum useful E1-A build:

- copper or copper-clad material
- 4–8 BNC connectors
- several 50-ohm coax cables
- 50-ohm terminators
- small BNC adapter set
- nonconductive sensor mount
- orientation fixture materials
- shielding material
- cable labels
- low-voltage pulse source or parts to build one

---

## 19. Initial Budget Target

For the physical E1 sensor and controls, excluding the serious oscilloscope:

\[
\$200-\$800
\]

depending mainly on the pulse source and tools already available.

---

## 20. First Build Package

The first physical package should contain:

### E1 Sensor

- 5 cm × 5 cm copper plate
- BNC connection
- rigid nonconductive mount

### Trigger

- low-voltage repeatable pulse
- direct trigger-reference output

### Cabling

- CABLE_A
- CABLE_B
- TRIGGER_REF_A

### Controls

- partial shielding material
- strong shielding enclosure
- orientation marks
- distance marks

---

## 21. First Bench Before Serious Scope

If an existing oscilloscope is available, even if it is slower than the final required system, it may be used for:

- confirming sensor response
- debugging trigger wiring
- checking polarity
- finding gross saturation
- testing shielding dependence
- testing orientation dependence

It must not be used to make unsupported sub-nanosecond timing claims.

---

## 22. Procurement Rule

Every purchased component used in confirmatory testing should eventually receive:

- manufacturer
- model
- serial number if applicable
- purchase source
- component ID
- calibration status where relevant

---

## 23. Bottom Line

The next physical goal does not require a \$10,000 instrument.

It requires:

> Build E1-A cheaply, make it respond to a known electrical transient, and learn the geometry before committing to the expensive timing hardware.
