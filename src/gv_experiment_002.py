from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.gv_experiment_001 import (
    build_propagation_matrix,
    generate_source_family,
    observe_downstream_state,
    reconstruct_baseline,
    reconstruct_source,
)


def _make_mask(length: int, fraction: float, strategy: str, seed: int) -> np.ndarray:
    if strategy == "uniform":
        if fraction >= 1.0:
            return np.ones(length, dtype=bool)
        count = max(1, int(round(length * fraction)))
        indices = np.linspace(0, length - 1, count, dtype=int)
        mask = np.zeros(length, dtype=bool)
        mask[indices] = True
        return mask

    if strategy == "window":
        if fraction >= 1.0:
            return np.ones(length, dtype=bool)
        count = max(1, int(round(length * fraction)))
        start = (length - count) // 2
        mask = np.zeros(length, dtype=bool)
        mask[start:start + count] = True
        return mask

    if strategy == "random":
        rng = np.random.default_rng(seed)
        if fraction >= 1.0:
            return np.ones(length, dtype=bool)
        keep_prob = float(fraction)
        return rng.random(length) < keep_prob

    raise ValueError(f"unsupported strategy: {strategy}")


def _clip_metric_value(value: float, lower: float, upper: float) -> float:
    if lower <= value <= upper:
        return float(value)
    if value > upper and value < upper + 1e-12:
        return float(upper)
    if value < lower and value > lower - 1e-12:
        return float(lower)
    return float(np.clip(value, lower, upper))


def _evaluate_reconstruction(source: np.ndarray, reconstruction: np.ndarray) -> Dict[str, float]:
    diff = source - reconstruction
    rmse = float(np.sqrt(np.mean(diff**2)))

    source_array = np.asarray(source, dtype=float)
    reconstruction_array = np.asarray(reconstruction, dtype=float)
    if source_array.size == 0 or reconstruction_array.size == 0:
        corr = np.nan
    else:
        source_centered = source_array - np.mean(source_array)
        reconstruction_centered = reconstruction_array - np.mean(reconstruction_array)
        denominator = np.sqrt(np.sum(source_centered**2) * np.sum(reconstruction_centered**2))
        if denominator <= 1e-12:
            corr = np.nan
        else:
            corr = float(np.sum(source_centered * reconstruction_centered) / denominator)
    if np.isfinite(corr):
        # Pearson correlation is mathematically bounded to [-1, 1]; this clip only guards tiny
        # floating-point excursions from the exact algebraic formula.
        corr = _clip_metric_value(corr, -1.0, 1.0)
    correlation_retention = np.nan if not np.isfinite(corr) else _clip_metric_value(corr**2, 0.0, 1.0)

    source_spectrum = np.abs(np.fft.rfft(source))**2
    reconstruction_spectrum = np.abs(np.fft.rfft(reconstruction))**2
    source_spectrum = np.maximum(source_spectrum, 1e-12)
    reconstruction_spectrum = np.maximum(reconstruction_spectrum, 1e-12)
    source_log = np.log(source_spectrum)
    reconstruction_log = np.log(reconstruction_spectrum)

    source_std = np.std(source_log)
    reconstruction_std = np.std(reconstruction_log)
    if source_std <= 1e-12:
        source_norm = np.zeros_like(source_log)
    else:
        source_norm = (source_log - np.mean(source_log)) / source_std
    if reconstruction_std <= 1e-12:
        reconstruction_norm = np.zeros_like(reconstruction_log)
    else:
        reconstruction_norm = (reconstruction_log - np.mean(reconstruction_log)) / reconstruction_std

    # Spectral-information retention is mathematically bounded to [0, 1]; the clip is only to absorb
    # tiny rounding noise from the normalization step.
    spectral_information_retention = 1.0 - np.mean(np.abs(source_norm - reconstruction_norm)) / 4.0
    spectral_information_retention = _clip_metric_value(float(spectral_information_retention), 0.0, 1.0)
    spectral_information_loss = _clip_metric_value(1.0 - spectral_information_retention, 0.0, 1.0)
    return {
        "rmse": rmse,
        "correlation": corr,
        "correlation_retention": correlation_retention,
        "spectral_information_retention": spectral_information_retention,
        "spectral_information_loss": spectral_information_loss,
    }


