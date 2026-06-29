# RESEARCH DIRECTIVE: P3 Forensic Matcher
**From:** AG (Research & Analysis)
**To:** Codex (Engineering & Execution)
**Date:** 2026-06-29

## Context
Codex, you correctly identified that timestamp matching from the Saxo export might be noisy. However, the GM has approved the architectural design to use `yfinance` to fetch historical OHLCV bars to reverse-engineer the timestamps by matching the `Open Price` and `Close Price`.

## Engineering Task
Build the `scripts/forensic_matcher.py` script as outlined below.

### 1. Data Ingestion & Alignment
- Load `AA_Research/ledgers/kenny_xauusd_june.xlsx` using pandas.
- For each unique trade date, use `yfinance` to fetch 1-minute or 5-minute OHLCV bars for `GC=F` (Gold Futures).

### 2. The Forensic Matching Algorithm
Implement a chronological price-sweep algorithm:
- **Find Entry:** Iterate through the day's OHLCV bars. An entry match occurs when the human's `Open Price` falls within a bar's `[Low, High]` range. 
- **Find Exit:** From the Entry Bar index forward, find the first subsequent bar where the human's `Close Price` falls within the `[Low, High]` range.
- **Calculate Time-in-Trade:** Subtract the Entry timestamp from the Exit timestamp.

### 3. Confidence Scoring & Fuzzing
Because `GC=F` futures prices have a slight premium over spot `XAUUSD` prices, exact matches might miss by pennies. Implement a fuzzing tolerance:
- **High Confidence (Score 1.0):** The prices fell within the exact high/low bounds in a chronologically valid sequence.
- **Medium Confidence (Score 0.5):** The algorithm had to expand the High/Low bounds by a small tolerance (e.g., ±$1.00) to find a match.
- **Low Confidence (Score 0.0):** Discard. Multiple ambiguous hits or no logical chronological sequence found.

### 4. Output (The Core Goal)
The output must report:
1. **Average Time-in-Trade (Winning Trades)**
2. **Average Time-in-Trade (Losing Trades)**
3. **Average MFE (Max Favorable Excursion)**
4. **Average MAE (Max Adverse Excursion)**

Please build this script, execute it against the ledger, and return the final read-only metrics.
