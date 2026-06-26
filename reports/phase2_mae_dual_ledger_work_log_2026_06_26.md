# Phase 2 MAE Dual-Ledger Work Log

Date: 2026-06-26

## Observation

Phase 2 implementation is complete in code and schema.

The live database has been migrated with the new dual-ledger columns:

- `mae_exit_price`
- `mae_pnl`
- `loop_slippage_cost`

These fields exist in:

- `challenger_positions`
- `challenger_trades`

## Research / Baseline

Phase 1B proved that Saxo SIM can serve 1-minute candles for recent trade-path reconstruction.

The engineering constraint remains:

Older 1-minute candles may fall outside the returned Saxo chart window, so reconstruction must occur promptly near trade closure.

## Logic Of Decisions

The dual-ledger design preserves Ari's original paper-trading ledger.

Original fields remain untouched:

- `exit`
- `closed_at`
- `pnl`

The new MAE fields create a second research ledger that answers:

"What was the worst 1-minute candle-path adverse P/L during the trade?"

This avoids changing Ari's trading behavior while improving research visibility.

## Engineering Execution

Implemented:

- schema migration for dual-ledger fields
- pure MAE reconstruction module
- Saxo chart-candle read method
- close-time hook in the challenger runner path
- focused unit tests for reconstruction, schema, and close-cycle dual-ledger writing
- AG 360-risk review controls:
  - MAE reconstruction is queued after the paper close instead of blocking the main cycle
  - default worker waits 65 seconds before candle fetch so the final Saxo 1-minute candle can settle
  - fetch failures are isolated in `try/except` and never reverse or delay the original close
  - candle count is bounded to the trade duration plus a small buffer instead of always requesting 1500 candles

Files changed:

- `saxo_trader/storage.py`
- `saxo_trader/mae_reconstruction.py`
- `saxo_trader/saxo_client.py`
- `saxo_trader/challenger.py`
- `saxo_trader/challenger_runner.py`
- `tests/test_mae_reconstruction.py`
- `tests/test_storage.py`
- `tests/test_challenger.py`

Backup created before live migration:

- `backups/hourly/20260626T072716Z`

## Deployment

Live SQLite schema migration was applied and verified.

Runner restart was attempted but blocked by local sandbox permissions:

- safe stop helper refused because process inspection was unavailable
- direct signal attempt was denied by the sandbox

Current runner remains healthy but is still the old process.

Manual restart is required before the new close-time MAE hook is active in the live runner.

Important: the hook is now non-blocking. The paper close writes immediately; the MAE dual-ledger update follows asynchronously when candle data is available.

## Verification

Test suite:

- `130 passed`
- `1 warning`

Post-360 focused test suite:

- `28 passed`
- `1 warning`

Live database column verification:

- `challenger_positions`: dual-ledger columns present
- `challenger_trades`: dual-ledger columns present

Current position counts at verification:

- Closed legacy_unknown: 103
- Closed standard_signal: 86
- Closed training_probe: 1
- Open standard_signal: 1
- Open training_probe: 3

## Next Step

Restart Ari from Kenny's Terminal so the new code is loaded:

1. Stop the current AA Challenger runner.
2. Start the 60-second background runner again.
3. Confirm status heartbeat is fresh.
4. Wait for the next closed trade.
5. Verify the closed row has `mae_exit_price`, `mae_pnl`, and `loop_slippage_cost`.
