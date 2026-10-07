# Physical State-Transition Program V1

**GV-PHY-001 HAS NOT BEEN RUN. STATUS: DESIGN / NOT RUN.**
Ledger status: PENDING, not assembled/certified hardware. This is a prospective
design and mockable software skeleton, not a measured GV signature.

> A residual is only a residual until known explanations are excluded.

**UNEXPLAINED ≠ GV; GV ≠ NEW PHYSICS; NEW PHYSICS ≠ GOD.**

## Existing Material Audit

The starting main commit is `22a3296a6bc7af80fc758bcadef8e4c72eb4b976`.

| Real repository material | What it establishes / what is missing |
| --- | --- |
| [Phase 0 hardware specification](../experiments/GV_SWITCH_PHASE0_HARDWARE_SPEC.md) and [BOM](../experiments/GV_SWITCH_PHASE0_BOM.md) | Known-channel acceptance designs, geometry and planning costs; no completed apparatus calibration. Its <=1 ns goals concern a different propagation experiment, not this v1 build. |
| [E1 preregistration](../experiments/GV_SWITCH_E1_PREREGISTRATION.md), [sensor specification](../experiments/GV_SWITCH_ELECTRIC_SENSOR_SPEC.md), assembly/wiring/procurement files | Real documented passive electrical-transient prototype and 576-trial plan, not physical results or a GV detector. |
| [E1 manifest](../experiments/gv_switch_e1_trial_manifest.py), [blocked manifest](../experiments/gv_switch_e1_blocked_manifest.py), [CSV schema](../experiments/GV_SWITCH_E1_CSV_SCHEMA.md), [calibration runner](../experiments/gv_switch_e1_calibration_runner.py) | Working trial/software concepts. CSV summaries lack explicit ADC full-scale/complete sample-clock evidence; default report writing can overwrite a path under experiments. New immutable raw storage does not alter those historical tools. |
| [Clock](../experiments/gv_switch_clock_crosscheck.py), [EM](../experiments/gv_switch_em_isolation.py), [environment](../experiments/gv_switch_environment_isolation.py), master protocol | Generated-model control logic only. Master gates use separate datasets, not one measured signal through all controls. |
| [Modality specification](../experiments/GV_SWITCH_DETECTOR_MODALITY_SPEC.md), [failure notes](../experiments/GV_SWITCH_FAILURE_NOTES.md) | Useful sensor/exclusion requirements and failed timing classifiers. No transferable physical sensitivity/noise measurements. |
| Local tuning / TUNING-HW-001, EM-001, EM-002 | Provenance remains missing; no continuity, aliases, protocols, or completion invented. This new ID is separate. |
| Experimental notebooks/raw waveforms | No tracked physical acquisition notebook or validated physical waveform dataset found in this main baseline. CI plots/CSV and tether simulations are not physical measurements. |

Missing: apparatus selection, actual transfer functions, noise floors, calibration
waveforms, verified timing budget, build-specific wiring review, hardware driver,
physical model adequacy, and independent validation. A useful design can be
published before any purchase; these gaps keep the ledger PENDING.

## Chosen System and Measurable States

Use one enclosed **5 V low-power electromechanical relay**, coil current <=100 mA,
with an isolated battery-powered LED/resistor load on its dry contacts. Limit the
contact load to <=5 V and <=5 mA. Use a rated driver and flyback clamp. No mains,
large energy-storage capacitors, exposed moving linkage or hazardous materials.

A relay is cheap, resettable and permits many repetitions; electrical, magnetic,
mechanical, acoustic and thermal pathways are all expected and measurable. A motor
adds rotation/control/settling complexity, heaters are slow, and a simple LED load
does not exercise mechanical/acoustic exclusions. This is not selected because a
relay is expected to produce GV. LED-only switching is a control, not an exotic source.

- **S0:** coil off, contacts open, optical LED response below 10% of the calibrated
  on plateau, current below 5% of the on plateau, stable for 150 ms before the marker.
- **T:** external controller command recorded as a hardware voltage edge; coil
  energization and independently measured contact/optical change are retained.
  Coil latency/contact bounce are ordinary dynamics, not signatures of GV.
