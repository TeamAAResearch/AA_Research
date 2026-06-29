# Human Trading Benchmark

Generated at: 2026-06-29T12:14:45.590027+00:00
Source file: `AA_Research/ledgers/kenny_xauusd_june.xlsx`

## Scope

This report is read-only research output. It does not modify Ari's execution engine, strategy, risk, thresholds, or portfolio logic.

## Full Ledger Benchmark

| Metric | Value |
|---|---:|
| Trades | 214 |
| Wins | 83 |
| Losses | 131 |
| Flats | 0 |
| Win Rate | 38.8% |
| Net P/L | 2,759.50 |
| Gross Profit | 14,998.77 |
| Gross Loss | -12,239.27 |
| Average Win | 180.71 |
| Average Loss | -93.43 |
| Payoff Ratio | 1.93 |
| Profit Factor | 1.23 |
| Directional Bias | Buy (1,846.15) |

## XAUUSD Benchmark

| Metric | Value |
|---|---:|
| Trades | 145 |
| Wins | 53 |
| Losses | 92 |
| Flats | 0 |
| Win Rate | 36.6% |
| Net P/L | -278.52 |
| Gross Profit | 7,250.09 |
| Gross Loss | -7,528.61 |
| Average Win | 136.79 |
| Average Loss | -81.83 |
| Payoff Ratio | 1.67 |
| Profit Factor | 0.96 |
| Directional Bias | Sell (1,424.46) |

## Directional Bias - Full Ledger

| Side | Trades | Win Rate | Net P/L | Avg Win | Avg Loss | Payoff Ratio |
|---|---:|---:|---:|---:|---:|---:|
| Buy | 92 | 40.2% | 1,846.15 | 213.44 | -110.02 | 1.94 |
| Sell | 122 | 37.7% | 913.35 | 154.38 | -81.42 | 1.90 |

## Directional Bias - XAUUSD

| Side | Trades | Win Rate | Net P/L | Avg Win | Avg Loss | Payoff Ratio |
|---|---:|---:|---:|---:|---:|---:|
| Sell | 83 | 39.8% | 1,424.46 | 154.50 | -73.48 | 2.10 |
| Buy | 62 | 32.3% | -1,702.98 | 107.57 | -91.77 | 1.17 |

## Temporal Data Limitation

The Saxo export records trade dates at date-level precision in this file. Exact intraday holding time, MFE, and MAE cannot be reconstructed reliably from this export alone without an independent tick/path match.

## Research Use

- Compare Kenny's payoff ratio against Ari's realized payoff ratio.
- Compare Kenny's XAUUSD side bias against Ari's XAUUSD side bias.
- Treat the benchmark as evidence for discussion, not as an automatic parameter update.
