# The God Variable

The God Variable is an open research program investigating whether certain state transitions contain reproducible signatures that remain unexplained after known causal pathways and simpler models are excluded.

## Status

**THE GOD VARIABLE HAS NOT BEEN CONFIRMED.**

Several tested formulations have produced negative results. Some experimental
programs remain open. No tracked physical experiment establishes a GV candidate.

This is an independent open research project. GV is hypothetical. Computational
anomalies are not proof of new physics; unexplained residuals require additional
controls, and extraordinary interpretations require independent replication.

> A residual is only a residual until known explanations are excluded.

**UNEXPLAINED ≠ GV; GV ≠ NEW PHYSICS; NEW PHYSICS ≠ GOD.**

## Two Research Programs

**GV Switch:** can a state transition contain a reproducible signature that
survives known timing, electromagnetic, mechanical, acoustic, thermal, software,
statistical, and environmental explanations? The strongest switch verdict is an
**unexplained propagation candidate**, not GV confirmation.

**Local Tuning / A:** can we identify a reproducible transition signature between
a pre-state and an aligned state A that ordinary dynamics or control behavior
cannot explain? Preserve **GV -> transition / tuning process -> A** as a
hypothesis: A is the resulting state, not GV. A conductor analogy is explanatory
only, never evidence.

The computational benchmark/falsification track tests predictive formulations,
not theology. [Roadmap](docs/EXPERIMENT_ROADMAP.md).

## What Would Count as Evidence?

A candidate must meet prospectively fixed, measurable criteria: temporal
localization, cross-sensor coherence, reproducibility, intervention dependence,
survival of known-cause controls, held-out discrimination, and performance against
simpler baselines. A residual alone is insufficient. Thresholds must be frozen
before confirmatory data, not chosen after seeing an anomaly.

See the [canonical definition](docs/THEORY.md), [current GV status](docs/GV_STATUS.md),
[claims ladder](docs/CLAIMS.md), and [competing explanations](docs/ALTERNATIVE_EXPLANATIONS.md).

## What Has Failed?

| Benchmark / method | Outcome |
| --- | --- |
| F0: ODE blow-up | **NOT SUPPORTIVE**: second derivative ties or beats GV. |
| F1: inviscid Burgers | **NOT SUPPORTIVE**: all warning medians tie; initial-distribution confound disclosed. |
| F1b: forced viscous Burgers | **NOT SUPPORTIVE**: total variation/gradient energy beat GV in the valid corrective test. |
| F2: Navier-Stokes | **INVALID / INCONCLUSIVE**: insufficient active event incidence; not a valid detector-performance test. |
| F2b: corrective Navier-Stokes | **NOT SUPPORTIVE**: new unchanged-code run passes implemented validity gates, but simpler vorticity/strain baselines are stronger. |
| Early switch classifiers | **NOT SUPPORTIVE** under adversarial controls: clock/cable artifacts and a zero-power correction exposed failures. |

[What was tested, what would support it, and what happened](docs/NEGATIVE_RESULTS.md).
Original results, confounds, and preregistrations remain accessible; thresholds and
weights are not retroactively changed.

## Current Experiments

Switch clock/EM/environment gate successes are **synthetic methodology only**.
Their modeled injected candidate is not an observed physical signal. The existing
three CI edge-case tests are engineering software checks, not physical GV evidence.

Phase 0 and E1 have specifications, acceptance logic and trial-manifest software;
no tracked completed physical validation or waveform dataset is established.
E1 is an ordinary electrical transient sensor, not a GV detector.

**GV-PHY-001** proposes a separate low-voltage relay/LED transition with synchronized
electrical, magnetic, vibration, acoustic, optical, thermal and reference channels.
It is **PENDING — DESIGN / NOT RUN**, not hardware-ready. Its
[program](docs/PHYSICAL_EXPERIMENT_PROGRAM.md) and
[prospective preregistration](experiments/GV_PHY_001_PREREGISTRATION.md) define
known-cause controls, a held-out endpoint, meaningful bounded nulls and independent
replication. Mock files are **SYNTHETIC PIPELINE TEST — NOT GV EVIDENCE**.
Its endpoint/counts are provisional pending physical noise/reset characterization,
timing/sensitivity certification and statistical approval. Software rejects analysis
mutation/leakage but cannot certify a physical null or complete the physical endpoint.
A [hardware design-review package](docs/GV_PHY_001_CONSTRUCTION_READINESS.md) now
specifies component/channel/fixture/power plans, timing and sensitivity procedures,
and a non-operational acquisition contract. **Actual components, schematics, driver
and qualification remain incomplete; GV-PHY-001 remains PENDING.**

