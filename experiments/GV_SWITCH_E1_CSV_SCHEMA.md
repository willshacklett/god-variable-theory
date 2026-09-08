# GV Switch E1 Calibration CSV Schema

Prototype: **E1**

Purpose:

Define the minimum tabular record required for electrical transient sensor calibration.

Each row represents one trial.

Required columns:

| Column | Meaning |
|---|---|
| trial_id | unique trial identifier |
| active_or_sham | active or sham |
| trigger_time_ns | trigger reference time |
| sensor_time_ns | detected sensor event time |
| sensor_peak_v | peak sensor voltage |
| sensor_rms_v | RMS sensor voltage |
| threshold_v | frozen detection threshold |
| source_state | source condition |
| source_level | source intensity setting |
| sensor_distance_m | physical sensor distance |
| sensor_orientation_deg | sensor orientation |
| shielding_state | shielding condition |
| cable_id | cable identity |
| scope_channel | acquisition channel |
| apparatus_config_id | hardware configuration identifier |
| git_commit_sha | software version used |

A blank `sensor_time_ns` means no detected event.

Synthetic demonstration files must be clearly marked and must never be represented as hardware results.
