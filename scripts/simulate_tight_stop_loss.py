#!/usr/bin/env python3
from __future__ import annotations

import csv
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from statistics import mean


REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = REPO_ROOT.parent
DB_PATH = PROJECT_ROOT / "trading_system.sqlite3"
CSV_PATH = REPO_ROOT / "ledgers" / "tight_stop_simulation_results.csv"
REPORT_PATH = REPO_ROOT / "reports" / "tight_stop_simulation_results.md"

REGIME_START_ID = 136
STOP_CAP = -20.0


@dataclass(frozen=True)
class Trade:
    id: int
    created_at: str
    symbol: str
    side: str
    pnl: float
    mfe: float
    mae: float
    duration_seconds: float
    close_reason: str
    sample_type: str


@dataclass(frozen=True)
class SimulationRow:
    trade: Trade
    stop_triggered: bool
    synthetic_pnl: float
    pnl_delta: float
    baseline_outcome: str
    synthetic_outcome: str


def main() -> None:
    rows = simulate()
    write_csv(rows)
    write_report(rows)
    print(f"Wrote {CSV_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(REPO_ROOT)}")


def simulate() -> list[SimulationRow]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        trades = _load_regime_trades(conn)
    return [_simulate_trade(trade) for trade in trades]


def _load_regime_trades(conn: sqlite3.Connection) -> list[Trade]:
    query = """
        SELECT
            id,
            created_at,
            symbol,
            side,
            pnl,
            mfe,
            mae,
            time_in_trade_seconds,
            close_reason,
            sample_type
        FROM challenger_trades
        WHERE id >= ?
          AND status = 'Closed'
          AND sample_type = 'standard_signal'
        ORDER BY id
    """
    trades: list[Trade] = []
    for row in conn.execute(query, (REGIME_START_ID,)):
        trades.append(
            Trade(
                id=int(row["id"]),
                created_at=str(row["created_at"]),
                symbol=str(row["symbol"]),
                side=str(row["side"]),
                pnl=float(row["pnl"] or 0),
                mfe=float(row["mfe"] or 0),
                mae=float(row["mae"] or 0),
                duration_seconds=float(row["time_in_trade_seconds"] or 0),
                close_reason=str(row["close_reason"] or ""),
                sample_type=str(row["sample_type"] or ""),
            )
        )
    return trades


def _simulate_trade(trade: Trade) -> SimulationRow:
    stop_triggered = trade.mae <= STOP_CAP
    synthetic_pnl = STOP_CAP if stop_triggered else trade.pnl
    return SimulationRow(
        trade=trade,
        stop_triggered=stop_triggered,
        synthetic_pnl=synthetic_pnl,
        pnl_delta=synthetic_pnl - trade.pnl,
        baseline_outcome="Win" if trade.pnl > 0 else "Loss",
        synthetic_outcome="Win" if synthetic_pnl > 0 else "Loss",
    )


def write_csv(rows: list[SimulationRow]) -> None:
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "trade_id",
                "created_at",
                "symbol",
                "side",
                "duration_seconds",
                "baseline_pnl",
                "mfe",
                "mae",
                "close_reason",
                "stop_triggered",
                "synthetic_pnl",
                "pnl_delta",
                "baseline_outcome",
                "synthetic_outcome",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row.trade.id,
                    row.trade.created_at,
                    row.trade.symbol,
                    row.trade.side,
                    round(row.trade.duration_seconds, 2),
                    round(row.trade.pnl, 2),
                    round(row.trade.mfe, 2),
                    round(row.trade.mae, 2),
                    row.trade.close_reason,
                    int(row.stop_triggered),
                    round(row.synthetic_pnl, 2),
                    round(row.pnl_delta, 2),
                    row.baseline_outcome,
                    row.synthetic_outcome,
                ]
            )