- **A:** contacts closed and optical response above 90% of calibrated on plateau,
   with optical/current plateau within +/-5% over [0.250,0.300) s after the marker.
  A is the observed post-state, **not GV**. Contact voltage corroborates optics.

These are prospective acceptance definitions, not established measurements. Failed
active transitions are retained and flagged by the acquisition operator before
unblinding. In sham/idle arms A need not occur. Each trial resets to S0. Controller
software only schedules commands; no feedback optimization seeks an unusual trace.

## Architecture and Controls

See [hardware](PHYSICAL_EXPERIMENT_HARDWARE.md) for 13 channel definitions, wiring,
calibration and a 100 us relative-timing target. Candidate channels are fixed:
remote magnetic, acceleration and acoustic channels. Source-proximal monitors,
electrical measurements and an external environmental reference predict ordinary
responses. Temperature and optical state are diagnostic, not additional searched
candidate channels. No c-like propagation, mass or field inference is possible
with this timing/bandwidth.

| Control | Manipulation / result that defeats independent-channel attribution |
| --- | --- |
| 0 idle | Record the acquisition marker but inhibit the driver command. Background signatures expose acquisition/environmental artifacts. |
| 1 disconnected | Issue identical command, disconnect relay coil; preserve controller/DAQ behavior. Residual here points to trigger/electrical pickup. |
| 2 load-only | Replace coil with current-matched resistive load/LED, no moving parts; match measured current/slew where practical. Responses tracking this path are ordinary electrical/EM effects. |
| 3 mechanical | Coil off; safely move armature with nonconductive linkage and optically time motion. This is a separate known-mechanical validation, not an assumed perfect counterfactual. Its altered trigger/latency must be characterized; unusable matching makes the control incomplete. |
| 4 EM / distance | At fixed 0.5 m geometry vary measured shielding attenuation; separately move receiver to 1.0 m with cables/configuration calibrated. Never change distance and shielding together as a single causal contrast. |
| 5 mechanical isolation | Change source/receiver structural connection while keeping sensor/cable geometry fixed; monitor fixture/floor acceleration. |
| 6 acoustic isolation | Add a noncontact acoustic barrier, preserve mechanical mounting; log source/reference microphone. Validate barrier response rather than assuming it. |
| 7 thermal shift | Repeat after a controlled warm-up/cool-down of the safe low-power coil; offset temperature windows and log drift. Avoid changing electrical amplitude unnoticed. |
| 8 randomized sham | Same command/marker/acquisition paths and duration, driver prevented from moving the relay; balanced hidden event ordering. |
| 9 blinding | Keep event/configuration labels and random seed in an operator-only key. Freeze per-run analysis before revealing labels; use independent label custodian where possible. |

Eight diagnostic arms in software correspond to controls 0-7; control 4 has two
separately logged subconditions. Randomized shams form the primary comparator;
blinding is a procedure, not an extra experimental arm. Tier 1 may only validate
instrumentation; missing/failed required controls prevent confirmatory interpretation.
The C3 motion counterfactual and shielding/material effects require pre-hardware review.

## Attribution, Not Identification

Hardware timing/trigger failures -> TIMING ARTIFACT; voltage/current pickup ->
ELECTRICAL TRANSIENT; EM -> KNOWN EM; vibration -> KNOWN MECHANICAL; pressure ->
KNOWN ACOUSTIC; temperature -> KNOWN THERMAL; indices/processing -> SOFTWARE
ARTIFACT; external references -> KNOWN ENVIRONMENTAL. Multiple causes remain
multiple causes, not an invitation to choose the preferred explanation.

The software's reference-channel labels are **provisional screening attributions**.
Association alone does not establish causality. Causal interpretation requires
the randomized interventions and validated controls above. A high residual is
retained even when a known reference is also present; it may mean model inadequacy.

Only a repeatable signature surviving all relevant validated controls and a locked
repeat could be discussed as an **UNEXPLAINED PROPAGATION CANDIDATE** under the
existing vocabulary. Here that name does not assert spatial propagation or speed.
It is not a GV candidate; the [claims ladder](CLAIMS.md) still applies. This v1
software cannot issue a physical success/GV verdict automatically.
Single-record physical scores use UNATTRIBUTED RESIDUAL - REQUIRES CONTROLS,
never the synthetic suite's unexplained-candidate label.

