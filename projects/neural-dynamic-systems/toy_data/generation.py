import math
import random
from typing import Any, Dict, List


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def _logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def p_series_from_flips(
    initial_p_head: float,
    flips: List[int],
    regimes: List[str] | None = None,
    latent_step: float = 0.4,
    mean_reversion: float = 0.30,
    lower: float = 0.25,
    upper: float = 0.75,
) -> List[float]:
    """Reconstruct p_head_before over time from initial state and flip history."""
    if not (lower < initial_p_head < upper):
        raise ValueError("initial_p_head must be strictly between lower and upper")

    if regimes is not None and len(regimes) != len(flips):
        raise ValueError("regimes must have the same length as flips")

    span = upper - lower
    z = _logit((initial_p_head - lower) / span)
    p_before: List[float] = []

    for idx, flip in enumerate(flips):
        p_before.append(lower + span * _sigmoid(z))

        if regimes is None:
            z = z + latent_step * flip
            continue

        regime = regimes[idx]
        if regime == "trend_updown":
            z = z + latent_step * flip
        elif regime == "mean_reverting":
            z = (1.0 - mean_reversion) * z + latent_step * flip
        else:
            raise ValueError(f"Unknown regime: {regime}")

    return p_before


def reconstruct_steps_from_flips_and_regimes(
    initial_p_head: float,
    flips: List[int],
    regimes: List[str],
    latent_step: float = 0.4,
    mean_reversion: float = 0.30,
    lower: float = 0.25,
    upper: float = 0.75,
) -> List[Dict[str, Any]]:
    """Reconstruct full step records exactly from initial p, flips, and regimes."""
    if len(regimes) != len(flips):
        raise ValueError("regimes must have the same length as flips")

    span = upper - lower
    z = _logit((initial_p_head - lower) / span)
    steps: List[Dict[str, Any]] = []

    for t, (flip, regime) in enumerate(zip(flips, regimes)):
        p_before = lower + span * _sigmoid(z)

        if regime == "trend_updown":
            z = z + latent_step * flip
        elif regime == "mean_reverting":
            z = (1.0 - mean_reversion) * z + latent_step * flip
        else:
            raise ValueError(f"Unknown regime: {regime}")

        p_after = lower + span * _sigmoid(z)
        steps.append(
            {
                "t": t,
                "p_head_before": p_before,
                "flip": flip,
                "p_head_after": p_after,
                "regime": regime,
            }
        )

    return steps


