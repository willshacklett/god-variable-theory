# God Variable (GV)

**God Variable (GV)** is an experimental research program exploring whether a common constraint-based framework can describe survivability, degradation, and state transitions across engineered and physical systems.

The project currently has two distinct tracks:

1. **Operational GV** — measurable constraint strain, drift, recoverability, CI scoring, and runtime monitoring.
2. **Theoretical GV** — speculative work asking whether a deeper constraint or activation principle could have physical meaning.

The operational work is software and engineering.

The theoretical work is a hypothesis.

They should not be treated as equivalent evidence.

---

## Current Research Focus — The GV Switch

The newest theoretical program is the **GV Switch Hypothesis**.

The core question is deliberately narrow:

> Could a reproducibly triggered physical event produce a measurable response that survives known electromagnetic, timing, cable, acoustic, mechanical, thermal, and instrumental explanations?

The conceptual analogy is a switch:

\[
\text{latent possibility}
\rightarrow
\text{activation}
\rightarrow
\text{lawful physical evolution}
\]

This does **not** assume that a literal switch exists in nature.

It provides a falsifiable experimental framing for asking whether any reproducible physical residual exists after conventional mechanisms are excluded.

See:

**theory/gv_switch_hypothesis.md**

---

## Scientific Status

### What has been done

The repository now contains:

- GV Switch hypothesis
- propagation timing simulations
- Monte Carlo calibration
- adversarial-null testing
- documented failed classifiers
- independent clock-artifact crosscheck
- electromagnetic isolation framework
- environmental isolation framework
- master synthetic protocol
- experimental preregistration
- benchtop roadmap
- Phase 0 hardware specification
- detector modality framework
- E1 electrical transient sensor specification
- randomized and blocked trial designs
- E1 calibration software
- E1 confirmatory preregistration
- E1 bench assembly specification
- E1 procurement plan

### What has NOT been done

No physical experiment has produced evidence for GV.

No unexplained propagation signal has been observed.

No new particle, field, force, or physical constant has been detected.

Synthetic tests validate only whether the experimental logic behaves correctly against the models encoded in the simulations.

---

## Experimental Standard

The strongest result currently permitted by the GV Switch protocol is:

`UNEXPLAINED PROPAGATION CANDIDATE`

That would mean only:

> A reproducible signal survived the conventional mechanisms actually tested and requires independent replication.

It would **not** mean:

> GV detected.

Unknown conventional mechanisms could still remain.

---

# Phase 0 — Learn How the Apparatus Can Fool Us

Before any unexplained-signal search, the apparatus must correctly identify known mechanisms.

Required Phase 0 controls include:

- trigger timing
- cable delay
- clock/channel bias
- electromagnetic coupling
- acoustic propagation
- mechanical vibration
- thermal drift
- active/sham trials

The current Phase 0 acceptance target is:

\[
7/7
\]

known-channel validation tests passed before Phase 1 is allowed.

See:

**experiments/GV_SWITCH_PHASE0_HARDWARE_SPEC.md**

---

# Prototype E1-A

The first physical prototype is intentionally ordinary.

**E1-A** is a passive electrical transient sensor designed to characterize electromagnetic pickup from the trigger apparatus.

It is **not** a GV detector.

Initial architecture:

- passive 5 cm × 5 cm copper pickup plate
- 50-ohm coaxial signal path
- CH1 trigger reference
- CH2 E1 sensor
- initial source distance of 0.25 m
- low-voltage, low-energy trigger
- no amplifier

E1-A must characterize:

- timing jitter
- cable delay
- oscilloscope channel skew
- shielding response
- orientation response
- noise floor
- sham false-positive rate
- saturation behavior

before it can be used as a trusted control instrument.

See:

**experiments/GV_SWITCH_ELECTRIC_SENSOR_SPEC.md**

**experiments/GV_SWITCH_E1_BENCH_ASSEMBLY.md**

**experiments/GV_SWITCH_E1_PREREGISTRATION.md**

---

# Why the Failed Tests Matter

Early synthetic classifiers initially appeared highly successful against simple null models.

Harder adversarial tests broke them.

Cable artifacts and clock bias could imitate apparent propagation.

A free linear timing model also demonstrated a fundamental problem:

\[
t=t_0+\beta d
\]

from an instrumental bias can resemble:

\[
t=t_0+\frac{d}{v}
\]

from physical propagation.

That failure changed the protocol.

The current design therefore uses independent physical interventions rather than relying on timing fits alone.

See:

**experiments/GV_SWITCH_FAILURE_NOTES.md**

Negative results and failed methods are retained as part of the scientific record.

---

# Operational GV

The operational side of GV predates the GV Switch work and addresses a different problem:

> Can cumulative constraint strain, degradation, and loss of recoverability be measured before conventional pass/fail systems notice failure?

Start here:

### GV Drift Demo

https://github.com/willshacklett/gv-drift-demo

Minimal demonstration of early drift detection.

### GodScore CI

https://github.com/willshacklett/godscore-ci

Survivability-aware CI scoring and optional enforcement.

### GvAI Safety Systems

https://github.com/willshacklett/gvai-safety-systems

Runtime monitoring for AI and agent systems.

---

# Original GV Framework

The broader GV framework proposes a scalar representation of total constraint structure.

A core conceptual form preserved in the theory is:

\[
G_v =
\int \rho_{\text{total}}(x,t)\,dV
+
\alpha
\]

where the interpretation of \(\alpha\) remains theoretical.

See:

**THEORY.md**

The equation is a proposed framework, not an experimentally established law of physics.

---

# Longer-Term Theoretical Program

Possible theoretical directions include:

### Constraint-flow dynamics

\[
\partial_t G_v =
-\nabla\cdot J_{GV}
+
S(G_v)
\]

### Cosmological embedding

Potential relationships to:

- FLRW evolution
- effective energy density
- structure growth
- early-universe dynamics

### Quantum-field interpretation

Possible questions involving:

- effective field theory
- symmetry behavior
- UV/IR relationships

### Black-hole sector

Possible questions involving:

- horizon constraints
- entropy
- evaporation

These remain speculative until they produce quantitative predictions distinguishable from established physics.

---

# Repository Principle

The project follows a simple hierarchy:

\[
\text{idea}
\rightarrow
\text{model}
\rightarrow
\text{adversarial test}
\rightarrow
\text{preregistration}
\rightarrow
\text{instrument calibration}
\rightarrow
\text{physical experiment}
\rightarrow
\text{replication}
\]

A later step does not become valid merely because an earlier one succeeded.

---

# Current Milestone

The current milestone is:

> Build and calibrate E1-A against known electrical and instrumental effects.

Not:

> Detect GV.

If E1-A reveals that an apparent fast signal is ordinary electromagnetic pickup, that is a successful Phase 0 result.

---

## Coherence Eternal ⭐

If a system must run longer than its designers,  
it needs constraints that outlive intent.

---

## License

MIT unless otherwise specified.
