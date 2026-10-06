from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import random
import re
import uuid

import numpy as np


EXPERIMENT_ID = "GV-PHY-001"
WARNING = "SYNTHETIC PIPELINE TEST - NOT GV EVIDENCE"
DATA_SCHEMA = json.loads((Path(__file__).resolve().parents[1] / "experiments/gv_phy_001_data_schema.json").read_text())
RATE_HZ = DATA_SCHEMA["sample_rate_hz"]
TIMES = np.arange(-4000, 6000) / RATE_HZ
BASELINE = (-0.18, -0.03)
EVENT = (0.0, 0.05)
CHANNELS = DATA_SCHEMA["channels"]
TARGETS = ("magnetic", "acceleration", "acoustic")
REFERENCES = ("current", "voltage", "em_reference", "mechanical_reference",
              "acoustic_reference", "environment_reference")
CONTROL_ARMS = ("idle", "disconnected", "load", "mechanical", "shielded",
                "isolated", "acoustic_isolated", "thermal")
SCENARIOS = ("timing", "electrical", "em", "vibration", "acoustic", "thermal",
             "environmental", "software", "overlap", "sham", "null", "unknown")
CLASSIFICATIONS = {
    "TIMING ARTIFACT", "ELECTRICAL TRANSIENT", "KNOWN EM", "KNOWN MECHANICAL",
    "KNOWN ACOUSTIC", "KNOWN THERMAL", "SOFTWARE ARTIFACT", "KNOWN ENVIRONMENTAL",
    "MULTIPLE KNOWN CAUSES", "NULL", "UNEXPLAINED PROPAGATION CANDIDATE",
    "INVALID ACQUISITION", "UNATTRIBUTED RESIDUAL - REQUIRES CONTROLS",
}


