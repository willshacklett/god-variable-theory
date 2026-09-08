# GV Switch — Experimental Failure Notes

These notes preserve failed synthetic approaches that materially improved the GV Switch experimental design.

They are included to document why the current protocol uses multiple independent exclusion gates rather than a single all-purpose classifier.

None of these results are empirical evidence for GV.

---

## Failure 1 — Naive Propagation Classifier

### Approach

The first falsification framework asked whether a detected signal showed:

- reproducibility
- distance-dependent timing
- low residual error
- weak control-channel matching

Synthetic scenarios included:

- null/random false positives
- known EM-like propagation
- hypothetical propagation at c
- hypothetical propagation at 0.90c

### Initial Result

The simple Monte Carlo calibration appeared strong:

- null FPR: approximately 0%
- c-like synthetic detection power: approximately 99%
- 0.90c synthetic detection power: approximately 99%

### Problem

The null was too easy.

Random false positives did not adequately represent real instrumental artifacts.

### Lesson

A low false-positive rate against an unrealistic null is not meaningful.

---

## Failure 2 — Adversarial Null Suite

More difficult known-physics artifacts were introduced:

- correlated noise
- EM leakage
- cable-delay artifact
- common clock bias
- acoustic/mechanical artifact
- mixed contamination

### Result

The naive classifier failed badly.

Most important failures:

- cable-delay artifact classified as anomalous: 100%
- common clock bias classified as anomalous: 100%

Overall adversarial false-positive rate was approximately:

\[
33.47\%
\]

### Lesson

A clean distance-time relationship is not sufficient evidence for a new propagation channel.

Known instrumentation can produce:

\[
t \propto d
\]

without any new physics.

---

## Failure 3 — Free Linear Model Comparison

### Approach

Candidate timing was compared against:

- light-speed propagation
- acoustic propagation
- several cable propagation velocities
- unrestricted linear propagation

### Result

The unrestricted linear model frequently won because it had greater flexibility.

Approximate adversarial unexplained rate:

\[
50.98\%
\]

### Problem

RMS fit alone rewarded the more flexible model.

More fundamentally, a clock bias of the form

\[
t=t_0+\beta d
\]

can be mathematically indistinguishable from propagation

\[
t=t_0+\frac{d}{v}
\]

when distance and arrival time are the only observables.

### Lesson

Some competing mechanisms are not identifiable from timing data alone.

Physical interventions are required.

---

## Failure 4 — First Control Matrix

### Approach

The next design introduced:

- cable swapping
- clock swapping
- EM shielding
- physical-position testing

### Result

The approach successfully rejected:

- common-mode noise
- cable artifacts

and mostly rejected EM.

However, clock artifacts still survived at a high rate.

Known-mechanism false-positive rate was approximately:

\[
21.76\%
\]

### Lesson

Clock artifacts require direct clock-identity testing rather than indirect timing thresholds.

---

## Failure 5 — First Clock Crosscheck

### Approach

Measurements were centered by clock identity before estimating a physical-distance slope.

### Result

The method achieved:

\[
\mathrm{FPR}=0
\]

but also rejected the hypothetical spatial signal:

\[
\mathrm{TPR}=0
\]

### Problem

Arrival times were centered by clock without correctly preserving the associated detector-distance structure.

The classifier effectively learned to reject everything.

### Lesson

A classifier with zero false positives is useless if it also has zero detection power.

Both must always be reported.

---

## Correction — Independent Slope by Clock

The successful clock-crosscheck design randomly reassigns clocks across physical detector positions and independently estimates the distance-time slope for each clock.

For a genuine spatial signal:

\[
\beta_1 \approx
\beta_2 \approx
\cdots
\approx
\frac{1}{v}
\]

regardless of clock identity.

For a clock-specific artifact:

\[
\beta_1,\beta_2,\ldots
\]

differ systematically.

### Synthetic Result

Clock artifact:

\[
0\%
\]

survival.

Synthetic c-like spatial signal:

\[
100\%
\]

survival.

EM also survives because EM is itself a spatial c-like mechanism.

That is correct behavior.

---

## Key Scientific Lesson

No single timing classifier can identify GV.

The proper structure is a chain of independent interventions:

\[
\text{candidate}
\rightarrow
\text{clock exclusion}
\rightarrow
\text{EM exclusion}
\rightarrow
\text{environmental exclusion}
\rightarrow
\text{unexplained residual}
\]

Each gate answers only one question.

---

## Current Protocol Philosophy

The current protocol intentionally avoids the statement:

> GV detected.

The strongest permitted result is:

> UNEXPLAINED PROPAGATION CANDIDATE

That result means only that the candidate survived the conventional mechanisms actually tested.

Unknown conventional mechanisms may still exist.

---

## Why These Failures Matter

These failures materially changed the experimental design.

Without them, the project could have mistaken:

- cable propagation
- clock drift
- electromagnetic leakage
- flexible curve fitting

for new physics.

Therefore these failed synthetic approaches are retained as part of the scientific development record.

They are not hidden negative results.

They are part of the reason the current protocol is more rigorous.
