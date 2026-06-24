from datetime import date
import os
from pathlib import Path

import streamlit as st

from saxo_trader.aa_decision import aa_active_mandate, aa_operating_decision
from saxo_trader.anomaly_scanner import anomaly_snapshot, clear_current_anomalies
from saxo_trader.challenger import run_challenger_cycle
from saxo_trader.challenger_review import (
    challenger_closed_trade_reviews,
    challenger_equity_snapshot,
    challenger_open_positions_with_live_pnl,
)
from saxo_trader.config import load_settings
from saxo_trader.execution_analyst import execution_analyst_snapshot
from saxo_trader.feedback_loop import evaluate_feedback
from saxo_trader.goals import challenger_score, goal_snapshot, human_score
from saxo_trader.macro_regime_analyst import macro_regime_snapshot
from saxo_trader.market_data_analyst import market_data_snapshot
from saxo_trader.mentor import mentor_brief
from saxo_trader.promotion import aa_promotion_snapshot
from saxo_trader.portfolio_manager import portfolio_manager_snapshot
from saxo_trader.risk_officer import risk_officer_snapshot
from saxo_trader.saxo_client import SaxoClient
from saxo_trader.staff_governance import support_staff_accountability
from saxo_trader.storage import TradeStore
from saxo_trader.strategy_researcher import strategy_researcher_snapshot
from saxo_trader.systems_reliability import systems_reliability_snapshot
from saxo_trader.sync import sync_historical_positions
from saxo_trader.team_architect import team_architect_brief
from saxo_trader.team_meeting import first_team_meeting
from saxo_trader.trade_reviewer import trade_reviewer_snapshot


st.set_page_config(page_title="Saxo Command Center", layout="wide")
st.title("Saxo Trading Command Center")

settings = load_settings()
store = TradeStore(settings.database_path)


def _update_env_value(key: str, value: str, env_path: Path = Path("/Users/kennylee/Documents/Saxo/.env")) -> None:
    lines = env_path.read_text().splitlines() if env_path.exists() else []
    replacement = f"{key}={value.strip()}"
    updated = False
    for index, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[index] = replacement
            updated = True
            break
    if not updated:
        lines.append(replacement)
    env_path.write_text("\n".join(lines) + "\n")
    os.environ[key] = value.strip()


def _update_watchlist_value(instruments: list[object]) -> None:
    value = ",".join(f"{item.label}|{item.uic}|{item.asset_type}" for item in instruments)
    _update_env_value("SAXO_WATCHLIST", value)


def _saxo_error_message(exc: Exception) -> str:
    text = str(exc)
    if "401" in text or "Unauthorized" in text:
        return "Could not load Saxo data: authentication failed. Refresh SAXO_ACCESS_TOKEN in /Users/kennylee/Documents/Saxo/.env."
    if "gateway.saxobank.com" in text:
        return "Could not load Saxo data: Saxo API connection failed. Check internet access and token validity."
    return f"Could not load Saxo data: {type(exc).__name__}"

st.sidebar.metric("Environment", "SIM")
st.sidebar.metric("Dry Run", str(settings.dry_run))
st.sidebar.metric("Kill Switch", str(settings.kill_switch))
st.sidebar.metric("Max Margin", f"{settings.max_margin_utilisation:.0%}")
with st.sidebar.expander("Refresh Saxo Token"):
    new_token = st.text_input("New SIM access token", type="password")
    if st.button("Save Token"):
        if new_token.strip():
            _update_env_value("SAXO_ACCESS_TOKEN", new_token)
            st.success("Token saved. Restart the dashboard and runner.")
        else:
            st.error("Paste the new token first.")

st.subheader("Refresh Saxo Token")
st.caption("Paste a new Saxo SIM access token here. It will be saved to .env and hidden from view.")
page_token = st.text_input("New SIM access token", type="password", key="page_saxo_token")
if st.button("Save Saxo Token", key="page_save_saxo_token"):
    if page_token.strip():
        _update_env_value("SAXO_ACCESS_TOKEN", page_token)
        st.success("Token saved. Restart the dashboard and AI Challenger runner.")
    else:
        st.error("Paste the new token first.")

balance = None
positions = []
quotes = []
fetch_errors = []

try:
    client = SaxoClient(
        access_token=settings.access_token,
        account_key=settings.account_key,
        client_key=settings.client_key,
        uics=settings.uics,
        base_url=settings.base_url,
    )
except Exception as exc:
    client = None
    st.error(_saxo_error_message(exc))

