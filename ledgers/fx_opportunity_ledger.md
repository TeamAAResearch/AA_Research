# AA Project — Research Ledger & Pipeline Analysis
**Official Baseline:** 2026-06-22 07:02:25 UTC (Clean restart / production collection start)  
**Last Updated:** 2026-06-23 10:24 UTC  
**Checkpoint:** N=25 FX Opportunities ✅ | N=50 Pending | N=100 Pending

---

## 1. Production Dataset Summary

| Metric | Value |
|---|---|
| Closed `standard_signal` trades | 25 |
| Open `standard_signal` trades | 3 |
| Closed realized P/L | **+$202.32** |
| Win rate | **96.0%** (24W / 1L) |

> [!NOTE]
> The 96% win rate over 25 trades is directionally encouraging but statistically premature. One large loss (GBPJPY Buy: -$284.41) was absorbed by many small wins. This pattern requires monitoring for survivorship bias.

---

## 2. FX Opportunity Ledger Summary

| Metric | Count |
|---|---|
| **FX opportunities observed** | **68** (45 blocked + 18 admitted + 5 execution blocks) |
| **FX admitted** | **18** |
| **FX blocked (pre-admission)** | **45** |
| **FX execution blocks** | **5** (Kill switch) |

---

## 3. Pipeline Attrition (FX Only, Since Baseline)

| Pipeline Stage | FX Opportunities Lost | % of FX Blocks |
|---|---|---|
| 2. Governance Block | 0 | 0% |
| 3. Portfolio Block | 0 | 0% |
| 4. Risk Block | 19 | 42.2% |
| 5. Admission Block | 23 | 51.1% |
| 6. Execution Block (Kill Switch) | 5 | — |
| Unclassified (Symbol Activity Cap) | 3 | 6.7% |

> [!IMPORTANT]
> **Bottleneck Shift:** At the N=3 checkpoint, Risk Block was 100% of FX attrition. At N=25, Admission Block has emerged as the co-dominant bottleneck (51.1% vs 42.2%). Neither stage is clearly dominant yet. The "unclassified" blocks are now identified as a **Symbol Activity Cap** (max 2 EURJPY entries per 60 minutes), which is a rate-limiting governance control.

---

## 4. Boundary Risk Events
*Opportunities rejected very near the risk limit.*

| Symbol | Risk Cap | Actual Planned Risk | Overshoot |
|---|---|---|---|
| GBPUSD | $250.00 | $250.04 | **$0.04** |
| GBPUSD | $250.00 | $250.15 | **$0.15** |
| USDCHF | $250.00 | $250.01 | **$0.01** |
| GBPUSD | $250.00 | $250.13 | **$0.13** |
| USDCHF | $250.00 | $250.26 | **$0.26** |
| GBPUSD | $250.00 | $250.11 | **$0.11** |

> [!WARNING]
> **Observation:** Multiple FX opportunities are being rejected by margins of $0.01 to $0.26. These are not trades failing a risk gate by a wide margin. They are trades failing by pennies. This is evidence to accumulate, not a recommendation to change the limit.

---

## 5. Symbol-Level P/L (Closed `standard_signal` Trades)

| Symbol | Side | Trades | Net P/L | Avg MFE | Avg MAE |
|---|---|---|---|---|---|
| XAUUSD | Sell | 5 | **+$311.82** | $63.31 | -$11.99 |
| EURJPY | Sell | 4 | +$52.76 | $17.93 | -$7.09 |
| XAUUSD | Buy | 5 | +$33.76 | $9.17 | -$9.57 |
| EURUSD | Sell | 1 | +$24.03 | $28.40 | -$0.87 |
| GBPUSD | Buy | 3 | +$15.47 | $10.95 | -$22.21 |
| GBPJPY | Sell | 1 | +$14.06 | $22.26 | -$12.65 |
| USDJPY | Sell | 2 | +$13.33 | $9.77 | -$17.21 |
| GBPUSD | Sell | 1 | +$3.02 | $8.68 | -$21.14 |
| **GBPJPY** | **Buy** | **3** | **-$265.93** | $11.46 | **-$101.74** |

> [!CAUTION]
> **GBPJPY Buy** is the only negative symbol/side combination. Its average MAE of -$101.74 is an order of magnitude worse than every other entry. Nolan's trade review of this pattern is critical.

---

## 6. Session Analysis (Closed `standard_signal` Trades)

| Session | Trades | Net P/L |
|---|---|---|
| Overlap | 12 | **+$142.37** |
| London | 10 | **-$212.03** |
| NY | 3 | **+$271.98** |

> [!IMPORTANT]
> **London session is net negative.** All 3 GBPJPY Buy losses occurred during the London session. The NY session, despite only 3 trades, is the highest P/L contributor. Session dependence hypothesis remains open but is gaining definition.

---

## 7. Hypothesis Status Update

| Hypothesis | Status | Evidence |
|---|---|---|
| H1: AA is over-filtering opportunities | **Open** | Admission Block is now 51% of FX attrition; boundary risk events show trades rejected by pennies |
| H2: AA cannot generate FX opportunities | **Weaker** | 68 FX opportunities observed in ~36 hours |
| H3: Metals dominance is a session effect | **Stronger** | Overlap and NY sessions produce meaningful FX flow |
| H4: Risk Block is the dominant FX bottleneck | **Weaker** | At N=25, Admission Block has overtaken Risk Block as the largest single attrition stage |

---

## 8. Open Questions (Ranked)

1. Is GBPJPY Buy a structural weakness or sample noise?
2. Are the boundary risk events ($0.01–$0.26 overshoots) systematically suppressing profitable FX trades?
3. Does session profitability (NY strong, London weak) persist beyond the current sample?
4. Would blocked opportunities have improved or worsened expected outcomes?
5. Is the 96% win rate masking a fragile risk/reward profile (many small wins, rare catastrophic losses)?
