# Diagnostic Investigation v1: Tail-Risk Root Cause

**Classification:** Diagnostic Report
**Owner:** AG (Chief Research Analyst)
**Date:** 2026-06-25
**Status:** Awaiting GM Review

---

## 1. Methodology
This investigation performed trade forensics on the three most catastrophic losing trades in the `challenger_trades` ledger. These three trades generated 83% of the portfolio's entire historical losses (-$1,122 combined). The objective was to reconstruct the decision path and execution reality of these trades to determine why the losses were so extreme.

**Evidence Reviewed:**
* Database: `trading_system.sqlite3`
* Table: `challenger_trades`
* Target IDs: 4, 1, 128 (Top 3 highest MAE/Realized losses)

---

## 2. Trade Forensic Summaries

### Trade A (ID: 4)
* **Symbol:** XAGUSD
* **Side:** Sell
* **Created At:** 2026-06-05
* **Realized Loss:** -$425.04
* **Close Reason:** `paper stop loss hit`
* **Entry / Exit:** 71.428 / 72.0352 (0.85% adverse move)
* **Time in Trade:** Unknown (Legacy record)
* **Sample Type:** `legacy_unknown`
* **Observation:** This trade predates the modern Observation Pipeline logging. It was executed with a massive quantity (700 units) and hit a programmed stop-loss at ~0.85% distance. 

### Trade B (ID: 1)
* **Symbol:** XAGUSD
* **Side:** Buy
* **Created At:** 2026-06-05
* **Realized Loss:** -$412.55
* **Close Reason:** `paper stop loss hit`
* **Entry / Exit:** 73.596 / 72.989 (0.82% adverse move)
* **Time in Trade:** Unknown (Legacy record)
* **Sample Type:** `legacy_unknown`
* **Observation:** Similar to Trade A, this is an untracked legacy trade from early June. It hit a standard stop-loss at ~0.82% distance. The absolute dollar loss was driven by position sizing (679 units) rather than a market gap or execution failure.

### Trade C (ID: 128)
* **Symbol:** GBPJPY
* **Side:** Buy
* **Created At:** 2026-06-23
* **Realized Loss:** -$284.41
* **Close Reason:** `paper stop loss hit`
* **Session:** London
* **Time in Trade:** 75,149 seconds (20.8 hours)
* **MFE / MAE:** -$0.47 MFE / -$284.41 MAE
* **Sample Type:** `standard_signal`
* **Observation:** This is a fully tracked modern trade. It hit a programmed stop-loss of ~0.56% (Entry: 214.658, Exit: 213.437). The trade was wrong from the exact moment of entry (Max Favorable Excursion was effectively zero). It bled slowly against the engine for nearly 21 hours before finally being killed by the hard stop loss.

---

## 3. Root-Cause Candidates

**Candidate 1: Data Contamination (Legacy Position Sizing)**
* *Applies to:* Trades A and B (XAGUSD)
* *Assessment:* The two worst trades in the system's history are not indicative of current tail-risk vulnerability. They are legacy artifacts from early testing (June 5). The losses occurred because the trades hit normal stop-losses while carrying improperly scaled legacy quantities.

**Candidate 2: Strategy Defect (Lack of Time-Based Exits)**
* *Applies to:* Trade C (GBPJPY)
* *Assessment:* Trade C was not a victim of a sudden market gap or an execution failure. The stop-loss executed exactly as programmed. The root cause of the loss is a strategy defect: the engine held onto a fundamentally dead long-side trade for 20.8 hours. Because there is no time-based kill switch or dynamic invalidation logic, the engine allowed a slow bleed to hit the maximum possible dollar loss.

---

## 4. Unknowns & Confidence Assessment

**Unknowns:**
* Why the modern opportunity engine generated a 75/100 score for GBPJPY exactly at the top of a local swing, leading to zero MFE.
* Whether legacy trades (IDs 1-100) should be purged from the overall expectancy review to provide a true reflection of the modern engine's performance.

**Confidence Assessment:** HIGH. 
The forensic data is explicit. We can state with high confidence that the system's catastrophic losses are **not** caused by market gaps, execution slippage, or a failure of the stop-loss code. The stops are executing correctly. The absolute losses are driven by legacy position sizing and strategic stubbornness (holding dead trades for 20+ hours).