## Independent Build and Run Workflow

1. Read the [prospective preregistration](../experiments/GV_PHY_001_PREREGISTRATION.md),
   [failure modes](PHYSICAL_EXPERIMENT_FAILURE_MODES.md), and hardware interface.
2. Set up Python 3.11 with the existing research lock. No new dependency is needed.
3. Conduct 40 engineering attempts only; verify low-energy safety, S0/T/A mapping,
   clock, front-end bandwidth, clipping flags, references and known injections.
4. Collect separate model-calibration and sham threshold-calibration sets. Freeze
   code commit, model/threshold hashes, calibration versions, units, apparatus IDs
   and manifest hashes before opening evaluation data. Retain unsuccessful attempts.
5. An operator creates randomized manifests before collection. Analysts receive
   only blinded manifests and raw files; operator key/seed must be stored elsewhere.
6. Implement/review an instrument-specific adapter returning the documented arrays
   and metadata; `acquire_physical` deliberately raises NotImplementedError today.
7. Collect fixed-count evaluation, then an independent-day/operator repeat with
   the same frozen rule. Physical summary issuance remains gated on independent
   hardware/control review; mock summary code is not apparatus certification.

Example prospective manifest (one of five blocks; omit seed for a private 128-bit seed):

```bash
python scripts/gv_phy_001.py manifest --stage evaluation --block 0 \
  --public-out artifacts/physical/public/block0.json \
  --private-out artifacts/physical/operator-only/block0-key.json
```

For real blinding, use a genuinely separate operator-controlled directory/account,
not the example directory visible to the same user. Keys are chmod 0600, not
encrypted. Waveforms can reveal conditions; label blinding is not sensory blinding.

## Raw Data and Software Dry Run

The [machine-readable contract](../experiments/gv_phy_001_data_schema.json) defines
13 arrays plus sample indices in `samples.npz`, paired `metadata.json`, and file
hashes. Sample-index timing is authoritative; ISO UTC is an audit timestamp only.
Fields include ID/UUID run ID, origin, blinded label, event type WITHHELD, common
clock/rate/trigger index, channel units and calibration versions/gain/offset/range,
hardware configuration, environment, operator notes, flags and manifest SHA-256.
Stored arrays retain nominal engineering units; declared gain/offset corrections
are applied only to derived analysis. NPZ never contains pickled objects.

Write once into a new run directory. Hashes detect accidental changes, not a
malicious owner who rewrites data and hashes. Keep read-only/WORM backups, original
DAQ exports and access logs. Invalid samples are retained, quarantined and counted;
NaNs, clipping, missing channels or timing faults cannot become positive evidence.
Actual labels/configuration descriptions remain in restricted acquisition logs;
public hardware tokens must not directly expose active/sham assignment.

```bash
python scripts/gv_phy_001.py dry-run --seed 42 --out artifacts/physical/dry-run-001
python scripts/gv_phy_001.py validate artifacts/physical/dry-run-001/raw/RUN_UUID
python scripts/gv_phy_001.py score --manifest artifacts/physical/dry-run-001/manifest.json \
   --model artifacts/physical/dry-run-001/model.json --threshold artifacts/physical/dry-run-001/threshold.json \
   --lock artifacts/physical/dry-run-001/analysis_lock.json \
   --raw-root artifacts/physical/dry-run-001/raw --out artifacts/physical/dry-run-001/blinded-score.json
python scripts/gv_phy_001.py summarize --analysis artifacts/physical/dry-run-001/blinded-score.json \
   --operator-key artifacts/physical/dry-run-001/operator_key.json --out artifacts/physical/dry-run-001/unblinded-summary.json
python -m pytest -q tests/test_physical_program.py
```

Replace RUN_UUID with a run in the generated blinded manifest; deliberately invalid
software case will fail validation as expected. Reusing an output directory fails
rather than overwriting files. The dry run has **300 model + 300 threshold mock
events and 12 test cases**, not physical scheduled acquisition or formal power.
It tests timing shift, electrical/EM/vibration/acoustic/thermal/environment signals,
overlap, software index corruption, sham, clean null, and an injected unknown.
The unknown tests plumbing, not a real mechanism.
`score` loads no operator key; `summarize` is a separate post-scoring step and
refuses physical conclusions. Comparison peak/RMS flags use separately frozen
sham-calibrated thresholds, never active outcomes.

