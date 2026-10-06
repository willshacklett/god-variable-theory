from __future__ import annotations

from abc import ABC, abstractmethod
import copy
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import re

from src.gv_physical_program import CHANNELS, EXPERIMENT_ID, RATE_HZ, save_raw, validate_dataset


ROOT = Path(__file__).resolve().parents[1]
HARDWARE_SCHEMA = json.loads((ROOT / "experiments/gv_phy_001_hardware_schema.json").read_text())
PREREGISTRATION = ROOT / "experiments/GV_PHY_001_PREREGISTRATION.md"


def configuration_hash(configuration: dict) -> str:
    content = {key: value for key, value in configuration.items() if key != "configuration_hash"}
    return hashlib.sha256(json.dumps(content, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def seal_configuration(configuration: dict) -> dict:
    return {**configuration, "configuration_hash": configuration_hash(configuration)}


def utc_time(value: str) -> datetime:
    stamp = datetime.fromisoformat(value)
    if stamp.tzinfo is None or stamp.utcoffset().total_seconds() != 0:
        raise ValueError("UTC timestamp required")
    return stamp


def bounded(value, minimum: float, maximum: float, label: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or not minimum <= value <= maximum:
        raise ValueError(f"Unsafe/incompatible {label}")


def validate_configuration(configuration: dict, calibration_registry: dict) -> None:
    if set(configuration) != set(HARDWARE_SCHEMA["required"]):
        raise ValueError("Hardware manifest fields mismatch")
    if configuration["schema_version"] != "1.0" or configuration["experiment_id"] != EXPERIMENT_ID:
        raise ValueError("Unsupported hardware schema/experiment")
    if configuration["origin"] not in HARDWARE_SCHEMA["origins"]:
        raise ValueError("Physical acquisition/driver is unsupported")
    if configuration["configuration_hash"] != configuration_hash(configuration):
        raise ValueError("Configuration hash mismatch")
    for field in ("apparatus_id", "relay_specification_id", "fixture_version", "cable_configuration", "shielding_configuration", "operator"):
        if not isinstance(configuration[field], str) or not configuration[field].strip():
            raise ValueError("Missing configuration identifier")
    if configuration["channel_map_version"] != HARDWARE_SCHEMA["channel_map_version"]:
        raise ValueError("Stale channel map")
    if configuration["preregistration_version"] != HARDWARE_SCHEMA["preregistration_version"]:
        raise ValueError("Incorrect preregistration version")
    if configuration["preregistration_sha256"] != hashlib.sha256(PREREGISTRATION.read_bytes()).hexdigest():
        raise ValueError("Stale preregistration reference")
    if not re.fullmatch(r"[0-9a-f]{40}", configuration["software_commit_sha"]):
        raise ValueError("Invalid software commit reference")
    stamp = utc_time(configuration["timestamp_utc"])
    driver = configuration["driver_configuration"]
    if set(driver) != {"specification_id", "logic_voltage_v", "flyback_protection", "physical_operational"}:
        raise ValueError("Invalid driver configuration")
    if not driver["specification_id"] or driver["physical_operational"] is not False:
        raise ValueError("Unsupported physical-driver claim")
    bounded(driver["logic_voltage_v"], 0, 3.3, "logic voltage")
    if driver["flyback_protection"] is not True:
        raise ValueError("Flyback protection required")
    power = configuration["power_configuration"]
    if set(power) != {"coil_voltage_v", "coil_current_limit_a", "load_voltage_v", "load_current_limit_a", "sensor_voltage_v", "isolated_load", "current_limited", "fused", "no_mains"}:
        raise ValueError("Invalid power-domain metadata")
    for field, limit in [("coil_voltage_v", 5), ("coil_current_limit_a", 0.1),
                         ("load_voltage_v", 5), ("load_current_limit_a", 0.005), ("sensor_voltage_v", 5)]:
        bounded(power[field], 0, limit, field)
    if any(power[field] is not True for field in ("isolated_load", "current_limited", "fused", "no_mains")):
        raise ValueError("Required power safety strategy absent")
    daq = configuration["daq_configuration"]
    if set(daq) != {"specification_id", "clock_id", "sample_rate_hz", "sample_count", "trigger_index", "analog_input_count", "common_clock", "timing_uncertainty_s"}:
        raise ValueError("Invalid DAQ configuration")
    if daq["sample_rate_hz"] != RATE_HZ or daq["sample_count"] != 10000 or daq["trigger_index"] != 4000:
        raise ValueError("Incompatible DAQ sample grid")
    if not daq["clock_id"] or not daq["specification_id"] or daq["common_clock"] is not True or daq["analog_input_count"] < 16:
        raise ValueError("Required common-clock DAQ absent")
    bounded(daq["timing_uncertainty_s"], 0, 0.0001, "timing budget")
    channels = configuration["channels"]
    if set(channels) != set(CHANNELS):
        raise ValueError("Missing required core channel")
    diagnostics = configuration["diagnostics"]
    if set(diagnostics) != set(HARDWARE_SCHEMA["diagnostic_channels"]):
        raise ValueError("Electric/RF diagnostic plan missing")
    identifiers, inputs = [], []
    for name, channel in {**channels, **diagnostics}.items():
        if set(channel) != {"sensor_id", "calibration_version", "adc_input", "units", "sample_rate_hz", "clock_id", "role"}:
            raise ValueError("Invalid channel configuration")
        identifiers.append(channel["sensor_id"]); inputs.append(channel["adc_input"])
        if not re.fullmatch(r"CAL-[A-Za-z0-9][A-Za-z0-9_.-]*", channel["calibration_version"]):
            raise ValueError("Invalid calibration version")
        if not channel["sensor_id"] or channel["sample_rate_hz"] != RATE_HZ or channel["clock_id"] != daq["clock_id"]:
            raise ValueError("Non-common-clock or missing sensor")
        if channel["role"] != ("diagnostic" if name in diagnostics else "core"):
            raise ValueError("Diagnostic channels cannot enter core endpoint")
        if channel["units"] != CHANNELS.get(name, "V"):
            raise ValueError("Channel units mismatch")
        reference = calibration_registry.get(channel["calibration_version"])
        if not reference or set(reference) != {"sensor_id", "kind", "valid_from", "valid_until", "artifact_sha256"}:
            raise ValueError("Stale/missing calibration reference")
        if reference["sensor_id"] != channel["sensor_id"] or reference["kind"] != configuration["origin"]:
            raise ValueError("Calibration sensor/origin mismatch")
        if not utc_time(reference["valid_from"]) <= stamp <= utc_time(reference["valid_until"]):
            raise ValueError("Expired calibration reference")
        if not re.fullmatch(r"[0-9a-f]{64}", reference["artifact_sha256"]):
            raise ValueError("Missing calibration artifact hash")
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Duplicate sensor/measurement-chain IDs")
    if len(inputs) != len(set(inputs)) or any(type(index) is not int or not 0 <= index < daq["analog_input_count"] for index in inputs):
        raise ValueError("Invalid/duplicate ADC assignment")


def validate_raw_binding(metadata: dict, configuration: dict, calibration_registry: dict) -> None:
    validate_configuration(configuration, calibration_registry)
    if metadata["origin"] != "synthetic" or configuration["origin"] != "synthetic":
        raise ValueError("Physical acquisition is not implemented")
    if metadata["hardware_configuration"] != configuration["configuration_hash"]:
        raise ValueError("Raw configuration hash mismatch")
    if metadata["clock"]["id"] != configuration["daq_configuration"]["clock_id"]:
        raise ValueError("Raw/configuration clock mismatch")
    daq = configuration["daq_configuration"]
    for field in ("sample_rate_hz", "trigger_index"):
        if metadata["clock"][field] != daq[field]:
            raise ValueError("Raw/configuration sampling mismatch")
    if metadata["clock"]["uncertainty_s"] > daq["timing_uncertainty_s"]:
        raise ValueError("Raw timing exceeds configured budget")
    captured = utc_time(metadata["timestamp_utc"])
    for name, channel in configuration["channels"].items():
        if metadata["calibrations"][name]["version"] != channel["calibration_version"]:
            raise ValueError("Stale raw calibration version")
        reference = calibration_registry[channel["calibration_version"]]
        if not utc_time(reference["valid_from"]) <= captured <= utc_time(reference["valid_until"]):
            raise ValueError("Calibration expired before capture")


class AcquisitionInterface(ABC):
    backend = "unsupported"
    physical_operational = False

    @abstractmethod
    def initialize(self): ...

    @abstractmethod
    def configure_channels(self, configuration: dict): ...

    @abstractmethod
    def start_common_clock(self): ...

    @abstractmethod
    def arm_trigger(self, event: dict): ...

    @abstractmethod
    def capture(self) -> tuple[dict, dict]: ...

    @abstractmethod
    def abort(self): ...


class UnsupportedPhysicalAcquisition(AcquisitionInterface):
    def unavailable(self, *args, **kwargs):
        raise NotImplementedError("No reviewed physical driver, wiring or certified apparatus exists")

    initialize = configure_channels = start_common_clock = arm_trigger = capture = unavailable

    def abort(self):
        return None


class MockAcquisition(AcquisitionInterface):
    """Replay explicitly synthetic unit-test arrays; no hardware I/O or evidence."""

    backend = "synthetic-replay"

    def __init__(self, metadata: dict, samples: dict):
        if metadata.get("origin") != "synthetic":
            raise ValueError("Mock driver only accepts explicit synthetic arrays")
        self.metadata, self.samples = copy.deepcopy(metadata), copy.deepcopy(samples)
        self.state = "new"

    def require(self, state: str):
        if self.state != state:
            raise ValueError("Invalid acquisition state sequence")

    def initialize(self):
        self.require("new")
        self.state = "initialized"

    def configure_channels(self, configuration: dict):
        self.require("initialized")
        if self.metadata["hardware_configuration"] != configuration["configuration_hash"]:
            raise ValueError("Replay configuration mismatch")
        self.state = "configured"

    def start_common_clock(self):
        self.require("configured")
        self.state = "clock-started"

    def arm_trigger(self, event: dict):
        self.require("clock-started")
        if self.metadata["run_id"] != event["run_id"] or self.metadata["blind_label"] != event["blind_label"]:
            raise ValueError("Replay event mismatch")
        self.state = "armed"

    def capture(self):
        self.require("armed")
        self.state = "captured"
        return copy.deepcopy(self.metadata), copy.deepcopy(self.samples)

    def abort(self):
        self.state = "aborted"


def capture_to_raw(device: AcquisitionInterface, configuration: dict, calibration_registry: dict,
                   event: dict, output_directory: Path) -> dict:
    if device.backend != "synthetic-replay" or device.physical_operational is not False:
        raise NotImplementedError("Physical driver operation remains blocked")
    validate_configuration(configuration, calibration_registry)
    try:
        device.initialize()
        device.configure_channels(configuration)
        device.start_common_clock()
        device.arm_trigger(event)
        metadata, samples = device.capture()
        validate_raw_binding(metadata, configuration, calibration_registry)
        if metadata["run_id"] != event["run_id"] or metadata["blind_label"] != event["blind_label"]:
            raise ValueError("Captured event identity mismatch")
        save_raw(output_directory, metadata, samples)
        try:
            validate_dataset(metadata, samples)
            format_valid = True
        except ValueError:
            format_valid = False
        return {"origin": "synthetic", "format_valid": format_valid,
                "physical_evidence": False, "physical_assay_certified": False,
                "status": "INVALID / INCONCLUSIVE",
                "warning": "UNIT-TEST REPLAY ONLY; NO PHYSICAL ACQUISITION"}
    except Exception:
        device.abort()
        raise