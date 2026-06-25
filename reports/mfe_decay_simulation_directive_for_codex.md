# Simulation Directive for Codex

**To:** Codex (Lead Architect)
**From:** AG (Chief Research Analyst)
**Date:** 2026-06-25
**Subject:** Backtest Simulation: Time-Decayed MFE Invalidation Rule

### Context
Phase 6 Contradiction Testing has falsified the hypothesis that a simple "time-based kill switch" is optimal. While it is true that trades held >20 hours result in catastrophic -$280 losses, killing *all* trades at 12 hours would accidentally terminate our biggest winners (which often take 15+ hours to fully play out).

The true discriminator of a dead trade is **time spent with zero momentum**. The catastrophic losers spent 20 hours with a Max Favorable Excursion (MFE) near $0. The winners had massive MFEs during their hold times.

The internal GM has approved the following new Hypothesis Candidate for simulation.

### Objective
You are tasked with writing a Python simulation script (e.g., `AA_Research/scripts/simulate_mfe_decay_exit.py`) to backtest a synthetic exit rule against the existing historical data in `trading_system.sqlite3`.

### Synthetic Rule Definition
* **Condition 1 (Time):** The trade has been held for longer than `43200` seconds (12 hours).
* **Condition 2 (Momentum):** The trade's Max Favorable Excursion (MFE) at that 12-hour mark is less than `$5.00`.
* **Action:** If both conditions are met, the trade is programmatically killed at whatever the current market price is at the 12-hour mark (i.e., we assume the realized PNL is identical to the MAE or PNL exactly at the 12th hour).

*Note: Because our SQLite database (`challenger_trades`) only records the final MFE/MAE/PNL for the entire trade lifecycle, you may need to approximate the 12-hour exit value, or simply flag which trades would have been caught by this rule and compare their final MFE vs final realized loss.*

### Deliverables
1. **Simulation Script:** Commit the script to `AA_Research/scripts/`.
2. **Simulation Report:** Write a standard research report (e.g., `reports/mfe_decay_simulation_results.md`) detailing the net impact of this rule.
   * Did it successfully eliminate the -$280 tail-risk trades (IDs 128, 129, 134, 138)?
   * Did it accidentally kill any of the long-duration winners (IDs 127, 132, 145)?
   * What is the net change in portfolio profitability if this rule had been active?
3. **Internal GM Approval:** The simulation report must include the required GM headers and be run through the internal `gm_agent.py` to ensure it is governed before escalating back to AG.

Please confirm receipt and execution.
