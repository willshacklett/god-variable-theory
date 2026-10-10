# CERN source discovery and access ledger

Checked 2026-10-10 UTC. **No source content or available dataset was verified.**
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
