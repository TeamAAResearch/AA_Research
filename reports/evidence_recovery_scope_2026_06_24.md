# Evidence Recovery Scope

Date: 2026-06-24
Prepared by: Codex
Scope: Determine maximum recoverable evidence from existing records under current freeze
Authority: AA Organizational Charter v1.0

## Objective

Determine the maximum evidence that can be recovered from existing records without changing:

- AA behavior
- Strategy
- Thresholds
- Risk rules
- Portfolio rules
- Trade frequency
- Signal generation

Focus:

- Admitted vs blocked opportunities
- Risk-block outcomes
- Cycle veto outcomes
- Opportunity flow through the decision funnel
- Evidence trapped in logs, journals, and serialized metadata

## Current Priority Source Counts

Observed local SQLite counts at review time:

| Source | Total Rows | Post-Baseline Rows |
|---|---:|---:|
| `blocked_signals` | 350 | 299 |
| `aa_journal` | 99,630 | 4,936 |
| `aa_decisions` | 593 | 367 |
| `challenger_ticks` | 11,674 | 3,984 |
| `challenger_positions` | 145 | 42 |

Official baseline:

2026-06-22 07:02:25 UTC

## 1. Maximum Recoverable Evidence By Source

### A. `blocked_signals`

Recoverable evidence:

- Blocked opportunity timestamp
- Symbol
- Asset class by symbol inference
- Side
- Signal score
- Block reason
- Block stage by reason parsing
- Admission score
- Required score
- Admission reasons
- Momentum threshold
- Tick count at signal
- Entry reference price
- Planned risk, stop loss, quantity, and cap where present in metadata
- Boundary vs material risk block where risk fields exist

Research questions enabled:

- Did blocked opportunities score worse than admitted opportunities?
- Which gate blocked each opportunity?
- Are risk blocks boundary or material?
- Which pairs/sessions produce the most blocked flow?
- Are metals dominating blocked opportunity flow?

Limitation:

- Session is not directly stored in `blocked_signals`; it can be inferred from timestamp.
- Some block-stage classification requires parsing unstructured `block_reason`.
- Follow-through requires joining to later `challenger_ticks`.

### B. `aa_journal`

Recoverable evidence:

- Cycle-level and symbol-level activity
- `NO_ENTRY` decisions by symbol
- `DATA_UNAVAILABLE` cycles
- `BLOCKED_SIGNAL` records
- `CYCLE_PAUSED` records
- `BLOCK_NEW_ENTRIES` records
- Entry actions
- Hold actions
- Exit actions
- Staff advice text
- AA reason text
- Outcome snapshots containing operating action, current price, unrealized P/L, entry details, stop, target, score, session, and sample type depending on action

Research questions enabled:

- How many symbols were scouted but produced no entry?
- Was low trade count caused by no signal, open position, staff veto, data outage, or actual block?
- How often did each pair disappear before becoming a scored opportunity?
- How many cycles were untradeable because data was unavailable?
- How often did AA hold vs exit vs scout?

Limitation:

- Some fields are embedded in text.
- Requires parsing `aa_reason` and `outcome_snapshot`.
- Does not always include numerical score unless event is entry or blocked signal.

### C. `aa_decisions`

Recoverable evidence:

- Cycle-level operating decision
- Clear-to-scout vs block-new-entries
- Accepted staff vetoes
- Overrides
- Blockers

Research questions enabled:

- How often was the entire cycle blocked before symbol-level scoring?
- Which staff or gate caused cycle-level vetoes?
- Were opportunity gaps caused by global operating gates rather than symbol-level weakness?

Limitation:

- Full nested risk, portfolio, downside, and anomaly snapshots are not persisted.
- Does not list symbols affected by cycle veto except via matching `aa_journal` entries around the same timestamp.

### D. `challenger_ticks`

Recoverable evidence:

- Bid
- Ask
- Mid
- Symbol
- UIC
- Asset type
- Timestamp
- Price path after admitted or blocked opportunity
- Spread at observed tick
- Quote availability by symbol and time

Research questions enabled:

- What was MFE / MAE after a blocked opportunity?
- Did risk blocks protect AA or suppress edge?
- Did admission blocks avoid weak trades?
- Were data outages symbol-specific or system-wide?
- Was spread materially different for admitted vs blocked opportunities?

Limitation:

- Tick cadence follows AA runner cycle, not high-frequency market data.
- For blocked follow-through, expected outcome must be modeled under fixed lookahead or AA exit-framework assumptions.
- Does not capture prices for symbols that failed quote fetch.

### E. `challenger_positions`

Recoverable evidence:

- Admitted trade timestamp
- Closed trade timestamp
- Symbol
- Asset class
- Side
- Quantity
- Entry
- Stop
- Target
- Exit
- P/L
- Status
- Entry reason
- Close reason
- Session
- Spread
- Entry score
- Entry score reasons
- Volatility regime
- Volatility snapshot
- Signal reason
- Exit reason
- Time in trade
- MFE
- MAE
- Realized P/L
- Sample type

Research questions enabled:

- How do admitted trades compare with blocked opportunities?
- Which score buckets produce expectancy?
- Which sessions, sides, and pairs produce realized value?
- Does duration explain losses?
- Does MFE convert to realized P/L?

Limitation:

- Contains admitted opportunities only.
- Requires comparison to `blocked_signals` and `aa_journal` to understand opportunity loss.

## 2. Recoverable Evidence Products

### 1. Unified Opportunity Decision Ledger

Sources:

- `blocked_signals`
- `challenger_positions`

Purpose:

Create one comparable view of admitted and blocked opportunities.

Recoverable fields:

- Timestamp
- Symbol
- Asset class
- Session
- Side
- Decision: admitted / blocked
- Block stage
- Block reason
- Admission score
- Required score
- Score bucket
- Entry reference price
- Sample type where applicable
- Source table
- Source id

Value:

High.

Effort:

Low-Medium.

Governance impact:

Low, if performed as offline extraction only.

### 2. Scout / No-Entry Ledger

Sources:

- `aa_journal`

Purpose:

Recover opportunity disappearance before scoring.

Recoverable fields:

- Timestamp
- Symbol
- Action
- Reason
- Operating action
- Session by timestamp
- Data available / unavailable

Value:

Very High.

Effort:

Low-Medium.

Governance impact:

Low.

### 3. Cycle Veto Ledger

Sources:

- `aa_decisions`
- `aa_journal`

Purpose:

Recover cycle-level suppression caused by staff/gates.

Recoverable fields:

- Timestamp
- Action
- Accepted staff
- Blocker text
- Symbols affected via nearby journal rows
- Duration until next `CLEAR_TO_SCOUT`

Value:

High.

Effort:

Medium.

Governance impact:

Low.

### 4. Blocked Follow-Through Ledger

Sources:

- `blocked_signals`
- `challenger_ticks`

Purpose:

Evaluate blocked opportunities without binary win/loss framing.

Recoverable fields:

- Blocked timestamp
- Symbol
- Side
- Reference entry price
- Lookahead window
- MFE
- MAE
- Spread-adjusted MFE
- Spread-adjusted MAE
- Expected outcome under AA's actual exit framework, where reconstructable

Value:

Very High.

Effort:

Medium-High.

Governance impact:

Medium, because methodology choices affect interpretation.

### 5. Data Quality Timeline

Sources:

- `aa_journal`
- `outputs/challenger_runner.log`
- `challenger_ticks`

Purpose:

Separate true opportunity starvation from feed failure.

Recoverable fields:

- Timestamp
- Symbols available
- Symbol count
- Error types
- Data unavailable flag
- Runner status
- Feed condition

Value:

High.

Effort:

Medium.

Governance impact:

Low.

### 6. Admitted Trade Quality Ledger

Sources:

- `challenger_positions`
- `challenger_ticks`

Purpose:

Normalize admitted trade lifecycle data for comparison with blocked opportunities.

Recoverable fields:

- Entry metadata
- Score
- Score reasons
- Volatility
- Spread
- MFE
- MAE
- Realized P/L
- Duration
- Exit reason
- Capture efficiency

Value:

High.

Effort:

Low.

Governance impact:

Low.

