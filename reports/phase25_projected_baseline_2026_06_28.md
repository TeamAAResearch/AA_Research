# Phase 25 Projected Baseline

Date achieved: 2026-06-28

Status: Research baseline / projected replay result.

This report records the mathematical baseline behind Ari's Phase 25 brain. It is not live realized P/L. It is the benchmark that future live paper-trading evidence should be compared against.

## Baseline Result

| Metric | Phase 25 Projection |
| --- | ---: |
| Sample size | 42 high-conviction trades |
| Universe represented | 11 currency/commodity instruments |
| Net P/L | $4,605.38 SGD |
| Expectancy per trade | $109.65 |
| Win rate | 61.9% |
| Average winning trade | $192.14 |
| Average losing trade | -$24.40 |
| Payoff ratio | 7.87x |

## Reproducible Proof

Canonical reproduction script:

`AA_Research/scripts/simulate_phase25_mae_optimization.py`

The script is read-only. It queries `trading_system.sqlite3`, reconstructs the 42-trade replay sample, and prints the stop-loss sweep that produced the Phase 25 baseline.

Command:

```bash
python3 AA_Research/scripts/simulate_phase25_mae_optimization.py
```

Expected key row:

```text
0.3 ATR  |     42 |   61.9% | $192.14 | $ -24.40 | $4605.38 | $   109.65
```

## Stop-Loss Sweep

| Stop loss | Trades | Win rate | Avg win | Avg loss | Net P/L | Expectancy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.3 ATR | 42 | 61.9% | $192.14 | -$24.40 | $4,605.38 | $109.65 |
| 0.4 ATR | 42 | 61.9% | $144.11 | -$21.58 | $3,401.53 | $80.99 |
| 0.5 ATR | 42 | 64.3% | $118.49 | -$19.22 | $2,911.07 | $69.31 |
| 0.6 ATR | 42 | 64.3% | $98.74 | -$18.01 | $2,395.89 | $57.04 |
| 0.7 ATR | 42 | 64.3% | $84.64 | -$16.79 | $2,033.33 | $48.41 |
| 0.8 ATR | 42 | 64.3% | $74.06 | -$15.94 | $1,760.42 | $41.91 |
| 1.0 ATR | 42 | 64.3% | $59.25 | -$14.75 | $1,378.33 | $32.82 |
| 1.2 ATR | 42 | 64.3% | $49.37 | -$13.61 | $1,128.94 | $26.88 |

## Model Assumptions

- Initial stop is swept from 0.3 ATR to 1.2 ATR.
- Position size is scaled inversely to stop distance so nominal risk remains $30 per trade.
- The 0.3 ATR stop therefore increases position size relative to the prior 0.5 ATR baseline.
- Pyramiding triggers at +1.0 ATR.
- Pyramiding size is 1.0x.
- After pyramiding, the original stop moves to breakeven plus 0.33 ATR.
- Trailing exit distance is fixed at 1.2 ATR.
- Time-decay exit triggers after 7,200 seconds.
- Session filter uses UTC hours 1, 2, 9, 10, 11, and 12.
- Static ATR constants are used to reproduce the approved sandbox result.

## Arithmetic Check

- Net P/L divided by trades: $4,605.38 / 42 = $109.65 expectancy.
- Win/loss count implied by 61.9%: 26 wins and 16 losses.
- 26 wins at $192.14 and 16 losses at -$24.40 approximates $4,605.38 after rounding.
- Payoff ratio: $192.14 / $24.40 = 7.87x.

## Interpretation

Observation:

The replay model shows the 0.3 ATR stop produces the highest projected expectancy in the sweep.

Explanation:

The 0.3 ATR stop barely reduces win rate versus 0.5 ATR, but it increases position size per unit of fixed risk. Combined with 1.0x pyramiding and a 1.2 ATR trailing exit, the payoff profile becomes strongly asymmetric.

Confidence:

Medium for mathematical reproduction. Low to medium for live-market durability until enough post-deployment paper trades close.

Evidence:

The baseline is reproducible from `AA_Research/scripts/simulate_phase25_mae_optimization.py` and matches the approved shared memo figures.

## Live Validation Standard

Future live paper-trading reviews should compare closed trades against:

- Expectancy near or above $109.65 per trade.
- Average win near or above $192.14.
- Average loss near or below -$24.40.
- Win rate near or above 61.9%.

If live losses exceed the model loss profile, investigate stop execution, slippage, spread, and soft-stop delay.

If live wins fall materially below the model win profile, investigate pyramiding, trailing exits, and whether winners are being choked before trend extension.