if client:
    try:
        balance = client.get_account_balance()
    except Exception as exc:
        fetch_errors.append(f"Balance: {_saxo_error_message(exc)}")
    try:
        positions = client.get_open_positions()
    except Exception as exc:
        fetch_errors.append(f"Open positions: {_saxo_error_message(exc)}")
    for instrument in settings.watchlist:
        try:
            quotes.append(client.get_instrument_price(instrument))
        except Exception as exc:
            fetch_errors.append(f"{instrument.label} price: {_saxo_error_message(exc)}")

for message in fetch_errors[:5]:
    st.warning(message)
if len(fetch_errors) > 5:
    st.caption(f"{len(fetch_errors) - 5} more Saxo fetch issue(s) hidden.")

goal_tab, challenger_tab, team_tab, history_tab = st.tabs(
    [
        "Goal Tracker",
        "AI Challenger",
        "AA Team",
        "Saxo History",
    ]
)

with goal_tab:
    st.subheader("SGD 1,000,000 Goal")
    current_capital = settings.goal.current_capital or settings.goal.starting_capital
    st.caption("The race uses your challenge capital below. Saxo SIM account value is shown separately and is not used as your score.")
    human_capital_input = st.number_input(
        "Human Challenge Capital",
        min_value=0.0,
        value=float(current_capital),
        step=100.0,
        format="%.2f",
    )
    if st.button("Save Human Capital"):
        _update_env_value("GOAL_CURRENT_CAPITAL", str(human_capital_input))
        st.success("Human challenge capital saved.")
        st.rerun()
    current_capital = human_capital_input

    goal = goal_snapshot(settings.goal, current_capital)
    human = human_score(settings.goal, current_capital)
    challenger_snapshot = challenger_equity_snapshot(store, settings.challenger.starting_capital, quotes)
    challenger_capital = challenger_snapshot["marked_capital"]
    challenger = challenger_score(settings.challenger, challenger_capital)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current Capital", f"{goal.current_capital:,.2f} {settings.goal.currency}")
    c2.metric("Target", f"{goal.target_capital:,.0f} {settings.goal.currency}")
    c3.metric("Distance", f"{goal.distance_to_target:,.2f} {settings.goal.currency}")
    c4.metric("Required Multiple", f"{goal.required_multiple:.2f}x")
    if balance:
        st.caption(f"Saxo SIM account value: {balance.account_value:,.2f} {balance.currency}")

    st.progress(goal.progress_pct)
    months = "Already there" if goal.estimated_months is None and goal.distance_to_target == 0 else goal.estimated_months
    st.write(
        {
            "monthly_growth_assumption": f"{settings.goal.monthly_growth_pct:.1%}",
            "estimated_months_to_target": months,
        }
    )

    st.subheader("Human vs AI Challenger")
    st.dataframe(
        [
            human.__dict__,
            challenger.__dict__,
        ],
        use_container_width=True,
    )

    st.subheader("AI Challenger Rules")
    st.write(
        {
            "virtual_starting_capital": settings.challenger.starting_capital,
            "target_capital": settings.challenger.target_capital,
            "max_daily_loss": settings.challenger.max_daily_loss,
            "max_risk_per_trade": settings.challenger.max_risk_per_trade,
            "max_trades_per_day": settings.challenger.max_trades_per_day,
            "min_ticks_for_signal": settings.challenger.min_ticks_for_signal,
            "momentum_threshold_pct": f"{settings.challenger.momentum_threshold_pct:.3%}",
            "stop_loss_pct": f"{settings.challenger.stop_loss_pct:.2%}",
            "take_profit_pct": f"{settings.challenger.take_profit_pct:.2%}",
        }
    )

    st.subheader("Background Runner")
    runner_log = Path("outputs/challenger_runner.log")
    if runner_log.exists():
        lines = runner_log.read_text().splitlines()[-5:]
        st.code("\n".join(lines))
    else:
        st.info("Background runner has not logged any cycles yet.")

    st.subheader("AA Latest Activity")
    st.caption("Latest structured AA activity from the autonomous FX day-trader loop.")
    latest_activity = store.recent_aa_journal(12)
    if latest_activity:
        st.dataframe(latest_activity, use_container_width=True)
    else:
        st.info("No AA activity has been logged yet. The next runner cycle will write SCOUT rows even if Saxo prices are unavailable.")
    st.write("Latest Blocked Signals")
    latest_blocked = store.recent_blocked_signals(12)
    if latest_blocked:
        st.dataframe(latest_blocked, use_container_width=True)
    else:
        st.info("No blocked entry signals yet.")

    st.subheader("Saxo SIM Snapshot")
    st.caption("Compact live account context. Detailed trading work happens through AA.")
    if balance:
        c1, c2, c3 = st.columns(3)
        c1.metric("Account Value", f"{balance.account_value:,.2f} {balance.currency}")
        c2.metric("Cash Balance", f"{balance.cash_balance:,.2f} {balance.currency}")
        c3.metric("Margin Utilisation", f"{balance.margin_utilisation:.1%}")
    if positions:
        st.write("Saxo Open Positions")
        st.dataframe(
            [
                {
                    "symbol": position.symbol,
                    "asset_type": position.asset_type,
                    "amount": position.amount,
                    "market_value": position.market_value,
                    "unrealized_pnl": position.unrealized_pnl,
                    "pnl_pct": None if position.pnl_pct is None else round(position.pnl_pct * 100, 2),
                }
                for position in positions
            ],
            use_container_width=True,
        )
    st.write("Live Watchlist Prices")
    st.dataframe(
        [
            {
                "symbol": q.symbol,
                "asset_type": q.asset_type,
                "bid": q.bid,
                "ask": q.ask,
                "mid": q.mid,
                "timestamp": q.timestamp.isoformat(),
            }
            for q in quotes
        ],
        use_container_width=True,
    )

