# Literature Review: AgenticAITA
**Date:** 24 June 2026  
**Source:** [arXiv:2605.12532](https://arxiv.org/abs/2605.12532)  
**Title:** AgenticAITA: A Proof-Of-Concept About Deliberative Multi-Agent Reasoning for Autonomous Trading Systems

---

## Executive Summary
This paper introduces *AgenticAITA*, an autonomous trading framework that entirely replaces the traditional "signal-then-execute" paradigm with a deliberative loop driven by specialized Large Language Model agents (Analyst, Risk Manager, Executor). It demonstrates that complex financial decision-making can be securely orchestrated without offline training, provided the agents are bounded by a deterministic safety layer and strict JSON contracts.

**Relevance to AA Project:** High. This paper provides external academic validation for AA's exact architectural design (the separation of Trader, Risk, Portfolio, and Research functions). 

---

## Key Architectural Contributions & AA Mapping

### 1. Sequential Deliberative Pipeline
* **Paper Concept:** A multi-agent reasoning chain where an Analyst proposes, a Risk Manager restricts, and an Executor acts. Inter-agent negotiation is required before an action reaches the market.
* **AA Mapping:** Direct 1:1 map. Ari (Trader) proposes, Mason (Risk) restricts, Clara (Portfolio) governs, and the core engine executes. The paper's finding of an "11.5% agentic friction rate" (where agents disagree and block trades) strongly validates AA's high rejection rate as an intended feature of safe multi-agent systems, not a bug.

### 2. Deterministic Hard-Gate Safety Layer
* **Paper Concept:** Agents reason, but deterministic code executes the hard limits. Agents are never allowed to override core mathematical risk boundaries.
* **AA Mapping:** Direct 1:1 map. This matches AA's Stage 3 (Portfolio) and Stage 4 (Risk) gates. The paper validates that placing hard ceilings (like our $250.00 risk cap) *above* the agents' reasoning layer is the correct pattern for survivability.

### 3. Adaptive Z-Score Trigger Engine
* **Paper Concept:** A "cognitive resource allocator" that only wakes up the LLM agents when statistically anomalous market conditions occur, saving compute and preventing the agents from hallucinating trades during market noise.
* **AA Mapping:** AA's "Admission Score" threshold (70 for FX, 85 for Metals) acts exactly like this engine. However, the paper suggests dynamically triggering based on statistical anomalies (Z-scores) rather than static thresholds, which could be an area for future AA research regarding the rigid 70-point FX threshold.

### 4. Correlation-Break Diversification
* **Paper Concept:** A composite score that prioritizes idiosyncratic signals (trades that don't correlate with the rest of the portfolio) within the individual agent's reasoning process.
* **AA Mapping:** Matches Clara's (Portfolio) cluster limit logic. 

---

## Strategic Takeaway for AA
The paper reinforces that the current AA Project mandate—treating opportunity starvation and risk bottlenecks as subjects for structural analysis rather than bugs to be patched—is the correct scientific approach. The architecture we are currently observing (a noisy generator heavily filtered by deterministic risk gates) is exactly what the state-of-the-art academic literature prescribes for autonomous financial agents.

*Note: Document synced to the official AA_Research repository. No optimization or code changes recommended based on this literature.*
