from __future__ import annotations

import json
from pathlib import Path
import re
import shlex
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

import pytest


ROOT = Path(__file__).resolve().parents[1]
LEDGER = json.loads((ROOT / "evidence/evidence_ledger.json").read_text())
RECORDS = LEDGER["experiments"]
STATUSES = {
    "SUPPORTIVE", "MIXED", "NOT SUPPORTIVE", "INVALID / INCONCLUSIVE",
    "PENDING", "HARDWARE READY / NOT RUN",
}
EXPECTED_IDS = {
    "F0", "F1", "F1b", "F2", "F2b", "SWITCH-TIMING",
    "SWITCH-FAILED-CLASSIFIERS", "SWITCH-CLOCK", "SWITCH-EM",
    "SWITCH-ENVIRONMENT", "SWITCH-MASTER", "SWITCH-PHASE0", "SWITCH-E1",
    "EM-001", "EM-002", "TUNING-HW-001", "TOY-COSMOLOGY", "TOY-TETHER",
    "EDGECASE-CI", "GV-PHY-001",
}
DOC_FILES = sorted([
    *ROOT.glob("*.md"), *(ROOT / "docs").glob("*.md"),
    *(ROOT / "theory").glob("*.md"), *(ROOT / "experiments").glob("*.md"),
])


