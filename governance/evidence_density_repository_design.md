# Repository Design Proposal: Evidence Density

**Scope:** Codex
**Objective:** Structure the repository to support comparative opportunity analysis without altering AA source code or trading logic.

## Proposed Repository Additions

To capture trapped data from AA's existing SQLite database and fulfill the GM's analytical requirements, Codex proposes adding two new flattened, auto-generated ledgers to the `ledgers/` directory.

### 1. `ledgers/opportunity_ledger.csv`
**Purpose:** A unified, flattened view of *every* scored opportunity, seamlessly merging `challenger_positions` (Admitted) and `blocked_signals` (Rejected).
**Method:** An offline script (run outside of AA's trading loop) will parse the `raw_metadata` JSON from `blocked_signals` and append it alongside executed positions.

**Proposed Columns:**
*   `timestamp`
*   `symbol`
*   `side`
*   `decision` (Admitted, Blocked_Admission, Blocked_Risk)
*   `block_reason` (Null if Admitted)
*   `score` (Extracted from JSON for blocked, from `entry_score` for admitted)
*   `session` (Extracted from JSON for blocked)
*   `planned_risk`
*   `simulated_mfe` (To be calculated post-hoc by a standalone script)

### 2. `ledgers/cycle_veto_ledger.csv`
**Purpose:** Quantify how often Staff (Portfolio Manager, Risk Officer) veto entire cycles, suppressing all opportunity generation.
**Method:** An offline script will parse the `aa_journal` table for `BLOCK_NEW_ENTRIES`.

**Proposed Columns:**
*   `timestamp`
*   `veto_agent` (Risk Officer, Portfolio Manager, Downside Limit, Anomaly Scanner)
*   `veto_duration_minutes` (Time until next CLEAR_TO_SCOUT)

## Implementation Constraint Checklist
* [x] No code changes to `saxo_trader/challenger.py`.
* [x] No changes to admission thresholds or risk limits.
* [x] Only involves standalone scripts reading the existing `.db` file and outputting to `AA_Research/ledgers/`.

**GM Review Required**
