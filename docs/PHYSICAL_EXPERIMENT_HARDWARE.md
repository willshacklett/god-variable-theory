# GV-PHY-001 Hardware Architecture

**STATUS: DESIGN / NOT RUN. No equipment selected, bought or certified.**
This v1 is distinct from E1's ns timing experiment. It measures bounded low-energy
relay transitions at millisecond scales; no c-like propagation inference is possible.

## Wiring and Interfaces

Use one external controller to emit a 3.3 V acquisition marker and separately
drive a rated low-side relay driver. Driver/flyback protection must follow relay
and driver ratings; do not remove clamps to seek a transient. Supply the coil from
a fused/current-limited <=5 V isolated supply, <=100 mA; allow at least 5 s between
commands and monitor temperature. Keep duty cycle <=10% during engineering and
reassess only through a prospective safety revision. Dry contacts switch a separate
<=5 V, <=5 mA battery LED/resistor circuit. Measure contact voltage at high impedance.
The intended hold is 0.300 s followed by coil-off reset. Five seconds is a minimum,
not a demonstrated thermal/structural settling time; longer fixed gaps require a
prospective qualification amendment before evaluation, not selective per-event waits.

Route shielded/differential analog signals to one >=16-channel simultaneous-sampling
DAQ at 20 ksample/s/channel. A multiplexed ADC is acceptable only if measured skew
and latency satisfy the same budget. Grounding, differential input common-mode
range, sensor supply isolation and digital/analog return paths require a reviewed
schematic. A microcontroller schedules triggers, not authoritative sensor timestamps.

Receiver fixture initially 0.5 m from source; second fixed position 1.0 m for
distance controls. Source references mount near relay, receiver sensors on a separate
fixture, environmental reference away from source and receiver. Record coordinates,
orientation, supports, cable IDs/lengths, gains/filters and photographs. Swap sensor
IDs/cables/positions during engineering to detect placement artifacts. Do not infer
EM attenuation from a metal box or magnetic attenuation from ordinary foil.

## Channels

All 13 channels are essential for the complete confirmatory assay. Tier 1 may
omit some only for instrumentation debugging, never to call an unexplained signal.
Bandwidths below are design minima/targets, not measured specifications or noise floors.
Select analog-output sensors or benchmark digital sensors with timestamped hardware
sampling; USB/polling magnetometers alone cannot meet this architecture.

| Channel / units | Purpose | Useful analog bandwidth | Scale / calibration / failure modes |
| --- | --- | --- | --- |
| trigger / V | Controller hardware marker | DC-2 kHz minimum; characterize edge/filter delay | 3.3 V nominal; level/edge/skew calibration; bounce, ground pickup, clipping. |
| current / A | Coil/load electrical pathway | DC-2 kHz | <=0.1 A intended; shunt/isolated current sensor gain and step response; common impedance, heating. |
| voltage / V | Contact/load state and electrical transient | DC-2 kHz | <=5 V intended; differential/high-impedance isolated measurement; ground loops or probe loading. |
| magnetic / uT | Receiver candidate magnetic response | DC-2 kHz | Signal/noise unknown until calibration; injected field/gain/axis/latency check; Hall offset, ambient mains, saturation. |
| acceleration / m/s^2 | Receiver candidate structural response | 10 Hz-2 kHz | No claimed scale; known low-energy tap/shaker and transfer response; mounting resonances/ringing. |
| acoustic / Pa | Receiver candidate pressure response | 20 Hz-2 kHz | No claimed scale; acoustic calibrator or traceable reference; AGC disabled, vibration crosstalk. |
| temperature / degC | Coil/room thermal drift | DC-10 Hz sufficient | Ambient plus small coil rise, not a frozen measured effect; calibrated reference thermometer; response lag, self-heating. |
| optical / V | Independent LED/contact post-state | DC-2 kHz | Bounded photodiode/TIA output inside ADC range; dark/on plateaus, comparator/edge latency, ambient light pickup. |
| environment_reference / uT | External low-frequency magnetic witness, not an RF monitor | DC-2 kHz | Unknown ambient scale; same field calibration as receiver; local gradients/shared supply confounds. |
| timing_reference / V | Independent oscillator/timebase check | DC-2 kHz minimum; characterize pulse/filter delay | 3.3 V nominal 20 Hz pulse train, known uncertainty; verify pulse periods and pre/post offsets on an independent instrument. |
| em_reference / uT | Source-proximal magnetic witness | DC-2 kHz | Calibrate field/axis/latency; source field may saturate. Not the receiver candidate channel. |
| mechanical_reference / m/s^2 | Source/fixture vibration witness | 10 Hz-2 kHz | Calibrated reference injection; floor/fixture paths and cable loading. |
| acoustic_reference / Pa | Source-proximal pressure witness | 20 Hz-2 kHz | Calibrated pressure/latency; cross-talk/room echoes. |

A Hall sensor does not monitor every RF electric-field pathway. An RF/electric
probe and broader-band scope are optional Tier 2 diagnostics; lack of coverage
prevents a claim that all EM mechanisms were excluded. Temperature sampled by the
DAQ can be oversampled; its bandwidth/lag must not be described as 50 us thermometry.
RF/electric-field characterization and impedance-matched dummy receiver inputs
are required qualification tests before any unexplained attribution, even though
they are not added to the three searched channels. RF may rectify into low-frequency
outputs. A 2 kHz Hall channel cannot certify its absence. Coil current-loop geometry,
core magnetization and three-axis pickup must be characterized; one-axis witnesses
are incomplete causal coverage. The temperature channel measures coil/body temperature;
ambient temperature is separately logged in environmental metadata.

