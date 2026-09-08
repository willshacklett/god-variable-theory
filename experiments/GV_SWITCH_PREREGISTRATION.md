# GV Switch Experimental Preregistration

Protocol version: **GV-SWITCH-PRE-REG-0.1**

Status: **Synthetic preregistration framework**

Important limitation:

> This protocol is not evidence that GV exists. It defines how a future candidate signal would be tested against modeled conventional explanations before any GV interpretation is considered.

---

## 1. Primary Research Question

If a controlled local activation event is produced, does any reproducible response appear at distant detectors that:

1. follows physical source-detector distance,
2. survives clock reassignment,
3. does not track electromagnetic controls,
4. does not track modeled mechanical, acoustic, or thermal controls,
5. and remains reproducible under repeated trials?

---

## 2. Core Hypotheses

### H0 — Conventional Explanation

No independent GV channel exists.

Any apparent response is caused by one or more of:

- random or correlated noise
- clock or timing bias
- cable propagation
- electromagnetic coupling
- acoustic propagation
- mechanical vibration
- thermal effects
- software timing error
- detector latency
- mixed instrumental contamination
- other known physical or statistical mechanisms

### H1 — Additional Propagating Channel

A reproducible distance-dependent response exists that survives the preregistered conventional-channel controls.

Important:

> H1 is not equivalent to "GV exists."

H1 means only:

> The measured response remains unexplained by the specific conventional mechanisms tested in this protocol.

---

## 3. Theoretical Timing Model

For a candidate propagation channel:

\[
t(d)=t_0+\frac{d}{v}
\]

where:

- \(t(d)\) is measured arrival time
- \(t_0\) is an unknown common offset
- \(d\) is source-detector distance
- \(v\) is estimated propagation velocity

For the c-like branch:

\[
v \approx c
\]

where:

\[
c = 299{,}792{,}458\ \mathrm{m/s}
\]

---

## 4. Detector Geometry

Synthetic reference geometry:

| Detector | Distance |
|---|---:|
| D1 | 10 m |
| D2 | 50 m |
| D3 | 100 m |
| D4 | 250 m |
| D5 | 500 m |
| D6 | 1000 m |

Real experiments may use different geometry, but the geometry must be fixed before unblinded analysis.

---

## 5. Gate Order

The protocol uses sequential exclusion gates.

### Gate 1 — Clock / Timing Crosscheck

Purpose:

Determine whether the timing law follows physical detector position or clock identity.

Method:

- repeat measurements
- randomly reassign clock channels
- estimate the propagation slope independently for each clock
- compare recovered slopes

Pass condition:

- recovered slopes remain consistent across clock identities
- spatial propagation remains stable after reassignment

Fail classifications:

- `CLOCK ARTIFACT`
- `CLOCK / TIMING ARTIFACT`

Passing classification:

- `CLOCK-CROSSCHECK SURVIVING CANDIDATE`

---

### Gate 2 — Electromagnetic Isolation

Purpose:

Determine whether the response tracks electromagnetic conditions.

Controls include:

- shielding
- source power
- antenna orientation
- modulation state

Pass condition:

The candidate remains reasonably stable under EM-specific manipulation.

Fail classification:

- `EM CHANNEL LIKELY`

Passing classification:

- `EM-ISOLATION SURVIVING CANDIDATE`

Important:

A c-speed signal is not by itself evidence against EM.

---

### Gate 3 — Environmental Isolation

Purpose:

Determine whether the response tracks environmental channels.

Controls include:

- vibration isolation
- acoustic damping
- temperature variation
- reduced-pressure condition

Fail classifications:

- `MECHANICAL CHANNEL LIKELY`
- `ACOUSTIC CHANNEL LIKELY`
- `THERMAL CHANNEL LIKELY`
- `NON-C ENVIRONMENTAL EFFECT`

Passing classification:

- `ENVIRONMENT-ISOLATION SURVIVING CANDIDATE`

---

## 6. Final Allowed Verdicts

The protocol permits only these final interpretations:

### `NULL SURVIVES`

No reproducible signal survives the minimum detection requirements.

### `KNOWN CLOCK/TIMING CHANNEL`

Timing behavior is explained or disrupted by clock/instrumental effects.

### `KNOWN EM CHANNEL`

The signal follows modeled electromagnetic controls.

### `KNOWN ENVIRONMENTAL CHANNEL`

The signal follows modeled mechanical, acoustic, or thermal controls.

### `UNEXPLAINED PROPAGATION CANDIDATE`

A reproducible spatial timing signal survives all preregistered modeled controls.

This verdict does **not** mean:

- GV detected
- new physics confirmed
- causality violation detected
- a new particle discovered

It means only:

> The tested conventional models did not explain the observed candidate.

---

## 7. Synthetic Calibration Targets

Current development targets:

### Null false-positive rate

\[
\mathrm{FPR} \le 1\%
\]

where:

\[
\mathrm{FPR}
=
P(
\text{unexplained candidate}
\mid
H_0
)
\]

