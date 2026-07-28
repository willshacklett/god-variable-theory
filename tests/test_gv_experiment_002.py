from pathlib import Path

import numpy as np

from src.gv_experiment_002 import _evaluate_reconstruction, run_experiment


def test_full_observation_approximately_reproduces_experiment_001_performance(tmp_path: Path):
    results = run_experiment(output_dir=tmp_path, save_plots=False)
    full_rows = [
        row
        for row in results["aggregate_metrics"]
        if row["condition"] == "oracle" and row["mask_strategy"] == "uniform" and row["observation_fraction"] == 1.0
    ]

    assert full_rows
    row = full_rows[0]
    assert row["rmse_mean"] < 0.05
    assert row["correlation_mean"] > 0.95


def test_trend_analysis_reports_adjacent_changes_and_uncertainty(tmp_path: Path):
    results = run_experiment(output_dir=tmp_path, save_plots=False)
    analyses = [
        entry
        for entry in results["trend_analysis"]
        if entry["condition"] == "blind" and entry["mask_strategy"] == "uniform" and entry["metric"] == "rmse"
    ]

    assert analyses
    analysis = analyses[0]
    assert analysis["adjacent_increases"] >= 0
    assert analysis["adjacent_decreases"] >= 0
    assert np.isfinite(analysis["spearman_correlation"])
    assert len(analysis["uncertainty"]) >= 2
    for point in analysis["uncertainty"]:
        assert np.isfinite(point["mean"])
        assert np.isfinite(point["ci95_lower"])
        assert np.isfinite(point["ci95_upper"])


def test_blind_reconstruction_outperforms_naive_baseline_at_moderate_observation(tmp_path: Path):
    results = run_experiment(output_dir=tmp_path, save_plots=False)
    moderate_rows = [
        row
        for row in results["aggregate_metrics"]
        if row["condition"] in {"blind", "naive_baseline"}
        and row["mask_strategy"] == "uniform"
        and row["observation_fraction"] == 0.5
    ]

    assert len(moderate_rows) == 2
    blind_row = next(row for row in moderate_rows if row["condition"] == "blind")
    naive_row = next(row for row in moderate_rows if row["condition"] == "naive_baseline")
    assert blind_row["rmse_mean"] < naive_row["rmse_mean"]
    if np.isfinite(blind_row["correlation_mean"]) and np.isfinite(naive_row["correlation_mean"]):
        assert blind_row["correlation_mean"] > naive_row["correlation_mean"]


def test_metrics_are_finite_and_bounded(tmp_path: Path):
    results = run_experiment(output_dir=tmp_path, save_plots=False)
    for row in results["trial_metrics"]:
        for metric_name in ["rmse", "correlation", "correlation_retention", "spectral_information_loss"]:
            if np.isnan(row[metric_name]):
                continue
            assert np.isfinite(row[metric_name])
            if metric_name == "rmse":
                assert row[metric_name] >= 0.0
            else:
                if metric_name == "correlation" and not np.isfinite(row[metric_name]):
                    continue
                if metric_name != "correlation" and not (0.0 <= row[metric_name] <= 1.0):
                    raise AssertionError(f"{metric_name} out of bounds: {row[metric_name]}")
        assert np.isfinite(row["parameter_estimation_error"])


def test_recomputes_metrics_from_saved_source_and_reconstruction_arrays(tmp_path: Path):
    results = run_experiment(output_dir=tmp_path, save_plots=False)
    sample_rows = results["trial_metrics"][:3]

    for row in sample_rows:
        recomputed = _evaluate_reconstruction(row["source_array"], row["reconstruction_array"])
        for metric_name in ["rmse", "correlation", "correlation_retention", "spectral_information_loss"]:
            assert np.isclose(recomputed[metric_name], row[metric_name], atol=1e-12)


