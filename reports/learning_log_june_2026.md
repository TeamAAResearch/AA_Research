# Continuous Learning Log: June 2026 Review

## 1. Executive Summary
This document fulfills the **Continuous Learning Doctrine (Monthly Review)** mandate. It captures the critical structural, architectural, and algorithmic discoveries made during the June 2026 performance review of the Ari trading system. 

Codex (Engineering) must review this log to internalize the architectural standards for future engineering functions.

## 2. The 60-Minute Time Decay Eradication
**The Discovery:** A forensic study of 109 XAUUSD trades proved that the hard-coded 60-minute time-exit rule was mathematically toxic, destroying $3,908 of value by killing winners before they matured.
**The Engineering Change:** The 60-minute rule was eradicated from the physical execution loop. It was replaced with the **Alpha-Decay Scaling Model** (Phase 3/4), which dynamically evaluates a trade's drift against historical expected PnL rather than using a blind countdown timer.

## 3. Maximum Favorable Excursion (MFE) & Phase 5 Exits
**The Discovery:** Analysis of 87 `standard_signal` trades showed that Ari's entries are highly accurate, generating significant MFE. However, the system consistently surrendered 30-80% of this MFE due to wide trailing stops and late time-exits. The system was failing to capture peak profit.
**The Engineering Directive:** Phase 5 introduces the **Institutional Profit Capture Engine**, utilizing fixed-ATR scale-outs (e.g., 50% at +1.0 ATR, 50% at +2.0 ATR) rather than relying exclusively on trailing stops to protect unrealized gains.

## 4. The Infinity Doctrine & Regime-Aware Thresholds
**The Discovery:** The GM correctly identified that static thresholds (like a +1.0 ATR scale-out) are fragile to non-stationary market regimes. A breakout regime will hit +2.0 ATR easily, while a mean-reverting regime will fail at +1.0 ATR.
**The Engineering Directive:** Future exit modules must implement a **Regime-Shift Validation Check**. The system must continuously measure the MFE capture ratio against a rolling 100-trade window. If the regime shifts, the parameters must dynamically re-calibrate rather than remaining static.

## 5. Entry Timing, Heat (MAE), and The Algorithmic Paradox
**The Discovery:** 96% of winning trades absorbed massive heat (drawdown) before becoming profitable. AG tested a "Retracement Limit Order" hypothesis (-0.5 ATR limit entry) across 372,596 minutes of USDJPY data.
**The Paradox:** The simulation proved that waiting for a better price *destroyed* the mathematical edge. While 96% of limit orders were filled, the 4% that were missed were the absolute strongest "runaway" momentum trades. Missing the tail-end winners turned a positive expectancy system negative.

## 6. Microstructure Routing (The Board of Experts Veto)
**The Discovery:** AG proposed a "Dual-Tier Execution Engine" to use Market Orders on high tick velocity (to catch runaways) and Limit Orders on normal velocity (to optimize the 96%).
**The Red Team Veto:** The Board of Experts rejected the Dual-Tier concept for three reasons:
1. **Adverse Selection:** Static limits on momentum trades only fill when the thesis is wrong.
2. **Liquidity Vacuum:** Firing Market Orders during a 95th-percentile velocity spike guarantees catastrophic slippage against a depleted order book.
3. **Latency:** SQLite/Python cannot compute 95th-percentile velocity fast enough.
**The Engineering Directive:** The execution architecture must move toward an **Institutional Scale-In**. The system should immediately cross the spread with a fractional size (e.g., 20%) to guarantee a seat on the runaways, and use passive midpoint pegs to average in the remaining 80%.

## 7. Volatility Compression (VC) Filter
**The Discovery:** A statistical simulation proved that momentum breakouts have a negative expectancy (-0.022 R) in normal conditions, but a positive expectancy (+0.021 R) when they occur immediately after a Volatility Squeeze (60-minute ATR compresses below 70% of the 24-hour baseline).
**The Engineering Directive:** The Signal Engine should incorporate a VC filter to govern or prioritize momentum entries.
