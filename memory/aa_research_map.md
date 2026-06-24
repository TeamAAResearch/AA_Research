# AA Research Map

Status: Current knowledge map
Date created: 2026-06-24
Authority: AA Organizational Charter v1.0

Purpose:

Maintain the organization's current state of knowledge.

Rules:

- Observation is not hypothesis.
- Hypothesis is not finding.
- Finding requires surviving contradiction.
- This document records knowledge state only.
- It does not authorize recommendations or changes.

## 1. Active Findings

No active findings.

No hypothesis has yet been promoted to finding under the current governance standard.

## 2. Active Hypotheses

### H1. FX Buy Weakness

Status: Hypothesis

Question:

Are FX Buy setups structurally weaker than FX Sell setups?

Current evidence:

- `reports/fx_long_analysis_2026_06_24.md` reports FX Buy as the largest negative class/side contributor in the reviewed sample.
- That report shows FX Buy with 8 trades, total P/L -$793.57, average P/L -$99.20, average MFE $9.09, average MAE -$114.37, and 3 stop losses.
- The same report shows FX Sell with 10 trades, total P/L +$146.17, average P/L +$14.62, average MFE $19.88, average MAE -$21.75, and 0 stop losses.
- `reports/daily_report_2026_06_23.md` identifies GBPJPY Buy as a warning pattern and notes that FX would have been positive excluding GBPJPY Buy at that checkpoint.

Contradictory evidence:

- `reports/fx_long_analysis_2026_06_24.md` includes several profitable FX Buy trades, especially short-duration GBPJPY and GBPUSD Buy winners.
- FX Buy weakness may be driven by a subset of long-duration or repeated-entry cases rather than all FX Buy setups.
- Sample size remains limited and may not represent other sessions, regimes, or pairs.

Evidence required for promotion to finding:

- Larger post-baseline sample across multiple FX pairs and sessions.
- Expectancy by FX side remains materially weaker for Buy after contradiction testing.
- Weakness persists after separating duration, session, score, and pair effects.
- FX Buy underperformance is not explained solely by one pair, one session, or one small cluster.

Evidence required for rejection:

- FX Buy expectancy normalizes or becomes positive over a larger sample.
- Underperformance is fully explained by duration, pair, session, or specific setup subtype rather than Buy side itself.
- Contradictory profitable FX Buy examples become sufficiently common and risk-adjusted.

### H2. Duration Effect

Status: Hypothesis

Question:

Do long-duration trades account for a disproportionate share of losses?

Current evidence:

- `reports/survival_analysis_2026_06_24.md` reports 32 closed standard_signal trades.
- Trades under 1 hour: 25 trades, 100% win rate, total P/L +$244.44, zero stop-loss exits.
- Trades over 8 hours: 6 trades, 33% win rate, total P/L -$608.69, four stop-loss exits.
- The report states that every catastrophic loss in that sample came from trades held longer than 8 hours.
- `reports/fx_long_analysis_2026_06_24.md` shows FX Buy losses concentrated in long-duration trades over 8 hours.

Contradictory evidence:

- `reports/survival_analysis_2026_06_24.md` includes at least one long-duration positive trade: XAUUSD Sell, 15h56m, +$267.59.
- Long duration may be a symptom of adverse trade development, not an independent cause.
- The sample is small and may be influenced by stop-loss mechanics and position type.

Evidence required for promotion to finding:

- Duration-outcome relationship persists across a larger sample and multiple symbols.
- The effect remains after separating asset class, side, score, session, and exit reason.
- Long-duration trades show consistently worse risk-adjusted expectancy.
- Contradictory long-duration winners are insufficient to explain away the pattern.

Evidence required for rejection:

- Longer-duration trades show neutral or positive risk-adjusted expectancy over a larger sample.
- Losses are explained by entry quality, symbol, side, or regime rather than duration.
- Duration no longer separates winners and losers after additional data accumulates.

### H3. Management Failure

Status: Hypothesis

Question:

Is AA losing value after entry due to exit or trade-management behavior?

Current evidence:

- `reports/fx_long_analysis_2026_06_24.md` classifies 2 of 3 major FX Buy losses as management failures.
- EURUSD Buy and GBPUSD Buy had high entry scores of 90, briefly went positive, then were held around 21 to 24.6 hours to stop loss.
- `reports/survival_analysis_2026_06_24.md` states that AA exits winners quickly but has no equivalent mechanism in the observed sample for cutting deteriorating trades before stop loss.
- MFE vs realized P/L evidence suggests some trades gave back potential value before closing.

Contradictory evidence:

- Some losses may be entry failures rather than management failures, such as the GBPJPY Buy case in `reports/fx_long_analysis_2026_06_24.md`.
- Small MFE values in losing trades may indicate weak or marginal entries rather than poor management.
- AA's current exit framework may be behaving as designed under frozen policy; poor outcomes do not by themselves prove management failure.

Evidence required for promotion to finding:

- Repeated examples where trades show meaningful favorable excursion, then close materially worse.
- Capture efficiency remains poor in specific setups after controlling for spread, symbol, side, score, session, and volatility.
- Exit reason and time-in-trade patterns consistently identify value leakage after entry.
- Contradictory evidence does not show that losses are primarily entry failures or market failures.

