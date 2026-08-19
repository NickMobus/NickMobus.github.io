from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any
import math


def get_model_probability_outputs(
    model: Any,
    X: Sequence[Any],
    predictor: Callable[[Any, Any], float] | None = None,
) -> list[float]:
    """
    Return model probabilities for each sample in X.

    By default this assumes `model(sample)` returns a scalar probability.
    For PyTorch or other frameworks where different preprocessing is needed,
    pass a custom `predictor(model, sample) -> float`.
    """
    preds: list[float] = []

    if predictor is None:
        if not callable(model):
            raise ValueError("model must be callable when predictor is not provided")

        for x in X:
            pred = float(model(x))
            preds.append(pred)
        return preds

    for x in X:
        pred = float(predictor(model, x))
        preds.append(pred)

    return preds


def plot_true_vs_pred_p_over_samples(
    model: Any,
    X: Sequence[Any],
    p_true: Sequence[float],
    predictor: Callable[[Any, Any], float] | None = None,
    max_points: int | None = None,
    save_path: str | Path = "true_vs_pred_p_over_samples.png",
    show: bool = True,
    title: str = "True vs Predicted P(head) Across Samples",
) -> list[float]:
    """
    Plot true latent p and model-predicted p over sample index.

    Args:
        model: trained model object
        X: model inputs aligned with p_true
        p_true: true p values aligned with each input sample
        predictor: optional function predictor(model, sample) -> probability
        max_points: optionally limit number of points for readability
        save_path: where the generated figure is saved
        show: whether to display the figure with matplotlib
        title: title string displayed on the plot

    Returns:
        List of predicted probabilities for the plotted samples.
    """
    import matplotlib.pyplot as plt

    if len(X) != len(p_true):
        raise ValueError("X and p_true must have the same length")

    p_pred = get_model_probability_outputs(model=model, X=X, predictor=predictor)

    if len(p_pred) != len(p_true):
        raise ValueError("Predicted probabilities and p_true must have the same length")

    if max_points is not None:
        if max_points <= 0:
            raise ValueError("max_points must be positive when provided")
        n_points = min(max_points, len(p_true))
    else:
        n_points = len(p_true)

    x_plot = list(range(n_points))
    p_true_plot = list(p_true[:n_points])
    p_pred_plot = p_pred[:n_points]

    plt.figure(figsize=(10, 4.5))
    plt.plot(x_plot, p_true_plot, label="True p", linewidth=2)
    plt.plot(x_plot, p_pred_plot, label="Model predicted p", alpha=0.85)
    plt.xlabel("Sample index")
    plt.ylabel("P(head)")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    if show:
        plt.show()

    return p_pred_plot


