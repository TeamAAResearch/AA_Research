# Directive: Data Protection & Analytics Pipeline (Pre-Stage 2)
**Date:** 2026-06-26
**To:** Codex (Engineering)
**From:** AG (Research)

The GM has authorized a "Data Protection" sprint before we begin building the Dynamic Volatility Engine. With the Stage 1 Training Mode operating at high frequency, the legacy safety limits and heuristic research modules are no longer sufficient.

Please execute the following engineering tasks immediately.

## 1. Widen Anomaly Scanner Tolerances
Ari just opened 4 trades instantly upon restart, which breaches the legacy anomaly scanner limits and risks triggering a false "meltdown" quarantine.
**Action:** Modify `saxo_trader/anomaly_scanner.py`:
*   Increase `MAX_OPENED_PER_MINUTE` from 3 to `10`.
*   Increase `MAX_CLOSED_PER_MINUTE` from 5 to `10`.

## 2. Scaffold the Analytics Pipeline
We are gathering N=100 trades, but we have no formal statistical engine to analyze the results. The current `trade_reviewer.py` (Rowan) is purely heuristic. We need a mathematical extraction script.
**Action:** Create a standalone Python script (e.g., `scripts/analyze_training_probes.py`) that:
*   Connects to `trading_system.sqlite3`.
*   Fetches all closed positions where `is_training_probe = 1`.
*   Calculates statistical baseline metrics: Total P/L, Win Rate, Expectancy per trade, average hold time, and Profit Factor.
*   Groups results by Symbol and Side (Buy/Sell).
*   *Note: Ensure this script can be run manually from the terminal by AG/GM to generate on-demand statistical reports.*

## 3. The Slippage Investigation (Request for Comment)
Because we are using "soft paper stops" evaluated only every 60 seconds, a violent momentum breakout will blow past our 0.5% stop loss before the Python loop wakes up to log the exit. 
**Action:** Please provide a brief technical RFC (Request for Comment) appended to your work log proposing how we can solve this slippage problem. Can we implement hard broker stops via Saxo API? Or do we need to build an MAE (Maximum Adverse Excursion) back-calculator using minute-candles to find the "true" exit price?

**Instructions:**
Execute the `anomaly_scanner.py` adjustments, build the `scripts/analyze_training_probes.py` tool, and present your RFC on the slippage risk.
