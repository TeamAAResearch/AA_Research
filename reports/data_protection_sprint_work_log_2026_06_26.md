# Data Protection Sprint Work Log

**Date:** 2026-06-26
**Classification:** Engineering Execution / RFC
**Author:** Codex
**Audience:** GM, AG, Ari Team

## 1. Observation

Stage 1 Training Mode increased Ari's decision and entry velocity. The previous anomaly scanner burst limits were calibrated for slower production-style activity and could falsely classify high-frequency training probes as a runner meltdown.

The organization also needs a direct statistical view of training probes, independent of dashboard/team narrative layers.

Finally, Incident 187 showed that soft paper stops can slip badly when the runner or Saxo data feed is unavailable.

## 2. Engineering Execution

Implemented:

- `MAX_OPENED_PER_MINUTE` widened from `3` to `10`.
- `MAX_CLOSED_PER_MINUTE` widened from `5` to `10`.
- Added standalone read-only analytics script: `scripts/analyze_training_probes.py`.
- Updated anomaly scanner tests to validate burst detection at the new threshold.

The analytics script reads `trading_system.sqlite3` and reports:

- closed training-probe count
- total P/L
- win rate
- profit factor
- expectancy per trade
- average win
- average loss
- average hold time
- symbol/side breakdown

Manual command:

```bash
cd /Users/kennylee/Documents/Saxo
python3 scripts/analyze_training_probes.py
```

## 3. RFC: Soft-Stop Slippage Risk

### Problem

Ari's stops are soft paper stops checked by the Python runner. At a 60-second polling interval, the recorded stop exit may lag the first moment price crossed the stop.

During API outages, the problem becomes larger: the runner cannot observe price at all, so paper stop execution waits until data returns.

### Option A: Broker-Side Hard Stops

Use Saxo OpenAPI order placement to attach stop-loss orders at the broker.

**Pros**

- Real stop protection during local runner failure.
- Better approximation of real trading survivability.

**Cons**

- Moves beyond current paper-only safety boundary.
- Requires live order-routing controls, cancellation logic, reconciliation, and explicit GM/Kenny authorization.
- Not suitable while the system is still in research-only paper mode.

### Option B: MAE Back-Calculator

Keep paper mode, but reconstruct the likely first stop-crossing point using higher-frequency stored ticks or Saxo candle history.

**Pros**

- Preserves paper-only mode.
- Gives better research truth on whether the stop would have been hit earlier.
- Can quantify stop slippage caused by 60-second polling.

**Cons**

- Requires reliable historical tick/candle availability.
- Still counterfactual; not a real protection mechanism.
- Quality depends on data granularity.

### Option C: Hybrid Research Path

For the current phase, use Option B first:

1. Add a stop-crossing reconstruction report for closed paper trades.
2. Measure observed exit price versus earliest reconstructed stop-crossing price.
3. Quantify slippage by symbol, side, volatility regime, and outage state.
4. Only after evidence review, decide whether broker-side stops are required for any future live-money phase.

### RFC Position

Do not implement broker-side hard stops during the current paper/simulation phase.

The next safest engineering step is a read-only MAE/stop-crossing back-calculator that improves research accuracy without changing Ari's trading behavior or touching live Saxo orders.

## 4. Governance Boundary

This sprint does not authorize:

- live Saxo order placement
- real-money trading
- stop-loss policy changes
- strategy changes
- threshold changes
- portfolio changes

