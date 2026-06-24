# Evidence Density Repository Design Proposal

Date: 2026-06-24
Prepared by: Codex
Scope: Repository design proposal only
Authority: AA Organizational Charter v1.0

## Objective

Increase evidence density without changing AA behavior.

This proposal does not recommend more trades, more risk, threshold changes, strategy changes, portfolio changes, or code changes.

Success criterion:

More observable AA decisions.

Not more AA trades.

Not more AA risk.

Not more AA optimization.

## 1. Decision Funnel Map

AA's observable decision funnel should be represented as:

1. Market observed
2. Symbol scanned
3. Opportunity generated
4. Opportunity scored
5. Admission decision
6. Risk decision
7. Portfolio decision
8. Execution decision
9. Trade opened or opportunity blocked
10. Position managed
11. Position exited
12. Trade reviewed
13. Ledger reconciled
14. Repository preserved

Research objective:

Identify where FX opportunities disappear without changing how AA makes those decisions.

## 2. Available vs Discarded Decision Data

### Already Available In Current Research Repository

Existing repository structures:

- `ledgers/fx_opportunity_ledger.csv`
- `ledgers/blocked_opportunity_ledger.csv`
- `ledgers/trade_history.csv`
- `memory/aa_research_map.md`
- `hypotheses/active_hypotheses.md`
- `governance/aa_organizational_charter_v1.md`

Current available fields include:

- Timestamp
- Pair / symbol
- Asset class
- Session
- Side
- Admission score
- Outcome
- Block stage
- Block classification
- Reason
- Source table
- Source id
- Baseline inclusion
- Trade entry
- Trade exit
- Realized P/L
- MFE
- MAE
- Exit reason
- Duration

### Decision Data That May Exist But Is Not Yet Fully Preserved In Repository Form

These are repository-design targets only. This document does not assert that all fields are currently available in the live system.

- Every scan cycle by symbol
- Symbols scanned but producing no signal
- Raw setup score components
- Admission pass / fail reason before later gates
- Risk pass / fail reason with numeric distance from limit
- Portfolio pass / fail reason with exposure context
- Execution pass / fail reason
- Kill-switch state at decision time
- Spread at decision time for blocked opportunities
- Live quote snapshot at decision time
- Duplicate-symbol or activity-cap reason
- Whether a blocked opportunity later produced favorable or adverse excursion
- Whether a non-signal scan later became a missed market opportunity

## 3. Proposed Repository Structures

The repository can increase evidence density through additional ledgers and observation files without changing AA behavior.

### A. Decision Cycle Ledger

Proposed path:

`ledgers/decision_cycle_ledger.csv`

Purpose:

Record each observed AA cycle and symbol-level scan outcome.

Suggested columns:

```text
cycle_id,timestamp_utc,symbol,asset_class,session,market_open,quote_available,spread,signal_generated,score_available,admission_checked,risk_checked,portfolio_checked,execution_checked,final_outcome,source_table,source_id,notes
```

Analysis enabled:

- Opportunity density by pair and session
- Symbols scanned but not generating signals
- Data outages vs true inactivity
- Whether AA is observing enough FX markets

### B. Opportunity Decision Ledger

Proposed path:

`ledgers/opportunity_decision_ledger.csv`

Purpose:

Track every opportunity that reaches scoring or gate evaluation.

Suggested columns:

```text
opportunity_id,timestamp_utc,pair,asset_class,session,side,admission_score,score_bucket,signal_reason,admission_result,admission_reason,risk_result,risk_reason,risk_amount,risk_limit,risk_overshoot,portfolio_result,portfolio_reason,execution_result,execution_reason,final_outcome,trade_id,baseline_included,notes
```

Analysis enabled:

- Admitted vs blocked opportunities
- High-score vs low-score opportunities
- Admission block vs risk block vs portfolio block
- Boundary Risk Block vs Material Risk Block
- Opportunity conversion rate by pair, side, session, and score bucket

### C. Blocked Follow-Through Ledger

Proposed path:

`ledgers/blocked_followthrough_ledger.csv`

Purpose:

Evaluate blocked opportunities without binary win/loss framing.

