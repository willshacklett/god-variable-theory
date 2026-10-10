"""Local descriptive analysis only; no significance or GV evidence claims."""

import csv
from dataclasses import dataclass
import math


FIELDS = ("timestamp_ns", "channel", "unit", "observed", "predicted", "provenance")
PROVENANCES = {"real", "synthetic"}
TRANSITIONS = {"injection", "ramp", "adjustment", "stable_beams", "dump", "non_colliding"}


def _timestamp(value):
    if type(value) is not int or value < 0:
        raise ValueError("Timestamp must be a nonnegative integer Unix UTC ns coordinate")


@dataclass(frozen=True)
class Observation:
    timestamp_ns: int
    channel: str
    unit: str
    observed: float
    predicted: float
    provenance: str

    def __post_init__(self):
        _timestamp(self.timestamp_ns)
        if not self.channel.strip() or not self.unit.strip():
            raise ValueError("Channel and physical unit are required")
        if self.provenance not in PROVENANCES:
            raise ValueError("Explicit real or synthetic provenance is required")
        if not all(math.isfinite(x) for x in (self.observed, self.predicted)):
            raise ValueError("Measurements and predictions must be finite")
        if not math.isfinite(self.observed - self.predicted):
            raise ValueError("Residual overflow")

    @property
    def residual(self):
        return self.observed - self.predicted


@dataclass(frozen=True)
class Transition:
    kind: str
    command_ns: int
    response_ns: int | None = None

    def __post_init__(self):
        if self.kind not in TRANSITIONS:
            raise ValueError("Unknown transition class")
        _timestamp(self.command_ns)
        if self.response_ns is not None:
            _timestamp(self.response_ns)
            if self.response_ns < self.command_ns:
                raise ValueError("Resolve clock/order uncertainty before alignment")


def load_observations(path, *, expected_provenance):
    """Read a local normalized export; origin labels are not authentication."""
    if expected_provenance not in PROVENANCES:
        raise ValueError("Expected provenance must be real or synthetic")
    observations = []
    last_timestamp = {}
    units = {}
    with open(path, newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != list(FIELDS):
            raise ValueError("CSV header must match the documented schema exactly")
        for line, row in enumerate(reader, start=2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"Malformed CSV row at line {line}")
            try:
                item = Observation(
                    int(row["timestamp_ns"]), row["channel"], row["unit"],
                    float(row["observed"]), float(row["predicted"]), row["provenance"],
                )
                if item.provenance != expected_provenance:
                    raise ValueError("Mixed or unexpected provenance")
                if item.channel in last_timestamp and item.timestamp_ns <= last_timestamp[item.channel]:
                    raise ValueError("Duplicate or out-of-order channel timestamp")
                if item.channel in units and item.unit != units[item.channel]:
                    raise ValueError("Channel unit changed")
            except (ValueError, TypeError) as error:
                raise ValueError(f"Invalid CSV row at line {line}: {error}") from error
            last_timestamp[item.channel] = item.timestamp_ns
            units[item.channel] = item.unit
            observations.append(item)
    if not observations:
        raise ValueError("No observations")
    return observations


def aligned_residuals(observations, transition, *, channel, before_ns, after_ns):
    """Return inclusive command-relative window; never interpolate or fit."""
    _timestamp(before_ns)
    _timestamp(after_ns)
    rows = [item for item in observations if item.channel == channel]
    if not rows:
        raise ValueError("Requested channel has no observations")
    if len({item.provenance for item in rows}) != 1 or len({item.unit for item in rows}) != 1:
        raise ValueError("Cannot combine origins or units")
    if any(b.timestamp_ns <= a.timestamp_ns for a, b in zip(rows, rows[1:])):
        raise ValueError("Channel timestamps must be strictly increasing")
    return [
        {
            "command_offset_ns": item.timestamp_ns - transition.command_ns,
            "response_offset_ns": (
                None if transition.response_ns is None
                else item.timestamp_ns - transition.response_ns
            ),
            "residual": item.residual,
            "unit": item.unit,
            "provenance": item.provenance,
        }
        for item in rows
        if transition.command_ns - before_ns <= item.timestamp_ns <= transition.command_ns + after_ns
    ]
