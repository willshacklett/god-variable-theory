# LHC transition study — Phases 1–2

**DESIGN / NOT RUN. GV has not been detected. No real LHC data are included.**

Question: do repeatable LHC operational transitions contain measurable residuals
after established accelerator physics and instrumental behavior are accounted for?
An unexplained residual indicates inadequacy of the tested explanations, not GV
or new physics. Do not assume CERN overlooked switching effects.

## Scope and repository boundary

This is an isolated foundation in the core `willshacklett/god-variable-theory`
repository, on `copilot/researchlhc-transition-study`, descended from verified base
`78d9f95918db36e9ac9779b28abb753020588cd5`. Historical theory, equations,
benchmarks and other experiments are unchanged. The canonical research definition
is `docs/THEORY.md`; its observable-space residual is X(t) minus K(t), with
measurement and model uncertainty. Historical equations are not validated here.

Study injection, acceleration ramps, adjustment/stable-beam entry, beam dumps,
and independently verified non-colliding transitions. Separate:

1. Initiating command/event, with independent provenance and timestamp.
2. Measured physical response, including latency and prior system history.
3. Residual after a frozen ordinary-physics/instrument model.

Beam-mode labels are not precise actuator timestamps; stable beams do not alone
establish collisions for a particular interaction point. No operations, hardware
interventions, deployment, paid access or unauthorized access are proposed.

## Method and current limitations

Follow `PROTOCOL.md`: characterize clocks and instruments, fit ordinary models on
training fills, freeze the analysis, then evaluate independent held-out fills and
replicate. Account for magnetic hysteresis, persistent currents, losses,
electromagnetic transients, thermal effects, detector timing and artifacts.
Controls include non-colliding states and matched pseudo-events.

`DATA_SOURCES.md` records direct access attempts and unverified CERN leads.
All attempted CERN hosts failed DNS resolution on 2026-10-10. There are **zero
verified available datasets** in `data_inventory.json`. This is not evidence that
CERN has no suitable data or that its services are down globally. No units,
sampling rates, timestamp precision or synchronized exports have been verified.
Confirmatory analysis is blocked until authorized, suitable data and timing
metadata are obtained and the preregistration is completed.

Phase 2 retried the three task-owner-supplied CERN URLs, again encountering DNS
failures. Their independently reported public-fill, NXCALS-authorization and
non-collision-cycle findings are recorded with attribution, not as locally
verified source contents. No candidate fill, transition timestamp, downloadable
measurement or synchronized source schema is verified. `DATA_SOURCES.md` contains
the prioritized measurement requirements and a precise **unsent** access-request
draft. No CERN ingestion adapter is warranted without an inspected real source.
The Phase 1 protocol and analysis scaffold remain unchanged.

## Minimal software contract

`analysis.py` reads a local CSV with exactly these columns:

`timestamp_ns,channel,unit,observed,predicted,provenance`

`timestamp_ns` is an integer Unix UTC nanosecond coordinate, not a claim of
nanosecond accuracy. Source time scale, clock uncertainty and conversion must be
documented before ingestion. Values and predictions must have the same unit;
predictions must come from an independently frozen model. Channel/unit pairs
must be consistent; duplicate or out-of-order timestamps per channel are rejected.
`provenance` must be `real` or `synthetic`; mixed origins are rejected.
The caller must explicitly select the expected origin. Labels cannot authenticate
data; source manifests and checksums are required for actual research.

The scaffold computes descriptive residuals only, without fitting models,
resampling, interpolating gaps, significance testing or evidence classification.
An explicit event window is aligned to the command; an optional independently
measured response timestamp is retained separately. No response time is inferred.
No command-line network access or automatic data download is provided.

## Focused tests (no installation needed)

From the existing terminal:

```sh
python -m unittest discover -s /home/runner/work/god-variable-theory/god-variable-theory/experiments/lhc_transition_study -p 'test_*.py' -v
```

If pytest is already installed, explicitly supply the directory because the
repository's default pytest discovery covers only `tests/`:

```sh
python -m pytest /home/runner/work/god-variable-theory/god-variable-theory/experiments/lhc_transition_study -q
```

All fixtures are **SYNTHETIC SOFTWARE TESTS — NOT SCIENTIFIC EVIDENCE**. No new
dependencies are required. These checks do not validate a physical model, CERN
data provenance, timing accuracy, statistical power or GV.

Phase 1 validation on 2026-10-10: Python 3.12.3 standard-library unittest ran
15 tests, all passed, with no failures or skips. `python -m pytest --version`
failed because pytest is not installed; no dependencies were installed.
The repository-wide pytest suite was not run. `git diff --check` passed.

Phase 2 validation on 2026-10-10: Python 3.12.3 standard-library unittest ran
17 tests, all passed, with no failures or skips. The two additional tests check
attribution and the absence of fabricated fill/measurement claims in the inventory.
Pytest remained unavailable (`No module named pytest`); the repository-wide suite
was not run and no dependencies were installed. `git diff --check` passed.
These results are software/inventory checks, not scientific observations.

Next action: from a CERN-reachable environment, inspect the NXCALS access-request
page and use its confirmed route to submit the draft request for a minimal
authorized pilot export. No request was sent by this session.
