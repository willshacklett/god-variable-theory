# GV-PHY-001 - Controlled Relay Transition Multi-Channel Test

**STATUS: DESIGN / NOT RUN**

Prospective v1 dated 2026-10-05. No physical data exist for this ID in the launch
evidence; code/mock outputs are not physical observations. Ledger status PENDING.
This is a repository preregistration proposal, not an externally registered study
or authorization to collect confirmatory data before adversarial hardware review.

Review amendment 2026-10-06: this is a **provisional pre-data design**, not a
final locked physical assay. No numerical detector/window/count was tuned to
mock outcomes. Engineering/pilot qualification and statistical approval must
produce a dated new protocol version before confirmatory collection. Pilot data
cannot be promoted into evaluation or used to erase the original planning rule.

> A residual is only a residual until known explanations are excluded.

**UNEXPLAINED ≠ GV; GV ≠ NEW PHYSICS; NEW PHYSICS ≠ GOD.**

## Hypotheses and Scope

H1: in the defined 5 V relay regime, a detectable time-localized joint residual
recurs on >=10 percentage points more active transitions than randomized shams,
survives known-pathway interventions and locked independent-session replication.

H0: ordinary transition dynamics, measured known pathways, artifacts and baseline
variation account for the observations; no added detectable repeatable signature
is established. Statistical H0 for the primary contrast is p(active)<=p(sham).
GV is not defined as a residual, and this test cannot causally identify GV.

The detectable domain is fixed bandwidth, amplitude floor, event window and
apparatus sensitivity, not an unrestricted metaphysical hypothesis. The activation
A(t) in older switch equations is unrelated to this measured post-state A.

## System, Channels, Windows

