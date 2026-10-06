import copy
import json
from pathlib import Path
import sys

import numpy as np
import pytest

from src.gv_physical_program import (
    CHANNELS, CLASSIFICATIONS, DATA_SCHEMA, TIMES, acquire_physical, analyze_run, calibration_metadata,
    check_timing, fit_model, load_raw, lock_threshold, manifest, mock_run,
    peak, proportion_interval, sample_fingerprint, save_raw, sealed, simple_scores, summarize_results, validate_dataset, write_json_new,
)


def valid_fixture():
    public, _ = manifest("engineering", 7)
    event = public["assignments"][0]
    metadata = {
        "schema_version": "1.0", "experiment_id": "GV-PHY-001",
        "run_id": event["run_id"], "timestamp_utc": "2026-10-05T00:00:00Z",
        "origin": "synthetic", "blind_label": event["blind_label"],
        "event_type": "WITHHELD", "clock": {"id": "MOCK-CLOCK", "sample_rate_hz": 20000,
        "trigger_index": 4000, "uncertainty_s": 0.00005, "software_time_authoritative": False},
        "calibrations": calibration_metadata(), "hardware_configuration": "MOCK-FIXTURE",
        "environment": {"room_temperature_degC": 20.0}, "operator_notes": "MOCK ONLY",
        "validity_flags": [], "manifest_sha256": "0" * 64,
    }
    samples = {channel: np.zeros_like(TIMES) for channel in CHANNELS}
    samples["sample_index"] = np.arange(len(TIMES))
    return metadata, samples


def test_manifest_deterministic_and_blinded():
    public, private = manifest("evaluation", 42)
    assert (public, private) == manifest("evaluation", 42)
    assert len(public["assignments"]) == 140
    assert len({row["run_id"] for row in public["assignments"]}) == 140
    assert all(row["event_type"] == "WITHHELD" and "arm" not in row for row in public["assignments"])
    assert {row["arm"] for row in private["assignments"]} >= {"active", "sham", "idle"}
    assert public != manifest("evaluation", 43)[0]


def test_schema_accepts_complete_mock_record():
    validate_dataset(*valid_fixture())


@pytest.mark.parametrize("defect", ["clock", "software", "units", "gain", "missing", "nan", "clipping", "indices", "physical"])
def test_invalid_metadata_and_samples_rejected(defect):
    metadata, samples = valid_fixture()
    if defect == "clock": metadata["clock"]["uncertainty_s"] = 0.001
    elif defect == "software": metadata["clock"]["software_time_authoritative"] = True
    elif defect == "units": metadata["calibrations"]["magnetic"]["units"] = "V"
    elif defect == "gain": metadata["calibrations"]["magnetic"]["gain"] = 0
    elif defect == "missing": del samples["acoustic"]
    elif defect == "nan": samples["acoustic"][0] = np.nan
    elif defect == "clipping": samples["acoustic"][0] = 100
    elif defect == "indices": samples["sample_index"][2] = 1
    else: metadata["origin"] = "physical"
    with pytest.raises(ValueError): validate_dataset(metadata, samples)


def test_exclusive_json_write(tmp_path: Path):
    path = tmp_path / "manifest.json"
    digest = write_json_new(path, {"value": 1})
    assert len(digest) == 64
    with pytest.raises(FileExistsError): write_json_new(path, {"value": 2})
    assert '"value": 1' in path.read_text()


def test_raw_files_are_exclusive_and_tamper_checked(tmp_path):
    metadata, samples = valid_fixture()
    directory = tmp_path / "raw"
    save_raw(directory, metadata, samples)
    assert load_raw(directory)[0] == metadata
    with pytest.raises(FileExistsError): save_raw(directory, metadata, samples)
    (directory / "metadata.json").write_text("{}")
    with pytest.raises(ValueError, match="modified"): load_raw(directory)