Evidence required for rejection:

- Most losing trades show little or no favorable excursion, indicating entries rather than management caused losses.
- Capture efficiency improves or remains acceptable across a larger sample.
- Losses are better explained by market regime, symbol selection, or score quality.

### H4. Score Predictive Power

Status: Hypothesis

Question:

Does admission score predict expectancy or risk-adjusted outcome?

Current evidence:

- `reports/fx_long_analysis_2026_06_24.md` includes high-score FX Buy losses at score 90 and lower-score FX Buy winners at score 75 to 80, which complicates a simple score-positive interpretation.
- Earlier daily research noted score buckets as a priority review area, but current repository evidence does not yet establish score as reliably predictive.
- The N=100 reassessment explicitly prioritizes expectancy by score.

Contradictory evidence:

- High-score trades can lose.
- Lower-score trades can win.
- Score may interact with side, pair, duration, session, or asset class.
- Current sample may be too small to judge score calibration.

Evidence required for promotion to finding:

- Clear monotonic or otherwise repeatable relationship between score bucket and expectancy over a larger sample.
- Score effect survives separation by asset class, side, session, and duration.
- Blocked vs admitted opportunity review supports that score improves expected business outcome.

Evidence required for rejection:

- No stable relationship between score and expectancy across N=100+ opportunities.
- Score signal disappears after controlling for symbol, side, session, duration, or regime.
- Lower-score opportunities consistently perform as well as or better than higher-score opportunities on a risk-adjusted basis.

### H5. Blocked-Opportunity Suppression

Status: Hypothesis

Question:

Are risk, portfolio, or admission blocks suppressing profitable FX opportunities?

Current evidence:

- `reports/daily_report_2026_06_23.md` reports 68 FX opportunities observed at the N=25 checkpoint, with 18 admitted, 45 blocked pre-admission, and 5 execution blocks.
- That report shows Admission Block at 23 and Risk Block at 19, making both major attrition stages in that sample.
- Boundary risk events were observed, including six FX opportunities rejected by risk cap overshoots of $0.01 to $0.26.
- Current governance specifically requires blocked opportunities to be evaluated by MFE, MAE, risk-adjusted outcome, and expected outcome under AA's actual exit framework.

Contradictory evidence:

- High rejection rates alone are not evidence of suppression.
- Blocks may be protecting AA from poor opportunities.
- Boundary overshoot does not prove expected profitability.
- Current repository evidence does not yet show whether blocked opportunities would have improved business outcomes under AA's exit framework.

Evidence required for promotion to finding:

- Blocked opportunities show favorable expected outcomes after evaluating MFE, MAE, risk-adjusted outcome, and AA exit-framework simulation.
- Suppression persists across multiple sessions, pairs, and block types.
- Boundary Risk Blocks and other block categories show materially different expected outcomes from admitted trades.
- Evidence survives comparison against admitted trades with similar score, pair, side, session, and regime.

Evidence required for rejection:

- Blocked opportunities show poor or inferior expected outcomes versus admitted trades.
- Blocks prevent adverse excursions, excessive risk, or poor risk-adjusted expectancy.
- Boundary and material blocks do not show economically meaningful lost opportunity after larger sample review.

## 3. Unknowns

- Whether AA can generate sufficient high-quality FX flow over a statistically meaningful period.
- Whether FX Buy weakness is structural, duration-driven, pair-specific, session-specific, or sample noise.
- Whether long-duration losses are caused by trade management failure or are only a symptom of bad entries.
- Whether admission score predicts risk-adjusted expectancy after controlling for side, asset, pair, session, and duration.
- Whether blocked opportunities would have improved or worsened expected business outcomes.
- Whether metals observations are useful comparison data or distracting from the FX mission.
- Whether current results persist across future regimes and sessions.

## 4. Rejected Hypotheses

No rejected hypotheses.

No hypothesis has yet accumulated sufficient contradictory evidence for formal rejection under the current governance standard.

## 5. Evidence Required

### Cross-Hypothesis Evidence Needed

- Production-only data from the official baseline: 2026-06-22 07:02:25 UTC onward.
- FX opportunity ledger with admitted and blocked opportunities.
- Trade history with symbol, side, session, score, MFE, MAE, realized P/L, exit reason, and duration.
- Blocked-opportunity review using MFE, MAE, risk-adjusted outcome, and expected outcome under AA's actual exit framework.
- Expectancy by score, duration, side, asset, session, pair, and block stage.
- Contradictory evidence review for every candidate finding.

### Promotion Standard

A hypothesis may be considered for promotion only if:

- Sample size is sufficient for the claim being made.
- Evidence spans relevant pairs, sessions, and regimes.
- Contradictory evidence has been actively searched for.
- Known limitations are documented.
- GM review accepts the claim as a finding candidate.
- Repository records the supporting evidence and contradiction review.

### Rejection Standard

A hypothesis may be rejected only if:

- The expected pattern fails to persist over a meaningful sample.
- Contradictory evidence explains the earlier pattern more convincingly.
- The rejected status is recorded with evidence and limitations.

### Current Status

The project remains in Data Collection & Learning.

The repository records hypotheses and observations only.

No findings are created by this document.