def write_report(rows: list[SimulationRow]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    baseline_pnl = sum(row.trade.pnl for row in rows)
    synthetic_pnl = sum(row.synthetic_pnl for row in rows)
    delta = synthetic_pnl - baseline_pnl
    baseline_wins = sum(1 for row in rows if row.trade.pnl > 0)
    synthetic_wins = sum(1 for row in rows if row.synthetic_pnl > 0)
    stopped_rows = [row for row in rows if row.stop_triggered]
    baseline_losses = [row.trade.pnl for row in rows if row.trade.pnl < 0]
    synthetic_losses = [row.synthetic_pnl for row in rows if row.synthetic_pnl < 0]
    false_stop_winners = [row for row in stopped_rows if row.trade.pnl > 0]
    tail_losses = [row for row in rows if row.trade.pnl <= -100]
    xau_rows = [row for row in rows if row.trade.symbol == "XAUUSD"]

    lines = [
        "# Tight Stop Simulation Results",
        "",
        "**Classification:** Simulation Report",
        "**Owner:** AG / Codex",
        "**Date:** 2026-06-25",
        "**Status:** Internal GM Review Required",
        "",
        "---",
        "",
        "## Evidence",
        "",
        f"- Source database: `{DB_PATH}`",
        "- Source table: `challenger_trades`.",
        f"- Cohort: closed `standard_signal` trades with `id >= {REGIME_START_ID}`.",
        f"- Trades reviewed: {len(rows)}.",
        f"- Synthetic rule tested: if recorded MAE <= ${STOP_CAP:.2f}, set synthetic P/L to ${STOP_CAP:.2f}; otherwise keep actual realized P/L.",
        f"- Baseline P/L: {baseline_pnl:.2f}.",
        f"- Synthetic P/L: {synthetic_pnl:.2f}.",
        f"- Net synthetic change: {delta:+.2f}.",
        f"- Baseline win rate: {_pct(baseline_wins, len(rows))}.",
        f"- Synthetic win rate: {_pct(synthetic_wins, len(rows))}.",
        f"- Trades where the synthetic stop triggered: {len(stopped_rows)}.",
        f"- Previously winning trades converted to synthetic losses: {len(false_stop_winners)}.",
        f"- Baseline average loss: {_mean_or_zero(baseline_losses):.2f}.",
        f"- Synthetic average loss: {_mean_or_zero(synthetic_losses):.2f}.",
        f"- Baseline losses at or below -$100: {len(tail_losses)}.",
        "",
        "### Regime Summary",
        "",
        f"- XAUUSD trades: {len(xau_rows)} of {len(rows)}.",
        f"- XAUUSD baseline P/L: {sum(row.trade.pnl for row in xau_rows):.2f}.",
        f"- XAUUSD synthetic P/L: {sum(row.synthetic_pnl for row in xau_rows):.2f}.",
        "",
        "### Trade-Level Simulation",
        "",
        "| ID | Symbol | Side | Baseline P/L | MAE | MFE | Stop Triggered | Synthetic P/L | Delta | Baseline | Synthetic |",
        "|---:|---|---|---:|---:|---:|---|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row.trade.id),
                    row.trade.symbol,
                    row.trade.side,
                    f"{row.trade.pnl:.2f}",
                    f"{row.trade.mae:.2f}",
                    f"{row.trade.mfe:.2f}",
                    "Yes" if row.stop_triggered else "No",
                    f"{row.synthetic_pnl:.2f}",
                    f"{row.pnl_delta:+.2f}",
                    row.baseline_outcome,
                    row.synthetic_outcome,
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "### Target Questions",
            "",
            f"- Did the rule remove losses below -$100 in the cohort? Yes. Baseline had {len(tail_losses)} such losses; synthetic results have 0 because all triggered losses are capped at -$20.",
            f"- Did it stop trades that historically became winners? Yes. {len(false_stop_winners)} baseline winners had MAE <= -$20 and become synthetic -$20 outcomes.",
            f"- Did the cohort become profitable under the synthetic rule? {'Yes' if synthetic_pnl > 0 else 'No'}. Synthetic P/L is {synthetic_pnl:.2f}.",
            "",
            "## Interpretation",
            "",
            "- The synthetic rule materially improves the cohort's P/L by compressing large losses.",
            "- The improvement comes with a meaningful reduction in win rate because several historical winners experienced MAE below -$20 before closing profitably.",
            "- This is a counterfactual result based on recorded final MAE, not proof that real-time fills would occur exactly at -$20.",
            "- The result does not authorize any operating policy modification.",
            "",
            "## Hypothesis candidates",
            "",
            "- Strict loss compression may improve the high-frequency day-trading regime if the system's small-win profile persists.",
            "- The hypothesis is weakened if the winners converted to synthetic losses represent repeatable recoveries rather than noise.",
            "",
            "## Contradiction tests",
            "",
            "- Compare results across future post-regime trades once the sample expands.",
            "- Reconstruct intratrade path from ticks where available to determine whether MAE breach timing occurs before or after favorable movement.",
            "- Test sensitivity at nearby caps, such as -$15, -$25, and -$30, before any adoption review.",
            "",
            "## Open questions",
            "",
            "- Is the `id >= 136` cohort stable enough to define a new regime, or is it a temporary Gold-heavy episode?",
            "- Are XAUUSD MAE values precise enough to infer real-time stop behavior without slippage assumptions?",
            "- Would the synthetic stop alter AA's future admission, portfolio, or risk state in ways not captured by this static replay?",
            "",
            "GM Review Required",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _pct(count: int, total: int) -> str:
    if total == 0:
        return "N/A"
    return f"{count / total:.1%}"


def _mean_or_zero(values: list[float]) -> float:
    if not values:
        return 0.0
    return mean(values)


if __name__ == "__main__":
    main()
