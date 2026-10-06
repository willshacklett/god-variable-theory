# GV-PHY-001 Component Requirements

**Component classes only; no product selected or purchased. PENDING.** A valid
manifest describes requirements, not an approved schematic or actual apparatus.
All shortfalls below make the relevant control/qualification incomplete; they do
not justify loosening the primary statistic, timing limit or scientific endpoint.

| Class | Required performance / reason | Scientific consequence if unmet |
| --- | --- | --- |
| Relay | 5 V coil, <=100 mA, dry contacts for <=5 V/5 mA LED load; enclosed motion; selected model must specify bounce, hold/release, heating and duty limits | Unknown bounce/reset/temperature or inaccessible mechanical geometry blocks matched-control and transition qualification |
| MOSFET/transistor driver | Rated for coil current and suppressed transient, 3.3 V command compatibility, safe off pull-down, current-limited supply; select ratings only after relay choice | Uncharacterized switching/ground return can cause cross-channel pickup; no certified control |
| Flyback protection | Rated clamp/diode appropriate to selected coil, current and stored energy; document loop area and actual turn-off response | Removing/changing clamp changes the source physics and can damage inputs; invalid comparison |
| Current front end | <=0.1 A safe measurement, DC-2 kHz useful response, known burden/CMRR, differential/isolated input, fixed gain | Loop loading or common impedance defeats electrical-only/EM attribution |
| Voltage front end | <=5 V contact load, high impedance, DC-2 kHz, isolated or independently assessed differential measurement | Probe grounds can defeat load isolation; false coherent signal |
| Magnetic sensors | Three distinct source/receiver/environment chains; analog or certified deterministic conversion, DC-2 kHz, fixed axis, dynamic range determined by pilot | Slow digital polling or one-axis blind spots prevent fast/complete magnetic attribution |
| Accelerometers | Source/receiver analog chains, 10 Hz-2 kHz, documented mounting/axis, impulse/group-delay tests | Resonance/cable/fixture changes mimic isolation or suppress a real response |
| Microphones | Source/receiver calibrated pressure chains, fixed preamp gain, 20 Hz-2 kHz, AGC off, phase/overload characterization | Sound/structural crosstalk, filtering and overload defeat coincidence/null validity |
| Temperature | Body sensor with characterized slow lag plus ambient logs; safe attachment and calibrated reference | Five-second resets cannot be assumed from an instantaneous/uncalibrated temperature value |
| Photodiode/TIA | Dark/on plateau range within ADC, DC-2 kHz, optical shield, fixed gain, independently measured latency | Cannot establish S0/A/bounce; optical/electrical pickup may be mislabeled |
| DAQ/ADC | >=16 protected differential analog inputs, >=20 ksample/s per channel simultaneous aperture, export exactly 20 kHz core grid; ADC resolution/full-scale selected from measured noise/dynamic range, not guessed | Multiplexing/skew/aliasing/clipping or inadequate dynamic range invalidates timing/sensitivity |
| Command source | Deterministic 3.3 V marker and separately routed driver command; same marker path in all arms, no software-time authority | Driver marker/feedthrough can masquerade as a candidate |
| Independent oscillator | Separate power/timebase and characterized pulse edge; not derived from DAQ clock | Shared-clock "independence" cannot certify drift |
| Independent timing verifier | Calibrated scope/time-interval instrument with <=1 us reference contribution for allocated timing tests, simultaneous reference channels, documented timebase/probe delay | 20 kHz sample ticks alone cannot demonstrate 10 us sensor or clock terms |
| Isolated low-voltage power | Coil <=5 V/0.1 A, independent contact battery <=5 V/5 mA, sensors <=5 V (use reviewed conditioning if needed), no mains work; fuse/current-limit | Shared supply noise and unsafe metadata are rejected; no valid causal control |
| Shielding | Defined conductive E/RF enclosure/return connection and separately characterized magnetic material if used; maintain acoustic/mechanical conditions | Foil is not magnetic shielding; enclosure changes multiple pathways |
| Fixture | Stable nonconductive/support-reviewed source and separate receiver supports; guarded mechanical control concept, reproducible axes/cable strain relief | Shared floor/support/cable motion defeats isolation |
| Cables/connectors | Fixed IDs/length/route, differential pairs, minimal coil loop, keyed/labelled connections, shielding termination plan | Loop changes and accidental channel swaps cause false attribution |
| Dummy resistive load | Safe resistor/electronic load matched to coil steady current and documented edge; no armature | Cannot match inductance/core/contact bounce; useful limited electrical control only |
| Electrical-only surrogate | Same driver/return, immobilized fixed-core inductive surrogate and separate LED-only switch; qualified source traces, no moving contacts | No exact counterfactual; differences in core/winding/stray capacitance require disclosure |
| Mechanical-control apparatus | Guarded, independently instrumented nonconductive remote linkage driving a mechanically accessible contact/armature surrogate, coil unenergized | A sealed relay cannot be actuated identically without alteration; control cannot claim equivalence |
| Electric reference | High-impedance differential field/pickup chain, measured quasi-static response and loading, AI13 diagnostic only | Magnetic-only channels cannot explain capacitive pickup |
| RF diagnostics | Broadband probe/envelope chain on AI14, plus independent survey/injection instruments with declared frequency/amplitude/antenna coverage | Detector blind bands, overload and RF rectification forbid full EM exclusion |

