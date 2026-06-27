# 360° Risk Review: Phase 2 (MAE Dual-Ledger)
**Date:** 2026-06-26
**Context:** Proactive 360-degree process review before Phase 2 goes live.

While the objective of Phase 2 is lean (measurement only), the act of wiring it into the live trading loop introduces new systemic vulnerabilities. By thinking through the exact process of trade closure, I have identified four critical risks that must be addressed before Codex finalizes Phase 2.

## Critical Risks Identified

### 1. The Synchronous Blocking Risk (Runner Latency)
*   **The Flaw:** If `challenger_review.py` runs the MAE back-calculator synchronously during the main trading loop, it will force Ari to wait for the Saxo API HTTP response.
*   **The Danger:** Fetching 1-minute candles takes time (e.g., 1-2 seconds per trade). If Ari closes 3 trades simultaneously, the runner is paralyzed for 6 seconds. If a violent market move happens during those 6 seconds, Ari will be blind to it.
*   **The Fix:** The MAE reconstruction *must* be handled asynchronously or fail gracefully and quickly. It cannot block the primary `run_challenger_cycle()` pulse.

### 2. The "Incomplete Candle" Blindspot
*   **The Flaw:** If Ari closes a trade at 10:15:05 AM, and we immediately fetch the 1-minute candles, Saxo may not have fully constructed the 10:15:00 AM candle yet. 
*   **The Danger:** The MAE reconstruction might miss the very candle where the stop-loss actually occurred, resulting in corrupted slippage data.
*   **The Fix:** The back-calculator must ensure it explicitly fetches the most recent tick data, or waits an extra 60 seconds (post-closure) before querying the final 1-minute candle to ensure Saxo's database has settled.

### 3. API Fragility (Crash Risk)
*   **The Flaw:** The MAE fetch adds another external API call to the system. 
*   **The Danger:** If the Saxo `/chart/v3/charts` endpoint times out or returns a 500 error when a trade closes, the unhandled exception could crash the entire `challenger_review` function. This would prevent the trade from being marked `Closed` in the SQLite database, causing the system to hallucinate that the trade is still open.
*   **The Fix:** Codex must wrap the MAE reconstruction in a strict, isolated `try/except` block. If the MAE fetch fails, the trade *must still close normally* in SQLite, and the dual-ledger columns can just be recorded as `NULL` or `FAILED`.

### 4. Rate Limiting 
*   **The Flaw:** Fetching deep histories for multiple symbols rapidly.
*   **The Danger:** Hitting Saxo's undocumented rate limits for the charting endpoint.
*   **The Fix:** Keep the `Count` parameter as small as mathematically required (e.g., if the trade was open for 45 minutes, don't ask for `Count=1500`, ask for `Count=60`).

## Recommendation for Codex
Before we deploy Phase 2 into the live runner, Codex must explicitly confirm that the MAE dual-ledger implementation is wrapped in strict error handling and will absolutely not block or slow down the main heartbeat of the `spotter -> challenger` loop.
