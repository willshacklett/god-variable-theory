# GV-PHY-001 Fixture and Geometry

**LOGICAL LAYOUT / NOT A CONSTRUCTION DRAWING. PENDING.** Relative locations are
planning settings, not measured millimeter precision or a certified mechanical fixture.

```text
Independent command box ---- isolated marker -------------------- ADC AI00
         |                    driver cable (fixed loop)
         v
 SOURCE BOARD S: guarded relay/driver + independent contact LED
   C10 field axis; C11 fixture acceleration; C12 source microphone
   C01 current; C02 contact voltage; C06 body temperature; C07 optics
         |                                      |
         |  0.5 m initial / 1.0 m distance arm   | native outputs
         v                                      v
 RECEIVER BOARD R: C03 field, C04 acceleration, C05 pressure
   D13 electric pickup, D14 RF detector near receiver inputs

 ENVIRONMENT E: C08 magnetic reference, separate from source/receiver
 CLOCK BOX T: independently powered C09 oscillator
 ADC/COMPUTER A: common analog clock; shield/ground plan reviewed separately
```

Record source/receiver sensing-element coordinates, axes, heights, fixture IDs,
room landmarks, relative source-reference spacing, ambient-reference position,
DAQ location, cable paths/lengths, shields and photographs. Source witnesses should
be close enough to characterize the source but outside measured saturation range;
the distance cannot be honestly fixed before actual sensor/relay selection. Fix and
publish it after pilot, never choose the favorable position from evaluation traces.
Environmental reference is initially >=2 m away where bench space allows; test
whether relay activity reaches it. An affected reference is not independent room noise.

Use a rigid source support and independently supported receiver. Nonconductive
mounts reduce conductive coupling but do not eliminate mechanical/floor paths.
Cable strain relief must not bridge isolation pads unnoticed. One-axis sensors
have a declared axis; rotate/calibrate during qualification, then lock geometry.
No mic/accelerometer may be relocated to chase a trace after the manifest is frozen.

## Controlled Variants

- Distance arm: receiver sensing positions at 0.5/1.0 m; preserve axis and document
  changed cable route/path. Distance is not an independent propagation-speed claim.
- Shield arm: distance fixed, documented conductive enclosure/return; magnetic
  shielding material is a separate variant. Measure acoustic/structural changes.
- Mechanical arm: fixed relay/receiver coordinates, change structural connection
  only through a reviewed support variant, measure vibration/sound/field effects.
- Acoustic arm: noncontact barrier, same supports and cables; measure reflections
  and any EM or mechanical effect of the barrier.
- Mechanical-only comparator: guarded remote nonconductive linkage/contact surrogate
  on a separate characterization support. It cannot pretend to reproduce an enclosed
  relay's armature/core/chassis. Record geometry and unmatched source waveforms.

Use a measured ruler/position jig and report its uncertainty; a proposed distance
does not justify fabricated +/-1 mm accuracy. A reconstruction record must name
every support/shield/cable variant and calibration/configuration hash. Actual fixture
dimensions, guard/linkage design and approved CAD/mechanical drawing remain gaps.
See [components](GV_PHY_001_COMPONENT_REQUIREMENTS.md) and [power](GV_PHY_001_POWER_AND_GROUNDING.md).