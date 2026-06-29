# RESEARCH DIRECTIVE: Human Trading Feedback Loop
**From:** AG (Research & Analysis)
**To:** Codex (Engineering & Execution)
**Date:** 2026-06-29

## Context for Codex
The GM has provided a 14-day manual trading log for XAUUSD (`AA_Research/ledgers/kenny_xauusd_june.xlsx`). 
AG has analyzed this data and found a critical asymmetry between Ari (The Machine) and the GM (The Human).
- **Ari:** 86% Win Rate, but choking on $14 wins and taking $180 losses (1:13 payoff ratio).
- **GM:** 36% Win Rate, but letting winners run to $137 and cutting losers at $82 (1.67:1 payoff ratio).

We must use human trading logs as a **"hard positive" benchmark** to calibrate Ari's execution settings, specifically `CHALLENGER_TRAILING_PROTECT_PCT`. We need a continuous feedback loop where human logs are routinely ingested to tune the machine.

---

## Part 1: What to Review
Codex, you must review the GM's trading data located at:
`AA_Research/ledgers/kenny_xauusd_june.xlsx`

**Specific Data Points to Extract:**
1. **Payoff Ratio:** Calculate the average winning trade vs. average losing trade.
2. **Directional Bias:** Split the PnL by Side (Buy vs. Sell) to identify macro regime bias.
3. **Missing Temporal Data:** The standard Saxo export truncates exact execution times (showing only `00:00:00`). You need to review if it's possible to cross-reference the raw `Open Price` and `Close Price` against our tick data store (`trade_store.sqlite3`) to reverse-engineer the exact entry/exit timestamps. This is critical for calculating true holding times and MFE/MAE.

---

## Part 2: How to Review (Engineering Tasks)
Do not do this manually. Build an automated ingestion script:
`scripts/ingest_human_ledger.py`

**Script Requirements:**
- **Input:** Takes a standard Saxo `.xlsx` or `.csv` export file.
- **Parsing:** Uses `pandas` to filter for closed positions, calculate Win Rate, Average Win, Average Loss, and Payoff Ratio.
- **Output:** Generates a standardized Markdown report summarizing the human benchmark (e.g., `AA_Research/reports/human_benchmark_YYYY_MM_DD.md`).
- **Bonus (If Possible):** Attempts to match the `Open Price` with tick data to estimate the actual time the human held the trade.

---

## Part 3: The Continuous Feedback Loop Architecture
To make this an ongoing, autonomous process, implement the following structure:

1. **The Drop Zone:** 
   Create a dedicated directory at `AA_Research/ledgers/human_benchmark/`. The GM will drop new Saxo exports into this folder periodically.
   
2. **The Calibration Pipeline:**
   When the ingestion script runs, it should not just generate a report. It must programmatically write the human benchmark (specifically the Target Payoff Ratio) into a new section in `AA_SHARED_RESEARCH_MEMO.md` called `## Active Human Benchmarks`.
   
3. **Ari's Intake:**
   Ari's execution code (e.g., `aa_decision.py` or `trade_manager.py`) should be modified by Codex to read these benchmarks. If the human is routinely achieving a 1.67 payoff ratio with average wins of $130, Ari's code should automatically widen its trailing stops to attempt to capture similar magnitude moves, rather than reverting to its default, anxious $14 capture rate.

**Codex:** Please begin engineering this ingestion script and feedback loop structure immediately. Report back to the GM when the pipeline is ready to consume the next batch of human logs.
