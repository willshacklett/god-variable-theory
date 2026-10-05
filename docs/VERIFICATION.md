# Launch Verification

Verified 2026-10-05 on `launch/public-research-baseline`, based on
`e5711b10fbce7f4949e62ee31db0c2216e19652a`. Python 3.11.16 on Linux;
[research lock](../requirements-research-lock.txt). This records computational
checks, not physical replication or GV confirmation.

## Exact Check Totals

| Check | Command / scope | Result |
| --- | --- | --- |
| Full existing and launch suite | `python -m pytest -q` | 68 passed, 0 failed |
| Research integrity | `python -m pytest -q tests/test_research_integrity.py` | 65 passed, 0 failed; included in the 68, not additional independent tests |
| Internal links | Integrity suite filtered with `-k 'internal_markdown_links or dashboard_local_asset_links'` | 43 passed, 22 deselected; Markdown file/heading links and dashboard assets |
| Computational smoke | `python scripts/reproduce_research.py --smoke` | 4/4 commands passed; 6 scenario verdicts, 4 CSV row-count checks, 2 nonempty plots |
| Frozen benchmarks | `python scripts/reproduce_research.py --benchmarks` | 5/5 commands passed; scientific outcomes below |
| Historical toy | `python scripts/reproduce_research.py --legacy` | 1/1 command passed; not physical evidence |
| Additional ledger entry points | Monte Carlo, clock crosscheck, EM isolation, environment isolation | 4/4 commands exited 0; synthetic only |
| Dependency consistency | `python -m pip check`; installed metadata against every lock pin | No broken requirements; 22/22 pins match, 0 mismatches |
| Whitespace | `git diff --check` | 0 errors |
| Setup shell syntax | `bash -n .devcontainer/postCreateCommand.sh` | Passed |
| Secret-pattern scan | 117 tracked/proposed launch files, 6 pattern families | 0 matches; not a guarantee against every possible secret |

The secret scan covers private-key headers, GitHub tokens, AWS access-key IDs,
Google API keys, Slack tokens, and long quoted literal credential assignments.
Environment-variable credential lookups are not embedded secrets. Ignored virtual
environments, generated artifacts and independent ecosystem clones are excluded.

## Frozen Computational Outcomes

Fresh stdout/stderr and hash/environment manifests are written under ignored
`artifacts/research/benchmarks/` and `artifacts/research/legacy/`; they do not
overwrite original reports or the archived switch audit. All five fluid source
files are unchanged from the baseline. Noise ordering below is 0%, 1%, 5%, 10%.

| ID | Fresh outcome | Numerical result / limitation |
| --- | --- | --- |
| F0 | NOT SUPPORTIVE | Difference of detector medians, not a median paired difference: 0, 0, 0, -0.001370; no gain over second derivative. |
| F1 | NOT SUPPORTIVE | All four paired advantages 0; initial-distribution confound remains. |
| F1b | NOT SUPPORTIVE | Paired lead advantages -0.180000, -0.140000, -0.066667, -0.040000; total variation/gradient energy stronger. |
| F2 | INVALID / INCONCLUSIVE | 20/60 active events (33.3%) versus required 70%; not a valid detector-performance negative. |
| F2b | NOT SUPPORTIVE | Implemented validity gates pass; 60/60 active events, zero controls. GV detects 5/60, 1/60, 0/60, 0/60; vorticity/strain detect all 60 at each level. Paired deltas -0.760000, -0.740000, undefined, undefined. |

F2b's [new report](../experiments/GV_FLUID_F2B_RESULTS.md) remains explicitly a
new unchanged-code run, not recovered historical evidence. Finite solver checks
are not convergence certification; FPR is in-sample and lead medians omit misses.

Additional synthetic checks reproduce easy-null FPR 0%, propagation injection
power 99.38%, clock artifact survival 0%, and encoded clock/EM/environment
intervention classifications. Their success does not identify a physical cause.
The historical toy produces stipulated entropy values 3.980 versus 0.040 and
probe counts 9.85e-10 versus 1.28e+08; those are programmed illustrative outcomes,
not observed entropy cancellation, eternal behavior, or demonstrated energy.