## Timing Budget and Calibration

Target **<=100 us worst-case relative uncertainty**, not 1 ns. Prospective budget:
50 us relative edge quantization (20 kHz), <=20 us residual channel skew,
<=20 us pairwise corrected front-end delay uncertainty (<=10 us per sensor),
<=10 us trigger/reference
comparison and clock drift within the capture. Sum bounds conservatively; correlated
errors cannot be combined as independent Gaussian uncertainties to shrink the budget.

Record each marker as a channel and the independently powered oscillator as another
channel. The oscillator diagnoses drift but is not a second independent timestamp
for every sensor. Validate common-clock skew with a split electrical injection;
characterize each sensor's analog latency with its appropriate physical injection.
Use an independent scope/timebase to test command-marker latency/jitter, pulse periods,
missing samples and pre/post drift. Software logs/USB arrival time are audit-only.

Calibrated fast sensor latency can exceed 10 us; **uncertainty after correction**
must meet 10 us per channel. If this cannot be achieved with the selected sensor/DAQ, v1 is
not valid: revise the design/version prospectively, not just relabel poor timing.
The slow temperature channel instead permits characterized latency uncertainty
<=0.5 s; it never participates in fast coincidence or propagation timing.
The toy pulse-period check catches gross errors only; a 20 Hz pulse sampled at
20 kHz cannot certify the 10 us clock-budget term. Independent calibration must.

Clock offsets can align unrelated impulses; event-loop jitter, hidden filters or
a shared trigger leak can make a false synchronized residual. Cable/sensor swaps,
independent reference tests and frozen latency corrections are required.

This target is not certified by any proposed product or by the mock. Qualification
requires documented simultaneous aperture/skew or a measured multiplexing scan
table, no dropped samples, a stable clock independently checked across the 0.5 s
record, external reference resolution substantially below 10 us, and gain/filter/
temperature/amplitude-dependent transfer measurements for every fast sensor.
The trigger/reference passband must roll off before the 10 kHz Nyquist frequency;
the old >=10 kHz analog-bandwidth wording left no anti-alias transition band.
Characterize rather than conceal that filter's delay. USB buffering and OS jitter
must not alter sample ordering. A fixed scalar latency is inadequate for frequency-
dependent phase/group-delay dispersion outside a calibrated pulse family. Such
channels fail v1 qualification; do not "correct" them by aligning physical events.
Microphones, accelerometers and digital magnetometers with undocumented smoothing/
AGC can readily fail these requirements. Tier 1 is therefore not a timing-qualified
apparatus, and Tier 2 feasibility/cost cannot be asserted until a capability review.

## Calibration and Run Acceptance

Before data: document sensor serials/axes, units, gains/offsets, measured full-scale,
ADC ranges, anti-alias filters (stopband adequate before 10 kHz Nyquist), bandwidth,
transfer/group-delay uncertainty and calibration versions. Disable AGC/autorange and
hidden smoothing. Use appropriate voltage/current/field/pressure/acceleration and
thermal references. Never claim traceability if only comparative calibration exists.

Verify S0/T/A on electrical and optical channels, independently inject known
multi-channel disturbances, retain raw responses and establish sensitivity in units
and baseline sigma. Required positive-injection checks must work above the declared
floor; failed sensitivity makes absence of detections inconclusive. Characterize
warm-up, bounce and fixture reset. The 500 ms record contains -200..+300 ms around
the hardware marker. Positive calibration pulses are ordinary controls, never GV.

## Tiers and Planning Costs

Ranges are rough USD planning allowances, **not researched quotes**; assume some
lab access/borrowed equipment, exclude labor/computer, taxes and shipping. No shopping
list or purchase is required. Calibration/instrument access can dominate the price.

| Tier | Component classes / required capability | Planning range / evidential role |
| --- | --- | --- |
| 0 simulation | Existing Python environment and mock arrays/manifests | $0 incremental hardware; pipeline only. |
| 1 instrumentation proof | 5 V relay/driver/LED fixture, isolated supply, basic current/voltage/optical, mic/accelerometer/field modules, borrowed scope or DAQ | $200-800 with borrowed instruments; may fail synchronization/sensitivity and cannot complete the full assay. |
| 2 credible synchronized test | >=16 simultaneous analog inputs at >=20 kHz/channel, appropriate ADC ranges/anti-aliasing, all 13 channels, independent oscillator/scope, isolated front ends, calibrated references, shielding and separate fixtures | $1,500-6,000, potentially more without borrowed calibration tools; must pass all gates. |
| 3 independent replication | Separately sourced/calibrated DAQ/sensors/fixtures, independent operator/site/timebase, same frozen protocol with independently documented transfer functions | $5,000-15,000+; apparatus independence matters more than price. |

## Safety and Build Review

No mains connections, high voltage, ionizing radiation, hazardous pressure,
explosives or chemical experiments. Ordinary relay inductive transients still need
rated suppression and protected DAQ inputs. Fuse/current-limit supplies; no large
capacitor banks. Enclose contacts/armature and protect fingers/eyes during mechanical
controls. Check component heating, stop on unexpected temperature/current, and keep
flammable material away. Never defeat scope earth or improvise mains isolation.
An electronics reviewer must approve the actual schematic and instrument interface
before construction. Component-specific driver/software and wiring are not supplied
as a certified build today; this limitation keeps the program PENDING.