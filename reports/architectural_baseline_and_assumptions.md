# Architectural Baseline And Assumptions Map

**Date:** 2026-06-26
**Classification:** Engineering Audit / Baseline Map
**Author:** Codex
**Audience:** GM, AG, Ari Team

## 1. Purpose

This artifact maps Ari's current trading architecture and the embedded assumptions that shape behavior.

It is documentation only. It does not authorize code, strategy, threshold, risk, portfolio, or execution changes.

## 2. Architectural Flow

### Stage 1: Polling And Runner

**Primary files:** `saxo_trader/challenger_runner.py`, `saxo_trader/challenger_status.py`, `saxo_trader/storage.py`

1. Runner loads `.env` through `load_settings()`.
2. Runner fetches live Saxo SIM quotes for every `SAXO_WATCHLIST` instrument.
3. Quote fetches run concurrently with up to 8 workers.
4. Quotes are sorted by symbol.
5. If no quotes are fetched, the cycle logs `DATA_UNAVAILABLE` and skips trading.
6. If quotes exist, runner calls `run_challenger_cycle()`.
7. Runner logs one status line and updates `runner_heartbeats`.
8. Current Stage 1 deployment runs at `--interval 60`.

**Key assumption:** one runner cycle is the atomic trading decision interval. Ari does not react between cycles.

### Stage 2: Spotter / Signal Generation

**Primary file:** `saxo_trader/spotter.py`

1. Challenger asks storage for the latest `config.min_ticks_for_signal` ticks per symbol.
2. Spotter compares first and last tick in that window.
3. If percentage move exceeds the symbol threshold, Spotter emits `Buy` or `Sell`.
4. Spotter also labels whether the tick path is mostly directionally consistent.

**Current thresholds:**

- FX default: `CHALLENGER_MOMENTUM_THRESHOLD_PCT = 0.001`
- Training FX threshold: `CHALLENGER_TRAINING_MOMENTUM_THRESHOLD_PCT = 0.0005`
- XAUUSD override: `0.0036`
- XAGUSD override: `0.0078`

**Key assumption:** a first-to-last move across the last N ticks is a sufficient proxy for actionable momentum.

### Stage 3: Challenger / Admission Gates

**Primary file:** `saxo_trader/challenger.py`

For each active supported symbol:

1. Manage open positions first.
2. Ask AA operating decision whether staff vetoes block new entries.
3. Skip symbol if an open position already exists.
4. Require enough tick history.
5. Ask Spotter for a momentum signal.
6. Score the signal using a 100-point rubric.
7. Apply structural blockers:
   - admission score
   - quarantine
   - symbol activity cap
   - currency cluster / metals concentration
8. If still clear, size position and check planned risk.
9. Open a paper position and tag learning metadata.

**Current Stage 1 behavior:**

- Training mode is enabled via `.env`.
- Training admission score is `45`.
- Training mode applies to FX and metals.
- Max training entries per cycle is `2`.
- Max training entries per symbol per 60 minutes is `4`.

### Stage 4: Risk And Sizing

**Primary files:** `saxo_trader/challenger.py`, `saxo_trader/aa_decision.py`, `saxo_trader/risk_officer.py`, `saxo_trader/portfolio_manager.py`

Sizing is based on:

```text
quantity = risk_amount / (entry_price * stop_loss_pct)
```

Risk amount:

- FX: `config.max_risk_per_trade`
- Metals: `min(config.max_risk_per_trade * 0.35, 100.0)`
- Training mode: above amount multiplied by `training_probe_risk_multiplier`

Risk gate:

- Planned risk must not exceed `max_allowed_risk * 1.05`.
- The 5% buffer prevents fractional rounding blocks.

Staff-level gates:

- Mason: portfolio heat, daily loss, USD exposure, metals count.
- Clara: same-currency directional exposure and metals concentration.
- Ari aggregate downside: realized daily P/L minus open stop risk must stay above `-1000`.
- Anomaly scanner: blocks if critical anomaly groups exist.

### Stage 5: Exit Management

**Primary files:** `saxo_trader/challenger.py`, `saxo_trader/challenger_review.py`

Open positions close when one of the following triggers:

1. Paper stop loss hit.
2. Paper take profit hit.
3. Clara reduction advice triggers early exit.
4. Quick profit threshold is reached.
5. Trailing protection closes positive open P/L that no longer exceeds the protection threshold.

Current exit parameters:

