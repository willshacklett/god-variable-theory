# GV Switch Experiments

> Public research inventory: [evidence](../docs/EVIDENCE.md),
> [negative results](../docs/NEGATIVE_RESULTS.md), and
> [roadmap](../docs/EXPERIMENT_ROADMAP.md). This directory also contains fluid
> benchmarks. F0/F1/F1b/F2b are NOT SUPPORTIVE; F2 is INVALID / INCONCLUSIVE.
> Switch simulations are methodology only. Hardware specifications and manifests
> do not establish completed physical runs; no equipment purchase is required
> to reproduce the computational record. THE GOD VARIABLE HAS NOT BEEN CONFIRMED.

## Goal

Convert the GV Switch Hypothesis into falsifiable timing tests.

This directory deliberately separates speculative theory from measurable experimental structure.

## First Toy Simulation

Run:

    python3 experiments/gv_switch_sim.py

The simulation compares:

- null response
- propagation at the speed of light
- propagation below the speed of light

The code does not claim to model a real GV field.

It only establishes a framework for asking:

> If a signal existed, what timing pattern would different propagation models produce?

## Experimental Discipline

Any real-world experiment must include controls for:

- electromagnetic coupling
- radio-frequency interference
- acoustic propagation
- mechanical vibration
- thermal effects
- common clock error
- cable delay
- detector latency
- software timing error
- statistical false positives

## Pre-Registered Null

Before testing:

> No independent GV channel exists.

A result counts as interesting only if it survives known-channel controls and independent replication.

## Development Path

1. Timing-only simulation
2. Add measurement uncertainty
3. Add false-positive models
4. Add shielding/control channels
5. Add preregistered statistical thresholds
6. Only then consider hardware experiments
