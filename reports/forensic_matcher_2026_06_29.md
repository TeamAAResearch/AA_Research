# P3 Forensic Matcher Report

Generated at: 2026-06-29T12:46:25.088356+00:00
Ledger: `AA_Research/ledgers/kenny_xauusd_june.xlsx`
Market proxy: `GC=F`
Interval: `5m`
Medium-confidence tolerance: `1.0` price points
CSV output: `/Users/kennylee/Documents/Saxo/AA_Research/ledgers/human_benchmark/forensic_matcher_2026_06_29_124625.csv`

## Read-Only Scope

This report reconstructs human trade paths for research only. It does not modify Ari, strategy, thresholds, risk, portfolio rules, or execution logic.

## Match Quality

- Total XAUUSD trades: 145
- Matched trades: 109
- High confidence matches: 105
- Medium confidence matches: 4
- Unmatched trades: 36

## Core Holding-Time Metrics

- Winning trades matched: 41
- Losing trades matched: 68
- Average hold, winners: 215.98 minutes
- Average hold, losers: 51.03 minutes
- Average MFE, winners: 20.83 points
- Average MFE, losers: 11.62 points
- Average MAE, winners: -17.40 points
- Average MAE, losers: -14.28 points

## Research Answer

Matched evidence suggests winners often require more than 60 minutes, so Ari's 60-minute time-decay rule may suppress some winners. Treat as research evidence, not an execution change.

## Caveats

- Saxo ledger timestamps are date-level in the provided export.
- GC=F futures are used as a proxy for XAUUSD spot path.
- Results should be weighted by confidence before any execution research is promoted.