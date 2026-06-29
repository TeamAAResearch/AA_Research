# Time-Exit Simulation Study

Generated at: 2026-06-29T13:01:15.943087+00:00
Input: `AA_Research/ledgers/human_benchmark/forensic_matcher_2026_06_29_124625.csv`
Market proxy: `GC=F`
Interval: `5m`
Thresholds: `[60, 120, 180, 240]` minutes
CSV output: `/Users/kennylee/Documents/Saxo/AA_Research/ledgers/human_benchmark/time_exit_simulation_2026_06_29_130115.csv`

## Read-Only Scope

This study simulates forced time exits on matched human trades. It does not modify Ari, strategy, thresholds, risk, portfolio rules, or execution logic.

## Performance Comparison

| scenario | trades | net_pnl | delta_vs_control | win_rate | average_win | average_loss | payoff_ratio | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Control | 109 | 857.26 | 0.0 | 37.6% | 136.0 | -69.39 | 1.96 | 1.18 |
| T60 | 109 | -3050.26 | -3907.52 | 28.4% | 84.32 | -72.62 | 1.16 | 0.46 |
| T120 | 109 | -2326.61 | -3183.87 | 33.0% | 83.86 | -73.23 | 1.15 | 0.56 |
| T180 | 109 | -2237.35 | -3094.61 | 33.9% | 85.65 | -75.09 | 1.14 | 0.59 |
| T240 | 109 | -2173.31 | -3030.57 | 33.0% | 99.29 | -78.73 | 1.26 | 0.62 |

## Forced Exit Counts

| scenario | forced_exit | unchanged | fallback_actual |
| --- | --- | --- | --- |
| T120 | 22 | 87 | 0 |
| T180 | 20 | 89 | 0 |
| T240 | 17 | 92 | 0 |
| T60 | 30 | 79 | 0 |

## Research Interpretation

- T60 underperformed the human control by -3907.52, supporting the hypothesis that a 60-minute forced exit can suppress winner maturation.
- Best simulated/control scenario by net PnL: Control with net PnL 857.26.
- Treat this as research evidence only until repeated on Ari's own matched trades.

## Caveats

- Uses GC=F futures as a path proxy for XAUUSD spot.
- Uses matched forensic trades with confidence > 0 only.
- PnL-per-point is inferred from each human trade's actual PnL and price movement.
- This is a simulation artifact, not approval to change Ari's live/paper execution logic.