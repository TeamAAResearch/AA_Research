# Directive: Architectural Baseline & Assumptions Map
**Date:** 2026-06-26
**To:** Codex (Engineering)
**From:** AG (Research)

The GM has requested a comprehensive summary of how Ari and the scaffolded team are currently built, including all embedded assumptions. This is required to plan the next phase of optimization. 

Please perform a codebase audit and generate a new artifact: `AA_Research/reports/architectural_baseline_and_assumptions.md`. 

The report must include:

## 1. Architectural Flow
Map the exact journey of a signal from inception to exit. 
*   **Stage 1: Polling** (`challenger_runner.py` / `heartbeat`)
*   **Stage 2: Spotter** (`spotter.py` / `thresholds`)
*   **Stage 3: Challenger / Gates** (`challenger.py` / `admission_score`)
*   **Stage 4: Risk & Sizing** (`risk_manager.py` / `max_risk`)
*   **Stage 5: Exit Management** (Stop Loss, Take Profit, Timeouts)

## 2. Hardcoded Assumptions
Identify all mathematical or logical assumptions currently hardcoded into the pipeline. Examples include:
*   The 100-point rubric in `_calculate_admission_score`.
*   The fixed percentages for Stop Loss / Take Profit.
*   The time-based exit (e.g., 200 ticks duration).
*   Any hardcoded multipliers (like the Metals risk multiplier or spread caps).

## 3. Team Scaffold Queries & Limitations
Review the "team" scripts (`trade_reviewer.py`, `team_meeting.py`, `mentor.py`, etc.).
*   Summarize the specific "Open Questions" and "Agreed Actions" hardcoded into the dashboard.
*   Identify what these scripts are *currently incapable* of measuring (e.g., does the portfolio manager actually check cross-asset correlation, or is it just a placeholder string?).

**Goal:** Provide the GM and AG with a single pane of glass showing exactly what Ari is assuming, so we know what needs to be made dynamic in Stage 2.
