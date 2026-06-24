from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .promotion import aa_promotion_snapshot
from .storage import TradeStore


@dataclass(frozen=True)
class SpecialistBlueprint:
    priority: int
    name: str
    role: str
    rank: str
    purpose: str
    why_now: str
    first_capability: str
    veto_power: str
    status: str


@dataclass(frozen=True)
class OperatingLoopStep:
    step: int
    owner: str
    department: str
    function: str
    input: str
    output: str
    aa_impact: str


@dataclass(frozen=True)
class DepartmentBlueprint:
    owner: str
    department: str
    mission: str
    sub_functions: str
    inputs: str
    outputs: str
    escalation_trigger: str
    first_build: str
    success_metric: str


@dataclass(frozen=True)
class AATeamRequestRule:
    trigger: str
    aa_request: str
    sofia_guidance: str
    decision_gate: str
    department_owner: str
    status: str


def team_architect_brief(store: TradeStore, starting_capital: float) -> dict[str, Any]:
    promotion = aa_promotion_snapshot(store, starting_capital)
    open_positions = store.challenger_positions("Open", 1000)
    closed_trades = store.challenger_trades(100000)
    latest_loss = next((trade for trade in store.challenger_trades(1000) if float(trade.get("pnl") or 0) < 0), None)
    blueprints = _blueprints(promotion, len(open_positions), len(closed_trades), latest_loss is not None)
    return {
        "agent": "AA Team Architect",
        "name": "Sofia Chen",
        "rank": "Chief Team Architect",
        "status": "GOOD STANDING",
        "mission": "Design the specialist team that helps Ari Axelrod become an autonomous, profitable trader.",
        "current_assessment": _assessment(promotion, len(open_positions), len(closed_trades)),
        "next_build": _next_build(blueprints).__dict__,
        "team_roadmap": [blueprint.__dict__ for blueprint in blueprints],
        "aa_performance_loop": [step.__dict__ for step in _aa_performance_loop()],
        "department_blueprints": [department.__dict__ for department in _department_blueprints()],
        "aa_team_build_guidance": [rule.__dict__ for rule in _aa_team_build_guidance()],
        "aa_current_team_requests": _aa_current_team_requests(promotion, len(open_positions), len(closed_trades), latest_loss is not None),
        "operating_principle": (
            "Every specialist must improve profitability, controlled drawdown, explainability, or repeatability. "
            "If it does not help AA earn promotion, it does not get built yet."
        ),
    }


def _assessment(promotion: dict[str, Any], open_count: int, closed_count: int) -> str:
    if closed_count < 30:
        return (
            f"AA is still an Intern with {closed_count} closed trade(s) and {open_count} open paper position(s). "
            "The team should focus on survival, clean data, and review quality before adding strategy complexity."
        )
    if promotion["profit_factor"] is None or promotion["profit_factor"] < 1:
        return "AA has enough activity to inspect but has not proven positive expectancy. Build diagnostics before new strategies."
    return "AA is developing evidence. Build portfolio and research specialists to test whether the edge is repeatable."