def _infer_blind_parameters(observation: np.ndarray, source: np.ndarray, parameter_grid: List[Tuple[float, float, int]]) -> Tuple[float, float, int, np.ndarray]:
    best_score = None
    best_params = None
    best_reconstruction = None
    for advection, diffusion, steps in parameter_grid:
        propagation_matrix = build_propagation_matrix(length=len(source), advection=advection, diffusion=diffusion, steps=steps)
        reconstruction = reconstruct_source(observation, propagation_matrix)
        metrics = _evaluate_reconstruction(source, reconstruction)
        score = -(metrics["rmse"] + 0.1 * metrics["spectral_information_loss"])
        if best_score is None or score > best_score:
            best_score = score
            best_params = (advection, diffusion, steps)
            best_reconstruction = reconstruction
    if best_params is None:
        best_params = (0.2, 0.03, 4)
        best_reconstruction = np.zeros_like(source)
    return best_params[0], best_params[1], best_params[2], best_reconstruction


def _interpolate_and_invert(observation: np.ndarray, mask: np.ndarray) -> np.ndarray:
    observed_index = np.flatnonzero(mask)
    if len(observed_index) < 2:
        return np.zeros_like(observation, dtype=float)
    if np.all(mask):
        return observation
    interpolated = np.interp(np.arange(len(observation)), observed_index, observation[observed_index])
    return interpolated


def _bootstrap_mean_interval(values: List[float], confidence: float = 0.95, n_boot: int = 2000, seed: int = 7) -> Tuple[float, float]:
    if not values:
        return float("nan"), float("nan")
    array = np.asarray(values, dtype=float)
    finite = array[np.isfinite(array)]
    if finite.size == 0:
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    samples = rng.choice(finite, size=(n_boot, finite.size), replace=True)
    boot_means = np.mean(samples, axis=1)
    lower = np.quantile(boot_means, (1.0 - confidence) / 2.0)
    upper = np.quantile(boot_means, 1.0 - (1.0 - confidence) / 2.0)
    return float(lower), float(upper)


def _spearman_correlation(x_values: List[float], y_values: List[float]) -> float:
    x = np.asarray(x_values, dtype=float)
    y = np.asarray(y_values, dtype=float)
    if x.size != y.size or x.size < 2:
        return float("nan")
    ranked_x = np.empty_like(x, dtype=float)
    ranked_y = np.empty_like(y, dtype=float)
    for idx, values in enumerate([x, y]):
        order = np.argsort(values)
        ranks = np.empty(values.size, dtype=float)
        for position, original_index in enumerate(order):
            ranks[original_index] = position + 1.0
        if idx == 0:
            ranked_x = ranks
        else:
            ranked_y = ranks
    centered_x = ranked_x - np.mean(ranked_x)
    centered_y = ranked_y - np.mean(ranked_y)
    denominator = np.sqrt(np.sum(centered_x**2) * np.sum(centered_y**2))
    if denominator <= 1e-12:
        return float("nan")
    return float(np.sum(centered_x * centered_y) / denominator)


def _summarize_rows(rows: List[Dict[str, object]]) -> Dict[str, float]:
    metric_names = ["rmse", "correlation", "correlation_retention", "spectral_information_loss", "parameter_estimation_error"]
    summary: Dict[str, float] = {"trial_count": float(len(rows))}
    for metric in metric_names:
        values = np.array([float(row[metric]) for row in rows], dtype=float)
        finite_values = values[np.isfinite(values)]
        summary[f"{metric}_mean"] = float(np.mean(finite_values)) if finite_values.size else float("nan")
        summary[f"{metric}_std"] = float(np.std(finite_values, ddof=0)) if finite_values.size > 1 else 0.0
        summary[f"{metric}_undefined_count"] = int(np.sum(~np.isfinite(values)))
    return summary


def _aggregate_trial_metrics(trial_metrics: List[Dict[str, object]], conditions: List[str], strategies: List[str], fractions: List[float]) -> List[Dict[str, object]]:
    aggregate_metrics: List[Dict[str, object]] = []
    for condition in conditions:
        for strategy in strategies:
            for fraction in fractions:
                rows = [row for row in trial_metrics if row["condition"] == condition and row["mask_strategy"] == strategy and row["observation_fraction"] == fraction]
                if rows:
                    summary = _summarize_rows(rows)
                    aggregate_metrics.append({
                        "condition": condition,
                        "mask_strategy": strategy,
                        "observation_fraction": float(fraction),
                        "trial_count": int(summary["trial_count"]),
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
                        "correlation_undefined_count": int(summary["correlation_undefined_count"]),
                    })
    return aggregate_metrics


