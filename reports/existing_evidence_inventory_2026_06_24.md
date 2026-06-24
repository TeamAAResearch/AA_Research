# Existing Evidence Inventory

Date: 2026-06-24
Prepared by: Codex
Scope: Inventory and ranking only
Authority: AA Organizational Charter v1.0

## Objective

Determine the maximum increase in evidence density achievable without changing:

- AA behavior
- Strategy
- Thresholds
- Risk rules
- Portfolio rules
- Trade frequency
- Signal generation

Principle:

The organization does not need more trades.

The organization needs more visibility into the decisions AA is already making.

## Summary

AA already records substantially more decision evidence than is currently represented in the research ledgers.

The largest immediate evidence-density gain is recoverable from existing persisted data, especially:

1. `aa_journal`
2. `blocked_signals`
3. `challenger_ticks`
4. `challenger_positions`
5. `challenger_trades`
6. `aa_decisions`
7. `outputs/challenger_runner.log`

No behavior change is required to extract these into research structures.

## Current Live Data Snapshot

Observed from the local SQLite database at review time:

| Source | Rows |
|---|---:|
| `aa_journal` | 99,630 |
| `aa_decisions` | 593 |
| `blocked_signals` | 350 |
| `challenger_ticks` | 11,674 |
| `challenger_positions` | 145 |
| `challenger_trades` | 143 |
| `symbol_quarantine` | 9 |
| `runner_heartbeats` | 1 |
| `anomaly_clearances` | 15 |
| `signals` | 14 |
| `simulated_orders` | 14 |
| `historical_positions` | 1 |

Important operational observation:

Recent runner log lines show `symbols=[]` and Saxo `HTTPError` cycles after 2026-06-24 09:27 UTC. That is operational evidence and should be separated from trading-performance interpretation.

## 1. Existing Data Source Inventory

### 1. `aa_journal`

Purpose:

AA action journal for scouting, no-entry, blocked signal, entry, hold, exit, cycle-pause, and data-unavailable events.

Available fields:

- `id`
- `created_at`
- `event_type`
- `action`
- `symbol`
- `position_id`
- `staff_advice`
- `aa_reason`
- `outcome_snapshot`

Observed action examples:

- `DATA_UNAVAILABLE`
- `NO_ENTRY`
- `HOLD_POSITION`
- `BLOCKED_SIGNAL`
- `CYCLE_PAUSED`
- `CLOSE_POSITION`
- `BLOCK_NEW_ENTRIES`
- `OPEN_SELL`
- `OPEN_BUY`

Retention period:

- Persisted in SQLite.
- No explicit table-level retention observed.
- Backed up by SQLite backup process.

Current usage:

- Dashboard shows recent AA activity.
- Used for recent activity counts.
- Not yet fully flattened into research ledgers.

Research value:

- Very high.
- Best current source for symbol-level decision density.
- Captures no-entry reasons that never become trades.
- Captures data-unavailable cycles, open-position holds, and per-symbol scout outcomes.

Currently underused evidence:

- Full per-symbol scan history.
- Frequency of `NO_ENTRY` by pair and session.
- Difference between true inactivity and unavailable data.
- Reasons for no-entry cycles before a signal becomes a blocked or admitted opportunity.

### 2. `blocked_signals`

Purpose:

Records signals that reached a blocking decision.

Available fields:

- `id`
- `created_at`
- `symbol`
- `side`
- `signal_score`
- `status`
- `block_reason`
- `raw_metadata`

`raw_metadata` may contain:

- Tick count
- Momentum threshold
- Entry reference price
- Admission approval state
- Admission score
- Required score
- Admission reasons
- Planned risk details for risk-cap blocks when applicable

Retention period:

- Persisted in SQLite.
- No explicit table-level retention observed.
- Backed up by SQLite backup process.

Current usage:

- Dashboard shows recent blocked signals.
- Research reports manually summarize some block counts.
- Not yet normalized into an opportunity-decision ledger.

Research value:

- Very high.
- Primary source for admitted vs blocked comparison.
- Primary source for score calibration of rejected opportunities.
- Primary source for admission, risk, portfolio, quarantine, metals, and activity-cap blocks.

Currently underused evidence:

- JSON metadata is trapped in text form.
- Block stage is inferable but not normalized.
- Admission score and required score are not flattened for all blocked opportunities.
- Boundary vs material risk blocks can be extracted when risk fields are present.