def _blueprints(
    promotion: dict[str, Any],
    open_count: int,
    closed_count: int,
    has_loss: bool,
) -> list[SpecialistBlueprint]:
    return [
        SpecialistBlueprint(
            priority=1,
            name="Mason Vale",
            role="Risk Officer",
            rank="Junior Risk Officer",
            purpose="Keep AA alive while it learns.",
            why_now=(
                f"AA has {open_count} open position(s), {closed_count} closed trade(s), and "
                f"max drawdown of {promotion['max_drawdown_pct']:.2f}%. "
                "Risk control must come before smarter entries."
            ),
            first_capability="Calculate open portfolio heat, correlated exposure, max loss if all stops hit, and daily loss status.",
            veto_power="Block new paper trades when daily loss, open risk, margin, or correlation limits are breached.",
            status="Built v1",
        ),
        SpecialistBlueprint(
            priority=2,
            name="Theo Park",
            role="Systems Reliability Officer",
            rank="Junior Systems Reliability Officer",
            purpose="Keep AA connected to Saxo and running exactly once.",
            why_now="AA has already been blocked by token expiry, data fetch failures, stale runners, and duplicate starts.",
            first_capability="Detect Saxo/data outages, stale runner heartbeats, duplicate runner locks, stale PID files, and launch errors.",
            veto_power="Pause paper trading when infrastructure reliability is compromised.",
            status="Built v1",
        ),
        SpecialistBlueprint(
            priority=3,
            name="Iris Quinn",
            role="Market Data Analyst",
            rank="Junior Market Data Analyst",
            purpose="Make sure AA is not trading bad or stale prices.",
            why_now="AA depends on live Saxo ticks. Bad data would make every downstream decision suspect.",
            first_capability="Flag stale ticks, wide spreads, missing symbols, and low-quality quote windows.",
            veto_power="Block signals when market data quality is poor.",
            status="Built v1",
        ),
        SpecialistBlueprint(
            priority=4,
            name="Nolan Price",
            role="Trade Reviewer",
            rank="Junior Trade Reviewer",
            purpose="Turn each closed trade into a clear lesson.",
            why_now=(
                "AA already reviews trades, but the review system should become more evidence-based as samples grow."
                if has_loss
                else "AA needs structured review before the first meaningful sample is complete."
            ),
            first_capability="Cluster losses by symbol, side, entry type, session, and path behavior.",
            veto_power="Flag setups for quarantine when repeated losses share the same cause.",
            status="Built v1",
        ),
        SpecialistBlueprint(
            priority=5,
            name="Clara Stone",
            role="Portfolio Manager",
            rank="Junior Portfolio Manager",
            purpose="Control position sizing and concentration across AA's book.",
            why_now="AA should not become profitable by accident while quietly building hidden concentration risk.",
            first_capability="Track symbol, currency, metal, and USD exposure across open paper positions.",
            veto_power="Reduce or block trades that over-concentrate the book.",
            status="Built v1",
        ),
        SpecialistBlueprint(
            priority=6,
            name="Rowan Pierce",
            role="Strategy Researcher",
            rank="Junior Strategy Researcher",
            purpose="Find which signals have repeatable edge.",
            why_now="Strategy changes should wait until AA has enough samples or a clear safety failure.",
            first_capability="Measure expectancy by symbol, side, regime, and signal pattern.",
            veto_power="Demote or quarantine strategies with persistent negative expectancy.",
            status="Built v1",
        ),
        SpecialistBlueprint(
            priority=7,
            name="Vera Lin",
            role="Execution Analyst",
            rank="Junior Execution Analyst",
            purpose="Study slippage, fill quality, and whether signal timing is improving or worsening AA's results.",
            why_now="Execution research should come after AA has better strategy and risk journals.",
            first_capability="Compare signal price, fill price, exit price, spread, and time in trade.",
            veto_power="Pause symbols when execution quality is persistently poor.",
            status="Built v1",
        ),
        SpecialistBlueprint(
            priority=8,
            name="Mira Tan",
            role="Macro Regime Analyst",
            rank="Junior Macro Regime Analyst",
            purpose="Help AA understand when FX momentum conditions are supportive or dangerous.",
            why_now="Regime awareness should come after execution and strategy diagnostics are stable.",
            first_capability="Classify risk-on, risk-off, USD trend, metals trend, and volatility state.",
            veto_power="Warn AA when the current regime does not match the strategy's historical winners.",
            status="Built v1",
        ),
    ]