## 3. Decision Funnel Visibility From Existing Records

### Funnel Stage 1: Market / Data Availability

Recoverable from:

- `aa_journal.DATA_UNAVAILABLE`
- `outputs/challenger_runner.log`
- `challenger_ticks`

Visibility:

Partial to high.

### Funnel Stage 2: Symbol Scouted

Recoverable from:

- `aa_journal.NO_ENTRY`
- `aa_journal.BLOCKED_SIGNAL`
- `aa_journal.OPEN_BUY`
- `aa_journal.OPEN_SELL`

Visibility:

High.

### Funnel Stage 3: Momentum Signal Generated

Recoverable from:

- `blocked_signals`
- `challenger_positions`
- Some `aa_journal.BLOCKED_SIGNAL`

Visibility:

High for scored opportunities.

Limited for near-miss momentum that never crossed signal threshold.

### Funnel Stage 4: Admission Decision

Recoverable from:

- `blocked_signals.raw_metadata`
- `challenger_positions.entry_score`
- `challenger_positions.entry_score_reasons`

Visibility:

High.

### Funnel Stage 5: Risk Decision

Recoverable from:

- `blocked_signals.block_reason`
- `blocked_signals.raw_metadata`
- `challenger_positions.stop_loss`
- `challenger_positions.quantity`
- `aa_decisions.blockers`

Visibility:

Medium to high.

### Funnel Stage 6: Portfolio Decision

Recoverable from:

- `blocked_signals.block_reason`
- `aa_decisions.accepted_staff`
- `aa_decisions.blockers`
- Open positions around timestamp, approximated from `challenger_positions`

Visibility:

Medium.

### Funnel Stage 7: Execution / Open Trade

Recoverable from:

- `challenger_positions`
- `aa_journal.OPEN_BUY`
- `aa_journal.OPEN_SELL`

Visibility:

High.

### Funnel Stage 8: Management / Exit

Recoverable from:

- `aa_journal.HOLD_POSITION`
- `aa_journal.CLOSE_POSITION`
- `challenger_positions`
- `challenger_ticks`

Visibility:

High.

## 4. Ranking By Learning Value, Effort, Governance Impact

| Rank | Evidence Product | Learning Value | Effort | Governance Impact | Why |
|---:|---|---|---|---|---|
| 1 | Unified Opportunity Decision Ledger | Very High | Low-Medium | Low | Directly compares admitted vs blocked opportunities. |
| 2 | Scout / No-Entry Ledger | Very High | Low-Medium | Low | Reveals where opportunities disappear before scoring. |
| 3 | Blocked Follow-Through Ledger | Very High | Medium-High | Medium | Tests whether blocks protected or suppressed AA. |
| 4 | Admitted Trade Quality Ledger | High | Low | Low | Normalizes existing trade lifecycle evidence. |
| 5 | Data Quality Timeline | High | Medium | Low | Prevents feed outages from being misread as strategy inactivity. |
| 6 | Cycle Veto Ledger | High | Medium | Low | Explains whole-cycle suppression from staff/gates. |

## 5. Governance Boundary

This report supports Evidence Recovery only.

It does not authorize:

- More trades
- More risk
- Strategy changes
- Threshold changes
- Risk changes
- Portfolio changes
- Trade-frequency changes
- AA behavior changes

This report does not create findings.

This report records recoverable evidence paths.

## 6. Answer To GM Task

Maximum evidence recoverable under the current freeze:

- Up to 299 post-baseline blocked opportunity records from `blocked_signals`.
- Up to 4,936 post-baseline AA journal records describing scout, no-entry, blocked, entry, hold, exit, cycle-pause, and data-unavailable events.
- Up to 367 post-baseline AA operating decisions from `aa_decisions`.
- Up to 3,984 post-baseline tick records from `challenger_ticks`.
- Up to 42 post-baseline challenger position records from `challenger_positions`.

The most valuable next repository-level evidence recovery is to convert these existing records into structured research ledgers, starting with:

1. Unified Opportunity Decision Ledger
2. Scout / No-Entry Ledger
3. Blocked Follow-Through Ledger

This increases visibility into AA's existing decision process without changing AA.