### 3. `challenger_ticks`

Purpose:

Stores live quote snapshots for tradeable quotes seen by AA.

Available fields:

- `id`
- `created_at`
- `symbol`
- `asset_type`
- `uic`
- `bid`
- `ask`
- `mid`

Retention period:

- Persisted in SQLite.
- No explicit pruning observed.
- Backed up by SQLite backup process.

Current usage:

- Used to form momentum decisions.
- Used to calculate MFE / MAE for closed trades.
- Used by trade reviews and market-data analysis.

Research value:

- Very high.
- Enables post-hoc MFE / MAE for admitted trades.
- May enable follow-through analysis for blocked opportunities if timestamp and symbol align.
- Helps evaluate whether blocked opportunities later moved favorably or adversely.

Currently underused evidence:

- Blocked-opportunity follow-through.
- Quote availability by pair and session.
- Spread behavior over time.
- Whether a no-entry decision later became a missed market move.

### 4. `challenger_positions`

Purpose:

Canonical paper-position lifecycle table.

Available fields:

- Open/close timestamps
- Symbol
- Asset type
- Side
- Quantity
- Entry
- Stop loss
- Take profit
- Exit
- P/L
- Status
- Entry reason
- Close reason
- Session
- Spread at entry
- Spread percentage at entry
- Entry score
- Entry score reasons
- Volatility regime
- Volatility snapshot
- Signal side
- Signal reason
- Exit reason
- Time in trade
- MFE
- MAE
- Realized P/L
- Close price
- Sample type
- Training-probe flag
- Training-mode flag

Retention period:

- Persisted in SQLite.
- No explicit table-level retention observed.
- Backed up by SQLite backup process.

Current usage:

- Dashboard open and closed trade views.
- Trade reviews.
- P/L and promotion snapshots.
- Risk, portfolio, anomaly, and strategy research modules.

Research value:

- Very high.
- Best source for executed-trade quality.
- Canonical for production-quality closed-trade analysis.

Currently underused evidence:

- Entry-score reasons are JSON/text and can be normalized.
- Volatility snapshots can be flattened.
- Side/session/duration interactions can be structured into reusable research ledgers.

### 5. `challenger_trades`

Purpose:

Closed trade record table, populated when a challenger position closes.

Available fields:

- Created timestamp
- Symbol
- Side
- Quantity
- Entry
- Exit
- P/L
- Status
- Entry reason
- Close reason
- Same learning tags as `challenger_positions`

Retention period:

- Persisted in SQLite.
- No explicit table-level retention observed.
- Backed up by SQLite backup process.

Current usage:

- Capital and realized P/L calculations.
- Daily P/L.
- Promotion and review modules.

Research value:

- High.
- Convenient source for closed-trade summaries.
- Less lifecycle-complete than `challenger_positions` because it lacks the original open-position row context.

Currently underused evidence:

- Can be joined back to `challenger_positions` for consistency checks.
- Can validate closed-trade count and P/L against position lifecycle data.

### 6. `aa_decisions`

Purpose:

Records AA's operating-level decision each cycle.

Available fields:

- `id`
- `created_at`
- `action`
- `conclusion`
- `accepted_staff`
- `overrides`
- `blockers`

Retention period:

- Persisted in SQLite.
- No explicit table-level retention observed.
- Backed up by SQLite backup process.

Current usage:

- Dashboard / decision history.
- Useful for understanding cycle-level gates.

Research value:

- High.
- Best current persisted source for cycle-wide staff veto decisions.
- Helps distinguish symbol-level opportunity loss from operating-level blocked cycles.

Currently underused evidence:

- Does not preserve the full nested risk, portfolio, downside, or anomaly snapshot.
- Still useful for reconstructing when AA was clear to scout vs blocked from new entries.

### 7. `outputs/challenger_runner.log`

Purpose:

Runner-level cycle log.

Available fields:

- Timestamp
- Cycle status
- Symbols successfully priced
- Opened count
- Closed count
- Idea count
- Capital
- First few skipped reasons
- First few errors

Retention period:

- Plain log file.
- No explicit rotation observed.
- Backed up by backup process when backup runs.

Current usage:

- Status checks.
- Systems reliability snapshots.
- Operational troubleshooting.

