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
| F0 | NOT SUPPORTIVE | Paired warning advantage 0, 0, 0, -0.001370; no gain over second derivative. |
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