`EM-001`, `EM-002`, and `TUNING-HW-001` are **PENDING provenance**: original
records were not located in this repository. No completion or apparatus readiness
is invented for them. Owner verification is needed. Hardware purchases are not
required for this launch. [Audit](docs/AUDIT.md).

## Reproduce the Work

### Computational Reproduction

Supported/tested baseline: **Python 3.11** on Linux (verified with 3.11.16).
Other Python/platform versions are not certified. No API keys or hardware are
needed. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-research-lock.txt
python -m pip check
make test
make reproduce-smoke
make reproduce-benchmarks
```

The [locked environment](requirements-research-lock.txt) records the verified
direct and transitive versions. [requirements-dev.txt](requirements-dev.txt)
offers bounded dependencies for development; changed versions require rerunning
checks. If `make` is unavailable, use `python -m pytest -q` and
`python scripts/reproduce_research.py --smoke` / `--benchmarks` directly.

Tests cover the existing software behavior plus evidence/document integrity.
The smoke runner checks six master switch scenario verdicts and generates seeded
CI CSVs and two plots. The full benchmark runner executes frozen F0, F1, F1b, F2
and F2b with original population sizes/seeds; it takes longer than the smoke run.
Expected benchmark outcomes: **NOT SUPPORTIVE, NOT SUPPORTIVE, NOT SUPPORTIVE,
BENCHMARK INVALID, success criterion not met (NOT SUPPORTIVE)**.

Outputs go to ignored `artifacts/research/`: per-command stdout/stderr, generated
audits/CSV/PNG files, and machine-readable run manifests recording code hashes,
interpreter, dependency versions, return codes and verdict checks. Historical
reports, longitudinal data and archived switch audit are not overwritten.
Negative scientific outcomes are successful reproductions, not execution errors.

`make reproduce-legacy` runs the historical cosmology/entropy toy separately.
Its assumed damping and target fitting do not validate its old physics claims.
The current toy fails to reproduce the claimed cosmological agreement (relative
error 1.00) and prints a negative entropy proxy; see [failures](docs/NEGATIVE_RESULTS.md).
Unseeded historical tether prototypes and superseded switch methods are not
advertised as exact reproductions. External-service LLM scripts are not part of
offline research reproduction.

### Physical Replication

Physical replication requires independent apparatus, calibration, validated
controls, raw waveforms, frozen analysis and independent data. Software demos or
generated trial manifests cannot substitute for measurements. No completed
physical replication is claimed, and it is not a prerequisite for publishing the
computational record.

The [physical-program dry run](docs/PHYSICAL_EXPERIMENT_PROGRAM.md#raw-data-and-software-dry-run)
needs no hardware: `python scripts/gv_phy_001.py dry-run --seed 42 --out artifacts/physical/dry-run-001`.
It exercises 12 injected/null pipeline cases, not a completed physical experiment.

## Theory

Start with [docs/THEORY.md](docs/THEORY.md). It defines $S(t)$, $X(t)$, $K(t)$,
$R(t)=X(t)-K(t)$, $t^*$, candidate $G(t)$, and the distinct states $S_0$, $T$, A.

[THEORY.md](THEORY.md), [PAPER.md](PAPER.md), and
[entropy_damping.md](entropy_damping.md) retain historical, unverified proposals.
Their unification, entropy cancellation, eternal replication and energy claims
are not current findings. Toy plots and philosophical analogies are not evidence.
Operational product repositories are outside this research launch; local
`ecosystem/` clones are ignored and neither modified nor required.

## Evidence Ledger

[Readable evidence inventory](docs/EVIDENCE.md) and
[machine-readable ledger](evidence/evidence_ledger.json): 20 scoped entries,
including all current experiment entry points, negative reports and missing-record
placeholders. SUPPORTIVE methodology entries do not mean physical GV is supportive.

## Falsification

[Rejecting a formulation](docs/FALSIFICATION.md): losing to simpler baselines,
known-pathway attribution, failed controls/replication, leakage, confounding,
out-of-sample collapse, or post-hoc-only success reject the relevant claim.
Revised formulations cannot erase failed ones or change their original criteria.

## Contributing

Replication, criticism, competing explanations, statistical review, alternative
baselines, and attempts to **disprove GV** are welcome.
[Contribution standards](CONTRIBUTING.md).

## Citation

Use [CITATION.cff](CITATION.cff), or cite Will Shacklett, *The God Variable*,
https://github.com/willshacklett/god-variable-theory, with the exact commit and
access date. No DOI, affiliation, peer review or publication acceptance is claimed.

[Proposed v0.1.0 release notes](docs/RELEASE_NOTES_v0.1.0.md): Public Research
Baseline. No release or tag has been created by this preparation.

License: [MIT](LICENSE).