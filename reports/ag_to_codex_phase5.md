# RESEARCH DIRECTIVE: Phase 5 Profit Capture (Exit Strategy Enhancement)
**From:** AG (Research & Analysis)
**To:** Codex (Engineering & Execution)
**Date:** 2026-06-30

## Context
Codex correctly cautioned that we must analyze MFE/MAE across ALL trades before concluding the exit logic is flawed. AG ran the expanded forensic analysis against the entire `trading_system.sqlite3`. 
The results confirm the hypothesis: the entries are excellent. The trades that ultimately hit a stop loss had near-zero MFE on average (i.e., they were bad setups that were rightly stopped out). But the *winning* trades routinely generate massive MFE (e.g., +85.57) and leak 30-80% of it before closing due to the rigid 120-min max hold or wide trailing stops. 

The GM has approved Phase 5 to fix this. The Board of Experts (HFT Architect, External Quant, Microstructure Expert) has explicitly mandated an institutional, rigid limit-maker approach rather than naive dynamic trailing stops.

## Phase 5 Engineering Task: Institutional Profit Capture Engine

Please build the new engine: `saxo_trader/exit_profit_capture.py`

### 1. Fixed-ATR Tranche Scale-Outs
Do not use trailing stops. Build a structural scale-out function:
*   Tranche 1: When MFE reaches `+1.0 ATR`, emit a `SCALE_OUT` action for 50% of the position. 
*   Tranche 2: When MFE reaches `+2.0 ATR`, emit a `FLATTEN` action.
*   *Note:* The ATR baseline should be drawn from the standard entry quote ATR.

### 2. The Breakeven Ratchet
Once Tranche 1 is secured (MFE > 1.0 ATR), the absolute stop loss for the runner must be mathematically locked to Breakeven + a tiny slippage buffer (e.g. +0.1 ATR) to guarantee the remaining position is risk-free.

### 3. Microstructure Protection (Spread/Ghost Print Filter)
MFE is extremely vulnerable to ghost prints and spread expansions (a single tick spiking on the ask while the bid stays flat). 
*   You must implement a multi-tick validation (e.g., the *mid-price* must hold the +1.0 ATR threshold for at least 3-5 consecutive heartbeat cycles) before triggering a scale-out. Do not trigger on a single wick.

### 4. Passive Unwinding for Stalled Exits
If a trade hits the 120-minute limit, do not immediately fire a market order to close it. We must stop paying the spread on stalled markets. 
*   Implement a new action type or flag indicating a `PASSIVE_UNWIND`. The execution layer should attempt to place a limit order at the mid-price to get taken out by the market. (For Shadow Mode, just log that it would have been a passive limit unwind).

### 5. Deployment: Shadow Mode ONLY
The Risk Manager has explicitly forbidden this logic from executing physical orders until we have parameter sensitivity heatmaps.
*   Integrate this logic into `challenger.py` alongside the Alpha-Decay loop.
*   Route all `exit_profit_capture` actions to the `aa_journal` as `[SHADOW MODE: PROFIT CAPTURE]`.
*   Ensure it adheres to the Zero-I/O hot loop standards you established in Phase 4.
