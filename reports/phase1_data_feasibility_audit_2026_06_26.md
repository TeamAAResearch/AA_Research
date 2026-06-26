# Phase 1 Data Feasibility Audit

**Date:** 2026-06-26
**Classification:** Engineering Feasibility / Read-Only Saxo API Test
**Author:** Codex
**Stage:** Stage 2 Architectural Reconstruction, Phase 1

## 1. Objective

Prove whether Saxo SIM can provide the daily candle data required for a future Dynamic ATR Engine.

This phase is read-only. It does not change Ari's live runner, strategy, thresholds, risk, portfolio logic, or database schema.

## 2. Script Created

Created:

```text
scripts/fetch_saxo_d1_candles.py
```

Purpose:

- load current `.env`
- read active `SAXO_WATCHLIST`
- fetch 14 daily candles for each active symbol
- calculate ATR as a percentage of latest close
- print a safe report without exposing secrets

Saxo endpoint verified:

```text
/chart/v3/charts
```

Required parameters:

```text
AssetType
Uic
Horizon=1440
Count=14
```

## 3. Result

The feasibility test succeeded.

```text
11/11 active symbols returned D1 candles.
```

## 4. ATR Output

| Symbol | Asset Type | UIC | Candles | First Candle | Latest Candle | ATR % |
|---|---|---:|---:|---|---|---:|
| EURUSD | FxSpot | 21 | 14 | 2026-06-09 | 2026-06-26 | 0.5374% |
| GBPUSD | FxSpot | 31 | 14 | 2026-06-09 | 2026-06-26 | 0.6476% |
| AUDUSD | FxSpot | 4 | 14 | 2026-06-09 | 2026-06-26 | 0.7423% |
| NZDUSD | FxSpot | 37 | 14 | 2026-06-09 | 2026-06-26 | 0.8500% |
| USDJPY | FxSpot | 42 | 14 | 2026-06-09 | 2026-06-26 | 0.3657% |
| USDCHF | FxSpot | 39 | 14 | 2026-06-09 | 2026-06-26 | 0.6179% |
| USDCAD | FxSpot | 38 | 14 | 2026-06-09 | 2026-06-26 | 0.4194% |
| EURJPY | FxSpot | 18 | 14 | 2026-06-09 | 2026-06-26 | 0.4741% |
| GBPJPY | FxSpot | 26 | 14 | 2026-06-09 | 2026-06-26 | 0.6177% |
| XAUUSD | FxSpot | 8176 | 14 | 2026-06-09 | 2026-06-26 | 2.9399% |
| XAGUSD | FxSpot | 8177 | 14 | 2026-06-09 | 2026-06-26 | 6.4370% |

## 5. Interpretation

Saxo SIM supports the Dynamic ATR Engine's daily-candle requirement for the current active FX/Metals watchlist.

This confirms Phase 1's first feasibility question:

```text
Can Saxo provide 14-day D1 candles for active Ari symbols?
Answer: Yes.
```

## 6. Notes

The first attempted endpoint, `/chart/v1/charts`, returned 404. The supported endpoint is `/chart/v3/charts`.

The script is standalone and can be rerun manually:

```bash
cd /Users/kennylee/Documents/Saxo
python3 scripts/fetch_saxo_d1_candles.py --days 14
```

## 7. Remaining Phase 1 Work

Still pending:

- prototype offline MAE back-calculator using historical 1-minute OHLC data
- verify Saxo candle access for the 1-minute horizon and held-trade windows
- decide whether Phase 2 dual-ledger columns should be added only after offline MAE proof

