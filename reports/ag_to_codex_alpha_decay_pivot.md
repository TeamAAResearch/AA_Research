# RESEARCH DIRECTIVE: Pivot to Continuous Alpha-Decay Scaling
**From:** AG (Research & Analysis)
**To:** Codex (Engineering & Execution)
**Date:** 2026-06-29

## Context
The GM and the Board of Experts (specifically the External Industry Quant) have issued a hard REJECT of the 4-state `exit_alive_score` behavioral module. The 109-trade dataset is deemed statistical noise, and discrete behavioral labels are considered retail over-engineering. 

We are officially pivoting to an institutional-grade **Continuous Alpha-Decay Scaling Function**. 

## Phase 1 Engineering Task: Massive Data Expansion
We cannot calibrate alpha-decay logic on 109 trades. Before building any exit logic, we need to drastically expand our backtest dataset.

1. **Build a historical entry simulator** (`scripts/simulate_ari_entries.py`) that sweeps the last 12-24 months of XAUUSD data.
2. **Execute Ari's core entry logic** (without exits) across this massive dataset to generate at least 5,000+ valid entry paths spanning different macro regimes (NFP, CPI, varying liquidity).
3. **Capture full forward-path data** for each entry (e.g., MFE, MAE, holding times) up to 240+ minutes so we can analyze the true baseline expectation of alpha decay.

## Future Phase 2 Task (Do Not Build Yet)
Once we have 5,000+ simulated entries, we will design the Continuous Alpha-Decay Scaling engine:
- Modeling expected return vs. hold time (alpha decay).
- Implementing dynamic size scaling (scaling out as decay accelerates) instead of fixed time-kills.
- Integrating a spread/liquidity microstructure penalty.

Please execute Phase 1 (Data Expansion) and return the bulk dataset.
