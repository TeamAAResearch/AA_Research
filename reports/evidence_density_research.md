# Evidence Density Research Report

**Scope:** AG
**Objective:** Increase evidence density without altering AA trading behavior.

## Evidence (Current Funnel Map)

The current decision funnel in `challenger.py` and `storage.py` operates as follows:
1. **Opportunities Generated:** AA scans liquid FX pairs. If momentum threshold is missed, the opportunity is discarded (not logged, only ticks remain).
2. **Cycle Vetoes (Portfolio/Staff Rejects):** If the Portfolio Manager, Risk Officer, or Downside Limit triggers a cycle-wide veto, no individual symbols are scored. This is logged only as unstructured text in the `aa_journal` table (action="BLOCK_NEW_ENTRIES").
3. **Opportunities Scored:** If momentum is found, `_signal_score` evaluates the setup.
4. **Admission Rejects:** If score is too low (< 70), or cluster/quarantine caps hit, it is blocked. Logged to `blocked_signals` table with a JSON blob in `raw_metadata`.
5. **Risk Rejects:** If planned risk exceeds budget, it is blocked. Logged to `blocked_signals` table.
6. **Executed Trades:** Fully logged to `challenger_positions` table with rich metadata (`session`, `spread`, `volatility_regime`, `entry_score`).

## Interpretation (What is Discarded vs. Trapped)

**Discarded Data:**
*   Zero-momentum opportunities are completely discarded. We do not know how many pairs were scouted and passed over gracefully versus scouted and actively blocked.

**Trapped Data (Hard to Analyze):**
*   **Admitted vs. Blocked Asymmetry:** Executed trades get clean columns in `challenger_positions` (like `entry_score`, `session`). Blocked trades dump this exact same data into a serialized JSON string (`raw_metadata`) in `blocked_signals`. This prevents SQL-level comparative analysis between high-score rejects and low-score admissions.
*   **Cycle Blocks:** When Portfolio limits block trading, we don't know *which* pairs would have fired, effectively obscuring the opportunity cost of portfolio risk caps.

## Hypothesis Candidates
*   **Hypothesis 1:** Extracting and flattening the `raw_metadata` from `blocked_signals` into a unified ledger will reveal that risk-blocked trades have a higher expected MFE than admitted trades.
*   **Hypothesis 2:** Parsing the `aa_journal` for cycle vetoes will show that portfolio balance limits suppress highly profitable FX flow during optimal sessions.

## Contradiction Tests
*   (For H1) Once the unified ledger is built, back-simulate the MFE/MAE of risk-blocked signals using historical tick data. If risk-blocked signals underperform admitted signals, H1 is contradicted, proving risk gates protect capital.

## Open Questions
*   How can we back-simulate the outcome (MFE/MAE) of blocked signals since AA did not execute them, without altering AA's live code?

**GM Review Required**
