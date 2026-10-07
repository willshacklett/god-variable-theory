import hashlib
import json
from pathlib import Path
import sys

import pytest

from src.gv_physical_acquisition import (
    HARDWARE_SCHEMA, PREREGISTRATION, MockAcquisition, UnsupportedPhysicalAcquisition,
    capture_to_raw, seal_configuration, validate_configuration, validate_raw_binding,
)
from src.gv_physical_program import CHANNELS, load_raw, manifest, mock_run


def configuration_fixture():
    channels, diagnostics, registry = {}, {}, {}
    for index, (name, units) in enumerate([*CHANNELS.items(), ("electric_reference", "V"), ("rf_envelope_reference", "V")]):
        version, sensor = f"CAL-test-{name}", f"TEST-CHAIN-{name}"
        record = {"sensor_id": sensor, "calibration_version": version, "adc_input": index,
                  "units": units, "sample_rate_hz": 20000, "clock_id": "TEST-CLOCK",
                  "role": "core" if name in CHANNELS else "diagnostic"}
        (channels if name in CHANNELS else diagnostics)[name] = record
        registry[version] = {"sensor_id": sensor, "kind": "synthetic", "valid_from": "2026-10-01T00:00:00Z",
                             "valid_until": "2026-11-01T00:00:00Z", "artifact_sha256": "0" * 64}
    config = {
        "schema_version": "1.0", "experiment_id": "GV-PHY-001", "origin": "synthetic",
        "apparatus_id": "TEST-ONLY", "relay_specification_id": "CLASS-NOT-PRODUCT",
        "driver_configuration": {"specification_id": "CLASS-NOT-CIRCUIT", "logic_voltage_v": 3.3,
                                 "flyback_protection": True, "physical_operational": False},
        "power_configuration": {"coil_voltage_v": 5, "coil_current_limit_a": 0.1, "load_voltage_v": 5,
                                "load_current_limit_a": 0.005, "sensor_voltage_v": 5, "isolated_load": True,
                                "current_limited": True, "fused": True, "no_mains": True},
        "daq_configuration": {"specification_id": "TEST-DAQ", "clock_id": "TEST-CLOCK", "sample_rate_hz": 20000,
                              "sample_count": 10000, "trigger_index": 4000, "analog_input_count": 16,
                              "common_clock": True, "timing_uncertainty_s": 0.0001},
        "channel_map_version": HARDWARE_SCHEMA["channel_map_version"], "channels": channels,
        "diagnostics": diagnostics, "fixture_version": "TEST-FIXTURE-1", "cable_configuration": "TEST-CABLE-1",
        "shielding_configuration": "TEST-SHIELD-1", "software_commit_sha": "0" * 40,
        "preregistration_version": HARDWARE_SCHEMA["preregistration_version"],
        "preregistration_sha256": hashlib.sha256(PREREGISTRATION.read_bytes()).hexdigest(),
        "operator": "UNIT-TEST-NOT-OPERATOR", "timestamp_utc": "2026-10-06T00:00:00Z",
    }
    return seal_configuration(config), registry


def test_hardware_schema_and_hash():
    config, registry = configuration_fixture()
    validate_configuration(config, registry)
    assert len(config["configuration_hash"]) == 64


@pytest.mark.parametrize("defect", ["duplicate_sensor", "bad_calibration", "sample_rate", "no_timing", "missing_channel",
                                    "different_clock", "unsafe_voltage", "unsafe_current", "physical_driver",
                                    "stale_calibration", "preregistration", "hash", "missing_rf"])
def test_invalid_hardware_configuration_rejected(defect):
    config, registry = configuration_fixture()
    if defect == "duplicate_sensor": config["channels"]["magnetic"]["sensor_id"] = config["channels"]["acoustic"]["sensor_id"]
    elif defect == "bad_calibration": config["channels"]["magnetic"]["calibration_version"] = "unknown"
    elif defect == "sample_rate": config["daq_configuration"]["sample_rate_hz"] = 1000
    elif defect == "no_timing": del config["channels"]["timing_reference"]
    elif defect == "missing_channel": del config["channels"]["current"]
    elif defect == "different_clock": config["channels"]["magnetic"]["clock_id"] = "USB-CLOCK"
    elif defect == "unsafe_voltage": config["power_configuration"]["coil_voltage_v"] = 120
    elif defect == "unsafe_current": config["power_configuration"]["load_current_limit_a"] = 1
    elif defect == "physical_driver": config["driver_configuration"]["physical_operational"] = True
    elif defect == "stale_calibration": registry[config["channels"]["current"]["calibration_version"]]["valid_until"] = "2026-10-01T00:00:00Z"
    elif defect == "preregistration": config["preregistration_version"] = "changed"
    elif defect == "missing_rf": del config["diagnostics"]["rf_envelope_reference"]
    if defect != "hash": config = seal_configuration(config)
    else: config["fixture_version"] = "mutated"
    with pytest.raises(ValueError): validate_configuration(config, registry)