Research value:

- High for operations.
- Medium for trading research.
- Helps detect data outages, partial symbol coverage, runner stalls, HTTP errors, and symbol coverage gaps.

Currently underused evidence:

- Feed-quality timeline.
- Symbol availability by cycle.
- Data outage vs low-opportunity distinction.

Limitation:

- Skipped reasons are truncated to the first few items in the runner summary, so `aa_journal` is better for full symbol-level scout outcomes.

### 8. `runner_heartbeats`

Purpose:

Current runner heartbeat/status table.

Available fields:

- `runner_name`
- `pid`
- `started_at`
- `last_heartbeat_at`
- `last_cycle_status`
- `last_error`
- `updated_at`

Retention period:

- Current state only.
- Upserted by runner, so history is overwritten.

Current usage:

- Official status command.
- Operational health checks.

Research value:

- Medium for operational reliability.
- Low for trading decision analysis.

Currently underused evidence:

- Since only latest state is retained, historical heartbeat quality must be reconstructed from runner logs, not this table.

### 9. `symbol_quarantine`

Purpose:

Records post-stop symbol quarantine events.

Available fields:

- `id`
- `created_at`
- `symbol`
- `reason`

Retention period:

- Persisted in SQLite.
- No explicit pruning observed.

Current usage:

- Entry blocking for symbols recently stopped out.

Research value:

- Medium.
- Helps connect stop-loss events to later opportunity suppression.

Currently underused evidence:

- Quarantine frequency by symbol.
- Whether quarantine blocks prevented repeated losses or suppressed recovery trades.

### 10. `anomaly_clearances`

Purpose:

Records anomalies manually or systemically cleared.

Available fields:

- `id`
- `created_at`
- `anomaly_id`
- `rule`
- `symbol`
- `severity`
- `detail`
- `clearance_reason`

Retention period:

- Persisted in SQLite.
- No explicit pruning observed.

Current usage:

- Prevents previously cleared anomalies from continuing to block AA.

Research value:

- Medium.
- Useful for governance and operational-quality analysis.

Currently underused evidence:

- Anomaly burden over time.
- Whether cleared anomalies later recur.

### 11. Config / `.env`

Purpose:

Stores current operating parameters and Saxo credentials.

Available fields:

- Watchlist
- UIC mappings
- Dry-run / kill-switch state
- Risk limits
- Training mode setting
- Challenger thresholds and sizing settings
- Saxo credentials and tokens

Retention period:

- Current file only.
- Backed up by backup process, with restricted file permissions.

Current usage:

- Runtime settings.

Research value:

- High for reproducibility.
- Sensitive and should not be copied into GitHub raw.

Currently underused evidence:

- Non-secret setting snapshots could explain regime changes in research state.

Governance note:

- Secrets, tokens, account keys, and credentials must never enter `AA_Research`.

### 12. Backup Manifests

Purpose:

Recovery and integrity metadata.

Available fields:

- Backup timestamp
- Database backup path
- Integrity check
- Source database metadata
- Row counts by table
- Runner log backup metadata
- Environment backup metadata

Retention period:

- Hourly backups retain 48 by default.
- Daily bundles retain 14 by default.

Current usage:

- Recovery and verification.

Research value:

- Medium for data integrity.
- Low for direct trading analysis.

Currently underused evidence:

- Row-count growth rate by table.
- Evidence-collection continuity.

### 13. Legacy `signals` and `simulated_orders`

Purpose:

Earlier rule-engine / dry-run idea flow.

Available fields:

- Signal timestamps
- Symbol
- Side
- Entry
- Stop loss
- Take profit
- Reason
- Dry-run order status
- Fill / close / realized P/L fields

Retention period:

- Persisted in SQLite.

Current usage:

- Legacy dashboard sections and idea-quality functions.

Research value:

- Low for current AA production research unless explicitly marked legacy.

Governance note:

- Should not be mixed into production-quality AA metrics unless GM explicitly requests legacy-context analysis.

### 14. `historical_positions`

Purpose:

Imported Saxo historical positions.

Available fields:

- Record id
- Synced timestamp
- Account key
- Account id
- Symbol
- Asset type
- Description
- Open / close dates
- Amount
- Prices
- P/L
- Raw JSON

Retention period:

- Persisted in SQLite.

Current usage:

- Saxo history analysis.

Research value:

- Low for current AA production research.
- Sensitive due account identifiers and raw Saxo data.

Governance note:

- Do not publish raw rows to GitHub.

## 2. Computed Evidence That Exists During AA Operation

The following data exists inside AA's current process or modules but is not always preserved as first-class research rows.

### A. Admission Component Reasons

Where computed:

- `saxo_trader/challenger.py`
- `_entry_admission`

Examples:

- Momentum strength vs threshold
- Tick path consistency
- Spread quality
- Recent symbol P/L
- Similar theme already active
- Metals confirmation requirement

Current preservation:

- For admitted trades: `entry_score` and `entry_score_reasons` are stored in `challenger_positions`.
- For blocked signals: admission data is stored inside `blocked_signals.raw_metadata`.

Evidence gain:

- Flatten into score-component columns for admitted and blocked opportunities.

### B. Risk Officer Snapshot

Where computed:

- `saxo_trader/risk_officer.py`

Fields available in memory:

- Portfolio heat %
- Max loss if stops hit
- Daily P/L
- Daily loss remaining
- USD long / short exposure count
- Metals count
- Correlation warning
- Position risks

Current preservation:

- Not fully persisted as a dedicated table.
- Some effects appear in `aa_decisions.blockers`, `aa_journal.staff_advice`, and blocked reasons.

Evidence gain:

- Existing effects can be partially reconstructed from open positions and decision text.
- Full historical risk snapshots would require future persistence, which would be a separate authorization question.

### C. Portfolio Manager Snapshot

Where computed:

- `saxo_trader/portfolio_manager.py`

Fields available in memory:

- Currency exposure
- Concentration warnings
- Open-position count
- Reduction candidates
- Position distance to stop
- Unrealized P/L

Current preservation:

- Not fully persisted as a dedicated table.
- Some warnings appear in `aa_decisions`, `aa_journal`, and `blocked_signals.block_reason`.

Evidence gain:

- Partial reconstruction from open/closed positions and journal text.
- Full historical portfolio snapshots would require future persistence.

### D. Anomaly Snapshot

Where computed:

- `saxo_trader/anomaly_scanner.py`

Fields available in memory:

- Burst entry anomalies
- Burst exit anomalies
- Very short hold anomalies
- Planned-risk anomalies
- Repeated loss clusters
- Missing trade-path anomalies

Current preservation:

- Cleared anomalies are persisted in `anomaly_clearances`.
- Active anomaly snapshots are not persisted unless they influence `aa_decisions` blockers.

Evidence gain:

- Current and historical anomaly state can be partially reconstructed from positions/ticks.
- Full historical anomaly snapshots would require future persistence.

### E. Trade Review Derived Fields

Where computed:

- `saxo_trader/challenger_review.py`

Fields available:

- Planned risk
- Planned reward
- Planned R/R
- Exit move
- Ticks observed during trade
- Max favorable P/L
- Max adverse P/L
- Best price
- Worst price
- Review text
- Takeaway text

Current preservation:

- Some MFE / MAE / duration are stored on close.
- Full review text is generated for dashboard/reports, not stored as a table.

Evidence gain:

- Can be exported offline from existing data without changing AA behavior.

## 3. Ranked Evidence Sources

| Rank | Source | Learning Value | Implementation Effort | Governance Impact | Reason |
|---:|---|---|---|---|---|
| 1 | `aa_journal` | Very High | Low | Low | Already preserves symbol-level scout/no-entry/hold/entry/exit/data-unavailable decisions. Largest evidence-density gain. |
| 2 | `blocked_signals` | Very High | Low-Medium | Low | Contains blocked opportunity score, side, reason, and JSON admission metadata. Needs flattening, not behavior change. |
| 3 | `challenger_ticks` | Very High | Medium | Low | Enables blocked follow-through, MFE/MAE, spread, and quote-availability analysis from existing prices. |
| 4 | `challenger_positions` | Very High | Low | Low | Canonical admitted-trade lifecycle with rich learning tags. Already structured. |
| 5 | `challenger_trades` | High | Low | Low | Convenient closed-trade P/L and metadata source. Good for cross-checking positions. |
| 6 | `aa_decisions` | High | Low | Low | Captures operating-level clear vs blocked cycles and accepted staff vetoes. |
| 7 | `outputs/challenger_runner.log` | Medium-High | Medium | Low | Useful for data outages, symbol coverage, cycle continuity, and operational context. |
| 8 | `symbol_quarantine` | Medium | Low | Low | Helps explain post-stop suppression and repeated setup cooling. |
| 9 | `anomaly_clearances` plus reconstructed anomalies | Medium | Medium | Medium | Useful governance evidence, but active snapshots are not fully persisted. |
| 10 | Non-secret config snapshots | Medium | Medium | Medium | Important for reproducibility; must avoid secrets and account identifiers. |
| 11 | Backup manifests | Medium | Low | Low | Measures evidence continuity and data integrity rather than trading edge. |
| 12 | `signals` / `simulated_orders` | Low | Low | Low | Legacy idea flow, not canonical current AA production research. |
| 13 | `historical_positions` | Low | Medium | High | Sensitive and pre-AA/historical. Do not publish raw rows to GitHub. |

