# GV-PHY-001 Null Validity Checklist

**DESIGN / NOT RUN. All physical gates are currently UNVERIFIED.** A quiet trace,
software hash or mock replay cannot pass any measurement gate. Any failed/missing
mandatory gate means **INVALID / INCONCLUSIVE**, not NOT SUPPORTIVE.

| Mandatory gate | Required reviewable artifact / present state |
| --- | --- |
| Timing certified | Measured <=100 us conservative pairwise budget and validity domain, independent verifier/calibration; UNVERIFIED |
| Channel calibration current | All 13 core chains plus relevant diagnostics, actual sensor/axis/range/filter/latency and reference artifacts; UNVERIFIED |
| Sensitivity certified | Physical-unit envelope, held-out end-to-end G/coincidence detection and uncertainty, each declared pair/family; UNVERIFIED |
| Bandwidth/EM coverage | Actual response/alias protection, axes, RF/electric/dummy-input challenges and remaining blind bands; UNVERIFIED |
| Controls valid | Current/voltage/geometry-qualified electrical comparisons, mechanical feasibility, shielding/isolation/thermal/sham tests; UNVERIFIED |
| No saturation | Sensor/front-end/ADC overload checks and recovery, every sample/status retained; UNVERIFIED |
| No missing required channels | Complete indices/core arrays/marker/reference, ancillary qualification records; UNVERIFIED |
| Valid counts and missingness | Existing attempted/minimum-count and missing-worst-case requirements, no replacements or selective stopping; UNVERIFIED |
| Acquisition stable | Reviewed driver, native files, clock/grid/hash consistency, dropped-sample/firmware/filter checks; UNVERIFIED |
| Reset validated | Pilot-approved fixed gap, S0/A/body/ambient/ringing/baseline and carryover evidence; UNVERIFIED |
| Operator protocol followed | Precreated blinded manifest, role separation, signed deviation/safety/invalid-attempt logs; UNVERIFIED |
| Analysis lock verified | External pre-evaluation deposit of model/threshold/source/schema/config/calibration references; UNVERIFIED |
| Split separation | Distinct pilot/model/sham-calibration/evaluation/replication IDs and sample fingerprints with documented provenance; UNVERIFIED |
| Statistical assumptions reviewed | Pre-data block/operator/session/dependence/missingness method and uncertainty approval; UNVERIFIED |
| Replication rule followed | Adequate sensitivity in locked independent session and eventually independent apparatus; UNVERIFIED |
| Independent adjudication | Raw/control review checks ordinary causal paths, physical provenance and bounded scope; UNVERIFIED |

Only an independently reviewed qualified negative outcome can be NOT SUPPORTIVE
for the stated detectable-signature formulation. It never rejects every GV proposal,
all unknown signals, new physics or theological interpretations. The present code
blocks physical summary issuance: `physical_assay_certified`, `null_result_valid`
and `frozen_endpoint_met` remain false. There is no checkbox API that grants validity
from user-supplied true flags. Do not infer independent observations from UUIDs/hashes.

Keep failed/missing/saturated captures, native logs, calibration records and operator
notes, not merely complete cases. Certifications can expire after gain/cable/fixture/
firmware/filter changes; such changes require requalification and a new configuration
hash. See [sensitivity](../docs/GV_PHY_001_SENSITIVITY_PLAN.md),
[timing](../docs/GV_PHY_001_TIMING_PLAN.md) and
[falsification](../docs/FALSIFICATION.md).