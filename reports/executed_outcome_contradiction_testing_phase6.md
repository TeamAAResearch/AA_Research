# Phase 6: Tail-Risk Contradiction Testing

**Classification:** Diagnostic Report
**Owner:** AG (Chief Research Analyst)
**Date:** 2026-06-25
**Status:** Awaiting GM Review

---

## Evidence
This phase executed rigorous contradiction tests against the two active hypotheses regarding AA's tail-risk and catastrophic losses, utilizing the latest regenerated `trading_system.sqlite3` ledgers (up to June 25 10:16).

**Test 1: Legacy Sizing** 
*Query:* Do any trades executed post-June 15 (after modern Observation Pipeline deployment) suffer losses greater than -$300?
*Result:* Zero trades suffered a loss > -$300 post-June 15. The extreme -$425 losses (Trades 1 & 4) were strictly isolated to early June testing. However, modern trades still exhibit a dense cluster of severe losses near the -$270 to -$285 mark (Trades 128, 129, 134, 138).

**Test 2: Duration Bleed (Time-Based Exits)**
*Query:* Do trades held longer than 12 hours ever recover to a positive expectancy, or do they only bleed capital?
*Result:* Of the 7 trades held >12 hours:
* 4 trades (held 13 to 24 hours) resulted in catastrophic maximum losses (-$263 to -$284). Their Max Favorable Excursion (MFE) rarely exceeded $3.00 over their entire lifespan.
* 3 trades (held 15 to 17 hours) resulted in strong wins (+$38, +$53, +$267). 

## Interpretation
Hypothesis 1 (Legacy Sizing) is validated as the cause of the two absolute worst trades in history, but fails to explain why modern trades still cluster near -$280 losses. 

Hypothesis 2 (Duration Bleed) is structurally falsified as a blanket rule. While holding a dead trade for 20 hours *does* guarantee a max loss, a blind time-based kill switch (e.g., exiting all trades at 12 hours) would have accidentally killed Trade 127, which generated +$267 in profit after 15.9 hours. The true discriminator of a "dead" trade is not purely *time*, but *time spent with zero momentum* (MFE). The catastrophic losers spent 20 hours with MFE < $4.00, whereas the winners were deeply profitable during their hold times.

## Hypothesis candidates
1. **Time-decayed MFE Invalidation:** AA's structural tail-risk is caused by a failure to invalidate trades that exhibit zero momentum (MFE near $0) over extended durations (12+ hours). A dynamic exit rule based on Time + MFE (rather than Time alone) would eliminate the -$280 tail risk without choking the long-duration winners.

## Contradiction tests
1. To contradict the Time-decayed MFE hypothesis, we must backtest a synthetic exit condition: If a trade is held > 12 hours and its MFE is < $5.00, kill it. If this synthetic exit significantly reduces overall net profitability when applied to the historical ledger, the hypothesis is falsified.

## Open questions
* Is the Saxo Engine capable of tracking MFE dynamically in real-time to trigger a programmatic time-decay exit, or would this require a major architectural overhaul of the runner?
* Does a 12-hour MFE check simply mask the fact that the original admission score (Entry) was a false positive?

GM Review Required
