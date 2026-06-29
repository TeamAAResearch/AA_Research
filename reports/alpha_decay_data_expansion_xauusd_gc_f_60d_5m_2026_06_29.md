# Alpha-Decay Data Expansion: Ari Entry Path Simulation

Generated at: 2026-06-29T13:36:09.523889+00:00
Output CSV: `/Users/kennylee/Documents/Saxo/AA_Research/ledgers/alpha_decay/ari_entry_paths_xauusd_gc_f_60d_5m_2026_06_29_133609.csv`

## Scope

Read-only research simulation. No Ari execution, strategy, threshold, risk, portfolio, or runner behavior was modified.

## Market Data

- Proxy ticker: `GC=F`
- Symbol modeled: `XAUUSD`
- Period requested: `60d`
- Interval: `5m`
- Bars loaded: 13330
- First bar: 2026-04-19T22:10:00+00:00
- Last bar: 2026-06-29T13:25:00+00:00

## Ari Entry Logic Approximation

- Minimum ticks/bars for signal: 5
- XAUUSD momentum threshold: 0.0036
- Training sample mode: True
- Required admission score: 45
- Proxy spread pct: 0.0002

## Dataset Summary

- Simulated valid entries: 631
- Buy entries: 320
- Sell entries: 311
- Average 240m MFE: 24.9366 points
- Average 240m MAE: -27.2560 points
- Average 240m forward return: -3.1558 points
- Meets 5,000-entry target: no

## Forward Return Quantiles

| horizon | mean | p10 | p25 | median | p75 | p90 |
| --- | --- | --- | --- | --- | --- | --- |
| 60m | -2.3493 | -26.7034 | -13.0804 | -2.2062 | 7.6391 | 20.4774 |
| 120m | -1.5789 | -33.5714 | -15.5343 | -2.1328 | 12.0912 | 26.8695 |
| 180m | -1.6872 | -35.5394 | -18.6552 | -1.9278 | 13.8788 | 32.6382 |
| 240m | -3.1558 | -41.1255 | -21.5625 | -5.0534 | 14.7033 | 34.3384 |

## Data Integrity Notes

- This uses `5m` GC=F futures bars. Yahoo does not provide 12-24 months of 1-minute/5-minute futures data.
- This is not a tick-accurate live execution backtest.
- Entry logic is Ari's current momentum/admission logic projected onto `5m` OHLC close windows.
- Forward path MFE/MAE are measured from OHLC highs/lows after the simulated entry.
- Dataset is suitable for alpha-decay shape research, not broker-execution claims.