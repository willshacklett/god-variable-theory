# Public Research Baseline Audit

Audit date: 2026-10-05. Baseline: `e5711b10fbce7f4949e62ee31db0c2216e19652a`
on origin's default branch, `main`. Origin:
https://github.com/willshacklett/god-variable-theory.git.
The launch branch is `launch/public-research-baseline`.

## Scope and Pre-Edit Findings

The baseline contains 100 tracked files. The tracked tree was unchanged before
editing; a pre-existing untracked `ecosystem/` directory prevents a claim of a
strictly clean workspace. It is not launch evidence and was neither modified nor
staged. No GVAI or GVAI Safety Systems repository is part of this work.

| Surface inspected | Finding and launch treatment |
| --- | --- |
| README | Cautious switch language, but negative fluid results absent from the front page; operational product work dominates later sections. Replace with research scope and prominent failures. |
| Historical THEORY, PAPER, entropy proposal | Assertions of QM/GR unification, fundamental-constant derivation, entropy repayment, eternal replication, infinite energy, and universal alignment exceed the evidence. Preserve text with prominent historical/unverified notices, not as current findings. |
| Equations and simulation | Energy integral and activation forms are exploratory; no dimensional closure or independently identified physical mechanism. The cosmology code fits to a target and assumes damping. Numerical output is not an independent prediction. |
| Switch theory and falsification | Existing sequential clock, EM, environmental gates are stronger than timing-only classification. Keep their limited interpretation. Old `A(t)` denotes activation, not the aligned state in the new notation. |
| Preregistrations and results | Preserve all thresholds, metrics, weights, validity rules, confounds, and historical verdicts. F0/F1/F1b are NOT SUPPORTIVE; F2 is INVALID, not a valid negative benchmark. F2b had code and preregistration but no tracked report. |
| New unchanged F2b run | 2026-10-05, Python 3.11.16, NumPy 2.4.6: implemented validity gates pass, 60/60 active events, no control events. Success criterion not met at any noise level. Record as a new NOT SUPPORTIVE result. |
| Switch failure notes | Five failed approaches retained: naive null, adversarial artifacts, flexible timing fit, first control matrix, and zero-power clock correction. Failure rates must stay visible. |
| Plots and data | Root PNGs are conceptual/toy illustrations, not raw physical measurements. Longitudinal CSVs are CI monitoring summaries, not GV experimental observations. No tracked physical waveform dataset supports a GV claim. |
| Hardware specifications | Phase 0, E1, modality, wiring, acceptance, procurement, and trial manifests are plans/software. No tracked completed bench calibration or apparatus certification. Procurement estimates are optional, not a launch prerequisite. |
| Scripts and prototypes | CI metrics, plots, and tether simulations illustrate encoded engineering dynamics. LLM outcome scripts use external services if credentials are supplied; excluded from offline reproduction. No product or safety-system changes. |
| Tests and CI | Three existing deterministic edge-case tests pass in a local virtual environment. CI uses Python 3.11. Initial container lacked pytest; requirements omitted NumPy/SciPy and prototype NetworkX. Legacy Makefile ends mid-rule. |
| References and versioning | PAPER has a historical bibliography, not evidence supporting GV. Bibliographic precision needs expert review, notably its Hawking title/year pairing. External cosmology documents are not local validated derivations. No baseline citation file or research release exists. |

## Requested Experiment IDs Without Records

`EM-001`, `EM-002`, and `TUNING-HW-001` do not occur in the tracked default-branch
research records. Read-only checks of the fetched switch, mathematics, and
upstream-inference branches also found no records for those IDs. They are retained
as **PENDING provenance**, not asserted to be completed, ready, or scientifically
inconclusive experiments. An owner must supply their original protocols, data,
and actual status before these entries can be promoted. No protocol is invented
for them. E1 is not silently renamed EM-001 or EM-002.

## Claim-Term Review

The tracked repository was searched case-insensitively for `prove`, `proof`,
`confirmed`, `God exists`, `God signal`, `new physics`, `discovery`, `detected`,
`impossible`, `supernatural`, `creator`, and `energy source`. Every baseline hit
was reviewed in context:

- THEORY and PAPER's proof/verification wording and stronger non-keyword claims
  require historical-status notices; fitting an observed target is not deriving it.
- Makefile's "fastest proof" is marketing for a drift demonstration, not scientific
  proof; the launch entry point must use research terminology.
- Switch preregistrations, failure notes, and detector documents mostly use these
  terms in explicitly forbidden interpretations or limits on inference. Keep them.
- "Prove" in hardware documents refers to apparatus validation, not GV; qualify
  those documents as unrun designs. "Analog Discovery" is an instrument name.
- `detected` in acquisition schemas and Python identifiers refers to threshold
  events or ordinary electrical pickup. It is not GV detection.
- Fluid F1b's detection rate refers to an encoded fluid event; its verdict remains
  NOT SUPPORTIVE. Code comments/plot labels implying eternal energy in the legacy
  cosmology toy need assumption-only context.
- No baseline positive assertion of "God exists", "God signal", "supernatural",
  or "creator signal" was located. Historical philosophical speculation is not
  promoted into causal evidence.

The launch does not rewrite results or merge alternate research branches.
See the [evidence ledger](../evidence/evidence_ledger.json) and
[new F2b report](../experiments/GV_FLUID_F2B_RESULTS.md).