from typing import Any, Dict, List, Tuple

from .generation import (
    generate_nonstationary_coin_flips,
    generate_nonstationary_coin_flips_probabilistic,
)


def _build_simulation(
    n: int,
    seed: int | None,
    mode: str = "deterministic",
    sim_kwargs: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Construct a simulation using either deterministic or probabilistic switching."""
    kwargs = sim_kwargs or {}

    if mode == "deterministic":
        return generate_nonstationary_coin_flips(n=n, seed=seed)
    if mode == "probabilistic":
        return generate_nonstationary_coin_flips_probabilistic(n=n, seed=seed, **kwargs)

    raise ValueError("mode must be one of: 'deterministic', 'probabilistic'")


def build_autoregressive_dataset_from_sim(
    sim: Dict[str, Any],
    k: int,
    include_p_true: bool = False,
):
    """Build fixed-window samples for MLP/CNN-style models."""
    flips = sim["flips"]
    p_before = [s["p_head_before"] for s in sim["steps"]]

    X: List[List[int]] = []
    y: List[int] = []
    p_true: List[float] = []

    for t in range(k, len(flips)):
        X.append(flips[t - k : t])
        y.append(flips[t])
        if include_p_true:
            p_true.append(p_before[t])

    if include_p_true:
        return X, y, p_true
    return X, y


def build_autoregressive_dataset(
    n: int,
    k: int,
    seed: int | None = None,
    include_p_true: bool = False,
    mode: str = "deterministic",
    sim_kwargs: Dict[str, Any] | None = None,
):
    """
    Build autoregressive dataset from simulated flips.

    mode:
    - "deterministic": original hard-threshold regime switching
    - "probabilistic": probabilistic regime switching with optional sim_kwargs
    """
    sim = _build_simulation(n=n, seed=seed, mode=mode, sim_kwargs=sim_kwargs)
    return build_autoregressive_dataset_from_sim(sim=sim, k=k, include_p_true=include_p_true)


def build_sequence_dataset_from_sim(sim: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build variable-length sequence targets for RNN/GRU/LSTM/Transformer models.

    Returns:
    - x_seq: flips[:-1]
    - y_flip_next: flips[1:]
    - y_p_next: p_head_before[1:]
    - regime_next: regime at target timestep
    """
    flips = sim["flips"]
    steps = sim["steps"]

    if len(flips) < 2:
        raise ValueError("Need at least 2 flips to build next-step sequence targets")

    p_before = [s["p_head_before"] for s in steps]
    regimes = [s["regime"] for s in steps]

    return {
        "initial_p_head": sim["initial_p_head"],
        "x_seq": flips[:-1],
        "y_flip_next": flips[1:],
        "y_p_next": p_before[1:],
        "regime_next": regimes[1:],
        "full_flips": flips,
        "full_p": p_before,
        "full_regimes": regimes,
    }


def build_sequence_dataset(
    n: int,
    seed: int | None = None,
    mode: str = "deterministic",
    sim_kwargs: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Build sequence dataset from simulated flips.

    mode:
    - "deterministic": original hard-threshold regime switching
    - "probabilistic": probabilistic regime switching with optional sim_kwargs
    """
    sim = _build_simulation(n=n, seed=seed, mode=mode, sim_kwargs=sim_kwargs)
    return build_sequence_dataset_from_sim(sim)