## Ledger Review

All 19 entries have unique IDs, existing source references and explicit scopes;
12 provide executable commands and 7 explicitly provide none. All 12 commands
were exercised across the benchmark, smoke, toy, additional-entry and test runs.
Coverage checks include every current experiment Python file, preregistration
Markdown file and fluid result report. No negative status was promoted.

| Status | Count |
| --- | ---: |
| SUPPORTIVE | 5 |
| MIXED | 1 |
| NOT SUPPORTIVE | 5 |
| INVALID / INCONCLUSIVE | 3 |
| PENDING | 3 |
| HARDWARE READY / NOT RUN | 2 |

SUPPORTIVE entries are four synthetic methodology checks and one software-check
entry, not physical GV evidence. Phase 0/E1 refer to protocol/software readiness,
not certified apparatus. EM-001, EM-002 and TUNING-HW-001 remain missing-record
provenance placeholders; no protocol, result or hardware completion was invented.

## Final Claim Review

The complete tracked/proposed launch tree was searched case-insensitively for
`prove`, `proof`, `confirmed`, `God exists`, `God signal`, `new physics`,
`discovery`, `detected`, `impossible`, `supernatural`, `creator`, `energy source`,
`infinite energy`, `entropy cancellation`, and `unification`. Relevant matches
were manually read in context, not automatically deleted.

| Match context | Classification / decision |
| --- | --- |
| Root THEORY/PAPER/entropy text and cosmology toy's strong conclusions | Historical proposal; prominent unverified-status notices and canonical rejection retained. Old drift-demo "proof" language is historical marketing, not current evidence. |
| Philosophical grace/conductor/eternal-coherence language | Philosophical interpretation or explanatory analogy only; no empirical causal conclusion. |
| "GV proven/detected", "new physics confirmed" and related quotes in preregistrations, modality/E1 specs, failure notes | Explicitly rejected interpretations; retain prohibitions and their surrounding context. |
| F1b's developing-event detection and code/schema `detected` identifiers | Harmless usage describing threshold events or ordinary electrical pickup, not detection of GV. F1b remains negative. |
| Apparatus "prove"/"proof of measurement", discovery thresholds, Analog Discovery product name | Harmless engineering/design usage; plans are unrun, screening is not discovery. |
| Public README, canonical theory, claims/evidence/release documents | Current scientific statements match the scoped ledger: no confirmed GV, new force/field, independently derived cosmological constant, entropy cancellation or infinite energy. |
| Contributions, tests, provenance words and scan vocabulary | Harmless usage or explicit inference limits. |

The README was read top to bottom. Its status, hierarchy, independent-replication
requirement, prominent failures and synthetic/physical distinction are explicit.
The [canonical theory](THEORY.md) preserves $S_0\xrightarrow{T}A$, keeps A
operational and distinct from GV, and distinguishes historical activation $A(t)$
from the aligned state. Citation, contribution, release and all research documents
resolve their internal links. Bibliographic correctness is not certified by links.

## Scope and Release Readiness

Only the 28 intended launch files are candidates for staging. No generated
artifacts, virtualenv contents, ecosystem files, frozen benchmark changes or
unrelated repository files belong in the commit. The pre-existing ecosystem
directory remains untouched and is now ignored; Git cleanliness must not be read
as its deletion. Cached whitespace, staged scope and post-commit/push cleanliness
are checked separately at publication time.

The computational/documentation baseline is technically ready for review as
v0.1.0. Human scientific approval is still required for F2b/statistical and solver
limitations, missing-ID provenance, historical bibliography and claim wording.
No tag, GitHub release, merge, physical experiment or hardware purchase is
authorized by these checks.

## Adversarial Pre-Merge Review

