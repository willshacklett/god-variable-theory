# GV-PHY-001 Channel Map

Version **GV-PHY-001-MAP-1**. **DESIGN / NOT RUN; PENDING; no signal amplitudes measured.**
Logical assignment, not a selected DAQ pinout. The core NPZ/schema and scientific
endpoint remain unchanged. Use a >=16-input simultaneous-sampling ADC, 20,000
samples/s/channel, 10,000 samples, recorded marker at index 4000. All 15 listed
analog channels share that clock; AI15 is spare. No USB timestamps or unsynchronized
fast sensors. The separate verification instrument measures timing certification,
not a searched channel. Ancillary RF native spectra have their own clock and need
recorded marker alignment; they cannot establish sub-ms coincidence without certification.

## Signal Map

| ID / proposed input | Raw core name / quantity | Units | Role / sensor class | Useful bandwidth |
| --- | --- | --- | --- | --- |
| C00 / AI00 | trigger / controller marker | V | reference / buffered logic edge | DC-2 kHz minimum, characterized edge |
| C01 / AI01 | current / coil current | A | source / differential shunt or isolated current transducer | DC-2 kHz |
| C02 / AI02 | voltage / contact-load voltage | V | source/state / isolated differential voltage front end | DC-2 kHz |
| C03 / AI03 | magnetic / receiver field axis | uT | searched receiver / analog Hall or equivalent field transducer | DC-2 kHz demonstrated |
| C04 / AI04 | acceleration / receiver axis | m/s^2 | searched receiver / calibrated analog accelerometer | 10 Hz-2 kHz |
| C05 / AI05 | acoustic / receiver pressure | Pa | searched receiver / measurement microphone and fixed-gain preamp | 20 Hz-2 kHz |
| C06 / AI06 | temperature / relay body | degC | diagnostic / calibrated contact temperature sensor | DC-10 Hz or characterized slower response |
| C07 / AI07 | optical / LED contact state | V | state witness / photodiode/TIA | DC-2 kHz |
| C08 / AI08 | environment_reference / ambient field axis | uT | remote environment / analog field transducer | DC-2 kHz, not RF |
| C09 / AI09 | timing_reference / independent pulse train | V | reference / independent powered oscillator output | DC-2 kHz minimum, characterized edge |
| C10 / AI10 | em_reference / source field axis | uT | source witness / analog field transducer | DC-2 kHz |
| C11 / AI11 | mechanical_reference / source fixture axis | m/s^2 | source witness / analog accelerometer | 10 Hz-2 kHz |
| C12 / AI12 | acoustic_reference / source pressure | Pa | source witness / measurement microphone/preamp | 20 Hz-2 kHz |
| D13 / AI13 | electric_reference / local electric pickup output | V | ancillary reference / high-impedance differential electric probe | DC-2 kHz measured; probe loading documented |
| D14 / AI14 | rf_envelope_reference / RF detector envelope output | V | ancillary reference / calibrated broadband probe/detector plus independent survey | envelope DC-2 kHz; carrier coverage separately specified/measured |

All target sample rates are 20 kHz, including oversampled temperature and diagnostic
envelopes. Do not describe temperature as fast thermometry or RF carrier sampling.
Voltage/current/marker upper bounds are safety/design limits, not observed amplitudes.
All other signal and noise scales are unknown until measured. Every chain has a unique
sensor/measurement-chain ID; multi-input instrument serial numbers may appear in
supporting logs but must not silently identify two physical sensing chains as one.

## Conditioning, Calibration and Failures

All fast chains: fixed gain, differential/isolated signal path appropriate to common
mode, input protection without undocumented clipping, measured analog anti-alias
roll-off before 10 kHz Nyquist, no AGC/autorange/hidden smoothing. Record transfer
functions; usable 2 kHz response is not achieved merely by sampling at 20 kHz.
After independent front-end calibration, uncertainty <=10 us per core fast channel;
temperature is excluded from timing/coincidence with <=0.5 s characterized uncertainty.
Ancillary envelope channels need characterized delay for attribution, not permission
to subtract physical travel time. Clipping checks use declared raw full-scale, every
sample, flat-top and overload flags; a sensor can saturate upstream before ADC full-scale.

| ID | Specific conditioning / isolation | Calibration | Expected bounded null / ordinary response; failures |
| --- | --- | --- | --- |
| C00 | Logic buffer/divider within ADC range; isolate driver return from acquisition | Split edge, external timebase, channel skew | Marker exists in every arm, even sham; feedthrough/bounce can mimic events |
| C01 | Low-burden shunt, differential amplifier or rated isolation; freeze loop geometry | Known DC current plus dynamic step/impulse | Coil switching is expected; shunt loading, shared return and thermal drift |
| C02 | High impedance contact-voltage sensing, separate load-domain isolation | DC/step source, impedance/loading check | Contact closure/bounce ordinary; measurement can defeat battery isolation |
| C03/C10/C08 | Fixed field axis, isolated low-noise supply, measured conditioning | Known field amplitude/axis, dynamic coil field with independent timing | Ordinary coil/ambient fields expected; offset, saturation, RF rectification, wrong axis |
| C04/C11 | Rigid documented mounting, isolated conditioning, strain relief | Calibrated shaker/impulse and local reference transducer | Impacts/ringing ordinary; mounting resonance, floor paths and cable loading |
| C05/C12 | Fixed-gain preamp, separate supports/supplies where feasible | Pressure calibrator plus local dynamic reference | Relay clicks/room sound ordinary; preamp delay, vibration crosstalk, AGC/overload |
| C06 | Thermally characterized attachment, no shared noisy sensor supply | Reference thermometer across safe range; lag/noise | Slow heat rise/drift ordinary; self-heating and poor contact |
| C07 | Fixed-gain TIA, optical hood, isolated load/probe path | Dark/on plateaus, independent light pulse and edge latency | LED/contact state ordinary; ambient light/electrical pickup, TIA clipping |
| C09 | Independently powered oscillator buffered into common ADC | Faster external instrument, period/drift/skew tests | Pulses diagnose gross drift only; shared clock/trigger pickup and aliasing |
| D13 | Differential high-impedance pickup; measure capacitance, shielding/return effects | Calibrated electric coupling, dummy terminated probe and step response | Pickup can explain apparent receiver signals; local probe is not full spatial E-field coverage |
| D14 | RF probe/detector overload protection, fixed envelope gain/filter | Frequency/amplitude sweeps, pulsed RF and independent spectrum survey | EMI bursts expected; blind bands, detector nonlinearity, rectification and envelope latency |

Null does not mean all channels are flat: a relay normally produces electrical,
magnetic, vibration and acoustic responses. A meaningful null means **no additional
qualified residual** in the existing bounded rule, with all validity gates passed.
Witness association alone cannot prove causal attribution. See [calibration](GV_PHY_001_SENSOR_CALIBRATION.md),
[timing](GV_PHY_001_TIMING_PLAN.md), and [null gates](../experiments/GV_PHY_001_NULL_VALIDITY_CHECKLIST.md).

## Raw and Ancillary Storage

Core storage is exactly the existing 13 arrays plus sample index, with no new
searched features. Archive D13/D14 native common-clock waveforms as separate immutable
ancillary files with indices, units, calibration and configuration hashes. Save RF
survey spectra/marker-alignment logs separately; never fuse their host timestamps
into core timing. The prototype replay interface writes core arrays only. Ancillary
device/export integration remains a construction-readiness gap, not an implemented
driver. No primary endpoint or candidate threshold changes are authorized here.