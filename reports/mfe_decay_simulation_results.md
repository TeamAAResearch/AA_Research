# MFE-Decay Exit Simulation Results

**Classification:** Simulation Report
**Owner:** AG / Codex
**Date:** 2026-06-25
**Status:** Internal GM Review Required

---

## Evidence

- Source database: `/Users/kennylee/Documents/Saxo/trading_system.sqlite3`
- Source table: `challenger_trades` joined with `challenger_ticks` by symbol and timestamp window.
- Cohort: closed `standard_signal` trades with `time_in_trade_seconds > 43200`.
- Trades reviewed: 7
- Rule tested: after 12 hours, exit if reconstructed MFE at the 12-hour checkpoint is below $5.00.
- Baseline cohort P/L: -730.56
- Synthetic cohort P/L: -945.48
- Net synthetic change: -214.92

| Trade ID | Symbol | Side | Duration h | Final P/L | MFE 12h | P/L 12h | Triggered | Synthetic P/L | Delta | Evidence |
|---:|---|---|---:|---:|---:|---:|---|---:|---:|---|
| 127 | XAUUSD | Sell | 15.93 | 267.59 | 303.99 | 172.50 | No | 267.59 | +0.00 | tick_reconstructed |
| 128 | GBPJPY | Buy | 20.87 | -284.41 | -254.13 | -357.78 | Yes | -357.78 | -73.37 | tick_reconstructed |
| 129 | EURUSD | Buy | 21.02 | -266.42 | -209.64 | -298.74 | Yes | -298.74 | -32.32 | tick_reconstructed |
| 132 | USDCHF | Sell | 17.59 | 38.97 | 48.25 | -102.68 | No | 38.97 | +0.00 | tick_reconstructed |
| 134 | GBPUSD | Buy | 24.66 | -276.69 | -230.14 | -255.58 | Yes | -255.58 | +21.11 | tick_reconstructed |
| 138 | AUDUSD | Buy | 13.74 | -263.57 | -183.64 | -393.92 | Yes | -393.92 | -130.35 | tick_reconstructed |
| 145 | GBPJPY | Sell | 17.42 | 53.97 | 125.07 | 27.81 | No | 53.97 | +0.00 | tick_reconstructed |

### Target Tail-Risk Trades

- Reviewed IDs: [128, 129, 134, 138]; triggered: [128, 129, 134, 138]; not triggered: []; P/L delta: -214.92.

### Long-Duration Winner Protection Check

- Reviewed IDs: [127, 132, 145]; triggered: []; not triggered: [127, 132, 145]; P/L delta: +0.00.

## Interpretation

- The rule triggered on 4 of 7 long-duration trades.
- The rule did not trigger on 3 long-duration trades.
- Target tail-risk trades caught: [128, 129, 134, 138].
- Target long-duration winners accidentally killed: [].
- In this historical cohort, the synthetic rule changes P/L by -214.92.
- This is a counterfactual simulation only. It does not authorize any operating policy modification.

## Hypothesis candidates

- Time-decayed MFE invalidation remains a candidate if it reduces tail-risk losses without materially cutting long-duration winners.
- The candidate is weakened if checkpoint MFE cannot separate dead trades from valid long-duration winners.

## Contradiction tests

- Re-test on future standard-signal trades after the current sample expands.
- Compare 12-hour MFE against score, side, and symbol to determine whether the rule is only masking entry-quality problems.
- Reconstruct path using denser tick history if available before any adoption review.

## Open questions

- Does sparse tick capture understate or overstate true 12-hour MFE?
- Is the 12-hour checkpoint economically meaningful across FX and metals, or only for the current sample?
- Would a smaller or larger MFE threshold produce a materially different separation?

GM Review Required
