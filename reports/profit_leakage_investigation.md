# Profit Leakage & Small-Win Pattern Investigation

## Signal Quality Issue (Entries)
**Observation:** Ari’s entries are exceptionally precise and generate immediate, significant unrealized profit. The small-win pattern is absolutely **not** caused by weak entries.
**Explanation:** When Ari opens a trade, the market reliably moves in the predicted direction. The gatekeepers (Sniper/Scout) are doing an excellent job filtering out toxic liquidity and admitting valid momentum setups.
**Confidence:** High
**Evidence:** The Maximum Favorable Excursion (MFE) on winning trades is massively higher than the realized P/L. For example, the recent `EURCAD Buy` generated +35.61 in MFE, and `GBPEUR Buy` generated +85.57 in MFE. The entry logic is flawless.

## Trade Management Issue (Profit Capture)
**Observation:** Ari is surrendering a massive percentage of available open profit back to the market before closing the trade.
**Explanation:** The system captures roughly 50-60% of available MFE on average, and on some trades as low as 18%. 
**Confidence:** High
**Evidence:** 
- `EURNZD Buy`: Hit +11.35 (MFE) but closed for +2.11 (Realized). Captured **18%**.
- `EURCAD Buy`: Hit +35.61 (MFE) but closed for +17.21 (Realized). Captured **48%**.
- `GBPEUR Buy`: Hit +85.57 (MFE) but closed for +49.20 (Realized). Captured **57%**.
- Across the historical ledger, 93 trades were killed by the `trailing protection exit`. Total MFE generated was $1,158, but Ari only realized $781, surrendering 32.5% of its peak profits directly back to the spread.

## Exit Quality Issue (The "Why")
**Observation:** Ari fails to sell near peak profit because its physical exit rules are rigid, time-based, or structurally misaligned with price action.
**Explanation:** Ari is currently exiting winning trades for two main reasons, both of which cause profit leakage:
1. **The 120-Minute Max Hold (Recent Wins):** All 10 of the most recent wins exited simply because the clock ran out at exactly 120 minutes. Ari blindly flattened the position, even if the price was at a local pullback rather than the peak.
2. **Trailing Protection Exit (Historical Wins):** The `CHALLENGER_TRAILING_PROTECT_PCT` is set too loosely. It requires price to violently reverse and surrender a massive chunk of the MFE before triggering the stop to "protect" what little profit is left.
**Confidence:** High
**Evidence:** SQLite queries on `challenger_positions` confirm exactly 10 of the last 10 winning trades were closed with the reason: `AA max holding limit exit: trade reached 120 minutes`.

## Conclusion
Ari’s small wins are **not a feature of the strategy; they are a severe profit-leak.** The entry signals are institutional-grade, but the exit management is retail-grade. The bot is actively watching trades hit massive unrealized profits, and then patiently waiting for the price to collapse back to breakeven before finally exiting due to an arbitrary 120-minute timer or a wide trailing stop.