### Detection power

For the synthetic injected candidate:

\[
\mathrm{TPR} \ge 95\%
\]

where:

\[
\mathrm{TPR}
=
P(
\text{candidate survives}
\mid
H_1
)
\]

---

## 8. Predefined Thresholds

The current synthetic gates use fixed thresholds.

These thresholds must not be changed after real data are inspected unless:

1. the original analysis is preserved,
2. the change is documented,
3. the revised analysis is explicitly labeled exploratory,
4. a new independent dataset is used for confirmation.

Threshold changes based on observed results invalidate the original preregistration claim.

---

## 9. Blinding

For a real experiment:

- detector identity should be masked during initial analysis where practical
- control-state ordering should be randomized
- cable assignments should be randomized
- clock assignments should be randomized
- data exclusion rules must be specified before unblinding
- analysis code should be frozen before the confirmatory dataset is opened

---

## 10. Required Controls

A real test must include, at minimum:

- clock reassignment
- cable reassignment or independent cable-delay calibration
- EM shielding controls
- source modulation controls
- RF monitoring
- acoustic monitoring
- vibration monitoring
- temperature logging
- pressure/environment logging where relevant
- detector latency calibration
- software timing validation
- independent timebase verification

---

## 11. Stopping Rules

A real experiment should stop or pause if:

- detector timing becomes unstable
- calibration drift exceeds preregistered tolerance
- shielding integrity fails
- clocks lose synchronization
- equipment configuration changes unexpectedly
- data corruption is detected
- an uncontrolled conventional signal is identified

Stopping must not depend on whether the interim result favors GV.

---

## 12. Exclusion Rules

Data may be excluded only for preregistered reasons such as:

- hardware failure
- missing timestamp
- synchronization failure
- detector saturation
- corrupted file
- documented protocol deviation

Data must not be excluded merely because they weaken the hypothesis.

---

## 13. Replication Requirement

A single unexplained result is not sufficient.

A candidate must survive:

1. internal repeat testing,
2. blinded replication,
3. independent apparatus replication,
4. preferably independent laboratory replication.

Only after independent replication should any new-physics interpretation be seriously considered.

---

## 14. Mass / Propagation Interpretation

If a candidate survives all controls and produces a reproducible propagation velocity \(v\):

### Case A — \(v \approx c\)

The propagating excitation is consistent with a massless or effectively massless mode.

This does not prove zero rest mass.

### Case B — \(v < c\)

A massive-mode interpretation may be considered only if the data also show a physically consistent dispersion relation.

Relevant relation:

\[
E^2 = p^2c^2 + m^2c^4
\]

Velocity alone is insufficient to determine mass.

---

## 15. Timeless / Pre-Spacetime Interpretation

If GV is treated as a pre-spacetime or timeless constraint, ordinary speed and mass may not apply directly to GV itself.

The measurable object would instead be the physical consequence of activation.

Conceptual form:

\[
\text{pre-spacetime constraint}
\rightarrow
\text{activation boundary}
\rightarrow
\text{physical propagation}
\]

The protocol therefore measures only the physical response.

---

## 16. Relationship to the GV Equation

Existing exploratory form:

\[
G_v
=
\int
\rho_{\text{total}}(x,t)
\,dV
+
\alpha
\]

Provisional switch extension:

\[
G_v(t)
=
\int
\rho_{\text{total}}(x,t)
\,dV
+
\alpha A(t)
\]

where:

- \(A(t)=0\) represents a latent state
- \(A(t)>0\) represents activation
- \(\alpha\) remains an initiating or boundary term

This extension is speculative and is not yet a derived physical law.

---

## 17. Locked Scientific Language

The following wording is permitted for a passing synthetic or experimental candidate:

> "Unexplained propagation candidate."

The following wording is prohibited without substantially stronger evidence:

- "GV detected"
- "God Variable proven"
- "new force discovered"
- "new particle discovered"
- "timeless field confirmed"
- "origin of the universe experimentally demonstrated"

---

## 18. Current Synthetic Protocol Status

Current implemented gates:

- clock crosscheck
- EM isolation
- environmental isolation
- master protocol audit runner

Current synthetic master result:

\[
6/6
\]

for the predefined demonstration scenarios.

This result validates only internal model routing and synthetic discrimination.

It is not an empirical physics result.

---

## 19. Next Development Stage

Before any physical experiment:

1. integrate adversarial null simulations
2. stress-test thresholds over wider parameter ranges
3. add confidence intervals
4. add power curves
5. add blinded synthetic datasets
6. test mixed-channel contamination
7. freeze protocol version 1.0
8. only then design hardware

---

## 20. Core Principle

The protocol is designed to make it easier to disprove the GV interpretation than to confirm it.

If known physics explains the signal, the protocol should say so.

If the signal disappears, the null survives.

If a signal survives every modeled control, the strongest allowed conclusion is:

> **Unexplained propagation candidate requiring independent replication.**
