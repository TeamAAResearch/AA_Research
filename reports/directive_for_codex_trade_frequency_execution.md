# Directive: Stage 1 Training Mode Optimizations
**Date:** 2026-06-26
**To:** Codex (Engineering)
**From:** AG (Research)

Ari's trade frequency is choked by overly restrictive admission gates and risk rounding limits. Execute the following structural adjustments to maximize signal throughput for Stage 1 evidence collection.

**1. Add 5% Risk Cap Tolerance (`saxo_trader/challenger.py`)**
Prevent fractional rounding blocks by adding a 1.05 multiplier to `max_allowed_risk`.
Modify `_execute_signal`:
```python
        planned_risk = _planned_risk(entry_price, stop_loss, quantity)
        max_allowed_risk = _max_allowed_risk(symbol, config.max_risk_per_trade)
        if planned_risk > (max_allowed_risk * 1.05):
            reason = f"Planned risk cap active: {planned_risk:.2f} exceeds {max_allowed_risk:.2f} (w/ 5% buffer)."
```

**2. Unblock Metals Training Mode (`saxo_trader/challenger.py`)**
Currently, `_required_admission_score` bypasses training mode for Metals. Refactor it so `training_sample_mode` overrides everything:
```python
def _required_admission_score(symbol: str, config: ChallengerConfig) -> int:
    if config.training_sample_mode:
        return config.training_min_admission_score
        
    if symbol in METALS:
        return MIN_METALS_ADMISSION_SCORE
        
    return MIN_ADMISSION_SCORE
```

**3. Lower Training Gate to 45 (`saxo_trader/models.py`)**
Set `training_min_admission_score` to `45`.
Modify `ChallengerConfig`:
```python
    training_min_admission_score: int = 45
```

**Instructions:**
Execute changes, ensure `training_sample_mode=True` is active in `.env` or `config.py`, run tests, and confirm completion. No live runner bounce needed; GM will manually bounce runner with `--interval 60` later.
