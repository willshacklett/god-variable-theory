# GV Switch Phase 0 — Hardware BOM and Instrument Selection

Status: **Pre-purchase design**

Purpose:

> Select hardware capable of validating known channels before any anomalous-signal search.

Prices are planning estimates and must be rechecked before purchase.

---

## 1. Primary Constraint

The proposed c-like branch requires nanosecond-scale timing.

At 1 meter:

\[
t \approx 3.34\ \mathrm{ns}
\]

At 8 meters:

\[
t \approx 26.7\ \mathrm{ns}
\]

Target timing uncertainty:

\[
\sigma_t \le 1\ \mathrm{ns}
\]

Preferred:

\[
\sigma_t \le 0.5\ \mathrm{ns}
\]

Sampling rate alone does not guarantee timing accuracy, but it establishes a minimum useful scale.

---

## 2. Instrument Classes

### Class A — Learning / Slow Calibration

Example class:

- USB mixed-signal instrument
- approximately 100–125 MS/s

Useful for:

- trigger logic
- sham-control development
- thermal measurements
- acoustic experiments
- software integration
- basic EM demonstrations

Not suitable as the primary instrument for a credible 1 ns timing claim.

---

### Class B — Serious Phase 0 Bench

Target:

- 4–6 analog channels
- approximately 5 GSa/s or better
- several hundred MHz bandwidth or better
- external trigger
- waveform export
- programmable control

This is the minimum class recommended for serious timing validation.

---

### Class C — Replication Grade

Target:

- 6 or more synchronized analog channels
- 5–10+ GSa/s
- 1 GHz-class bandwidth where needed
- traceable calibration
- low timing jitter
- deep acquisition memory
- automated data export

---

## 3. Current Instrument Reference Matrix

| Instrument class | Channels | Sample rate | Approx. current price | Phase 0 role |
|---|---:|---:|---:|---|
| Analog Discovery 3 | 2 scope inputs | 125 MS/s | ~$379 | software / slow calibration only |
| Teledyne T3DSO3000 family | 4 | up to 5 GS/s | from ~$5,300 | possible serious entry bench |
| Siglent SDS5036X HD | 6 | 5 GSa/s | ~$8,880 | strong Phase 0 candidate |
| Tektronix MSO46B | 6 | 6.25 GS/s | ~$14,400 | strong calibrated lab option |
| Teledyne HDO4000A family | 4 | up to 10 GS/s | from ~$14,900 | high-resolution lab option |

---

## 4. Preferred Architecture

For the six-detector experiment, synchronized acquisition is strongly preferred.

Ideal:

\[
6\ \text{detectors}
+
1\ \text{trigger/reference}
\]

A six-channel scope can acquire the detector array directly, with trigger/reference handled through external trigger or a separate reference channel depending on architecture.

If only four analog channels are available, detector groups must be measured in repeated configurations.

That introduces additional synchronization and reproducibility problems.

Therefore:

> Six synchronized analog channels are preferred over multiple unsynchronized low-cost scopes.

---

## 5. Initial Recommendation

### Recommended serious Phase 0 target

A 6-channel, approximately 5 GSa/s instrument.

Reason:

- six physical detector channels
- common acquisition clock
- approximately 200 ps raw sample spacing at 5 GSa/s
- enough temporal granularity to investigate several-nanosecond propagation differences
- fewer inter-instrument synchronization problems

This does not guarantee 200 ps measurement accuracy.

Actual timing uncertainty must be experimentally calibrated.

---

## 6. Trigger Hardware

Phase 0 does not require exotic switching hardware.

Preferred initial trigger:

- logic-controlled transistor or MOSFET switch
- low-voltage load
- independent electrical trigger/reference output

Alternative:

- calibrated pulse/function generator

Required:

- reproducible edge
- low jitter
- safe energy level
- sham mode
- trigger timestamp output

Budget target:

\[
\$50-\$500
\]

depending on whether a dedicated pulse generator is purchased.

---

## 7. Cable Set

Required:

- 50-ohm coax where appropriate
- known cable IDs
- multiple deliberate lengths
- BNC/SMA adapters
- terminators
- splitters where required

Every cable delay must be measured.

Do not assume propagation velocity solely from manufacturer nominal values.

Planning budget:

\[
\$150-\$500
\]

---

