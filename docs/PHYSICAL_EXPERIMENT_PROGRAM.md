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
  with optical/current plateau within +/-5% for the final 50 ms of the 300 ms capture.
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