Review date: 2026-10-05; reviewed PR #3 head
`0b1ccb27ac8093333101985558f5c10de3939103`. The preceding totals describe the
initial launch checks and are preserved as history. The focused review corrections
do not alter any fluid implementation, seed, threshold, success rule or status.
At review start PR #3 was open/unmerged, mergeable, with one successful `gv-ci`
check, no comments/reviews/inline comments, and no requested changes. Two workflow
annotations concern Node action-runtime deprecation and the Ubuntu runner migration,
not scientific results. New main commits only append longitudinal CI summaries.

### Must-Fix Findings and Corrections

1. F0 was mislabeled as a median paired advantage. Its script/report compute a
	 difference of detector medians. The protocol names a trajectory-wise comparison;
	 that implementation gap is now explicit. The negative verdict is unchanged.
2. The current cosmology toy contradicts the historical claimed agreement: Lambda
	 `5.844e-237`, target `1.1056e-52`, relative error `1.00`, entropy proxy
	 `-1.292e27`. These failures are now visible in the ledger, README and failure
	 document. The historical paper is not rewritten. Standalone generated plots
	 carry historical/non-evidence notices; their numerical computation is unchanged.
3. Master switch gates generate separate model-specific datasets. This supports
	 routing checks, not a single measured signal surviving composite controls.
	 The ledger now states this limitation explicitly.
4. The legacy core consistency placeholder accepts zero Lambda because its
	 `1e-50` absolute tolerance exceeds the `1.1056e-52` target. Its docstrings now
	 identify it as non-validating historical code. No tolerance was tuned.
5. The switch preregistration's old activation A(t) now cross-references canonical
	 aligned-state notation, explicitly without changing the original protocol.
6. Integrity tests now compare five ledger verdicts with actual report outcomes,
	 discriminate F0's endpoint, preserve undefined F2b medians, and exercise invalid
	 statuses/schema/references/scripts, missing/duplicate IDs, negative promotion,
	 broken headings/files and paths outside the repository.

### Scientific Statement Classification

Classification: **A** directly supported by repository evidence; **B** procedural
or methodological requirement; **C** hypothesis/prospective definition; **D**
interpretation; **E** historical proposal; **F** unsupported/overstated current
claim requiring correction. These classifications apply to the scientific
sentences/tables in the listed documents, not merely their headings. Definitions
and future requirements are not classified as completed observations.

| Document / statement group | Classification and basis |
| --- | --- |
| README description, Switch/Local Tuning questions, hypothetical GV arrow | C: research questions, no claimed causal identification. |
| README status, negative/current experiments, computational commands/counts | A: reports, ledger, executable checks; missing IDs mean bounded provenance search, not proof of nonexistence. |
| README evidence requirements, hierarchy, independent replication, contribution rules | B: required inference/procedure boundaries. |
| README historical paragraphs and legacy failure description | E for old proposals; A for current failed numerical output; D for limits on interpretation. |
| Canonical THEORY S/X/K/R/t*/G definitions, aligned-state thresholds | C: proposed operational quantities; B: training/test separation and frozen tolerances. No measured physical A is asserted. |
| Canonical THEORY code observables, existing composite, negative verdicts | A: code/protocol/report references. |
| Canonical THEORY clock/propagation degeneracy and energy-integral unit limits | A: displayed algebra; D: no causal identification from those equations. |
| Canonical THEORY activation/integral proposals | E; no established law or mapping to measurements. |
| CLAIMS ladder requirements and prohibition of automatic escalation | B; current ceiling A from scoped ledger and synthetic audit, with D interpretation. |
| EVIDENCE inventory/status/results/provenance | A for file-backed results; B for controlled vocabulary/coverage requirements; D for each limited interpretation. |
| NEGATIVE_RESULTS numerical observations and original criteria | A; lessons and reasons against incremental-value claims D; next-test requirements B. Historical unsupported conclusions E, not current findings. |
| FALSIFICATION failure decisions, versions/IDs/new-data and anti-goalpost rules | B; no supported universal formulation A/D. It permits rejecting the tested formulations rather than redefining them. |
| ALTERNATIVE_EXPLANATIONS diagnostics and control matrix | B: prospective tests, not assertions that those controls have physically been implemented. Known confounding examples A; inference limits D. |
| EXPERIMENT_ROADMAP completed/failed/inconclusive entries | A; future questions C and procedural readiness B. READY is not certified apparatus. |
| RELEASE_NOTES and original VERIFICATION outcomes | A within computational/software scope; readiness D; future human approval B. |
| Ledger hypotheses, success rules, results, interpretations, limitations | C/E for hypotheses, B/A for frozen/documented criteria, A for available results, D for interpretation. Missing-record entries explicitly have no empirical hypothesis/result record. |
| CITATION author/repository/license and CONTRIBUTING standards | A for existing author/repository/license records; B for citation/procedure, replication and criticism requirements. No affiliation/publication status is invented. |
| Root PAPER/THEORY/entropy proposals, legacy cosmology/tether illustrations | E; unsupported as current science, retained with prominent notices. Philosophical interpretations D, not evidence. |
| Initially incorrect F0 attribution and any implication of successful cosmology fitting | F at the reviewed head; corrected above to match actual code/output. No current F claim is retained as a finding. |

