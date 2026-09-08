# GV Switch E1 Confirmatory Preregistration

Prototype: **E1**

Phase: **0 — Known-channel validation**

Status: **Locked before hardware data collection**

## Purpose

This document freezes the confirmatory E1 calibration design before real measurements are examined.

E1 is an electrical transient sensor.

It is not a GV detector.

## Confirmatory Trial Design

The confirmatory design uses two complete balanced blocks.

Each block contains 144 physical/acquisition configurations.

Each configuration receives:

- one active trial
- one sham trial

Therefore:

\[
144 \times 2 = 288
\]

trials per block.

Two blocks produce:

\[
N = 576
\]

with:

- 288 active trials
- 288 sham trials

## Frozen Variables

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

Cable IDs:

- CABLE_A
- CABLE_B

Scope channels:

- CH1
- CH2

## Timing Requirement

Target timing jitter:

\[
\sigma_t \le 1.0\ \mathrm{ns}
\]

Preferred:

\[
\sigma_t \le 0.5\ \mathrm{ns}
\]

## Sham Requirement

Maximum engineering screening false-positive rate:

\[
FPR_{sham} \le 1\%
\]

This is an apparatus-development criterion, not a discovery threshold.

## Threshold Rule

The detection threshold must be determined from calibration data before confirmatory trials.

Thresholds must not be tuned independently after examining each result.

Post-hoc threshold changes require a new preregistration version.

## Required Controls

The confirmatory calibration must include:

- direct electrical injection
- cable swap
- oscilloscope channel swap
- shielding change
- orientation change
- active/sham trials
- source-disconnected trials

## Allowed Exclusions

A trial may be excluded only for a documented technical reason such as:

- missing trigger reference
- missing required metadata
- scope saturation
- acquisition failure
- manifest mismatch
- corrupted waveform

## Forbidden Exclusions

A trial may not be excluded merely because:

- the result is unexpected
- the waveform is unusual
- the result disagrees with the hypothesis
- the result appears noisy without satisfying a preregistered failure condition

## Required Data Retention

Retain:

- raw waveforms
- manifest
- manifest SHA-256
- analysis output
- software commit SHA
- apparatus configuration ID

Derived timing values alone are insufficient.

## Allowed Final E1 Verdicts

Only:

- E1 CALIBRATION PASS
- E1 CALIBRATION FAIL
- E1 CALIBRATION INCOMPLETE

## Scientific Boundary

Passing E1 means:

> The electrical transient sensor satisfied the defined engineering calibration requirements.

It does not mean:

> GV was detected.

Phase 0 exists to characterize known physics and known instrumental behavior before any anomalous-signal search.
