# Phase 7: Regime Shift Observation

**Classification:** Diagnostic Report
**Owner:** AG (Chief Research Analyst)
**Date:** 2026-06-25
**Status:** Awaiting GM Review

---

## Evidence
A review of the newly available trading data (June 24 to June 25 10:16) reveals a massive structural shift in AA's execution behavior. 

**Dataset Analyzed:** `challenger_trades` IDs 136 through 186 (51 total trades in the new regime).

**Regime Statistics:**
* **Volume:** 51 trades executed in roughly 36 hours.
* **Symbol Concentration:** 40 of 51 trades (78%) were XAUUSD (Gold). The remaining were sporadic EURJPY, GBPJPY, and USDCHF.
* **Win Rate:** 45 wins, 6 losses (88% win rate).
* **Average Win:** +$11.15
* **Average Loss:** -$134.43
* **Duration:** The average time in trade for XAUUSD has collapsed from ~15 hours down to between 5 and 30 minutes. 

**Exit Mechanisms Triggered:**
In the previous regime (pre-June 24), almost all trades were exited via `paper stop loss hit` or `Open/Timeout` after 15-20 hours. In the new regime, 45 of 51 trades exited via a new mechanism: `AA day-trader trailing protection exit: protect open profit` or `AA day-trader quick profit exit: intraday target captured`. 

The 6 losing trades (5 XAUUSD, 1 legacy AUDUSD) were all closed via `paper stop loss hit` at roughly -$100 to -$120 (for Gold) or -$263 (for the legacy AUD). The trailing stop mechanism did not close any trades for a loss.

## Interpretation
AA has undergone a complete regime shift. It is no longer behaving as a slow, long-duration FX trend follower. It is currently operating as a hyper-active, high-probability Gold scalper. 

The system relies on a trailing stop to aggressively lock in small, rapid profits (~$11). However, it retains a standard hard stop-loss that is roughly 10x to 12x the size of its average win (-$110 to -$130 for Gold). This mathematically means that a single stop-loss hit wipes out roughly 11 consecutive scalping wins. The system's extreme 88% win rate is the only thing keeping the net PNL from collapsing.

## Hypothesis candidates
1. **The Negative Skew Hypothesis:** AA's new day-trading regime exhibits extreme negative skew (risk-reward ratio of ~ 1:12). While the win rate is high enough to generate short-term stability, this mathematical profile guarantees that a single low-volatility chop session will wipe out weeks of accumulated scalping profits. The system is structurally fragile.

## Contradiction tests
1. To contradict the Negative Skew hypothesis, we must query the ledger to find if the trailing stop ever allows a trade to capture a "home run" (e.g. a win > $50 for Gold) that offsets the -$120 stops. If the trailing stop *always* chokes profits at ~$11, the negative skew is permanent.

## Open questions
* Why did AA spontaneously switch from long-duration FX trading to high-frequency Gold scalping on June 24? Was a new module or strategy deployed to the runner?
* Given the new behavior, does the previous Phase 6 simulation (Time-Decayed MFE exit at 12 hours) even apply to the current engine, since it now exits trades in under 30 minutes?

GM Review Required
