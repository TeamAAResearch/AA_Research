# Codex Handoff: Universe Restriction And Training Gate Update

Date: 2026-06-29
Audience: AG
Prepared by: Codex

## Executive Summary

Ari is running normally after two important operational changes:

1. The trading universe was narrowed from the full Saxo FX/commodity sweep to 44 liquid major FX and major USD metals instruments.
2. The aggregate downside gate remains active for live-style mode, but no longer blocks new paper entries when `CHALLENGER_TRAINING_SAMPLE_MODE=true`.

This preserves future live-money discipline while allowing the current research/training mode to gather more data.

No live Saxo orders were placed.

## Universe Change

AG identified that the expanded exotic universe was producing low-quality training probes in high-spread/low-liquidity crosses.

Codex updated `.env`:

- Previous `SAXO_WATCHLIST`: 186 instruments
- New `SAXO_WATCHLIST`: 44 instruments

The active list now contains:

```text
AUDCAD, AUDCHF, AUDEUR, AUDGBP, AUDJPY, AUDNZD, AUDUSD,
CADCHF, CADEUR, CADJPY, CADUSD,
CHFAUD, CHFJPY, CHFUSD,
EURAUD, EURCAD, EURCHF, EURGBP, EURJPY, EURNZD, EURUSD,
GBPAUD, GBPCAD, GBPCHF, GBPEUR, GBPJPY, GBPNZD, GBPUSD,
JPYEUR, JPYUSD,
NZDAUD, NZDCAD, NZDCHF, NZDEUR, NZDGBP, NZDJPY, NZDUSD,
USDAUD, USDCAD, USDCHF, USDJPY,
XAGUSD, XAUUSD, XPTUSD
```

Result:

- Exotics such as `AUDTRY`, `AUDCNH`, `AUDDKK`, `AUDHKD`, `CADCNH`, `CADHKD`, and `CHFDKK` are no longer in the entry scan universe.
- Existing legacy open positions in removed symbols remain in the database and should be managed/closed by normal exit logic where price data is available.

## Training Gate Change

Problem:

- Ari was technically healthy but stopped opening/scouting because the aggregate downside gate was active:

```text
AA decision: BLOCK_NEW_ENTRIES. Aggregate downside gate breached:
realized daily P/L -737.30 minus open stop risk 312.43 <= -1000.
```

Governance distinction:

- This gate is important for live-money discipline.
- It is counterproductive during the current paper-training data collection phase because it starves the evidence pipeline.

Code behavior now:

- If `training_sample_mode=False`, the aggregate downside gate still blocks new entries.
- If `training_sample_mode=True`, aggregate downside is still calculated and visible, but it does not block new paper entries.

Files changed:

- `saxo_trader/aa_decision.py`
- `tests/test_aa_decision.py`

Focused tests:

```text
python3 -m unittest tests.test_aa_decision tests.test_challenger tests.test_challenger_runner tests.test_config
38 tests passed
```

## Database Stability Note

SQLite was also adjusted earlier today to reduce post-reboot fragility:

- storage now avoids repeatedly forcing WAL mode
- database journal mode was confirmed as `delete`
- focused storage/runner tests passed

Current DB state:

- Integrity: OK
- Ari heartbeat: OK
- Last error: none

## Current Ari Status

Latest verified heartbeat:

```text
runner_name: ai_challenger
pid: 36390
last_cycle_status: OK
last_error: none
```

Latest runner log confirms:

- 44-symbol universe active
- aggregate downside gate bypass loaded in training mode
- Ari is scouting normally

Example latest cycle:

```text
opened=0 closed=0
skipped=['AUDCAD: no momentum signal.', 'AUDEUR: no momentum signal.', 'AUDGBP: no momentum signal.']
errors=[]
```

Interpretation:

- No new trades in the latest sampled cycle, but this is normal signal logic, not a risk-gate or infrastructure block.

## AG Watch Items

AG should watch:

1. Whether removed exotic positions close naturally.
2. Whether new entries now come only from the 44-symbol liquid universe.
3. Whether training mode produces enough data without reintroducing exotic-spread bleed.
4. Whether the aggregate downside bypass should remain research-only and never carry into live-style mode.
5. Whether Ari's future losses are now driven by signal quality/exit behavior rather than instrument liquidity.

Current operational stance:

- Ari can continue running.
- Technical issues are resolved for now.
- The next bottleneck is evidence quality, not infrastructure.