def replay_fixture():
    config, registry = configuration_fixture()
    event = manifest("engineering", 123)[0]["assignments"][0]
    metadata, samples = mock_run(event, "null", 456)
    metadata["hardware_configuration"] = config["configuration_hash"]
    metadata["clock"]["id"] = config["daq_configuration"]["clock_id"]
    for name in CHANNELS:
        metadata["calibrations"][name]["version"] = config["channels"][name]["calibration_version"]
    metadata["timestamp_utc"] = "2026-10-06T00:00:00Z"
    return config, registry, event, metadata, samples


def test_mock_acquisition_is_replay_not_a_physical_driver(tmp_path):
    config, registry, event, metadata, samples = replay_fixture()
    result = capture_to_raw(MockAcquisition(metadata, samples), config, registry, event, tmp_path / "unit-raw")
    assert result["format_valid"] is True
    assert result["physical_evidence"] is False and result["physical_assay_certified"] is False
    assert load_raw(tmp_path / "unit-raw")[0]["hardware_configuration"] == config["configuration_hash"]
    with pytest.raises(FileExistsError):
        capture_to_raw(MockAcquisition(metadata, samples), config, registry, event, tmp_path / "unit-raw")


@pytest.mark.parametrize("defect", ["raw_hash", "raw_version", "raw_clock", "capture_expired", "physical_origin"])
def test_raw_binding_rejects_mismatch(defect):
    config, registry, _, metadata, _ = replay_fixture()
    if defect == "raw_hash": metadata["hardware_configuration"] = "f" * 64
    elif defect == "raw_version": metadata["calibrations"]["magnetic"]["version"] = "CAL-old"
    elif defect == "raw_clock": metadata["clock"]["id"] = "USB-TIME"
    elif defect == "capture_expired": metadata["timestamp_utc"] = "2026-12-01T00:00:00Z"
    else: metadata["origin"] = "physical"
    with pytest.raises(ValueError): validate_raw_binding(metadata, config, registry)


def test_non_operational_physical_interface(tmp_path):
    device = UnsupportedPhysicalAcquisition()
    with pytest.raises(NotImplementedError): device.initialize()
    config, registry = configuration_fixture()
    with pytest.raises(NotImplementedError): capture_to_raw(device, config, registry, {}, tmp_path / "forbidden")
    assert not (tmp_path / "forbidden").exists()


def test_state_sequence_and_abort(tmp_path):
    config, registry, event, metadata, samples = replay_fixture()
    device = MockAcquisition(metadata, samples)
    with pytest.raises(ValueError): device.capture()
    event["blind_label"] = "B-" + "0" * 24
    with pytest.raises(ValueError): capture_to_raw(device, config, registry, event, tmp_path / "rejected")
    assert device.state == "aborted" and not (tmp_path / "rejected").exists()


def test_invalid_captured_raw_is_retained_not_deleted(tmp_path):
    config, registry, event, metadata, samples = replay_fixture()
    samples["acoustic"][0] = float("nan")
    result = capture_to_raw(MockAcquisition(metadata, samples), config, registry, event, tmp_path / "invalid")
    assert result["format_valid"] is False and result["status"] == "INVALID / INCONCLUSIVE"
    assert (tmp_path / "invalid" / "samples.npz").exists()


def test_validation_cli_cannot_promote_design(tmp_path, monkeypatch, capsys):
    from scripts.gv_phy_001 import main

    config, registry = configuration_fixture()
    (tmp_path / "configuration.json").write_text(json.dumps(config))
    (tmp_path / "calibrations.json").write_text(json.dumps(registry))
    monkeypatch.setattr(sys, "argv", ["gv_phy_001", "validate-hardware", "--configuration",
                        str(tmp_path / "configuration.json"), "--calibration-registry", str(tmp_path / "calibrations.json")])
    main()
    assert "PENDING; no physical driver or certification" in capsys.readouterr().out


def test_duplicate_sensor_identity_is_rejected_even_with_matching_registry():
    config, registry = configuration_fixture()
    config["channels"]["magnetic"]["sensor_id"] = config["channels"]["acoustic"]["sensor_id"]
    registry[config["channels"]["magnetic"]["calibration_version"]]["sensor_id"] = config["channels"]["magnetic"]["sensor_id"]
    with pytest.raises(ValueError, match="Duplicate"):
        validate_configuration(seal_configuration(config), registry)


@pytest.mark.parametrize("defect", ["wrong_units", "duplicate_adc", "stale_prereg_hash", "unsafe_sensor_supply", "lost_isolation", "missing_clamp"])
def test_additional_design_safety_and_binding_guards(defect):
    config, registry = configuration_fixture()
    if defect == "wrong_units": config["channels"]["current"]["units"] = "V"
    elif defect == "duplicate_adc": config["channels"]["magnetic"]["adc_input"] = 0
    elif defect == "stale_prereg_hash": config["preregistration_sha256"] = "f" * 64
    elif defect == "unsafe_sensor_supply": config["power_configuration"]["sensor_voltage_v"] = 12
    elif defect == "lost_isolation": config["power_configuration"]["isolated_load"] = False
    else: config["driver_configuration"]["flyback_protection"] = False
    with pytest.raises(ValueError): validate_configuration(seal_configuration(config), registry)