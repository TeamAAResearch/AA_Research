# Strategy Pivot: Trade Frequency Optimization

The data reveals that the drop in trade frequency is a layered issue. Ari's core momentum engine (Spotter) is working correctly, but the downstream execution gates are too rigid. To restore a healthy trade velocity without sacrificing risk management, we need to implement three targeted architectural adjustments.

## User Review Required
> [!CAUTION]
> Loosening the admission gates and decreasing the polling interval will significantly increase the trade velocity of the system. We must be prepared to monitor slippage and false-breakouts over the next 48 hours.

## Proposed Changes

### 1. Training Phase Risk Buffer (Relaxed Sizing)
#### [MODIFY] [challenger.py](file:///Users/kennylee/Documents/Saxo/saxo_trader/challenger.py)
Since we are in Stage 1 (evaluating signal accuracy), we should not block valid momentum signals over minor risk-cap rounding errors. We will add a generous 5% operational tolerance buffer to `_max_allowed_risk`.
*   **Action:** Update line 149 in `challenger.py`: `if planned_risk > (max_allowed_risk * 1.05):`

### 2. Admission Scoring Cleanup
#### [MODIFY] [challenger.py](file:///Users/kennylee/Documents/Saxo/saxo_trader/challenger.py)
The GM correctly challenged this point. A deep-dive into `_calculate_admission_score` reveals a 100-point rubric:
1.  **Momentum Strength:** Up to 35 pts (marginal gets 15).
2.  **Tick Consistency:** Up to 20 pts (choppy gets 0).
3.  **Spread:** Up to 20 pts (wide gets 4).
4.  **Paper Performance:** Up to 15 pts (losing streak gets 0).
5.  **Theme Concentration:** Up to 10 pts (correlated position open gets 0).

**The Problem:** Because we are in Stage 1 (Signal Evaluation), factors like "Paper Performance" and "Theme Concentration" shouldn't block us from collecting raw signal data. Furthermore, Metals are hardcoded to require 85 points, meaning a Gold signal requires near-perfection (strong momentum, clean tick, tight spread, winning streak, and unique theme) to execute.

*   **Action:** Modify `_required_admission_score` so that `config.training_sample_mode` applies equally to FX and Metals (currently it bypasses Metals).
*   **Action:** Update `training_min_admission_score` in `models.py` to **45**. This explicitly allows a signal with "Marginal Momentum (15) + Clean Tick (20) + Acceptable Spread (12) = 47 points" to pass, even if historical performance is currently poor.

### 3. Polling Interval Acceleration
#### [MODIFY] Runner Execution Command
The 5-minute polling interval creates a massive 25-minute blind spot for the Spotter.
*   **Action:** The GM will bounce the runner using `--interval 60`. This creates a tight, highly reactive 5-minute momentum window.

## Verification Plan

### Automated Tests
- Run `pytest tests/test_challenger.py` to ensure the risk buffer logic passes existing bounds tests.

### Manual Verification
- Restart the runner with `--interval 60`.
- Monitor the SQLite database over the next 2 hours. We expect to see more signals generated (due to the 1-minute interval) and fewer blocks (due to the 60/75 gates and 1% risk buffer).
