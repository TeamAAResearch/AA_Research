# AA Project — Failure & Survivability Study
**Date:** 2026-06-22
**Objective:** Determine why autonomous systems fail and identify measurable warning signs prior to failure, mapped directly against AA's existing telemetry.

---

## Part 1: Case Studies of Historic Failures

### Case 1: Long-Term Capital Management (LTCM)
*   **Type:** Institutional Quant Fund
*   **Time Period:** 1998
*   **Failure Description:** Total fund collapse requiring a $3.6 billion bailout.
*   **Root Cause:** **Regime Dependency & Risk Explosion.** The models assumed historical correlations would hold. When the Russian financial crisis occurred, correlations broke, liquidity evaporated, and massive leverage triggered an uncontrollable drawdown.
*   **Earliest Warning Sign:** Spreads on paired trades began diverging rather than converging, simultaneously across uncorrelated assets.
*   **Measurable Before Failure?:** Yes. The Value at Risk (VaR) models were actively flashing red prior to the ultimate margin calls, but humans overrode the risk gates assuming mean reversion.

### Case 2: Knight Capital Group
*   **Type:** Systematic Market Maker
*   **Time Period:** August 2012
*   **Failure Description:** Lost $440 million in 45 minutes, bankrupting the firm.
*   **Root Cause:** **Infrastructure & Execution Failure.** A faulty software deployment reactivated dormant, untested test-code (Power Peg) which executed millions of erratic trades at a loss.
*   **Earliest Warning Sign:** An explosion in fill volume and execution errors immediately at the market open.
*   **Measurable Before Failure?:** Yes. A hard kill-switch based on execution frequency/volume or abnormal P/L velocity would have caught it in seconds.

### Case 3: Generic Retail "Expert Advisors" (Grid/Martingale)
*   **Type:** Retail Algorithmic Systems
*   **Time Period:** Continuous / Modern Era
*   **Failure Description:** Complete account liquidation (Margin Call).
*   **Root Cause:** **Overfitting & Risk Explosion.** The models are over-optimized for ranging markets. When a trending macro regime hits, the system recursively doubles down on losing positions.
*   **Earliest Warning Sign:** Exponentially growing Maximum Adverse Excursion (MAE) without corresponding trade closure.
*   **Measurable Before Failure?:** Yes. Continuous tracking of MAE and Portfolio Concentration would clearly identify the risk explosion before account ruin.

---

## Part 2: Failure Taxonomy

### 1. Opportunity Starvation
*   **Definition:** The system is fundamentally unable to find trades that meet its criteria.
*   **Observable Symptoms:** Trade frequency drops to near zero; capital remains entirely in cash.
*   **Earliest Indicators:** A prolonged divergence between "Signals Generated" and "Signals Admitted."
*   **AA Evidence Status:** Yes, explicitly tracked in the FX Opportunity Ledger.

### 2. Strategy Decay
*   **Definition:** The statistical edge of the signal deteriorates as market participants adapt.
*   **Observable Symptoms:** Gradual decline in win rate and average profit per trade.
*   **Earliest Indicators:** The ratio of MFE (Maximum Favorable Excursion) to MAE (Maximum Adverse Excursion) begins shrinking before the win rate drops.
*   **AA Evidence Status:** Partial (Requires a much larger sample size to measure MFE/MAE decay reliably).

### 3. Overfitting
*   **Definition:** The model learned the noise of historical data rather than the underlying signal.
*   **Observable Symptoms:** Excellent backtest performance followed by immediate, consistent failure in live/forward testing.
*   **Earliest Indicators:** High confidence admission scores consistently resulting in immediate, sharp drawdowns upon entry.
*   **AA Evidence Status:** Yes, observable through `entry_score` vs `realized_pnl` tracking.

### 4. Regime Dependency
*   **Definition:** The strategy only works in specific environments (e.g., low volatility) and collapses when the regime shifts.
*   **Observable Symptoms:** Clustered losses occurring simultaneously across the portfolio following a macro event.
*   **Earliest Indicators:** A sudden shift in the `volatility_regime` tags accompanied by widespread risk-gate triggers.
*   **AA Evidence Status:** Yes, currently logged via `volatility_regime` and session tracking.

### 5. Portfolio Concentration
*   **Definition:** The system unintentionally takes massive directional risk by buying correlated assets.
*   **Observable Symptoms:** Multiple positions moving in lockstep, compounding drawdowns.
*   **Earliest Indicators:** Cluster limit warnings triggering in the portfolio filter.
*   **AA Evidence Status:** Yes, actively tracked via Stage 3 Portfolio Blocks (e.g., Long USD cluster limit).

### 6. Risk Suppression (Gates Too Tight)
*   **Definition:** Overly aggressive risk rules prevent the system from taking perfectly valid, profitable trades.
*   **Observable Symptoms:** High opportunity generation but zero admitted trades.
*   **Earliest Indicators:** High volume of Stage 4 (Risk Block) rejections for trades that subsequently would have won.
*   **AA Evidence Status:** Yes, actively tracked in the Pipeline Attrition matrix.

### 7. Risk Explosion (Gates Too Loose)
*   **Definition:** The system takes on catastrophic risk due to failed sizing logic or ignored stops.
*   **Observable Symptoms:** Single trades generating outsized losses that wipe out weeks of profit.
*   **Earliest Indicators:** MAE greatly exceeding historical averages on open positions.
*   **AA Evidence Status:** Yes, actively tracked via Risk Cap limits and MAE logging.

### 8. Execution Failure
*   **Definition:** The system generates good signals but cannot execute them effectively due to slippage, spread, or API latency.
*   **Observable Symptoms:** Large divergence between paper profit and live profit.
*   **Earliest Indicators:** High `spread_at_entry` or Stage 6 (Kill Switch/Broker) blocks.
*   **AA Evidence Status:** Yes, currently monitored by Stage 6 block tracking.

---

## Part 3: AA Telemetry Mapping
*If AA fails, what are the earliest indicators we should expect to see?*

| Failure Mode | Observable? | Evidence Source | Current Status |
| :--- | :--- | :--- | :--- |
| **Opportunity Starvation** | Yes | FX Opportunity Ledger | **Collecting** |
| **Risk Suppression** | Yes | Pipeline Attrition (Stage 4) | **Collecting** |
| **Portfolio Concentration** | Yes | Pipeline Attrition (Stage 3) | **Collecting** |
| **Regime Dependency** | Yes | Session Analysis / Volatility Tags | **Collecting** |
| **Execution Failure** | Yes | Pipeline Attrition (Stage 6) | **Collecting** |
| **Data Quality Failure** | Yes | Heartbeat / Runner Logs | **Collecting** |
| **Strategy Decay** | Partial | MFE/MAE Database | Pending (Insufficient sample) |
| **Overfitting** | Partial | Score vs P/L Database | Pending (Insufficient sample) |
| **Risk Explosion** | Partial | MAE / Risk Block Logic | Pending (Requires open exposure) |

### Survivability Awareness Conclusion
AA is currently deeply insulated against *Risk Explosion*, *Portfolio Concentration*, and *Execution Failure* due to the strictness of the Stage 3, 4, and 6 gates. 

Conversely, the data proves AA is currently suffering from **Risk Suppression** and **Opportunity Starvation** (specifically in FX). The primary warning sign for a "slow death" by starvation is already clearly observable in the FX Opportunity Ledger. We have successfully caught the earliest indicator of this failure mode before the system ever touched real capital.