The expanded tracked-text scan also includes `derived`, `derivation`, `validated`
and `verified`, in addition to the original vocabulary. Scientific hits are
covered by this table and the prior contextual classifications. Code `detected`
identifiers, schema events, empty checklist items, instrument names and credential
lookups are harmless usage. Forbidden GV-detection quotes remain prohibitions.
"Validated synthetic gates" means checks within the supplied generator, not
independent methodology validation. Historical philosophical text remains E/D.

### Ledger and Supportive-Entry Challenge

All 19 entries were checked against their referenced code/protocol/result files;
counts remain **5 SUPPORTIVE, 1 MIXED, 5 NOT SUPPORTIVE, 3 INVALID / INCONCLUSIVE,
3 PENDING, 2 HARDWARE READY / NOT RUN**. Existing protocol Git history precedes
implementation, including F0 (8e7ac8f8 before e8d3647d) and F2b (5b432bc0 before
6546fa0d). This establishes repository chronology, not externally registered
preregistration or proof that outcomes were unknown privately. No original rule
or numerical result was changed by this review.

| Entry | What exactly is supportive? | What is not established? |
| --- | --- | --- |
| SWITCH-CLOCK | Clock reassignment/slope code rejects encoded clock artifacts and retains spatial injections in its generator. | Real clock calibration or physical GV; ordinary EM also survives. |
| SWITCH-EM | Generator-specific shielding/power/orientation/modulation classification follows its encoded EM response. | Measured shielding, all EM exclusions, independent validation or a field. |
| SWITCH-ENVIRONMENT | Encoded mechanical/acoustic/thermal models receive the expected classifications. | Real environmental exclusion, joint confounds, physical causation. |
| SWITCH-MASTER | Six seeded scenario routes produce the specified software verdicts. | A shared measured signal through all gates, composite-null FPR, physical detection. |
| EDGECASE-CI | Three seeded assertions about programmed monitor behavior pass. | General detector superiority, independent replication or physical GV. |

These narrow successes justify their scoped labels only; none supports creator
signals, new physics, fields or independent physical replication. The timing
entry remains MIXED and failed classifiers remain NOT SUPPORTIVE.

### Statistical and Numerical Limitations

- Calibration controls are reused to estimate normalization, thresholds and FPR.
	Reported 5% FPR is not an independent held-out estimate or a confidence bound.
	Quantile ties can produce 0% FPR for a baseline; matching is not always exact.
- F0's primary-statistic mismatch is disclosed above. F1's separated amplitudes
	and different observation windows limit precursor interpretation.
- F2b has 60 controls/60 actives; the noise conditions reuse the same flows, not
	four independent studies. Its complete paired samples are only 5 and 1 at
	0%/1%, and absent at 5%/10%. Missing alarms remain NaN/undefined, not zero.
