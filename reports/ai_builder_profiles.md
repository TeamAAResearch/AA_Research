# AI Builder Profiles: Retail "Vibe Coding" Approaches

Based on the Business Insider article detailing Brendan Li, Dr. Reid Daitzman, and the retail trend of "vibe coding" AI trading bots.

## Architecture
Modular architecture. Traders use generative AI platforms (e.g., Anthropic's Claude, Cursor) to define separate functions for data ingestion, signal generation, and order execution. The AI-generated logic is connected to real-time market data and brokerage accounts using "bridge" tools or APIs (such as Alpaca's MCP server or standard REST APIs).

## Decision flow
The development flow begins with "vibe coding": traders describe their trading strategy, signal criteria, and execution requirements using natural language prompts, and the AI generates the corresponding code. Once deployed, the bot acts as an objective executor. The operational decision flow often relies on "pre-evaluation logic," where the system screens multiple timeframes and technical indicators (such as volume, liquidity, and volatility) to filter out market "noise" before triggering any trade. 

## Memory design
Not explicitly detailed in source. 

## Learning mechanism
Iterative human-in-the-loop refinement. The AI does not learn autonomously on the fly; instead, the human trader tests the AI-generated code and continuously refines the natural language prompts and rule sets based on market performance.

## Risk controls
- **Emotional Mitigation:** The primary risk control is psychological. By enforcing strict, pre-programmed rule-based execution, the bot acts as a "buffer" to prevent impulsive human errors driven by fear, greed, overtrading, and "revenge trading."
- **Operational Guardrails:** Emphasis is placed on using strict anomaly detection and monitoring systems to prevent the bot from executing trades based on unexpected logic or flawed data.
- **Human Oversight:** Advanced users treat the bot as a supportive assistant rather than a fully autonomous "black box," frequently verifying the AI's logic against their own market intuition.

## Failure modes
- **Over-reliance by novices:** Treating the AI as a "get-rich-quick" device without a foundational understanding of market fundamentals.
- **Flawed data execution:** Without proper anomaly detection guardrails, the AI can execute trades based on flawed data inputs or unexpected logic anomalies.

## Evidence of success
- **Dr. Reid Daitzman (79-year-old psychologist and veteran trader):** Successfully developed an AI tool named "Merlin" to act as an emotional buffer between himself and the market, effectively mitigating psychological pitfalls that typically cause financial loss.
- **Brendan Li (27-year-old former banker):** Established a successful educational community teaching retail traders how to foster consistency by leveraging AI agents to remove emotional interference from their strategies.

## Relevance to AA
Demonstrates the viability of using LLMs to rapidly prototype algorithmic trading bots via natural language ("vibe coding"). It validates that one of AI's highest immediate value-adds in trading is objective, emotionless execution rather than pure predictive modeling. The modular integration with brokerage APIs, the necessity of "pre-evaluation logic" to filter noise, and the requirement for human-in-the-loop anomaly guardrails provide highly transferable knowledge for structuring AA's autonomous execution and multi-agent risk models.
