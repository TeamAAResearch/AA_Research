# AA Research Department — Observation Period Studies
**Date:** 23 June 2026  
**Status:** Research only. No code changes. No recommendations.

---

# Study 1: GBPJPY Buy Autopsy

## Question
Is GBPJPY Buy a structural weakness or sample noise?

## Evidence

### The Three Trades

| # | Opened | Closed | Entry | Session | Score | MFE | MAE | P/L | Exit Reason | Duration |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 09:03:02 | 09:08:04 | 213.745 | London | 75 | +$22.46 | -$8.19 | **+$14.27** | Trailing protection | 5 min |
| 2 | 09:08:04 | 09:33:12 | 213.876 | London | 75 | +$12.39 | -$12.62 | **+$4.21** | Trailing protection | 25 min |
| 3 | 12:39:09 | 09:31:38+1d | 214.658 | London | 75 | -$0.47 | **-$284.41** | **-$284.41** | Stop loss hit | **20.8 hours** |

### Common Factors (All 3 Trades)
- **Session:** London (100%)
- **Admission Score:** 75/70 (all identical, barely above threshold)
- **Volatility Regime:** Normal (all identical)
- **Entry Score Reason:** *"Recent GBPJPY paper performance is poor"* (flagged on every entry)
- **Signal:** Momentum Buy

### What Separates Winner from Loser
- Trades 1 & 2: Entered during the same 30-minute window. Both caught a small upward push. Both exited via trailing protection within minutes.
- Trade 3: Entered 3.5 hours later at a **higher price** (214.658 vs 213.745). The momentum had already exhausted. The trade never went positive (MFE = -$0.47), meaning **price moved against it from the very first tick** and never recovered. It held for 20.8 hours before hitting the stop loss.

### Findings

| Element | Finding |
|---|---|
| **Observation** | GBPJPY Buy trade #3 entered at the end of an exhausted momentum move, 91 pips above trade #1's entry. It never showed a positive MFE. |
| **Explanation** | AA re-entered a momentum signal that had already been captured twice. The admission score did not penalize re-entry after the move was spent. The score reason even flagged *"Recent GBPJPY paper performance is poor"* but the system still admitted it. |
| **Confidence** | **Medium.** The pattern is consistent (late re-entry into spent momentum) but the sample is only 1 catastrophic loss. |
| **Evidence** | MFE of -$0.47 (never profitable). Duration of 20.8 hours (10x–60x longer than the winners). Price was 91 pips above the first GBPJPY Buy entry. |

> [!WARNING]
> **Key Insight:** The admission system flagged the problem ("paper performance is poor") but did not block the trade. The score of 75 still passed the 70 threshold. This is not a signal generation failure. This is an admission calibration question for future investigation.

---

# Study 2: Winner DNA — What Does AA's Edge Look Like?

## Question
What do the 24 winning trades have in common?

## Score Band Analysis

| Score Band | Trades | Total P/L | Avg P/L | Avg MFE | Avg MAE |
|---|---|---|---|---|---|
| **91+** | **10** | **+$356.34** | **+$35.63** | **$37.91** | -$15.39 |
| 85–90 | 4 | +$32.39 | +$8.10 | $11.08 | -$8.51 |
| 75–84 | 10 | -$189.43 | -$18.94 | $14.81 | -$36.80 |
| <75 | 1 | +$3.02 | +$3.02 | $8.68 | -$21.14 |

> [!IMPORTANT]
> **The admission score predicts outcomes.** Trades scored 91+ produced +$356.34 across 10 trades. Trades scored 75–84 produced -$189.43 across 10 trades. The scoring system has signal, but the 70-point FX threshold allows too many weak trades through.

## MFE Capture Efficiency
*How much of the available profit does AA actually bank?*

| Symbol | Side | Trades | Avg MFE | Avg Realized | **Capture %** |
|---|---|---|---|---|---|
| XAUUSD | Sell | 5 | $63.31 | $62.36 | **98.5%** |
| EURUSD | Sell | 1 | $28.40 | $24.03 | **84.6%** |
| XAUUSD | Buy | 5 | $9.17 | $6.75 | 73.6% |
| EURJPY | Sell | 4 | $17.93 | $13.19 | 73.6% |
| USDJPY | Sell | 2 | $9.77 | $6.67 | 68.3% |
| GBPJPY | Sell | 1 | $22.26 | $14.06 | 63.2% |
| GBPJPY | Buy | 2 | $17.43 | $9.24 | 53.0% |
| GBPUSD | Buy | 3 | $10.95 | $5.16 | 47.1% |
| GBPUSD | Sell | 1 | $8.68 | $3.02 | **34.8%** |

### Findings

| Element | Finding |
|---|---|
| **Observation** | XAUUSD Sell captures 98.5% of available profit. GBP pairs capture only 35–53%. |
| **Explanation** | XAUUSD Sell trades hit take-profit cleanly (1 out of 5 hit TP). GBP pairs are exited early by trailing protection, leaving significant profit on the table. The trailing exit mechanism appears well-calibrated for metals but too aggressive for GBP crosses. |
| **Confidence** | Medium. The pattern is consistent across all GBP entries but the sample remains small. |
| **Evidence** | Capture efficiency table above. XAUUSD Sell avg MFE: $63.31 → realized $62.36. GBPUSD Sell avg MFE: $8.68 → realized $3.02. |

