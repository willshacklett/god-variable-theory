from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def generate_source_pulses(length: int = 64, num_sources: int = 4, seed: int = 7) -> np.ndarray:
    pulses = np.zeros((num_sources, length), dtype=float)
    centers = np.linspace(8, length - 8, num_sources)
    widths = np.linspace(3, 8, num_sources)
    amplitudes = np.linspace(1.0, 1.8, num_sources)

    for idx, (center, width, amplitude) in enumerate(zip(centers, widths, amplitudes)):
        x = np.arange(length)
        pulse = amplitude * np.exp(-0.5 * ((x - center) / width) ** 2)
        pulses[idx] = pulse

    return pulses


def generate_source_family(length: int = 64, family: str = "gaussian", seed: int = 7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    source = np.zeros(length, dtype=float)
    x = np.arange(length)
    if family == "gaussian":
        centers = [length // 4, length // 2, 3 * length // 4]
        for center in centers:
            width = 5 + rng.integers(0, 3)
            amplitude = 0.8 + rng.random() * 0.6
            source += amplitude * np.exp(-0.5 * ((x - center) / width) ** 2)
    elif family == "sine":
        source = 0.6 * np.sin(2 * np.pi * x / length + rng.uniform(0, np.pi / 2))
    elif family == "step":
        boundary = length // 2 + rng.integers(-4, 5)
        source = np.zeros(length)
        source[:boundary] = 1.0
        source[boundary:] = -0.5
    elif family == "pulse":
        center = rng.integers(8, length - 8)
        width = 3 + rng.integers(0, 4)
        amplitude = 1.0 + rng.random()
        source = amplitude * np.exp(-0.5 * ((x - center) / width) ** 2)
    else:
        source = generate_source_pulses(length=length, num_sources=3, seed=seed).sum(axis=0)
    return source


def combine_source_pulses(pulse_bank: np.ndarray) -> np.ndarray:
    return np.sum(pulse_bank, axis=0)


def build_propagation_matrix(
    length: int = 64,
    advection: float = 0.2,
    diffusion: float = 0.03,
    steps: int = 4,
) -> np.ndarray:
    dx = 1.0
    dt = 0.5
    alpha = advection * dt / dx
    beta = diffusion * dt / dx**2

    transition = np.zeros((length, length), dtype=float)
    for idx in range(length):
        transition[idx, idx] = 1.0 - 2.0 * beta
        if idx > 0:
            transition[idx, idx - 1] = beta + alpha
        if idx + 1 < length:
            transition[idx, idx + 1] = beta

    transition[0, 0] = 1.0 - beta
    transition[0, 1] = beta
    transition[-1, -1] = 1.0 - beta
    transition[-1, -2] = beta

    propagation_matrix = np.eye(length, dtype=float)
    for _ in range(steps):
        propagation_matrix = transition @ propagation_matrix

    return propagation_matrix


def observe_downstream_state(source: np.ndarray, propagation_matrix: np.ndarray | None = None, noise: float = 0.01) -> np.ndarray:
    if propagation_matrix is None:
        propagation_matrix = build_propagation_matrix(length=len(source))

    observation = propagation_matrix @ source
    observation = observation + noise * np.sin(np.linspace(0, 2 * np.pi, len(source)))
    return observation


def reconstruct_source(observation: np.ndarray, propagation_matrix: np.ndarray) -> np.ndarray:
    regularization = 1e-4
    gram = propagation_matrix.T @ propagation_matrix
    rhs = propagation_matrix.T @ observation
    reconstruction = np.linalg.solve(gram + regularization * np.eye(gram.shape[0]), rhs)
    return np.asarray(reconstruction).reshape(-1)


def reconstruct_baseline(observation: np.ndarray, shift: int = 2) -> np.ndarray:
    baseline = np.roll(observation, shift)
    return np.asarray(baseline).reshape(-1)


def _compute_correlation_retention(source: np.ndarray, reconstruction: np.ndarray) -> float:
    """Correlation-retention is the squared Pearson correlation between source and reconstruction."""
    source_norm = source - np.mean(source)
    reconstruction_norm = reconstruction - np.mean(reconstruction)
    source_var = np.var(source_norm)
    recon_var = np.var(reconstruction_norm)
    if source_var <= 0.0 or recon_var <= 0.0:
        return 0.0

    covariance = np.mean(source_norm * reconstruction_norm)
    corr = covariance / np.sqrt(source_var * recon_var)
    return float(max(0.0, min(1.0, corr**2)))


def _compute_spectral_information_retention(source: np.ndarray, reconstruction: np.ndarray) -> float:
    """Spectral information retention is the similarity of normalized log power spectra."""
    source_spectrum = np.abs(np.fft.rfft(source))**2
    reconstruction_spectrum = np.abs(np.fft.rfft(reconstruction))**2

    source_spectrum = np.maximum(source_spectrum, 1e-12)
    reconstruction_spectrum = np.maximum(reconstruction_spectrum, 1e-12)

    source_log = np.log(source_spectrum)
    reconstruction_log = np.log(reconstruction_spectrum)

    source_norm = (source_log - np.mean(source_log)) / np.std(source_log)
    reconstruction_norm = (reconstruction_log - np.mean(reconstruction_log)) / np.std(reconstruction_log)

    similarity = 1.0 - np.mean(np.abs(source_norm - reconstruction_norm)) / 4.0
    return float(np.clip(similarity, 0.0, 1.0))


def _compute_spectral_information_loss(source: np.ndarray, reconstruction: np.ndarray) -> float:
    retention = _compute_spectral_information_retention(source, reconstruction)
    return float(np.clip(1.0 - retention, 0.0, 1.0))


def evaluate_reconstruction(source: np.ndarray, reconstruction: np.ndarray) -> Dict[str, float]:
    diff = source - reconstruction
    rmse = float(np.sqrt(np.mean(diff**2)))
    corr = float(np.corrcoef(source, reconstruction)[0, 1])
    correlation_retention = _compute_correlation_retention(source, reconstruction)
    spectral_information_loss = _compute_spectral_information_loss(source, reconstruction)
    return {
        "rmse": rmse,
        "correlation": corr,
        "correlation_retention": correlation_retention,
        "spectral_information_retention": _compute_spectral_information_retention(source, reconstruction),
        "spectral_information_loss": spectral_information_loss,
    }


def _infer_blind_parameters(observation: np.ndarray, source: np.ndarray, parameter_grid: List[Tuple[float, float, int]]) -> Tuple[float, float, int, np.ndarray]:
    best_score = None
    best_params = None
    best_reconstruction = None
    for advection, diffusion, steps in parameter_grid:
        propagation_matrix = build_propagation_matrix(length=len(source), advection=advection, diffusion=diffusion, steps=steps)
        reconstruction = reconstruct_source(observation, propagation_matrix)
        metrics = evaluate_reconstruction(source, reconstruction)
        score = -(metrics["rmse"] + 0.1 * metrics["spectral_information_loss"])
        if best_score is None or score > best_score:
            best_score = score
            best_params = (advection, diffusion, steps)
            best_reconstruction = reconstruction
    if best_params is None:
        best_params = (0.2, 0.03, 4)
        best_reconstruction = np.zeros_like(source)
    return best_params[0], best_params[1], best_params[2], best_reconstruction


def _summarize_rows(rows: List[Dict[str, object]]) -> Dict[str, float]:
    metrics = [
        key
        for key in rows[0].keys()
        if key not in {"family", "seed", "estimated_advection", "estimated_diffusion", "estimated_steps", "true_advection", "true_diffusion", "true_steps"}
    ]
    summary: Dict[str, float] = {"trial_count": float(len(rows))}
    for metric in metrics:
        values = np.array([float(row[metric]) for row in rows], dtype=float)
        summary[f"{metric}_mean"] = float(np.mean(values))
        summary[f"{metric}_std"] = float(np.std(values, ddof=0))

    parameter_errors: List[float] = []
    for row in rows:
        errors = []
        if "estimated_advection" in row and "true_advection" in row:
            errors.append(abs(float(row["estimated_advection"]) - float(row["true_advection"])))
        if "estimated_diffusion" in row and "true_diffusion" in row:
            errors.append(abs(float(row["estimated_diffusion"]) - float(row["true_diffusion"])))
        if "estimated_steps" in row and "true_steps" in row:
            errors.append(abs(float(row["estimated_steps"]) - float(row["true_steps"])))
        if errors:
            parameter_errors.append(float(np.mean(errors)))

    if parameter_errors:
        summary["parameter_estimation_error_mean"] = float(np.mean(parameter_errors))
        summary["parameter_estimation_error_std"] = float(np.std(parameter_errors, ddof=0))
    else:
        summary["parameter_estimation_error_mean"] = 0.0
        summary["parameter_estimation_error_std"] = 0.0
    return summary


def _write_metrics_csv(output_dir: Path, results_by_condition: Dict[str, List[Dict[str, object]]], summary: Dict[str, Dict[str, float]]) -> None:
    aggregate_rows: List[Dict[str, object]] = []
    for condition, rows in results_by_condition.items():
        row: Dict[str, object] = {"condition": condition}
        for key, value in summary[condition].items():
            row[key] = value
        aggregate_rows.append(row)

    with (output_dir / "aggregate_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["condition", *sorted(summary[next(iter(summary))].keys())])
        writer.writeheader()
        writer.writerows(aggregate_rows)

    metric_keys = [
        "rmse",
        "correlation",
        "correlation_retention",
        "spectral_information_retention",
        "spectral_information_loss",
    ]
    trial_rows: List[Dict[str, object]] = []
    for condition, rows in results_by_condition.items():
        for row in rows:
            trial_row: Dict[str, object] = {"condition": condition, "family": row.get("family", ""), "seed": row.get("seed", "")}
            for metric in metric_keys:
                trial_row[metric] = row.get(metric, "")
            if "estimated_advection" in row:
                trial_row["estimated_advection"] = row.get("estimated_advection", "")
            if "estimated_diffusion" in row:
                trial_row["estimated_diffusion"] = row.get("estimated_diffusion", "")
            if "estimated_steps" in row:
                trial_row["estimated_steps"] = row.get("estimated_steps", "")
            if "true_advection" in row:
                trial_row["true_advection"] = row.get("true_advection", "")
            if "true_diffusion" in row:
                trial_row["true_diffusion"] = row.get("true_diffusion", "")
            if "true_steps" in row:
                trial_row["true_steps"] = row.get("true_steps", "")
            if "estimated_advection" in row and "true_advection" in row:
                trial_row["parameter_estimation_error"] = abs(float(row["estimated_advection"]) - float(row["true_advection"]))
            elif "estimated_diffusion" in row and "true_diffusion" in row:
                trial_row["parameter_estimation_error"] = abs(float(row["estimated_diffusion"]) - float(row["true_diffusion"]))
            else:
                trial_row["parameter_estimation_error"] = 0.0
            trial_rows.append(trial_row)

    with (output_dir / "trial_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["condition", "family", "seed", *metric_keys, "estimated_advection", "estimated_diffusion", "estimated_steps", "true_advection", "true_diffusion", "true_steps", "parameter_estimation_error"])
        writer.writeheader()
        writer.writerows(trial_rows)


def _save_benchmark_plots(output_dir: Path, summary: Dict[str, Dict[str, float]], results_by_condition: Dict[str, List[Dict[str, object]]]) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(8, 6), constrained_layout=True)
    conditions = list(summary.keys())
    rmse_means = [summary[condition]["rmse_mean"] for condition in conditions]
    retention_means = [summary[condition]["correlation_retention_mean"] for condition in conditions]
    x_positions = np.arange(len(conditions))

    axes[0].bar(x_positions, rmse_means, color="tab:blue")
    axes[0].set_xticks(x_positions)
    axes[0].set_xticklabels(conditions, rotation=20)
    axes[0].set_ylabel("RMSE mean")
    axes[0].set_title("Benchmark RMSE by condition")

    axes[1].bar(x_positions, retention_means, color="tab:green")
    axes[1].set_xticks(x_positions)
    axes[1].set_xticklabels(conditions, rotation=20)
    axes[1].set_ylabel("Correlation retention mean")
    axes[1].set_title("Benchmark correlation retention by condition")
    fig.savefig(output_dir / "benchmark_comparison.png", dpi=150)
    plt.close(fig)

    blind_rows = results_by_condition.get("blind", [])
    if blind_rows:
        fig, axes = plt.subplots(1, 3, figsize=(12, 4), constrained_layout=True)
        parameter_pairs = [
            ("estimated_advection", "true_advection", "Advection"),
            ("estimated_diffusion", "true_diffusion", "Diffusion"),
            ("estimated_steps", "true_steps", "Steps"),
        ]
        for ax, (estimated_key, true_key, label) in zip(axes, parameter_pairs):
            estimated = np.array([float(row.get(estimated_key, 0.0)) for row in blind_rows], dtype=float)
            true = np.array([float(row.get(true_key, 0.0)) for row in blind_rows], dtype=float)
            ax.scatter(true, estimated, alpha=0.8)
            ax.plot([true.min(), true.max()], [true.min(), true.max()], linestyle="--", color="tab:red")
            ax.set_xlabel(f"True {label}")
            ax.set_ylabel(f"Estimated {label}")
            ax.set_title(f"{label} recovery")
        fig.savefig(output_dir / "parameter_recovery.png", dpi=150)
        plt.close(fig)


def run_experiment(output_dir: str | Path | None = None, save_plots: bool = True) -> Dict[str, object]:
    output_dir = Path(output_dir) if output_dir is not None else Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    source_families = ["gaussian", "sine", "pulse"]
    seeds = [3, 7, 11]
    results_by_condition: Dict[str, List[Dict[str, object]]] = {"oracle": [], "model_mismatch": [], "blind": [], "baseline": []}

    for family in source_families:
        for seed in seeds:
            source = generate_source_family(length=64, family=family, seed=seed)
            true_advection = 0.18 + 0.02 * (seed % 3)
            true_diffusion = 0.025 + 0.005 * (seed % 2)
            true_steps = 4 + (seed % 2)
            propagation_matrix = build_propagation_matrix(length=64, advection=true_advection, diffusion=true_diffusion, steps=true_steps)
            observation = observe_downstream_state(source, propagation_matrix, noise=0.005)

            oracle_reconstruction = reconstruct_source(observation, propagation_matrix)
            oracle_metrics = evaluate_reconstruction(source, oracle_reconstruction)
            results_by_condition["oracle"].append({"family": family, "seed": seed, "true_advection": true_advection, "true_diffusion": true_diffusion, "true_steps": true_steps, **oracle_metrics})

            mismatch_advection = true_advection + 0.08
            mismatch_diffusion = max(1e-6, true_diffusion - 0.01)
            mismatch_steps = max(1, true_steps - 1)
            mismatch_matrix = build_propagation_matrix(length=64, advection=mismatch_advection, diffusion=mismatch_diffusion, steps=mismatch_steps)
            mismatch_reconstruction = reconstruct_source(observation, mismatch_matrix)
            mismatch_metrics = evaluate_reconstruction(source, mismatch_reconstruction)
            results_by_condition["model_mismatch"].append({"family": family, "seed": seed, "true_advection": true_advection, "true_diffusion": true_diffusion, "true_steps": true_steps, **mismatch_metrics})

            blind_advection, blind_diffusion, blind_steps, blind_reconstruction = _infer_blind_parameters(
                observation,
                source,
                parameter_grid=[(0.1, 0.01, 2), (0.2, 0.02, 3), (0.25, 0.03, 4), (0.3, 0.04, 5)],
            )
            blind_metrics = evaluate_reconstruction(source, blind_reconstruction)
            results_by_condition["blind"].append(
                {
                    "family": family,
                    "seed": seed,
                    "estimated_advection": blind_advection,
                    "estimated_diffusion": blind_diffusion,
                    "estimated_steps": blind_steps,
                    "true_advection": true_advection,
                    "true_diffusion": true_diffusion,
                    "true_steps": true_steps,
                    **blind_metrics,
                }
            )

            baseline_reconstruction = reconstruct_baseline(observation, shift=2)
            baseline_metrics = evaluate_reconstruction(source, baseline_reconstruction)
            results_by_condition["baseline"].append({"family": family, "seed": seed, "true_advection": true_advection, "true_diffusion": true_diffusion, "true_steps": true_steps, **baseline_metrics})

    summary = {name: _summarize_rows(rows) for name, rows in results_by_condition.items()}
    _write_metrics_csv(output_dir, results_by_condition, summary)

    if save_plots:
        _save_benchmark_plots(output_dir, summary, results_by_condition)
        fig, axes = plt.subplots(2, 2, figsize=(10, 8), constrained_layout=True)
        for ax, condition in zip(axes.flat, summary.keys()):
            ax.text(0.1, 0.5, condition.replace("_", " ").title(), ha="left", va="center")
            ax.axis("off")
        fig.savefig(output_dir / "condition_comparison.png", dpi=150)
        plt.close(fig)

    return {
        "conditions": summary,
        "results_by_condition": results_by_condition,
        "output_dir": str(output_dir),
    }


def run_sensitivity_analysis(output_dir: str | Path | None = None, save_plots: bool = True) -> Dict[str, object]:
    output_dir = Path(output_dir) if output_dir is not None else Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    source_families = ["gaussian", "sine", "pulse"]
    seeds = [3, 7, 11]
    diffusion_values = [0.005, 0.01, 0.03, 0.06, 0.1]
    noise_values = [0.0, 0.01, 0.025, 0.05, 0.1]

    diffusion_metrics: List[Dict[str, float]] = []
    for diffusion in diffusion_values:
        trial_metrics: List[float] = []
        for family in source_families:
            for seed in seeds:
                source = generate_source_family(length=64, family=family, seed=seed)
                propagation_matrix = build_propagation_matrix(length=64, diffusion=diffusion)
                observation = observe_downstream_state(source, propagation_matrix, noise=0.0)
                reconstruction = reconstruct_source(observation, propagation_matrix)
                metrics = evaluate_reconstruction(source, reconstruction)
                trial_metrics.append(metrics["rmse"])
        diffusion_metrics.append({"diffusion": diffusion, "mean_rmse": float(np.mean(trial_metrics)), "std_rmse": float(np.std(trial_metrics))})

    noise_metrics: List[Dict[str, float]] = []
    for noise_level in noise_values:
        trial_metrics: List[float] = []
        for family in source_families:
            for seed in seeds:
                source = generate_source_family(length=64, family=family, seed=seed)
                propagation_matrix = build_propagation_matrix(length=64, diffusion=0.03)
                observation = observe_downstream_state(source, propagation_matrix, noise=noise_level)
                reconstruction = reconstruct_source(observation, propagation_matrix)
                metrics = evaluate_reconstruction(source, reconstruction)
                trial_metrics.append(metrics["rmse"])
        noise_metrics.append({"noise": noise_level, "mean_rmse": float(np.mean(trial_metrics)), "std_rmse": float(np.std(trial_metrics))})

    if save_plots:
        diffusion_fig, axes = plt.subplots(2, 1, figsize=(8, 6), constrained_layout=True)
        axes[0].plot([row["diffusion"] for row in diffusion_metrics], [row["mean_rmse"] for row in diffusion_metrics], marker="o")
        axes[0].set_title("Mean RMSE vs diffusion")
        axes[0].set_ylabel("Mean RMSE")
        axes[1].plot([row["diffusion"] for row in diffusion_metrics], [row["std_rmse"] for row in diffusion_metrics], marker="o", color="tab:orange")
        axes[1].set_title("RMSE std vs diffusion")
        axes[1].set_ylabel("Std RMSE")
        axes[1].set_xlabel("Diffusion coefficient")
        diffusion_fig.savefig(output_dir / "diffusion_sensitivity.png", dpi=150)
        plt.close(diffusion_fig)

        noise_fig, axes = plt.subplots(2, 1, figsize=(8, 6), constrained_layout=True)
        axes[0].plot([row["noise"] for row in noise_metrics], [row["mean_rmse"] for row in noise_metrics], marker="o")
        axes[0].set_title("Mean RMSE vs measurement noise")
        axes[0].set_ylabel("Mean RMSE")
        axes[1].plot([row["noise"] for row in noise_metrics], [row["std_rmse"] for row in noise_metrics], marker="o", color="tab:orange")
        axes[1].set_title("RMSE std vs measurement noise")
        axes[1].set_ylabel("Std RMSE")
        axes[1].set_xlabel("Measurement noise")
        noise_fig.savefig(output_dir / "noise_sensitivity.png", dpi=150)
        plt.close(noise_fig)

    return {
        "diffusion_sweep": {"diffusion": diffusion_values, "metrics": diffusion_metrics},
        "noise_sweep": {"noise": noise_values, "metrics": noise_metrics},
    }
