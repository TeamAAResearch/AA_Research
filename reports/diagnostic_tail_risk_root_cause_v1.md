# Diagnostic Investigation v1: Tail-Risk Root Cause

**Classification:** Diagnostic Report
**Owner:** AG (Chief Research Analyst)
**Date:** 2026-06-25
**Status:** Awaiting GM Review

---

## Evidence
This investigation performed trade forensics on the three most catastrophic losing trades in the `challenger_trades` ledger. These three trades generated 83% of the portfolio's entire historical losses (-$1,122 combined). The objective was to reconstruct the decision path and execution reality of these trades to determine why the losses were so extreme.

**Evidence Reviewed:**
* Database: `trading_system.sqlite3`
* Table: `challenger_trades`
* Target IDs: 4, 1, 128 (Top 3 highest MAE/Realized losses)

### Trade A (ID: 4) & Trade B (ID: 1)
* **Symbol:** XAGUSD
* **Realized Loss:** -$425.04 and -$412.55
* **Close Reason:** `paper stop loss hit`
* **Observation:** These trades predate the modern Observation Pipeline logging (early June). They hit programmed stop-losses at ~0.85% distance. The absolute dollar loss was driven by massive legacy position sizing (700 and 679 units) rather than market gaps or execution failure.

### Trade C (ID: 128)
* **Symbol:** GBPJPY
* **Realized Loss:** -$284.41
* **Close Reason:** `paper stop loss hit`
* **Time in Trade:** 75,149 seconds (20.8 hours)
* **MFE / MAE:** -$0.47 MFE / -$284.41 MAE
* **Observation:** Fully tracked modern trade. It hit a programmed stop-loss of ~0.56%. The trade was wrong from entry (zero MFE). It bled slowly against the engine for nearly 21 hours before being killed by the hard stop loss.

## Interpretation
The forensic data is explicit. We can state with high confidence that the system's catastrophic losses are **not** caused by market gaps, execution slippage, or a failure of the Saxo stop-loss code. The stops are executing correctly. The absolute losses are driven by legacy position sizing and strategic stubbornness (holding dead trades for 20+ hours).

## Hypothesis candidates
1. **Legacy Sizing Hypothesis:** The extreme tail-risk observed in historical ledger performance is an artifact of untracked legacy position sizing from early June, not a structural flaw in the modern trading engine.
2. **Duration Bleed Hypothesis:** The modern trading engine is bleeding capital because it lacks a time-based exit or dynamic invalidation logic, forcing it to absorb maximum possible MAE on trades that are fundamentally dead from entry.

## Contradiction tests
1. To contradict Hypothesis 1, we must query the SQLite database for any trade executed *after* the implementation of the modern Observation Pipeline (post June 15) that suffered a loss greater than -$300 due to position sizing.
2. To contradict Hypothesis 2, we must query the database to see if trades held longer than 12 hours ever recover to a positive expectancy, which would justify the engine holding them.

## Open questions
* Why did the modern opportunity engine generate a 75/100 admission score for GBPJPY exactly at the top of a local swing, leading to zero MFE?
* Should legacy trades (IDs 1-100) be purged from the overall expectancy review to provide a true reflection of the modern engine's performance?

GM Review Required