def test_invalid_raw_is_retained_but_not_analyzed_as_valid(tmp_path):
    metadata, samples = valid_fixture()
    samples["acoustic"][0] = np.nan
    directory = tmp_path / "invalid"
    save_raw(directory, metadata, samples)
    assert (directory / "samples.npz").is_file()
    with pytest.raises(ValueError): load_raw(directory)


def test_intervals_and_missing_events():
    result = proportion_interval(0, 120)
    assert result["rate"] == 0 and 0 < result["interval"][1] < 0.04
    assert proportion_interval(0, 0)["rate"] is None
    assert proportion_interval(0, 0)["interval"] == [None, None]


def test_no_physical_acquisition_driver():
    with pytest.raises(NotImplementedError): acquire_physical()


def test_end_to_end_synthetic_only(tmp_path, monkeypatch):
    from scripts.gv_phy_001 import dry_run, main

    summary = dry_run(tmp_path / "dry", 42)
    assert len(summary["pipeline_checks"]) == 12
    assert all(row["passed"] for row in summary["pipeline_checks"])
    assert summary["physical_evidence"] is False
    assert summary["status"] == "INVALID / INCONCLUSIVE"
    assert "NOT GV EVIDENCE" in summary["warning"]
    assert summary["model_calibration_count"] == summary["threshold_calibration_count"] == 300
    directory = tmp_path / "dry"
    hidden_key = tmp_path / "operator-only.json"
    (directory / "operator_key.json").rename(hidden_key)
    arguments = ["gv_phy_001", "score", "--manifest", str(directory / "manifest.json"),
                 "--model", str(directory / "model.json"), "--threshold", str(directory / "threshold.json"),
                 "--lock", str(directory / "analysis_lock.json"),
                 "--raw-root", str(directory / "raw"), "--out", str(directory / "blind.json")]
    monkeypatch.setattr(sys, "argv", arguments)
    main()
    analyzed = json.loads((directory / "blind.json").read_text())
    assert len(analyzed["results"]) == 12
    assert all(row["classification"] in CLASSIFICATIONS for row in analyzed["results"])
    assert all(row["physical_evidence"] is False for row in analyzed["results"])
    assert sum(not row["valid"] for row in analyzed["results"]) == 2
    monkeypatch.setattr(sys, "argv", ["gv_phy_001", "summarize", "--analysis", str(directory / "blind.json"),
                        "--operator-key", str(hidden_key), "--out", str(directory / "unblind.json")])
    main()
    assert json.loads((directory / "unblind.json").read_text())["physical_evidence"] is False
    threshold_path = directory / "threshold.json"
    saved = json.loads(threshold_path.read_text())
    saved["value"] += 1
    threshold_path.write_text(json.dumps(sealed(saved)))
    monkeypatch.setattr(sys, "argv", arguments[:-1] + [str(directory / "mutated.json")])
    with pytest.raises(ValueError, match="lock"):
        main()


@pytest.fixture(scope="module")
def locked_mock():
    from scripts.gv_phy_001 import calibration_records

    model = fit_model(calibration_records("model_calibration", 44,
                      ["null", "em", "vibration", "acoustic", "overlap", "environmental"]))
    threshold = lock_threshold(calibration_records("threshold_calibration", 45, ["sham"]), model)
    return model, threshold


def test_model_threshold_and_evaluation_splits_are_disjoint(locked_mock):
    model, threshold = locked_mock
    assert not set(model["training_ids"]) & set(threshold["calibration_ids"])
    public, _ = manifest("model_calibration", 44)
    record = mock_run(public["assignments"][0], "null", 1)
    with pytest.raises(ValueError, match="leakage"): analyze_run(*record, model, threshold)
    with pytest.raises(ValueError, match="leakage"): lock_threshold([record], model)


def test_insufficient_calibration_rejected():
    public, _ = manifest("engineering", 1)
    with pytest.raises(ValueError, match="240"):
        fit_model([mock_run(public["assignments"][0], "null", 1)])