**SYNTHETIC PIPELINE TEST - NOT GV EVIDENCE.**

## Readiness and Honest Nulls

Readiness is **adversarial pre-hardware review**, not hardware-ready. Component
choices, calibration floors, waveform transfer functions, mechanical matching,
geometry-dependent model adequacy, complete physical evaluation integration and
independent replication remain unresolved. No purchase or release is authorized.

An adequately calibrated null can constrain the frequency of signatures detectable
by this fixed sensor/window/rule, with stated uncertainty and amplitude/bandwidth
limits. It cannot exclude arbitrarily weak, rare, delayed or unmeasured effects,
all GV formulations, new physics, or theological interpretations. A failed assay
is INCONCLUSIVE rather than a scientifically meaningful null.

## Software Verification

2026-10-05, Python 3.11.16/Linux, existing 22-package research lock:

| Check | Measured outcome |
| --- | --- |
| Full `make test` suite | 123 passed |
| Physical-program tests | 33 passed, included in full total |
| Research integrity | 87 passed, included in full total |
| Internal links | 47 passed; 40 integrity tests deselected |
| Schema/metadata/timing/latency/raw subset | 23 passed; 10 physical tests deselected |
| Synthetic acquisition/classifier | 12/12 expected pipeline outcomes, including one injected unknown; 300 model + 300 threshold mock events |
| Saved raw schema/hash validation | 11 valid-format runs; 1 deliberately corrupted software-index run retained and rejected. Timing-shift run is additionally invalid for event timing, not file format. |
| Separate blind scoring and unblinding CLI | Both completed; score loads no operator key; summary physical_evidence=False |
| Seeded prospective manifest CLI | One 140-attempt block generated; five blocks total 700 (150 active, 150 sham, 50 each diagnostic arm) |
| Dependencies | `pip check` clean; all 22 exact pins match, no new dependency |
| Secret-pattern scan | 125 tracked/proposed files, 6 pattern families, zero hits; not exhaustive secret assurance |
| Whitespace / editor diagnostics | `git diff --check` clean; no diagnostics in new/changed Python files |

No generated raw data, manifests, operator keys, virtualenvs or ecosystem files
are included in the commit. All five existing fluid benchmark implementations and
negative classifications remain unchanged. These measured outcomes are **software
checks only**, not experiment results, apparatus acceptance or independent replication.

## Adversarial Pre-Hardware Review

2026-10-06 review of PR #4 at `9560c2bb85f521d3c6b3ae71acab5101b713e2f0`.
**PENDING remains mandatory.** The design can proceed to hardware **design review**,
not construction approval or experiment execution. No physical measurements were used.
The preceding software totals describe the original commit, not the corrected head.

### Confirmed Software Defects

- The original mock used overlapping calibration seed ranges: **35 identical
  waveforms** occurred in both model and threshold calibration despite different
  UUIDs. New stage/block/run-namespaced streams and content fingerprints reject
  reused arrays. Identical hashes can flag duplicate captures, not prove deliberate
  copying or physical independence; altered copies can still evade a hash check.
- Nonfinite/invalid model and threshold values were accepted, allowing invalid
  arithmetic or an infinite threshold to resemble a null. Values/shapes/scales,
  versions, split IDs, content fingerprints and payload seals are now checked.
  Scoring requires an independently retained pre-evaluation lock of file/source/
  schema hashes. This protects against accidental drift, not an owner rewriting
  every lock. External custodian deposit is required for meaningful immutability.
- Raw peak/RMS comparators previously inherited the residual detector's chosen
  channel-pair coincidence. Each now selects its own pair: the residual method
  is not privileged. No baseline superiority is established by a toy suite.
- Keys were chmodded only after writing; they are now created exclusively with
  mode 0600. This does not isolate an analyst sharing the same account.
- An arithmetic mock screen was named a complete frozen endpoint. The summary
  now separates `screening_endpoint_met` from `frozen_endpoint_met=False`,
  `physical_assay_certified=False` and `null_result_valid=False`. Physical-tagged
  records cannot count as assay-valid merely by passing a format/timing screen.
