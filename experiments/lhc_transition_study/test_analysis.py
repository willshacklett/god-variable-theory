"""SYNTHETIC SOFTWARE FIXTURES ONLY — NOT LHC OBSERVATIONS OR GV EVIDENCE."""

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


DIRECTORY = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("lhc_transition_analysis", DIRECTORY / "analysis.py")
analysis = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = analysis
SPEC.loader.exec_module(analysis)
HEADER = ",".join(analysis.FIELDS) + "\n"
SYNTHETIC = "100,current,A,3,2,synthetic\n110,current,A,5,2,synthetic\n"


class AnalysisTests(unittest.TestCase):
    def load(self, body, expected="synthetic", header=HEADER):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic_fixture.csv"
            path.write_text(header + body, encoding="utf-8")
            return analysis.load_observations(path, expected_provenance=expected)

    def test_synthetic_residuals(self):
        self.assertEqual([row.residual for row in self.load(SYNTHETIC)], [1, 3])

    def test_command_and_response_are_separate(self):
        event = analysis.Transition("ramp", 100, 105)
        result = analysis.aligned_residuals(
            self.load(SYNTHETIC), event, channel="current", before_ns=0, after_ns=10,
        )
        self.assertEqual([row["command_offset_ns"] for row in result], [0, 10])
        self.assertEqual([row["response_offset_ns"] for row in result], [-5, 5])
        self.assertTrue(all(row["provenance"] == "synthetic" for row in result))

    def test_missing_response_is_not_inferred(self):
        result = analysis.aligned_residuals(
            self.load(SYNTHETIC), analysis.Transition("dump", 100),
            channel="current", before_ns=0, after_ns=0,
        )
        self.assertEqual(len(result), 1)
        self.assertIsNone(result[0]["response_offset_ns"])

    def test_empty_window_not_zero_signal(self):
        self.assertEqual(analysis.aligned_residuals(
            self.load(SYNTHETIC), analysis.Transition("injection", 200),
            channel="current", before_ns=0, after_ns=0,
        ), [])

    def test_no_synthetic_as_real(self):
        with self.assertRaises(ValueError):
            self.load(SYNTHETIC, expected="real")

    def test_unknown_provenance(self):
        with self.assertRaises(ValueError):
            self.load(SYNTHETIC, expected="unknown")

    def test_mixed_provenance(self):
        with self.assertRaises(ValueError):
            self.load(SYNTHETIC + "120,current,A,1,1,real\n")

    def test_nonfinite_and_overflow(self):
        for observed, predicted in [("nan", "1"), ("inf", "1"), ("1", "-inf"), ("1e308", "-1e308")]:
            with self.subTest(observed=observed, predicted=predicted), self.assertRaises(ValueError):
                self.load(f"100,current,A,{observed},{predicted},synthetic\n")

    def test_bad_timestamps(self):
        for stamp in ["-1", "1.5", "not-a-time"]:
            with self.subTest(stamp=stamp), self.assertRaises(ValueError):
                self.load(f"{stamp},current,A,1,1,synthetic\n")

    def test_duplicate_and_out_of_order(self):
        for stamp in [100, 99]:
            with self.subTest(stamp=stamp), self.assertRaises(ValueError):
                self.load(f"100,current,A,1,1,synthetic\n{stamp},current,A,1,1,synthetic\n")

    def test_unit_changes_and_empty_identifiers(self):
        for body in [
            SYNTHETIC + "120,current,T,1,1,synthetic\n",
            "100,,A,1,1,synthetic\n",
            "100,current,,1,1,synthetic\n",
        ]:
            with self.subTest(body=body), self.assertRaises(ValueError):
                self.load(body)

    def test_malformed_schema_and_rows(self):
        with self.assertRaises(ValueError):
            self.load(SYNTHETIC, header="wrong,header\n")
        for body in ["", "100,current,A,1,1\n", "100,current,A,1,1,synthetic,extra\n"]:
            with self.subTest(body=body), self.assertRaises(ValueError):
                self.load(body)

    def test_event_and_window_validation(self):
        for args in [("unknown", 100), ("dump", -1), ("dump", 100, 99), ("dump", True)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                analysis.Transition(*args)
        with self.assertRaises(ValueError):
            analysis.aligned_residuals(
                self.load(SYNTHETIC), analysis.Transition("dump", 100),
                channel="current", before_ns=-1, after_ns=0,
            )
        with self.assertRaises(ValueError):
            analysis.aligned_residuals(
                self.load(SYNTHETIC), analysis.Transition("dump", 100),
                channel="missing", before_ns=0, after_ns=0,
            )

    def test_multiple_channels_keep_distinct_units(self):
        items = self.load(SYNTHETIC + "100,field,T,0.5,0.4,synthetic\n")
        result = analysis.aligned_residuals(
            items, analysis.Transition("stable_beams", 100),
            channel="field", before_ns=0, after_ns=0,
        )
        self.assertEqual(result[0]["unit"], "T")
        self.assertAlmostEqual(result[0]["residual"], 0.1)

    def test_inventory_does_not_claim_verified_data(self):
        inventory = json.loads((DIRECTORY / "data_inventory.json").read_text(encoding="utf-8"))
        self.assertFalse(inventory["real_measurements_included"])
        self.assertEqual(inventory["verified_available_datasets"], [])
        self.assertEqual(len(inventory["source_leads"]), 4)
        for source in inventory["source_leads"]:
            self.assertEqual(source["verification_status"], "unverified_dns_failure")
            self.assertIsNone(source["timestamp_precision"])
            self.assertFalse(source["synchronized_measurements_verified"])

    def test_phase_2_findings_are_attributed_not_verified(self):
        inventory = json.loads((DIRECTORY / "data_inventory.json").read_text(encoding="utf-8"))
        phase = inventory["phase_2"]
        self.assertEqual(len(phase["source_assessments"]), 3)
        for source in phase["source_assessments"]:
            self.assertEqual(source["finding_provenance"], "task_owner_report")
            self.assertEqual(source["direct_verification_status"], "dns_failure")
            self.assertEqual(source["curl_exit_code"], 6)
            self.assertIsNone(source["http_status"])
            self.assertFalse(source["content_retrieved"])
            self.assertFalse(source["dataset_access_verified"])

    def test_phase_2_does_not_invent_fills_or_measurements(self):
        inventory = json.loads((DIRECTORY / "data_inventory.json").read_text(encoding="utf-8"))
        phase = inventory["phase_2"]
        self.assertEqual(phase["selected_fill_ids"], [])
        self.assertEqual(phase["verified_downloadable_measurements"], [])
        self.assertEqual(phase["verified_alignment_variables"], [])
        self.assertTrue(all(value is None for value in phase["measurement_metadata_status"].values()))
        self.assertEqual(phase["access_request"]["status"], "draft_not_sent")
        self.assertIsNone(phase["access_request"]["selected_query_bounds"])
        self.assertEqual(phase["transition_priorities"], ["injection", "ramp", "stable_beams", "dump"])
        self.assertEqual(
            phase["ingestion_adapter_status"], "not_implemented_no_verified_source_schema_or_payload",
        )


if __name__ == "__main__":
    unittest.main()
