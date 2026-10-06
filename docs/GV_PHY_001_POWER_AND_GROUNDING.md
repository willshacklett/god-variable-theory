# GV-PHY-001 Power and Grounding

**REVIEW ARCHITECTURE ONLY; NOT A RATED ELECTRICAL SCHEMATIC. PENDING.**
No mains experimentation, lifted protective earth, high voltage, pressure,
hazardous radiation, explosive/chemical system or large energy-storage capacitor.

## Power Domains and Logical Circuit

```text
P-CMD isolated controller supply: marker buffer ---> isolated DAQ marker input
                                command -------> reviewed logic/driver interface

P-COIL <=5 V, <=100 mA current-limited, fused
   + ---- relay coil ---- drain/collector of rated low-side driver ---- P-COIL return
   |______ rated flyback clamp across coil (orientation/rating reviewed) _______|

P-LOAD independent battery <=5 V, <=5 mA
   + ---- current-limiting resistor ---- LED ---- dry relay contact ---- battery -
         optical photodiode/TIA observes LED; no assumed galvanic bridge

P-SENSOR isolated low-noise domains ---> sensor / fixed conditioning ---> differential ADC
P-DAQ reviewed DAQ supply -----------> common-clock ADC ---- isolated/data-reviewed USB ---- host
P-TIME separate oscillator supply ---> timing reference input (do not derive from DAQ clock)
```

This diagram intentionally omits unselected component values, pinouts, fuse/clamp
ratings and isolation parts. Do not construct from it. A qualified reviewer must
approve a component-specific driver and wiring schematic before energization.

Record each domain, return connection, differential/common-mode range, shield bond,
isolation barrier, leakage/capacitance and probe ground. Single-point signal reference
at the reviewed acquisition boundary where needed; don't assume that joining all
returns creates a clean star ground. Galvanic isolation is preferred for contact
voltage/current probes where a bridge would defeat the independent load. Every
isolation/front-end part must meet low-voltage signal ranges and preserve bandwidth;
isolation delay/dispersion is part of timing calibration, not a free correction.

Sensor supplies must not share the coil return. Separate source/receiver branches
and measure their rails in qualification. A common DAQ can still couple channels
through reference rails or protection networks; use terminated inputs, injected
single-channel tests, swapped inputs and external comparisons. Independent sensors
do not imply independent electronics.

Cable shields bond at the declared boundary by reviewed design, never by arbitrary
both-end clips. Some RF shielding needs short multiple bonds; such a variant must
be assessed for low-frequency loops and documented, not represented as perfect
single-point grounding. Keep driver/flyback loop small and fixed, sensor leads
differential/twisted and strain-relieved, power away from receiver leads.

USB/computer ground and charger earth are potential bridges. Prefer reviewed data
isolation or a battery-host configuration and check actual remaining paths; never
defeat scope/computer protective earth. Independent timing/RF verifier probes can
also bridge domains. Record changes when verifier hardware is connected/disconnected.

## Ground-Loop and Pickup Qualification

With safe low-energy dummy loads, test source disconnected, controller marker only,
resistive/inductive electrical-only switching, terminated receiver inputs and one
injected ADC input. Compare cable and permissible shield termination variants with
measured gain/latency held valid. Log supply ripple and common-mode pickup using
appropriate protected differential inputs. A transient reaching magnetic, mic and
accelerometer outputs through shared rails can manufacture 1 ms coherence without
any new pathway. Do not dismiss it because every channel has a different sensor label.

Current-limit/fuse ratings, wire gauge, MOSFET SOA, flyback voltage/energy, input
clamps, enclosed motion and thermal stop rules need actual component data and
independent safety sign-off. No such approval is claimed. See
[construction readiness](GV_PHY_001_CONSTRUCTION_READINESS.md).