def _aa_performance_loop() -> list[OperatingLoopStep]:
    return [
        OperatingLoopStep(1, "Theo Park", "Systems Reliability", "Verify AA can operate.", "Runner heartbeat, Saxo errors, locks, PID files", "Stable, watch, or blocker status", "AA does not trade when the plumbing is unreliable."),
        OperatingLoopStep(2, "Iris Quinn", "Market Data", "Validate tradable symbols.", "Saxo quotes, watchlist, fetch errors", "Data-quality status", "AA avoids stale, missing, or wide-spread prices."),
        OperatingLoopStep(3, "Mira Tan", "Macro Regime", "Label market environment.", "FX/metals movement and volatility", "Risk tone and regime tags", "AA learns whether conditions helped or hurt each setup."),
        OperatingLoopStep(4, "Rowan Pierce", "Strategy Research", "Judge repeatable edge.", "Closed trades and setup clusters", "Keep, test, or quarantine recommendation", "AA changes rules only from evidence."),
        OperatingLoopStep(5, "Mason Vale", "Risk", "Decide if AA may add risk.", "Open positions, stops, daily P/L", "Clear or block-new-trades status", "AA survives long enough to learn."),
        OperatingLoopStep(6, "Clara Stone", "Portfolio", "Shape the book.", "Open positions and exposure", "Concentration warnings and reduction candidates", "AA avoids making the same trade several times unknowingly."),
        OperatingLoopStep(7, "Ari Axelrod", "AA Decision Desk", "Make the final paper decision.", "Signal plus staff advice", "Enter, hold, exit, block, or wait", "AA remains accountable; staff advise, AA decides."),
        OperatingLoopStep(8, "Vera Lin", "Execution", "Assess implementation quality.", "Entry, exit, spread, timing, giveback", "Execution grade and diagnosis", "AA separates bad idea from bad execution."),
        OperatingLoopStep(9, "Nolan Price", "Trade Review", "Turn results into lessons.", "Closed trade, path, reasons", "Conclusion, takeaway, next action", "AA builds memory from every trade."),
        OperatingLoopStep(10, "Evelyn Cross", "Mentorship", "Set training gates.", "Promotion score and team warnings", "Do-next, do-not-do, authority limit", "AA earns autonomy gradually."),
        OperatingLoopStep(11, "Helena Ward", "Governance", "Hold staff accountable.", "Department outputs and missed warnings", "Good standing, watch, PIP, or replace", "AA's support team improves instead of becoming decorative."),
        OperatingLoopStep(12, "AG", "Observation Pipeline", "Recover and structure evidence from AA decision records.", "blocked_signals, aa_journal, cycle_vetoes, challenger_ticks", "Structured Observations submitted to GM Review", "Data \u2192 Observation \u2192 GM Review \u2192 Hypothesis \u2192 Contradiction Test \u2192 Finding."),
    ]


