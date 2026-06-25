# Tight Stop Simulation Results

**Classification:** Simulation Report
**Owner:** AG / Codex
**Date:** 2026-06-25
**Status:** Internal GM Review Required

---

## Evidence

- Source database: `/Users/kennylee/Documents/Saxo/trading_system.sqlite3`
- Source table: `challenger_trades`.
- Cohort: closed `standard_signal` trades with `id >= 136`.
- Trades reviewed: 51.
- Synthetic rule tested: if recorded MAE <= $-20.00, set synthetic P/L to $-20.00; otherwise keep actual realized P/L.
- Baseline P/L: -304.85.
- Synthetic P/L: -118.88.
- Net synthetic change: +185.97.
- Baseline win rate: 88.2%.
- Synthetic win rate: 56.9%.
- Trades where the synthetic stop triggered: 22.
- Previously winning trades converted to synthetic losses: 16.
- Baseline average loss: -134.43.
- Synthetic average loss: -20.00.
- Baseline losses at or below -$100: 4.

### Regime Summary

- XAUUSD trades: 40 of 51.
- XAUUSD baseline P/L: -151.58.
- XAUUSD synthetic P/L: -24.30.

### Trade-Level Simulation

| ID | Symbol | Side | Baseline P/L | MAE | MFE | Stop Triggered | Synthetic P/L | Delta | Baseline | Synthetic |
|---:|---|---|---:|---:|---:|---|---:|---:|---|---|
| 136 | XAUUSD | Sell | 24.90 | -0.96 | 29.17 | No | 24.90 | +0.00 | Win | Win |
| 137 | XAUUSD | Sell | 10.20 | -27.40 | 11.18 | Yes | -20.00 | -30.20 | Win | Loss |
| 138 | AUDUSD | Buy | -263.57 | -263.57 | -23.76 | Yes | -20.00 | +243.57 | Loss | Loss |
| 139 | XAUUSD | Sell | 9.19 | -39.06 | 10.16 | Yes | -20.00 | -29.19 | Win | Loss |
| 140 | XAUUSD | Sell | -98.59 | -98.59 | -8.85 | Yes | -20.00 | +78.59 | Loss | Loss |
| 141 | XAUUSD | Buy | 2.45 | -17.85 | 3.65 | No | 2.45 | +0.00 | Win | Win |
| 142 | XAUUSD | Buy | 13.68 | -1.20 | 14.67 | No | 13.68 | +0.00 | Win | Win |
| 143 | XAUUSD | Sell | 5.19 | -26.94 | 6.20 | Yes | -20.00 | -25.19 | Win | Loss |
| 144 | XAUUSD | Buy | -123.06 | -123.06 | -20.17 | Yes | -20.00 | +103.06 | Loss | Loss |
| 145 | GBPJPY | Sell | 53.97 | -88.70 | 75.32 | Yes | -20.00 | -73.97 | Win | Loss |
| 146 | GBPJPY | Sell | 0.24 | -8.23 | 8.46 | No | 0.24 | +0.00 | Win | Win |
| 147 | XAUUSD | Sell | 11.35 | -0.99 | 12.39 | No | 11.35 | +0.00 | Win | Win |
| 148 | XAUUSD | Sell | 5.49 | 5.49 | 6.46 | No | 5.49 | +0.00 | Win | Win |
| 149 | EURJPY | Sell | 8.18 | -28.50 | 12.95 | Yes | -20.00 | -28.18 | Win | Loss |
| 150 | XAUUSD | Sell | 16.29 | -0.04 | 17.28 | No | 16.29 | +0.00 | Win | Win |
| 151 | XAUUSD | Sell | 65.65 | 65.65 | 66.65 | No | 65.65 | +0.00 | Win | Win |
| 152 | XAUUSD | Sell | 10.84 | -8.02 | 12.07 | No | 10.84 | +0.00 | Win | Win |
| 153 | XAUUSD | Sell | -99.52 | -99.52 | -1.23 | Yes | -20.00 | +79.52 | Loss | Loss |
| 154 | EURJPY | Buy | 6.27 | -16.49 | 11.04 | No | 6.27 | +0.00 | Win | Win |
| 155 | USDCHF | Sell | 6.77 | -15.38 | 16.00 | No | 6.77 | +0.00 | Win | Win |
| 156 | XAUUSD | Sell | 12.11 | -65.99 | 13.11 | Yes | -20.00 | -32.11 | Win | Loss |
| 157 | XAUUSD | Sell | 11.42 | 11.42 | 12.60 | No | 11.42 | +0.00 | Win | Win |
| 158 | EURJPY | Buy | 13.62 | -55.97 | 18.38 | Yes | -20.00 | -33.62 | Win | Loss |
| 159 | EURJPY | Buy | 8.44 | -1.50 | 13.20 | No | 8.44 | +0.00 | Win | Win |
| 160 | GBPUSD | Buy | 3.80 | -93.42 | 9.49 | Yes | -20.00 | -23.80 | Win | Loss |
| 161 | XAUUSD | Buy | 2.22 | -61.34 | 3.34 | Yes | -20.00 | -22.22 | Win | Loss |
| 162 | XAUUSD | Buy | 7.19 | 7.19 | 8.46 | No | 7.19 | +0.00 | Win | Win |
| 163 | XAUUSD | Buy | 1.96 | -1.26 | 3.33 | No | 1.96 | +0.00 | Win | Win |
| 164 | XAUUSD | Sell | 12.06 | -1.18 | 13.45 | No | 12.06 | +0.00 | Win | Win |
| 165 | XAUUSD | Sell | 6.41 | 6.41 | 7.55 | No | 6.41 | +0.00 | Win | Win |
| 166 | XAUUSD | Sell | 12.44 | 12.44 | 13.43 | No | 12.44 | +0.00 | Win | Win |
| 167 | XAUUSD | Sell | 14.78 | -18.87 | 15.88 | No | 14.78 | +0.00 | Win | Win |
| 168 | XAUUSD | Buy | 14.08 | -1.18 | 42.26 | No | 14.08 | +0.00 | Win | Win |
| 169 | XAUUSD | Buy | 3.98 | -9.78 | 28.26 | No | 3.98 | +0.00 | Win | Win |
| 170 | XAUUSD | Buy | 21.97 | -59.41 | 33.51 | Yes | -20.00 | -41.97 | Win | Loss |
| 171 | XAUUSD | Buy | 0.74 | -2.12 | 1.72 | No | 0.74 | +0.00 | Win | Win |
| 172 | XAUUSD | Sell | 23.64 | 23.64 | 25.22 | No | 23.64 | +0.00 | Win | Win |
| 173 | XAUUSD | Sell | 15.37 | -64.43 | 26.47 | Yes | -20.00 | -35.37 | Win | Loss |
| 174 | XAUUSD | Sell | 7.51 | -9.40 | 34.50 | No | 7.51 | +0.00 | Win | Win |
| 175 | XAUUSD | Sell | -109.67 | -109.67 | -1.15 | Yes | -20.00 | +89.67 | Loss | Loss |
| 176 | XAUUSD | Sell | 2.29 | -24.62 | 3.89 | Yes | -20.00 | -22.29 | Win | Loss |
| 177 | XAUUSD | Sell | -112.19 | -112.19 | -6.17 | Yes | -20.00 | +92.19 | Loss | Loss |
| 178 | XAUUSD | Buy | 0.44 | -36.78 | 1.99 | Yes | -20.00 | -20.44 | Win | Loss |
| 179 | XAUUSD | Sell | 4.35 | -38.69 | 6.40 | Yes | -20.00 | -24.35 | Win | Loss |
| 180 | XAUUSD | Sell | 14.60 | -2.05 | 15.97 | No | 14.60 | +0.00 | Win | Win |
| 181 | XAUUSD | Buy | 12.42 | -56.82 | 13.41 | Yes | -20.00 | -32.42 | Win | Loss |
| 182 | GBPUSD | Buy | 5.31 | -58.78 | 11.00 | Yes | -20.00 | -25.31 | Win | Loss |
| 183 | XAUUSD | Buy | 5.22 | 5.22 | 6.29 | No | 5.22 | +0.00 | Win | Win |
| 184 | USDCHF | Sell | 3.70 | -16.65 | 12.95 | No | 3.70 | +0.00 | Win | Win |
| 185 | XAUUSD | Buy | 8.19 | -0.99 | 9.19 | No | 8.19 | +0.00 | Win | Win |
| 186 | XAUUSD | Sell | 0.83 | -14.29 | 2.06 | No | 0.83 | +0.00 | Win | Win |

