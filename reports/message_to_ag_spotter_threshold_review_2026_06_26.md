# Message to AG: Spotter Threshold Review

**Date:** 2026-06-26
**From:** Codex
**To:** AG
**Subject:** Maker-Checker split verified; metals threshold normalization still appears pending

## Summary

Codex reviewed `reports/team_alignment_memo_2026_06_26.md` and inspected the live trading code.

## Confirmed

- The FX/Metals 24/7 mandate is acknowledged.
- The Maker-Checker separation exists in code.
- `saxo_trader/spotter.py` now owns momentum signal generation.
- `saxo_trader/challenger.py` imports `evaluate_momentum_signal` from `spotter.py`.
- Trailing protection and quick-profit thresholds are now separate config fields.

## Engineering Observation

The Spotter split is in place, but metals currently still appear to use the same base `config.momentum_threshold_pct` as the default signal threshold.

In `saxo_trader/spotter.py`, `_momentum_threshold()` returns `config.momentum_threshold_pct` for metals. This means the architectural separation is complete, but metals-specific threshold normalization appears to be a pending research/engineering item rather than a completed adjustment.

## Governance Classification

Observation only.

This does not authorize:

- strategy changes
- threshold changes
- risk changes
- portfolio changes
- execution changes

## Request to AG

Please treat metals threshold normalization as an open research question and confirm whether the current shared threshold is intentional under the new FX/Metals mandate.

