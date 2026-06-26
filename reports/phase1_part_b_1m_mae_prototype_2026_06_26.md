# Phase 1 Part B: Saxo 1-Minute MAE Prototype

Date: 2026-06-26

## Observation

Saxo SIM successfully returned 1-minute candles through the chart endpoint for recent Ari paper-trade reconstruction.

Prototype output:

- Script: `scripts/prototype_saxo_1m_mae.py`
- Output CSV: `AA_Research/ledgers/prototype_1m_mae_reconstruction.csv`
- Positions checked: 12
- Positions reconstructed: 8
- Stop crossings detected: 1
- Target crossings detected: 0
- Source database modified: No
- Saxo orders placed: No

## Research / Baseline

The prototype uses:

- `trading_system.sqlite3`
- `challenger_positions`
- Saxo SIM `/chart/v3/charts`
- `Horizon=1`
- `Count=1500`

The script reconstructs each recent position's 1-minute path and estimates:

- MFE
- MAE
- whether stop loss crossed inside the 1-minute candle path
- whether take profit crossed inside the 1-minute candle path
- first stop-crossing timestamp
- first target-crossing timestamp

## Logic Of Decisions

The purpose of Part B is not to change Ari's exit logic.

The purpose is to prove whether the data needed for a future soft-stop slippage audit exists.

The prototype stays offline and read-only because the correct sequence is:

1. Prove Saxo can serve the required candles.
2. Reconstruct historical candle paths outside the trading loop.
3. Quantify slippage or missed exits.
4. Only then decide whether dual-ledger storage is justified.

This protects the current live-data + paper-trading loop from premature engine changes.

## Engineering Execution

Created standalone script:

`scripts/prototype_saxo_1m_mae.py`

The script:

- loads the existing `.env`
- reads recent challenger positions from SQLite
- fetches 1-minute Saxo candles by symbol
- filters candles to each position's open/close window
- calculates reconstructed MFE and MAE
- detects stop/target crossings
- writes a research CSV

No source trading data is changed.

## Prototype Result

Recent positions reconstructed successfully.

Representative rows:

| Position | Symbol | Side | Status | Candles | Reconstructed MFE | Reconstructed MAE | Diagnostic |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| 194 | NZDUSD | Buy | Open | 43 | -4.65 | -15.71 | no stop/target crossing |
| 193 | EURUSD | Buy | Open | 44 | -1.87 | -12.41 | no stop/target crossing |
| 192 | EURJPY | Buy | Closed | 5 | 2.31 | -2.45 | no stop/target crossing |
| 190 | XAUUSD | Sell | Closed | 7 | 17.65 | -2.00 | no stop/target crossing |
| 187 | XAUUSD | Sell | Closed | 746 | 47.26 | -263.60 | stop crossed inside 1-minute path |

## Important Limitation

Four older positions were not reconstructed because no 1-minute candles overlapped the position window returned by Saxo.

This means the 1-minute approach is feasible, but reconstruction appears time-sensitive. If the chart endpoint only returns a bounded recent candle window, the future dual-ledger job must run promptly or prove that Saxo supports historical time-window parameters for older intraday candles.

This is an engineering constraint, not a trading conclusion.

## Deployment

No deployment was performed.

No runner restart was required.

No trading behavior changed.

## Roadmap / Open Questions

Open questions before Phase 2:

1. What is the maximum reliable 1-minute candle lookback returned by Saxo for each asset class?
2. Does `/chart/v3/charts` support explicit historical `Time`, `From`, or equivalent window parameters in this SIM account?
3. Should the future MAE process run as a daily research job so older trades do not fall outside the retrievable 1-minute window?
4. Should Phase 2 store reconstructed MAE in a separate research table before adding any canonical trade fields?

## Next Step

Phase 1 Part B is functional.

Recommended next engineering step:

Run a focused Saxo chart parameter audit to determine whether older 1-minute windows can be requested directly. If not, Phase 2 should use a prompt scheduled reconstruction job rather than relying on delayed backfills.
