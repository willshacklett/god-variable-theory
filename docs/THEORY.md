# The God Variable: Research Definition

**THE GOD VARIABLE HAS NOT BEEN CONFIRMED.**

## Three Layers of Meaning

Keep three distinct uses of “GV” separate:

1. **Historical GV** is the speculative material preserved in the root
   [`THEORY.md`](../THEORY.md), [`PAPER.md`](../PAPER.md), and
   [`entropy_damping.md`](../entropy_damping.md). Its equations, $\alpha$,
   Switch language, entropy proposals, and original interpretations remain
   historical hypotheses. Their dimensional, dynamical, and empirical meanings
   are unresolved; preserving them does not validate them.
2. **Operational GV** is the research framework defined here: measurements,
   known-model comparisons, candidate statistics, preregistered tests, Local
   Tuning endpoints, ordinary baselines, and explicit rejection rules.
3. **Physical GV** would be a specified physical law, constraint, coupling, or
   independently measurable observable. It is presently unspecified. A physical
   claim requires quantitative prospective predictions distinguishable from the
   strongest ordinary model.

> **$G \neq GV$.** $G$ is a formulation-specific measured statistic, not the
> hypothesized physical entity. An unexplained residual is evidence that the
> tested model is inadequate for the data; it is not automatic evidence for GV.

The God Variable (GV) is hypothetical. This independent open research project
asks whether some state transitions have reproducible signatures not accounted
for by known causal pathways and simpler models. It does not establish a deity,
new physics, a force, a field, or an energy source.

> A residual is only a residual until known explanations are excluded.

**UNEXPLAINED ≠ GV; GV ≠ NEW PHYSICS; NEW PHYSICS ≠ GOD.**

Excluding the explanations actually tested is not excluding all possible ordinary
causes. An unexplained residual is not positive identification of GV.

## State, Observations, and Residuals

Let $S(t)$ be the system state, including relevant latent or controlled variables.
Let $X(t)=(X_1(t),\ldots,X_m(t))$ be the measured observable vector, with channel
units, calibration uncertainty, sampling bandwidth, and missing-data rules stated.
Let $K(t)$ be predictions in those same observable coordinates from an explicitly
specified known explanatory model, including ordinary dynamics, instrument response,
and control behavior. It is not an adjustable catch-all fit to the test data.

$$R(t)=X(t)-K(t).$$

Residual uncertainty includes model error and measurement error. Fit $K$ only on
permitted training/calibration data; evaluate it on independent test data. Compare
multiple defensible known models and report sensitivity to their assumptions.

A candidate transition time $t^*$ is set by an independent trigger or a frozen
detection rule. Selecting the most striking residual after inspection incurs a
search penalty; it cannot be treated as a preregistered trigger.

Define a formulation-specific candidate statistic:

$$G(t)=f\big(R(t),\text{temporal structure},\text{cross-channel structure},
\text{controls}\big).$$

$G(t)$ is a measured statistic, not the hypothesized GV itself. It must have a
versioned definition, fixed features/weights, declared units or normalization,
calibration population, missing-alarm treatment, and decision rule before test
data are opened. A large $G$ does not by itself identify a cause.

Generic finite-dimensional hidden-state representations of GV are reducible to
ordinary state-space/control theory unless they impose an additional, testable
restriction. No nontrivial cross-system transition invariant has been derived.

## Testable Candidate Criteria

These are prospective requirements, **not a claim that existing experiments have
met them**. Each formulation must freeze numerical tolerances, sample size,
uncertainty analysis, multiplicity correction, and rejection conditions in its
own preregistration. An unspecified threshold means the formulation is not ready
for confirmatory testing.

| Criterion | Measurement and discriminating test |
| --- | --- |
| Temporal localization | Freeze a window around independent $t^*$; compare event counts/statistics with equal-length pre-event, sham, and randomized-trigger windows. |
| Cross-sensor coherence | Specify independent channel pairs, correlation or delay statistic, and uncertainty; compare with shuffled channels and common-clock/common-mode controls. |
| Reproducibility | Freeze tolerances and an independent repeat dataset; estimate effect and failure rates across runs and apparatus, not just selected positive trials. |
| Intervention dependence | Randomize active/sham or tuning interventions; test a prespecified contrast with blinded labels and retained failed trials. |
| Resistance to known-cause controls | Predict responses under clock/cable swaps, EM shielding, vibration/acoustic isolation and thermal changes; a known-pathway match rejects the independent-channel interpretation. |
| Out-of-sample discrimination | Lock calibration/training before opening held-out data; report trajectory/trial-level FPR, detection power, missed events and uncertainty. |
| Simpler-baseline performance | Freeze conventional competing detectors and a primary endpoint; require positive predefined advantage at matched false positives, including the declared noise regime. A tie fails an advantage claim. |

The switch preregistration's synthetic FPR <=1% and TPR >=95% are development
targets, not physical discovery thresholds. The fluid benchmarks' control FPR
target is 5%; their frozen metrics and validity criteria remain unchanged.
Retrospectively applying this table does not upgrade historical results.

## Program A: GV Switch

Question: can a transition into a new state contain a reproducible signature that
survives known timing, electromagnetic, mechanical, acoustic, thermal, software,
statistical, and environmental explanations?

Use the existing [sequential switch protocol](../experiments/GV_SWITCH_PREREGISTRATION.md):