with challenger_tab:
    st.subheader("AI Challenger")
    st.caption("Paper competitor using live Saxo prices. These are not Saxo account positions and no real orders are placed.")
    challenger_snapshot = challenger_equity_snapshot(store, settings.challenger.starting_capital, quotes)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Marked Capital", f"{challenger_snapshot['marked_capital']:,.2f} {settings.goal.currency}")
    c2.metric("Realized P/L", f"{challenger_snapshot['realized_pnl']:,.2f}")
    c3.metric("Unrealized P/L", f"{challenger_snapshot['unrealized_pnl']:,.2f}")
    c4.metric("Open Positions", challenger_snapshot["open_positions"])

    st.subheader("Ari Axelrod Rank")
    promotion = aa_promotion_snapshot(store, settings.challenger.starting_capital)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("AA Rank", promotion["rank"])
    c2.metric("Closed Trades", promotion["closed_trades"])
    c3.metric("Expectancy", f"{promotion['expectancy']:,.2f}")
    c4.metric("Profit Factor", promotion["profit_factor"] or "N/A")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Max Drawdown", f"{promotion['max_drawdown_pct']:.2f}%")
    c2.metric("Risk Violations", promotion["risk_violations"])
    c3.metric("Explanation Quality", promotion["explanation_quality"])
    c4.metric("Next Rank", promotion["next_rank"])
    st.progress(promotion["promotion_progress"])
    st.caption(f"Next unlock: {promotion['next_unlock']}")
    st.caption(f"Promotion requirements: {promotion['requirements']}")
    graduation = promotion["training_graduation"]
    st.caption(f"Training graduation: {graduation['status']} - {graduation['summary']}")
    st.dataframe(graduation["criteria"], use_container_width=True)

    if st.button("Run Challenger Cycle"):
        result = run_challenger_cycle(store, settings.challenger, quotes)
        st.session_state["last_challenger_matrix"] = result.matrix or []
        st.success(f"Opened {result.opened} paper position(s), closed {result.closed}.")
        if result.skipped:
            st.write(result.skipped[:10])
    if st.session_state.get("last_challenger_matrix"):
        st.subheader("Latest Day-Trader Decision Matrix")
        st.dataframe(st.session_state["last_challenger_matrix"], use_container_width=True)

    st.subheader("AA Operating Decision")
    aa_decision = aa_operating_decision(store, settings.challenger, quotes)
    c1, c2, c3 = st.columns(3)
    c1.metric("Decision Maker", aa_decision["name"])
    c2.metric("Action", aa_decision["action"])
    c3.metric("Authority", "Intern")
    st.write(aa_decision["conclusion"])
    if aa_decision["blockers"]:
        for blocker in aa_decision["blockers"]:
            st.warning(blocker)
    st.dataframe(aa_decision["staff_inputs"], use_container_width=True)
    st.write("Recent AA Decisions")
    st.dataframe(store.recent_aa_decisions(), use_container_width=True)

    st.subheader("AA Active Mandate")
    aa_mandate = aa_active_mandate(store, settings.challenger, quotes)
    c1, c2, c3 = st.columns(3)
    c1.metric("Mode", aa_mandate["mode"])
    c2.metric("Open Positions", aa_mandate["open_positions"])
    c3.metric("Activity", "Required")
    st.info(aa_mandate["current_duty"])
    st.caption(aa_mandate["activity_standard"])
    st.dataframe([{"requirement": item} for item in aa_mandate["cycle_requirements"]], use_container_width=True)

    st.subheader("Recent FX Day-Trader Activity")
    st.caption("ENTRY, EXIT, HOLD, and SCOUT records are written every active cycle.")
    recent_fx_activity = store.recent_aa_journal(50)
    if recent_fx_activity:
        st.dataframe(recent_fx_activity, use_container_width=True)
    else:
        st.info("No FX day-trader activity yet. Runner cycles now log DATA_UNAVAILABLE scouts if Saxo quote fetch fails.")
    st.write("Blocked Signal Diagnostics")
    blocked_diagnostics = store.recent_blocked_signals(50)
    if blocked_diagnostics:
        st.dataframe(blocked_diagnostics, use_container_width=True)
    else:
        st.info("No blocked entry signals yet.")
    st.write("Post-Stop Quarantine")
    quarantines = store.recent_symbol_quarantines(20)
    if quarantines:
        st.dataframe(quarantines, use_container_width=True)
    else:
        st.info("No post-stop quarantines yet.")

    st.subheader("Open Paper Positions")
    open_challenger = challenger_open_positions_with_live_pnl(store, quotes)
    if open_challenger:
        st.dataframe(open_challenger, use_container_width=True)
    else:
        st.info("No open AI Challenger paper positions.")

    st.subheader("Closed Trade Reviews")
    anomalies = anomaly_snapshot(store)
    c1, c2, c3 = st.columns(3)
    c1.metric("Anomaly Status", anomalies["status"])
    c2.metric("Critical", anomalies["critical_count"])
    c3.metric("Warnings", anomalies["warning_count"])
    st.caption(anomalies["summary"])
    if anomalies["anomalies"]:
        st.dataframe(anomalies["anomalies"], use_container_width=True)
        st.write("Anomaly Clearance")
        st.caption("Use only after the lesson has been converted into a rule or operating control.")
        clearance_text = st.text_input("Type CLEAR AA ANOMALIES to acknowledge current lessons", key="anomaly_clearance_text")
        clearance_reason = st.text_area(
            "Clearance reason",
            value="Lessons captured: runner lock, anomaly gate, stricter admission score, and metals risk reduction are active.",
            key="anomaly_clearance_reason",
        )
        if st.button("Clear Current Anomalies", disabled=clearance_text != "CLEAR AA ANOMALIES"):
            cleared = clear_current_anomalies(store, clearance_reason)
            st.success(f"Cleared {cleared} current anomaly group(s). New future anomalies will still block AA.")
            st.rerun()
    else:
        st.success("No AA ledger anomalies detected.")
    clearances = store.recent_anomaly_clearances(20)
    if clearances:
        with st.expander("Cleared Anomaly Lessons", expanded=False):
            st.dataframe(clearances, use_container_width=True)

    reviews = challenger_closed_trade_reviews(store)
    if reviews:
        for review in reviews:
            title = (
                f"#{review['id']} {review['symbol']} {review['side']} - "
                f"{review['outcome']} {float(review.get('pnl') or 0):,.2f}"
            )
            with st.expander(title, expanded=False):
                st.write("Conclusion")
                if review["outcome"] == "Win":
                    st.success(review["verdict"])
                elif review["outcome"] == "Loss":
                    st.error(review["verdict"])
                else:
                    st.info(review["verdict"])
                st.write(review["conclusion"])
                st.caption(review["evidence_level"])

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Entry", f"{float(review.get('entry') or 0):,.5f}")
                c2.metric("Exit", f"{float(review.get('exit') or 0):,.5f}")
                c3.metric("P/L", f"{float(review.get('pnl') or 0):,.2f}")
                c4.metric("Held", review.get("time_held") or "N/A")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Planned Risk", f"{float(review.get('planned_risk') or 0):,.2f}")
                c2.metric("Planned Reward", f"{float(review.get('planned_reward') or 0):,.2f}")
                c3.metric("Best Open P/L", "N/A" if review.get("max_favorable_pnl") is None else f"{review['max_favorable_pnl']:,.2f}")
                c4.metric("Worst Open P/L", "N/A" if review.get("max_adverse_pnl") is None else f"{review['max_adverse_pnl']:,.2f}")
                st.write("Why it was taken")
                st.info(review["entry_reason"])
                st.write("Why it closed")
                st.warning(review["close_reason"] or "Close condition not recorded.")
                st.write("Review")
                st.write(review["review"])
                st.write("Takeaway")
                st.success(review["takeaway"])
                st.write("Next Action")
                st.info(review["next_action"])
    else:
        st.info("No closed AI Challenger trades yet.")

    st.subheader("AA Decision Journal")
    st.caption("Every autonomous paper-trading action should explain why AA entered, held, exited, or skipped a pair.")
    st.dataframe(store.recent_aa_journal(), use_container_width=True)

    st.subheader("Signals and Simulated Orders")
    c1, c2 = st.columns(2)
    with c1:
        st.write("Recent Signals")
        st.dataframe(store.recent_signals(), use_container_width=True)
    with c2:
        st.write("Legacy Simulated Orders")
        st.dataframe(store.recent_orders(), use_container_width=True)