def _analyze_metric_trends(trial_metrics: List[Dict[str, object]]) -> List[Dict[str, object]]:
    analyses: List[Dict[str, object]] = []
    for condition in ["oracle", "blind", "interpolation_baseline", "naive_baseline"]:
        for strategy in ["uniform", "window", "random"]:
            rows = [row for row in trial_metrics if row["condition"] == condition and row["mask_strategy"] == strategy]
            if not rows:
                continue
            fractions = sorted({float(row["observation_fraction"]) for row in rows})
            for metric in ["rmse", "correlation", "correlation_retention", "spectral_information_loss"]:
                per_fraction_values: List[List[float]] = []
                per_fraction_uncertainty: List[Dict[str, object]] = []
                for fraction in fractions:
                    values = [float(row[metric]) for row in rows if float(row["observation_fraction"]) == fraction and np.isfinite(float(row[metric]))]
                    if not values:
                        continue
                    lower, upper = _bootstrap_mean_interval(values)
                    per_fraction_values.append(values)
                    per_fraction_uncertainty.append({
                        "fraction": fraction,
                        "mean": float(np.mean(values)),
                        "std": float(np.std(values, ddof=0)),
                        "ci95_lower": lower,
                        "ci95_upper": upper,
                    })
                if len(per_fraction_uncertainty) < 2:
                    continue
                means = [item["mean"] for item in per_fraction_uncertainty]
                if metric in {"rmse", "spectral_information_loss"}:
                    increases = sum(1 for earlier, later in zip(means, means[1:]) if later > earlier)
                    decreases = sum(1 for earlier, later in zip(means, means[1:]) if later < earlier)
                else:
                    increases = sum(1 for earlier, later in zip(means, means[1:]) if later > earlier)
                    decreases = sum(1 for earlier, later in zip(means, means[1:]) if later < earlier)
                analyses.append({
                    "condition": condition,
                    "mask_strategy": strategy,
                    "metric": metric,
                    "fractions": fractions,
                    "adjacent_increases": increases,
                    "adjacent_decreases": decreases,
                    "spearman_correlation": _spearman_correlation(fractions, means),
                    "uncertainty": per_fraction_uncertainty,
                })
    return analyses


def _evaluate_preregistered_hypothesis(trial_metrics: List[Dict[str, object]]) -> Dict[str, object]:
    matched_rows = [
        row
        for row in trial_metrics
        if row["condition"] in {"blind", "naive_baseline"}
        and row["mask_strategy"] == "uniform"
        and row["observation_fraction"] == 0.5
    ]
    by_trial: Dict[Tuple[str, int], Dict[str, Dict[str, object]]] = {}
    for row in matched_rows:
        key = (str(row["family"]), int(row["seed"]))
        by_trial.setdefault(key, {})[str(row["condition"])] = row

    paired_differences: List[float] = []
    for group in by_trial.values():
        blind_row = group.get("blind")
        naive_row = group.get("naive_baseline")
        if blind_row is None or naive_row is None:
            continue
        blind_value = float(blind_row["rmse"])
        naive_value = float(naive_row["rmse"])
        paired_differences.append(naive_value - blind_value)

    if not paired_differences:
        return {
            "metric": "rmse",
            "paired_differences": [],
            "mean_difference": float("nan"),
            "ci95_lower": float("nan"),
            "ci95_upper": float("nan"),
            "win_rate": float("nan"),
            "n_pairs": 0,
        }

    lower, upper = _bootstrap_mean_interval(paired_differences)
    return {
        "metric": "rmse",
        "paired_differences": paired_differences,
        "mean_difference": float(np.mean(paired_differences)),
        "ci95_lower": lower,
        "ci95_upper": upper,
        "win_rate": float(np.mean(np.array(paired_differences) > 0.0)),
        "n_pairs": len(paired_differences),
    }