- Complete-case rates could hide selective acquisition failure. Invalid attempts
  are separately counted, retained and included in worst-case uncertainty bounds.
  Missing/duplicate manifest events and string validity flags are rejected.

No 0..50 ms window, signed second-largest statistic, threshold formula, 1 ms
coincidence or 0.10 excess was tuned to make synthetic results favorable. Original
mock independence was overstated; the corrected mock is still not physical validation.

### Ordinary Relay Pathways

| Pathway | How it can mislead / required qualification |
| --- | --- |
| Contact bounce/arcing and coil flyback | Multiple ordinary electrical/optical edges, magnetic pulses and mechanical impacts. Measure entire voltage/current/optical traces and bounce distribution; a linear peak model does not model bounce physics. |
| Current loops, driver and return geometry | Coil/core remanence, loop area, twisting, return current and probe grounds can dominate receiver field. Freeze routing/axis/position and compare measured source/receiver transfer functions, not current alone. |
| Chassis/armature/fixture motion | Sound and structure share one source and can look coherent across modalities. Source references do not observe every floor/cable/air path. Separate calibrated acoustic and structural interventions are essential. |
| LED/contact load and photodiode electronics | Battery isolation is not zero capacitive/EM coupling; LED leads, optical pickup, TIA and DAQ grounds can couple. Qualify coil-driver dummy and LED-only switching separately; do not attribute all optical-correlated effects to a novel process. |
| Stable A / reset | Bounce, supply droop, heating and hysteresis can prevent a stable plateau. Verify S0 and A in their stated windows with independent contact/optical checks; failure means invalid transition, not a null. |
| Five-second spacing | Thermal/mechanical settling and mains/HVAC/operator correlations may persist much longer. Five seconds is a minimum, not decorrelation proof. Pilot determines a prospectively fixed gap and stability criteria before evaluation. |

### Control Challenge

| Control | Confound / required interpretation |
| --- | --- |
| 0 idle | Marker itself can couple; idle background need not match energized electronics. Qualify fixed acquisition settings and terminated/dummy receiver inputs. |
| 1 disconnected | Removes inductance/current and changes driver ringing/ground return. Tests command feedthrough, not every energized-source artifact. |
| 2 electrical-only | A resistor cannot match coil inductance, flyback, magnetic geometry and contact LED path simultaneously. Characterize separate load-path challenges; freeze the chosen comparator before evaluation and do not call it an exact counterfactual. |
| 3 mechanical-only | An enclosed commercial relay may have no accessible armature. Opening it or using another actuator changes chassis, force, timing, EM and sound. A safe mechanically accessible fixture/matched motion is **not specified today**; no exclusion claim until independently validated. |
| 4 shielding/distance | Shields change capacitance/grounding, acoustics and magnetic material response; moving receivers changes cable pickup and floor/air paths. Calibrate each subcondition independently, separate the two interventions, retain cable/axis/fixture records. |
| 5 mechanical isolation | Changes resonance, acoustic radiation and cable tension. Keep measured transfer functions and do not interpret a smaller signal as removal of one cause without sensitivity checks. |
| 6 acoustic isolation | Barrier alters reflections/pressure and may touch structures or act as an EM shield. Verify noncontact placement and acceleration/field response as well as acoustic attenuation. |
| 7 thermal shift | Changes coil resistance/current, mechanical compliance, sensors and timebase. Log both electrical and temperature behavior; a 500 ms record cannot characterize all slow drift. |
| 8 sham | Operators hear/see true transitions; inhibition can change electronics and current. Hide labels from automated analysis, not claim identical waveforms or double blinding. |
| 9 blinding | Public timing/order, raw current/optics, block balance and metadata can reveal arms. No manual window/threshold choice after labels or waveform cues; custodian separates keys and freezes outputs. |

### Sensor and Timing Scope