def generate_nonstationary_coin_flips(n: int, seed: int | None = None) -> Dict[str, Any]:
    """
    Generate non-stationary coin flips with deterministic two-regime switching.

    Regimes:
    - trend_updown: z <- z + latent_step * flip
    - mean_reverting: z <- (1 - mean_reversion) * z + latent_step * flip

    Switching rules:
    - switch to mean_reverting if p >= 0.70 or p <= 0.30
    - switch to trend_updown if 0.45 < p < 0.55
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")

    rng = random.Random(seed)

    lower, upper = 0.25, 0.75
    span = upper - lower
    latent_step = 0.4
    mean_reversion = 0.30

    initial_p_head = rng.uniform(0.40, 0.60)
    z = _logit((initial_p_head - lower) / span)
    regime = "trend_updown"

    flips: List[int] = []
    symbols: List[str] = []
    steps: List[Dict[str, Any]] = []

    for t in range(n):
        p_before = lower + span * _sigmoid(z)

        if p_before >= 0.70 or p_before <= 0.30:
            regime = "mean_reverting"
        elif 0.45 < p_before < 0.55:
            regime = "trend_updown"

        flip = 1 if rng.random() < p_before else -1

        flips.append(flip)
        symbols.append("H" if flip == 1 else "T")

        if regime == "trend_updown":
            z = z + latent_step * flip
        else:
            z = (1.0 - mean_reversion) * z + latent_step * flip

        p_after = lower + span * _sigmoid(z)

        steps.append(
            {
                "t": t,
                "p_head_before": p_before,
                "flip": flip,
                "p_head_after": p_after,
                "regime": regime,
            }
        )

    return {
        "initial_p_head": initial_p_head,
        "flips": flips,
        "flip_symbols": symbols,
        "steps": steps,
    }


def _switch_probability_from_p(
    p: float,
    center_low: float = 0.45,
    center_high: float = 0.55,
    extreme_low: float = 0.30,
    extreme_high: float = 0.70,
    min_prob: float = 0.01,
) -> float:
    """
    Compute a switch probability that is low near p=0.5 and high at extremes.

    Behavior:
    - p in [center_low, center_high] -> min_prob
    - p <= extreme_low or p >= extreme_high -> 1.0
    - linear interpolation in between
    """
    if not (0.0 <= min_prob <= 1.0):
        raise ValueError("min_prob must be in [0, 1]")

    if center_low >= center_high:
        raise ValueError("center_low must be < center_high")
    if extreme_low >= center_low:
        raise ValueError("extreme_low must be < center_low")
    if extreme_high <= center_high:
        raise ValueError("extreme_high must be > center_high")

    if p <= extreme_low or p >= extreme_high:
        return 1.0

    if center_low <= p <= center_high:
        return min_prob

    if p < center_low:
        frac = (center_low - p) / (center_low - extreme_low)
    else:
        frac = (p - center_high) / (extreme_high - center_high)

    return min_prob + (1.0 - min_prob) * frac


def generate_nonstationary_coin_flips_probabilistic(
    n: int,
    seed: int | None = None,
    latent_step: float = 0.4,
    mean_reversion: float = 0.30,
    noise_std: float = 0.05,
    lower: float = 0.25,
    upper: float = 0.75,
    center_low: float = 0.45,
    center_high: float = 0.55,
    extreme_low: float = 0.30,
    extreme_high: float = 0.70,
    min_switch_prob: float = 0.01,
) -> Dict[str, Any]:
    """
    Generate non-stationary coin flips with probabilistic two-regime switching.

    Regimes:
    - trend_updown: z <- z + latent_step * flip + noise
    - mean_reverting: z <- (1 - mean_reversion) * z + latent_step * flip + noise

    Switching:
    - At each step, the chance to switch regimes depends on p_head_before.
    - Switch probability is min_switch_prob near p in [center_low, center_high].
    - It rises to 1.0 once p <= extreme_low or p >= extreme_high.
    - The same probability rule is used in both directions (mirrored behavior).
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")
    if not (lower < upper):
        raise ValueError("lower must be < upper")
    if noise_std < 0.0:
        raise ValueError("noise_std must be >= 0")

    rng = random.Random(seed)

    span = upper - lower
    initial_p_head = rng.uniform(0.40, 0.60)
    z = _logit((initial_p_head - lower) / span)
    regime = "trend_updown"

    flips: List[int] = []
    symbols: List[str] = []
    steps: List[Dict[str, Any]] = []

    for t in range(n):
        p_before = lower + span * _sigmoid(z)

        p_switch = _switch_probability_from_p(
            p=p_before,
            center_low=center_low,
            center_high=center_high,
            extreme_low=extreme_low,
            extreme_high=extreme_high,
            min_prob=min_switch_prob,
        )
        switched = rng.random() < p_switch
        if switched:
            regime = "mean_reverting" if regime == "trend_updown" else "trend_updown"

        flip = 1 if rng.random() < p_before else -1

        flips.append(flip)
        symbols.append("H" if flip == 1 else "T")

        noise = rng.gauss(0.0, noise_std)
        if regime == "trend_updown":
            z = z + latent_step * flip + noise
        else:
            z = (1.0 - mean_reversion) * z + latent_step * flip + noise

        p_after = lower + span * _sigmoid(z)

        steps.append(
            {
                "t": t,
                "p_head_before": p_before,
                "flip": flip,
                "p_head_after": p_after,
                "regime": regime,
                "switched": switched,
                "switch_probability": p_switch,
                "noise": noise,
            }
        )

    return {
        "initial_p_head": initial_p_head,
        "flips": flips,
        "flip_symbols": symbols,
        "steps": steps,
    }
