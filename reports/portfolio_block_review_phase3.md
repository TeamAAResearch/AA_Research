# Phase 3: Portfolio Block Review

**Classification:** Observation Report
**Owner:** AG (Chief Research Analyst)
**Date:** 2026-06-24
**Status:** Awaiting GM Review

---

## 1. Portfolio Block Inventory

This phase quantifies how frequently opportunities that pass initial generation are subsequently vetoed by the Portfolio Manager or Risk limits before execution.

* **Total Blocked Opportunities Analyzed:** 377
* **Opportunities with Portfolio/Risk Blocks:** 164
* **Portfolio Block Frequency:** 43.50% of all blocked opportunities hit at least one portfolio or risk-level constraint.

**Observation 1:** Portfolio and concentration controls are a highly active layer of the funnel, materially shaping AA's realized trade flow by vetoing nearly half of all blocked setups.

---

## 2. Block Reason Analysis

A single blocked signal can trigger multiple portfolio vetoes simultaneously. The following limits were triggered:

| Portfolio / Risk Veto Reason | Frequency |
|---|---|
| Similar currency theme is already active in the book. | 99 |
| Metals concentration gate: active metals count 1 at limit 1. | 99 |
| Symbol activity cap active (Velocity Cap). | 38 |
| Planned risk cap active (Margin/Exposure Limit). | 21 |
| Currency cluster gate: Long USD exposure at limit (3/3). | 4 |

**Observation 2:** The "Metals concentration gate" and "Similar currency theme" vetoes fired in perfect lockstep (99 instances each). This indicates that the portfolio engine heavily penalizes metals for both their asset class (metals limit) and their underlying currency exposure (USD theme).

**Observation 3:** Velocity caps (e.g., "2 entries in 60 minutes") are actively suppressing high-frequency signal clusters, preventing the engine from firing multiple bullets into the same price action.

---

## 3. Symbol Analysis

Portfolio blocks are not evenly distributed across the tradable universe. They are highly concentrated in specific assets.

* **Top Affected Symbols:**
  * XAGUSD: 99 blocks (60.3%)
  * XAUUSD: 32 blocks (19.5%)
  * USDCHF: 10 blocks (6.0%)
  * USDCAD: 6 blocks (3.6%)
  * GBPUSD: 6 blocks (3.6%)
* **Side Distribution:**
  * Sell: 100 blocks
  * Buy: 64 blocks

**Observation 4:** Metals account for nearly 80% of all portfolio blocks. The portfolio constraints are effectively acting as a secondary filter that strips out Gold and Silver opportunities.

---

## 4. Opportunity Distribution Review

The data reveals that portfolio blocks are not randomly distributed. They concentrate heavily in specific assets and structural scenarios:

* **Signal Noise Suppression:** Of the 38 "Velocity Cap" blocks, 32 were directed at **XAUUSD**. This indicates that the opportunity generation engine is frequently producing rapid, clustered signals for Gold within a 60-minute window, which the portfolio manager is intentionally suppressing to prevent over-trading.
* **Structural Lockout:** XAGUSD's 99 portfolio blocks demonstrate a structural lockout. When the book already holds a single metal or a USD-heavy theme, XAGUSD opportunities are systematically discarded regardless of their individual merit.

---

## 5. Anomaly Watchlist Update

The following assets have been flagged for future review due to extreme deviation from the broader portfolio distribution:

1. **XAGUSD (Silver):** Added in Phase 2 due to negative expectancy blocks. Confirmed in Phase 3 as the primary victim of portfolio concentration limits.
2. **XAUUSD (Gold):** *New Candidate.* Added due to extreme signal velocity. Gold generated 32 velocity cap blocks ("2 entries in 60 mins"), suggesting the underlying signal generation logic is highly noisy or sensitive to Gold's tick path.

---

## 6. Evidence Quality Assessment

* **Data Sources Used:** `trading_system.sqlite3` (`blocked_signals` table).
* **Missing Fields:** Trading session data is not explicitly logged in the `blocked_signals` text output, preventing analysis of whether the XAUUSD velocity blocks occurred during overlapping liquidity windows (e.g., London/NY overlap).
* **Unknowns:** We do not know if the portfolio concentration limits (e.g., "Metals limit 1") are mathematically optimal, or if they are legacy heuristics that are overly restrictive.
* **Areas for Future Review:** The underlying signal generation logic for XAUUSD needs review to understand why it produces such rapid, clustered entry signals compared to forex pairs.

*(No strategy, risk, portfolio, or threshold changes are proposed. This document serves strictly as an Observation Report.)*