@pytest.mark.parametrize("scenario,expected", [("null", True), ("timing", False), ("software", True)])
def test_hardware_trigger_timing_check(scenario, expected):
    public, _ = manifest("engineering", 2)
    _, samples = mock_run(public["assignments"][0], scenario, 1)
    assert check_timing(samples) is expected


def test_slow_temperature_latency_is_not_fast_channel_timing():
    metadata, samples = valid_fixture()
    metadata["calibrations"]["temperature"]["latency_uncertainty_s"] = 0.2
    validate_dataset(metadata, samples)
    metadata["calibrations"]["acoustic"]["latency_uncertainty_s"] = 0.2
    with pytest.raises(ValueError, match="latency"): validate_dataset(metadata, samples)


def test_private_em_subconditions_balanced():
    _, private = manifest("evaluation", 55)
    variants = [row["variant"] for row in private["assignments"] if row["arm"] == "shielded"]
    assert variants.count("shielding") == variants.count("distance") == 5


@pytest.mark.parametrize("defect", ["timestamp", "hash", "range", "calibration_kind", "integer_index"])
def test_additional_schema_guards(defect):
    metadata, samples = valid_fixture()
    if defect == "timestamp": metadata["timestamp_utc"] = "2026-10-05"
    elif defect == "hash": metadata["manifest_sha256"] = "unknown"
    elif defect == "range": metadata["calibrations"]["magnetic"]["range_max"] = -100
    elif defect == "calibration_kind": metadata["calibrations"]["magnetic"]["kind"] = "physical"
    else: samples["sample_index"] = samples["sample_index"].astype(float)
    with pytest.raises(ValueError): validate_dataset(metadata, samples)


def test_mock_endpoint_success_never_becomes_physical_evidence():
    private, results = {"assignments": []}, []
    active_hits = 0
    for block in range(5):
        _, key = manifest("evaluation", 72, block)
        private["assignments"].extend(key["assignments"])
        for row in key["assignments"]:
            hit = row["arm"] == "active" and active_hits < 60
            if hit: active_hits += 1
            results.append({"run_id": row["run_id"], "origin": "synthetic",
                            "valid": True, "residual_flag": hit})
    summary = summarize_results(results, private)
    assert summary["screening_endpoint_met"] is True
    assert summary["frozen_endpoint_met"] is False and summary["null_result_valid"] is False
    assert summary["physical_evidence"] is False and summary["status"] == "INVALID / INCONCLUSIVE"
    for row in private["assignments"]:
        if row["arm"] == "shielded": row["variant"] = "distance"
    assert summarize_results(results, private)["screening_endpoint_met"] is False
    with pytest.raises(ValueError): summarize_results(results[:-1], private)
    for result in results: result["origin"] = "physical"
    with pytest.raises(NotImplementedError): summarize_results(results, private)


def test_machine_contract_matches_sample_grid():
    assert DATA_SCHEMA["sample_count"] == len(TIMES) == 10000
    assert DATA_SCHEMA["trigger_index"] == 4000
    assert DATA_SCHEMA["sample_rate_hz"] == 20000


def test_physical_tag_cannot_promote_single_trace(locked_mock):
    model, threshold = copy.deepcopy(locked_mock)
    public, _ = manifest("engineering", 999)
    metadata, samples = mock_run(public["assignments"][0], "unknown", 77)
    metadata.update(origin="physical", hardware_configuration="TEST-FIXTURE", operator_notes="Constructed unit-test data, not measurements")
    metadata["clock"]["id"] = "TEST-CLOCK"
    for calibration in metadata["calibrations"].values():
        calibration.update(kind="physical", version="TEST-VERSION")
    model["origin"] = threshold["origin"] = "physical"
    model = sealed(model)
    threshold["model_sha256"] = model["sha256"]
    threshold = sealed(threshold)
    result = analyze_run(metadata, samples, model, threshold)
    assert result["classification"] == "UNATTRIBUTED RESIDUAL - REQUIRES CONTROLS"
    assert result["physical_evidence"] is False
    assert result["valid"] is False and result["physical_assay_certified"] is False