def save_metrics_comparison_table_png(
    metrics_by_split: dict[str, dict[str, float]],
    save_path: str | Path,
) -> None:
    """
    Render a multi-split metrics comparison as a single PNG table.

    Args:
        metrics_by_split: ordered dict mapping split name (e.g. "Train", "Test")
            to a metrics dict containing 'mae', 'rmse', and 'corr'.
        save_path: path to write the PNG file.

    Example:
        save_metrics_comparison_table_png(
            {"Train": metrics_train, "Test": metrics_test},
            save_path="metrics_comparison.png",
        )
    """
    import matplotlib.pyplot as plt

    fmt = lambda v: f"{v:.4f}" if not math.isnan(v) else "NaN"

    col_labels = ["Split", "MAE", "RMSE", "Corr"]
    rows = [
        [split, fmt(m["mae"]), fmt(m["rmse"]), fmt(m["corr"])]
        for split, m in metrics_by_split.items()
    ]

    fig_h = 0.5 + 0.4 * (len(rows) + 1)
    fig, ax = plt.subplots(figsize=(5.5, fig_h))
    ax.axis("off")
    tbl = ax.table(
        cellText=rows,
        colLabels=col_labels,
        cellLoc="center",
        loc="center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(11)
    tbl.scale(1, 1.6)
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _save_metrics_table_png(
    metrics: dict[str, float],
    save_path: str | Path,
) -> None:
    """Render a single-split metrics dict as a table and save it to a PNG file."""
    import matplotlib.pyplot as plt

    fmt = lambda v: f"{v:.4f}" if not math.isnan(v) else "NaN"
    rows = [["MAE", fmt(metrics["mae"])],
            ["RMSE", fmt(metrics["rmse"])],
            ["Corr", fmt(metrics["corr"])]]

    fig, ax = plt.subplots(figsize=(3.2, 1.4))
    ax.axis("off")
    tbl = ax.table(
        cellText=rows,
        colLabels=["Metric", "Value"],
        cellLoc="center",
        loc="center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(11)
    tbl.scale(1, 1.6)
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def compute_true_vs_pred_metrics(
    p_true: Sequence[float],
    p_pred: Sequence[float],
    table_save_path: str | Path | None = None,
) -> dict[str, float]:
    """
    Compute regression-style fit metrics for latent probability tracking.

    Returns a dictionary with:
    - mae: mean absolute error
    - rmse: root mean squared error
    - corr: Pearson correlation (NaN if variance is zero)

    Args:
        p_true: true latent probabilities
        p_pred: model-predicted probabilities
        table_save_path: optional path to save a PNG table of the metrics
    """
    if len(p_true) != len(p_pred):
        raise ValueError("p_true and p_pred must have the same length")
    if len(p_true) == 0:
        raise ValueError("p_true and p_pred must be non-empty")

    n = len(p_true)
    abs_err_sum = 0.0
    sq_err_sum = 0.0

    for yt, yp in zip(p_true, p_pred):
        err = float(yp) - float(yt)
        abs_err_sum += abs(err)
        sq_err_sum += err * err

    mae = abs_err_sum / n
    rmse = math.sqrt(sq_err_sum / n)

    mean_true = sum(float(v) for v in p_true) / n
    mean_pred = sum(float(v) for v in p_pred) / n

    cov = 0.0
    var_true = 0.0
    var_pred = 0.0
    for yt, yp in zip(p_true, p_pred):
        dt = float(yt) - mean_true
        dp = float(yp) - mean_pred
        cov += dt * dp
        var_true += dt * dt
        var_pred += dp * dp

    denom = math.sqrt(var_true * var_pred)
    corr = float("nan") if denom == 0.0 else cov / denom

    result = {
        "mae": mae,
        "rmse": rmse,
        "corr": corr,
    }

    if table_save_path is not None:
        _save_metrics_table_png(result, table_save_path)

    return result


def compute_true_vs_pred_metrics_from_model(
    model: Any,
    X: Sequence[Any],
    p_true: Sequence[float],
    predictor: Callable[[Any, Any], float] | None = None,
    table_save_path: str | Path | None = None,
) -> dict[str, float]:
    """
    Compute fit metrics by first generating model probabilities for X.

    Args:
        table_save_path: optional path to save a PNG table of the metrics
    """
    p_pred = get_model_probability_outputs(model=model, X=X, predictor=predictor)
    return compute_true_vs_pred_metrics(p_true=p_true, p_pred=p_pred, table_save_path=table_save_path)


def get_torch_sequence_model_probability_outputs(
    model: Any,
    X: Sequence[Any],
    device: str | None = None,
    apply_sigmoid: bool = True,
    use_last_timestep: bool = True,
) -> list[float]:
    """
    Return probabilities from a PyTorch sequence model for each sample in X.

    This helper supports common output shapes:
    - [batch, seq_len, 1] (per-timestep logits/probabilities)
    - [batch, 1] (single output per sequence)

    Args:
        model: PyTorch model
        X: sequence samples; each sample is usually shape [seq_len] or [seq_len, input_dim]
        device: optional device string, e.g. "cpu" or "cuda"
        apply_sigmoid: set True when model outputs logits, False when model already outputs probabilities
        use_last_timestep: when model returns per-timestep outputs, use the final timestep if True;
            otherwise use the mean over timesteps
    """
    import torch

    if len(X) == 0:
        return []

    resolved_device = torch.device(device) if device is not None else next(model.parameters()).device

    was_training = model.training
    model.eval()

    preds: list[float] = []

    with torch.no_grad():
        for sample in X:
            sample_t = torch.as_tensor(sample, dtype=torch.float32, device=resolved_device)

            if sample_t.ndim == 1:
                sample_t = sample_t.unsqueeze(0).unsqueeze(-1)
            elif sample_t.ndim == 2:
                sample_t = sample_t.unsqueeze(0)
            elif sample_t.ndim != 3:
                raise ValueError("Each sample must be 1D, 2D, or batched 3D tensor-like input")

            out = model(sample_t)
            if isinstance(out, tuple):
                out = out[0]

            if out.ndim == 3:
                if use_last_timestep:
                    out = out[:, -1, :]
                else:
                    out = out.mean(dim=1)
            elif out.ndim == 1:
                out = out.unsqueeze(-1)

            if apply_sigmoid:
                out = torch.sigmoid(out)

            preds.append(float(out.reshape(-1)[0].item()))

    if was_training:
        model.train()

    return preds


def plot_true_vs_pred_p_over_samples_torch_sequence(
    model: Any,
    X: Sequence[Any],
    p_true: Sequence[float],
    device: str | None = None,
    apply_sigmoid: bool = True,
    use_last_timestep: bool = True,
    max_points: int | None = None,
    save_path: str | Path = "true_vs_pred_p_over_samples.png",
    show: bool = True,
    title: str = "True vs Predicted P(head) Across Samples",
) -> list[float]:
    """
    Convenience wrapper for plotting true vs predicted p with PyTorch sequence models.

    This is equivalent to `plot_true_vs_pred_p_over_samples(...)` with an internal
    predictor tailored to common RNN/GRU/LSTM output shapes.
    """

    def torch_predictor(torch_model: Any, sample: Any) -> float:
        pred = get_torch_sequence_model_probability_outputs(
            model=torch_model,
            X=[sample],
            device=device,
            apply_sigmoid=apply_sigmoid,
            use_last_timestep=use_last_timestep,
        )
        return float(pred[0])

    return plot_true_vs_pred_p_over_samples(
        model=model,
        X=X,
        p_true=p_true,
        predictor=torch_predictor,
        max_points=max_points,
        save_path=save_path,
        show=show,
        title=title,
    )


def compute_true_vs_pred_metrics_torch_sequence(
    model: Any,
    X: Sequence[Any],
    p_true: Sequence[float],
    device: str | None = None,
    apply_sigmoid: bool = True,
    use_last_timestep: bool = True,
    table_save_path: str | Path | None = None,
) -> dict[str, float]:
    """
    Convenience metric computation for PyTorch sequence models.

    Args:
        table_save_path: optional path to save a PNG table of the metrics
    """
    p_pred = get_torch_sequence_model_probability_outputs(
        model=model,
        X=X,
        device=device,
        apply_sigmoid=apply_sigmoid,
        use_last_timestep=use_last_timestep,
    )
    return compute_true_vs_pred_metrics(p_true=p_true, p_pred=p_pred, table_save_path=table_save_path)
