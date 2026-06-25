#!/usr/bin/env python3
from __future__ import annotations

import csv
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = REPO_ROOT.parent
DB_PATH = PROJECT_ROOT / "trading_system.sqlite3"
REPORT_PATH = REPO_ROOT / "reports" / "mfe_decay_simulation_results.md"
CSV_PATH = REPO_ROOT / "ledgers" / "mfe_decay_simulation_results.csv"

SECONDS_12H = 43_200
MFE_THRESHOLD = 5.0
TAIL_RISK_IDS = {128, 129, 134, 138}
LONG_DURATION_WINNER_IDS = {127, 132, 145}


@dataclass(frozen=True)
class Trade:
    id: int
    created_at: datetime
    symbol: str
    side: str
    quantity: float
    entry: float
    exit: float
    pnl: float
    close_reason: str
    duration_seconds: float
    final_mfe: float
    final_mae: float
    sample_type: str


@dataclass(frozen=True)
class Tick:
    created_at: datetime
    mid: float


@dataclass(frozen=True)
class SimulationRow:
    trade: Trade
    tick_count_to_12h: int
    checkpoint_time: datetime | None
    checkpoint_price: float | None
    mfe_at_12h: float | None
    mae_at_12h: float | None
    pnl_at_12h: float | None
    rule_triggered: bool
    synthetic_pnl: float
    pnl_delta: float
    evidence_quality: str


def main() -> None:
    rows = simulate()
    write_csv(rows)
    write_report(rows)
    print(f"Wrote {CSV_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(REPO_ROOT)}")


def simulate() -> list[SimulationRow]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        trades = _load_long_duration_standard_trades(conn)
        rows = [_simulate_trade(conn, trade) for trade in trades]
    return rows


def _load_long_duration_standard_trades(conn: sqlite3.Connection) -> list[Trade]:
    query = """
        SELECT
            id,
            created_at,
            symbol,
            side,
            quantity,
            entry,
            exit,
            pnl,
            close_reason,
            time_in_trade_seconds,
            mfe,
            mae,
            sample_type
        FROM challenger_trades
        WHERE status = 'Closed'
          AND sample_type = 'standard_signal'
          AND time_in_trade_seconds > ?
        ORDER BY id
    """
    trades = []
    for row in conn.execute(query, (SECONDS_12H,)):
        trades.append(
            Trade(
                id=int(row["id"]),
                created_at=_parse_timestamp(str(row["created_at"])),
                symbol=str(row["symbol"]),
                side=str(row["side"]),
                quantity=float(row["quantity"] or 0),
                entry=float(row["entry"] or 0),
                exit=float(row["exit"] or 0),
                pnl=float(row["pnl"] or 0),
                close_reason=str(row["close_reason"] or ""),
                duration_seconds=float(row["time_in_trade_seconds"] or 0),
                final_mfe=float(row["mfe"] or 0),
                final_mae=float(row["mae"] or 0),
                sample_type=str(row["sample_type"] or ""),
            )
        )
    return trades


def _simulate_trade(conn: sqlite3.Connection, trade: Trade) -> SimulationRow:
    cutoff = trade.created_at + timedelta(seconds=SECONDS_12H)
    ticks = _load_ticks(conn, trade.symbol, trade.created_at, cutoff)
    if not ticks:
        rule_triggered = trade.final_mfe < MFE_THRESHOLD
        synthetic_pnl = trade.pnl if not rule_triggered else trade.final_mae
        return SimulationRow(
            trade=trade,
            tick_count_to_12h=0,
            checkpoint_time=None,
            checkpoint_price=None,
            mfe_at_12h=None,
            mae_at_12h=None,
            pnl_at_12h=None,
            rule_triggered=rule_triggered,
            synthetic_pnl=synthetic_pnl,
            pnl_delta=synthetic_pnl - trade.pnl,
            evidence_quality="fallback_final_mfe_no_ticks",
        )

    pnl_path = [_pnl_at_price(trade, tick.mid) for tick in ticks]
    mfe_at_12h = max(pnl_path)
    mae_at_12h = min(pnl_path)
    checkpoint_tick = min(ticks, key=lambda tick: abs((tick.created_at - cutoff).total_seconds()))
    pnl_at_12h = _pnl_at_price(trade, checkpoint_tick.mid)
    rule_triggered = mfe_at_12h < MFE_THRESHOLD
    synthetic_pnl = pnl_at_12h if rule_triggered else trade.pnl
    return SimulationRow(
        trade=trade,
        tick_count_to_12h=len(ticks),
        checkpoint_time=checkpoint_tick.created_at,
        checkpoint_price=checkpoint_tick.mid,
        mfe_at_12h=mfe_at_12h,
        mae_at_12h=mae_at_12h,
        pnl_at_12h=pnl_at_12h,
        rule_triggered=rule_triggered,
        synthetic_pnl=synthetic_pnl,
        pnl_delta=synthetic_pnl - trade.pnl,
        evidence_quality="tick_reconstructed",
    )


def _load_ticks(conn: sqlite3.Connection, symbol: str, start: datetime, end: datetime) -> list[Tick]:
    query = """
        SELECT created_at, mid
        FROM challenger_ticks
        WHERE symbol = ?
        ORDER BY created_at
    """
    ticks = []
    for row in conn.execute(query, (symbol,)):
        created_at = _parse_timestamp(str(row["created_at"]))
        if start <= created_at <= end:
            ticks.append(Tick(created_at=created_at, mid=float(row["mid"] or 0)))
    return ticks


def _pnl_at_price(trade: Trade, price: float) -> float:
    if trade.side.lower() == "buy":
        return (price - trade.entry) * trade.quantity
    return (trade.entry - price) * trade.quantity


