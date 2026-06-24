# Evidence Recovery Pilot Observations

**Scope:** AG
**Objective:** Review the recovered evidence ledgers (`opportunity_funnel.csv`, `cycle_vetoes.csv`) and generate strict observations.

## Observation 1: The Funnel Attrition Rate
Of the 495 recorded opportunities in the combined dataset:
*   **Admitted:** 145 (29.3%)
*   **Blocked at Admission:** 327 (66.1%)
*   **Blocked at Risk:** 23 (4.6%)

The vast majority of generated opportunities never reach the risk-sizing phase, being killed immediately by admission gates. 

## Observation 2: The Simulation Dependency Gap
*   **Observation:** 100% of the 350 blocked signals (327 Admission blocks + 23 Risk blocks) resulted in `No_Risk_Brackets` during the offline MFE/MAE simulation.
*   **Cause:** AA's `blocked_signals` table records the state of the opportunity *exactly* as it was when blocked. Because 93% of blocks occur at the Admission phase (before Stop Loss and Take Profit brackets are calculated by the Risk Manager), those prices do not exist in the serialized `raw_metadata` database field.
*   **Impact:** Post-hoc simulation of blocked trades requires offline risk-bracket generation (synthesizing the SL/TP thresholds based on the config) rather than just reading them from the DB. 

## Observation 3: Systemic Loop Vetoes
Of the 107 recorded full-cycle loop vetoes (where AA entirely stopped looking for trades):
*   **Downside Limit Breach:** 68 instances (63.5%)
*   **Concentrated Exposure Limits:** 38 instances (35.5%)
*   **Anomaly Scanner:** 1 instance (0.9%)

The primary cause of organizational downtime is the hard downside gate (`realized daily P/L - open stop risk <= limit`), followed by currency concentration limits. 

## Summary
The evidence recovery pipeline successfully flattened the historical data, but revealed an architectural dependency: because AA discards opportunities *before* pricing them, we cannot simulate their outcomes using purely "existing" fields. We must mathematically infer their hypothetical risk brackets based on the config in order to simulate their outcome.

**GM Review Required**
