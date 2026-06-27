# 360° Strategic Gap Review (Pre-Stage 2)
**Date:** 2026-06-26
**Context:** Pre-flight check before initiating Stage 2 (Dynamic Volatility) development.

The GM correctly halted immediate development to perform a 360-degree review of the entire system. While the Stage 1 Training Mode is successfully capturing high-throughput data, charging ahead to build a *new* Alpha generator (Dynamic ATR) exposes us to several severe downstream vulnerabilities.

If we do not address these gaps first, the N=100 data we collect over the next 48 hours will be statistically corrupted.

## Critical Gaps Discovered

### 1. The Exit Mechanics Integrity Risk (Slippage)
*   **The Flaw:** We shifted Ari from a 5-minute pulse to a 60-second pulse to catch fast breakouts. However, our Stop Loss (`0.5%`) and Take Profit (`1.0%`) are **soft paper stops**, evaluated only when the Python script wakes up.
*   **The Danger:** In a volatile breakout, price can easily slice through a 0.5% stop loss within 20 seconds. Since Ari sleeps for 60 seconds, the soft stop won't trigger until he wakes up, recording the exit at 0.8% or 1.0% loss. 
*   **The Consequence:** Our N=100 ledger will be polluted with massive artificial slippage. We won't be measuring the accuracy of the Spotter; we will be measuring the latency of our Python loop.
*   **Solution Needed:** We must design an MAE/MFE (Maximum Adverse/Favorable Excursion) back-calculator, or implement hard broker-side stops, before we can trust the P/L data.

### 2. The Anomaly Scanner False Positives
*   **The Flaw:** The `anomaly_scanner.py` was built under the assumption of 5-minute polling and strict admission gates.
*   **The Danger:** Now that Ari is polling every 60 seconds with wide-open gates, he might easily open 3 training probes in 2 minutes (he just opened 4 immediately upon restart). The Anomaly Scanner's hardcoded limits (e.g., `Max opened per minute = 3`) will likely trigger a false "system meltdown" quarantine, killing the runner while we sleep.
*   **Solution Needed:** The Anomaly Scanner limits must be expanded to accommodate the high-frequency Training Mode profile.

### 3. The Absent Analytics Pipeline
*   **The Flaw:** We are eagerly waiting for N=100 trades, but we have no statistical engine ready to analyze them. The current "Strategy Researcher" (Rowan) relies on simple heuristics, not p-values or out-of-sample validation.
*   **The Danger:** When we hit 100 trades, we will be staring at raw SQLite rows without a standardized script to calculate expectancy, profit factor, or signal decay.
*   **Solution Needed:** We must build the formal Analytics Extraction Script concurrently while Ari gathers the data.

## Strategic Recommendation

Building the Dynamic Volatility Engine right now is the wrong move. It is adding a new engine to a car with flat tires. 

Instead, I propose we split our efforts into a "Data Protection" sprint before Stage 2:
1.  **Immediate Fix:** Have Codex immediately adjust the `anomaly_scanner.py` thresholds to prevent Ari from auto-quarantining himself due to the new high-throughput flow.
2.  **Short-term Build:** Architect the Analytics Extraction Script so we are ready to mathematically ingest the N=100 ledger the moment it completes.
3.  **Medium-term Investigation:** Decide how we will filter "Python loop slippage" from the true signal edge when evaluating the exits.
