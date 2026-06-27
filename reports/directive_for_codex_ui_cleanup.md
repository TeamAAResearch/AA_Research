# Directive: Dashboard UI Cleanup (Deprecate Human Challenger)
**Date:** 2026-06-26
**To:** Codex (Engineering)
**From:** AG (Research)

The GM has requested the complete removal of the "Human Challenger" tracking from the `dashboard.py` host page. The project is now solely focused on the autonomous AI engine, making the human tracking redundant.

Please perform the following cleanup:

1. **`dashboard.py`**:
   - Remove the `human_score` import.
   - Remove the `Human Challenge Capital` input field and save logic (lines ~144-155).
   - Remove the `human = human_score(...)` calculation.
   - Remove the "Human vs AI Challenger" subheader and the associated dual-metric display logic.
   - Re-title the section to focus purely on the AI Challenger's performance towards the goal.

2. **`saxo_trader/goals.py`**:
   - Delete the `human_score` function entirely, as it is no longer used.

Confirm when the UI has been successfully cleaned and all tests still pass.
