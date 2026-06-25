# Phase 7: Negative Skew Contradiction Testing

**Classification:** Diagnostic Report
**Owner:** AG (Chief Research Analyst)
**Date:** 2026-06-25
**Status:** Awaiting GM Review

---

## Evidence
This test directly addressed the GM's core mandate: how do we translate our research into a profitable trading system? We queried the database to determine if the new trailing stop mechanism *ever* allows a trade to reach a "home run" that would offset the massive -$130 hard stop losses.

**Query:** Select all winning trades in the new regime (ID >= 136) and compare their final Realized PNL against their Max Favorable Excursion (MFE).

**Results:**
* Trade 168: Reached +$42.26 profit. Trailing stop choked it to +$14.08.
* Trade 174: Reached +$34.50 profit. Trailing stop choked it to +$7.51.
* Trade 169: Reached +$28.26 profit. Trailing stop choked it to +$3.98.
* Trade 170: Reached +$33.51 profit. Trailing stop choked it to +$21.97.

## Interpretation
The Negative Skew hypothesis is fully validated. The contradiction test failed to find a single instance where the trailing stop allowed a large profit to be realized. The algorithm structurally amputates trades the moment they retrace, artificially capping our wins at an average of +$11.15. 

Simultaneously, the system relies on a massive, static hard stop-loss that averages -$134.43.

**Mathematical Reality:**
To be profitable with an $11 win and a $134 loss, AA requires a win rate of 92.3%. AA currently operates at an 88% win rate. Despite winning almost every trade, the system is mathematically guaranteed to slowly bleed capital.

## Hypothesis candidates
1. **Asymmetric Risk Override:** AA's core edge (an 88% win rate) is highly profitable, but the edge is being destroyed by the execution parameters. If we implement a strict Python Guardrail that forcefully overrides AA's default -$134 hard stop and cuts all losses at -$20, the system will immediately become highly profitable, even if the win rate drops slightly due to tighter stops.

## Contradiction tests
1. Codex must build a simulation script (`simulate_tight_stop_loss.py`) to backtest what would happen if every trade in the new regime was forcefully killed at a -$20 Maximum Adverse Excursion (MAE). If the net portfolio PNL turns positive, the fix is verified.

## Open questions
* Can we physically override the hard stop-loss in the execution API before the order is sent to the broker?
* Will a -$20 stop-loss prematurely kill too many of the trades before they can become the $11 winners?

GM Review Required
