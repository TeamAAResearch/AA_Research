# Autonomous Trading Research Master Review
**Date:** 2026-06-24
**Author:** Independent Challenger
**Objective:** Synthesis of 8 leading academic, industry, and retail methodologies regarding autonomous and agentic trading systems.

## 1. Common Architectures
Across all reviewed systems, the dominant architectural paradigm is **Hierarchical Separation of Duties**.
*   **Multi-Agent Pipelines:** Systems like *TradingAgents* and *AgenticAITA* decompose the monolithic "trader" into highly specialized sub-agents (Analysts, Bear/Skeptics, Risk Managers, Executors).
*   **Hybrid / Two-Tiered Models:** Instead of a single "black box," experts like Ernie Chan and René Balke utilize a baseline causal signal generator paired with a secondary Machine Learning (ML) or deterministic overlay whose sole job is risk filtration.
*   **Uncorrelated Swarms:** Algorithmic purists (Kevin Davey) advocate for deploying swarms of simple, uncorrelated logic models (90+ simultaneous strategies) rather than chasing complex "holy grail" logic.

## 2. Common Learning Patterns
The consensus strongly favors **offline, reflective adaptation** over continuous online weight updating during live markets.
*   **Reflective Epistemology:** *FinMem*, *FinAgent*, and *TradingAgents* utilize post-trade reflection loops. The models do not update weights; rather, they generate qualitative "lessons learned" text that is retrieved as experiential context during future inferences.
*   **Walk-Forward Optimization:** Validating predictive edge requires repeatedly testing on rolling out-of-sample windows to prevent curve-fitting (Davey).
*   **Meta-Labeling:** Training models on the *probability of a trade's success/failure* rather than predicting the absolute price of the asset (Chan).

## 3. Common Memory Patterns
A critical innovation in agentic trading is moving beyond stateless prompts to **Layered Cognitive Memory**.
*   **Working vs. Stratified Memory:** Systems divide short-term transient noise (tick data, daily news) from enduring institutional knowledge (long-term trends, fundamental regimes) via layered vector databases (*FinMem*).
*   **Decay and Promotion:** Implementations utilize "freshness" and "importance" scoring to naturally decay obsolete context while permanently "promoting" high-impact lessons to deeper memory layers.
*   **Episodic Traces:** Storing the qualitative reasoning traces (the "why") of past trade proposals allows agents to perform "hot restarts" and cross-reference past reasoning on identical assets (*AgenticAITA*).

## 4. Common Risk Controls
Risk management is universally recognized as the primary differentiator between theoretical success and live survival.
*   **Deterministic Hard Gates:** LLMs are intrinsically optimistic and prone to hallucination. Consequently, robust systems (*AgenticAITA*, René Balke) enforce rigid, database-level mathematical boundaries (e.g., maximum drawdown locks, notional caps) that the LLM cannot override.
*   **Adversarial Validation:** Structurally forcing a "Bear" or "Skeptic" agent to debate the trade proposal to pressure-test assumptions (*TradingAgents*).
*   **ML as a Veto Engine:** Utilizing ML purely as an overlay to predict the conditional probability of profit for a base signal, vetoing or reducing size if the probability drops below a threshold (*Ernie Chan*).

## 5. Common Failure Modes
*   **Curve-Fitting / Over-Optimization:** Constructing models that perfectly map historical data but instantly collapse in live, out-of-sample dynamic markets.
*   **Groupthink & Directional Bias:** Unchecked multi-agent systems often enter an "echo chamber" of mutual validation, leading to extreme long-bias (optimism) and unforced errors.
*   **Friction Ignorance:** Achieving high theoretical Sharpe ratios in backtests that evaporate in production because slippage, market impact, and commission costs (10-20 bps) were not structurally modeled.
*   **Contextual Obsolescence:** Memory retrieval systems surfacing outdated historical patterns that no longer apply due to undetected macroeconomic regime shifts.

## 6. Evidence-Supported Best Practices
*   Implement strict structural separation between Alpha Generation and Risk Execution.
*   Enforce Walk-Forward Optimization and Monte Carlo simulations before live capital deployment.
*   Use deterministic hard gates as the absolute ceiling for risk; do not trust prompt-level LLM boundaries.
*   Adopt "Meta-Labeling" to predict trade success probabilities rather than chasing asset price prediction.

## 7. Evidence-Supported Anti-Patterns
*   Deploying complex, unconstrained "black box" models without causal, fundamental economic rationale.
*   Relying on continuous, unchecked online learning (RL) in live volatile markets.
*   "Holy Grail" complexity: Seeking one massive monolithic model instead of many simple, uncorrelated strategies.
*   Treating execution environments as frictionless.

## 8. Applicable Lessons for AA
*   **Validate the Multi-Agent Structure:** AA's current separation of duties is fundamentally correct and aligns with state-of-the-art academic practice.
*   **Formalize the "Skeptic":** AA should explicitly codify the "Independent Challenger" role into the pipeline as an adversarial "Bear" agent to mechanically suppress the LLM's natural optimistic directional bias.
*   **Expand the Blocked Ledger to Episodic Memory:** AA's current tracking of "Blocked Opportunities" should be evolved into a formal episodic memory database. AA can use this to retrieve qualitative traces of *why* trades failed or were blocked, utilizing it for pre-trade reflection.
*   **Meta-Labeling for Admission Scoring:** AA's "Score" should be re-contextualized not as an absolute measure of truth, but as a "Meta-Label" predicting the probability of the trade's survival through the risk gates.
*   **Agentic Friction:** The high rejection rate in AA should be celebrated, not "fixed." Agentic friction is a proven mechanism for capital protection (*AgenticAITA*).

## 9. Non-Applicable Lessons for AA
*   **"Vibe Coding" via Retail Chatbots:** The manual, prompt-heavy approach used by retail AI builders is entirely insufficient for AA's institutional, fully autonomous deterministic governance structure.
*   **Prompt-Level Risk Constraints:** Frameworks that rely on telling the LLM to "be conservative" (*FinAgent*) are fundamentally unsafe. AA must maintain its non-negotiable deterministic hard gates.
*   **Visual Multimodal Ingestion:** Parsing K-line charts visually (*FinAgent*) introduces unnecessary latency and hallucination risk, given that AA operates efficiently on structured tick and feature data.
