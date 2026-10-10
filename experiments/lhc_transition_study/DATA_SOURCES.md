# CERN source discovery and access ledger

Phase 1 checked 2026-10-10 UTC. **No source content or available dataset was
directly verified in this environment.** Phase 2 attribution and retries follow.
Direct `web_fetch` and `curl -L --max-time 25 -sS -I` requests failed DNS
resolution for every host below (`curl: (6) Could not resolve host`).
These are CERN-domain **unverified leads**, not verified citations or evidence of
public transition data. No restricted login, API, download or payment was attempted.

| Source lead / attempted URL | Intended verification | Access, units, precision and limitations |
| --- | --- | --- |
| LHC Programme Coordination: https://lpc.web.cern.ch/ | Fill chronology, beam-mode transitions, stable-beam intervals and fill context | Expected public-facing coordination material; actual access and downloadable records unverified. Units, clock basis, precision, completeness and synchronization unknown. Summaries would not substitute for raw magnet/timing measurements. |
| NXCALS documentation: https://nxcals-docs.web.cern.ch/ | Logging schemas, query access rules, timestamps, magnet-current/ramp, beam-mode, loss and timing variables | Documentation availability unverified here. Treat operational logging access as requiring authorization until CERN explicitly confirms otherwise. Public documentation would not grant access to logged data. No variable names, units, cadence, timestamp precision or entitlements verified. |
| CERN Open Data: https://opendata.cern.ch/docs/about | Catalogue scope, licences, specific records containing operational transition timestamps and synchronized instruments | Public-release portal lead, not a verified release. Collision/event datasets must not be assumed to contain operational command, magnet or dump logs. No eligible record, dataset licence, unit or precision verified. |
| CERN Document Server publication lead: https://cds.cern.ch/record/1129806 | LHC design/accelerator reference and links to relevant instrumentation publications | Record identity, title, content and access not verified; do not cite it as a confirmed publication. Publication descriptions are not measurements or export permissions. Units and timing precision unknown. |

## Publication follow-up (unverified topics, not citations)

Use CERN Document Server to locate and read accelerator publications on:

- Superconducting magnet field quality, hysteresis, persistent-current decay and
  snapback, precycle and ramp-history dependence.
- Beam-mode/state-machine semantics, power converters and magnet-ramp control.
- Beam-loss monitors and dump protection, abort timing, asynchronous dumps,
  extraction/kicker transients and post-mortem records.
- Machine timing distribution, detector clock synchronization, trigger latency,
  bandwidth, dead time and logging timestamp semantics.
- Cryogenic/thermal relaxation and environmental/common-mode effects.

Record exact authors, title, year, persistent URL/identifier and supporting page
or section only after reading each source. No publication findings are asserted
by this topic list.

## Required evidence for a usable dataset

For each specific record/export, capture the persistent URL or authorized export
identifier, owner, licence/permission, retrieval date, checksum, run/fill and beam
identifiers, variable definitions, units and calibration, clock/time scale,
timestamp encoding/precision/accuracy, sampling and integration intervals,
latencies, missingness, synchronization evidence and prior machine history.
Separate command, beam-mode announcement and physical response timestamps.
Verify both-beam/bunch/interaction-point collision status independently.

Record public, authorization-required and unavailable states separately.
Unknown remains unknown. Do not infer sampling accuracy from a timestamp's number
of digits. Coarse fill summaries may support event selection but cannot support a
fast-transient endpoint. A source becomes a verified available dataset only after
an actual eligible record and its access/metadata are inspected. Until then the
inventory's `verified_available_datasets` stays empty.

## Phase 2 — attribution and direct verification

On 2026-10-10 the task owner reported independent verification of:

| Supplied CERN URL | Task-owner-reported finding | Local verification |
| --- | --- | --- |
| https://lpc.web.cern.ch/ | CERN provides public LHC programme and fill information. | `web_fetch` failed hostname lookup; direct curl GET failed with exit 6 and HTTP 000. No content retrieved. |
| https://nxcals-docs.web.cern.ch/current/user-guide/data-access/nxcals-access-request/ | Detailed NXCALS data access requires authorization. | Same DNS failure; exact policy, eligibility and request procedure not inspected. Do not access logged data without authorization. |
| https://home.cern/accelerator-report-10-000-lhc-fills/ | LHC fills include non-collision machine cycles that may provide controls. | Same DNS failure; no specific fill ID, chronology or measurement retrieved. |

These findings are attributed to the task owner, not independently confirmed by
this session. They justify follow-up but not invented data rows, citations to
unread article text, or assumed timestamp accuracy. The Phase 1 ledger above is
retained as a historical access-attempt record. DNS failures cannot establish
global unavailability. No search proxy, restricted credentials or paid API was
used to circumvent access.

## Candidate fills and downloadable measurements

**Selected fills: none. Exact downloadable measurements: none verified.**
The article URL's “10 000” is not used as a verified fill identifier. The supplied
findings contain no individual fill records, transition timestamps or downloads.
Public programme/fill information is reported available, but its precise fields,
download formats, historical coverage and clocks remain uninspected. No public
measurement is currently demonstrated to align to any transition.

