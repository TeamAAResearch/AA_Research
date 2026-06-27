# Directive for Codex: Trade Frequency Code Investigation
**Date:** 2026-06-26
**From:** Antigravity (AG - Research & Strategy)
**To:** Codex (Engineering)
**CC:** GM

## The Problem
Ari's trade frequency has dropped to near zero since the Metals momentum threshold normalization (0 trades in the last 6 hours). 

AG hypothesized that this is entirely due to the strict `challenger.py` admission gates (e.g., FX requiring 70/100, Metals requiring 85/100), as evidenced by the 27 blocked signals in the SQLite database.

However, the GM has correctly challenged this as an unverified hypothesis. The drop in frequency might be caused by a deeper structural issue in the codebase itself.

## Codex Investigation Mandate
Codex is directed to perform a deep-dive engineering audit of Ari's trading loop to identify any structural bottlenecks suppressing trade frequency. 

Please investigate the following areas:
1. **Signal Generation (`spotter.py`):** Is the momentum calculation or lookback window structured in a way that artificially suppresses signals during normal market conditions?
2. **Admission Logic (`challenger.py`):** Are the scoring criteria (e.g., paper performance modifiers, spread checks, trend alignment) mathematically too harsh? Are there hidden short-circuits blocking trades before they even reach the database?
3. **Risk Caps (`risk_manager.py` / models):** Are risk caps or portfolio exposure limits silently suppressing entries?
4. **Execution Loop (`challenger_runner.py`):** Is the runner polling interval or data consumption logic lagging, causing Ari to miss the momentum window entirely?

## Deliverable
Do not write any code changes yet. First, provide an engineering report to the GM and AG detailing the exact code paths that are currently choking the trade frequency, and present technical options for safely increasing the velocity of the system.
