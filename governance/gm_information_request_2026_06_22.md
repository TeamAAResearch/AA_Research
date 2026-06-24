# AA Project — GM Information Request
**Date:** 2026-06-22
**Purpose:** Documentation to support independent governance review.

---

## 1. Trading Pipeline
**Sequence:** Market Scan ➔ Signal Generation ➔ Governance Filter ➔ Portfolio Filter ➔ Risk Filter ➔ Admission Scoring ➔ Execution.

*   **Signal:** The initial identification of a directional market opportunity (momentum/mean-reversion).
*   **Governance Filter:** Checks for manual quarantine, macro intervention overrides, or prohibited symbols.
*   **Portfolio Filter:** Evaluates concentration limits (e.g., USD-cluster limits, maximum active positions per asset class).
*   **Risk Filter:** Evaluates account margin, maximum drawdown constraints, and individual trade risk caps (e.g., $250 maximum risk).
*   **Admission Scoring:** The ML-driven confidence gate. FX requires a score of 70; Metals require a score of 85.
*   **Execution:** Final routing to the broker API. Can be rejected by system "kill switches" or broker-side failures.

---

## 2. FX Opportunity Ledger
**Schema:** `[Pair | Timestamp (UTC) | Session | Terminal Outcome | Block Stage | Primary Culprit]`

**Baseline:** `2026-06-22 07:02:25 UTC` (Clean restart / production-quality collection start)
**Sample Entries:**
*   `2026-06-22 07:32:34 | GBPUSD | London | Blocked | 4. Risk Block | Planned risk cap exceeded`
*   `2026-06-22 07:37:36 | GBPJPY | London | Admitted | N/A | N/A`

**Current Cumulative Counts (Post-Baseline):**
*   **Opportunities observed:** 3
*   **Opportunities admitted:** 1
*   **Opportunities blocked:** 2
*   **Executed trades:** 1
*   **Open trades:** 0

---

## 3. Opportunity Loss Attribution
For every blocked opportunity, the classification is purely data-driven based on the database `block_reason`:
*   **Governance Block:** Blocked by `quarantine` or `intervention` flags. (Owner: Sofia / Governance)
*   **Portfolio Block:** Blocked by `cluster limit` or `exposure` caps. (Owner: Clara / Portfolio)
*   **Risk Block:** Blocked by `risk cap` or `margin` limits. (Owner: Mason / Risk Controls)
*   **Admission Block:** Blocked by `admission score` failure. (Owner: Ari / Trader)
*   **Execution Block:** Blocked by `kill switch` or routing failure. (Owner: Theo / Infrastructure)

---

## 4. AA Decision Journal
The system logs structured data for all decisions:
*   **Enters:** Logs `entry_score`, `entry_score_reasons`, `volatility_regime`, `spread_pct_at_entry`.
*   **Exits:** Logs `exit_reason` (e.g., "AA day-trader trailing protection exit: protect open profit"), `realized_pnl`, `mfe`, `mae`.
*   **Rejects (Blocks):** Logs the exact `block_reason` string (e.g., "Currency cluster gate: Long USD exposure at limit").

---

## 5. Team Deliverables
*   **Iris (Market Coverage):** Daily tracking of raw signals generated per session (Outputs: Volume charts).
*   **Clara & Mason (Gates):** Daily tracking of pipeline attrition at Stages 3 & 4.
*   **Ari (Trader):** Daily tracking of Stage 5 score performance and actual traded portfolio composition.
*   **Rowan (Research):** Daily compilation of the FX Opportunity Ledger.
*   **Theo (Infrastructure):** Continuous heartbeat and DB integrity monitoring.
*   **Helena (Standard):** Enforces that all deliverables adhere to the Observation/Explanation/Confidence/Evidence framework.

---

## 6. Research Success Criteria
The project concludes the Data Collection phase when statistically significant evidence proves:
1.  **AA has no viable edge:** Admitted FX trades consistently produce negative expectancy over a large sample, or AA fundamentally cannot generate FX flow.
2.  **AA has a viable edge:** Admitted FX trades produce positive expectancy outperforming a random walk over a large sample.
3.  **AA is ready to advance:** If positive expectancy is proven, the system moves from Observation to Optimization/Scaling.

---

## 7. Current Open Questions
1.  Can AA generate enough FX opportunity flow after the clean restart to build a statistically meaningful FX dataset?
2.  Is the Risk Block (Stage 4) consistently the dominant FX bottleneck, or was the current sample of 3 trades noise?
3.  Does FX flow reliably increase during the London/US overlap compared to the Asia session?

---

## 8. Current Metrics Dashboard (Post-Baseline Only)
*Sample Size: 3 Opportunities*
*   **Win Rate:** 100% (1 trade, 1 win)
*   **Opportunity Conversion Rate:** 33.3% (1 admitted / 3 observed)
*   **Risk Rejection Rate:** 66.6% (2 blocked at Risk / 3 observed)
*   **Portfolio Rejection Rate:** 0.0%
*   **Average Opportunity Value (Realized):** +$14.06
*   **MFE / MAE Statistics:** MFE: $22.26 | MAE: -$12.65
*   **Session Breakdown:** London: 100% | Asia: 0%
*   **Pair Breakdown:** GBPUSD: 2 (Blocked) | GBPJPY: 1 (Admitted)

---

## 9. Constraints
The following constraints are actively enforced and remain strictly unchanged until 29 June:
*   **Code:** Frozen.
*   **Strategy:** Frozen.
*   **Thresholds:** Frozen (FX=70, Metals=85).
*   **Risk:** Frozen.
*   **Portfolio Construction:** Frozen.

---

## 10. Governance
*   **Ledger:** Owned by Research (Antigravity).
*   **Metrics:** Owned by Research (Antigravity).
*   **Opportunity classification:** Owned by Database integrity/logs (Objective truth).
*   **Promotion decisions:** Owned by algorithmic logic (Zero manual intervention).
*   **Research conclusions:** Governed by Helena (Requires the 4-pillar evidence standard), delivered to the GM.
