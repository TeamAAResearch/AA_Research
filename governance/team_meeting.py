from __future__ import annotations

from typing import Any

from .market_data_analyst import market_data_snapshot
from .mentor import mentor_brief
from .promotion import aa_promotion_snapshot
from .risk_officer import risk_officer_snapshot
from .storage import TradeStore
from .systems_reliability import systems_reliability_snapshot
from .team_architect import team_architect_brief
from .trade_reviewer import trade_reviewer_snapshot


def first_team_meeting(
    store: TradeStore,
    challenger_config: Any,
    watchlist: list[Any],
    quotes: list[Any],
    fetch_errors: list[str],
) -> dict[str, Any]:
    promotion = aa_promotion_snapshot(store, challenger_config.starting_capital)
    mentor = mentor_brief(store, challenger_config)
    architect = team_architect_brief(store, challenger_config.starting_capital)
    risk = risk_officer_snapshot(store, challenger_config)
    systems = systems_reliability_snapshot()
    data = market_data_snapshot(store, watchlist, quotes, fetch_errors)
    reviewer = trade_reviewer_snapshot(store)
    return {
        "meeting": "AA Team Meeting #2",
        "chair": "Helena Ward",
        "chair_role": "Governance / Chair",
        "vision": (
            "Train Ari Axelrod into a profitable autonomous trader by earning trust through "
            "profitability, controlled drawdown, explainability, and repeatability. "
            "The organization now operates under a formal Evidence Review function: "
            "Data → Observation → GM Review → Hypothesis → Contradiction Test → Finding."
        ),
        "attendees": [
            {"name": "Ari Axelrod", "role": "AI Challenger", "rank": promotion["rank"], "status": "Training"},
            {"name": mentor["name"], "role": "Mentor", "rank": mentor["rank"], "status": mentor["mentor_status"]},
            {"name": architect["name"], "role": "Team Architect", "rank": architect["rank"], "status": architect["status"]},
            {"name": "Helena Ward", "role": "Governance / Chair", "rank": "Governance / Chair", "status": "Chair"},
            {"name": risk["name"], "role": "Risk Officer", "rank": risk["rank"], "status": risk["agent_status"]},
            {"name": systems["name"], "role": systems["role"], "rank": systems["rank"], "status": systems["agent_status"]},
            {"name": data["name"], "role": "Market Data Analyst", "rank": data["rank"], "status": data["agent_status"]},
            {"name": reviewer["name"], "role": "Trade Reviewer", "rank": reviewer["rank"], "status": reviewer["agent_status"]},
            {"name": "AG", "role": "Chief Research Analyst / Observation Pipeline Owner", "rank": "Chief Research Analyst", "status": "Active"},
            {"name": "Codex", "role": "Chief Knowledge Officer / Organizational Memory Owner", "rank": "Chief Knowledge Officer", "status": "Active"},
        ],
        "feedback": [
            {
                "speaker": "Ari Axelrod",
                "feedback": (
                    f"I am still {promotion['rank']} with {promotion['closed_trades']} closed trade(s). "
                    "I need more clean samples before I can claim edge."
                ),
            },
            {"speaker": mentor["name"], "feedback": mentor["mentor_advice"]},
            {"speaker": architect["name"], "feedback": architect["current_assessment"]},
            {
                "speaker": "Helena Ward",
                "feedback": "Staff are accountable and replaceable. AA is accountable but trained, not replaced.",
            },
            {
                "speaker": risk["name"],
                "feedback": (
                    f"My current status is {risk['status']}. "
                    + (" ".join(risk["warnings"]) if risk["warnings"] else "No risk veto is active.")
                ),
            },
            {
                "speaker": systems["name"],
                "feedback": (
                    f"Systems status is {systems['status']}. Runner state: {systems['runner_state']}. "
                    + (" ".join(systems["warnings"]) if systems["warnings"] else "No systems blocker is active.")
                ),
            },
            {
                "speaker": data["name"],
                "feedback": f"Market data status is {data['status']} with {data['tradable_symbols']} tradable symbol(s).",
            },
            {
                "speaker": reviewer["name"],
                "feedback": (
                    f"I have reviewed {reviewer['closed_reviews']} closed trade(s). "
                    f"Current loss clusters: {len(reviewer['loss_clusters'])}."
                ),
            },
        ],
        "agreed_actions": [
            "Let current AA positions resolve; do not force new trades while risk is blocked.",
            "Theo owns Saxo/token/data/runner troubleshooting before AA strategy is changed.",
            "Use the current sample to isolate leaking symbols, sides, regimes, and execution patterns.",
            "Clara keeps portfolio concentration enforced while Mason controls daily loss and stop-risk exposure.",
            "Keep all staff accountable through Helena Ward's governance table.",
            "Do not increase AA size until profit factor is back above the next-rank threshold.",
            "Evidence Review is now a formal organizational function: review existing ledgers before creating new pipelines.",
            "Organizational workflow: Data → Observation → GM Review → Hypothesis → Contradiction Test → Finding.",
            "AG owns the Observation Pipeline (read-only). Codex owns Organizational Memory and Governance Records.",
            "Finding Adoption Framework is now in effect: Finding ≠ Automatic Change.",
        ],
        "open_questions": [
            "What concentration limit should Portfolio Manager enforce by currency and asset class?",
            "When should AA reduce open positions early instead of waiting for stop or target?",
        ],
    }