Once records are accessible, select a documented physics fill containing
injection, ramp, stable-beam entry and dump, and a history/configuration-matched
non-colliding fill. Record permanent fill URLs and event times before selecting
analysis windows. Non-collision controls require verified bunch and
interaction-point status; no stable-beam interval alone does not prove no
collisions. A fill summary is contextual metadata, not synchronized sensor data.

## Prioritized measurement feasibility checklist

The following are **requested observables**, not verified CERN channel names,
units or sampling rates. Exact variable identifiers and metadata must come from
CERN. Physical unit examples specify desired dimensions only.

| Priority / transition | Independent marker and physical measurements requested | Alignment and instrumental limitations to resolve |
| --- | --- | --- |
| 1 — injection | Injection command/event and beam-mode marker separately; both-beam intensity, energy, magnet current/field and losses | Injection pulses may be shorter than logging integration; distinguish actuator time, acquisition time and published mode time. |
| 2 — acceleration ramp | Ramp command, current setpoint/readback, independent field if available, beam energy, intensity/losses, temperature | Ramp/history-dependent hysteresis and persistent currents, dwell/precycle, converter filtering and current-versus-field lag. |
| 3 — stable-beam entry | Mode declaration, adjustment history, energy/intensity, orbit/optics indicators, interaction-point collision status and luminosity if available | Administrative mode declaration is not a unique physical switch; detector clocks, latency/dead time and gain/configuration changes. |
| 4 — beam dump | Dump request/cause, actual extraction marker, kicker response, intensity drop and loss-monitor measurements | Protection versus planned dumps, hardware versus logging clocks, clipping/integration and post-mortem retention/access. |

For every row: actual sampling rate or irregular acquisition schedule, integration
duration, physical unit, timestamp precision, timestamp accuracy, clock/time scale,
cross-channel synchronization, latency and bandwidth are **unknown** here.
Do not substitute assumed 1 Hz logging or nanosecond accuracy. No adapter is
implemented because no genuine synchronized source schema or payload is verified.
The existing normalized CSV scaffold is not a CERN ingestion adapter.

## CERN data-access request — draft, NOT SENT

**Intended route:** first inspect the supplied NXCALS access-request documentation
from a reachable environment; use only the contact/process it actually specifies.
No recipient, eligibility, account or approved authorization is assumed.

**Subject:** Read-only historical LHC transition export and timing metadata for
an independent observational research feasibility study.

We seek to determine whether ordinary accelerator and instrument models account
for repeatable transition responses. We make no claim of GV detection or new
physics and request no machine operation or intervention.

Please first advise whether an existing public, licensed synchronized export can
meet the requirements below. Otherwise, please describe eligibility, approval
and permitted sharing for a minimal read-only historical export; we will not
query restricted systems before authorization.

1. **Pilot selection:** please identify one archived physics fill with documented
   injection, ramp, stable-beam entry and dump, plus one comparable non-collision
   cycle with verified collision status. Provide fill IDs, persistent references,
   dates/time scale, machine configuration, both-beam IDs and dump reasons.
   No specific fill numbers or dates are presently verified; CERN confirmation is
   required to define the actual query bounds.
2. **Time coverage:** request the complete selected cycles, including the
   immediately preceding precycle/current path and injection dwell, and at least
   30 minutes following dump if retained. Extend preceding history if needed for
   hysteresis, persistent-current decay or thermal relaxation. This is a pilot
   request bound, not a preregistered endpoint. Please state coverage/retention
   limits and any necessary reduction.
3. **Independent event records:** injection and ramp commands, mode changes,
   stable-beam declaration and dump request/cause versus actual hardware response.
   State which markers are unavailable and what each timestamp actually means.
4. **Synchronized channels:** native-resolution current setpoint/readback and
   field if independently measured; beam energy, both-beam intensity, losses,
   thermal/cryogenic readings and independent clock/reference channels; collision
   status per interaction point, and luminosity/orbit/optics where available.
   Please supply actual variable identifiers, source devices and definitions;
   do not replace unmeasured field with current without labeling the inference.
5. **Units and timing:** export values with physical units (e.g. current in A,
   field in T, temperature in K, with energy/intensity/loss units explicitly
   defined by the source). Supply actual cadence, integration windows, native
   timestamp precision, accuracy, clock/time scale and conversion, offsets/drift,
   per-channel latency/bandwidth and synchronization evidence. Native-resolution
   exports without resampling are preferred; no universal cadence is assumed.
6. **Instrument/history metadata:** calibration/gain/configuration versions,
   uncertainties, clipping/saturation/dead time, missingness and quality flags,
   preceding ramps/dumps/resets, injection dwell and environmental history.
   Describe whether dump post-mortem or fast timing records need separate approval.
7. **Delivery/provenance:** a documented CSV/JSON or other existing export with
   immutable source/export identifiers, query intervals, retrieval time, row
   counts and checksums. State licence, attribution, permitted publication and
   redistribution, access restrictions and anonymization/redaction requirements.
   We will preserve raw files unchanged and keep restricted data out of git.

If the pilot is feasible, additional independent fills for training, confirmation
and replication will be selected prospectively after power/timing qualification.
Two pilot fills alone cannot demonstrate reproducibility. Please explicitly
identify unavailable channels and whether logging is adequate for fast
transients; a coarse export would permit only a slower endpoint or an
inconclusive feasibility result.
