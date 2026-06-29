# Alpha-Decay Data Expansion: Ari Entry Path Simulation

Generated at: 2026-06-29T13:36:04.639500+00:00
Output CSV: `/Users/kennylee/Documents/Saxo/AA_Research/ledgers/alpha_decay/ari_entry_paths_xauusd_gc_f_730d_60m_2026_06_29_133604.csv`

## Scope

Read-only research simulation. No Ari execution, strategy, threshold, risk, portfolio, or runner behavior was modified.

## Market Data

- Proxy ticker: `GC=F`
- Symbol modeled: `XAUUSD`
- Period requested: `730d`
- Interval: `60m`
- Bars loaded: 13786
- First bar: 2024-02-05T05:00:00+00:00
- Last bar: 2026-06-29T13:00:00+00:00

## Ari Entry Logic Approximation

- Minimum ticks/bars for signal: 5
- XAUUSD momentum threshold: 0.0036
- Training sample mode: True
- Required admission score: 45
- Proxy spread pct: 0.0002

## Dataset Summary

- Simulated valid entries: 4143
- Buy entries: 2309
- Sell entries: 1834
- Average 240m MFE: 18.7016 points
- Average 240m MAE: -17.7483 points
- Average 240m forward return: 0.9505 points
- Meets 5,000-entry target: no

## Forward Return Quantiles

| horizon | mean | p10 | p25 | median | p75 | p90 |
| --- | --- | --- | --- | --- | --- | --- |
| 60m | 0.0664 | -12.6078 | -5.0111 | -0.3499 | 4.7775 | 12.2665 |
| 120m | 0.5111 | -16.7436 | -7.0188 | -0.1717 | 6.9306 | 18.1768 |
| 180m | 0.7959 | -20.0055 | -8.3934 | -0.1655 | 8.5962 | 22.5816 |
| 240m | 0.9505 | -23.9087 | -9.6498 | -0.1014 | 10.4297 | 26.0303 |

## Data Integrity Notes

- This uses `60m` GC=F futures bars. Yahoo does not provide 12-24 months of 1-minute/5-minute futures data.
- This is not a tick-accurate live execution backtest.
- Entry logic is Ari's current momentum/admission logic projected onto `60m` OHLC close windows.
- Forward path MFE/MAE are measured from OHLC highs/lows after the simulated entry.
- Dataset is suitable for alpha-decay shape research, not broker-execution claims.