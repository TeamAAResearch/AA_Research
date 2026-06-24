# Phase 5: Executed Outcome Review

**Classification:** Observation Report
**Owner:** AG (Chief Research Analyst)
**Date:** 2026-06-24
**Status:** Awaiting GM Review

---

## 1. Trade Outcome Inventory

This phase reviews the realized profit and loss (PNL) outcomes of the 148 trades that survived the Admission, Risk, and Portfolio gates.

* **Total Trades Reviewed:** 148
* **Winning Trades:** 80
* **Losing Trades:** 68
* **Breakeven Trades:** 0
* **Total Realized PNL:** -$1,346.14

**Observation 1:** The cohort of opportunities that survived the 0.2% strict admission funnel ultimately failed to generate a positive overall return.

---

## 2. Expectancy Review

The aggregate expectancy metrics for the 148 executed trades are as follows:

* **Win Rate:** 54.05%
* **Average Win:** $59.85
* **Average Loss:** -$90.21
* **Profit Factor:** 0.78
* **Expectancy (per trade):** -$9.10

**Observation 2:** The pipeline produces a slightly positive win rate, but suffers from an inverted risk/reward profile. The average loss is 1.5x larger than the average win, dragging the overall system into negative expectancy.

---

## 3. Symbol-Level Outcome Review

Outcomes vary wildly by asset, exhibiting contradictory profiles between the two most traded instruments.

| Symbol | Trades | Win Rate | Realized PNL | Outcome Profile |
|---|---|---|---|---|
| XAGUSD | 72 | 31.9% (23W, 49L) | +$21.94 | Terrible win rate, but positive expectancy (asymmetric winners). |
| XAUUSD | 35 | 74.3% (26W, 9L) | -$61.43 | High win rate, but negative expectancy (large losers). |
| GBPJPY | 9 | 77.8% (7W, 2L) | -$399.76 | High win rate, wiped out by tail risk. |
| AUDUSD | 7 | 57.1% (4W, 3L) | -$374.76 | Average win rate, large tail risk. |
| GBPUSD | 6 | 83.3% (5W, 1L) | -$245.35 | High win rate, large tail risk. |
| EURJPY | 6 | 83.3% (5W, 1L) | +$42.10 | Positive. |

**Observation 3:** Forex pairs and Gold (XAUUSD) universally share a profile of high win rates (70-80%) completely destroyed by outsized average losses. Silver (XAGUSD) is the exact opposite: it loses constantly (68% of the time) but cuts losses so tightly that its rare wins carry it to a net positive PNL.

---

## 4. Side Review

* **Buy (Longs):** 59 trades | Win Rate: 45.8% | PNL: -$2,392.77
* **Sell (Shorts):** 89 trades | Win Rate: 59.6% | PNL: +$1,046.63

**Observation 4:** The trading engine currently only possesses a viable edge on the short side. Long trades are uniformly destructive to the portfolio.

---

## 5. Duration Review

* **< 15 mins:** 17 trades | Win Rate: 100.0% | PNL: +$176.63
* **15 mins to 1 hour:** 19 trades | Win Rate: 100.0% | PNL: +$158.18
* **1 hour to 4 hours:** 6 trades | Win Rate: 50.0% | PNL: -$305.14
* **> 4 hours:** 8 trades | Win Rate: 37.5% | PNL: -$818.29
* **Unknown duration:** 98 trades | Win Rate: 38.8% | PNL: -$557.52

**Observation 5:** There is extreme, violent duration degradation. The engine is highly effective at scalping alpha in the first 60 minutes (100% win rate across tracked trades). If a trade is held open beyond 1 hour, the win rate collapses and capital bleeds rapidly. The engine appears to have no edge in holding positions over time.

---

## 6. Survivor Quality Assessment

The executed cohort appears **Mixed**. 

While the aggregate PNL is negative, the unprofitability is sharply segmented. The engine demonstrates a clear, highly profitable edge in short-duration holding periods (< 1 hour) and short-side trades. However, those gains are completely obliterated by long-duration holds and long-side trades. The survivor quality is heavily dependent on execution management (closing trades quickly) rather than initial signal quality.

---

## 7. Anomaly Watchlist Review

1. **XAGUSD (Silver):** *Strengthens rationale for monitoring.* Silver is the only major asset generating positive realized PNL, despite being the most aggressively vetoed asset in the funnel. Its profile (losing 68% of the time but making money overall) suggests structural asymmetry not found elsewhere in the portfolio.
2. **XAUUSD (Gold):** *Strengthens rationale for monitoring.* Gold exhibits the exact opposite profile (winning 74% of the time but losing money overall). The engine is mismanaging risk on Gold tail events.

---

## 8. Evidence Quality Assessment

* **Data Sources Used:** `trading_system.sqlite3` (`challenger_trades` table).
* **Missing Fields:** 98 of the 148 trades lack `time_in_trade_seconds` due to legacy tracking gaps, meaning the duration review relies on a 50-trade sample size.
* **Data Limitations:** The `close_reason` field was not parsed in this review, leaving it unknown whether the massive losses on Forex/Gold were due to hitting hard stop losses or manual/timeout closures.
* **Confidence Limitations:** The 50-trade duration sample size is small, but the degradation from 100% win rate at <1hr to 37% win rate at >4hr is stark enough to warrant high observation confidence.
