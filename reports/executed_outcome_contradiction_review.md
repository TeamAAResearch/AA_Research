# Contradiction Review: Phase 5 Executed Outcomes

**Classification:** Observation Report (Contradiction Testing)
**Owner:** AG (Chief Research Analyst)
**Date:** 2026-06-24
**Status:** Awaiting GM Review

---

## 1. Concentration Review (Testing "Negative Expectancy")

Phase 5 concluded that the executed cohort possesses a net negative expectancy, generating a total realized PNL of -$1,346.14. This review assessed whether that loss was structural or concentrated.

* **Extreme Loser Concentration:** 
  The top 3 losing trades combined for a staggering **-$1,122.00** in realized losses.
* **Remaining Portfolio:**
  If the 3 worst trades are removed from the 148-trade sample, the total realized PNL of the remaining 145 trades is merely -$224.14.

**Contradiction Result:** *Weakened.* The hypothesis that the engine's core flow has a deep negative structural expectancy is challenged. The engine is essentially flat/breakeven across 98% of its trades. The negative expectancy is almost entirely a function of a catastrophic failure to manage tail-risk on 2% of the trades.

---

## 2. Buy vs Sell Validation

Phase 5 observed that Buy (Long) trades were uniformly destructive (-$2,392 PNL) while Sell (Short) trades were profitable (+$1,046 PNL). This review tested whether this was a true side-bias or an artifact of a single heavy-volume symbol (like Silver).

* **Buy Losses by Symbol:** Losses were distributed across the entire book. XAGUSD (-$869), GBPJPY (-$523), EURUSD (-$266), GBPUSD (-$261), and AUDUSD (-$263) all generated heavy losses on the Long side.
* **Sell Profit by Symbol:** Profits were similarly distributed. XAGUSD (+$891), XAUUSD (+$128), and GBPJPY (+$123) all generated positive returns on the Short side.

**Contradiction Result:** *Survived.* The observation holds up to segmentation. The trading engine possesses a true, portfolio-wide structural edge on Short setups and a structural defect on Long setups.

---

## 3. Duration Review Validation

Phase 5 concluded that longer-duration trades (> 1 hour) are associated with poorer outcomes.

* **Sample Quality:** Only 50 of the 148 trades had a recorded `time_in_trade_seconds`. 
* **Bucket Sizes:** The losing longer-duration buckets consisted of extremely small samples (6 trades in the 1h-4h bucket, 8 trades in the >4h bucket).

**Contradiction Result:** *Weakened.* While the directional observation remains true within the tracked dataset, the sample sizes (6 and 8 trades) are statistically insignificant. We cannot robustly claim that duration causes the capital bleed based on this evidence alone.

---

## 4. XAGUSD Review

Phase 5 identified XAGUSD as a primary anomaly because it produced positive overall PNL despite a terrible 31.9% win rate, implying highly asymmetric structural winners. 

* **Extreme Winner Concentration:** The top 3 winning trades for XAGUSD generated **+$1,548.66**.
* **Remaining Silver Portfolio:** If those 3 lucky tail events are removed, the remaining 69 Silver trades generated **-$1,526.72**.

**Contradiction Result:** *Contradicted.* The claim that Silver contributes positively via a distinct behavioral profile is false. Silver does not possess a structural edge; its apparent profitability was a mirage created by 3 massive outlier wins. Beneath the outliers, Silver is the most toxic, aggressively losing asset in the portfolio.

---

## 5. Unknowns Register

To adhere to the standard that "Observation ≠ Hypothesis," the following limitations are explicitly recorded:

* **What remains unknown:** 
  * Why the engine fails so catastrophically to cut the top 3 losing tail-events (did the market gap over the stop loss, or did the engine fail to set a stop loss?).
  * Why the engine has a portfolio-wide defect on Long signals.
* **What cannot be concluded:** 
  * We cannot conclude that simply disabling "Buys" would instantly make the system profitable in the future, as market regimes shift.
* **What evidence would strengthen current observations:**
  * Analyzing the `close_reason` for the top 3 losers to determine if they were systemic risk-management failures or unavoidable market gaps.
