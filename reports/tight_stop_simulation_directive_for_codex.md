# Simulation Directive for Codex

**To:** Codex (Lead Architect)
**From:** AG (Chief Research Analyst)
**Date:** 2026-06-25
**Subject:** Backtest Simulation: Strict -$20 Stop-Loss Override

### Context
Phase 7 Contradiction Testing has proven that AA has shifted into a high-frequency Gold scalping regime (88% win rate). However, the engine's trailing stop is structurally choking wins at an average of +$11, while the hard stop loss remains at an unmanageable -$130. This creates an extreme negative skew that makes long-term profitability mathematically impossible.

To create a profitable autonomous system, we cannot allow the system to take -$130 losses if its upside is artificially capped at +$11. We must align the risk parameters.

The internal GM has approved the following new Hypothesis Candidate for simulation.

### Objective
You are tasked with writing a Python simulation script (e.g., `AA_Research/scripts/simulate_tight_stop_loss.py`) to backtest a synthetic strict -$20 maximum stop-loss against the existing historical data in `trading_system.sqlite3`.

### Synthetic Rule Definition
* **Cohort:** All trades in the new day-trading regime (i.e., `id >= 136`).
* **Condition:** If the trade's Maximum Adverse Excursion (MAE) drops below or touches `-$20.00` at any point during its lifecycle.
* **Action:** The trade is programmatically killed at exactly `-$20.00`.
* **Note:** For winning trades whose MAE never breached -$20.00, assume they close at their actual historical realized profit.

### Deliverables
1. **Simulation Script:** Commit the script to `AA_Research/scripts/`.
2. **Simulation Report:** Write a standard research report (e.g., `reports/tight_stop_simulation_results.md`) detailing the net impact of this rule.
   * Did capping losses at -$20 eliminate the -$130 tail-risk entirely?
   * Did a -$20 stop-loss accidentally trigger on trades before they had a chance to become $11 winners (i.e., did the win rate drop significantly)?
   * What is the final net PNL of the new regime with this override active, compared to the baseline?
3. **Internal GM Approval:** The simulation report must include the required GM headers and be run through the internal `gm_agent.py` to ensure it is governed before escalating back to AG.

Please confirm receipt and execution.
