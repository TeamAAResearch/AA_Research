from __future__ import annotations

from saxo_trader.models import ChallengerConfig, Side

METALS = ["XAUUSD", "XAGUSD", "XPTUSD", "XPDUSD"]

def _momentum_threshold(symbol: str, config: ChallengerConfig) -> float:
    """Returns the required percentage move to trigger a signal."""
    symbol_key = symbol.upper()
    if config.threshold_overrides and symbol_key in config.threshold_overrides:
        production_threshold = config.threshold_overrides[symbol_key]
    else:
        production_threshold = config.momentum_threshold_pct

    if not config.training_sample_mode:
        return production_threshold
    if symbol_key in METALS:
        return production_threshold
    return min(production_threshold, config.training_momentum_threshold_pct)

def _signal_score(ticks: list[dict]) -> float:
    """Calculates the true percentage change from first to last tick."""
    first = float(ticks[0]["mid"])
    last = float(ticks[-1]["mid"])
    return round((last - first) / first, 6) if first else 0.0

def _momentum_decision(ticks: list[dict], threshold_pct: float) -> Side | None:
    """
    Evaluates the true tick path for momentum.
    Rejects signals if the path violently whipsawed across both upper and lower thresholds.
    """
    first = float(ticks[0]["mid"])
    if first <= 0:
        return None

    mids = [float(tick["mid"]) for tick in ticks]
    max_mid = max(mids)
    min_mid = min(mids)
    last = float(ticks[-1]["mid"])

    # Trace the absolute extremes of the path
    max_upward_pct = (max_mid - first) / first
    max_downward_pct = (min_mid - first) / first

    # Did the path breach the thresholds at any point?
    breached_upper = max_upward_pct >= threshold_pct
    breached_lower = max_downward_pct <= -threshold_pct

    # WHIPSAW REJECTION: If it violently swung in both directions within 5 ticks, it is pure noise.
    if breached_upper and breached_lower:
        return None

    # Valid BUY: It breached upper, never breached lower, and is currently holding the breakout
    if breached_upper and ((last - first) / first) >= threshold_pct:
        return Side.BUY

    # Valid SELL: It breached lower, never breached upper, and is currently holding the breakdown
    if breached_lower and ((last - first) / first) <= -threshold_pct:
        return Side.SELL

    return None

def _consistent_momentum(ticks: list[dict], side: Side) -> bool:
    """Checks if the tick path smoothly trends in the signal direction."""
    mids = [float(tick["mid"]) for tick in ticks]
    if len(mids) < 3:
        return False
    moves = [later - earlier for earlier, later in zip(mids, mids[1:])]
    aligned = [move for move in moves if (move > 0 if side == Side.BUY else move < 0)]
    return len(aligned) >= max(2, len(moves) - 1)

def evaluate_momentum_signal(symbol: str, ticks: list[dict], config: ChallengerConfig) -> dict | None:
    """
    The Maker (Spotter). 
    Analyzes raw ticks and proposes a trade signal if conditions are met.
    Returns None if no signal is found.
    """
    if len(ticks) < config.min_ticks_for_signal:
        return None

    threshold = _momentum_threshold(symbol, config)
    decision = _momentum_decision(ticks, threshold)
    
    if not decision:
        return None

    score = _signal_score(ticks)
    consistent = _consistent_momentum(ticks, decision)
    
    return {
        "side": decision,
        "score": score,
        "threshold": threshold,
        "consistent": consistent
    }