def test_latency_correction_changes_feature_time_not_raw_samples():
    values = np.exp(-0.5 * ((TIMES - 0.017) / 0.001)**2)
    saved = values.copy()
    _, _, corrected_time = peak(values, 0.005)
    assert corrected_time == pytest.approx(0.012, abs=1e-10)
    assert np.array_equal(values, saved)


@pytest.mark.parametrize("defect", ["infinite_threshold", "nan_threshold", "negative_threshold", "nan_model", "zero_scale"])
def test_invalid_frozen_analysis_cannot_create_a_null(locked_mock, defect):
    model, threshold = copy.deepcopy(locked_mock)
    public, _ = manifest("engineering", 1001)
    metadata, samples = mock_run(public["assignments"][0], "unknown", 88)
    if defect == "infinite_threshold": threshold["value"] = float("inf")
    elif defect == "nan_threshold": threshold["value"] = float("nan")
    elif defect == "negative_threshold": threshold["value"] = -1.0
    elif defect == "nan_model": model["weights"][0][0] = float("nan")
    else: model["scales"][0] = 0.0
    with pytest.raises(ValueError):
        analyze_run(metadata, samples, model, threshold)


def test_finite_threshold_mutation_rejected(locked_mock):
    model, threshold = copy.deepcopy(locked_mock)
    public, _ = manifest("engineering", 1002)
    threshold["value"] += 0.1
    with pytest.raises(ValueError, match="mutation"):
        analyze_run(*mock_run(public["assignments"][0], "null", 1), model, threshold)


def test_baselines_choose_their_own_channels_not_residual_channels():
    from src.gv_physical_program import TARGETS

    rng = np.random.default_rng(82)
    samples = {channel: rng.normal(0, 0.001, len(TIMES)) for channel in CHANNELS}
    for channel, amplitude, time in zip(TARGETS, [10, 9, 1], [0.01, 0.01, 0.04]):
        samples[channel] += amplitude * np.exp(-0.5 * ((TIMES - time) / 0.001)**2)
    _, _, peak_coherent, rms_coherent = simple_scores(samples)
    assert peak_coherent is True and rms_coherent is True


def evaluation_fixture():
    private, results = {"assignments": []}, []
    for block in range(5):
        _, key = manifest("evaluation", 92, block)
        private["assignments"].extend(key["assignments"])
        for row in key["assignments"]:
            results.append({"run_id": row["run_id"], "origin": "synthetic", "valid": True,
                            "residual_flag": row["arm"] == "active"})
    return private, results


@pytest.mark.parametrize("defect", ["active_count", "sham_count", "control_count", "control_hits", "sham_hits", "duplicate_key", "missing_raw"])
def test_counts_controls_and_invalid_events_cannot_bypass_endpoint(defect):
    private, results = evaluation_fixture()
    assignments = {row["run_id"]: row["arm"] for row in private["assignments"]}
    arm = {"active_count": "active", "sham_count": "sham", "control_count": "idle",
           "control_hits": "idle", "sham_hits": "sham"}.get(defect)
    if defect == "duplicate_key":
        private["assignments"].append(copy.deepcopy(private["assignments"][0]))
        with pytest.raises(ValueError, match="Duplicate"): summarize_results(results, private)
        return
    if defect == "missing_raw":
        with pytest.raises(ValueError, match="every manifest"): summarize_results(results[:-1], private)
        return
    affected = [row for row in results if assignments[row["run_id"]] == arm]
    if defect.endswith("count"):
        for row in affected[:31 if arm in {"active", "sham"} else 6]: row["valid"] = False
    else:
        for row in affected[:3 if arm == "idle" else 30]: row["residual_flag"] = True
    summary = summarize_results(results, private)
    assert summary["screening_endpoint_met"] is False
    assert summary["null_result_valid"] is False and summary["physical_evidence"] is False