S0 -> externally commanded T -> measured closed-contact/LED plateau A as defined
in the [program](../docs/PHYSICAL_EXPERIMENT_PROGRAM.md#chosen-system-and-measurable-states).
A is not GV. Both contact voltage and optical state are observed; command time is
not assumed equal to physical closure time. No physical alignment has yet been measured.

DAQ 20 kHz/channel, common clock; t0 is recorded controller marker. Record
[-0.200,+0.300) s. Baseline [-0.180,-0.030) s. Primary event [0,+0.050) s;
late diagnostic [0.150,0.250) s for temperature. These are fixed before physical
evaluation. Inter-event spacing >=5 s is a planning minimum, not proof of reset.
A fixed longer gap, if needed, must be declared before evaluation. No selective
waiting based on the waveform. Coil hold is 0.300 s; A's plateau is [0.250,0.300) s.

Three searched channels only: receiver magnetic (uT), acceleration (m/s^2), acoustic
(Pa). Ten other required channels appear in the [data contract](gv_phy_001_data_schema.json).
Source EM/vibration/acoustic witnesses and environmental reference are distinct
from searched channels. Temperature/optical/electrical channels are diagnostic.
Sensor/range/latency calibration and <=100 us timing budget must be demonstrated,
not inferred from sample rate. No propagation-speed or particle-mass test is performed.

## Frozen Primary Statistic

For each channel baseline use median b and sigma=1.4826 MAD; no data-driven window
changes. Apply documented calibration gain/offset only to derived arrays. For
fast channels subtract the independently calibrated front-end `latency_s` from
sample coordinates before selecting windows and comparing peaks. Offsets are
relative to the recorded trigger (zero), bounded +/-10 ms and frozen before test
data. Never subtract physical travel delays or fit latency to an interesting trace.
No samples are interpolated or rewritten; temperature lag is diagnostic only.
Fast per-channel latency uncertainty must be <=10 us (<=20 us per pair). Electrical
front-end delay is calibrated independently; acoustic travel from source to sensor,
mechanical propagation and actual relay actuation delay are never calibration offsets.
For each searched channel, y is the maximum absolute baseline-centered value in the
primary window. Retain the time of that maximum. This is a feature residual, not
a reconstructed residual waveform or a new physical scalar.

Fit K using only the model-calibration set: intercept plus primary-window peaks
of current, voltage, source EM/vibration/acoustic, and environmental reference.
Standardize columns by calibration SD (intercept unchanged), use ridge 1e-6,
and normalize y-K by calibration residual MAD with a numerical 1e-6 floor. No
searched target feeds its own predictor. Frozen values depend on declared units;
the numerical floor is not a claimed sensor sensitivity. Validate model adequacy
in held-out controls, including geometry/isolation changes.

G is the second-largest of the three signed normalized residuals. Flag an event
only if G exceeds the locked threshold **and** the two corresponding observed
peak times differ by <=1 ms. A peak-coincidence rule is not independent physical
coherence: ordinary crosstalk can satisfy it. It must pass interventions.

Threshold=max(8, 99th percentile of G on the separate sham-calibration set, using
the higher empirical quantile). Strict greater-than comparison. Threshold is
frozen before evaluation. Target event-level calibration FPR is 1%, not a guaranteed
population FPR. This single joint statistic includes the fixed channel/time search;
no additional scanned thresholds, channels or lags enter the primary endpoint.

Primary endpoint: active minus sham flag rate >=0.10, a conservative 95% risk-
difference lower bound >0, and held-out sham 95% upper bound <=0.05, **plus** all
validity/control/replication requirements below. A small p-value alone is insufficient.
Simple comparison statistics are the second-largest baseline-sigma-normalized raw
peak and event RMS in the same three channels. Calibrate each with the same separate
sham set, higher 99th percentile and floor 8; apply their **own** top-two-channel
peak coincidence gates, not the residual detector's selected pair, and the same
hardware timing screen. RMS uses peak times in its independently selected channels.
They have matched target upper FPR, not necessarily equal realized FPR. Their mock
counts are reported; physical baseline/control validation remains incomplete.
No GV-candidate label can follow here.

### Pre-Data Rationale and Limits

| Choice | Prospective rationale, not a physical derivation |
| --- | --- |
| Second-largest of three | Requires two positive amplitude excesses rather than one noisy sensor; channels are not independent causal witnesses. Misses single-channel signatures. |
| Signed y-K | Tests excess peak magnitude only. Suppression/negative residuals and phase-only effects are outside H1. A symmetric rule would require another version. |
| 1 ms coincidence | Twenty samples, broad relative to a qualified 100 us budget; provisional operational localization, not a predicted GV timescale. Sound crosses 0.5 m in roughly 1.5 ms, so ordinary or genuine delayed cross-modal signals may fail it. |
| Floor 8 and 99th percentile | Conservative operational calibration rules. Residual-MAD units are not Gaussian sigma; neither "8 sigma" significance nor universal 1% FPR follows. The floor can make the assay insensitive. |
| 0.10 rate excess | Bounds H1 to a gross recurring signature considered practically interesting, not a theoretically predicted effect. At the boundary, sampling fluctuations can frequently fail the same empirical cutoff. |
| Baseline/event windows | Planned guard from the marker and 50 ms horizon for relay onset/bounce, not measured relay latency. Pilot must show S0 stability and useful closure/sensitivity in this domain or revise prospectively. |
| Ridge/floors/scales | Fixed numerical stabilizers, not selected optimum physics. Scales depend on units; in-sample residual variance can understate model uncertainty. |

Training K on ordinary active calibration runs can absorb a genuine effect that
tracks current/source witnesses. Conversely, changed geometry/filter/gain or nonlinear
interactions can make ordinary behavior a large residual. A fitted feature model
does not causally identify a channel. The 12 toy cases cannot justify these constants.

## Stages and Fixed Counts

Five randomized blocks per calibration/evaluation session; no outcome-based stopping.

| Stage | Attempted schedule | Minimum valid / purpose |
| --- | --- | --- |
| A engineering | 40 (4 each active/sham/eight diagnostic arms) | Debug/safety only; no evidence, no retrospective promotion. |
| B1 model calibration | 300: 60 active, 30 each of eight controls | >=240 valid, all control families represented; fit K and characterize ordinary responses only. |
| B2 threshold calibration | 300 new randomized shams | >=240 valid; lock joint threshold separately from fitting K. |
| C locked evaluation | 700: 150 active, 150 sham, 50 each of eight controls | >=120 active, >=120 sham, >=45 in each diagnostic arm. |
| D locked repeat | New independent-day/operator 700, same allocation | Same minimums and unchanged detector/threshold; no refit to rescue the first session. |

Each C/D block has 30 active, 30 sham, 10 per control. Control 4 divides into
shielding at fixed distance and distance at fixed shielding, 25 attempts each;
retain subcondition labels in operator logs and require >=20 valid of each.
Calibration/evaluation/replication UUID sets must be disjoint. Counts give an
approximately 1/240 calibration-tail resolution and allow limited technical loss;
120 valid active events give a useful bound on a gross recurring signal, not on
arbitrarily rare effects. Mechanical reset, coil thermal drift and session duration
motivate five blocks with rest/calibration checks. Budget at least 5 s per attempt
(~58 min per 700 before fixture changes/rest); practical sessions can take hours.

No formal power is asserted: actual noise, transfer functions, autocorrelation and
effect size are unknown. Run positive known-channel injections to establish the
reportable detection floor in each unit before a physical null is interpretable.
If those fail, do not use synthetic injection power as apparatus power.

After 40 debugging attempts, require a separately archived **non-evidential physical
noise/reset pilot** before B1/B2 or final count approval. Fix its schedule and sensor
injections before starting; do not stop when traces become attractive. Its purpose
is transfer functions, saturation, reset/thermal stability, false-positive variability,
block dependence and detectable-unit floors, not an H1 test. No pilot is run here.
The 300/300/700/700 numbers remain planning counts pending that review, not a power-
certified sample size. Any change requires a new prospective version and new test data.

## Statistics and Missing Data

Report per arm attempted, valid, invalid, hits, misses and event detection rate;
missing detections on valid events are non-detections, not exclusions. Missing/
invalid acquisition is separate and can make the study inconclusive. No warning
lead-time endpoint exists; undefined lead time remains null, never zero.

Report 95% exact Clopper-Pearson intervals for active/sham rates. For the primary
risk difference, subtract two 97.5% component intervals: [active lower - sham upper,
active upper - sham lower]. Bonferroni yields conservative >=95% joint coverage
under independent Bernoulli assumptions; it is not a falsely precise exact interval
for the difference. Block/session dependence must be assessed by an independent
statistician before confirmatory approval; clustered data may violate those assumptions.
Current software intervals are descriptive under those assumptions. Five blocks
and one day do not establish independence. A new block-aware analysis must be fully
specified before evaluation; no post-hoc choice of mixed-effects/cluster correction
may rescue a result. Within-block randomized active/sham assignment may support a
future restricted-randomization analysis if exchangeability/carryover assumptions
are justified; it is not implemented or approved by this proposal.

The eight diagnostic contrasts form a declared family; if inferential tests are
reported use Holm correction at family alpha=0.05. Secondary late-time, dose/distance,
configuration, optical-closure latency and simple-baseline comparisons are exploratory,
with endpoints/exclusions retained and no promotion from a post-hoc subgroup.
For control screening, more than 2 residual flags in any >=45-valid diagnostic arm
fails model/control adequacy; otherwise it does **not** establish <5% FPR in every
arm (intervals will be wide). Sham alone supplies the primary FPR bound.

A zero-hit result among 120 valid active events has a two-sided 95% upper bound
about 3.03% only for those valid events under independent Bernoulli assumptions.
Thirty invalid events out of 150 attempts could conceal a 20% rate before uncertainty.
Report missing-event worst cases: all invalid active events hits and invalid shams
misses for an upper contrast, and the reverse for a lower contrast. The code uses
97.5% component bounds on attempted counts and requires a positive worst-case lower
contrast for its arithmetic screen. These bounds still assume independence. A null
over all attempts is not licensed by complete-case counts or unverified missingness.
It cannot exclude weaker/below-bandwidth/rare signatures or all GV formulations.

Planning precision, not measured power: the 5% sham upper-bound gate allows only
1 hit among 120 or 2 among 150 valid shams. With independent true FPR=1%, the gate
passes about 66.23% or 80.95% respectively. Zero-hit upper bounds are 3.03%/2.43%.
Correlations or repeated sessions weaken inference further. Passing two locked
sessions compounds sensitivity loss; the cutoff >=0.10 has poor power at its own
boundary. A small sample of positive synthetic cases cannot resolve this issue.

## Controls and Attribution

Controls 0-9 are defined in the [program](../docs/PHYSICAL_EXPERIMENT_PROGRAM.md#architecture-and-controls).
They intentionally test timing/electrical/EM/mechanical/acoustic/thermal/software/
environmental paths and ordinary controller behavior. Reference-channel threshold
>8 baseline sigma is a provisional known-channel screen, not proof that every
residual is explained. An elevated residual with a known reference is retained
for model/control review, not discarded as an inconvenient event.

Isolation/shielding effects must be independently measured. Changes to sensor
gain/latency, cables, fixtures or noise floor can mimic removal of a signal.
Mixed causes remain possible. Missing RF/gravitational/other pathway coverage
precludes universal known-cause exclusion. No interesting trace counts as evidence.

## Blinding and Retention

Generate block manifests before collection. Public manifest has run UUID/sequence,
opaque label, stage, gap and event_type WITHHELD; no seed/arm. Operator key contains
labels and seed, stored separately with restricted access. Default seed has 128-bit
entropy; fixed demo seed is synthetic/testing only. Freeze per-run feature/flag
outputs and their hashes before revealing labels; a separate custodian unblinds.
Operators know fixtures; waveform/configuration cues may reveal conditions, so
this is imperfect analyst-label blinding, not a double-blind apparatus claim.
Sound, optical/current traces, UTC/order, fixture-change gaps, metadata and fixed
arm counts near a block's end can reveal labels. Scripts do not guarantee concealment.
Use predeclared common scheduling, generic metadata, automated frozen scoring and
an independent custodian; report any leakage. Restricted keys are created 0600 from
the outset, but the same user/account can still read them; genuine separation is external.

Never overwrite raw files. Keep original DAQ export, NPZ arrays, metadata,
hashes, manifest, calibration waveforms, full-scale/filter/firmware settings,
geometry/configuration logs, environmental conditions, operator notes, code commit,
model/threshold hashes and every invalid attempt. Use read-only backups/WORM where
available. A filesystem hash does not authenticate physical provenance.
The CLI requires a separately saved pre-evaluation lock of model/threshold files,
source and schema hashes; model/threshold payloads are also cross-bound and reject
nonfinite/invalid scales or changed values. An owner can rewrite all hashes/locks:
deposit them with an independent custodian/timestamp before opening evaluation data.
Keep device-native acquisition logs, configuration hashes, calibration records,
operator attestations and independent witness logs; these establish traceability,
not certainty against colluding fabrication. No authenticity service is claimed.

Allowed technical flags are missing/corrupt samples or required metadata, clipping,
lost/ambiguous marker, >100 us timing uncertainty, uncalibrated/changed front ends,
failed S0/reset or active transition, and acquisition/hash/manifest mismatch.
Freeze these flags before unblinding. Unexpected/noisy/negative signals alone are
not exclusions. No outcome-directed replacements; insufficient counts invalidate
that session and require a separately recorded prospective repeat/version.

## Decisions, Replication and Falsification

- **INVALID / INCONCLUSIVE:** invalid instruments/timing/sensitivity/controls,
  insufficient valid counts, incomplete physical analysis/known-pathway comparison,
  saturation, leakage, or unreviewed statistical dependence. No positive conclusion.
- **NOT SUPPORTIVE:** valid null/failed fixed endpoint, shams comparable, ordinary
  pathways/simpler models explain the signature, isolation removes it with validated
  sensitivity, or adequately sensitive locked independent-session repeat fails.
- **Unexplained propagation candidate:** only after complete control validation,
  both frozen sessions passing the endpoint, independent review of alternatives
  and raw data. This v1 software does not automatically issue that physical verdict.
  It does not establish GV, a new field, energy, God, or new physics.

The mock-only summary's `screening_endpoint_met` reports arithmetic/count gates,
not the complete scientific endpoint. `frozen_endpoint_met`, `null_result_valid`
and `physical_assay_certified` remain false. Physical-tagged single-run scoring
may pass a format/gross-timing screen but is not an admissible physical assay.
Physical summary issuance stays blocked until a separately reviewed driver,
timing/sensitivity/controls and block-aware inference are implemented. Missing
these requirements means INVALID / INCONCLUSIVE, never a valid negative result.

A GV-candidate claim additionally requires the [canonical criteria](../docs/THEORY.md)
and [claims ladder](../docs/CLAIMS.md), including stronger baseline discrimination
and independent apparatus replication. Tier 3 uses separately sourced/calibrated
DAQ/sensors/fixture, independent operator/site, unchanged primary detector and
documented transfer-function differences. If necessary predeclare recalibration
without using evaluation outcomes; it is a new validation, not a rescue.

New formulation/version requires prospective criteria, new/held-out data and
explicit comparison with the failed record. Never redefine this formulation to
escape its null. Independent raw-data and bibliographic/scientific review precedes
any extraordinary interpretation. No purchases or physical claims are authorized.

## Reproduction Status

[Software and raw-data commands](../docs/PHYSICAL_EXPERIMENT_PROGRAM.md#raw-data-and-software-dry-run)
exercise a **SYNTHETIC PIPELINE TEST - NOT GV EVIDENCE**. No hardware driver,
validated sensor transfer functions or completed physical control report exist.
Mock classifications test the encoded nulls, not comprehensive real-world causes.

**GV-PHY-001 HAS NOT BEEN RUN.**