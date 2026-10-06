# GV-PHY-001 Sensitivity Certification

**PLAN / NOT RUN. No measured detection floor or power is claimed.** A null
cannot be interpreted merely because a trace looks quiet or a mock detects pulses.

## Search-Channel Injection Concepts

| Searched channel | Local calibrated physical stimulus | Minimum detectable feature to report |
| --- | --- | --- |
| Magnetic C03 | Known local low-energy field coil/reference probe, fixed axis/geometry and independently measured field | Extra peak field in uT over the frozen known-pathway feature prediction, within stated pulse/band/axis family |
| Acceleration C04 | Calibrated shaker/guarded impulse and local reference accelerometer on actual receiver mount | Extra acceleration peak in m/s^2 with declared waveform/mount and source-reference coupling |
| Acoustic C05 | Calibrated local pulsed pressure source and reference microphone at the sensing location | Extra peak pressure in Pa with declared spectrum/geometry and acoustic/vibration crosstalk |

No numerical amplitude is invented. Obtain baseline MAD/PSD/drift in units from
pilot, calibrate response and select an amplitude ladder in a dated qualification
protocol **before** sensitivity-validation data. The existing floor 8/residual-MAD
rule is not a physical-unit amplitude. Individual sensor detectability is necessary
but insufficient: G requires two positive residual features and <=1 ms observed-peak
coincidence. Qualify each of three channel pairs and each declared pulse family.

Test added calibrated stimuli on top of ordinary relay/control waveforms, not only
quiet sensors. Characterize effects on source witnesses and prediction K: an injection
that K learns/subtracts does not prove sensitivity to all state-linked effects. Preserve
all genuine physical propagation delays. Two locally timed stimuli test coincidence
acceptance; they do not demonstrate a natural mechanism or GV.

## Prospective Validation Counts and Uncertainty

For each declared amplitude/pulse/pair condition: 100 validation attempts in five
blocks of 20, with a separately randomized 100 stimulus-off controls. Target observed
detectability must support a **one-sided 95% lower bound >=0.90** for the frozen
detector and a control FPR bound consistent with the qualification protocol.
Calculate exact binomial bounds only if independent-trial assumptions are justified;
otherwise use a pre-data approved block-aware method or mark sensitivity inconclusive.
The target is a planning performance criterion, not calculated actual power.

All attempts count: invalid capture/stimulus delivery is disclosed and prevents
certification unless a prospectively reviewed accounting scheme justifies it.
Do not pick the smallest amplitude that looks successful from these validation
results; choose the ladder in pilot, then validate it on new data. Report hit/miss/
invalid counts, amplitudes with calibration uncertainty, model/threshold/configuration
hashes, raw/native waveform references, and confidence assumptions. A failure at a
level sets a limitation, not permission to lower the scientific threshold.

## Sensitivity Envelope and Valid Null

Publish usable units/axes/band/pulse duration, saturation range, tested coincidence
offsets, gain/filter/temperature/reset conditions and held-out detection probability.
Unknown group delay or nonlinear response may invalidate a whole waveform family.
RF-only, electric-only, delayed/noncoincident, weak/rare/single-channel/suppressive
signals and effects absorbed by K remain outside this bounded formulation.

A qualified null is limited to the **measured detectable excess-feature envelope**,
the existing windows, event counts and approved dependence/missingness inference.
Failed timing, sensitivity, controls, reset or acquisition means INVALID / INCONCLUSIVE,
not NOT SUPPORTIVE. Independent apparatus replication needs a separate sensitivity
qualification, not reuse of the author's sensor claims. See
[null checklist](../experiments/GV_PHY_001_NULL_VALIDITY_CHECKLIST.md) and
[calibration](GV_PHY_001_SENSOR_CALIBRATION.md).