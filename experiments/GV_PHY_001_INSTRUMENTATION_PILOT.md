# GV-PHY-001 Instrumentation Pilot

**STATUS: PILOT DESIGN / NOT RUN. NOT GV EVIDENCE.** No apparatus exists or is
authorized by this document. This separate qualification proposal does not alter
the existing confirmatory detector/window/count rule.

## Purpose and Admission

Measure real noise, timing/capture stability, transfer response, relay bounce,
reset behavior, clipping, control confounds and event/block dependence. Admit
only after actual components, wiring/driver/fixture, safety and acquisition reviews.
Do not collect confirmatory GV-PHY-001 data or claim an anomaly from this pilot.
Use distinct run IDs/stage namespace and archive pilot data separately from all
calibration/evaluation/replication sets. No pilot is executed by current software.

## Proposed Fixed Engineering Schedule

160 attempts, after the existing 40 debugging attempts, with a dated operator
schedule locked before pilot collection:

| Group | Attempts | Purpose |
| --- | ---: | --- |
| Electrical loopback/clock/reference | 40 | Capture/index/skew/marker checks and verifier comparison; not full timing certification |
| Local sensor/reference injections | 40 | Gain/response/noise/overload reconnaissance; a later complete calibration/sensitivity schedule is still required |
| Real relay transitions | 20 | Bounce/S0/A and reset-study families below |
| Marker/sham records | 20 | Background, controller pickup and stability |
| Eight diagnostic controls | 40 (5 each) | Feasibility/confounds, including shielding vs distance logged separately |

These counts are instrumentation planning, not formal power or enough repetitions
to certify independence. A control that cannot physically be implemented is a
documented gap, not a missing cell silently filled by a mock. No substitutions
based on interesting traces. Stop only for preset safety/acquisition failures;
report attempted/aborted/missing/invalid events, no outcome-driven replacements.

## Reset Study

The 20 real transitions comprise five attempts at each **planned gap** 5, 10, 20,
40 s, ordered by a predeclared balanced schedule after safety review. Coil on-hold
remains 0.300 s, then off. Log receiver/source baselines and body/ambient temperature
continuously for at least 60 s after each test and up to a predeclared 10-minute
observation if recovery is not reached. Device-native ancillary/temperature logging
may extend beyond the core 0.5 s record; it does not extend the primary event window.

Measure thermal return/slope, vibration ringing, magnetic relaxation, acoustic
background, sensor baseline recovery and DAQ drift. Before pilot choose recovery
criteria from instrument/reference uncertainty and safe component limits, not an
H1 outcome: for example return within combined baseline/calibration uncertainty
with no sustained slope beyond that uncertainty. Numerical criteria cannot be
honestly supplied before selected sensor/uncertainty data; therefore this pilot
is not execution-ready. If a gap does not recover, stop the unsafe/invalid schedule
and report it; don't choose per-event waits to make residuals disappear.

After the complete pilot, propose one fixed conservative gap, warm-up/rest schedule
and block design in a new dated protocol version before confirmatory data. Five
attempts per gap do not prove event independence or bound rare thermal carryover.
Statistical dependence requires longer/new qualification, not optimistic binomial
counts or selective exclusion of warm events.

## Outputs and Review

Retain original DAQ exports, core and ancillary waveforms, manifest/key, apparatus
configuration hash, calibration references, clocks/verifier logs, bounce measures,
noise PSD/MAD, saturation/recovery, environment and operator notes. Publish all
qualified and failed controls. No p-value, residual flag or model fit becomes GV
support. Pilot can inform future **prospective** component/gap/count/statistical
revisions, never rewrite previous failures or change the endpoint after evaluation.
Independent reviewers decide timing/calibration/sensitivity and construction gaps.
See [program](../docs/PHYSICAL_EXPERIMENT_PROGRAM.md),
[timing](../docs/GV_PHY_001_TIMING_PLAN.md), and
[readiness](../docs/GV_PHY_001_CONSTRUCTION_READINESS.md).