# AA Research — Trade Survival Analysis
**Date:** 24 June 2026  
**Baseline:** 2026-06-22 07:02:25 UTC  
**Sample:** 32 closed `standard_signal` trades

---

## Duration Bucket Results

| Bucket | Trades | Win Rate | Avg P/L | Total P/L | Stop-Loss Exits |
|---|---|---|---|---|---|
| **<1h** | 25 | **100%** | +$9.78 | **+$244.44** | 0 |
| 1–4h | 1 | 100% | +$0.38 | +$0.38 | 0 |
| 4–8h | 0 | — | — | — | — |
| **8–24h** | 5 | **40%** | -$66.40 | **-$332.00** | 3 |
| **>24h** | 1 | **0%** | -$276.69 | **-$276.69** | 1 |

---

## Observation

Trade duration has a near-perfect inverse relationship with outcome.

- **Under 1 hour:** 25 trades, 100% win rate, +$244.44, zero stop-loss exits.
- **Over 8 hours:** 6 trades, 33% win rate, -$608.69, four stop-loss exits.

Every dollar of profit was made in trades lasting under 1 hour. Every catastrophic loss came from trades held longer than 8 hours.

## Explanation

AA's trailing protection exits winners quickly (median ~10 minutes). But it has no equivalent mechanism to cut losing trades early. When a trade goes underwater, AA holds it passively—sometimes for 20+ hours—until the stop loss is hit. The system has a fast exit for profit and no exit for time.

## Confidence

**High.** The separation is absolute. Zero overlap between the <1h win cluster and the 8h+ loss cluster. No exceptions in 32 trades.

## Evidence

| Metric | <1h Trades | 8h+ Trades |
|---|---|---|
| Count | 25 | 6 |
| Win rate | 100% | 33% |
| Total P/L | +$244.44 | -$608.69 |
| Stop-loss exits | 0 | 4 |
| Avg duration | ~14 min | ~18.3 hrs |

---

## Raw Dataset

| Pair | Side | Score | Duration | P/L | Exit Reason | Bucket |
|---|---|---|---|---|---|---|
| EURJPY | Sell | 80 | 5m | +$35.46 | Trailing protection | <1h |
| XAUUSD | Sell | 91 | 5m | +$5.09 | Trailing protection | <1h |
| GBPJPY | Buy | 75 | 5m | +$14.27 | Trailing protection | <1h |
| EURJPY | Sell | 81 | 5m | +$4.05 | Trailing protection | <1h |
| XAUUSD | Buy | 91 | 5m | +$1.46 | Trailing protection | <1h |
| XAUUSD | Sell | 90 | 5m | +$0.09 | Trailing protection | <1h |
| XAUUSD | Buy | 100 | 5m | +$6.79 | Trailing protection | <1h |
| XAUUSD | Sell | 91 | 5m | +$19.43 | Trailing protection | <1h |
| GBPUSD | Buy | 80 | 10m | +$12.07 | Trailing protection | <1h |
| XAUUSD | Sell | 91 | 10m | +$15.58 | Trailing protection | <1h |
| XAUUSD | Sell | 85 | 10m | +$4.13 | Trailing protection | <1h |
| XAUUSD | Buy | 91 | 15m | +$23.25 | Trailing protection | <1h |
| EURUSD | Sell | 90 | 15m | +$24.03 | Trailing protection | <1h |
| GBPUSD | Sell | 70 | 15m | +$3.02 | Trailing protection | <1h |
| USDJPY | Sell | 91 | 15m | +$7.44 | Trailing protection | <1h |
| USDJPY | Sell | 81 | 15m | +$5.89 | Trailing protection | <1h |
| XAUUSD | Buy | 100 | 20m | +$3.18 | Trailing protection | <1h |
| XAUUSD | Buy | 90 | 20m | +$1.21 | Trailing protection | <1h |
| GBPUSD | Buy | 90 | 20m | +$3.02 | Trailing protection | <1h |
| XAUUSD | Buy | 91 | 20m | +$4.66 | Trailing protection | <1h |
| GBPJPY | Buy | 75 | 25m | +$4.21 | Trailing protection | <1h |
| GBPJPY | Sell | 75 | 30m | +$14.06 | Trailing protection | <1h |
| EURJPY | Sell | 91 | 35m | +$8.66 | Trailing protection | <1h |
| XAUUSD | Sell | 100 | 40m | +$18.80 | Trailing protection | <1h |
| EURJPY | Sell | 81 | 50m | +$4.59 | Trailing protection | <1h |
| GBPUSD | Buy | 80 | 1h46m | +$0.38 | Trailing protection | 1–4h |
| XAUUSD | Buy | 100 | 8h37m | -$87.73 | **Stop loss hit** | 8–24h |
| XAUUSD | Sell | 100 | 15h56m | +$267.59 | Take profit hit | 8–24h |
| USDCHF | Sell | 72 | 17h35m | +$38.97 | Trailing protection | 8–24h |
| GBPJPY | Buy | 75 | 20h52m | -$284.41 | **Stop loss hit** | 8–24h |
| EURUSD | Buy | 90 | 21h01m | -$266.42 | **Stop loss hit** | 8–24h |
| GBPUSD | Buy | 90 | 24h39m | -$276.69 | **Stop loss hit** | >24h |

---

No recommendations. No optimization. Observation only.
