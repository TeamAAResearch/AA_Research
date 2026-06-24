# AA Data Source Inventory & Evidence Density Roadmap

**Scope:** AG
**Objective:** Identify existing AA data sources that can increase evidence density without altering trading behavior, strategy, or code.

---

## 1. Inventory of Existing Data Sources

AA currently records data across 12 distinct SQLite tables in its `TradeStore`. The following sources contain high-value, unstructured, or isolated data that is not currently surfaced for comparative research.

### Source A: `blocked_signals` (The JSON Metadata Blob)
*   **Available fields:** `symbol`, `side`, `signal_score`, `block_reason`, and notably `raw_metadata` (a JSON string containing `entry_price`, `planned_risk`, `max_allowed_risk`, `momentum_threshold_pct`, and the full `admission` dict).
*   **Retention period:** Permanent (SQLite append-only).
*   **Current usage:** Auditing individual rejected trades. Currently discarded from quantitative analysis because the features are trapped inside the `raw_metadata` string.
*   **Research value:** Very High. This is the missing half of the opportunity funnel. Flattening this JSON allows direct side-by-side comparison with executed trades (e.g., comparing the predictive power of `signal_score` on blocked vs. admitted trades).

### Source B: `aa_decisions` & `aa_journal` (The Text Logs)
*   **Available fields:** `action`, `conclusion`, `blockers`, `staff_advice`, `aa_reason`, `outcome_snapshot`.
*   **Retention period:** Permanent (SQLite append-only).
*   **Current usage:** Diagnostic logging to trace why the AA autonomous loop paused or scouted.
*   **Research value:** High. Currently, cycle-wide vetoes (e.g., Portfolio Manager blocks all entries due to concentration) are logged as unstructured text. Parsing these logs allows us to quantify the exact opportunity cost of our hard risk and portfolio gates.

### Source C: `challenger_ticks`
*   **Available fields:** `symbol`, `bid`, `ask`, `mid`, `created_at`.
*   **Retention period:** Permanent (SQLite append-only).
*   **Current usage:** Driving real-time momentum thresholds and `_signal_score` generation.
*   **Research value:** High. This is the raw material needed to calculate the hypothetical Maximum Favorable Excursion (MFE) and Maximum Adverse Excursion (MAE) of the `blocked_signals`.

### Source D: `simulated_orders` / `signals`
*   **Available fields:** `quantity`, `entry`, `stop_loss`, `take_profit`, `dry_run`, `blocked`.
*   **Retention period:** Permanent (SQLite append-only).
*   **Current usage:** Legacy or parallel idea generation storage.
*   **Research value:** Low to Medium. Appears mostly redundant to the active `challenger_positions` and `blocked_signals` tables, but could serve as a cross-reference for system integrity.

---

## 2. Evidence Source Ranking

Ranked by maximum yield to the organization under the current Governance Freeze.

### Rank 1: Flattening `blocked_signals.raw_metadata`
*   **Learning Value:** High (Enables Admitted vs. Blocked statistical comparison).
*   **Implementation Effort:** Low (Requires a simple offline Python/SQL script to extract JSON keys into columns; no AA code changes).
*   **Governance Impact:** Zero (Read-only extraction).

### Rank 2: Post-Hoc Simulation of Blocked Signals using `challenger_ticks`
*   **Learning Value:** Critical (Answers the core question: Do risk blocks protect AA or suppress edge?).
*   **Implementation Effort:** High (Requires building an offline script that walks forward the `challenger_ticks` starting from the timestamp of a `blocked_signal` to simulate if it would have hit its stop-loss or take-profit).
*   **Governance Impact:** Zero (Strictly offline simulation).

### Rank 3: Categorizing Vetoes from `aa_journal`
*   **Learning Value:** Medium (Reveals systemic opportunity suppression by staff agents).
*   **Implementation Effort:** Medium (Requires text-parsing or NLP classification of the `aa_reason` and `staff_advice` columns).
*   **Governance Impact:** Zero (Read-only extraction).

---

## Interpretation

The maximum achievable increase in evidence density comes from linking **Rank 1** and **Rank 2**. AA is already scoring and pricing rejected trades, and saving the exact ticks that follow them. By writing an offline script to simulate the outcome of those blocked trades, we can definitively prove whether the hard risk gates are generating alpha (by stopping losers) or suppressing edge (by blocking winners).

**GM Review Required**
