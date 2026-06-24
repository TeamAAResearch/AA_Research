# Evidence Review Program

**Owner:** AG (Chief Research Analyst / Observation Pipeline Owner)
**Status:** Active
**Date:** 2026-06-24

---

## 1. Evidence Inventory Summary

The organization possesses a deep backlog of unreviewed evidence across the following data stores:

* **`aa_journal`**: 2,866 raw decision entries detailing AA's internal evaluations, scores, and confidence levels.
* **`blocked_signals`**: 2,674 entries where AA's intended decisions were blocked by governance, risk, or portfolio thresholds.
* **`challenger_positions`**: Snapshot of currently active or recently managed positions.
* **`challenger_trades`**: The final realized outcome (P/L, duration) of executed trades.
* **`aa_decisions`**: The action log matching signals to execution or rejection.
* **`challenger_ticks`**: 395,000+ tick events providing high-resolution market context during evaluations.
* **Recovered Ledgers**:
  * `opportunity_funnel.csv`: Extracted funnel metrics (79,000+ total rows, 2,866 valid journal entries, 2,674 blocked signals).
  * `cycle_vetoes.csv`: Detailed breakdowns of which vetoes blocked which decisions.
  * `opportunity_funnel_simulated.csv`: Shadow risk engine outcomes providing counterfactual paths for blocked signals.

## 2. Review Prioritization

The review is structured sequentially to isolate variables, starting with the admission gates where the majority of data drops occur, moving towards realized performance.

* **Phase 1: Admission Funnel** (Highest Priority)
  * *Why:* The funnel drops from 79,000+ loops to 2,866 evaluations to 192 executed trades. Understanding this loss rate is critical.
* **Phase 2: Risk Blocks**
  * *Why:* "No_Risk_Brackets" blocked thousands of trades. The Shadow Risk Engine has opened this data for review.
* **Phase 3: Portfolio Blocks**
  * *Why:* Evaluates whether the concentration limits and correlation blockers are preventing good trades or saving the portfolio from ruin.
* **Phase 4: Score Distribution**
  * *Why:* AA generates confidence scores. We need to determine if high scores actually correlate with positive expectancy.
* **Phase 5: Duration Analysis**
  * *Why:* Analyzes hold times, stale signals, and whether the time-in-trade aligns with the original hypothesis.
* **Phase 6: Pair / Symbol Analysis**
  * *Why:* Identify if AA has specific blind spots or strengths in certain currencies or asset classes.
* **Phase 7: Side Analysis**
  * *Why:* Determine if there is a directional bias (Long vs. Short) in AA's performance or blocked signals.

## 3. Deliverables

For each phase, the following deliverables must be produced:

* **Objective:** The core question the phase attempts to answer.
* **Data Sources:** Explicit listing of the tables or ledgers used.
* **Expected Output:** A qualitative synthesis of the data.
* **Observation Format:** Documented strictly as an "Observation" (What the data says) and optionally a "Hypothesis" (What it might mean), conforming to the Observation Pipeline workflow. No findings or rule changes can be embedded in these deliverables.

## 4. Completion Criteria

A review phase is considered **Complete** when:
1. The specified data sources have been fully analyzed.
2. A formalized Observation Report has been submitted to the GM.
3. The GM has reviewed and approved the Observations.
4. (Optional) Any approved Hypotheses have been moved to Contradiction Testing.

## 5. Backlog Estimate

The current backlog is substantial and represents the organization's primary constraint. 

* **Total Records to Evaluate:** ~5,500 significant decision points (2,866 journal entries + 2,674 blocked signals), plus their corresponding tick and execution data.
* **Estimated Effort:** 
  * Phases 1 & 2 represent the largest conceptual lift, expected to require multiple review cycles.
  * Phases 3-7 are narrower and more analytical.
* **Timeline:** The full program is expected to drive the organization's research agenda for the immediate future. No new pipelines or evidence generation tools are necessary until this backlog is exhausted.

---

> [!IMPORTANT]
> **Operating Constraint:** The purpose of this program is strictly to review existing evidence. It does **not** authorize building new tools, creating new pipelines, developing Shadow AA, proposing immediate strategy changes, or altering risk parameters. "Evidence owns the organization."