The design defaults to simultaneous sampling to make the <=100 us certification
credible. A different ADC architecture needs a measured timing review before use,
not a changed endpoint. The 2 kHz useful-band target needs anti-alias transition
before 10 kHz Nyquist, stable phase response and <=10 us uncertainty per fast
sensor after independently calibrated front-end correction. These are **requirements**,
not achieved performance. No manufacturer limit, actual noise floor or ADC bit depth
is fabricated. Actual chosen parts, ratings, schematic values and safety approval
remain blank until an independent electronics review.

## Electrical and Mechanical Comparators

Electrical control is a **pair of limited comparisons**, not a magical matched
resistor: a safe resistive load checks command/driver/return pickup; a reviewed
fixed-core nonmoving inductive surrogate checks current/field behavior; LED-only
switching checks the contact-load/TIA pathway. Preserve driver/clamp/lead routing
and marker. After pilot define allowable current/voltage slew, energy, spectrum and
source-field discrepancy in physical units with uncertainty **before evaluation**.
No numerical matching tolerance can be honestly frozen without selected components
and measurement. If those cannot match in the declared domain, the control fails;
never tune the scientific threshold to absorb the mismatch.

For C3, do not open a sealed live relay or infer safety from low voltage. Review a
purpose-built accessible low-energy contact/armature fixture operated by a guarded
nonconductive linkage from outside the measurement region. Measure motion optically,
force/displacement where feasible, source sound/acceleration and repeatability.
It tests downstream motion/contact/click paths, **not** original coil/core/geometry
equivalence. Compare the genuine relay, guarded surrogate and coil-disabled dummy
in a qualification series; unmatched waveforms leave mechanical attribution
incomplete. A matched mechanical-only relay counterfactual is not yet specified.

See [construction gaps](GV_PHY_001_CONSTRUCTION_READINESS.md),
[grounding](GV_PHY_001_POWER_AND_GROUNDING.md), and [fixture](GV_PHY_001_FIXTURE_LAYOUT.md).

## EM/RF Coverage Decision

**Magnetic channels alone cannot establish known-EM attribution or full EM exclusion.**
They can witness low-frequency magnetic responses but miss capacitive electric pickup,
RF rectification, near-field polarization and instrumentation common-mode effects.

Plan D13 quasi-static electric pickup over a measured DC-2 kHz domain and D14 RF
envelope plus an independent survey with an initial engineering target 9 kHz-3 GHz.
That survey target is a **declared requirement to review**, not achieved coverage or
a selected product. The 2-9 kHz gap, >3 GHz sources (including higher-frequency
wireless electronics), probe polarization/spatial coverage and pulse-detector dead
time remain blind spots unless additional qualification covers them. Extend the
diagnostic capability if actual nearby sources or susceptibility tests require it;
never extend or alter the primary searched statistic to compensate silently.

At each declared band test low-energy pulsed coupling, envelope latency, overload,
front-end rectification and terminated/dummy receiver inputs. Log external electronics
and independent spectra. Presence can support a conventional explanation with the
appropriate intervention; absence means only "not observed within tested diagnostic
coverage." Unresolved bands/coupling prevent universal EM exclusion and keep the
apparatus attribution incomplete/PENDING. No cost envelope promises such coverage.