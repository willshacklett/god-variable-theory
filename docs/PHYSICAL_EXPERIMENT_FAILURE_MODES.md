# Physical Experiment Failure Modes

**GV-PHY-001: DESIGN / NOT RUN.** This checklist is prospective. No listed cause
is excluded merely because a sensor or a checkbox exists.

| Failure mode | Diagnostic / response |
| --- | --- |
| Ground loops | Differential inputs, single reviewed grounding plan, disconnected-source test; do not defeat protective earth. |
| EMI/RFI pickup | Field/electric probes, shield/cable/orientation swaps; Hall sensor bandwidth alone does not exclude RF. |
| Shared power supplies | Independent source/sensor supplies, supply rails recorded; shared impedance can synchronize all channels. |
| USB timing jitter | Hardware-clocked buffered DAQ and trigger channel; never use host arrival times. |
| OS scheduler jitter | External deterministic marker; load-test software logging separately. |
| Aliasing | Document analog anti-alias filters and repeat prespecified calibration at alternate sample rates; do not post-hoc search rates. |
| Clipping / ADC saturation | Record full-scale and range, check every sample; retain invalid captures, do not analyze flat-tops as a residual. |
| Sensor ringing | Calibrated impulse/step response and fixed group-delay model; echoes are ordinary dynamics. |
| Cable movement | Strain-relieved cables, dummy/sham movement, swapped cable IDs. |
| Microphone/vibration crosstalk | Reference microphones/accelerometers, independent acoustic and structural isolation. |
| Temperature drift | Warm-up logs, randomized blocks, thermal time-shift controls; thermal lag is not instantaneous temperature. |
| Magnetic pickup | Coil/source field witness, axis/placement swaps; measured attenuation, not assumed magnetic shielding. |
| Trigger bounce | Independently recorded controller edge; multiple edges invalidate authoritative t0. |
| Relay bounce | Optical/contact-voltage waveform; preserve ordinary bounce/settling, never call it a GV transient. |
| Sensor placement bias | Frozen coordinates, ID/position swaps, distance changes independent of shielding. |
| Clock drift | Independent timebase/oscillator calibration before and after each session. |
| Synchronization offsets | Split-pulse channel-skew test and sensor-specific latency corrections with uncertainty. |
| Hidden filtering | Disable undocumented device filters; archive transfer function and firmware/settings. |
| Automatic gain control / autorange | Disable/lock gains; changed calibration invalidates locked comparisons. |
| Operator movement | Remote operation, movement log/reference sensors, blinded randomized order; operator is not fully blinded to fixtures. |
| Table/floor vibration | Separate fixtures, floor/source references, mechanical isolation intervention. |
| HVAC / acoustic background | Reference microphone/environment logs, randomized times, retained negative runs. |
| Mains frequency | Log nearby electronics and spectrum only as declared diagnostic; no mains experiment or post-hoc notch rescue. |
| Nearby electronics | Disconnected-source/control command trials, radio/supply monitoring, electronic-device inventory. |
| Post-hoc window selection | One fixed primary window and threshold; exploratory windows require new held-out confirmation. |
| Sham/label leakage | Separate operator key/seed, generic public configuration tokens; freeze results before unblinding. Waveforms still can reveal conditions. |
| Ordinary control/feedback dynamics | Same controller/flyback/LED paths in controls; do not confuse programmed settling with a distinctive mechanism. |
| Model inadequacy / omitted cause | Held-out diagnostic controls, simpler baselines and sensor coverage review; residual is not attribution. |
| Invalid-run selection / early stopping | Fixed attempted counts, prespecified flags, all raw captures retained; no replacement based on an interesting trace. |
| RF rectification / electric-field blind spot | A low-frequency Hall witness cannot exclude it; qualify electric/RF response and terminated dummy receiver inputs before unexplained attribution. |
| Current-loop geometry / coil core hysteresis | Freeze return routing, loop area and axes; source current alone is not a magnetic transfer model. |
| Contact bounce / LED probe coupling | Preserve voltage/optical/current traces; isolated battery load can still couple through capacitance or instrument grounds. |
| Frequency-dependent group delay | Scalar latency cannot remove arbitrary dispersion; characterize transfer functions or invalidate the v1 timing assumption. Never subtract real propagation. |
| Calibration stream/content leakage | Reject overlapping UUIDs and waveform fingerprints; mock seeds are stage/run-namespaced. Different IDs alone do not establish independent data. |
| Frozen threshold/model drift | Require pre-evaluation external lock and internal cross-binding; self-rewritten hashes cannot prove immutability. |
| Missing-not-at-random runs / clustering | Retain all attempts and worst-case missing-event bounds; independent-binomial intervals are not certified for correlated blocks. |

Failure of timing, calibration, sensitivity, required controls or acquisition is
**INVALID / INCONCLUSIVE**, not support and not a valid null. Known-pathway
attribution or a reliable null rejects the stated detectable-signature formulation,
not every conceivable GV proposal. See the [preregistration](../experiments/GV_PHY_001_PREREGISTRATION.md).