- Stop loss: `CHALLENGER_STOP_LOSS_PCT = 0.005`
- Take profit: `CHALLENGER_TAKE_PROFIT_PCT = 0.01`
- Trailing protection: `CHALLENGER_TRAILING_PROTECT_PCT = 0.005`
- Quick profit: `CHALLENGER_QUICK_PROFIT_PCT = 0.0075`

**Key assumption:** paper stops are soft stops managed by the Python loop. They are not broker-side hard stops.

## 3. Hardcoded Assumptions

### Runner / Data

| Assumption | Value | Location | Effect |
|---|---:|---|---|
| Fetch workers | `min(watchlist, 8)` | `challenger_runner.py` | Caps concurrent Saxo quote requests. |
| Data outage throttle | `60 minutes` | `challenger_runner.py` | Prevents repeated outage journaling. |
| Current run interval | `60 seconds` | runner command | Sets reaction speed. |
| Supported symbols | FX pairs plus XAUUSD/XAGUSD | `challenger.py`, `challenger_runner.py` | Non-FX/non-metals ignored by Challenger. |

### Spotter

| Assumption | Value | Location | Effect |
|---|---:|---|---|
| Required ticks | `.env`, currently `5` | `config.py` | Signal window equals last 5 stored ticks. |
| FX production threshold | `0.001` | `.env` | 0.1% FX movement required. |
| FX training threshold | `0.0005` | `.env` | 0.05% FX movement required in training. |
| XAUUSD threshold | `0.0036` | `config.py` | 0.36% gold movement required. |
| XAGUSD threshold | `0.0078` | `config.py` | 0.78% silver movement required. |
| Consistent path | at least `max(2, len(moves)-1)` aligned moves | `spotter.py` | Rewards smooth paths, penalizes chop. |

### Admission Rubric

Current rubric totals up to 100 points:

| Component | Points | Rule |
|---|---:|---|
| Momentum strength | `35 / 25 / 15` | `>= 1.8x threshold`, `>= 1.2x`, else marginal. |
| Path consistency | `20` | Mostly aligned tick path. |
| Spread quality | `20 / 12 / 4` | Based on spread as share of `MAX_SPREAD_PCT`. |
| Recent symbol P/L | `15 / 6 / 0` | Last 10 closed trades for that symbol. |
| No same-theme open exposure | `10` | Entry cluster blockers absent. |

Admission thresholds:

- FX production: `70`
- Metals production: `85`
- Training: `45`

### Spread And Quote Quality

| Assumption | Value | Location | Effect |
|---|---:|---|---|
| Tradeable spread cap | `0.001` | `challenger.py` | Quote rejected if spread > 0.1% of mid. |
| Strong spread score | `<= 35%` of cap | `challenger.py` | Adds 20 points. |
| Medium spread score | `<= 65%` of cap | `challenger.py` | Adds 12 points. |
| Dashboard data warning spread | `0.15%` | `market_data_analyst.py` | Different from Challenger cap. |

### Frequency Limits

| Assumption | Production | Training | Location |
|---|---:|---:|---|
| Max entries per cycle | `1` | `.env`, currently `2` | `challenger.py` |
| Trade limit window | `60 minutes` | same | `challenger.py` |
| Max trades per window | `.env`, default `5` | same | `config.py` |
| Symbol limit window | `60 minutes` | same | `challenger.py` |
| Max entries per symbol/window | `2` | `.env`, currently `4` | `challenger.py` |

### Risk And Portfolio

| Assumption | Value | Location | Effect |
|---|---:|---|---|
| Max daily loss default | `100` | `config.py` | Daily hard stop for new entries. |
| Max risk per trade default | `50` | `config.py` | Base sizing input. |
| Metals risk multiplier | `0.35` | `challenger.py` | Reduces metals risk budget. |
| Max metals risk amount | `100` | `challenger.py` | Absolute metals cap. |
| Planned risk buffer | `5%` | `challenger.py` | Avoids tiny rounding rejections. |
| Aggregate downside limit | `1000` | `aa_decision.py` | Blocks if realized daily P/L minus open stop risk <= -1000. |
| Portfolio heat cap | `5%` | `risk_officer.py` | Mason warning threshold. |
| USD exposure cap | `3` | `risk_officer.py`, `portfolio_manager.py` | Blocks/cautions concentrated USD direction. |
| Clara metals active cap | `1` | `portfolio_manager.py` | Entry blocker at one active metals position. |
| Mason metals exposure warning | `>2` | `risk_officer.py` | Risk warning only above two metals positions. |