def _write_csv(output_dir: Path, trial_metrics: List[Dict[str, object]], aggregate_metrics: List[Dict[str, object]]) -> None:
    trial_fields = ["condition", "mask_strategy", "observation_fraction", "family", "seed", "rmse", "correlation", "correlation_retention", "spectral_information_loss", "parameter_estimation_error"]
    serializable_trial_metrics = []
    for row in trial_metrics:
        serializable_row = {field: row[field] for field in trial_fields if field in row}
        serializable_trial_metrics.append(serializable_row)

    with (output_dir / "exp002_trial_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=trial_fields)
        writer.writeheader()
        writer.writerows(serializable_trial_metrics)

    aggregate_fields = ["condition", "mask_strategy", "observation_fraction", "trial_count", "rmse_mean", "rmse_std", "correlation_mean", "correlation_std", "correlation_retention_mean", "correlation_retention_std", "spectral_information_loss_mean", "spectral_information_loss_std", "parameter_estimation_error_mean", "parameter_estimation_error_std", "correlation_undefined_count"]
    with (output_dir / "exp002_aggregate_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=aggregate_fields)
        writer.writeheader()
        writer.writerows(aggregate_metrics)


def _save_plots(output_dir: Path, aggregate_metrics: List[Dict[str, object]], example_rows: List[Dict[str, object]]) -> None:
    fractions = sorted({float(row["observation_fraction"]) for row in aggregate_metrics if row["condition"] == "blind"})
    by_fraction: Dict[float, List[float]] = {fraction: [] for fraction in fractions}
    for row in aggregate_metrics:
        if row["condition"] == "blind" and row["mask_strategy"] == "uniform":
            by_fraction[float(row["observation_fraction"])].append(float(row["rmse_mean"]))

    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
    for fraction in fractions:
        values = by_fraction[fraction]
        ax.plot([fraction], [np.mean(values)], marker="o", label=f"{fraction:.0%}")
    ax.set_xlabel("Observed fraction")
    ax.set_ylabel("Mean RMSE")
    ax.set_title("Observation fraction vs RMSE")
    ax.legend()
    fig.savefig(output_dir / "exp002_observation_fraction.png", dpi=150)
    plt.close(fig)

    strategies = sorted({row["mask_strategy"] for row in aggregate_metrics if row["condition"] == "blind"})
    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
    for strategy in strategies:
        rows = [row for row in aggregate_metrics if row["condition"] == "blind" and row["mask_strategy"] == strategy and float(row["observation_fraction"]) == 0.5]
        if rows:
            ax.bar([strategy], [float(rows[0]["rmse_mean"])], label=strategy)
    ax.set_ylabel("Mean RMSE")
    ax.set_title("Mask strategy comparison at 50% observation")
    ax.legend()
    fig.savefig(output_dir / "exp002_mask_comparison.png", dpi=150)
    plt.close(fig)

    if example_rows:
        fig, axes = plt.subplots(1, 3, figsize=(12, 4), constrained_layout=True)
        for ax, row in zip(axes, example_rows[:3]):
            ax.plot(row["source"], label="source")
            ax.plot(row["reconstruction"], label="reconstruction", alpha=0.8)
            ax.set_title(f"{row['condition']} / {row['mask_strategy']}")
            ax.legend(loc="upper right")
        fig.savefig(output_dir / "exp002_example_reconstructions.png", dpi=150)
        plt.close(fig)


def run_experiment(output_dir: str | Path | None = None, save_plots: bool = True) -> Dict[str, object]:
    output_dir = Path(output_dir) if output_dir is not None else Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    source_families = ["gaussian", "sine", "pulse"]
    seeds = [3, 7, 11]
    fractions = [1.0, 0.75, 0.5, 0.25, 0.1]
    strategies = ["uniform", "window", "random"]
    conditions = ["oracle", "blind", "interpolation_baseline", "naive_baseline"]

    trial_metrics: List[Dict[str, object]] = []
    aggregate_metrics: List[Dict[str, object]] = []
    example_rows: List[Dict[str, object]] = []

    for family in source_families:
        for seed in seeds:
            source = generate_source_family(length=64, family=family, seed=seed)
            true_advection = 0.18 + 0.02 * (seed % 3)
            true_diffusion = 0.025 + 0.005 * (seed % 2)
            true_steps = 4 + (seed % 2)
            propagation_matrix = build_propagation_matrix(length=64, advection=true_advection, diffusion=true_diffusion, steps=true_steps)
            observation = observe_downstream_state(source, propagation_matrix, noise=0.005)

            for strategy in strategies:
                for fraction in fractions:
                    mask = _make_mask(len(observation), fraction, strategy, seed)
                    observed = observation.copy()
                    observed[~mask] = np.nan
                    observed_value = np.nan_to_num(observed, nan=0.0)
                    interpolated_observation = _interpolate_and_invert(observation, mask)

                    oracle_reconstruction = reconstruct_source(interpolated_observation, propagation_matrix)
                    oracle_metrics = _evaluate_reconstruction(source, oracle_reconstruction)
                    trial_metrics.append({
                        "condition": "oracle",
                        "mask_strategy": strategy,
                        "observation_fraction": float(fraction),
                        "family": family,
                        "seed": seed,
                        "rmse": oracle_metrics["rmse"],
                        "correlation": oracle_metrics["correlation"],
                        "correlation_retention": oracle_metrics["correlation_retention"],
                        "spectral_information_loss": oracle_metrics["spectral_information_loss"],
                        "parameter_estimation_error": 0.0,
                        "source_array": source,
                        "reconstruction_array": oracle_reconstruction,
                    })

                    blind_advection, blind_diffusion, blind_steps, blind_reconstruction = _infer_blind_parameters(
                        interpolated_observation,
                        source,
                        parameter_grid=[(0.1, 0.01, 2), (0.2, 0.02, 3), (0.25, 0.03, 4), (0.3, 0.04, 5)],
                    )
                    blind_metrics = _evaluate_reconstruction(source, blind_reconstruction)
                    trial_metrics.append({
                        "condition": "blind",
                        "mask_strategy": strategy,
                        "observation_fraction": float(fraction),
                        "family": family,
                        "seed": seed,
                        "rmse": blind_metrics["rmse"],
                        "correlation": blind_metrics["correlation"],
                        "correlation_retention": blind_metrics["correlation_retention"],
                        "spectral_information_loss": blind_metrics["spectral_information_loss"],
                        "parameter_estimation_error": float(np.mean([abs(blind_advection - true_advection), abs(blind_diffusion - true_diffusion), abs(blind_steps - true_steps)])),
                        "source_array": source,
                        "reconstruction_array": blind_reconstruction,
                    })

                    interpolation_reconstruction = _interpolate_and_invert(observation, mask)
                    interpolation_metrics = _evaluate_reconstruction(source, interpolation_reconstruction)
                    trial_metrics.append({
                        "condition": "interpolation_baseline",
                        "mask_strategy": strategy,
                        "observation_fraction": float(fraction),
                        "family": family,
                        "seed": seed,
                        "rmse": interpolation_metrics["rmse"],
                        "correlation": interpolation_metrics["correlation"],
                        "correlation_retention": interpolation_metrics["correlation_retention"],
                        "spectral_information_loss": interpolation_metrics["spectral_information_loss"],
                        "parameter_estimation_error": 0.0,
                        "source_array": source,
                        "reconstruction_array": interpolation_reconstruction,
                    })

                    naive_reconstruction = np.zeros_like(source)
                    naive_metrics = _evaluate_reconstruction(source, naive_reconstruction)
                    trial_metrics.append({
                        "condition": "naive_baseline",
                        "mask_strategy": strategy,
                        "observation_fraction": float(fraction),
                        "family": family,
                        "seed": seed,
                        "rmse": naive_metrics["rmse"],
                        "correlation": naive_metrics["correlation"],
                        "correlation_retention": naive_metrics["correlation_retention"],
                        "spectral_information_loss": naive_metrics["spectral_information_loss"],
                        "parameter_estimation_error": 0.0,
                        "source_array": source,
                        "reconstruction_array": naive_reconstruction,
                    })

                    if strategy == "uniform" and fraction == 0.5 and family == "gaussian" and seed == 3 and len(example_rows) < 3:
                        example_rows.append({"condition": "blind", "mask_strategy": strategy, "source": source, "reconstruction": blind_reconstruction})

    aggregate_metrics = _aggregate_trial_metrics(trial_metrics, conditions, strategies, fractions)
    trend_analysis = _analyze_metric_trends(trial_metrics)
    preregistered_hypothesis = _evaluate_preregistered_hypothesis(trial_metrics)

    _write_csv(output_dir, trial_metrics, aggregate_metrics)
    if save_plots:
        _save_plots(output_dir, aggregate_metrics, example_rows)

    return {
        "trial_metrics": trial_metrics,
        "aggregate_metrics": aggregate_metrics,
        "trend_analysis": trend_analysis,
        "preregistered_hypothesis": preregistered_hypothesis,
        "example_rows": example_rows,
        "output_dir": str(output_dir),
    }
