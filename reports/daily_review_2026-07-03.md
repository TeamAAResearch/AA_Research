# Ari Daily Trading Review (2026-07-03)

**Window:** 2026-07-02 01:40:06 UTC to 2026-07-03 01:40:06 UTC  
**Anchor:** latest ledger trade timestamp, `2026-07-03 01:40:06`  
**Database:** `/Users/kennylee/.saxo_data/trading_system.sqlite3`

## 1. High-Level Metrics
| Metric             | Value |
|:-------------------|:------|
| Total Trades       | 154 positions in window |
| Closed Trades      | 142 |
| Open Positions     | 12 opened in window, 19 total open including older probes |
| Realized PnL       | -473.71 |
| Win Rate           | 28.9% |
| Avg Win            | +5.20 |
| Avg Loss           | -6.80 |
| Profit Factor      | 0.31 |
| Largest Winner     | +20.66 |
| Largest Loser      | -61.46 |

Population note:

| Sample Type | Closed | PnL | Win Rate | Profit Factor |
|:------------|:-------|:----|:---------|:--------------|
| `vc_shadow_validation` | 91 | -185.87 | 29.7% | 0.48 |
| `legacy_unknown` | 51 | -287.84 | 27.5% | 0.13 |

## 2. Exit Mechanism Breakdown
| Exit Reason                  | Count | % of Closed |
|:-----------------------------|:------|:------------|
| Alpha-decay low-MFE flatten  | 48 | 33.8% |
| Alpha-decay TTL flatten      | 13 | 9.2% |
| Momentum exhaustion / ratchet | 0 | 0.0% |
| Micro-stop                   | 0 | 0.0% |
| Paper stop loss              | 5 | 3.5% |
| Other                        | 76 | 53.5% |

Top raw exit reasons:

| Exit Reason | Count |
|:------------|:------|
| Clara early exit near stop | 21 |
| `stall_velocity_exit_120m (MFE only 0.00 ATR)` | 17 |
| `alpha_decay_ttl_flatten_240m` | 13 |
| `alpha_decay_low_mfe_flatten`, threshold 0.75, MFE 0.00 | 6 |
| Paper stop loss hit | 5 |

## 3. Intraday Performance (4-Hour Blocks)
| Time Block (UTC) | Trades | Win Rate | Block PnL | Cumulative PnL |
|:-----------------|:-------|:---------|:----------|:---------------|
| 2026-07-02 00:00 | 17 | 11.8% | -54.49 | -54.49 |
| 2026-07-02 04:00 | 22 | 31.8% | -42.89 | -97.38 |
| 2026-07-02 08:00 | 21 | 71.4% | +111.97 | +14.59 |
| 2026-07-02 12:00 | 25 | 0.0% | -364.37 | -349.78 |
| 2026-07-02 16:00 | 25 | 32.0% | -96.33 | -446.11 |
| 2026-07-02 20:00 | 23 | 21.7% | -34.52 | -480.63 |
| 2026-07-03 00:00 | 9 | 44.4% | +6.92 | -473.71 |

## 4. MFE/MAE Analysis
| Metric                          | Value |
|:--------------------------------|:------|
| Avg MFE (winners)               | +8.59 |
| Avg Realized PnL (winners)      | +5.20 |
| Avg Profit Left on Table        | +3.39 |
| MFE Capture Ratio               | 60.6% |
| Avg MAE (losers)                | -8.19 |

Duration:

| Duration Bucket | Trades | PnL | Win Rate |
|:----------------|:-------|:----|:---------|
| 0-10m | 7 | -21.75 | 0.0% |
| 10-60m | 4 | -53.02 | 0.0% |
| 60-120m | 11 | -71.99 | 0.0% |
| 120-180m | 105 | -355.88 | 30.5% |
| 180-240m | 2 | -5.90 | 0.0% |
| 240m+ | 13 | +34.83 | 69.2% |

## 5. VC Filter Activity
| Metric                 | Value |
|:-----------------------|:------|
| Signals blocked        | 911 |
| Order-flow veto against Sell | 106 |
| Order-flow veto against Buy | 102 |
| Admission score 40 below 50 | 76 |
| Admission score 40 below 50 plus daily downtrend | 66 |

Other frequent blocks were dynamic spread caps across wide or synthetic FX pairs.

