# GV-PHY-001 Timing Certification Plan

**PLAN ONLY; NOT CERTIFIED.** Preserve 20 kHz core sample grid, <=100 us relative
uncertainty and existing 1 ms peak coincidence. No speed/mass/GV inference follows.
Default architecture requires simultaneous-sampling shared-clock ADC inputs.

## Conservative Pairwise Budget

The following allocation separates terms previously grouped. Values are **maximum
uncertainty contributions**, not measured delays. Use worst-case bounds, not root-
sum-square of conveniently independent errors. Do not double count a delay and its
calibrated residual uncertainty. A reviewer must approve the measured accounting.

| Contribution | Allocated pairwise bound | Measurement / failure |
| --- | --- | --- |
| Sample quantization | 50 us | Two sampled peaks at 50 us intervals: conservative relative bound; bench split-pulse tests with varied phase validate indexing |
| ADC channel/aperture skew | 20 us | Same conditioned reference into every input, swap channels/cables, compare against independent simultaneous verifier; do not use datasheet alone |
| Analog filter group-delay uncertainty | 10 us total (5 us per chain) | Physical/electrical impulse and sweep across declared passband, input gain/amplitude/temperature extremes; unknown dispersion fails |
| Sensor group-delay uncertainty | 10 us total (5 us per chain) | Appropriate local field/pressure/acceleration/light reference at the sensor, independent verifier; no source-to-receiver travel subtraction |
| Marker/trigger delay uncertainty | 3 us | Compare controller marker and command output externally before/after session; actual relay actuation latency is retained, not corrected |
| Clock drift/timebase | 3 us over 0.5 s | Independent calibrated timebase, pre/post session interval measurements; target <=6 ppm contribution over capture, measured not assumed |
| Timestamp/index error | 0 us permitted | Hardware indices only; lost/duplicated/reordered samples or authoritative USB/OS timestamps invalidate capture rather than spending budget |
| Reference/verifier/probe uncertainty | 4 us | Verifier/probe/cable uncertainty accounting with <=1 us individual verifier contribution; calibrated cable swaps, shared reference common-mode not independence |
| **Total** | **100 us** | All mandatory contributions demonstrated jointly over operating conditions |

Combined sensor/filter uncertainty <=10 us per fast core chain agrees with existing
metadata limit. A nominal 2 kHz sensor may have hundreds of us delay; only independently
calibrated delay can be corrected, and **uncertainty/dispersion** must fit allocation.
One scalar cannot flatten unknown phase response. Peak time depends on waveform;
qualification is limited to a predeclared pulse family/bandwidth/amplitude domain.

## Certification Procedure

1. Archive actual DAQ, firmware/filter/range/channel map, clock source, wiring and
   verifier/probe calibration records. Hold configuration fixed during qualification.
2. Capture a split test pulse at 20 randomized phases within a sample interval and
   5 repeats each (100 attempts). Repeat routing/channel swaps; retain all raw files.
   This validates quantization/indexing and skew, not physical sensor response.
3. For each fast chain, characterize amplitude response, phase/group delay and
   uncertainty with at least 10 repeats for each predeclared local reference pulse
   shape, amplitude and gain/filter condition. Use the [sensor plan](GV_PHY_001_SENSOR_CALIBRATION.md).
   More measurements may be prospectively required; these counts are engineering,
   not evidence/power calculations.
4. Measure independent 0.5 s intervals, marker-command delay, cable/probe delays
   and drift before/after each block/session and across safe temperature/duty states.
   A 20 Hz pulse sampled at 20 kHz is only a gross check, not a 3 us drift certificate.
5. Add measured upper bounds and calibration uncertainty conservatively for every
   relevant pair. Any term above allocation, missing transfer record, nonlinear delay,
   AGC, sample loss or inability to resolve the reference makes certification fail.
6. Freeze approved offset table, validity domain, file hashes and report/version
   before evaluation; use signed independent review and external retention.

The proposed component classes have **not** demonstrated this budget. Required
verifier resolution and sensor transfer stability may exceed affordable hobby
instrumentation. Upgrade hardware capability or publish a separately reviewed
physical-design revision; never silently relax 100 us or 1 ms to suit parts.

## Diagnostic and External Timing

AI13 electric pickup and AI14 RF-envelope outputs share the core ADC clock. Their
envelope/front-end delays need measurement for association; uncalibrated carrier/
envelope latency cannot establish precise arrival. Independent RF spectra and
scope recordings retain their own acquisition clock and common recorded marker.
They remain ancillary until alignment uncertainty is certified, and never enter G.
Temperature is slow and excluded from all fast coincidence/timing tests. USB receipt
and ISO timestamps are audit trail only. Controller/coil/contact bounce and acoustic/
structural propagation delays are physical observables, not sensor offsets.