def heading_anchors(text):
    anchors = set()
    counts = {}
    for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.MULTILINE):
        slug = re.sub(r"[^\w\s-]", "", heading.lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        anchors.add(f"{slug}-{count}" if count else slug)
        counts[slug] = count + 1
    return anchors


def check_internal_link(source, link):
    parsed = urlsplit(link)
    if parsed.scheme or parsed.netloc:
        return
    target = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
    assert target.is_relative_to(ROOT), (source, link)
    assert target.exists(), (source, link)
    if parsed.fragment and target.suffix == ".md":
        assert unquote(parsed.fragment) in heading_anchors(target.read_text()), (source, link)


def test_ledger_schema_and_coverage():
    assert LEDGER["schema_version"] == "1.0"
    assert len(LEDGER["baseline_commit"]) == 40
    identifiers = [record["experiment_id"] for record in RECORDS]
    assert len(identifiers) == len(set(identifiers))
    assert EXPECTED_IDS <= set(identifiers)
    covered_code = {path for record in RECORDS for path in record["code"]}
    assert {str(path.relative_to(ROOT)) for path in (ROOT / "experiments").glob("*.py")} <= covered_code
    covered_protocols = {path for record in RECORDS for path in record["protocol"]}
    assert {str(path.relative_to(ROOT)) for path in (ROOT / "experiments").glob("*PREREGISTRATION.md")} <= covered_protocols
    covered_sources = {path for record in RECORDS for path in record["sources"]}
    assert {str(path.relative_to(ROOT)) for path in (ROOT / "experiments").glob("*RESULTS.md")} <= covered_sources


@pytest.mark.parametrize("record", RECORDS, ids=lambda record: record["experiment_id"])
def test_ledger_record_schema_and_references(record):
    fields = {
        "experiment_id", "program", "evidence_scope", "hypothesis", "protocol",
        "dataset", "baseline", "success_criterion", "result", "status",
        "interpretation", "limitations", "reproduction_command", "sources", "code",
    }
    assert set(record) == fields
    for field in fields - {"protocol", "dataset", "limitations", "reproduction_command", "sources", "code"}:
        assert isinstance(record[field], str) and record[field].strip()
    assert record["program"] in {"A", "B", "C"}
    assert record["status"] in STATUSES
    assert set(record["dataset"]) == {"kind", "description", "paths"}
    assert record["dataset"]["kind"] in {"synthetic", "none", "physical", "derived"}
    assert isinstance(record["dataset"]["description"], str) and record["dataset"]["description"]
    assert isinstance(record["limitations"], list) and record["limitations"]
    assert all(isinstance(item, str) and item.strip() for item in record["limitations"])
    command = record["reproduction_command"]
    assert command is None or (isinstance(command, str) and command.startswith("python "))
    if command:
        for argument in shlex.split(command):
            if argument.endswith(".py"):
                assert (ROOT / argument).is_file(), argument
    for paths in [record["protocol"], record["sources"], record["code"], record["dataset"]["paths"]]:
        assert isinstance(paths, list)
        for path in paths:
            assert isinstance(path, str)
            resolved = (ROOT / path).resolve()
            assert resolved.is_relative_to(ROOT)
            assert resolved.is_file(), path
    assert record["sources"]


def test_negative_and_unrun_results_cannot_be_promoted():
    by_id = {record["experiment_id"]: record for record in RECORDS}
    for experiment_id in ["F0", "F1", "F1b", "F2b", "SWITCH-FAILED-CLASSIFIERS"]:
        assert by_id[experiment_id]["status"] == "NOT SUPPORTIVE"
    assert by_id["F2"]["status"] == "INVALID / INCONCLUSIVE"
    for experiment_id in ["EM-001", "EM-002", "TUNING-HW-001", "GV-PHY-001"]:
        assert by_id[experiment_id]["status"] == "PENDING"
        assert by_id[experiment_id]["dataset"]["kind"] == "none"
    for experiment_id in ["SWITCH-PHASE0", "SWITCH-E1"]:
        assert by_id[experiment_id]["status"] == "HARDWARE READY / NOT RUN"
        assert by_id[experiment_id]["dataset"]["kind"] == "none"


def test_f0_endpoint_is_difference_of_medians(capsys):
    import numpy as np
    from experiments.gv_fluid_instability_test import summarize

    leads = {
        "GV": np.array([0.0, 10.0, 11.0]),
        "|x|": np.array([0.0, 0.0, 0.0]),
        "|dx/dt|": np.array([0.0, 0.0, 0.0]),
        "|d2x/dt2|": np.array([0.0, 1.0, 20.0]),
    }
    _, delta = summarize(0.0, leads, dict.fromkeys(leads, 0.05))
    assert delta == 9.0
    assert delta != np.median(leads["GV"] - leads["|d2x/dt2|"])
    capsys.readouterr()


def test_f2b_missing_alarms_remain_undefined(capsys):
    import numpy as np
    from experiments.gv_fluid_f2b_2d_test import DETECTORS, summarize

    leads = {name: np.full(60, np.nan) for name in DETECTORS}
    outcome = summarize(0.10, leads, np.full(60, np.nan),
                        dict.fromkeys(DETECTORS, 0.05), 1.0, 0.0, True)
    output = capsys.readouterr().out
    assert outcome == "NOT SUPPORTIVE"
    paired_line = next(line for line in output.splitlines() if "Median paired Delta L:" in line)
    assert paired_line.split()[-1] == "nan"


@pytest.mark.parametrize("link", ["evidence/nonexistent-result.md", "README.md#nonexistent-heading", "../outside-repository.md"])
def test_link_checks_reject_broken_targets(link):
    with pytest.raises(AssertionError):
        check_internal_link(ROOT / "README.md", link)


@pytest.mark.parametrize("experiment_id", ["F0", "F1", "F1b", "F2", "F2b"])
def test_benchmark_ledger_verdict_matches_report(experiment_id):
    record = next(item for item in RECORDS if item["experiment_id"] == experiment_id)
    report = (ROOT / record["sources"][0]).read_text()
    outcome = re.search(r"^\*\*(NOT SUPPORTIVE|SUPPORTIVE|BENCHMARK INVALID)\*\*$", report, re.MULTILINE)
    assert outcome is not None
    status = outcome.group(1)
    if status == "BENCHMARK INVALID":
        status = "INVALID / INCONCLUSIVE"
    assert record["status"] == status


@pytest.mark.parametrize("mutation", ["invalid_status", "missing_source", "missing_field", "missing_script"])
def test_record_checks_reject_invalid_records(mutation):
    record = json.loads(json.dumps(RECORDS[0]))
    if mutation == "invalid_status":
        record["status"] = "CONFIRMED"
    elif mutation == "missing_source":
        record["sources"] = ["evidence/nonexistent-result.md"]
    elif mutation == "missing_field":
        del record["hypothesis"]
    else:
        record["reproduction_command"] = "python experiments/nonexistent.py"
    with pytest.raises(AssertionError):
        test_ledger_record_schema_and_references(record)


@pytest.mark.parametrize("mutation", ["missing_benchmark", "duplicate_id", "promoted_negative"])
def test_coverage_checks_reject_inventory_drift(monkeypatch, mutation):
    records = json.loads(json.dumps(RECORDS))
    if mutation == "missing_benchmark":
        records = [record for record in records if record["experiment_id"] != "F2b"]
    elif mutation == "duplicate_id":
        records.append(records[0])
    else:
        records[0]["status"] = "SUPPORTIVE"
    monkeypatch.setitem(globals(), "RECORDS", records)
    with pytest.raises(AssertionError):
        if mutation == "promoted_negative":
            test_negative_and_unrun_results_cannot_be_promoted()
        else:
            test_ledger_schema_and_coverage()


@pytest.mark.parametrize("document", DOC_FILES, ids=lambda path: str(path.relative_to(ROOT)))
def test_internal_markdown_links(document):
    text = re.sub(r"```.*?```", "", document.read_text(), flags=re.DOTALL)
    for link in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", text):
        check_internal_link(document, link)


def test_dashboard_local_asset_links():
    class AssetParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            for key, value in attrs:
                if key in {"href", "src"} and value:
                    check_internal_link(ROOT / "dashboard/index.html", value)

    AssetParser().feed((ROOT / "dashboard/index.html").read_text())


def test_public_claim_boundaries_and_required_sections():
    readme = (ROOT / "README.md").read_text()
    headings = re.findall(r"^## (.+)$", readme, re.MULTILINE)
    assert headings == [
        "Status", "Two Research Programs", "What Would Count as Evidence?",
        "What Has Failed?", "Current Experiments", "Reproduce the Work", "Theory",
        "Evidence Ledger", "Falsification", "Contributing", "Citation",
    ]
    for phrase in [
        "THE GOD VARIABLE HAS NOT BEEN CONFIRMED.",
        "A residual is only a residual until known explanations are excluded.",
        "UNEXPLAINED ≠ GV", "GV ≠ NEW PHYSICS", "NEW PHYSICS ≠ GOD",
        "Computational Reproduction", "Physical Replication",
    ]:
        assert phrase in readme
    for record in RECORDS:
        if record["status"] == "SUPPORTIVE":
            assert record["evidence_scope"] in {"synthetic methodology", "engineering software checks"}
    for filename in ["THEORY.md", "PAPER.md", "entropy_damping.md"]:
        assert "THE GOD VARIABLE HAS NOT BEEN CONFIRMED." in (ROOT / filename).read_text()[:1200]