## 8. EM Monitoring

Minimum:

- near-field RF probe set
- independent RF monitoring channel
- shielding materials

Preferred:

- broadband RF detector or spectrum-monitor capability
- Faraday enclosure for detector/source control tests

Planning budget:

\[
\$100-\$1{,}000+
\]

depending on sophistication.

---

## 9. Acoustic Monitoring

Minimum:

- measurement microphone or fast microphone module
- independent acquisition channel

The acoustic channel does not need nanosecond timing.

Planning budget:

\[
\$30-\$300
\]

---

## 10. Mechanical Monitoring

Minimum:

- accelerometer
- rigid mounting point
- vibration-isolated mounting option

Planning budget:

\[
\$20-\$300
\]

---

## 11. Thermal Monitoring

Minimum:

- multiple calibrated temperature sensors
- source sensor
- detector-area sensor
- ambient sensor

Planning budget:

\[
\$20-\$150
\]

---

## 12. Shielding and Isolation

Required materials may include:

- conductive enclosure
- copper/aluminum shielding
- ferrites
- shielded cables
- feedthroughs
- isolation pads
- vibration isolation

Planning budget:

\[
\$100-\$1{,}000
\]

---

## 13. Phase 0 Budget Scenarios

### Budget A — Software / Apparatus Development

Approximate total:

\[
\$500-\$1{,}500
\]

Purpose:

- build trigger
- develop software
- validate acoustic/mechanical/thermal logic
- perform basic EM experiments

Not sufficient for strong c-like timing claims.

---

### Budget B — Serious Phase 0

Approximate total:

\[
\$6{,}000-\$12{,}000
\]

Purpose:

- multi-GSa/s timing instrument
- proper cabling
- sensors
- shielding
- controlled trigger
- hardware validation

This is the realistic target for an independent serious prototype.

---

### Budget C — High-End Phase 0 / Replication

Approximate total:

\[
\$15{,}000-\$30{,}000+
\]

Purpose:

- calibrated high-bandwidth scope
- improved probes
- redundant monitoring
- higher-quality timing reference
- stronger shielding/isolation
- replication-quality documentation

---

## 14. Do Not Buy Yet

Do not purchase hardware until these are resolved:

1. exact detector modality
2. required detector bandwidth
3. trigger topology
4. number of simultaneously acquired channels
5. reference-clock architecture
6. shielding geometry
7. cable topology
8. required waveform record length

The oscilloscope should not be selected only from sample rate.

---

## 15. First Purchase Decision

The first major decision is:

> Do we want to build a learning prototype first, or go directly to a serious six-channel timing bench?

For a real test of the c-like GV Switch branch, the recommendation is:

> Skip using a 125 MS/s educational instrument as the primary timing system and target a synchronized multi-GSa/s oscilloscope.

---

## 16. Current Shortlist

### Value-oriented serious bench

**Siglent SDS5036X HD class**

- 6 channels
- 5 GSa/s
- 350 MHz base-class bandwidth
- common acquisition system

Primary advantage:

> Six synchronized channels at a substantially lower price than many traditional lab platforms.

---

### Traditional calibrated lab bench

**Tektronix MSO46B class**

- 6 analog channels
- 6.25 GS/s
- bandwidth options up to 1.5 GHz
- calibration certificate

Primary advantage:

> Mature test-and-measurement platform with six-channel synchronized acquisition.

---

## 17. Hardware Selection Rule

Before purchase, score each candidate on:

1. synchronized channel count
2. sample rate
3. analog bandwidth
4. trigger jitter
5. timebase accuracy
6. channel-to-channel skew
7. memory
8. automation/API support
9. calibration
10. cost

The cheapest instrument is not necessarily the cheapest experiment if synchronization problems invalidate the data.

---

## 18. Next Engineering Question

The next specification must define:

> What physical quantity are the six primary detectors actually detecting?

Possible detector families include:

- electrical field
- magnetic field
- optical
- RF
- broadband electrical transient
- multiple orthogonal sensor types

The detector modality must be defined before final instrument purchase.

---

## 19. Bottom Line

Phase 0 hardware should be purchased to falsify artifacts, not to hunt for a preferred answer.

The most important instrument is the timing/acquisition system.

For the c-like branch, a synchronized multi-GSa/s acquisition platform is the current minimum serious direction.