## 6. Symbol, Side, and Agent Breakdown
| Slice | Trades | PnL | Win Rate | Profit Factor |
|:------|:-------|:----|:---------|:--------------|
| FX | 137 | -467.92 | 27.7% | 0.30 |
| Metals | 5 | -5.79 | 60.0% | 0.59 |
| Buy | 90 | -245.10 | 28.9% | 0.35 |
| Sell | 52 | -228.61 | 28.8% | 0.27 |
| ARI | 91 | -185.87 | 29.7% | 0.48 |
| PLUGIN / legacy | 51 | -287.84 | 27.5% | 0.13 |

Worst symbols:

| Symbol | Trades | PnL | Win Rate |
|:-------|:-------|:----|:---------|
| AUDUSD | 11 | -74.16 | 9.1% |
| USDCHF | 9 | -57.32 | 44.4% |
| USDAUD | 10 | -51.75 | 30.0% |
| EURUSD | 10 | -46.90 | 30.0% |
| USDCAD | 10 | -44.01 | 20.0% |
| NZDUSD | 4 | -39.97 | 25.0% |

Best symbols:

| Symbol | Trades | PnL | Win Rate |
|:-------|:-------|:----|:---------|
| GBPEUR | 6 | +11.93 | 50.0% |
| GBPAUD | 4 | +3.23 | 25.0% |
| JPYEUR | 1 | +2.76 | 100.0% |

## 7. Comparison to Baseline
Official baseline from `AA_SHARED_RESEARCH_MEMO.md`:

| Baseline Metric | Official Baseline | Last 24h Actual |
|:----------------|:------------------|:----------------|
| Net PnL | +4605.38 | -473.71 |
| Win Rate | 61.9% | 28.9% |
| Avg Win | +192.14 | +5.20 |
| Avg Loss | -24.40 | -6.80 |
| Expectancy / Trade | +109.65 | -3.34 |
| Sample Size | 42 high-conviction trades | 142 closed mixed ledger trades |

Scale is not directly comparable because the current ledger uses small paper sizing and includes mixed populations, but the direction is decisively below baseline.

## 8. Observations & Hypotheses
- Observation: Ari closed 142 trades for -473.71 over the 24-hour window, with 28.9% win rate and 0.31 profit factor.
- Observation: The worst damage came from the 2026-07-02 12:00 UTC block: 25 trades, 0 wins, -364.37 PnL.
- Observation: A profitable pocket existed at 2026-07-02 08:00 UTC: 21 trades, 71.4% win rate, +111.97 PnL.
- Observation: FX remains the main problem: 137 trades, -467.92 PnL, 27.7% win rate.
- Observation: AUDUSD, USDCHF, USDAUD, EURUSD, USDCAD, and NZDUSD account for the largest symbol losses.
- Observation: `legacy_unknown` / `PLUGIN` trades performed worse than ARI-tagged `vc_shadow_validation` trades.
- Observation: The latest runner cycles are blocking new entries due to portfolio heat above 5% and concentrated long USD exposure.
- Hypothesis: Ari's major failure mode is not a lack of exits; it is admitting too much FX exposure into low-follow-through or crowded USD regimes.
- Hypothesis: The 08:00 UTC profitable pocket may contain the offensive regime AG should study before implementing adversarial exploitation.
- Hypothesis: The 12:00 UTC block likely reflects portfolio/regime concentration failure rather than random single-trade noise.
- Emerging Finding: Duration alone is not the enemy. The 240m+ bucket was profitable, while 0-120m trades were all-loss buckets in this sample.
- Finding: This 24-hour sample is not behaving like the official high-conviction baseline and should remain in research/discovery mode.

## 9. Trading Recommendation
Prioritize offensive research, but do not expand live/sim execution blindly.

Next research steps:

1. Compare the winning 08:00 UTC block against the losing 12:00 UTC block by symbol, side, USD exposure, spread/ATR, and order-flow veto pressure.
2. Isolate `PLUGIN` / `legacy_unknown` trades from ARI `vc_shadow_validation` trades before judging Ari's core trader.
3. Study whether blocked order-flow vetoes during the 12:00 UTC loss block would have produced profitable opposite-side trades.
4. Treat AUDUSD, USDAUD, EURUSD, USDCAD, NZDUSD, and USDCHF as high-priority review symbols before allowing more offensive expansion.
5. Investigate whether portfolio heat and USD concentration should feed into earlier admission scoring, not only late-cycle blocking.