## 4. Maximum Evidence Density Without AA Behavior Change

Highest-yield repository extraction:

1. Normalize `aa_journal` into a decision-cycle / scout ledger.
2. Flatten `blocked_signals.raw_metadata` into an opportunity-decision ledger.
3. Use `challenger_ticks` to calculate follow-through MFE / MAE for blocked opportunities.
4. Export `challenger_positions` into production trade-history ledgers.
5. Join `aa_decisions` with `aa_journal` to identify cycle-level vetoes and staff blockers.
6. Parse `outputs/challenger_runner.log` into a data-quality timeline.

This would increase observable decision density without increasing trade count or changing AA behavior.

## 5. Evidence Currently Discarded Or Weakly Preserved

### Fully or Mostly Preserved But Not Surfaced

- No-entry scout decisions by symbol.
- Data-unavailable cycles by watchlist and error type.
- Blocked signal admission metadata.
- Entry-score reasons.
- Volatility snapshots.
- Tick paths around admitted trades.
- Tick paths after blocked signals.
- Staff-veto cycle decisions.
- Runner cycle continuity.

### Partially Preserved

- Risk officer snapshots.
- Portfolio manager snapshots.
- Anomaly scanner snapshots.
- Portfolio reduction candidate state.
- Full score component breakdown for admitted vs blocked opportunities.

### Not Reliably Preserved As Research Rows

- Full historical risk snapshot per cycle.
- Full historical portfolio exposure snapshot per cycle.
- Full active anomaly snapshot per cycle.
- Every quote-fetch failure by symbol beyond runner-log summaries.

Capturing the last group would require new persistence behavior and therefore should be treated as a separate governance question, not part of this inventory.

## 6. Repository Structures Best Suited To Recover Existing Evidence

Existing proposed structures remain suitable:

- `ledgers/decision_cycle_ledger.csv`
- `ledgers/opportunity_decision_ledger.csv`
- `ledgers/blocked_followthrough_ledger.csv`
- `observations/score_bucket_summary.md`
- `observations/pair_session_matrix.csv`
- `memory/evidence_gap_register.md`

Additional useful structure:

`observations/data_quality_timeline.csv`

Suggested fields:

```text
timestamp_utc,symbols_available_count,symbols_available,errors_count,errors,runner_status,data_available,notes
```

Purpose:

Separate true low-opportunity periods from data-feed outage periods.

## 7. Governance Classification

This inventory is an observation and repository-design artifact.

It does not create findings.

It does not promote hypotheses.

It does not recommend changing AA behavior.

It identifies recoverable evidence already created by AA's existing decision process.

## 8. Answer To GM Question

What information already exists inside AA today but is not preserved, structured, or surfaced for research?

Answer:

The largest existing evidence pool is AA's journaled decision stream, blocked-signal metadata, quote tick history, and lifecycle trade tags. Together, these already contain enough raw material to materially increase evidence density through offline extraction into research ledgers.

The maximum near-term evidence-density gain comes from recovering and structuring:

- Per-symbol scout/no-entry decisions from `aa_journal`
- Admission and block reasons from `blocked_signals.raw_metadata`
- Follow-through price paths from `challenger_ticks`
- Trade lifecycle metadata from `challenger_positions`
- Cycle-level staff vetoes from `aa_decisions`
- Data-feed health from `challenger_runner.log`

This is recoverable evidence, not new AA behavior.
