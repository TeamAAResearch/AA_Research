# Shadow AA — Organizational Hypothesis

**Classification:** Organizational Hypothesis
**Date Captured:** 2026-06-24
**Status:** Idea Captured. No Action Authorized.
**Repository:** TeamAAResearch/AA_Research

---

> [!CAUTION]
> The existence of this document does **not** authorize:
> - Design work
> - Coding or architecture work
> - Staffing or agent creation
> - New trader creation
> - Resource allocation
> - Any implementation activity
>
> This document exists solely to preserve the concept for future organizational consideration.

---

## 1. Concept Definition

Shadow AA is a hypothetical independent decision engine that would observe the same market opportunities as Ari Axelrod (the live AI Challenger) but:

- Does **not** control capital
- Does **not** execute trades
- Does **not** influence live AA decisions
- Does **not** interact with the Saxo execution layer

Shadow AA would evaluate each opportunity using an alternative decision framework (e.g., different admission thresholds, different risk parameters, or different signal logic) and record its hypothetical decisions alongside AA's actual decisions — creating a parallel record of "what another decision process would have done."

The concept is analogous to a "paper portfolio shadow" used in quantitative research: it generates counterfactual evidence without risking capital or disrupting the live system.

---

## 2. Potential Benefits

If the concept were eventually pursued and validated, potential organizational benefits could include:

| Benefit | Description |
|---|---|
| **Evidence Generation** | Shadow AA would produce a continuous stream of counterfactual decisions, increasing the evidence density of each AA trading cycle without increasing trade count. |
| **Comparative Analysis** | Enables direct comparison between AA's actual decision and an alternative decision at the same market moment — same tick, same signal, different gate. |
| **Organizational Learning** | Provides a structured mechanism for testing alternative configurations (e.g., relaxed admission thresholds, adjusted risk brackets) without exposing capital. |
| **Decision-Engine Benchmarking** | Creates a baseline against which AA's improvement can be measured over time — not just "did AA win this trade?" but "did AA outperform its shadow?" |
| **Hypothesis Testing Infrastructure** | Shadow AA could serve as the controlled rollout mechanism referenced in the Finding Adoption Framework — a safe environment to test the operational implications of validated findings before live implementation. |

---

## 3. Potential Risks

Risks that would need to be evaluated before any implementation decision:

| Risk | Description |
|---|---|
| **Organizational Complexity** | A second decision engine introduces a second source of organizational noise. The team may mistake Shadow AA's outputs for findings before they are validated. |
| **Governance Contamination** | Shadow AA outputs could be used to justify premature changes to live AA if governance discipline is not maintained. |
| **Resource Diversion** | Building and maintaining Shadow AA requires engineering capacity that may have higher-value uses during the current evidence accumulation phase. |
| **False Confidence** | A Shadow AA that "outperforms" AA over a small sample provides no statistically meaningful signal. Premature promotion of shadow results could be worse than having no shadow at all. |
| **Dependency on Evidence Review Maturity** | Shadow AA is only useful if the organization has sufficient infrastructure to review, classify, and interpret its outputs correctly. That infrastructure is not yet mature. |

---

## 4. Unknowns

The following are material unknowns that must be resolved before the concept can be seriously evaluated:

1. **What decision framework would Shadow AA use?** An alternative framework must be evidence-backed, not assumed.
2. **How would Shadow AA's outputs be governed?** Who owns the ledger? Who reviews it? Who classifies outputs as Observations vs. Hypotheses?
3. **What is the minimum evidence threshold before Shadow AA results become research-grade?** The same evidence standards that apply to AA must apply to Shadow AA.
4. **Would Shadow AA use the same Saxo data feed?** If yes, does this introduce infrastructure risk for the live system?
5. **What does "outperformance" mean in this context?** Risk-adjusted returns over what time horizon? Against what baseline?
6. **Is the organization's current Evidence Review capacity sufficient to absorb Shadow AA outputs?** The current team is already reviewing AA's existing evidence. Additional output volume may be premature.

---

## 5. Evidence Required Before Consideration

Before this concept could be elevated from Hypothesis to a research-grade evaluation request, the following evidence conditions must be met:

1. **The organization has completed a full review of all existing Evidence Recovery ledgers.** We must exhaust the evidence we already have before generating new evidence infrastructure.
2. **The Shadow Risk Engine results have been fully reviewed and classified by GM.** The simulated blocked-signal outcomes must be analyzed first — they may answer the core question without requiring Shadow AA at all.
3. **At least one validated Finding has been produced** through the full `Data → Observation → GM Review → Hypothesis → Contradiction Test → Finding` workflow. The organization must demonstrate it can handle a Finding before it builds a system designed to generate more of them.
4. **A clear, testable hypothesis is defined** that only Shadow AA (and not existing evidence) can answer.
5. **Evelyn Cross (Mentor) has assessed AA's current learning trajectory** and confirmed that a benchmarking engine would accelerate rather than distract from AA's development.

---

## 6. Conditions Required Before Future Evaluation

Even if the evidence conditions in Section 5 are met, the following organizational conditions must exist before a Shadow AA evaluation can be formally initiated:

| Condition | Owner | Status |
|---|---|---|
| Current Evidence Review backlog is fully cleared | AG, GM | Not yet met |
| At least one validated Finding exists in the Findings Register | GM, Codex | Not yet met |
| Finding Adoption Framework has been exercised at least once | Helena Ward, GM | Not yet met |
| GM has formally requested a Shadow AA evaluation | GM | Not yet met |
| Kenny has been briefed and has not objected | Kenny | Not yet met |
| A governance framework for Shadow AA outputs has been designed | Helena Ward, GM | Not yet met |

---

## 7. Relationship to Existing Work

This concept is connected to — but distinct from — the following existing organizational work:

| Related Work | Relationship |
|---|---|
| Evidence Recovery Pilot | The pilot revealed the evidence density gap that makes Shadow AA conceptually attractive. Shadow AA would address future evidence density; the pilot addresses historical evidence density. |
| Shadow Risk Engine | The Shadow Risk Engine already performs a limited version of this concept offline, for historical blocked signals only. Shadow AA would extend this to real-time, forward-looking decisions. |
| Finding Adoption Framework | Shadow AA's controlled rollout mechanism could eventually be the controlled rollout environment referenced in the framework for Risk, Portfolio, and Strategy findings. |
| Observation Pipeline | Shadow AA would need its own Observation Pipeline governance structure before its outputs could enter the research workflow. |

---

## Status

**Idea captured.**

**No action authorized.**

**GM Review Required**