with team_tab:
    st.subheader("AA Team Meeting #2")
    meeting = first_team_meeting(store, settings.challenger, settings.watchlist, quotes, fetch_errors)
    c1, c2 = st.columns(2)
    c1.metric("Chair", meeting["chair"])
    c2.metric("Role", meeting["chair_role"])
    st.write("Vision")
    st.info(meeting["vision"])
    st.write("Attendees")
    st.dataframe(meeting["attendees"], use_container_width=True)
    st.write("Feedback")
    for item in meeting["feedback"]:
        with st.expander(item["speaker"], expanded=False):
            st.write(item["feedback"])
    st.write("Agreed Actions")
    st.dataframe([{"action": action} for action in meeting["agreed_actions"]], use_container_width=True)
    st.write("Open Questions")
    st.dataframe([{"question": question} for question in meeting["open_questions"]], use_container_width=True)

    st.subheader("AA Mentor")
    mentor = mentor_brief(store, settings.challenger)
    c1, c2 = st.columns(2)
    c1.metric("Mentor", mentor["name"])
    c2.metric("Rank", mentor["rank"])
    st.caption(mentor["mandate"])
    st.info(mentor["current_read"])
    st.write("Training Focus")
    st.warning(mentor["training_focus"])
    st.write("Mentor Advice")
    st.write(mentor["mentor_advice"])
    st.write("Do Next")
    st.success(mentor["do_next"])
    st.write("Do Not Do")
    st.error(mentor["do_not_do"])
    st.caption(mentor["promotion_gate"])
    st.write("Mentor Accountability")
    c1, c2 = st.columns(2)
    c1.metric("Mentor Status", mentor["mentor_status"])
    c2.metric("Accountability Basis", "Evidence + Risk")
    st.write(mentor["mentor_review"])
    st.caption(mentor["mentor_scorecard"])
    with st.expander("Mentor PIP / Replacement Rules"):
        st.write("PIP triggers")
        st.write(mentor["pip_triggers"])
        st.write("Replacement rule")
        st.warning(mentor["replacement_rule"])

    st.subheader("AA Team Architect")
    brief = team_architect_brief(store, settings.challenger.starting_capital)
    c1, c2, c3 = st.columns(3)
    c1.metric("Architect", brief["name"])
    c2.metric("Rank", brief["rank"])
    c3.metric("Status", brief["status"])
    st.caption(brief["mission"])
    st.write("Current Assessment")
    st.info(brief["current_assessment"])
    st.write("Operating Principle")
    st.write(brief["operating_principle"])

    st.subheader("AA Performance Loop")
    st.caption("Sofia's loop for how each specialist improves AA, trade by trade.")
    st.dataframe(brief["aa_performance_loop"], use_container_width=True)

    st.subheader("Specialist Department Blueprints")
    st.caption("Each founding specialist owns a department. Departments expand only when evidence shows a measured gap.")
    st.dataframe(brief["department_blueprints"], use_container_width=True)

    st.subheader("AA Team-Build Requests")
    st.caption("AA may request help. Sofia decides whether it is a valid department build, tooling request, promotion issue, or no action.")
    st.write("Current Requests")
    st.dataframe(brief["aa_current_team_requests"], use_container_width=True)
    st.write("Request Rules")
    st.dataframe(brief["aa_team_build_guidance"], use_container_width=True)

    st.subheader("Next Specialist To Build")
    next_build = brief["next_build"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Priority", next_build["priority"])
    c2.metric("Role", next_build["role"])
    c3.metric("Rank", next_build["rank"])
    c4.metric("Status", next_build["status"])
    st.write("Purpose")
    st.write(next_build["purpose"])
    st.write("Why Now")
    st.warning(next_build["why_now"])
    st.write("First Capability")
    st.write(next_build["first_capability"])
    st.write("Veto Power")
    st.info(next_build["veto_power"])

    st.subheader("Team Roadmap")
    st.dataframe(brief["team_roadmap"], use_container_width=True)

    st.subheader("Risk Officer v1")
    risk_brief = risk_officer_snapshot(store, settings.challenger)
    c1, c2, c3 = st.columns(3)
    c1.metric("Risk Officer", risk_brief["name"])
    c2.metric("Rank", risk_brief["rank"])
    c3.metric("Agent Status", risk_brief["agent_status"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Status", risk_brief["status"])
    c2.metric("Portfolio Heat", f"{risk_brief['portfolio_heat_pct']:.2f}%")
    c3.metric("Max Loss If Stops Hit", f"{risk_brief['max_loss_if_stops_hit']:,.2f}")
    c4.metric("Daily Loss Remaining", f"{risk_brief['daily_loss_remaining']:,.2f}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Open Positions", risk_brief["open_positions"])
    c2.metric("USD Long Count", risk_brief["usd_long_count"])
    c3.metric("USD Short Count", risk_brief["usd_short_count"])
    c4.metric("Metals Count", risk_brief["metals_count"])
    if risk_brief["warnings"]:
        for warning in risk_brief["warnings"]:
            st.warning(warning)
    else:
        st.success("Risk Officer is clear: no current veto condition.")
    st.dataframe(risk_brief["position_risks"], use_container_width=True)

    st.subheader("Systems Reliability Officer v1")
    systems = systems_reliability_snapshot()
    c1, c2, c3 = st.columns(3)
    c1.metric("Systems Officer", systems["name"])
    c2.metric("Rank", systems["rank"])
    c3.metric("Agent Status", systems["agent_status"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Status", systems["status"])
    c2.metric("Runner State", systems["runner_state"])
    c3.metric("Lock Blocks", systems["recent_lock_blocks"])
    c4.metric("Data Errors", systems["recent_data_errors"])
    c1, c2 = st.columns(2)
    c1.metric(
        "Last Cycle Age",
        "N/A" if systems["last_cycle_age_minutes"] is None else f"{systems['last_cycle_age_minutes']:.1f} min",
    )
    c2.metric("Launch Error Log", f"{systems['launchd_error_log_mb']:.2f} MB")
    st.caption(systems["veto_power"])
    if systems["warnings"]:
        for warning in systems["warnings"]:
            st.warning(warning)
    else:
        st.success("Systems Reliability is clear: runner and Saxo plumbing look usable.")
    st.write("PID Checks")
    st.dataframe(systems["pid_checks"], use_container_width=True)
    st.write("Last Runner Line")
    st.code(systems["last_runner_line"])

    st.subheader("Market Data Analyst v1")
    data_brief = market_data_snapshot(store, settings.watchlist, quotes, fetch_errors)
    c1, c2, c3 = st.columns(3)
    c1.metric("Data Analyst", data_brief["name"])
    c2.metric("Rank", data_brief["rank"])
    c3.metric("Agent Status", data_brief["agent_status"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Status", data_brief["status"])
    c2.metric("Tradable Symbols", data_brief["tradable_symbols"])
    c3.metric("Watchlist Symbols", data_brief["watchlist_symbols"])
    st.caption(data_brief["veto_power"])
    if data_brief["warnings"]:
        for warning in data_brief["warnings"][:5]:
            st.warning(warning)
    else:
        st.success("Market Data Analyst is clear: current symbol data is usable.")
    st.dataframe(data_brief["symbol_quality"], use_container_width=True)

    st.subheader("Trade Reviewer v1")
    reviewer = trade_reviewer_snapshot(store)
    c1, c2, c3 = st.columns(3)
    c1.metric("Trade Reviewer", reviewer["name"])
    c2.metric("Rank", reviewer["rank"])
    c3.metric("Agent Status", reviewer["agent_status"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Closed Reviews", reviewer["closed_reviews"])
    c2.metric("Review Quality", f"{reviewer['review_quality_pct']:.1f}%")
    c3.metric("Loss Clusters", len(reviewer["loss_clusters"]))
    st.caption(reviewer["veto_power"])
    if reviewer["warnings"]:
        for warning in reviewer["warnings"]:
            st.warning(warning)
    else:
        st.success("Trade Reviewer is clear: no repeated loss cluster yet.")
    st.dataframe(reviewer["loss_clusters"], use_container_width=True)

    st.subheader("Strategy Researcher v1")
    researcher = strategy_researcher_snapshot(store)
    c1, c2, c3 = st.columns(3)
    c1.metric("Strategy Researcher", researcher["name"])
    c2.metric("Rank", researcher["rank"])
    c3.metric("Agent Status", researcher["agent_status"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Closed Trades", researcher["closed_trades"])
    c2.metric("Setups Reviewed", researcher["setups_reviewed"])
    c3.metric("Veto Power", "Research")
    st.caption(researcher["veto_power"])
    if researcher["warnings"]:
        for warning in researcher["warnings"]:
            st.warning(warning)
    else:
        st.success("Strategy Researcher is clear: no strategy quarantine yet.")
    st.write("Current Conclusion")
    st.info(researcher["current_conclusion"])
    st.write("Next Test")
    st.write(researcher["next_test"])
    st.dataframe(researcher["setup_research"], use_container_width=True)

    st.subheader("Execution Analyst v1")
    execution = execution_analyst_snapshot(store)
    c1, c2, c3 = st.columns(3)
    c1.metric("Execution Analyst", execution["name"])
    c2.metric("Rank", execution["rank"])
    c3.metric("Agent Status", execution["agent_status"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Closed Trades Reviewed", execution["closed_trades_reviewed"])
    c2.metric("Weak Execution Count", execution["weak_execution_count"])
    c3.metric("Veto Power", "Execution")
    st.caption(execution["veto_power"])
    if execution["warnings"]:
        for warning in execution["warnings"]:
            st.warning(warning)
    else:
        st.success("Execution Analyst is clear: no persistent execution issue yet.")
    st.write("Current Conclusion")
    st.info(execution["current_conclusion"])
    st.write("Next Action")
    st.write(execution["next_action"])
    st.dataframe(execution["execution_quality"], use_container_width=True)

    st.subheader("Macro Regime Analyst v1")
    macro = macro_regime_snapshot(store, settings.watchlist, quotes)
    c1, c2, c3 = st.columns(3)
    c1.metric("Macro Regime Analyst", macro["name"])
    c2.metric("Rank", macro["rank"])
    c3.metric("Agent Status", macro["agent_status"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Risk Tone", macro["risk_tone"])
    c2.metric("USD Regime", macro["usd_regime"])
    c3.metric("Metals Regime", macro["metals_regime"])
    c4.metric("Volatility", macro["volatility_state"])
    st.caption(macro["veto_power"])
    if macro["warnings"]:
        for warning in macro["warnings"]:
            st.warning(warning)
    else:
        st.success("Macro Regime Analyst is clear: no regime warning yet.")
    st.write("Current Conclusion")
    st.info(macro["current_conclusion"])
    st.write("Next Action")
    st.write(macro["next_action"])
    st.dataframe(macro["symbol_regimes"], use_container_width=True)

    st.subheader("Portfolio Manager v1")
    portfolio = portfolio_manager_snapshot(store, quotes)
    c1, c2, c3 = st.columns(3)
    c1.metric("Portfolio Manager", portfolio["name"])
    c2.metric("Rank", portfolio["rank"])
    c3.metric("Agent Status", portfolio["agent_status"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Status", portfolio["status"])
    c2.metric("Open Positions", portfolio["open_positions"])
    c3.metric("Metals Cap", portfolio["max_metals_positions"])
    st.caption(portfolio["veto_power"])
    if portfolio["warnings"]:
        for warning in portfolio["warnings"]:
            st.warning(warning)
    else:
        st.success("Portfolio Manager is clear: no concentration issue.")
    st.write("Currency Exposure")
    st.dataframe(portfolio["currency_exposure"], use_container_width=True)
    st.write("Reduction Candidates")
    st.dataframe(portfolio["reduction_candidates"], use_container_width=True)

    st.subheader("Feedback Loop")
    feedback_rows = evaluate_feedback(meeting["open_questions"], portfolio)
    st.dataframe(feedback_rows, use_container_width=True)

    st.subheader("Support Staff Accountability")
    st.caption("AA is trained, not replaced. Supporting staff can be promoted, demoted, placed in PIP, or replaced.")
    staff_rows = support_staff_accountability(
        [
            {"name": mentor["name"], "role": "Mentor", "rank": mentor["rank"], "status": mentor["mentor_status"]},
            {"name": brief["name"], "role": "Team Architect", "rank": brief["rank"], "status": brief["status"]},
            {"name": risk_brief["name"], "role": "Risk Officer", "rank": risk_brief["rank"], "status": risk_brief["agent_status"]},
            {"name": systems["name"], "role": systems["role"], "rank": systems["rank"], "status": systems["agent_status"]},
            {"name": data_brief["name"], "role": "Market Data Analyst", "rank": data_brief["rank"], "status": data_brief["agent_status"]},
            {"name": reviewer["name"], "role": "Trade Reviewer", "rank": reviewer["rank"], "status": reviewer["agent_status"]},
            {"name": researcher["name"], "role": "Strategy Researcher", "rank": researcher["rank"], "status": researcher["agent_status"]},
            {"name": execution["name"], "role": "Execution Analyst", "rank": execution["rank"], "status": execution["agent_status"]},
            {"name": macro["name"], "role": "Macro Regime Analyst", "rank": macro["rank"], "status": macro["agent_status"]},
            {"name": portfolio["name"], "role": "Portfolio Manager", "rank": portfolio["rank"], "status": portfolio["agent_status"]},
        ]
    )
    st.dataframe(staff_rows, use_container_width=True)

    st.subheader("Expand FX Watchlist")
    st.caption("Fetches Saxo SIM FxSpot instruments available to your token, validates live pricing, then updates SAXO_WATCHLIST.")
    if st.button("Discover Full Saxo FX Universe"):
        if not client:
            st.error("Saxo client is unavailable.")
        else:
            try:
                discovered = client.get_fx_spot_universe()
                priced = []
                skipped = []
                for instrument in discovered:
                    try:
                        client.get_instrument_price(instrument)
                        priced.append(instrument)
                    except Exception as exc:
                        skipped.append(f"{instrument.label}: {type(exc).__name__}")
                if priced:
                    _update_watchlist_value(priced)
                    st.success(f"Updated SAXO_WATCHLIST with {len(priced)} priceable FxSpot symbols. Restart runner/dashboard to use it.")
                    if skipped:
                        st.caption(f"Skipped {len(skipped)} symbols that could not be priced.")
                else:
                    st.error("No priceable FxSpot instruments found.")
            except Exception as exc:
                st.error(f"FX universe discovery failed: {_saxo_error_message(exc)}")

with history_tab:
    st.subheader("Saxo Historical Closed Positions")
    st.caption("Read-only sync from Saxo historical positions. No orders are placed.")
    c1, c2 = st.columns(2)
    from_date = c1.date_input("From", value=date(2024, 1, 1))
    to_date = c2.date_input("To", value=date.today())

    if st.button("Sync From Saxo"):
        try:
            result = sync_historical_positions(
                settings,
                store,
                from_date.isoformat(),
                to_date.isoformat(),
            )
            st.success(
                f"Fetched {result['fetched']} historical positions; "
                f"stored/updated {result['stored_or_updated']} rows. "
                f"Source: {result['source']}."
            )
        except Exception as exc:
            st.error(f"Historical sync failed. {_saxo_error_message(exc)}")

    analysis = store.historical_analysis()
    if analysis.get("overall", {}).get("trades", 0):
        c1, c2, c3, c4 = st.columns(4)
        overall = analysis["overall"]
        c1.metric("Closed Trades", overall["trades"])
        c2.metric("Realized P/L", f"{overall['pnl']:,.2f}")
        c3.metric("Win Rate", f"{overall['win_rate']:.1%}")
        c4.metric("Profit Factor", overall["profit_factor"] or "N/A")

        st.subheader("By Channel")
        st.dataframe(
            [{"channel": channel, **stats} for channel, stats in analysis["by_channel"].items()],
            use_container_width=True,
        )

        st.subheader("Most Traded")
        st.dataframe(analysis["most_traded"], use_container_width=True)

        st.subheader("Worst Symbols")
        st.dataframe(analysis["worst_symbols"], use_container_width=True)

        st.subheader("Recent Synced Closed Positions")
        st.dataframe(store.historical_positions(200), use_container_width=True)
    else:
        st.info("No Saxo historical positions have been synced yet.")
