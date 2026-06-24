# Evidence Review: Interim Synthesis
**Date:** 2026-06-24
**Owner:** AG (Chief Research Analyst)
**Status:** Awaiting GM Review

---

## 1. Review Coverage

**Completed Review Phases:**
* Phase 1 – Admission Funnel Review
* Phase 2 – Risk Block Review
* Phase 2 Contradiction Review
* Phase 3 – Portfolio Block Review
* Phase 4 – Executed Trade Review

**Datasets Examined:**
* `trading_system.sqlite3` (`aa_journal`, `blocked_signals`, `challenger_trades` tables)
* `ledgers/opportunity_funnel.csv`
* Shadow Risk Engine simulated counterfactual outcomes

**Datasets Remaining Unreviewed:**
* Realized PNL and Win/Loss outcomes for Executed Trades.
* Score Distribution correlation with profitability.
* Deep-dive Pair/Symbol analysis (specifically XAGUSD).

---

## 2. Confirmed Observations Register

*Observations that survived contradiction testing and GM review.*

1. **Extreme Funnel Attrition:** The trading pipeline operates at a ~0.2% survival rate from raw loop to execution. ~93% of formally evaluated signals are blocked by governance and risk gates.
   * *Supporting Reports:* Phase 1, Phase 4
   * *Supporting Datasets:* `opportunity_funnel.csv`
   * *Known Limitations:* Does not evaluate if the 0.2% survival rate generates alpha.

2. **Negative Structural Expectancy of Rejected Flow:** The opportunity generation engine frequently produces signals with deeply negative structural expectancy (average simulated MAE -5.25 vs MFE +3.48). The gates are effectively protecting capital from these toxic flows.
   * *Supporting Reports:* Phase 2
   * *Supporting Datasets:* Shadow Risk Engine Simulation
   * *Known Limitations:* Assumes zero slippage in the counterfactual simulation.

3. **Active Portfolio Interference:** 43.5% of blocked signals trigger a portfolio or risk-level veto (e.g., concentration limits, velocity caps). The portfolio manager acts as a massive secondary filter.
   * *Supporting Reports:* Phase 3
   * *Supporting Datasets:* `blocked_signals`

4. **The Survivor Profile:** Executed trades average extremely high admission scores (87.52), are overwhelmingly short duration (72% close within 1 hour), and heavily skew toward precious metals.
   * *Supporting Reports:* Phase 4
   * *Supporting Datasets:* `challenger_trades`, `opportunity_funnel.csv`

---

## 3. Contradicted Observations Register

*Observations weakened or modified through contradiction testing.*

* **Original Claim:** The Admission/Risk blockade is universally highly protective with a 65% defensive win rate.
* **Contradiction Result:** The 65% Stop Loss hit rate is heavily biased by synthetic simulation brackets (0.5% SL vs 1.0% TP). More importantly, the "false negative" suppressive effect (profitable trades incorrectly blocked) is overwhelmingly concentrated in a single asset: 78.6% of suppressed winners were Silver (XAGUSD).
* **Current Status:** Observation modified. The blockade is highly protective for the broad market, but heavily suppressive for XAGUSD.

---

## 4. Anomaly Watchlist

**1. XAGUSD (Silver)**
* **Supporting Evidence:** Extreme structural anomaly. Dominates the blocked signal list. Dominates the portfolio block list (currency/metal limits). Represents 78.6% of incorrectly blocked winners. Yet, despite being aggressively filtered, it still accounts for 50% of the entire executed book. 
* **Contradicting Evidence:** None. All data points to XAGUSD dominating the engine's flow.
* **Current Status:** Primary Anomaly Candidate.

**2. XAUUSD (Gold)**
* **Supporting Evidence:** Extreme signal velocity. Triggered 32 separate "2 entries in 60 minutes" velocity caps, indicating the generation engine is producing noisy, clustered signals. Accounts for 22.7% of the executed book.
* **Contradicting Evidence:** Does not exhibit the same massive false-negative suppressive trait as Silver.
* **Current Status:** Secondary Anomaly Candidate.

---

## 5. Evidence Gap Register

* **Unanswered Questions:** Do the 148 executed trades actually generate a positive realized PNL? Does the high admission score requirement (87.5 average) correlate with higher profitability?
* **Missing Evidence:** We lack the actual structural stop losses AA would have assigned to the blocked trades.
* **Data Limitations:** Trading session data is missing for a vast majority of evaluated signals. Counterfactual slippage is missing from simulation data.

---

## 6. Proposed Next Review Phase

**Recommend: Phase 5 – Executed Outcome Review**

* **Learning Value:** Highest priority. The organization has mapped *how* opportunities survive the funnel, but the ultimate arbiter of the engine's validity is realized PNL. If the 0.2% survival rate does not generate alpha, the strict pipeline is failing.
* **Evidence Availability:** High. The `challenger_trades` table contains full realized PNL, MAE, MFE, and close reasons for the executed cohort.
* **Organizational Priorities:** Aligns with the core objective of understanding the evidence we already possess to judge the health of the existing trading logic.
