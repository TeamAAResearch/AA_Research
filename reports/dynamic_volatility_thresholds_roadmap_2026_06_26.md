# Research Roadmap: Dynamic Volatility Thresholding
**Date:** 2026-06-26
**Owner:** Antigravity (AG)

## The Strategic Gap
Currently, the system relies on static momentum thresholds (`config.momentum_threshold_pct` and the new `threshold_overrides`). While we have accurately calibrated these based on the trailing 6-month ATR (Average True Range), market volatility regimes are not static. 

A static threshold of `0.36%` for Gold may be mathematically optimal today, but if macro conditions shift (e.g., a central bank rate cycle change or a geopolitical shock), Gold's daily ATR could double or halve.
*   **If volatility drops:** The static 0.36% threshold becomes too high, starving the funnel of valid opportunities.
*   **If volatility spikes:** The 0.36% threshold becomes too low, resulting in signal flooding and sub-optimal entries (as we saw with the 0.1% FX threshold).

## Proposed Architecture: The Volatility Engine
To transition from static thresholds to a dynamically self-adjusting system, we must build a **Volatility Engine** that calculates the trailing N-day ATR on a rolling basis.

### Mechanism
1.  **Daily Calibration Phase:** At the start of the trading session, the system queries historical daily candles (e.g., the last 14 days) for every active symbol in the portfolio.
2.  **Relative Multiplier Calculation:** The engine calculates the current ATR for the benchmark asset (e.g., EURUSD) and the target asset (e.g., XAUUSD).
3.  **Dynamic Override Injection:** The engine computes the real-time volatility multiplier (`Target ATR / Benchmark ATR`) and dynamically injects the resulting normalized threshold into `ChallengerConfig.threshold_overrides` in memory.

### Required Evidence & Research Steps (Next Phase)
Before we authorize Codex to build this engine, AG must validate the following:
1.  **Lookback Window Optimization:** Is a 14-day, 30-day, or 90-day ATR the most predictive of the *current* day's intraday momentum profile?
2.  **Data Source Feasibility:** Does the execution engine have reliable, lightweight access to daily candles via the Saxo API without blocking the high-frequency tick stream?
3.  **Boundary Constraints:** Should we impose floor/ceiling guardrails on the dynamic thresholds to prevent anomalous math during extreme "black swan" market crashes?

## Status
*   **Current Phase:** Logged as a priority architectural research track.
*   **Immediate Action:** None required. The static 6-month baselines will serve as our stable foundation while this dynamic architecture is researched.
