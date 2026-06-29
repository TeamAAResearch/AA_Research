# RESEARCH DIRECTIVE: Time-Exit Simulation Study
**From:** AG (Research & Analysis)
**To:** Codex (Engineering & Execution)
**Date:** 2026-06-29

## Context
The P3 Forensic Matcher results indicate the GM's winning trades average 215.98 minutes, while Ari is hardcoded to kill trades at 60 minutes via the `time_decay` exit rule. The GM has approved a simulation study to mathematically quantify how much PnL Ari's 60-minute rule is leaving on the table compared to wider time exits.

## Engineering Task
Build the `scripts/simulate_time_exits.py` script.

### 1. Data Ingestion
- Load the forensic matcher output: `AA_Research/ledgers/human_benchmark/forensic_matcher_2026_06_29_124625.csv`.
- Filter strictly for `status == 'matched'` and `confidence > 0`.

### 2. The Simulation Logic
Iterate through the matched trades and simulate forcing them closed at four distinct thresholds: `T = [60, 120, 180, 240]` minutes.

For each trade and each threshold `T`:
- **Scenario A (Human Exited Early):** If `hold_minutes` $\le T$, the trade remains unaffected. The Simulated PnL equals the actual human PnL.
- **Scenario B (Forced Exit at T):** If `hold_minutes` $> T$, the trade is artificially killed.
  - Use `yfinance` to fetch 5-minute `GC=F` data for the exact date.
  - Locate the bar corresponding to `entry_time + T`.
  - The simulated exit price is the `Close` price of that bar.
  - Recalculate the trade's PnL based on this simulated exit price (accounting for `side`).

### 3. Output Metrics
The script must generate a markdown report (`AA_Research/reports/time_exit_simulation_YYYY_MM_DD.md`) comparing the following metrics for the Control Group (Actual Human Trading) and all four simulated time thresholds:
- Total Net PnL
- Win Rate
- Average Win
- Average Loss
- Payoff Ratio

Please build the script, execute the simulation, and return the mathematical results.
