# AA Shared Research Memo

Date: 2026-06-24
Project: AA Research

## Mission

Build an autonomous FX trader capable of producing positive expectancy consistently in paper/simulation mode.

AA remains live Saxo/SIM market data plus paper/simulated trades only. No live Saxo orders. No real-money trading.

## Current Governance State

Code freeze remains active.

No changes to:

- Code
- Strategy
- Thresholds
- Risk controls
- Portfolio construction
- Dashboard

Allowed intervention only for operational failure, database integrity failure, or data-feed failure.

## Official Baseline

Current quantitative baseline:

**Phase 25 Projected: 0.3 ATR Stop + 1.0x Pyramid Optimization**

Date achieved: 2026-06-28

- Net P/L: $4,605.38 SGD
- Previous baseline: $2,911.07 SGD
- Win rate: 61.9%
- Average winning trade: $192.14
- Average losing trade: -$24.40
- Expectancy per trade: $109.65
- Previous expectancy: $69.31
- Sample size: 42 high-conviction trades across 11 instruments

Canonical proof:

- Report: `AA_Research/reports/phase25_projected_baseline_2026_06_28.md`
- Script: `AA_Research/scripts/simulate_phase25_mae_optimization.py`

Interpretation:

This is a projected replay baseline for Ari's optimized brain, not live realized P/L. Future live paper-trading results should be compared against this benchmark.

Official production research baseline:

2026-06-22 07:02:25 UTC

Everything before this is legacy transition analysis and must not be mixed into production research metrics.

## Current Research Position

The organization must avoid premature certainty.

Every major conclusion must be classified as:

- Observation: raw fact from ledger.
- Hypothesis: pattern observed but insufficient sample size.
- Emerging Finding: pattern persists across meaningful sample.
- Finding: supported by sufficient evidence and survives review.

For every major conclusion, record:

- Sample size
- Time range
- Number of pairs involved
- Number of sessions involved
- Observation
- Explanation
- Confidence
- Evidence

## Priority Hypotheses

Treat all as hypotheses until disproven:

- FX Buy weakness
- Duration effect
- Management failure
- Score predictive power
- Blocked-opportunity suppression

Seek contradictory evidence as aggressively as supporting evidence.

## N=100 Reassessment Focus

At N=100 FX opportunities, review:

- Expectancy by score
- Expectancy by duration
- Expectancy by side
- Expectancy by asset
- Expectancy by session
- Blocked vs admitted expectancy

## Current Evidence Summary

Latest reported production sample showed:

- FX Buy weak
- FX Sell positive
- Metals positive
- Losses concentrated in long-duration trades
- Cause vs symptom still unknown

Current interpretation:

- AA is revealing stable behaviors.
- The team does not yet understand the causes.

## Opportunity Economics Framework

Track and report at N=25, N=50, and N=100 FX opportunities:

1. Funnel:
   Observed -> Admission -> Risk Pass -> Executed -> Closed

2. Attrition:
   Admission Block
   Boundary Risk Block
   Material Risk Block
   Portfolio Block

3. Opportunity density by:
   Pair
   Session
   Day

4. Capture efficiency:
   MFE vs realized P/L

5. Business identity:
   FX share vs Metals share by opportunities, trades, and P/L

Research question:

Can AA generate sufficient FX opportunity flow to support a trading business?

## Blocked Opportunity Methodology

Do not classify blocked opportunities as simple wins or losses.

Evaluate:

- Favorable excursion (MFE)
- Adverse excursion (MAE)
- Risk-adjusted outcome
- Expected outcome under AA's actual exit framework

Research question:

Did the block improve or worsen expected business outcomes?

Not:

Did the market move in the predicted direction?

## Team Responsibilities

Ari Axelrod: Trader / AA Decision Desk.
Explains what AA chose, rejected, held, and exited.

Rowan Pierce: Strategy Research.
Determines whether AA has repeatable edge and separates signal from noise.

Nolan Price: Trade Review.
Reviews wins and losses, recurring mistakes, and actionable lessons.

Clara Stone: Portfolio Manager.
Reviews concentration by instrument, currency, side, and exposure.

Mira Tan: Macro Regime Analyst.
Reviews market regime, session effects, volatility, and performance context.

Mason Vale: Risk Officer.
Reviews stop risk, drawdown, daily loss, risk blocks, and whether risk protects or suppresses AA.

Vera Lin: Execution Analyst.
Reviews entry/exit quality, spread, timing, MFE/MAE, and value leakage.

Iris Quinn: Market Data Analyst.
Verifies quote quality, symbol coverage, stale data, and whether FX opportunities genuinely existed.

Theo Park: Systems Reliability.
Keeps runner, heartbeat, backups, Saxo connection, and database health green/amber/red.

Evelyn Cross: Mentor.
Judges whether AA is learning and whether promotion is justified.

Sofia Chen: Team Architect.
Ensures the team is solving the right problem and avoids unnecessary expansion.

Helena Ward: Governance / Chair.
Demands evidence for conclusions and holds specialists accountable.

## 29 June GM Review

Purpose:

Explain AA's trading business, not merely report statistics.

The team must answer:

AA makes money when ______.

AA loses money when ______.

If the team cannot answer clearly with evidence, AA remains in discovery mode.

## Operational Notes

Recent operational issue:

Heartbeat stalls appeared consistent with Mac sleep/app suspension gaps.

Operational fix:

A no-sleep guard was activated with caffeinate.

Research instruction:

Ignore the caffeinate operational fix in trading-performance interpretation.