The [13-channel map](PHYSICAL_EXPERIMENT_HARDWARE.md#channels) is a provisional
millisecond/low-frequency design, not an experimentally justified universal band.
Analog Hall sensors must demonstrate 2 kHz transfer response; common slow digital
magnetometers may fail. Accelerometer mount resonances and microphone preamp/AGC/
filter delays require phase/impulse characterization, not a nominal bandwidth label.
Source witness channels and the environmental Hall probe cannot exclude RF/electric
pickup, hidden ground paths or every combined cause. Temperature intentionally stays
slow and never participates in coincidence. Trigger/optical/current/voltage channels
must preserve measured edge/plateau information without ADC or filter artifacts.

The **100 us target is unproven**. Budget uses 50 us relative sampling quantization,
20 us scan/aperture skew, 20 us pairwise front-end uncertainty (10 us each), and
10 us clock/reference contribution. Certify these conservatively with simultaneous
DAQ or measured multiplex offsets, an independent faster timebase and sensor-specific
injections. Anti-alias/digital filters, amplitude/temperature-dependent group delay,
clock drift and command propagation cannot be waved away by a scalar offset.
USB/OS timing must not determine sample coordinates. Never calibrate out real sound,
structure or relay travel time. If group-delay uncertainty cannot meet the budget
over the specified waveform family, v1 is INVALID / INCONCLUSIVE and needs a new
prospective design version, not retroactive alignment of peaks.

### Endpoint, Counts and Statistics

The [amended preregistration](../experiments/GV_PHY_001_PREREGISTRATION.md#pre-data-rationale-and-limits)
states which constants are operational choices, not predictions or synthetic-derived
optima. Second-largest requires two excesses but does not ensure independence;
signed residuals ignore suppression; 1 ms can miss ordinary or genuine delayed
cross-modal propagation. Floor 8 is not an 8-sigma significance claim. K may absorb
real state-linked changes in calibration, or miss ordinary nonlinear interactions.
Model residual MAD is in-sample; raw peak/RMS comparators remain required.

40/300/300/700/700 are **planning counts**. A separately archived non-evidential
physical noise/reset pilot and statistician approval must precede final count/assay
lock. No claimed power from unknown noise or five nominal blocks. With independent
1% true sham FPR, the 5% upper-bound gate passes only about 66.23% at n=120 and
80.95% at n=150; empirical excess >=0.10 frequently fails at a true 0.10 boundary.
Repeating the same cutoff can further reduce detection. Sensor/time autocorrelation,
operator/session clustering, drift and carryover invalidate naive binomial precision.
Bonferroni component bounds and Holm secondary contrasts do not repair dependence.
No post-hoc choice of cluster/mixed-effects/permutation method may rescue evaluation.

Invalid events can be related to strong signals (clipping, bounce, failed reset).
Thirty invalid active events among 150 attempts cannot be discarded to advertise
a 3.03% null bound from the remaining 120. Both complete-case and missing-event
worst-case bounds are reported; neither certifies independent trials or good sensors.
No physical null can be issued by this prototype. Warning lead times remain undefined.

### Meaningful Null Qualification Checklist

Before NOT SUPPORTIVE can represent a physical null rather than an invalid assay,
independent reviewers must approve and archive all of:

1. Selected components, actual schematic/channel map, grounding/isolation, safe
   fixture and driver, DAQ interface and device-native acquisition logs.
2. Measured timing budget, no dropped/clipped samples, filter/transfer functions,
   sensor placement and corrected front-end latency (not physical propagation).
3. Sensitivity floors **in physical units**, stated bandwidth/axes/waveform families,
   positive/negative end-to-end injections and uncertainty. Demonstrate power of
   the actual G/coincidence rule at specified amplitudes, not sensor response alone
   or synthetic code injection; report failure fractions and confidence assumptions.
4. Validated controls, including dummy input/instrument coupling and RF/electric
   characterization before unexplained attribution. Mechanical-only feasibility
   and fair shielding/isolation contrasts cannot remain assumed.
5. Stable S0/A/reset/thermal behavior, prospectively fixed gaps and attempted counts,
   all invalid/missing attempts retained, no selective stopping or replacements.
6. Final dated protocol/version, pre-evaluation external model/threshold/source/
   schema lock, label custodian, pilot exclusion and no content/UUID split leakage.
7. Pre-data approval of block dependence/missingness handling, uncertainty and
   replication requirements. Independent day/operator is not independent apparatus;
   same-device systematic errors survive both sessions.

Failure of any item means **INVALID / INCONCLUSIVE**, not a valid negative finding.
An engineering checklist/prototype hash alone cannot certify these facts. Calibration
certificates, hardware configuration hashes, signed operator/witness logs, timestamped
manifest deposit and read-only native exports give traceability, not certainty against
fabrication. No new provenance authority or purchased apparatus is implied.

The subsequent [hardware design-review package](GV_PHY_001_CONSTRUCTION_READINESS.md)
adds channel/component/fixture/ground/timing/calibration/sensitivity plans,
an [instrumentation pilot](../experiments/GV_PHY_001_INSTRUMENTATION_PILOT.md),
a [null validity checklist](../experiments/GV_PHY_001_NULL_VALIDITY_CHECKLIST.md)
and a guarded non-operational acquisition interface. These review artifacts do not
complete the physical qualification items above. **GV-PHY-001 remains PENDING.**

### False Positives and False Negatives

Ordinary common-mode pickup without reference-channel activity passes the same toy
residual test as the unknown injection; a regression test deliberately demonstrates
this. RF rectification, ground returns, acquisition-channel crosstalk, cable motion,
shield leaks, driver noise, aliasing/filtering, clipping, bounce and correlated room
disturbances may survive single-cause controls. The toy fits 0.6 times the same
Gaussian source pulse and injects a 50-noise-scale reference-free unknown; these
are deliberately easy, generator-matched cases. Their success does not validate
K, causal exclusion, hardware sensitivity, FPR, blinding or physical inference.
Dry-run arm labels organize pipeline plumbing, not a randomized physical treatment
contrast; its per-arm intervals/rates must not be read as experiment estimates.

The assay may miss <sample-interval or >50 ms effects, RF/electric-only or out-of-band
signals, weak/rare/single-channel/suppressive effects, noncoincident peak changes,
delayed propagation, phase-only or nonlinear/state-dependent interactions, and
changes already learned by K. A negative result concerns only this qualified,
detectable excess-feature formulation in this apparatus regime, never every GV.

### Readiness and Cost

Costs remain **unresearched planning envelopes** ($0; $200-800 borrowed-tool
instrumentation; $1,500-6,000+ synchronized test; $5,000-15,000+ independent build).
No quote, completeness or affordability guarantee is made. Apparatus timing, field
coverage and calibration access can exceed those ranges. PENDING cannot advance
to HARDWARE READY / NOT RUN until the seven qualification items, selected/interface
specifications and safety review are actually documented. Review/merge of this
limited design PR does not authorize construction, purchase, execution or physical claims.

### Fresh Review Verification

2026-10-06, a new `/tmp/gv-phy-review-venv`, Python 3.11.16/Linux and the unchanged
22-package research lock. No prior environment contents are required.

| Check | Measured review outcome |
| --- | --- |
| Full suite | 147 passed, 0 failed |
| Physical-program tests | 57 passed, 0 failed; included above |
| Research integrity | 87 passed, 0 failed; included above |
| Internal-link subset | 47 passed; 40 integrity tests deselected |
| Dry-run acquisition/classification | 12/12 expected outcomes; still deliberately easy synthetic cases |
| Manifest creation / locked blinded score / separate unblinding | 3/3 CLI steps complete; no operator key loaded by scoring |
| Model/threshold sample-content intersection | 0 among 300 + 300 mock events, instead of the original 35 reused waveforms |
| Physical endpoint / valid null / assay certification | All blocked/false; GV-PHY-001 remains PENDING with no physical dataset |
| Dependencies | Fresh lock installation succeeds; pip check clean; 22/22 exact pins match |
| Secret scan | 125 tracked/proposed files, 6 pattern families, 0 matches; not exhaustive assurance |
| Whitespace / Python diagnostics | git diff --check clean; no diagnostics in the three touched Python files |

Adversarial regressions include invalid/finite-mutated/resealed-but-lock-mismatched
analysis parameters, overflow, content leakage under changed UUIDs, string flags,
missing/private-duplicate IDs, count/sham/control/subcondition bypass, private key
permissions, overt label leakage, independent comparator pairs, physical/non-null
promotion barriers and ordinary unmeasured common-mode pickup. No benchmark
outcome was improved, no hardware acquired, and no physical evidence is claimed.