# AA Research Policy

## Baseline

Official production research baseline:

2026-06-22 07:02:25 UTC

Everything before this is legacy transition analysis and must not be mixed into production research metrics.

## Governance Rules

Observation is not hypothesis.

Hypothesis is not finding.

Finding requires surviving contradiction.

Approved Organizational Workflow (2026-06-24):

  Data → Observation → GM Review → Hypothesis → Contradiction Test → Finding

The step "Data → Observation → GM Review" is a mandatory pre-hypothesis gate.

Observations must not be promoted to Hypotheses without explicit GM authorization.

## Evidence Review

Evidence Review is a formal organizational function approved 2026-06-24.

Evidence Review means reviewing structured Evidence Recovery ledgers to generate Observations.

Evidence Review is not Evidence Recovery.

Evidence Review does not produce findings.

Evidence Review does not authorize strategy, threshold, risk, portfolio, or code changes.

Primary ledgers under Evidence Review:

- ledgers/opportunity_funnel.csv
- ledgers/cycle_vetoes.csv
- ledgers/opportunity_funnel_simulated.csv (Shadow Risk Engine output)

## Evidence Standard

Every major conclusion must include:

- Sample size
- Time range
- Number of pairs involved
- Number of sessions involved
- Observation
- Explanation
- Confidence: Low / Medium / High
- Evidence

## Classification Standard

Observation:

Raw fact from ledger or trade history.

Hypothesis:

Pattern observed but insufficient sample size.

Emerging Finding:

Pattern persists across meaningful sample and has faced some contradiction testing.

Finding:

Supported by sufficient evidence and survives review.

## Contradiction Rule

For every active hypothesis, the team must seek evidence that could disprove it.

Supportive evidence alone is insufficient.

## Research Freeze

Until the next GM decision, do not modify:

- Strategy
- Thresholds
- Risk rules
- Portfolio rules
- Trading code
- Dashboard

Operational intervention is allowed only when evidence collection is threatened.

## Primary Research Artifact

The FX Opportunity Ledger is the primary artifact for determining where FX opportunities disappear.

## Opportunity Economics

Track at N=25, N=50, and N=100 FX opportunities:

- Funnel: Observed -> Admission -> Risk Pass -> Executed -> Closed
- Attrition: Admission Block, Boundary Risk Block, Material Risk Block, Portfolio Block
- Opportunity density by pair, session, and day
- Capture efficiency: MFE vs realized P/L
- Business identity: FX share vs metals share by opportunities, trades, and P/L

## Blocked Opportunity Methodology

Do not classify blocked opportunities as simple wins or losses.

Evaluate:

- Favorable excursion
- Adverse excursion
- Risk-adjusted outcome
- Expected outcome under AA's actual exit framework

Research question:

Did the block improve or worsen expected business outcomes?
