# GV-PHY-001 Sensor and Transfer Calibration

**PROCEDURE DESIGN / NOT RUN. No calibration certificates or noise floors exist.**
Each chain requires a versioned artifact naming sensor/axis, DAQ/range, supply,
mount, cable, gain/filter, units, UTC validity dates, software/configuration hash,
reference instrument, uncertainty and reviewer. Version validity is not proven by
a string or date; retain the actual waveform/reference certificate. No synthetic
calibration may certify a physical chain.

## Common Procedure

Select reference waveforms/amplitudes and safe operating limits after actual part
review but **before qualification data**. Archive 10 repeats at each prespecified
amplitude/frequency/pulse family, including below/near/full useful range without
unsafe overload. Record ambient/coil temperature and supply condition. Never
discard an unexpected response merely because it breaks the expected transfer.

Measure DC gain/offset where meaningful, response magnitude/phase across the useful
band (proposed logarithmic frequencies 10, 20, 50, 100, 200, 500, 1000, 2000 Hz where
the sensor supports them), impulse/step ringing, baseline MAD/PSD and drift. Low-
frequency/high-frequency points outside a sensor's useful range are diagnostic,
not claimed sensitivity. Show repeatability and uncertainty, not one best pulse.

Test clipping **both** upstream sensor/preamp overload and ADC full-scale: overload
flags, flat-tops, gain reversals, recovery and dynamic range. Safe overload tests
require selected ratings/input protection; no damage or high-energy source.
Disable AGC/autorange/hidden smoothing. Freeze gain/offset/range/latency table only
after independent review. An ADC range alone cannot detect saturated Hall cores,
microphone preamps or accelerometers.

## Chain-Specific Reference Concepts

| Chain | Amplitude / latency / response calibration | Dominant limitations |
| --- | --- | --- |
| Marker, independent timing reference | Calibrated voltage/edge into split inputs, external verifier and measured probe/cable delay; DC-2 kHz passband and pulses | Sampled 20 Hz periods cannot certify microsecond offsets; shared trigger/ground paths |
| Coil current | Known low-energy DC current/shunt comparison, dynamic current measured by independent reference, slew/phase test | Shunt burden and amplifier common-mode; changed loop geometry |
| Contact voltage | Calibrated <=5 V source/steps and high-impedance probe comparison | Probe loading/ground coupling can change the load itself |
| Three magnetic chains | Calibrated local field coil/reference probe, axis/direction sweep, controlled pulse and frequency response | Single-axis blindness, coil field nonuniformity, core/offset/supply drift; no RF exclusion |
| Source/receiver accelerometers | Calibrated shaker/impulse with local reference sensor, fixed mounting, frequency/phase sweep | Mount resonance and cable force; no subtraction of propagation through fixture/floor |
| Source/receiver microphones | Pressure calibrator for amplitude; local pulsed acoustic source with co-located reference microphone for phase/lag | Propagation to remote microphone must remain physical delay; preamp AGC/overload/room reflections |
| Optical contact state | Dark/on plateau, independent pulsed light and calibrated voltage/light reference | Ambient light/TIA saturation and electrical feedthrough |
| Body temperature | Reference thermometer across safe range, attachment lag/self-heating, repeated warm/cool baseline | Slow lag remains diagnostic, not fast timing or a short-window thermal exclusion |
| Electric reference | Calibrated quasi-static electric coupling/probe loading plus electrical step; document geometry | Pickup voltage is not calibrated V/m without a field calibration; local spatial blind spots |
| RF envelope reference | Known-frequency/amplitude/pulsed low-energy RF injection and independent survey/probe; detector envelope delay/filter/overload | Carrier bands, polarization, near-field/far-field geometry and rectification; not full EM exclusion |

Latency references are local to the sensor sensing element/input. Never estimate
"sensor delay" by forcing remote acoustic, mechanical or EM peaks to coincide.
Separate sensor and analog-filter phase uncertainty as in the [timing plan](GV_PHY_001_TIMING_PLAN.md).
Unmodeled frequency-dependent group delay fails scalar-offset qualification.

Noise floor is measured per chain/unit/mount/temperature, using fixed idle/sham
records and baseline windows. Report autocorrelation, drift and operator/HVAC
conditions; MAD conversion is not a guarantee of Gaussian noise. Certification
needs the [end-to-end sensitivity plan](GV_PHY_001_SENSITIVITY_PLAN.md), not merely
a sensor datasheet or visible pulse. Changed gain/filter/cable/mount invalidates the
affected calibration and creates a new configuration hash. Recalibration must not
use evaluation labels/outcomes to rescue the detector.