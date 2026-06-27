import pytest
from saxo_trader.spotter import _momentum_decision
from saxo_trader.models import Side

def test_momentum_decision_clean_buy():
    # Clean 1% move up
    ticks = [
        {"mid": 1.000},
        {"mid": 1.002},
        {"mid": 1.005},
        {"mid": 1.008},
        {"mid": 1.010},
    ]
    assert _momentum_decision(ticks, 0.01) == Side.BUY

def test_momentum_decision_clean_sell():
    # Clean 1% move down
    ticks = [
        {"mid": 1.000},
        {"mid": 0.998},
        {"mid": 0.995},
        {"mid": 0.992},
        {"mid": 0.990},
    ]
    assert _momentum_decision(ticks, 0.01) == Side.SELL

def test_momentum_decision_whipsaw_rejected():
    # Price crashes 1%, then rockets up 2%. 
    # Original logic only compares 1.000 to 1.010 and calls it a BUY.
    # True Tick-Path must return None (Whipsaw).
    ticks = [
        {"mid": 1.000},
        {"mid": 0.990}, # Crossed lower threshold (-1%)
        {"mid": 0.995},
        {"mid": 1.005},
        {"mid": 1.010}, # Crossed upper threshold (+1%)
    ]
    assert _momentum_decision(ticks, 0.01) is None

def test_momentum_decision_spike_reversal_rejected():
    # Price spikes up 1%, but crashes back to baseline at the final tick.
    # It breached upper, but didn't hold it.
    ticks = [
        {"mid": 1.000},
        {"mid": 1.005},
        {"mid": 1.010}, # Breached upper
        {"mid": 1.005},
        {"mid": 1.000}, # Failed to hold
    ]
    assert _momentum_decision(ticks, 0.01) is None
