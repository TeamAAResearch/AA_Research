# Directive: Phase 2 MAE Dual-Ledger
**Date:** 2026-06-26
**To:** Codex (Engineering)
**From:** AG (Research)

Phase 1 (Data Feasibility) is officially complete. We are now advancing to Phase 2: The MAE Dual-Ledger.

**Context from your Phase 1B finding:**
You correctly identified that older trades may fall outside Saxo's 1-minute candle lookback window (the `Count=1500` limit). To solve this, we will execute the MAE reconstruction *promptly* upon trade closure, rather than doing deep historical backfills.

Please execute the following:

## 1. Schema Expansion
Add the following columns to the closed positions / reviews table in `trading_system.sqlite3`:
*   `mae_exit_price`
*   `mae_pnl`
*   `loop_slippage_cost` (The difference between the original loop P/L and the reconstructed MAE P/L)

## 2. Immediate Reconstruction Hook
Modify `saxo_trader/challenger_review.py` (or the equivalent module that finalizes closed paper trades). 
*   The moment a trade is marked closed, the system should immediately fetch the 1-minute Saxo candles for that trade's duration.
*   Run the MAE reconstruction logic you built in the prototype.
*   Populate the new dual-ledger columns.
*   **Crucial Rule:** Do *not* overwrite the original `exit`, `closed_at`, or `pnl` columns. We need both ledgers intact to measure the latency cost.

Confirm when the database schema is updated, the prompt reconstruction logic is wired up, and the unit tests pass.
