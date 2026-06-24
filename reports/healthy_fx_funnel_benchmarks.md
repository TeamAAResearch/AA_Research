# AA Project — Research Memo: Healthy FX Opportunity Funnels
**Date:** 2026-06-22
**Topic:** What does a profitable systematic FX operation typically look like?

---

## 1. Opportunity Frequency
Systematic FX operations generally operate on the principle that edge is small and must be applied across a statistically significant sample to yield a smooth equity curve. For an intraday/short-term momentum system like AA:
*   **Opportunities (Signals) per day:** 50 – 250 across a basket of 10-20 pairs.
*   **Executed Trades per day:** 5 – 25.
*   **Implication:** A healthy systematic FX firm expects to see continuous raw signal flow. Total silence is a sign of broken generation logic, not high quality.

## 2. Funnel Economics (Signal-to-Trade Conversion)
Institutional systematic models are essentially massive rejection engines. 
*   **Signal-to-Trade Conversion:** Typically **10% to 20%**. 
*   **Rejection Rates:** A healthy system rejects 80% to 90% of all generated signals.
*   **Why?** Raw signals are naive. The majority of rejections in a healthy firm do not happen because the signal is "bad," but because the *portfolio* cannot support it (e.g., USD exposure is already maxed, volatility is too high, or spread/liquidity during that hour ruins the math).

## 3. Pair Concentration
Where do profits typically come from in systematic FX?
*   **The Majors (70%+ of profit):** EURUSD, USDJPY, GBPUSD, AUDUSD, USDCAD, USDCHF. These pairs offer the deepest liquidity and tightest spreads, allowing algorithmic models to execute with minimal slippage.
*   **The Crosses (10-30% of profit):** Pairs like GBPJPY or EURGBP offer higher volatility and larger average pip movements, but carry higher transaction costs.
*   **Warning Sign:** If an FX operation derives 100% of its P/L from a single exotic cross or solely from metals, it is not an FX business; it is exposed to an unhedged idiosyncratic risk.

## 4. Session Concentration
The FX market is continuous, but opportunity flow is highly localized:
*   **London/NY Overlap (13:00 - 16:00 UTC):** The absolute peak of daily liquidity and volatility. For momentum or breakout systems, this 3-hour window often generates the highest quality opportunity flow and the cleanest executions.
*   **London Session (08:00 - 16:00 UTC):** Accounts for roughly 40% of global daily FX turnover.
*   **Asia Session (00:00 - 08:00 UTC):** Characterized by lower volume, tighter ranges, and mean-reverting behavior. Systematic momentum models typically experience "signal droughts" or false breakouts here.
*   **Implication:** A healthy FX funnel expects opportunity generation to spike dramatically at 08:00 UTC and peak at 13:00 UTC.

## 5. Opportunity Starvation
How do systematic firms determine if they are too selective?
*   **The "Win Rate vs. Trade Frequency" Paradox:** Firms monitor for a scenario where the Win Rate approaches 70-80%, but Trade Frequency drops to near zero. In systematic trading, exceptionally high win rates are usually a symptom of over-filtering (curve fitting) rather than genius.
*   **The Benchmark:** If the portfolio is sitting in 100% cash during the London/NY overlap despite the market moving 100+ pips, the risk gates or admission thresholds are mathematically starving the portfolio of the variance needed to capture the edge.

## 6. Opportunity Coverage
How do firms estimate the opportunities missed by the system?
*   **Shadow Portfolios:** Successful systematic funds run "Shadow Ledgers." When a trade is blocked by a Risk Gate or Portfolio Limit, the system records it as a "Shadow Trade" and tracks its theoretical entry, MFE, MAE, and exit. 
*   **Analysis:** At the end of the month, the firm compares the Realized P/L of the admitted trades against the Theoretical P/L of the Shadow Portfolio. If the Shadow Portfolio is highly profitable, it mathematically proves that the risk gates are suppressing the firm's edge.

---

### Conclusion: What does a healthy funnel look like?
A healthy FX funnel generates a massive, noisy top-of-funnel signal flow (50+ per day), rejects 85% of them through strict portfolio-level correlation and risk gates, and executes the remaining 15% cleanly, predominantly during the London and New York sessions using major currency pairs.
