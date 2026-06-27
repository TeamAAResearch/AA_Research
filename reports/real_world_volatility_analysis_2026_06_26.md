# Real-World Volatility Analysis: FX vs Metals
**Date:** 2026-06-26
**Scope:** ATR Baseline calculation (6-month trailing window)

## The Data

We extracted the daily True Range (TR) for the past 6 months and calculated the 14-day Average True Range (ATR) as a percentage of the closing price for the major assets. 

| Asset | Ticker | 6-Mo Average Daily ATR (%) |
| :--- | :--- | :--- |
| **Euro** | EURUSD=X | 0.6467% |
| **Pound** | GBPUSD=X | 0.7339% |
| **Yen** | JPY=X | 0.6477% |
| **Gold** | GC=F | **2.3461%** |
| **Silver** | SI=F | **5.0844%** |

## Baseline Mathematical Extrapolations

If we treat the EURUSD average ATR (0.64%) as the statistical baseline for the `0.1%` momentum threshold parameter, we can calculate the mathematically equivalent momentum push for Metals.

*   **Gold (XAUUSD):** Volatility Multiplier vs EURUSD = **3.63x**
    *   **Optimal Intraday Momentum Threshold:** `0.1% * 3.63 = 0.3628%`

*   **Silver (XAGUSD):** Volatility Multiplier vs EURUSD = **7.86x**
    *   **Optimal Intraday Momentum Threshold:** `0.1% * 7.86 = 0.7862%`

## Conclusion
The heuristic guess of 0.25% was completely wrong. Gold is 3.6x more volatile than Euro, meaning its threshold must be roughly 0.36% to represent an identical level of signal conviction. Silver is wildly volatile (nearly 8x Euro), requiring a massive 0.78% push to clear the equivalent noise band.

> [!WARNING]
> Because Silver's volatility is double that of Gold, a generic "Metals Threshold" is mathematically unsound. We must update the system to support per-symbol threshold overrides.
