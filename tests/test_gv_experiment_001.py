from __future__ import annotations

from pathlib import Path

import numpy as np

from src.gv_experiment_001 import (
    build_propagation_matrix,
    combine_source_pulses,
    evaluate_reconstruction,
    generate_source_pulses,
    observe_downstream_state,
    reconstruct_baseline,
    reconstruct_source,
    run_experiment,
    run_sensitivity_analysis,
)


def test_source_generation_and_inverse_filtering_reconstructs_well():
    pulse_bank = generate_source_pulses(length=64, num_sources=4, seed=11)
    source = combine_source_pulses(pulse_bank)
    observation = observe_downstream_state(source)
    propagation_matrix = build_propagation_matrix(length=64)
    reconstruction = reconstruct_source(observation, propagation_matrix)
    metrics = evaluate_reconstruction(source, reconstruction)

    assert pulse_bank.shape == (4, 64)
    assert source.shape == (64,)
    assert observation.shape == (64,)
    assert metrics["rmse"] < 0.35
    assert metrics["correlation"] > 0.80
    assert metrics["correlation_retention"] > 0.5
    assert metrics["spectral_information_retention"] > 0.0
    assert metrics["spectral_information_loss"] >= 0.0


def test_run_experiment_creates_plots_and_reports_metrics(tmp_path: Path):
    results = run_experiment(output_dir=tmp_path, save_plots=True)

    assert "conditions" in results
    assert results["conditions"]["oracle"]["rmse_mean"] < results["conditions"]["baseline"]["rmse_mean"]
    assert results["conditions"]["model_mismatch"]["rmse_mean"] >= results["conditions"]["oracle"]["rmse_mean"]
    assert results["conditions"]["blind"]["rmse_mean"] >= results["conditions"]["oracle"]["rmse_mean"]
    assert (tmp_path / "aggregate_metrics.csv").exists()
    assert (tmp_path / "trial_metrics.csv").exists()
    assert (tmp_path / "benchmark_comparison.png").exists()
    assert (tmp_path / "parameter_recovery.png").exists()


def test_sensitivity_analysis_creates_plots(tmp_path: Path):
    results = run_sensitivity_analysis(output_dir=tmp_path, save_plots=True)

    diffusion_metrics = results["diffusion_sweep"]["metrics"]
    noise_metrics = results["noise_sweep"]["metrics"]

    assert len(results["diffusion_sweep"]["diffusion"]) > 1
    assert len(results["noise_sweep"]["noise"]) > 1
    assert diffusion_metrics[0]["mean_rmse"] <= diffusion_metrics[-1]["mean_rmse"]
    assert noise_metrics[0]["mean_rmse"] <= noise_metrics[-1]["mean_rmse"]
    assert (tmp_path / "diffusion_sensitivity.png").exists()
    assert (tmp_path / "noise_sensitivity.png").exists()


def test_oracle_outperforms_naive_baseline_and_metrics_are_bounded():
    source = generate_source_pulses(length=64, num_sources=3, seed=11).sum(axis=0)
    propagation_matrix = build_propagation_matrix(length=64, advection=0.2, diffusion=0.03, steps=4)
    observation = observe_downstream_state(source, propagation_matrix, noise=0.0)

    oracle_reconstruction = reconstruct_source(observation, propagation_matrix)
    baseline_reconstruction = reconstruct_baseline(observation, shift=2)

    oracle_metrics = evaluate_reconstruction(source, oracle_reconstruction)
    baseline_metrics = evaluate_reconstruction(source, baseline_reconstruction)

    assert oracle_metrics["rmse"] < baseline_metrics["rmse"]
    assert oracle_metrics["correlation"] > baseline_metrics["correlation"]
    for metric_name in ["rmse", "correlation", "correlation_retention", "spectral_information_retention", "spectral_information_loss"]:
        assert np.isfinite(oracle_metrics[metric_name])
        assert np.isfinite(baseline_metrics[metric_name])
        assert 0.0 <= oracle_metrics[metric_name] <= 1.0 or metric_name == "rmse"
        assert 0.0 <= baseline_metrics[metric_name] <= 1.0 or metric_name == "rmse"
