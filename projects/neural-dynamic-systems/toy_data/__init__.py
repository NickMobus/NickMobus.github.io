"""Reusable toy non-stationary coin data package."""

from .generation import (
    generate_nonstationary_coin_flips,
    generate_nonstationary_coin_flips_probabilistic,
    p_series_from_flips,
    reconstruct_steps_from_flips_and_regimes,
)
from .adapters import (
    build_autoregressive_dataset,
    build_autoregressive_dataset_from_sim,
    build_sequence_dataset,
    build_sequence_dataset_from_sim,
)
from .plotting import (
    compute_true_vs_pred_metrics,
    compute_true_vs_pred_metrics_from_model,
    compute_true_vs_pred_metrics_torch_sequence,
    get_model_probability_outputs,
    get_torch_sequence_model_probability_outputs,
    plot_true_vs_pred_p_over_samples,
    plot_true_vs_pred_p_over_samples_torch_sequence,
    save_metrics_comparison_table_png,
)

__all__ = [
    "generate_nonstationary_coin_flips",
    "generate_nonstationary_coin_flips_probabilistic",
    "p_series_from_flips",
    "reconstruct_steps_from_flips_and_regimes",
    "build_autoregressive_dataset",
    "build_autoregressive_dataset_from_sim",
    "build_sequence_dataset",
    "build_sequence_dataset_from_sim",
    "compute_true_vs_pred_metrics",
    "compute_true_vs_pred_metrics_from_model",
    "compute_true_vs_pred_metrics_torch_sequence",
    "get_model_probability_outputs",
    "get_torch_sequence_model_probability_outputs",
    "plot_true_vs_pred_p_over_samples",
    "plot_true_vs_pred_p_over_samples_torch_sequence",
    "save_metrics_comparison_table_png",
]