Suggested columns:

```text
blocked_id,opportunity_id,timestamp_utc,pair,session,side,block_stage,block_reason,admission_score,entry_reference_price,lookahead_window_minutes,max_favorable_excursion,max_adverse_excursion,spread_adjusted_mfe,spread_adjusted_mae,expected_outcome_under_aa_exit,risk_adjusted_outcome,followthrough_status,notes
```

Analysis enabled:

- Whether blocks improved or worsened expected business outcomes
- Favorable excursion vs adverse excursion for blocked ideas
- Boundary risk block quality
- Admission rejection quality

### D. Score Bucket Summary

Proposed path:

`observations/score_bucket_summary.md`

Purpose:

Human-readable summary of score calibration evidence.

Suggested sections:

- `<50`
- `50-60`
- `60-70`
- `70-80`
- `80-85`
- `85+`

For each bucket:

- Signals
- Admissions
- Blocks
- Closed trades
- Net P/L
- MFE
- MAE
- Current interpretation status: Observation / Hypothesis / Finding

### E. Pair Session Matrix

Proposed path:

`observations/pair_session_matrix.csv`

Purpose:

Track opportunity flow by pair and session.

Suggested columns:

```text
date_utc,pair,session,signals,admitted,blocked,closed_trades,net_pnl,avg_score,avg_mfe,avg_mae,notes
```

Analysis enabled:

- FX opportunity flow by session
- Whether Asia remains negligible
- Whether London / overlap dominate
- Whether pair concentration is structural

### F. Evidence Gap Register

Proposed path:

`memory/evidence_gap_register.md`

Purpose:

Track what the organization cannot yet know because data is missing, sparse, or unreconciled.

Suggested fields:

- Question
- Missing evidence
- Current source
- Current limitation
- Required future evidence
- Owner
- Review trigger

## 4. Future Analysis Enabled

### Admitted vs Blocked Opportunities

Required structures:

- `opportunity_decision_ledger.csv`
- `blocked_followthrough_ledger.csv`
- `trade_history.csv`

Primary comparisons:

- Admission outcome vs realized / expected outcome
- Risk-blocked expected outcome vs admitted trade outcome
- Boundary risk blocks vs material risk blocks
- Execution blocks vs admitted trades

### High-Score vs Low-Score Opportunities

Required structures:

- `opportunity_decision_ledger.csv`
- `score_bucket_summary.md`
- `trade_history.csv`

Primary comparisons:

- Score bucket vs admission rate
- Score bucket vs expectancy
- Score bucket vs MFE / MAE
- Score bucket vs block stage

### Risk-Blocked Opportunities

Required structures:

- `opportunity_decision_ledger.csv`
- `blocked_followthrough_ledger.csv`

Primary comparisons:

- Risk amount vs risk limit
- Overshoot size
- Boundary vs material block
- MFE / MAE after block
- Expected outcome under AA's actual exit framework

### Opportunity Flow By Pair And Session

Required structures:

- `decision_cycle_ledger.csv`
- `opportunity_decision_ledger.csv`
- `pair_session_matrix.csv`

Primary comparisons:

- Pair scan count
- Signal generation count
- Admission rate
- Block rate
- Closed-trade expectancy
- Session concentration

## 5. Repository-Only Implementation Principle

This proposal is intentionally limited to repository structure.

It does not require:

- More trades
- Higher risk
- Different thresholds
- Strategy changes
- Risk-rule changes
- Portfolio-rule changes
- AA behavior changes

Any future automated population of these structures would require a separate authorization decision.

## 6. Current Bottleneck Framing

Current bottleneck:

Insufficient observable decision density.

Not necessarily insufficient trade count.

The organization needs more visibility into AA's existing decisions, including:

- What AA scanned
- What AA scored
- What AA rejected
- Which gate rejected it
- What happened after rejection
- Whether admitted opportunities were actually better than blocked opportunities

## 7. Record-Only Conclusion

This document proposes repository structures for preserving more of AA's existing decision process.

No findings are created.

No hypotheses are promoted.

No recommendations are made to change AA behavior.