### Exit Logic

| Assumption | Value | Location | Effect |
|---|---:|---|---|
| Stop loss | `0.5%` | `.env` / `config.py` | Paper stop boundary. |
| Take profit | `1.0%` | `.env` / `config.py` | Paper target boundary. |
| Trailing protection | `0.5%` | `.env` / `config.py` | Closes positive P/L if move is below threshold. |
| Quick profit | `0.75%` | `.env` / `config.py` | Early take-profit style exit. |
| Near-stop reduction | `0.75` distance in Challenger early exit | `challenger.py` | Clara candidate can trigger early exit. |
| Portfolio near-stop flag | `0.5` distance | `portfolio_manager.py` | Clara reduction candidate flag. |

### Anomaly Scanner

| Assumption | Value | Location |
|---|---:|---|
| Max opened per minute | `3` | `anomaly_scanner.py` |
| Max closed per minute | `5` | `anomaly_scanner.py` |
| Minimum hold seconds | `60` | `anomaly_scanner.py` |
| Max planned FX risk | `250` | `anomaly_scanner.py` |
| Max planned metals risk | `100` | `anomaly_scanner.py` |
| Loss cluster count | `3` | `anomaly_scanner.py` |
| Missing path limit | `3` | `anomaly_scanner.py` |

## 4. Team Scaffold Queries And Limitations

### Ari Axelrod

**Measures today:**

- Entries, exits, holds, scouts.
- Staff vetoes.
- Admission scores.
- Sample type and training flags.

**Limitations:**

- Does not independently optimize.
- Does not override staff.
- Does not compare blocked opportunity outcomes live.
- Does not understand causal regimes beyond tags provided by the team.

### Mason Vale - Risk Officer

**Measures today:**

- Risk to stop per open position.
- Portfolio heat as stop-risk / starting capital.
- Daily realized P/L.
- USD long/short counts.
- Metals count.

**Limitations:**

- Correlation is count-based, not statistical.
- Does not calculate covariance, beta, volatility-adjusted exposure, or cross-asset correlation.
- Does not measure liquidity or gap risk.
- Does not place hard broker stops.

### Clara Stone - Portfolio Manager

**Measures today:**

- Currency exposure direction from symbol and side.
- Metals position count.
- Reduction candidates when concentration warnings exist.

**Limitations:**

- Portfolio risk is rule/count based.
- No notional allocation policy by asset.
- No volatility-adjusted concentration.
- Metals cap differs from Mason's metals warning threshold.

### Iris Quinn - Market Data Analyst

**Measures today:**

- Quote availability.
- Latest tick fallback.
- Stale price age.
- Spread percentage.
- Fetch errors.

**Limitations:**

- Dashboard warning spread cap is not the same as Challenger tradeability cap.
- Does not validate Saxo candle history.
- Does not detect quote freezes beyond stale-time checks.
- Does not classify partial market sessions or holiday liquidity.

### Theo Park - Systems Reliability

**Measures today:**

- Runner log freshness.
- Lock blocks.
- Recent data errors and HTTP errors.
- PID status.
- LaunchAgent error log size.

**Limitations:**

- Reads log symptoms; does not guarantee Saxo account/session validity.
- Does not auto-recover token expiry.
- Cannot prove paper stops executed during API blackouts.

### Nolan Price - Trade Reviewer

**Measures today:**

- Closed trade reviews.
- Review completeness.
- Loss clusters by symbol, side, close reason.

**Limitations:**

- Loss clustering is coarse.
- Does not yet classify losses as entry failure, management failure, or market failure automatically.
- No formal causal model.

### Rowan Pierce - Strategy Researcher

**Measures today:**

- Expectancy by symbol and side.
- Weak/good setup clusters once trades >= 3.
- Sample-size warnings below 30 trades.

**Limitations:**

- No statistical significance test.
- No out-of-sample validation.
- No blocked-vs-admitted counterfactual in the live module.
- Research actions are recommendations only, not governance-approved changes.

### Vera Lin - Execution Analyst

**Measures today:**

- Spread proxy.
- Adverse movement versus planned risk.
- Giveback detection.
- Execution grade.

**Limitations:**

- Uses latest tick spread, not true spread at execution for older trades unless stored elsewhere.
- No live slippage model.
- No broker-fill comparison because trading is paper-only.

