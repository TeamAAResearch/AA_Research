# AA Project — Daily Report
**Date:** 23 June 2026  
**Audience:** GM & Codex  
**Phase:** DATA COLLECTION AND LEARNING  
**Constraints:** Code freeze in effect. No changes authorized.

---

## Executive Summary

AA has reached its first statistical checkpoint: **25 closed production-quality trades** and **68 FX opportunities observed** since the official baseline.

The system is profitable (+$202.32 realized), operationally stable, and generating meaningful FX flow. However, three findings require close monitoring as data accumulates toward N=50.

---

## Operational Status (Codex)

| Component | Status |
|---|---|
| Runner (PID 32693) | 🟢 Healthy |
| Heartbeat | 🟢 OK |
| Database Integrity | 🟢 OK |
| Backup System | 🟢 Operational |
| Saxo Feed | 🟡 Token expired and was refreshed. Feed recovered. No code change required. |
| Code Freeze | ✅ Enforced |

**Codex Action Items:**
- Continue monitoring runner health and heartbeat.
- No intervention required unless the runner crashes or the feed fails again without self-recovery.

---

## Production Dataset (N=25 Checkpoint)

| Metric | Value |
|---|---|
| Closed `standard_signal` trades | 25 |
| Open `standard_signal` trades | 3 |
| Realized P/L (closed) | **+$202.32** |
| Win rate | 96.0% (24W / 1L) |
| Largest win | XAUUSD Sell: +$267.59 |
| Largest loss | GBPJPY Buy: -$284.41 |

> [!NOTE]
> The win rate of 96% is not yet a meaningful indicator of edge. The single loss (GBPJPY Buy) is larger than any individual win. This is a "many small wins, rare large loss" profile that requires extended observation.

---

## FX Opportunity Pipeline (N=25 Checkpoint)

| Metric | Count |
|---|---|
| FX opportunities observed | 68 |
| FX admitted | 18 |
| FX blocked (pre-admission) | 45 |
| FX execution blocks (kill switch) | 5 |
| **Conversion rate** | **26.5%** |

### Pipeline Attrition by Stage (FX Only)

| Stage | Blocks | Share |
|---|---|---|
| 5. Admission Block | 23 | 51.1% |
| 4. Risk Block | 19 | 42.2% |
| Unclassified (Symbol Activity Cap) | 3 | 6.7% |
| 3. Portfolio Block | 0 | 0% |
| 2. Governance Block | 0 | 0% |

**Key Change:** At the N=3 checkpoint (22 June), Risk Block was 100% of FX attrition. At N=25, Admission Block has overtaken Risk Block as the largest single attrition stage. Neither is clearly dominant. Both require continued tracking through N=50 and N=100.

---

## Three Findings for GM Attention

### Finding 1: GBPJPY Buy Is a Warning Pattern

| Observation | GBPJPY Buy accounts for -$265.93 across 3 trades. Average MAE is -$101.74, an order of magnitude worse than any other symbol/side. |
|---|---|
| **Explanation** | Unknown. Nolan (Trade Review) is investigating. |
| **Confidence** | Medium. The pattern is consistent (3/3 trades negative or severely stressed) but the sample is small. |
| **Evidence** | Without GBPJPY Buy, portfolio P/L would be +$468.25 instead of +$202.32. |

### Finding 2: Boundary Risk Events

| Observation | Six FX opportunities were rejected by the $250 risk cap with overshoots of $0.01 to $0.26. |
|---|---|
| **Explanation** | The risk cap is a hard ceiling. Trades that mathematically require $250.01 of risk are rejected identically to trades requiring $500. |
| **Confidence** | High. The data is unambiguous. |
| **Evidence** | GBPUSD (4 blocks), USDCHF (2 blocks), all within $0.26 of the limit. |

### Finding 3: Session Profitability Diverges

| Session | Trades | Net P/L |
|---|---|---|
| NY | 3 | **+$271.98** |
| Overlap | 12 | +$142.37 |
| London | 10 | **-$212.03** |

| Observation | The London session is net negative. NY is the highest P/L contributor despite having the fewest trades. |
|---|---|
| **Explanation** | All 3 GBPJPY Buy losses occurred during the London session. If GBPJPY Buy is removed, London may normalize. Causation is not yet separable from the GBPJPY Buy outlier. |
| **Confidence** | Low. Sample is too small and confounded by the GBPJPY Buy pattern. |
| **Evidence** | Session/P/L breakdown from `challenger_positions`. |

---

## Hypothesis Tracker

| # | Hypothesis | Prior Status | Current Status | Direction |
|---|---|---|---|---|
| H1 | AA is over-filtering opportunities | Unchanged | Open | ➡️ Admission Block is now 51% of FX attrition |
| H2 | AA cannot generate FX opportunities | Weaker | **Weaker** | ⬇️ 68 FX opportunities observed in ~36 hours |
| H3 | Metals dominance is a session effect | Stronger | **Stronger** | ⬆️ Overlap and NY produce meaningful FX flow |
| H4 | Risk Block is the dominant FX bottleneck | New (22 June) | **Weaker** | ⬇️ Admission Block has overtaken Risk Block |

---

## Business Identity

AA is no longer a metals-only trader. Current profile:

- **Metals:** 10 closed trades, +$345.58 realized P/L (XAUUSD dominates).
- **FX:** 15 closed trades, -$143.26 realized P/L (GBPJPY Buy is the primary drag).
- **Excluding GBPJPY Buy:** FX would be +$122.67.

**Assessment:** AA is a mixed trader. Metals currently subsidize FX losses. The FX book's viability depends on whether GBPJPY Buy is a fixable pattern or a structural weakness.

---

## Open Questions (Ranked by Priority)

1. Is GBPJPY Buy a structural weakness or sample noise?
2. Are boundary risk events ($0.01–$0.26 overshoots) systematically suppressing profitable FX trades?
3. Does session profitability (NY strong, London weak) persist beyond the current sample?
4. Would blocked opportunities have improved or worsened expected outcomes?
5. Is the 96% win rate masking a fragile risk/reward profile?

---

## Next Checkpoints

| Checkpoint | Trigger | Purpose |
|---|---|---|
| **N=50 FX Opportunities** | ~50 more FX blocks/admissions | Determine if Admission Block vs Risk Block dominance stabilizes |
| **N=100 FX Opportunities** | ~100 total | Statistical significance threshold for bottleneck conclusion |
| **29 June GM Review** | Calendar | Full team presentation using Observation/Explanation/Confidence/Evidence standard |

---

## Directives Confirmed

- ✅ Code freeze enforced
- ✅ No strategy changes
- ✅ No threshold changes
- ✅ No risk changes
- ✅ No portfolio changes
- ✅ Evidence collection continues
