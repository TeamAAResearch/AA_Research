# AA Research — FX Long Analysis & Loss Classification
**Date:** 24 June 2026  
**Directive:** Determine whether underperformance originates from FX long selection, trade management, or the FX asset class itself.

---

## 1. FX vs Metals Contribution (Asset Class + Side)

| Class | Side | Trades | Total P/L | Avg P/L | Avg MFE | Avg MAE | Stop Losses |
|---|---|---|---|---|---|---|---|
| Metals | Sell | 7 | **+$330.71** | +$47.24 | $48.24 | -$12.63 | 0 |
| FX | Sell | 10 | **+$146.17** | +$14.62 | $19.88 | -$21.75 | 0 |
| Metals | Buy | 7 | -$47.18 | -$6.74 | $14.96 | -$19.54 | 1 |
| **FX** | **Buy** | **8** | **-$793.57** | **-$99.20** | $9.09 | **-$114.37** | **3** |

> [!CAUTION]
> **FX Buy is the sole source of catastrophic loss.** It accounts for -$793.57 against a total portfolio of -$363.87. Every other class/side combination is profitable. Remove FX Buy and the portfolio is +$429.70.

---

## 2. FX Longs — Individual Trade Detail

| Pair | Score | Session | Duration | MFE | MAE | P/L | Exit | Classification |
|---|---|---|---|---|---|---|---|---|
| GBPJPY | 75 | London | 5m | +$22.46 | -$8.19 | **+$14.27** | Trailing | ✅ Clean win |
| GBPJPY | 75 | London | 25m | +$12.39 | -$12.62 | **+$4.21** | Trailing | ✅ Clean win |
| GBPUSD | 80 | London | 10m | +$17.91 | -$3.58 | **+$12.07** | Trailing | ✅ Clean win |
| GBPUSD | 90 | London | 20m | +$8.70 | -$10.21 | **+$3.02** | Trailing | ✅ Clean win |
| GBPUSD | 80 | London | 1h46m | +$6.23 | -$52.84 | **+$0.38** | Trailing | ⚠️ Survived |
| EURUSD | 90 | Overlap | 21h | +$1.75 | -$266.42 | **-$266.42** | Stop loss | 🔴 Loss |
| GBPUSD | 90 | Overlap | 24.6h | +$3.77 | -$276.69 | **-$276.69** | Stop loss | 🔴 Loss |
| GBPJPY | 75 | London | 20.8h | -$0.47 | -$284.41 | **-$284.41** | Stop loss | 🔴 Loss |

---

## 3. Loss Classification

### Loss 1: GBPJPY Buy — **Entry Failure**
- **MFE: -$0.47.** The trade never showed a single tick of profit.
- The momentum signal was exhausted. AA had already captured the same move twice.
- The system flagged "paper performance is poor" but admitted at 75/70.
- **Verdict:** AA should not have entered. The signal was spent.

### Loss 2: EURUSD Buy — **Management Failure**
- **MFE: +$1.75.** The trade briefly went positive, then reversed.
- Score was 90, indicating a high-quality setup.
- The trade was held for 21 hours without intervention as it moved -$266 against.
- **Verdict:** The entry was defensible. The failure was holding a deteriorating position for 21 hours with no time-based or adverse-movement exit.

### Loss 3: GBPUSD Buy — **Management Failure**
- **MFE: +$3.77.** The trade briefly went positive, then reversed.
- Score was 90, indicating a high-quality setup.
- Held for 24.6 hours to stop loss.
- **Verdict:** Same as EURUSD. Defensible entry. No mechanism to exit a losing trade before the stop is hit.

### Summary

| Classification | Trades | Total Loss | Root Cause |
|---|---|---|---|
| **Entry Failure** | 1 | -$284.41 | Exhausted momentum, re-entry into spent move |
| **Management Failure** | 2 | -$543.11 | No time-based exit, no adverse-movement exit |
| **Market Failure** | 0 | $0 | — |

> [!IMPORTANT]
> **2 of 3 losses (66%, -$543) are management failures, not entry failures.** The admission score correctly identified quality setups (score 90). The system failed to manage the downside after entry. Market conditions were not anomalous.

---

## 4. MFE vs Realized P/L (FX Only)

| Side | Trades | Avg MFE | Avg Realized | Capture % | Observation |
|---|---|---|---|---|---|
| **Sell** | 10 | $19.88 | +$14.62 | **73.5%** | Healthy capture |
| **Buy (winners only)** | 5 | $13.54 | +$6.79 | **50.1%** | Leaves half on the table |
| **Buy (all)** | 8 | $9.09 | -$99.20 | **N/A** | Catastrophic losses dominate |

---

## 5. Duration vs Outcome (FX Longs Only)

| Duration | Trades | Win Rate | Avg P/L | Stop Losses |
|---|---|---|---|---|
| **<1 hour** | 4 | **100%** | +$8.39 | 0 |
| **1–4 hours** | 1 | 100% | +$0.38 | 0 |
| **>8 hours** | 3 | **0%** | -$275.84 | 3 |

The pattern from the general survival analysis holds perfectly for FX longs specifically.

---

## 6. Conclusions (Evidence Only)

| Question | Answer | Confidence |
|---|---|---|
| Is the problem FX long **selection**? | Partially. 1 of 3 losses was an entry failure. But 2 of 3 had defensible entries (score 90). | Medium |
| Is the problem **trade management**? | **Yes.** 2 of 3 losses (-$543) were management failures. AA has no mechanism to exit a losing trade before the stop. | **High** |
| Is the problem the **FX asset class**? | No. FX Sell is profitable (+$146). The issue is isolated to FX Buy held overnight. | High |

---

No recommendations. No changes. Evidence only.
