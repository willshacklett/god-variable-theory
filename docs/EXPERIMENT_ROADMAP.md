# Experiment Roadmap

Roadmap statuses describe progress, not evidential support: **DONE**, **FAILED**,
**INCONCLUSIVE**, **READY**, **FUTURE**. The controlled scientific statuses live
in the [ledger](EVIDENCE.md). READY means a documented computational/protocol step,
not certified assembled equipment. Hardware purchase is not a launch prerequisite.

## PROGRAM A - GV SWITCH

| Work | Progress | Evidence / next boundary |
| --- | --- | --- |
| Toy timing and Monte Carlo | DONE | Easy-model development checks; not a physical experiment. |
| Five early identification approaches | FAILED | [Failure notes](../experiments/GV_SWITCH_FAILURE_NOTES.md); artifacts or zero power defeat inference. |
| Corrected clock, EM, environmental gates and master scenario audit | DONE | Synthetic methodology only; [archived audit](../experiments/gv_switch_protocol_audit.json). |
| Phase 0 acceptance framework | READY | Seven known-channel checks defined; no tracked completed physical validation. |
| E1 passive EM sensor specifications/manifests/calibration software | READY | Locked [576-trial design](../experiments/GV_SWITCH_E1_PREREGISTRATION.md); no physical acquisition established. |
| GV-PHY-001 prospective relay design and mock pipeline | READY | [Program](PHYSICAL_EXPERIMENT_PROGRAM.md), [preregistration](../experiments/GV_PHY_001_PREREGISTRATION.md); documentation/software review only. Scientific status PENDING, DESIGN / NOT RUN. |
| GV-PHY-001 hardware/calibration/locked sessions | FUTURE | No selected apparatus or driver. Demonstrate sensitivity, timing, controls and independent repeat before any physical candidate interpretation. |
| GV-PHY-001 hardware design-review package | READY | [Requirements and explicit gaps](GV_PHY_001_CONSTRUCTION_READINESS.md); design artifacts and non-operational interface only. Status remains PENDING, not construction or execution readiness. |
| EM-001 and EM-002 original records | FUTURE | Owner must supply protocols/results and actual status; pending provenance, not invented aliases or completed experiments. |
| Independently calibrated physical switch test | FUTURE | Optional external collaboration; satisfy apparatus controls before any candidate search. |
| Independent apparatus/laboratory replication | FUTURE | Needed before causal interpretation, even if a residual eventually survives. |

## PROGRAM B - LOCAL TUNING / A

| Work | Progress | Evidence / next boundary |
| --- | --- | --- |
| Historical tether/feedback illustrations | INCONCLUSIVE | Encoded strain damping and aligned labels do not identify GV. |
| Operational A definition | READY | [Target error/stabilization definition](THEORY.md); measurable proposed endpoint, not a completed physical result. |
| TUNING-HW-001 original record | FUTURE | No located original protocol or dataset. PENDING provenance; cannot certify hardware-ready or completed. |
| Prospective transition-signature comparison | FUTURE | Freeze $S_0$, $T$, A, ordinary controller baseline, sham, $K$, $G$ and held-out evaluation. |

Separate reaching A from identifying a distinctive signature during T. Reduced
error from ordinary feedback is a useful controller result, not evidence for GV.
Do not invent physical phase/synchronization measurements that the existing work
does not provide.

## PROGRAM C - BENCHMARK / FALSIFICATION

| Work | Progress | Scientific record |
| --- | --- | --- |
| F0 ODE blow-up | FAILED | NOT SUPPORTIVE; second derivative ties or wins. |
| F1 inviscid Burgers | FAILED | NOT SUPPORTIVE; initial distribution confound disclosed. |
| F1b forced viscous Burgers | FAILED | Valid corrective benchmark; total variation/gradient energy stronger. |
| F2 forced 2-D Navier-Stokes | INCONCLUSIVE | Invalid active event incidence; preserve that verdict. |
| F2b corrective Navier-Stokes | FAILED | New unchanged-code run NOT SUPPORTIVE; simpler vorticity/strain stronger. |
| Three existing CI edge-case assertions | DONE | Engineering software checks only. |
| Historical cosmology/entropy toy | INCONCLUSIVE | No independently validated derivation or physical mechanism. |
| Solver convergence, held-out FPR and statistical review | FUTURE | Audit current limitations before proposing any new formulation. |
| F3 3-D candidate-data benchmark | FUTURE | Mentioned in historical roadmap; no completed experiment/data here. |

Launch deliverables are transparent documentation, an auditable ledger, executable
computational checks and invitation to criticism. Physical experiments can remain
open without blocking a public research baseline.