def _department_blueprints() -> list[DepartmentBlueprint]:
    return [
        DepartmentBlueprint("Sofia Chen", "Team Architecture Office", "Keep AA's organization lean and tied to measurable performance.", "Roadmap; bottleneck diagnosis; department design; anti-bloat review", "AA rank, bottlenecks, warnings, user goals", "Team roadmap, operating loop, next-build gate", "A repeated bottleneck appears that no current department owns.", "Monthly operating review with evidence-based next-build decision.", "No new role is added without a measured AA performance gap."),
        DepartmentBlueprint("Mason Vale", "Risk Department", "Keep AA alive and prevent avoidable drawdown.", "Portfolio heat; daily loss; max stop loss; correlation risk; veto audit", "Open positions, stops, daily P/L, account settings, Evidence Recovery ledgers (cycle_vetoes.csv — Downside Limit and Concentration freeze events)", "Risk status, blockers, risk violations, risk lessons", "Drawdown rises, daily loss is hit, or concentration keeps recurring.", "Risk ledger that records every veto and whether AA respected it.", "Zero unresolved risk violations while AA is Intern or Junior Analyst."),
        DepartmentBlueprint("Theo Park", "Systems Reliability Department", "Keep AA connected, observable, and running exactly once.", "Saxo token checks; quote fetch health; runner heartbeat; lock audit; PID cleanup; error-log triage", "Runner logs, Saxo fetch errors, token symptoms, PID files, LaunchAgent logs", "System status, blockers, troubleshooting actions, restart recommendation", "AA has no activity, duplicate runners, stale heartbeats, or Saxo data failures.", "Ops health panel with heartbeat, data, lock, PID, and launch diagnostics.", "No training session runs with unresolved system blocker."),
        DepartmentBlueprint("Iris Quinn", "Market Data Department", "Ensure AA trades from clean and complete market data.", "Quote availability; stale tick checks; spread checks; watchlist coverage", "Saxo quotes, watchlist, fetch errors, tick history", "Tradable universe, blocked symbols, data-quality warnings", "A signal is generated from stale, missing, or wide-spread data.", "Data-quality history table by symbol.", "No AA trade is opened from a blocked or stale symbol."),
        DepartmentBlueprint("Nolan Price", "Trade Review Department", "Make every closed trade teach AA something concrete.", "Win/loss review; path analysis; loss clustering; lesson extraction", "Closed trades, ticks during hold, entry and exit reasons", "Verdict, conclusion, takeaway, next action, loss clusters", "Reviews become vague or repeated losses lack a cause.", "Trade lesson library searchable by symbol, side, reason, and regime.", "At least 95% of closed trades have conclusion and next action."),
        DepartmentBlueprint("Clara Stone", "Portfolio Department", "Shape AA's book so risk is intentional rather than accidental.", "Currency exposure; metals exposure; crowding; reduction candidates", "Open positions, live P/L, symbol exposures, concentration limits", "Do-not-add status, reduction list, exposure table", "More than 3 same-currency directional positions or metals cap breach.", "Position-sizing and allocation policy by rank.", "AA never exceeds concentration limits without a logged override."),
        DepartmentBlueprint("Ari Axelrod", "AA Decision Desk", "Make final paper trading decisions and account for all specialist inputs.", "Trade admission; signal evaluation; hold/exit decisions; opportunity log", "Signal, staff advice, risk status, portfolio status, Evidence Recovery ledgers (opportunity_funnel.csv)", "Enter, hold, exit, block, or wait decision with reasoning", "Repeated unexplained decisions or repeated ignoring of staff veto.", "Decision log with reasoning for every entry, hold, and exit.", "AA can explain every decision with reference to evidence."),
        DepartmentBlueprint("Rowan Pierce", "Strategy Research Department", "Find repeatable edge and protect AA from overfitting.", "Expectancy; profit factor; setup clustering; quarantine tests; rule experiments", "Closed trades, regime labels, execution grades, reviews, Evidence Recovery ledgers (opportunity_funnel_simulated.csv — blocked signal counterfactuals)", "Keep, test, quarantine, or collect-more-samples recommendation", "A setup reaches 3+ losses or 30+ samples with negative expectancy.", "Experiment backlog with hypothesis, sample size, pass/fail criteria.", "No strategy rule changes before evidence threshold is met."),
        DepartmentBlueprint("Vera Lin", "Execution Department", "Separate trade idea quality from implementation quality.", "Spread; timing; entry/exit delay; giveback; slippage proxy", "Entries, exits, ticks, spread, time held, adverse/favorable movement", "Execution grade, weak-execution warning, timing diagnosis", "Weak execution is 30%+ of reviewed trades.", "Execution scorecard by symbol and session.", "Execution problems are identified before AA increases risk."),
        DepartmentBlueprint("Mira Tan", "Macro Regime Department", "Tell AA what kind of market environment it is trading.", "USD regime; metals regime; risk tone; volatility; regime tagging", "FX/metals ticks, live quotes, volatility ranges", "Regime label, warnings, next action, trade tags", "High volatility or mixed regime persists while AA keeps adding directional risk.", "Attach regime tag to every AA entry and closed-trade review.", "Rowan can compare winners and losers by regime after 30+ trades."),
        DepartmentBlueprint("Evelyn Cross", "Mentorship Department", "Train AA without promoting it too early.", "Promotion gates; training focus; do-next/do-not-do; authority unlocks", "AA score, risk status, explanation quality, team findings", "Training focus, promotion readiness, authority limits", "AA wants more autonomy before evidence supports it.", "Authority ladder linking rank to overrides and sizing.", "AA gains authority only after meeting rank requirements."),
        DepartmentBlueprint("Helena Ward", "Governance Department", "Keep every staff member accountable to AA's performance. Owns Finding Adoption Framework: every Finding passes through Adoption Review before any operational change.", "Staff scorecards; PIP; demotion; replacement; meeting discipline; Adoption Review chairmanship", "Department outputs, missed warnings, stale advice, user priorities, Finding candidates", "Good standing/watch/PIP status and accountability table; Adoption Review memos", "A specialist gives unsafe, vague, or repeatedly wrong guidance; or a validated Finding has no adoption process.", "Department scorecard table with weekly review cadence.", "Every specialist has measurable output and clear PIP triggers. Every Finding passes Adoption Review before implementation."),
    ]


