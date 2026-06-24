# AA Research Mission

Date created: 2026-06-24
Project: AA autonomous trading research
Canonical baseline: 2026-06-22 07:02:25 UTC

## Mission

Build an autonomous FX trader capable of producing positive expectancy consistently in paper/simulation mode.

## Current Phase

Data Collection & Learning.

AA is not in validation, optimization, deployment, or real-money trading mode.

## Operating Constraints

- Live Saxo/SIM market data only.
- Paper/simulated trades only.
- No live Saxo order placement.
- No real-money trading.
- Production metrics must use only data from 2026-06-22 07:02:25 UTC onward.

## Hard Freeze

No changes to:

- Code
- Strategy
- Thresholds
- Risk controls
- Portfolio construction

Allowed intervention only for operational failure, database integrity failure, or data-feed failure.

## Research Objective

Success is evidence, not activity.

The project must determine whether AA can become a profitable autonomous FX trader by measuring:

- Opportunity generation
- Opportunity loss
- Trade quality
- Exit quality
- Risk-adjusted expectancy
- Operational stability
- Explainability

## Core Management Question

AA makes money when ______.

AA loses money when ______.

If the team cannot answer these with evidence, AA remains in discovery mode.