- Conditional lead medians select detected events; a longer median among rare
	detections is not broad reliability. The paired best-baseline maximum is an
	oracle per trajectory, not a single deployable detector. That frozen rule was
	not changed, and vorticity/strain also individually outperform GV here.
- Multiple baselines/noise levels are compared without inferential multiplicity
	correction. No p-values, confidence intervals, population-effect uncertainty
	or independent power study are supplied for fluid superiority claims. Reported
	switch "power" is an empirical simulated detection fraction, not apparatus power.
- Event definitions reuse ordinary diagnostics; results concern those predefined
	events, not universal instability detection. Viscosity regimes differ in F2/F2b;
	this is an ordinary simulated-regime comparison, not proof of a distinctive cause.
- Finite values and fixed resolution are not grid/time-step convergence, error
	bounds or physically validated solver regimes. A log composite depends on the
	specified diagnostic scales; no unit-invariant physical scalar is established.

These gaps weaken generalization and significance claims; they do not turn a
failed frozen superiority criterion into support. Any improved analysis requires
a new formulation/version, prospective criteria and independent/held-out data.

### Provenance and Bibliography

All fetched reachable Git history/branches were searched for the three missing
IDs and hyphen/underscore/space variants. Only the launch placeholders were found.
Deleted/unfetched/private records cannot be ruled out. EM-001, EM-002 and
TUNING-HW-001 remain PENDING provenance; no protocol or hardware result is invented.

Public Crossref metadata confirms Weinberg (1989), Landauer (1961), Yudkowsky's
2008 chapter and Hawking's **Black holes and thermodynamics** (1976, Physical
Review D), DOI `10.1103/PhysRevD.13.191`. The initial Hawking audit concern is
resolved; query-ranking mismatches were not treated as incorrect citations.
Planck DOI `10.1051/0004-6361/201833910` matches collaboration/year/journal;
exact title/subtitle formatting merits bibliographic review. Penrose's specific
1989 edition was not verified by the query. Maldacena's retrieved journal record
`10.1023/A:1026654312961` is dated 1999 rather than the draft's 1998 reference;
identify the intended version before editing history. Tononi DOI `10.2307/25470707`
is **Consciousness as Integrated Information: a Provisional Manifesto** (2008);
the historical reference abbreviates the title. No bibliography item supports GV
by association; no invented DOI, affiliation, publication or peer review is added.

### Clean-Environment Review Verification

Created a fresh `/tmp/gv-review-venv` with Python 3.11.16 and installed all 22
research-lock pins successfully. This is a fresh dependency environment, not
independent scientific replication or certification of other platforms.

| Check | Review result |
| --- | --- |
| `make test` / full suite | 85 passed, 0 failed |
| Integrity suite | 82 passed, 0 failed, included in the full total |
| Internal-link tests | 43 passed; 39 integrity tests deselected |
| Evidence schema/coverage/negative/report/mutation/endpoint checks | 36 passed; 46 integrity tests deselected |
| Smoke commands | 4/4; 6 verdicts, 4 CSV row counts, 2 nonempty plots |
| Frozen benchmark commands | 5/5 exit 0; all five stdout files byte-identical to the initial run |
| Additional synthetic commands | 4/4 exit 0; outputs under ignored review artifacts |
| Legacy toy | 1/1 exit 0; numerical failure disclosed, figures labeled historical |
| F2b unrounded-array inspection | 0 control events, 60 active events; GV 5/1/0/0, vorticity/strain 60 each; paired n=5/1/0/0, medians -0.76/-0.74/undefined/undefined |
| Dependency consistency | No broken requirements; 22/22 pins match |

Before publishing the correction, tracked-file secret patterns, working/cached
whitespace, staged scope, clean post-commit state and new-head GitHub checks are
verified separately. Scientific approval is not conferred by green CI. Readiness
means this limited public research baseline can be reviewed/merged, not that GV
is established. One additional human scientific/bibliographic review is recommended
before any public tag/release. No merge, tag or release is performed here.