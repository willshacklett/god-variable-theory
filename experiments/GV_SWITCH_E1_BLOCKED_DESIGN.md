# GV Switch E1 Blocked Experimental Design

Prototype: **E1**

Phase: **0 — Known-channel validation**

Purpose:

Replace purely random configuration assignment with a balanced design.

---

## Configuration Space

The current Phase 0 E1 design uses:

Distances:

- 0.25 m
- 0.50 m
- 1.00 m
- 2.00 m

Orientations:

- 0 degrees
- 90 degrees
- 180 degrees

Shielding states:

- unshielded
- partial
- strong

Cable identities:

- CABLE_A
- CABLE_B

Scope channels:

- CH1
- CH2

The total number of unique physical/acquisition configurations is:

\[
4
\times
3
\times
3
\times
2
\times
2
=
144
\]

---

## Paired Active / Sham Structure

Each configuration receives:

- one active trial
- one sham trial

Therefore one complete balanced block contains:

\[
144 \times 2 = 288
\]

trials.

---

## Repeat Blocks

A repeat count of 1 produces:

\[
N=288
\]

A repeat count of 2 produces:

\[
N=576
\]

A repeat count of 3 produces:

\[
N=864
\]

For initial serious Phase 0 calibration, two complete blocks are a reasonable starting target:

\[
N=576
\]

This produces:

- 288 active trials
- 288 sham trials

with equal representation across the defined configuration space.

---

## Why Blocking Matters

Pure randomization balances conditions only approximately.

A blocked design guarantees that each modeled configuration is deliberately represented.

This makes it easier to distinguish:

- distance effects
- orientation effects
- shielding effects
- cable effects
- scope-channel effects

without relying on chance balance.

---

## Randomization Still Matters

The configuration set is balanced first.

The resulting trials are then shuffled using a fixed randomization seed.

Therefore the design is both:

- balanced
- randomized

---

## Manifest Integrity

The generated CSV receives a SHA-256 digest.

Once physical data collection begins:

> The manifest must not be edited.

Any changed manifest requires a new run identifier and new hash.

---

## Phase 0 Role

This manifest is for known-channel sensor calibration.

It does not contain results.

It does not search for GV.

Its purpose is to prevent experimental design from changing in response to observed measurements.