### Target Questions

- Did the rule remove losses below -$100 in the cohort? Yes. Baseline had 4 such losses; synthetic results have 0 because all triggered losses are capped at -$20.
- Did it stop trades that historically became winners? Yes. 16 baseline winners had MAE <= -$20 and become synthetic -$20 outcomes.
- Did the cohort become profitable under the synthetic rule? No. Synthetic P/L is -118.88.

## Interpretation

- The synthetic rule materially improves the cohort's P/L by compressing large losses.
- The improvement comes with a meaningful reduction in win rate because several historical winners experienced MAE below -$20 before closing profitably.
- This is a counterfactual result based on recorded final MAE, not proof that real-time fills would occur exactly at -$20.
- The result does not authorize any operating policy modification.

## Hypothesis candidates

- Strict loss compression may improve the high-frequency day-trading regime if the system's small-win profile persists.
- The hypothesis is weakened if the winners converted to synthetic losses represent repeatable recoveries rather than noise.

## Contradiction tests

- Compare results across future post-regime trades once the sample expands.
- Reconstruct intratrade path from ticks where available to determine whether MAE breach timing occurs before or after favorable movement.
- Test sensitivity at nearby caps, such as -$15, -$25, and -$30, before any adoption review.

## Open questions

- Is the `id >= 136` cohort stable enough to define a new regime, or is it a temporary Gold-heavy episode?
- Are XAUUSD MAE values precise enough to infer real-time stop behavior without slippage assumptions?
- Would the synthetic stop alter AA's future admission, portfolio, or risk state in ways not captured by this static replay?

GM Review Required