def test_aggregate_rows_equal_direct_aggregation_of_trial_rows(tmp_path: Path):
    results = run_experiment(output_dir=tmp_path, save_plots=False)
    expected = []
    grouped = {}
    for row in results["trial_metrics"]:
        key = (row["condition"], row["mask_strategy"], row["observation_fraction"])
        grouped.setdefault(key, []).append(row)

    for key in sorted(grouped):
        rows = grouped[key]
        metric_names = ["rmse", "correlation", "correlation_retention", "spectral_information_loss", "parameter_estimation_error"]
        summary = {}
        for metric_name in metric_names:
            values = [float(item[metric_name]) for item in rows]
            finite_values = [value for value in values if np.isfinite(value)]
            summary[f"{metric_name}_mean"] = float(np.mean(finite_values)) if finite_values else float("nan")
            summary[f"{metric_name}_std"] = float(np.std(finite_values, ddof=0)) if len(finite_values) > 1 else 0.0
        expected.append({
            "condition": key[0],
            "mask_strategy": key[1],
            "observation_fraction": key[2],
            "trial_count": len(rows),
            "rmse_mean": summary["rmse_mean"],
            "rmse_std": summary["rmse_std"],
            "correlation_mean": summary["correlation_mean"],
            "correlation_std": summary["correlation_std"],
            "correlation_retention_mean": summary["correlation_retention_mean"],
            "correlation_retention_std": summary["correlation_retention_std"],
            "spectral_information_loss_mean": summary["spectral_information_loss_mean"],
            "spectral_information_loss_std": summary["spectral_information_loss_std"],
            "parameter_estimation_error_mean": summary["parameter_estimation_error_mean"],
            "parameter_estimation_error_std": summary["parameter_estimation_error_std"],
            "correlation_undefined_count": int(sum(1 for item in rows if not np.isfinite(item["correlation"]))),
        })

    actual = sorted(results["aggregate_metrics"], key=lambda item: (item["condition"], item["mask_strategy"], item["observation_fraction"]))
    expected_sorted = sorted(expected, key=lambda item: (item["condition"], item["mask_strategy"], item["observation_fraction"]))
    for actual_row, expected_row in zip(actual, expected_sorted):
        for key in [
            "condition", "mask_strategy", "observation_fraction", "trial_count",
            "rmse_mean", "rmse_std", "correlation_mean", "correlation_std",
            "correlation_retention_mean", "correlation_retention_std",
            "spectral_information_loss_mean", "spectral_information_loss_std",
            "parameter_estimation_error_mean", "parameter_estimation_error_std",
            "correlation_undefined_count",
        ]:
            if isinstance(actual_row[key], float) and isinstance(expected_row[key], float):
                if np.isnan(actual_row[key]) and np.isnan(expected_row[key]):
                    continue
                assert np.isclose(actual_row[key], expected_row[key], atol=1e-12)
            else:
                assert actual_row[key] == expected_row[key]


def test_preregistered_hypothesis_is_evaluated_from_trial_level_pairs(tmp_path: Path):
    results = run_experiment(output_dir=tmp_path, save_plots=False)
    hypothesis = results["preregistered_hypothesis"]

    assert hypothesis["metric"] == "rmse"
    assert hypothesis["n_pairs"] > 0
    assert np.isfinite(hypothesis["mean_difference"])
    assert np.isfinite(hypothesis["ci95_lower"])
    assert np.isfinite(hypothesis["ci95_upper"])
    assert 0.0 <= hypothesis["win_rate"] <= 1.0


def test_results_are_reproducible_for_fixed_seeds(tmp_path: Path):
    first = run_experiment(output_dir=tmp_path / "first", save_plots=False)
    second = run_experiment(output_dir=tmp_path / "second", save_plots=False)

    assert len(first["aggregate_metrics"]) == len(second["aggregate_metrics"])
    assert len(first["trial_metrics"]) == len(second["trial_metrics"])
    for left, right in zip(first["aggregate_metrics"], second["aggregate_metrics"]):
        for key in ["condition", "mask_strategy", "observation_fraction", "trial_count", "correlation_undefined_count"]:
            assert left[key] == right[key]
        for key in ["rmse_mean", "rmse_std", "correlation_mean", "correlation_std", "correlation_retention_mean", "correlation_retention_std", "spectral_information_loss_mean", "spectral_information_loss_std", "parameter_estimation_error_mean", "parameter_estimation_error_std"]:
            if np.isnan(left[key]) and np.isnan(right[key]):
                continue
            assert np.isclose(left[key], right[key], atol=1e-12)
    for left, right in zip(first["trial_metrics"], second["trial_metrics"]):
        for key in ["condition", "mask_strategy", "observation_fraction", "family", "seed", "parameter_estimation_error"]:
            assert left[key] == right[key]
        for key in ["rmse", "correlation", "correlation_retention", "spectral_information_loss"]:
            if np.isnan(left[key]) and np.isnan(right[key]):
                continue
            assert np.isclose(left[key], right[key], atol=1e-12)


def test_experiment_outputs_are_written(tmp_path: Path):
    run_experiment(output_dir=tmp_path, save_plots=True)

    for relative_path in [
        "exp002_trial_metrics.csv",
        "exp002_aggregate_metrics.csv",
        "exp002_observation_fraction.png",
        "exp002_mask_comparison.png",
        "exp002_example_reconstructions.png",
    ]:
        assert (tmp_path / relative_path).exists()
