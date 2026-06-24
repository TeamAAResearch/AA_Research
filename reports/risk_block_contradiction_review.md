# Contradiction Review: Phase 2 Risk Blocks

**Classification:** Observation Report (Contradiction Testing)
**Owner:** AG (Chief Research Analyst)
**Date:** 2026-06-24
**Status:** Awaiting GM Review

---

## 1. Simulation Dependency Review

Phase 2 proposed the hypothesis that the admission blockade is highly protective because 65% of blocked signals hit their stop loss. This review assesses whether that conclusion is a function of the data or an artifact of the simulation logic.

* **Bracket Dependency:** The Shadow Risk Engine applies a fixed 0.5% Stop Loss and a 1.0% Take Profit. Because the stop loss distance is exactly half the take profit distance, it is mathematically more likely to be triggered by random market noise. The "65% win rate" for the defense is heavily reliant on this skewed ratio. If the synthetic brackets were inverted, the hit rates would likely invert.
* **Independent Observations:** While the exact hit-rate is bracket-dependent, the Phase 2 observation that Maximum Adverse Excursion (MAE: -5.25) was worse than Maximum Favorable Excursion (MFE: +3.48) is **independent** of the synthetic brackets. The trades structurally move further against the entry price than for it.
* **Evidence Limitations:** Because AA was blocked at the Admission Gate, it never calculated dynamic, structure-based risk brackets for these setups. We do not know if AA would have naturally applied wider or tighter stops.

---

## 2. Cohort Segmentation

We separated the blocked opportunities into two distinct cohorts to determine if the outcomes remained consistent regardless of the rejection mechanism.

* **Admission Blocks (327 signals):**
  * Hit Stop Loss: 212 (64.8%)
  * Hit Take Profit: 74 (22.6%)
  * Open / Timeout: 41 (12.5%)

* **Risk / Portfolio Blocks (23 signals):**
  * Hit Stop Loss: 15 (65.2%)
  * Hit Take Profit: 1 (4.3%)
  * Open / Timeout: 7 (30.4%)

**Observation 1:** The failure rate is statistically identical (~65% hit Stop Loss) regardless of whether the signal was rejected for low admission scores or rejected due to downstream portfolio/risk limits. 

---

## 3. Winner Concentration Review

Phase 2 identified that 75 blocked signals would have hit their Take Profit (the "suppressive" false negative rate). We reviewed this profitable cohort to see if the suppression is random or concentrated.

* **Side Concentration:** Perfectly balanced (38 Buys, 37 Sells). Directionality is not a factor.
* **Session Concentration:** Unknown (Data field missing from funnel ledger).
* **Symbol Concentration:** Extreme clustering.
  * XAGUSD: 59 winners (78.6% of all false negatives)
  * NZDUSD: 8 winners
  * XAUUSD: 5 winners
  * AUDUSD: 3 winners

**Observation 2:** The suppressive effect of the blockade is not randomly distributed; it is overwhelmingly concentrated in a single asset (Silver). If XAGUSD is removed from the dataset, the admission/risk gates only incorrectly blocked 16 profitable trades out of the entire remaining population. 

**Observation 3:** The hypothesis that "the blockade is inherently protective" holds true for the broad market, but may be actively false for XAGUSD, where the strict threshold is suppressing a large cluster of profitable trades.

---

## 4. Unknowns Register

To adhere to the standard that "Observation ≠ Hypothesis," the following limitations are explicitly recorded:

* **What remains unknown:** 
  * Whether the 59 XAGUSD winners occurred sequentially in a single strong trend, or were distributed evenly over time.
  * Which trading sessions generated the profitable blocked trades.
  * What exact structural stop losses AA would have assigned if admitted.
* **What cannot be concluded:** 
  * We cannot conclude that 0.5% / 1.0% are the optimal risk brackets.
  * We cannot conclude that AA would have successfully held the 75 winners to their take profit targets without interfering and closing them early.
* **What evidence would be required for stronger conclusions:**
  * Re-running the simulation with symmetric brackets (e.g., 1.0% SL and 1.0% TP) to remove the distance-bias from the Stop Loss hit rate.
  * Extracting session time data to identify if XAGUSD winners correspond to specific liquidity windows.
