"""Reproduce the Phase 25 MAE stop-loss optimization baseline.

This is a research-only script. It reads the local AA SQLite database and
does not modify trading data, strategy, risk controls, runner state, or Saxo.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "trading_system.sqlite3"

R_DOLLARS = 30.0
SESSION_HOURS_UTC = {1, 2, 9, 10, 11, 12}
STOP_OPTIONS_ATR = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2]

# Static ATR values used by the Phase 25 sandbox. These reproduce the approved
# Phase 25 baseline; dynamic ATR is a separate live-engine concern.
ATRS = {
    "EURUSD": 0.0060,
    "GBPUSD": 0.0080,
    "AUDUSD": 0.0060,
    "NZDUSD": 0.0060,
    "USDCAD": 0.0070,
    "USDCHF": 0.0060,
    "USDJPY": 0.4000,
    "EURJPY": 0.6000,
    "GBPJPY": 0.8000,
    "XAUUSD": 15.000,
    "XAGUSD": 0.5000,
}


def parse_dt(dt_str: str | None) -> datetime | None:
    if not dt_str:
        return None
    dt_str = dt_str.replace("Z", "+00:00")
    try:
        dt_clean = dt_str.split("+")[0].split(".")[0]
        if "T" in dt_clean:
            return datetime.strptime(dt_clean, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
        return datetime.strptime(dt_clean, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    except Exception:
        return None


def load_ticks_for_trade(db_path: Path, symbol: str, start_time_str: str, duration_hours: int = 4) -> list[dict]:
    start_dt = parse_dt(start_time_str)
    if not start_dt:
        return []
    end_dt = start_dt + timedelta(hours=duration_hours)
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT created_at, mid
            FROM challenger_ticks
            WHERE symbol = ? AND created_at >= ?
            ORDER BY id ASC
            """,
            (symbol, start_time_str),
        ).fetchall()
    filtered = []
    for row in rows:
        tick_dt = parse_dt(row["created_at"])
        if tick_dt and start_dt <= tick_dt <= end_dt:
            filtered.append({"timestamp": int(tick_dt.timestamp()), "mid": float(row["mid"])})
    return filtered


def simulate_mae(
    trade: dict,
    ticks: list[dict],
    atr: float,
    *,
    trail_dist_atr: float,
    pyramid_activation_atr: float,
    pyramid_size: float,
    stop_loss_atr: float,
) -> float | None:
    if not ticks:
        return None

    entry = float(trade["entry"])
    side = trade["side"]
    start_ts = int(ticks[0]["timestamp"])

    # Position size scales inversely with stop distance so every tested stop
    # keeps the same nominal $30 risk budget.
    qty = R_DOLLARS / (stop_loss_atr * atr)
    current_stop_loss = entry - (stop_loss_atr * atr) if side == "Buy" else entry + (stop_loss_atr * atr)
    current_max_price = entry
    has_pyramided = False

    for tick in ticks:
        price = float(tick["mid"])
        time_elapsed = int(tick["timestamp"]) - start_ts
        if side == "Buy" and price > current_max_price:
            current_max_price = price
        elif side == "Sell" and price < current_max_price:
            current_max_price = price

        mfe_dist = (current_max_price - entry) if side == "Buy" else (entry - current_max_price)
        current_profit_dist = (price - entry) if side == "Buy" else (entry - price)

        if time_elapsed <= 600 and current_profit_dist <= -stop_loss_atr * atr:
            return -R_DOLLARS

        if not has_pyramided and current_profit_dist >= pyramid_activation_atr * atr:
            has_pyramided = True
            be_dist = 0.33 * atr
            current_stop_loss = entry + be_dist if side == "Buy" else entry - be_dist

        if (side == "Buy" and price <= current_stop_loss) or (side == "Sell" and price >= current_stop_loss):
            if has_pyramided:
                pyramid_loss_dist = pyramid_activation_atr - 0.33
                return (0.33 * atr * qty) - (pyramid_loss_dist * atr * (qty * pyramid_size))
            return -R_DOLLARS

        if mfe_dist >= 1.5 * atr:
            retracement = (current_max_price - price) if side == "Buy" else (price - current_max_price)
            if retracement >= trail_dist_atr * atr:
                exit_dist = mfe_dist - (trail_dist_atr * atr)
                if has_pyramided:
                    return (exit_dist * qty) + ((exit_dist - pyramid_activation_atr * atr) * (qty * pyramid_size))
                return exit_dist * qty

        if time_elapsed >= 7200:
            if has_pyramided:
                return (current_profit_dist * qty) + (
                    (current_profit_dist - pyramid_activation_atr * atr) * (qty * pyramid_size)
                )
            return current_profit_dist * qty

    if has_pyramided:
        return (current_profit_dist * qty) + ((current_profit_dist - pyramid_activation_atr * atr) * (qty * pyramid_size))
    return current_profit_dist * qty


def summarize(pnls: list[float]) -> dict:
    wins = [pnl for pnl in pnls if pnl > 0]
    losses = [pnl for pnl in pnls if pnl < 0]
    net = sum(pnls)
    return {
        "trades": len(pnls),
        "win_rate": len(wins) / len(pnls) if pnls else 0.0,
        "avg_win": sum(wins) / len(wins) if wins else 0.0,
        "avg_loss": sum(losses) / len(losses) if losses else 0.0,
        "net_pnl": net,
        "expectancy": net / len(pnls) if pnls else 0.0,
    }


def run(db_path: Path = DB_PATH) -> dict[float, dict]:
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT symbol, side, entry, created_at
            FROM challenger_trades
            WHERE created_at >= '2026-06-22'
            ORDER BY id ASC
            """
        ).fetchall()

    results = {dist: [] for dist in STOP_OPTIONS_ATR}
    for row in rows:
        trade = dict(row)
        symbol = trade["symbol"]
        atr = ATRS.get(symbol)
        if not atr:
            continue
        opened_at = parse_dt(trade["created_at"])
        if not opened_at or opened_at.hour not in SESSION_HOURS_UTC:
            continue
        ticks = load_ticks_for_trade(db_path, symbol, trade["created_at"])
        if not ticks:
            continue
        for stop_dist in STOP_OPTIONS_ATR:
            pnl = simulate_mae(
                trade,
                ticks,
                atr,
                trail_dist_atr=1.2,
                pyramid_activation_atr=1.0,
                pyramid_size=1.0,
                stop_loss_atr=stop_dist,
            )
            if pnl is not None:
                results[stop_dist].append(pnl)

    return {dist: summarize(pnls) for dist, pnls in results.items() if pnls}


def main() -> None:
    print("\n=================== PHASE 25 INITIAL STOP LOSS OPTIMIZATION (MAE) ===================")
    print("StopLoss | Trades | Win Rate | Avg Win  | Avg Loss | Net PnL  | Expectancy")
    print("-" * 92)
    for dist, metrics in run().items():
        highlight = " <-- PHASE 25 BASELINE" if dist == 0.3 else ""
        previous = " <-- PREVIOUS BASELINE" if dist == 0.5 else ""
        print(
            f"{dist:.1f} ATR  | {metrics['trades']:6d} | {metrics['win_rate']:7.1%} | "
            f"${metrics['avg_win']:6.2f} | ${metrics['avg_loss']:7.2f} | "
            f"${metrics['net_pnl']:7.2f} | ${metrics['expectancy']:9.2f}{highlight}{previous}"
        )
    print("====================================================================================")


if __name__ == "__main__":
    main()
