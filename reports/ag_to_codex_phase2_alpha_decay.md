# RESEARCH DIRECTIVE: Phase 2 Alpha-Decay Logic Execution
**From:** AG (Research & Analysis)
**To:** Codex (Engineering & Execution)
**Date:** 2026-06-29

## Context
Phase 1 (Data Expansion) was a success. We now have 4,143 validated entry paths. AG invoked the `institutional-red-team` Board of Experts to review the initial continuous decay math. The Board unanimously rejected the initial math due to positive skew choking, transaction cost multiplication, and a suicidal spread-pause execution trap. 

We have pivoted to a **Discrete Tranche Scaling** architecture, which the GM has approved.

## Phase 2 Engineering Task: Build the Exit Module

Please build the `exit_alpha_decay` module based on the exact specifications below. Do NOT use the 4-state behavioral logic or the continuous linear scaler.

### 1. Causal Rolling Baseline
*   The baseline expectation $E_{median}[PnL(t)]$ and the baseline volatility $ATR(t)$ must NOT be computed using global historical data (no look-ahead bias).
*   They must be computed dynamically using a trailing 60-day window based on the time $t$ of the execution.

### 2. Alpha Retention Score
*   Formula: $A(t) = \frac{PnL(t) - E_{median}[PnL(t)]}{ATR(t)}$

### 3. Discrete Tranche Execution
*   **Tranche 1 (Momentum Stall):** At $t=60$ minutes, if $A(t) < -1.5$ ATR, immediately scale out (liquidate) **50%** of the position.
*   **Tranche 2 (Terminal Invalid):** At any time $t$, if $A(t) < -2.5$ ATR, hard flatten the remaining position.
*   **Circuit Breaker (TTL):** At $t=240$ minutes, hard flatten 100% of the position regardless of $A(t)$.

### 4. Toxicity Routing (Volume-Participation Limit)
*   Do NOT pause the exit if the bid-ask spread widens. Execute aggressively to escape the toxic regime.
*   To prevent catastrophic slippage on our own sweeping, the exit function must cap the market order size to a maximum of **10% of the trailing 1-minute volume**. If the position is larger than this, it must slice the order sequentially rather than sweeping the book instantly.

## Next Steps for Codex
1. Write the Python logic for this exit module.
2. Run your own engineering Red-Team (`institutional-red-team` skill -> Workflow B) to review the Python latency, async I/O, and fail-closed error handling before you commit.
3. Test the logic on the historical simulation.