### Mira Tan - Macro Regime Analyst

**Measures today:**

- Tick-based USD score.
- Tick-based metals score.
- Simple volatility state from recent tick range.
- Risk tone labels.

**Limitations:**

- Regime labels are heuristic.
- No calendar, macro-event, rates, yields, or cross-market inputs.
- Uses recent ticks, not multi-timeframe market structure.

### Evelyn Cross - Mentor

**Measures today:**

- Promotion status.
- Risk officer status.
- Closed trade count.
- Training focus.

**Limitations:**

- Coaching rules are hardcoded.
- Does not learn from AG/GM findings unless encoded elsewhere.

### Helena Ward - GM

**Measures today:**

- Uses repository-governance documents through `gm_agent.py`.
- Produces simple approval/rejection/return decisions for artifacts.

**Limitations:**

- Internal GM is a scaffold, not a reasoning model.
- It checks governance presence and prohibited language, not trading truth.

## 5. Hardcoded Open Questions And Agreed Actions

From `team_meeting.py`, current hardcoded open questions:

1. What concentration limit should Portfolio Manager enforce by currency and asset class?
2. When should AA reduce open positions early instead of waiting for stop or target?

Current hardcoded agreed actions include:

- Let current AA positions resolve; do not force new trades while risk is blocked.
- Theo owns Saxo/token/data/runner troubleshooting before AA strategy is changed.
- Use the current sample to isolate leaking symbols, sides, regimes, and execution patterns.
- Clara keeps portfolio concentration enforced while Mason controls daily loss and stop-risk exposure.
- Keep all staff accountable through Helena Ward's governance table.
- Do not increase AA size until profit factor is back above the next-rank threshold.
- Evidence Review is formal: Data -> Observation -> GM Review -> Hypothesis -> Contradiction Test -> Finding.
- AG owns the Observation Pipeline; Codex owns Organizational Memory and Governance Records.
- Finding Adoption Framework is in effect: Finding does not automatically authorize change.

## 6. Primary Hidden Load-Bearing Assumptions

1. **Momentum is first-to-last tick movement.**
   - This ignores intrawindow reversals except for the consistency score.

2. **Five ticks are enough to define a tradeable momentum window.**
   - At 60-second polling, this is roughly a 5-minute window.

3. **Admission scoring is additive and linear.**
   - A weak recent-symbol P/L can suppress otherwise valid signals.

4. **Recent symbol P/L is a valid penalty.**
   - This may protect against repeated weak setups, but can also suppress recovery after a bad sequence.

5. **Spread quality is measured against a universal cap.**
   - FX and metals share the same tradeability spread cap in Challenger.

6. **Soft paper stops are sufficient.**
   - Incident 187 showed this fails when data or runner access fails.

7. **Correlation risk can be approximated by currency-count rules.**
   - This is simple and auditable, but not statistically measured.

8. **Static threshold overrides are valid after 6-month ATR calibration.**
   - AG has already logged dynamic volatility thresholding as a roadmap item.

9. **Training probes can increase evidence density safely.**
   - Probe sizing reduces risk, but higher trade frequency can still create portfolio crowding.

10. **Staff modules are advisory snapshots, not full specialist engines.**
    - Several agents label risk, regime, or execution quality with heuristics rather than formal models.

## 7. Stage 2 Candidate Areas To Make Dynamic

This section is not a recommendation to change behavior now. It identifies where static assumptions currently sit.

- Dynamic per-symbol volatility thresholds.
- Volatility-adjusted stop loss and take profit.
- Symbol-specific spread caps.
- Statistical correlation / covariance risk.
- Dynamic admission scoring by regime and asset class.
- Explicit blocked-opportunity counterfactual outcomes.
- Hard-stop survivability design for data outages.
- Time-in-trade and MFE/MAE-aware exit policy.
- Formal session/regime labels from richer market data.
- Separate production mode and training mode dashboards/metrics.

## 8. Current Baseline Summary

Ari is currently a live-data, paper-only FX/Metals system using:

- 60-second polling.
- Spotter signal generation.
- Challenger admission and paper execution.
- Symbol-specific metals momentum thresholds.
- Training mode with lower admission gate.
- Soft stop/target management.
- Count-based risk and portfolio controls.
- Heuristic specialist team snapshots.

The architecture is now observable and modular enough for Stage 2 planning, but many of the core trading assumptions remain static, heuristic, and hand-tuned.

