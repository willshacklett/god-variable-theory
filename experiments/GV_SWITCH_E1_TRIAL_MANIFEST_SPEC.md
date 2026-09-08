# GV Switch E1 Trial Manifest Specification

Prototype: **E1**

Phase: **0 — Known-channel validation**

Purpose:

Freeze the randomized trial plan before physical measurements are collected.

The manifest determines:

- active versus sham state
- physical sensor distance
- sensor orientation
- shielding condition
- cable identity
- oscilloscope channel
- apparatus configuration
- randomization seed

The manifest must be generated before data collection.

---

## Active / Sham Balance

Recommended initial confirmatory block:

\[
250\ \text{active}
\]

and:

\[
250\ \text{sham}
\]

for:

\[
N=500
\]

total trials.

---

## Randomization

Trial order is randomized from a fixed integer seed.

The seed is stored in:

- every trial row
- manifest metadata

This allows exact regeneration of the design.

---

## Manifest Integrity

After generation, the manifest SHA-256 hash is calculated.

Once real data collection begins, the manifest must not be modified.

If the manifest changes, the hash changes.

Any changed manifest requires a new apparatus run identifier.

---

## Experimental Variables

Initial randomized values:

Distances:

- 0.25 m
- 0.50 m
- 1.00 m
- 2.00 m

Orientations:

- 0 degrees
- 90 degrees
- 180 degrees

Shielding:

- unshielded
- partial
- strong

Cable identity:

- CABLE_A
- CABLE_B

Scope channel:

- CH1
- CH2

---

## Important Limitation

Pure random assignment does not guarantee perfect balance across every combination.

Before confirmatory hardware trials, the design should be upgraded to blocked or stratified randomization if balanced representation across configurations is required.

---

## Scientific Rule

Trial configuration must be determined before observing the corresponding measurement.

The operator must not change:

- distance
- cable
- orientation
- shielding
- channel
- active/sham assignment

because of previously observed results.

---

## Interpretation

The manifest is experimental infrastructure only.

It contains no detection result.

It cannot provide evidence for or against GV.