---

# Study 3: Shadow Portfolio — Blocked FX Opportunities

## Question
What pairs is AA rejecting, and where?

## Pair-Level Block Breakdown (FX Only, Post-Baseline)

| Symbol | Admission Blocks | Risk Blocks | Activity Cap | **Total Blocks** |
|---|---|---|---|---|
| **NZDUSD** | 11 | 0 | 0 | **11** |
| AUDUSD | 5 | 2 | 0 | 7 |
| USDCHF | 0 | 6 | 0 | 6 |
| GBPUSD | 0 | 6 | 0 | 6 |
| USDJPY | 5 | 0 | 3 | 5 |
| USDCAD | 0 | 5 | 0 | 5 |
| EURJPY | 0 | 0 | 3 | 3 |
| GBPJPY | 2 | 0 | 0 | 2 |

### Findings

| Element | Finding |
|---|---|
| **Observation** | Different pairs fail at different pipeline stages. NZDUSD (11 blocks) fails exclusively at Admission. USDCHF and GBPUSD (6 each) fail exclusively at Risk. USDCAD (5) fails exclusively at Risk. |
| **Explanation** | The pipeline does not have a single bottleneck. It has two structurally separate bottlenecks: (1) Pairs with weak momentum/spread characteristics die at Admission (NZDUSD, AUDUSD, USDJPY). (2) Pairs with viable signals but tight risk math die at the $250 cap (GBPUSD, USDCHF, USDCAD). |
| **Confidence** | High. The separation is clean with zero overlap for 4 of 8 pairs. |
| **Evidence** | Block reason classification table above. |

> [!IMPORTANT]
> **Two-Bottleneck Model:** The pipeline does not have one dominant bottleneck. It has two distinct failure modes operating on different pairs:
> - **Admission kills low-quality signals** (NZDUSD, AUDUSD, USDJPY, GBPJPY)
> - **Risk cap kills viable signals** (GBPUSD, USDCHF, USDCAD)
> 
> These are fundamentally different problems requiring different analyses.

### Boundary Risk Events (Full List)

| Timestamp | Symbol | Cap | Actual | Overshoot |
|---|---|---|---|---|
| 07:32:34 | GBPUSD | $250.00 | $250.04 | $0.04 |
| 07:42:37 | GBPUSD | $250.00 | $250.15 | $0.15 |
| 08:32:53 | USDCHF | $250.00 | $250.01 | **$0.01** |
| 08:42:56 | GBPUSD | $250.00 | $250.13 | $0.13 |
| 09:18:07 | USDCHF | $250.00 | $250.26 | $0.26 |
| 12:14:02 | GBPUSD | $250.00 | $250.11 | $0.11 |
| 12:14:02 | USDCAD | $250.00 | $250.08 | $0.08 |
| 12:19:03 | USDCAD | $250.00 | $250.07 | $0.07 |
| 12:19:03 | USDCHF | $250.00 | $250.09 | $0.09 |
| 13:19:23 | USDCHF | $250.00 | $250.19 | $0.19 |
| 13:24:25 | USDCAD | $250.00 | $250.16 | $0.16 |
| 13:24:25 | USDCHF | $250.00 | $250.20 | $0.20 |
| 13:29:27 | USDCAD | $250.00 | $250.05 | $0.05 |
| 13:34:30 | USDCAD | $250.00 | $250.06 | $0.06 |
| 13:59:39 | GBPUSD | $250.00 | $250.03 | $0.03 |
| 14:14:44 | GBPUSD | $250.00 | $250.04 | $0.04 |
| 15:05:00 | AUDUSD | $250.00 | $250.19 | $0.19 |
| 15:05:00 | USDCHF | $250.00 | $250.21 | $0.21 |
| 15:50:16 | AUDUSD | $250.00 | $250.08 | $0.08 |

> [!CAUTION]
> 19 risk blocks identified. **100% are within $0.26 of the limit. The median overshoot is $0.09.** These are not trades failing a risk gate by a wide margin. They are trades failing by pennies. Whether these trades would have been profitable is the critical unanswered question for the Shadow Portfolio.

---

# Summary of Research Findings

| Study | Key Discovery |
|---|---|
| **GBPJPY Buy Autopsy** | The catastrophic loss entered at the tail of an exhausted momentum move. The system flagged the problem ("performance is poor") but admitted anyway at 75/70. |
| **Winner DNA** | The admission score is predictive. Score 91+ trades: +$356.34. Score 75–84 trades: -$189.43. The 70-point FX threshold allows the weakest trades through. |
| **Shadow Portfolio** | Two distinct bottlenecks: Admission kills weak-momentum pairs (NZDUSD). Risk cap kills viable-signal pairs (GBPUSD, USDCHF, USDCAD) by margins of pennies. |

**No recommendations made. No code changes. Evidence only.**