def test_missing_events_do_not_support_a_null_over_all_attempts():
    private, results = evaluation_fixture()
    assignments = {row["run_id"]: row["arm"] for row in private["assignments"]}
    active = [row for row in results if assignments[row["run_id"]] == "active"]
    for row in active: row["residual_flag"] = False
    for row in active[:30]: row["valid"] = False
    summary = summarize_results(results, private)
    assert summary["groups"]["active"]["rate"] == 0
    assert summary["groups"]["active"]["missing_worst_case_interval"][1] > 0.20
    assert summary["null_result_valid"] is False


def test_private_key_is_private_at_creation(tmp_path):
    path = tmp_path / "operator-key.json"
    write_json_new(path, {"seed": 7}, private=True)
    assert path.stat().st_mode & 0o777 == 0o600


def test_public_manifest_does_not_contain_arm_variant_or_seed():
    public, _ = manifest("evaluation", 1003)
    text = json.dumps(public)
    assert all(f'"{key}"' not in text for key in ["seed", "arm", "variant"])


def test_mock_unknown_can_be_ordinary_unmeasured_common_mode(locked_mock):
    model, threshold = locked_mock
    public, _ = manifest("engineering", 1004)
    metadata, samples = mock_run(public["assignments"][0], "null", 93)
    pulse = np.exp(-0.5 * ((TIMES - 0.012) / 0.002)**2)
    for channel, amplitude in [("magnetic", 0.5), ("acceleration", 0.5), ("acoustic", 0.005)]:
        samples[channel] += amplitude * pulse
    result = analyze_run(metadata, samples, model, threshold)
    assert result["residual_flag"] is True
    assert result["physical_evidence"] is False


def test_model_arithmetic_overflow_is_invalid_not_a_null(locked_mock):
    model, threshold = copy.deepcopy(locked_mock)
    model["weights"] = (np.ones((7, 3)) * 1e308).tolist()
    model = sealed(model)
    threshold["model_sha256"] = model["sha256"]
    threshold = sealed(threshold)
    public, _ = manifest("engineering", 1005)
    with pytest.raises(ValueError, match="arithmetic"):
        analyze_run(*mock_run(public["assignments"][0], "unknown", 94), model, threshold)


def test_unblinded_event_label_rejected():
    metadata, samples = valid_fixture()
    metadata["blind_label"] = "active"
    with pytest.raises(ValueError, match="Unblinded"):
        validate_dataset(metadata, samples)


def test_timing_budget_rejects_20us_per_sensor():
    metadata, samples = valid_fixture()
    metadata["calibrations"]["acoustic"]["latency_uncertainty_s"] = 0.00002
    with pytest.raises(ValueError, match="latency"):
        validate_dataset(metadata, samples)


def test_string_validity_flag_cannot_bypass_counts():
    private, results = evaluation_fixture()
    results[0]["valid"] = "false"
    with pytest.raises(ValueError, match="booleans"):
        summarize_results(results, private)


def test_mock_calibration_stages_have_no_reused_sample_streams(locked_mock):
    model, threshold = locked_mock
    assert not set(model["training_fingerprints"]) & set(threshold["calibration_fingerprints"])


def test_changed_uuid_does_not_hide_copied_calibration_data(locked_mock):
    from scripts.gv_phy_001 import calibration_records

    model, threshold = locked_mock
    metadata, samples = next(calibration_records("model_calibration", 44,
                              ["null", "em", "vibration", "acoustic", "overlap", "environmental"]))
    metadata["run_id"] = manifest("engineering", 2001)[0]["assignments"][0]["run_id"]
    assert sample_fingerprint(samples) in model["training_fingerprints"]
    with pytest.raises(ValueError, match="Content-level"):
        analyze_run(metadata, samples, model, threshold)
    with pytest.raises(ValueError, match="Content-level"):
        lock_threshold([(metadata, samples)], model)