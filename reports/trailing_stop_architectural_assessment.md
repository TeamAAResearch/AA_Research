# Trailing Stop Architectural Assessment

**Classification:** Architectural Assessment Report
**Owner:** Codex
**Date:** 2026-06-25
**Status:** Internal GM Review Required

---

## Evidence

### Source location

The trailing protection exit is defined in the Python codebase, not in Ari's prompt, not in Saxo OpenAPI, and not in a hidden module.

Exact source:

- `saxo_trader/challenger.py`
- Function: `_day_trader_exit_reason`
- Lines reviewed: 300-319

Relevant logic:

```python
quick_profit_pct = max(config.take_profit_pct * 0.35, 0.0015)
trailing_protect_pct = max(config.stop_loss_pct * 0.3, 0.001)
if move_pct >= quick_profit_pct:
    return "AA day-trader quick profit exit: intraday target captured"
if pnl > 0 and move_pct <= trailing_protect_pct:
    return "AA day-trader trailing protection exit: protect open profit"
```

The close reason string is generated directly at:

```python
return "AA day-trader trailing protection exit: protect open profit"
```

### How it executes

Open positions are managed in:

- `saxo_trader/challenger.py`
- Function: `_manage_open_positions`
- Lines reviewed: 219-281

The sequence is:

1. Fetch current quote for each open challenger position.
2. Check hard stop-loss and hard take-profit.
3. If neither hard bracket is hit, call `_day_trader_exit_reason`.
4. If `_day_trader_exit_reason` returns a reason, close the paper position at current execution price.
5. Record the close reason into SQLite through `store.close_challenger_position`.

### Current parameter source

Config is loaded from:

- `saxo_trader/config.py`
- `.env`

Current relevant `.env` values:

- `CHALLENGER_STOP_LOSS_PCT=0.005`
- `CHALLENGER_TAKE_PROFIT_PCT=0.01`

Therefore:

- `quick_profit_pct = max(0.01 * 0.35, 0.0015) = 0.0035`
- `trailing_protect_pct = max(0.005 * 0.3, 0.001) = 0.0015`

The trailing protection threshold is therefore approximately a 0.15% favorable move threshold.

### Observed post-regime exit outcomes

For `challenger_trades` with `id >= 136`:

| Close reason | Count | Total P/L | Avg P/L | Avg MFE | Avg MAE |
|---|---:|---:|---:|---:|---:|
| Trailing protection | 44 | +436.10 | +9.91 | +14.87 | -20.53 |
| Paper stop loss hit | 6 | -806.60 | -134.43 | -10.22 | -134.43 |
| Quick profit exit | 1 | +65.65 | +65.65 | +66.65 | +65.65 |

The trailing protection mechanism is the dominant exit path by count.

---

## Interpretation

I do not fully agree with the statement that the trailing stop is the only root cause.

The evidence supports a more precise architectural interpretation:

The current day-trading regime has a **coupled expectancy defect**:

1. Trailing protection closes most winning trades quickly, producing an average realized win around +$9.91 in the post-regime cohort.
2. Hard stop-loss exits remain much larger, producing an average loss around -$134.43.
3. The resulting win/loss asymmetry creates negative skew.

The trailing protection is therefore a major contributor to the profit cap, but the unprofitability is caused by the interaction between:

- small realized wins,
- large stop-loss exits,
- and no intermediate loss-management exit that preserves win rate.

The strict -$20 simulation supports this interpretation. It compressed tail losses, but still did not make the cohort profitable because it converted 16 historical winners into synthetic losses.

So the architectural problem is not simply:

> trailing stop bad

It is:

> the exit stack has no calibrated middle layer between small-profit protection and large hard-stop loss.

---

## Hypothesis candidates

1. **Profit Cap Hypothesis:** The current trailing-protection threshold is too aggressive for the observed Gold scalping regime and prevents enough larger winners from offsetting stop-loss events.
2. **Exit Stack Gap Hypothesis:** The system needs an intermediate exit-management layer that cuts deteriorating trades before hard stop without converting too many recoverable winners into losses.
3. **Coupled Skew Hypothesis:** Neither widening the trailing protection nor tightening the stop-loss can be judged independently; the profitable solution, if one exists, must tune the full exit stack together.

These are hypothesis candidates only.

They do not authorize implementation.

---

## Contradiction tests

To contradict the Profit Cap Hypothesis:

- Show that increasing the trailing-protection threshold would not materially improve realized P/L in replay.
- Show that most trades closed by trailing protection had already exhausted favorable movement before exit.

To contradict the Exit Stack Gap Hypothesis:

- Show that intermediate loss exits consistently reduce expectancy by converting too many future winners into losses.
- Show that large hard-stop losses are rare enough over larger samples that they do not dominate long-term expectancy.

To test the Coupled Skew Hypothesis:

- Run parameter-grid simulations across both profit protection and loss invalidation.
- Evaluate net P/L, win rate, average win, average loss, max loss, and number of winners converted into losses.
- Use tick-path reconstruction where possible rather than final MFE/MAE only.

---

## Open questions

1. Does trailing protection trigger after a trade has given back from a higher MFE, or does it trigger soon after a small favorable move?
2. Would widening trailing protection increase realized winners, or simply allow small winners to reverse into hard-stop losses?
3. Is the current high-frequency Gold scalping regime stable, or a temporary artifact of recent market conditions?
4. Should exit parameters be symbol-specific, especially for XAUUSD, rather than globally tied to `CHALLENGER_STOP_LOSS_PCT` and `CHALLENGER_TAKE_PROFIT_PCT`?

---

## Technical Steps Required If GM/Kenny Later Authorize A Controlled Rollout

No rollout is authorized by this memo.

If authorized later, the technical change points are:

1. Modify `_day_trader_exit_reason` in `saxo_trader/challenger.py`.
2. Decouple trailing protection from `config.stop_loss_pct`.
3. Add explicit config fields such as:
   - `CHALLENGER_TRAILING_PROTECT_PCT`
   - `CHALLENGER_QUICK_PROFIT_PCT`
   - optionally symbol-specific overrides for XAUUSD.
4. Add tests covering:
   - trailing protection disabled,
   - wider trailing threshold,
   - quick-profit priority,
   - hard stop priority,
   - no change to paper-only safety.
5. Run backtests before changing the live paper runner.
6. Use controlled rollout only after GM/Kenny authorization under the Finding Adoption Framework.

GM Review Required

