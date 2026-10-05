# Contributing

Attempts to **DISPROVE GV are welcome**. A useful negative result, competing
explanation, or corrected claim is a contribution, not a threat to the project.

We welcome replication, criticism, alternative baselines, statistical review,
sensor/control design, falsification attempts, competing explanations, and
documentation corrections. This independent open research project claims no
academic affiliation or established physical GV mechanism.

## Research Standards

Read the [theory](docs/THEORY.md), [claims ladder](docs/CLAIMS.md),
[negative results](docs/NEGATIVE_RESULTS.md), and [falsification rules](docs/FALSIFICATION.md).
State the formulation, measurable prediction, strongest conventional alternative,
and result that would reject it. Preregister confirmatory changes before independent
test data; label exploration and post-hoc tuning. Disclose all endpoints, exclusions,
missing events, stopping rules, seeds, uncertainty, calibration and test splits.

Preserve original protocols/results. New formulations receive new IDs/versions;
they do not replace failed ones. Include negative/null/invalid outcomes in the
[ledger](evidence/evidence_ledger.json) with data provenance, baseline, success
criterion, limitations and an honest reproduction command. Do not assign support
to physical GV because a simulated injection or controller behaves as programmed.

For physical work retain raw waveforms, instrument configuration, calibrated
controls, manifest/data hashes and analysis commit. Do not submit sensitive data,
credentials, unsafe electrical designs, or unsubstantiated completion claims.
Equipment purchase is optional and not required to contribute.

## Software and Documentation

Use Python 3.11 and the [locked setup](README.md#reproduce-the-work).
Run `make test`, `make reproduce-smoke`, `python -m pip check`, and
`git diff --check`. Run the full affected frozen benchmark before changing its
reproduction/reporting code. Retain original numerical definitions and thresholds.
Document versions and output locations. Prefer small changes with focused tests.

Integrity checks intentionally fail if negative results are silently promoted or
expected experiments disappear. A justified historical correction must preserve
the original record and explicitly explain the change, not merely relax tests.

## Discussion and Review

Open an issue or pull request with the claim being challenged, source/file/commit,
reproduction steps, observed outcome, and proposed correction. No favorable result
is required. Missing EM-001, EM-002 and TUNING-HW-001 records require original
owner provenance before status changes. Review uncertainty and ordinary causes
before interpretation. A residual is only a residual until known explanations
are excluded.