```text
CLOCK                         -> KNOWN CLOCK / TIMING
EM                            -> KNOWN EM
MECHANICAL / ACOUSTIC / THERMAL -> KNOWN ENVIRONMENTAL
Only after the tested exclusions:
UNEXPLAINED PROPAGATION CANDIDATE
```

Also retain null, insufficient-sensitivity and invalid-acquisition outcomes.
Survival of tested gates is not GV confirmation. Timing alone is unidentifiable:

$$t=t_0+\beta d\quad\text{and}\quad t=t_0+d/v$$

can describe a clock/cable artifact and a propagation law equally well. Ordinary
EM can propagate near $c$. Speed alone cannot identify a particle, mass, or GV.
The six archived master scenarios are generated models, not detector observations.

## Program B: Local Tuning / A

Question: can we identify a reproducible transition signature between a pre-state
and A that cannot be explained by ordinary dynamics, control behavior, or known
causes?

$$S_0\xrightarrow{T}S_1=A.$$

$S_0$ is the measured pre-state; $T$ is the transition/tuning process, including
ordinary feedback; $A$ is the resulting aligned state, not GV. The proposed
relation **GV -> transition / tuning process -> A** is a hypothesis about a
process, not an established causal arrow. Alignment alone does not test it.
The conductor analogy describes coordination only; it is not evidence.

### A Measurable Aligned State

The existing [stabilization code](../gv_stability.py) exposes `s_total`, `s_target`,
`ds_dt_effective`, `s_total_next`, and `gain`; the
[monitor simulations](../src/gv_edgecase_sims.py) expose strain time series and
recoverability. These support a prospective engineering definition based on
target error and stabilization, not claims about unmeasured physical phase:

$$e(t)=|s_{\mathrm{total}}(t)-s_{\mathrm{target}}|.$$

For an experiment with declared measurement interval $W$, define A as the state
for which $e(t)\le\epsilon$ and $|ds/dt|\le\delta$ throughout $W$, with a frozen
recoverability floor if recoverability is actually measured. Compare pre/post
error, settling time, and strain variability against the same ordinary controller,
sham intervention, and matched initial conditions. Freeze $W$, $\epsilon$,
$\delta$, sensor mapping and the error endpoint before collection. Existing
controller defaults are not a hardware preregistration.

This definition does not assert that error or variance reduction has been
demonstrated in a controlled GV experiment. Synchronization and physical phase
alignment are not established measurements here and are not assigned to A by
analogy. `TUNING-HW-001` has no located original record; its status is pending
provenance. No hardware completion is claimed.

Measure a candidate signature during $T$ separately from whether A is reached.
If ordinary feedback explains both $T$ and A, the GV-specific claim fails even
when the controller works well.

Local Tuning therefore defines a measurable endpoint, not a GV mechanism.

## Existing Mathematics and Its Limits

Historical proposal:

$$G_v=\int\rho_{\mathrm{total}}(x,t)\,dV+\alpha.$$

This is preserved, not established as a physical law. An energy-density volume
integral has energy units; $\alpha$ must have matching units. Domain, boundary
conditions, convergence, normalization, and connection to measured $G(t)$ remain
unspecified. The cosmology toy instead integrates over scale factor; that is not
the same mathematical object. Tuning to observed $\Lambda$ is not an independent
derivation, and imposed entropy repayment is not a demonstrated mechanism.

The historical descriptions of $\alpha$ as initiating, boundary, or origin term
do not uniquely determine whether it is a source, boundary functional, initial
condition, symmetry-breaking coupling, intervention, integration constant, or
dimensionless parameter. The displayed equation supplies no evolution law or
coupling that would decide among these roles. Treating $\alpha$ as dimensionless
would require an explicit reference scale before adding it to an energy.

The historical switch extension $G_v(t)=\int\rho_{\mathrm{total}}dV+\alpha A(t)$
uses $A(t)$ as an activation function. In this canonical notation call that
function $a_{\mathrm{act}}(t)$, leaving the old text intact. It is **not** the
aligned state A. No empirical mapping from either proposal to $G(t)$ is known.
The Switch specifies no unique activation dynamics, discontinuity, bifurcation,
boundary-condition change, or causal intervention.

The historical entropy-repayment proposal is unoperationalized: the system
boundary, entropy accounting, repayment channel, and quantitative endpoint are
not defined well enough to derive a test here. Preserve it as a separate
falsifiable hypothesis candidate, not as established GV structure.

The computationally explicit fluid formulation is stronger as a testable object:

$$G_{\mathrm{fluid}}=\sum_i z\big(\log(1+B_i)\big),$$

with baseline diagnostics $B_i$, equal weights, and control-only normalization
as frozen in each preregistration. It is a composite of ordinary observables,
not a new force. F0, F1, F1b and the corrective F2b do not support their respective
advantage claims; F2 is invalid. Do not modify them to meet this launch definition.

## Inference Boundary

Use the [claims ladder](CLAIMS.md), [evidence](EVIDENCE.md),
[negative results](NEGATIVE_RESULTS.md), and [falsification rules](FALSIFICATION.md).
Computational anomalies are not proof of new physics. Unexplained residuals need
additional controls. Extraordinary interpretations require independent replication
and independent causal evidence, not renaming a residual.