def _aa_team_build_guidance() -> list[AATeamRequestRule]:
    return [
        AATeamRequestRule(
            trigger="AA has no activity, stale logs, duplicate starts, or Saxo token/data failures.",
            aa_request="Ask Theo to diagnose runner and Saxo connectivity before changing trading logic.",
            sofia_guidance="Route to Systems Reliability first. Do not tune strategy until uptime and data health are clean.",
            decision_gate="Any stale runner heartbeat, repeated lock block, stale PID file, or 3+ recent data errors.",
            department_owner="Systems Reliability",
            status="Allowed now as tooling request",
        ),
        AATeamRequestRule(
            trigger="AA cannot explain a repeated loss pattern.",
            aa_request="Ask Sofia for a deeper research tool or sub-function, not a new trader.",
            sofia_guidance="Route first to Rowan and Nolan. Build a new specialist only if loss causes remain unowned after review.",
            decision_gate="3+ similar losses or 30+ closed trades with unclear negative expectancy.",
            department_owner="Strategy Research / Trade Review",
            status="Allowed after evidence",
        ),
        AATeamRequestRule(
            trigger="AA is blocked by risk or concentration for multiple cycles.",
            aa_request="Ask for portfolio/risk tooling to reduce or rotate exposure.",
            sofia_guidance="Route to Mason and Clara. Improve policy before adding staff.",
            decision_gate="Repeated block with no clear reduction candidate or no logged AA decision.",
            department_owner="Risk / Portfolio",
            status="Allowed now as tooling request",
        ),
        AATeamRequestRule(
            trigger="AA sees signals but no trades are taken.",
            aa_request="Ask whether signal quality, data quality, or regime mismatch is the cause.",
            sofia_guidance="Route to Iris, Mira, and Rowan. Do not add a new strategist until data/regime filters are tagged.",
            decision_gate="10+ no-entry scout logs with same unresolved cause.",
            department_owner="Market Data / Macro Regime / Strategy Research",
            status="Allowed after journal evidence",
        ),
        AATeamRequestRule(
            trigger="AA loses money despite good trade ideas.",
            aa_request="Ask Vera for execution diagnosis before changing strategy.",
            sofia_guidance="Separate bad idea from bad execution. Build execution tooling before changing entries.",
            decision_gate="Weak execution on 30%+ of closed reviewed trades.",
            department_owner="Execution",
            status="Allowed after execution sample",
        ),
        AATeamRequestRule(
            trigger="AA wants more autonomy, override power, or higher size.",
            aa_request="Ask Evelyn for promotion review, not more resources.",
            sofia_guidance="Authority is earned by rank. Team expansion cannot bypass promotion gates.",
            decision_gate="Rank requirements met: sample size, drawdown, risk discipline, explanation quality.",
            department_owner="Mentorship / Governance",
            status="Promotion gate only",
        ),
    ]


def _aa_current_team_requests(
    promotion: dict[str, Any],
    open_count: int,
    closed_count: int,
    has_loss: bool,
) -> list[dict[str, str]]:
    requests = []
    if open_count >= 5:
        requests.append(
            {
                "aa_observation": f"I have {open_count} open positions and may be too crowded.",
                "requested_help": "Better rotation/reduction guidance.",
                "sofia_response": "Valid. Route to Clara and Mason first; no new specialist.",
                "action": "Use Portfolio and Risk departments to reduce crowding and log AA decisions.",
            }
        )
    if closed_count < 30:
        requests.append(
            {
                "aa_observation": f"I only have {closed_count} closed trade(s).",
                "requested_help": "More confidence before strategy changes.",
                "sofia_response": "Valid concern, but not a staffing gap.",
                "action": "Keep trading paper samples until 30 closed trades before changing strategy structure.",
            }
        )
    if has_loss:
        requests.append(
            {
                "aa_observation": "I have at least one loss and need to know why.",
                "requested_help": "Loss explanation and execution diagnosis.",
                "sofia_response": "Valid. Nolan, Rowan, and Vera already own this.",
                "action": "Review loss through Trade Review, Strategy Research, and Execution departments.",
            }
        )
    if promotion["rank"].startswith("Level 0"):
        requests.append(
            {
                "aa_observation": "I am still an Intern and need resources without bypassing discipline.",
                "requested_help": "Clear path to earn more autonomy.",
                "sofia_response": "Valid. Evelyn owns the authority ladder; Helena audits it.",
                "action": "Do not add staff for autonomy. Earn Level 1 through sample size, drawdown control, and explanations.",
            }
        )
    return requests


def _next_build(blueprints: list[SpecialistBlueprint]) -> SpecialistBlueprint:
    for blueprint in blueprints:
        if blueprint.status != "Built v1":
            return blueprint
    return SpecialistBlueprint(
        priority=len(blueprints) + 1,
        name="AA Core Team",
        role="Phase 1 Team Complete",
        rank="Operational",
        purpose="Let the current team run, gather evidence, and improve AA's process before adding more specialists.",
        why_now="The Phase 1 bench now covers risk, data, review, portfolio, strategy, execution, and regime context.",
        first_capability="Monitor whether the team produces better decisions, lower drawdown, and clearer lessons.",
        veto_power="No new specialist until the current team identifies a measured gap.",
        status="Complete",
    )
