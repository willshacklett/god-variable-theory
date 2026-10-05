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
    "EDGECASE-CI",
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
    for experiment_id in ["EM-001", "EM-002", "TUNING-HW-001"]:
        assert by_id[experiment_id]["status"] == "PENDING"
        assert by_id[experiment_id]["dataset"]["kind"] == "none"
    for experiment_id in ["SWITCH-PHASE0", "SWITCH-E1"]:
        assert by_id[experiment_id]["status"] == "HARDWARE READY / NOT RUN"
        assert by_id[experiment_id]["dataset"]["kind"] == "none"


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