def write_json_new(path: Path, payload: dict) -> str:
    serialized = (json.dumps(payload, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(serialized)
    return hashlib.sha256(serialized).hexdigest()


def manifest(stage: str, seed: int, block: int = 0) -> tuple[dict, dict]:
    if stage == "engineering":
        arms = ["active", "sham", *CONTROL_ARMS] * 4
    elif stage == "model_calibration":
        arms = ["active"] * 12 + [arm for arm in CONTROL_ARMS for _ in range(6)]
    elif stage == "threshold_calibration":
        arms = ["sham"] * 60
    elif stage in {"evaluation", "replication"}:
        arms = ["active"] * 30 + ["sham"] * 30 + [arm for arm in CONTROL_ARMS for _ in range(10)]
    else:
        raise ValueError("Unknown prospective stage")
    rng = random.Random(f"{seed}:{stage}:{block}")
    rng.shuffle(arms)
    namespace = uuid.uuid5(uuid.NAMESPACE_URL, f"{EXPERIMENT_ID}:{seed}:{stage}:{block}")
    public, private = [], []
    shielded_count = 0
    for sequence, arm in enumerate(arms):
        run_id = str(uuid.uuid5(namespace, str(sequence)))
        label = f"B-{rng.getrandbits(96):024x}"
        public.append({"run_id": run_id, "sequence": sequence, "blind_label": label,
                       "event_type": "WITHHELD", "minimum_gap_s": 5.0})
        variant = "standard"
        if arm == "shielded":
            variant = "shielding" if shielded_count % 2 == 0 else "distance"
            shielded_count += 1
        private.append({"run_id": run_id, "blind_label": label, "arm": arm, "variant": variant})
    return ({"experiment_id": EXPERIMENT_ID, "stage": stage, "block": block,
             "assignments": public},
            {"experiment_id": EXPERIMENT_ID, "seed": seed, "assignments": private})


def calibration_metadata() -> dict:
    return {
        channel: {"units": units, "version": "MOCK-CAL-1", "gain": 1.0,
                  "offset": 0.0, "range_min": -100.0, "range_max": 100.0,
                  "latency_s": 0.0, "latency_uncertainty_s": 0.00002, "kind": "synthetic"}
        for channel, units in CHANNELS.items()
    }


def window(values: np.ndarray, interval: tuple[float, float], latency_s: float = 0.0) -> np.ndarray:
    corrected_times = TIMES - latency_s
    selected = (corrected_times >= interval[0]) & (corrected_times < interval[1])
    return values[selected]


def validate_dataset(metadata: dict, samples: dict[str, np.ndarray]) -> None:
    required = set(DATA_SCHEMA["metadata_required"])
    if set(metadata) != required or metadata["schema_version"] != "1.0":
        raise ValueError("Invalid metadata schema")
    if metadata["experiment_id"] != EXPERIMENT_ID or metadata["origin"] not in {"synthetic", "physical"}:
        raise ValueError("Invalid experiment or data origin")
    uuid.UUID(metadata["run_id"])
    timestamp = datetime.fromisoformat(metadata["timestamp_utc"])
    if timestamp.tzinfo is None or timestamp.utcoffset().total_seconds() != 0:
        raise ValueError("UTC audit timestamp required")
    if not re.fullmatch(r"[0-9a-f]{64}", metadata["manifest_sha256"]):
        raise ValueError("Invalid manifest digest")
    if not metadata["hardware_configuration"] or not isinstance(metadata["environment"], dict):
        raise ValueError("Hardware/environment metadata required")
    if metadata["event_type"] != "WITHHELD" or not metadata["blind_label"]:
        raise ValueError("Unblinded analysis input")
    if set(samples) != {*CHANNELS, "sample_index"}:
        raise ValueError("Missing or unexpected raw channels")
    if (samples["sample_index"].dtype.kind not in "iu"
            or not np.array_equal(samples["sample_index"], np.arange(len(TIMES)))):
        raise ValueError("Sample indices must be complete and monotonic")
    clock = metadata["clock"]
    if set(clock) != {"id", "sample_rate_hz", "trigger_index", "uncertainty_s", "software_time_authoritative"}:
        raise ValueError("Invalid common-clock metadata")
    if clock["sample_rate_hz"] != RATE_HZ or clock["trigger_index"] != 4000:
        raise ValueError("Sampling grid or trigger mismatch")
    if not clock["id"] or clock["software_time_authoritative"] is not False:
        raise ValueError("Software time cannot replace hardware timing")
    if not 0 <= clock["uncertainty_s"] <= 0.0001:
        raise ValueError("Timing uncertainty exceeds 100 us")
    if metadata["validity_flags"] or set(metadata["calibrations"]) != set(CHANNELS):
        raise ValueError("Invalid acquisition flags or calibrations")
    for channel, units in CHANNELS.items():
        calibration = metadata["calibrations"][channel]
        expected = {"units", "version", "gain", "offset", "range_min", "range_max", "latency_s", "latency_uncertainty_s", "kind"}
        if set(calibration) != expected or calibration["units"] != units or not calibration["version"]:
            raise ValueError(f"Invalid calibration for {channel}")
        numeric = [calibration[key] for key in ("gain", "offset", "range_min", "range_max", "latency_s", "latency_uncertainty_s")]
        if not np.all(np.isfinite(numeric)) or calibration["gain"] <= 0:
            raise ValueError("Invalid calibration values")
        latency_limit = 0.5 if channel == "temperature" else 0.00002
        if not 0 <= calibration["latency_uncertainty_s"] <= latency_limit:
            raise ValueError("Uncharacterized sensor latency")
        if channel != "temperature" and abs(calibration["latency_s"]) > 0.01:
            raise ValueError("Fast sensor latency outside the v1 correction domain")
        if channel == "trigger" and calibration["latency_s"] != 0:
            raise ValueError("Latency offsets must be relative to the recorded trigger")
        if calibration["range_min"] >= calibration["range_max"]:
            raise ValueError("Invalid ADC range")
        if calibration["kind"] != metadata["origin"]:
            raise ValueError("Mock calibration cannot certify physical data")
        values = samples[channel]
        if values.shape != TIMES.shape or not np.all(np.isfinite(values)):
            raise ValueError("Missing, nonfinite or wrong-length samples")
        if np.any(values <= calibration["range_min"]) or np.any(values >= calibration["range_max"]):
            raise ValueError("Clipping or ADC saturation")
    if metadata["origin"] == "physical" and any("MOCK" in str(value).upper() for value in
            [metadata["hardware_configuration"], clock["id"],
             *(item["version"] for item in metadata["calibrations"].values())]):
        raise ValueError("Mock apparatus/calibration cannot be labeled physical")


def save_raw(directory: Path, metadata: dict, samples: dict[str, np.ndarray]) -> None:
    directory.mkdir(parents=True, exist_ok=False)
    with (directory / "samples.npz").open("xb") as handle:
        np.savez_compressed(handle, **samples)
    write_json_new(directory / "metadata.json", metadata)
    hashes = {name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
              for name in ("samples.npz", "metadata.json")}
    write_json_new(directory / "hashes.json", hashes)


def load_raw(directory: Path, validate: bool = True) -> tuple[dict, dict[str, np.ndarray]]:
    hashes = json.loads((directory / "hashes.json").read_text())
    if set(hashes) != {"samples.npz", "metadata.json"}:
        raise ValueError("Invalid raw-file hash manifest")
    for name, digest in hashes.items():
        if hashlib.sha256((directory / name).read_bytes()).hexdigest() != digest:
            raise ValueError("Raw file was modified")
    metadata = json.loads((directory / "metadata.json").read_text())
    with np.load(directory / "samples.npz", allow_pickle=False) as archive:
        samples = {name: archive[name] for name in archive.files}
    if validate:
        validate_dataset(metadata, samples)
    return metadata, samples


def acquire_physical(*args, **kwargs):
    raise NotImplementedError("No hardware driver or physical acquisition has been implemented")


def mock_run(event: dict, scenario: str, seed: int, manifest_sha256: str = "0" * 64):
    if scenario not in SCENARIOS:
        raise ValueError("Unknown synthetic injection")
    rng = np.random.default_rng(seed)
    noise = dict.fromkeys(CHANNELS, 0.001)
    noise.update(current=0.0001, magnetic=0.01, acceleration=0.01,
                 acoustic=0.0001, temperature=0.001, environment_reference=0.01,
                 em_reference=0.01, mechanical_reference=0.01, acoustic_reference=0.0001)
    samples = {channel: rng.normal(0, noise[channel], len(TIMES)) for channel in CHANNELS}
    samples["sample_index"] = np.arange(len(TIMES))
    samples["temperature"] += 20.0
    samples["trigger"] += (TIMES >= 0).astype(float) * 3.3
    samples["timing_reference"] += ((np.arange(len(TIMES)) + 500) % 1000 < 10) * 3.3
    amplitude = rng.uniform(0.8, 1.2)
    pulse = np.exp(-0.5 * ((TIMES - 0.012) / 0.002)**2) * amplitude
    causes = set(scenario.split("+"))
    if scenario == "overlap": causes = {"em", "vibration", "acoustic"}
    for cause, reference, target, scale in [
        ("em", "em_reference", "magnetic", 2.0),
        ("vibration", "mechanical_reference", "acceleration", 2.0),
        ("acoustic", "acoustic_reference", "acoustic", 0.02),
    ]:
        if cause in causes:
            samples[reference] += scale * pulse
            samples[target] += 0.6 * scale * pulse
    if scenario == "electrical":
        samples["current"] += 0.05 * pulse
        samples["voltage"] += 0.5 * pulse
    if scenario == "thermal":
        samples["temperature"] += np.maximum(TIMES, 0) * 2
    if scenario == "environmental":
        samples["environment_reference"] += pulse
        samples["magnetic"] += pulse
    if scenario == "timing":
        samples["trigger"] = np.roll(samples["trigger"], 40)
    if scenario == "software":
        samples["sample_index"][4001] = 4000
    if scenario == "unknown":
        for channel in TARGETS:
            samples[channel] += noise[channel] * 50 * pulse
    metadata = {
        "schema_version": "1.0", "experiment_id": EXPERIMENT_ID,
        "run_id": event["run_id"], "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "origin": "synthetic", "blind_label": event["blind_label"], "event_type": "WITHHELD",
        "clock": {"id": "MOCK-CLOCK", "sample_rate_hz": RATE_HZ, "trigger_index": 4000,
                  "uncertainty_s": 0.00005, "software_time_authoritative": False},
        "calibrations": calibration_metadata(), "hardware_configuration": "MOCK-FIXTURE",
        "environment": {"room_temperature_degC": 20.0}, "operator_notes": WARNING,
        "validity_flags": [], "manifest_sha256": manifest_sha256,
    }
    return metadata, samples


def baseline_noise(values: np.ndarray, latency_s: float = 0.0) -> tuple[float, float]:
    baseline = window(values, BASELINE, latency_s)
    center = float(np.median(baseline))
    sigma = max(float(1.4826 * np.median(np.abs(baseline - center))), 1e-12)
    return center, sigma


def peak(values: np.ndarray, latency_s: float = 0.0) -> tuple[float, float, float]:
    center, sigma = baseline_noise(values, latency_s)
    observed = np.abs(window(values, EVENT, latency_s) - center)
    index = int(np.argmax(observed))
    corrected_times = TIMES - latency_s
    event_times = corrected_times[(corrected_times >= EVENT[0]) & (corrected_times < EVENT[1])]
    return float(observed[index]), sigma, float(event_times[index])


def features(samples: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    latencies = samples.get("_latencies", dict.fromkeys(CHANNELS, 0.0))
    predictors = [1.0, *(peak(samples[channel], latencies[channel])[0] for channel in REFERENCES)]
    targets = [peak(samples[channel], latencies[channel]) for channel in TARGETS]
    return np.array(predictors), np.array([value[0] for value in targets]), np.array([value[2] for value in targets])


def calibrated_samples(metadata: dict, samples: dict) -> dict:
    return {"sample_index": samples["sample_index"], "_latencies": {
        channel: metadata["calibrations"][channel]["latency_s"] for channel in CHANNELS}, **{
        channel: samples[channel] * metadata["calibrations"][channel]["gain"]
        + metadata["calibrations"][channel]["offset"] for channel in CHANNELS}}


def check_timing(samples: dict) -> bool:
    trigger_edges = np.flatnonzero(np.diff((samples["trigger"] > 1.65).astype(int)) == 1) + 1
    reference_edges = np.flatnonzero(np.diff((samples["timing_reference"] > 1.65).astype(int)) == 1) + 1
    return bool(len(trigger_edges) == 1 and abs(int(trigger_edges[0]) - 4000) <= 1
                and len(reference_edges) >= 8 and np.all(np.abs(np.diff(reference_edges) - 1000) <= 1))


def fit_model(records) -> dict:
    predictors, targets, ids, origins = [], [], [], set()
    for metadata, samples in records:
        validate_dataset(metadata, samples)
        samples = calibrated_samples(metadata, samples)
        if not check_timing(samples): raise ValueError("Invalid calibration timing")
        observed, response, _ = features(samples)
        predictors.append(observed); targets.append(response)
        ids.append(metadata["run_id"]); origins.add(metadata["origin"])
    if len(ids) < 240 or len(ids) != len(set(ids)) or len(origins) != 1:
        raise ValueError("Need 240 distinct, single-origin model calibration runs")
    design, response = np.asarray(predictors), np.asarray(targets)
    scales = np.maximum(np.std(design, axis=0), 1e-12); scales[0] = 1.0
    weights = np.linalg.solve((design / scales).T @ (design / scales) + np.eye(design.shape[1]) * 1e-6,
                              (design / scales).T @ response)
    residual = response - (design / scales) @ weights
    residual_sigma = np.maximum(1.4826 * np.median(np.abs(residual - np.median(residual, axis=0)), axis=0), 1e-6)
    return {"version": "GV-PHY-001-FEATURE-1", "origin": origins.pop(), "training_ids": ids,
            "weights": weights.tolist(), "scales": scales.tolist(),
            "residual_sigma": residual_sigma.tolist()}


def residual_score(samples: dict, model: dict) -> tuple[float, bool]:
    observed, response, peak_times = features(samples)
    residual = (response - (observed / np.array(model["scales"])) @ np.array(model["weights"])) / np.array(model["residual_sigma"])
    selected = np.argsort(residual)[-2:]
    coherent = bool(abs(peak_times[selected[0]] - peak_times[selected[1]]) <= 0.001)
    return float(np.sort(residual)[-2]), coherent


def simple_scores(samples: dict) -> tuple[float, float]:
    peaks, rms = [], []
    latencies = samples.get("_latencies", dict.fromkeys(CHANNELS, 0.0))
    for channel in TARGETS:
        value, sigma, _ = peak(samples[channel], latencies[channel])
        center, _ = baseline_noise(samples[channel], latencies[channel])
        peaks.append(value / sigma)
        rms.append(float(np.sqrt(np.mean(((window(samples[channel], EVENT, latencies[channel]) - center) / sigma)**2))))
    return float(np.sort(peaks)[-2]), float(np.sort(rms)[-2])


def lock_threshold(records, model: dict) -> dict:
    scores, peak_scores, rms_scores, ids = [], [], [], []
    for metadata, samples in records:
        validate_dataset(metadata, samples)
        samples = calibrated_samples(metadata, samples)
        if metadata["origin"] != model["origin"] or not check_timing(samples):
            raise ValueError("Calibration origin/timing mismatch")
        if metadata["run_id"] in model["training_ids"]:
            raise ValueError("Model/threshold calibration leakage")
        scores.append(residual_score(samples, model)[0]); ids.append(metadata["run_id"])
        simple_peak, simple_rms = simple_scores(samples)
        peak_scores.append(simple_peak); rms_scores.append(simple_rms)
    if len(ids) < 240 or len(ids) != len(set(ids)):
        raise ValueError("Need 240 distinct threshold calibration events")
    return {"value": max(8.0, float(np.quantile(scores, 0.99, method="higher"))),
            "simple_peak_value": max(8.0, float(np.quantile(peak_scores, 0.99, method="higher"))),
            "simple_rms_value": max(8.0, float(np.quantile(rms_scores, 0.99, method="higher"))),
            "calibration_ids": ids, "target_fpr": 0.01, "origin": model["origin"]}


def analyze_run(metadata: dict, samples: dict, model: dict, threshold: dict) -> dict:
    validate_dataset(metadata, samples)
    samples = calibrated_samples(metadata, samples)
    if metadata["origin"] != model["origin"] or metadata["origin"] != threshold["origin"]:
        raise ValueError("Synthetic/physical origin mismatch")
    if metadata["run_id"] in model["training_ids"] + threshold["calibration_ids"]:
        raise ValueError("Evaluation data leakage")
    score, coherent = residual_score(samples, model)
    simple_peak, simple_rms = simple_scores(samples)
    candidate = bool(score > threshold["value"] and coherent)
    causes = []
    if not check_timing(samples): causes.append("TIMING ARTIFACT"); candidate = False
    for channels, label in [
        (("current", "voltage"), "ELECTRICAL TRANSIENT"),
        (("em_reference",), "KNOWN EM"),
        (("mechanical_reference",), "KNOWN MECHANICAL"),
        (("acoustic_reference",), "KNOWN ACOUSTIC"),
        (("environment_reference",), "KNOWN ENVIRONMENTAL"),
    ]:
         if any(peak(samples[channel], samples["_latencies"][channel])[0]
             / peak(samples[channel], samples["_latencies"][channel])[1] > 8 for channel in channels):
            causes.append(label)
    temperature = samples["temperature"]
    if abs(float(np.median(window(temperature, (0.15, 0.25)))) - baseline_noise(temperature)[0]) > 0.1:
        causes.append("KNOWN THERMAL")
    classification = ("MULTIPLE KNOWN CAUSES" if len(causes) > 1 else causes[0]) if causes else (
        "UNEXPLAINED PROPAGATION CANDIDATE" if candidate else "NULL")
    if classification == "UNEXPLAINED PROPAGATION CANDIDATE" and metadata["origin"] == "physical":
        classification = "UNATTRIBUTED RESIDUAL - REQUIRES CONTROLS"
    return {"run_id": metadata["run_id"], "origin": metadata["origin"],
            "physical_evidence": False,
            "valid": check_timing(samples),
            "classification": classification, "known_channels_present": causes,
            "score": score, "coherent": coherent, "residual_flag": candidate,
            "simple_peak_flag": bool(simple_peak > threshold["simple_peak_value"] and coherent and check_timing(samples)),
            "simple_rms_flag": bool(simple_rms > threshold["simple_rms_value"] and coherent and check_timing(samples)),
            "interpretation": WARNING if metadata["origin"] == "synthetic" else
            "Screening only; measured references do not establish causal attribution"}


def proportion_interval(hits: int, total: int, alpha: float = 0.05) -> dict:
    from scipy.stats import beta

    if not 0 <= hits <= total or not 0 < alpha < 1:
        raise ValueError("Invalid binomial count or interval level")
    if total == 0: return {"n": 0, "hits": 0, "rate": None, "interval": [None, None]}
    lower = 0.0 if hits == 0 else float(beta.ppf(alpha / 2, hits, total - hits + 1))
    upper = 1.0 if hits == total else float(beta.ppf(1 - alpha / 2, hits + 1, total - hits))
    return {"n": total, "hits": hits, "rate": hits / total, "interval": [lower, upper]}


def summarize_results(results: list[dict], private: dict) -> dict:
    if {row["origin"] for row in results} != {"synthetic"}:
        raise NotImplementedError("Physical conclusions require independent hardware/control review")
    assignments = {row["run_id"]: row["arm"] for row in private["assignments"]}
    ids = [row["run_id"] for row in results]
    if len(ids) != len(set(ids)) or set(ids) != set(assignments):
        raise ValueError("Summary requires every manifest event exactly once, including invalid events")
    groups = {}
    for arm in sorted(set(assignments.values())):
        selected = [row for row in results if assignments[row["run_id"]] == arm]
        valid = [row for row in selected if row["valid"]]
        groups[arm] = proportion_interval(sum(row["residual_flag"] for row in valid), len(valid))
        groups[arm].update(attempted=len(selected), invalid=len(selected) - len(valid))
        groups[arm]["simple_peak_hits"] = sum(row.get("simple_peak_flag", False) for row in valid)
        groups[arm]["simple_rms_hits"] = sum(row.get("simple_rms_flag", False) for row in valid)
    active = groups.get("active", proportion_interval(0, 0))
    sham = groups.get("sham", proportion_interval(0, 0))
    difference, bounds = None, [None, None]
    if active["n"] and sham["n"]:
        active_bound = proportion_interval(active["hits"], active["n"], 0.025)["interval"]
        sham_bound = proportion_interval(sham["hits"], sham["n"], 0.025)["interval"]
        difference = active["rate"] - sham["rate"]
        bounds = [active_bound[0] - sham_bound[1], active_bound[1] - sham_bound[0]]
    enough = active["n"] >= 120 and sham["n"] >= 120 and all(
        groups.get(arm, {"n": 0})["n"] >= 45 for arm in CONTROL_ARMS)
    valid_ids = {row["run_id"] for row in results if row["valid"]}
    em_subconditions = {variant: sum(row["run_id"] in valid_ids for row in private["assignments"]
        if row["arm"] == "shielded" and row.get("variant") == variant)
        for variant in ("shielding", "distance")}
    enough = enough and all(count >= 20 for count in em_subconditions.values())
    controls_pass = all(groups.get(arm, {"hits": 999})["hits"] <= 2 for arm in CONTROL_ARMS)
    endpoint = bool(enough and controls_pass and difference >= 0.10 and bounds[0] > 0
                    and sham["interval"][1] <= 0.05)
    return {"experiment_id": EXPERIMENT_ID, "status": "INVALID / INCONCLUSIVE",
            "physical_evidence": False, "warning": WARNING,
            "groups": groups, "risk_difference": difference, "risk_difference_interval": bounds,
            "minimum_valid_counts_met": enough, "diagnostic_controls_pass": controls_pass,
            "em_subcondition_valid_counts": em_subconditions,
            "frozen_endpoint_met": endpoint,
            "reason": "Mock-only software; physical control validation and replication not established",
            "missing_detections": "Retained as non-detections; no lead-time endpoint", "lead_time": None}


def inspect_run(metadata: dict, samples: dict, model: dict, threshold: dict) -> dict:
    try:
        return analyze_run(metadata, samples, model, threshold)
    except ValueError as error:
        software = not np.array_equal(samples.get("sample_index"), np.arange(len(TIMES)))
        return {"run_id": metadata["run_id"], "origin": metadata["origin"], "valid": False,
            "physical_evidence": False,
                "classification": "SOFTWARE ARTIFACT" if software else "INVALID ACQUISITION",
                "residual_flag": False, "reason": str(error), "interpretation": WARNING}