def write_csv(rows: Iterable[SimulationRow]) -> None:
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "trade_id",
                "symbol",
                "side",
                "duration_seconds",
                "final_pnl",
                "final_mfe",
                "final_mae",
                "tick_count_to_12h",
                "checkpoint_time",
                "checkpoint_price",
                "mfe_at_12h",
                "mae_at_12h",
                "pnl_at_12h",
                "rule_triggered",
                "synthetic_pnl",
                "pnl_delta",
                "evidence_quality",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row.trade.id,
                    row.trade.symbol,
                    row.trade.side,
                    round(row.trade.duration_seconds, 2),
                    round(row.trade.pnl, 2),
                    round(row.trade.final_mfe, 2),
                    round(row.trade.final_mae, 2),
                    row.tick_count_to_12h,
                    row.checkpoint_time.isoformat() if row.checkpoint_time else "",
                    round(row.checkpoint_price, 5) if row.checkpoint_price is not None else "",
                    round(row.mfe_at_12h, 2) if row.mfe_at_12h is not None else "",
                    round(row.mae_at_12h, 2) if row.mae_at_12h is not None else "",
                    round(row.pnl_at_12h, 2) if row.pnl_at_12h is not None else "",
                    int(row.rule_triggered),
                    round(row.synthetic_pnl, 2),
                    round(row.pnl_delta, 2),
                    row.evidence_quality,
                ]
            )


def write_report(rows: list[SimulationRow]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    triggered = [row for row in rows if row.rule_triggered]
    not_triggered = [row for row in rows if not row.rule_triggered]
    baseline = sum(row.trade.pnl for row in rows)
    synthetic = sum(row.synthetic_pnl for row in rows)
    delta = synthetic - baseline
    tail_rows = [row for row in rows if row.trade.id in TAIL_RISK_IDS]
    winner_rows = [row for row in rows if row.trade.id in LONG_DURATION_WINNER_IDS]

    lines = [
        "# MFE-Decay Exit Simulation Results",
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
        "- Source table: `challenger_trades` joined with `challenger_ticks` by symbol and timestamp window.",
        f"- Cohort: closed `standard_signal` trades with `time_in_trade_seconds > {SECONDS_12H}`.",
        f"- Trades reviewed: {len(rows)}",
        f"- Rule tested: after 12 hours, exit if reconstructed MFE at the 12-hour checkpoint is below ${MFE_THRESHOLD:.2f}.",
        f"- Baseline cohort P/L: {baseline:.2f}",
        f"- Synthetic cohort P/L: {synthetic:.2f}",
        f"- Net synthetic change: {delta:+.2f}",
        "",
        "| Trade ID | Symbol | Side | Duration h | Final P/L | MFE 12h | P/L 12h | Triggered | Synthetic P/L | Delta | Evidence |",
        "|---:|---|---|---:|---:|---:|---:|---|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row.trade.id),
                    row.trade.symbol,
                    row.trade.side,
                    f"{row.trade.duration_seconds / 3600:.2f}",
                    f"{row.trade.pnl:.2f}",
                    _fmt(row.mfe_at_12h),
                    _fmt(row.pnl_at_12h),
                    "Yes" if row.rule_triggered else "No",
                    f"{row.synthetic_pnl:.2f}",
                    f"{row.pnl_delta:+.2f}",
                    row.evidence_quality,
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "### Target Tail-Risk Trades",
            "",
            _target_summary(tail_rows),
            "",
            "### Long-Duration Winner Protection Check",
            "",
            _target_summary(winner_rows),
            "",
            "## Interpretation",
            "",
            f"- The rule triggered on {len(triggered)} of {len(rows)} long-duration trades.",
            f"- The rule did not trigger on {len(not_triggered)} long-duration trades.",
            f"- Target tail-risk trades caught: {sorted(row.trade.id for row in tail_rows if row.rule_triggered)}.",
            f"- Target long-duration winners accidentally killed: {sorted(row.trade.id for row in winner_rows if row.rule_triggered)}.",
            f"- In this historical cohort, the synthetic rule changes P/L by {delta:+.2f}.",
            "- This is a counterfactual simulation only. It does not authorize any operating policy modification.",
            "",
            "## Hypothesis candidates",
            "",
            "- Time-decayed MFE invalidation remains a candidate if it reduces tail-risk losses without materially cutting long-duration winners.",
            "- The candidate is weakened if checkpoint MFE cannot separate dead trades from valid long-duration winners.",
            "",
            "## Contradiction tests",
            "",
            "- Re-test on future standard-signal trades after the current sample expands.",
            "- Compare 12-hour MFE against score, side, and symbol to determine whether the rule is only masking entry-quality problems.",
            "- Reconstruct path using denser tick history if available before any adoption review.",
            "",
            "## Open questions",
            "",
            "- Does sparse tick capture understate or overstate true 12-hour MFE?",
            "- Is the 12-hour checkpoint economically meaningful across FX and metals, or only for the current sample?",
            "- Would a smaller or larger MFE threshold produce a materially different separation?",
            "",
            "GM Review Required",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _target_summary(rows: list[SimulationRow]) -> str:
    if not rows:
        return "- No matching target rows found."
    caught = [row.trade.id for row in rows if row.rule_triggered]
    missed = [row.trade.id for row in rows if not row.rule_triggered]
    delta = sum(row.pnl_delta for row in rows)
    return f"- Reviewed IDs: {sorted(row.trade.id for row in rows)}; triggered: {sorted(caught)}; not triggered: {sorted(missed)}; P/L delta: {delta:+.2f}."


def _fmt(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:.2f}"


def _parse_timestamp(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is not None:
        return parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


if __name__ == "__main__":
    main()
