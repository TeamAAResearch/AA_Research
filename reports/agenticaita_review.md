# AgenticAITA Literature Review

**Source:** [arXiv:2605.12532](https://arxiv.org/abs/2605.12532)

## Architecture
- **Infrastructure:** Deployed as containerized microservices over an isolated private network. Uses SQLite (WAL mode) for data persistence.
- **Cognitive Layer:** Built on a multi-agent orchestration framework (Agno) using the `qwen3.5:9b` LLM via Ollama.
- **Core Modules:** 
  - **AZTE (Adaptive Z-Score Trigger Engine):** Statistical anomaly detector triggering LLMs only during high-information market events.
  - **SDP (Structured Deliberative Pipeline):** A 3-agent chain comprising an Analyst, Risk Manager, and Executor.
  - **IGP (Inference Gating Protocol):** A mutex-based cognitive resource scheduler handling concurrent triggers.
  - **CBD (Cross-asset Behavioral Divergence):** A portfolio-aware composite score prioritizing decorrelated trading opportunities.

## Decision flow
1. **Trigger:** The AZTE continuously polls assets and wakes the pipeline if a statistical volatility anomaly occurs (Z-score ≥ 2.0 or absolute return ≥ 0.3%). 
2. **Scheduling:** The IGP locks the pipeline to prevent concurrent executions and race conditions.
3. **Proposal:** The Analyst agent receives context (OHLCV, L2 orderbook, CBD score, episodic memory) and proposes a trade.
4. **Validation:** The Risk Manager processes the proposal. It first checks deterministic hard gates. If passed, it uses the LLM to contextually validate and size the position.
5. **Execution:** The Executor agent receives the final JSON contract and routes the order through a privacy-preserving dual-channel network (Tor/VPN).

## Memory design
- **Episodic Narrative Memory:** The Analyst's qualitative reasoning traces are stored verbatim in a persistent SQLite database.
- **Cross-Episode Retrieval:** During future invocations for the same asset, prior reasoning is retrieved to form an experiential context briefing.
- **State Tracking:** Rolling baseline volatility estimators are continuously written to a `vol_history` database, enabling instant "hot restarts" after container failures.

## Learning mechanism
- **Training-Free Inference:** Operates purely via inference-time ("zero-shot") reasoning, requiring no offline training, fine-tuning, or RL policy optimization.
- **Context Accumulation:** Relies on retrieving episodic memory to accumulate experiential context over time, rather than updating model weights. (Future work proposes using RL to adapt CBD weights based on PnL).

## Risk controls
- **Deterministic Hard Gates (Layer A):** Executed by the Risk Manager *before* any LLM inference, strictly vetoing unsafe trades. These include:
  - Asset Risk Cap (≤ 2.0% equity)
  - Asset Notional Cap (≤ 15.0% equity)
  - Portfolio Cluster Limit (≤ 3 correlated assets)
  - Global Drawdown Guard (halts at ≥ 10.0% DD)
- **Contextual Gate (Layer B):** Secondary LLM-based verification for positioning and sizing.
- **Execution Safeguard:** Real-time network check (`tor_active AND exchange_reachable`) required before live order placement.

## Failure modes
- **LLM Output Instability:** Mitigated by strict typed JSON contracts and the deterministic hard-gate safety layer.
- **Network/Persistence Latency:** Mitigated by SQLite WAL mode and a conservative fallback policy that defaults to non-action.
- **Directional Bias:** The LLM exhibited a 90.4% long signal rate due to intrinsic language model overconfidence and optimistic framing. (The paper proposes a future "Skeptic Agent" to structurally penalize this bias).

## Evidence of success
- Conducted a 5-day autonomous dry-run resulting in 157 zero-intervention invocations across 76 assets.
- Achieved an 11.5% "Agentic Friction" rate (8.3% Analyst self-abstentions, 3.2% Risk Manager gate rejections), proving that agents actively negotiate and reject sub-optimal trades rather than acting as uncritical pass-throughs.
- Cleanly handled concurrent triggers via the IGP without race conditions.
- Generated +14.94 percentage points of benchmark-relative alpha during a 15% market correction, structurally protecting capital.

## Relevance to AA
- **Architectural Validation:** High relevance. Direct 1:1 mapping with AA's separation of duties (Analyst = Trader, Risk Manager = Risk, etc.).
- **Safety Paradigm:** Validates that deterministic mathematical bounds must sit *above* LLM reasoning (matching AA's absolute risk ceilings like the $250 cap).
- **Agentic Friction:** Confirms that AA's high trade rejection rate is an intended feature of safe multi-agent orchestration, not a flaw.
- **Strategic Opportunity:** The AZTE trigger suggests AA could research dynamic Z-score thresholds instead of static Admission Scores (e.g., 70 for FX) to wake agents. The CBD logic maps directly to Clara's (Portfolio) correlation clusters to prioritize idiosyncratic signals.
