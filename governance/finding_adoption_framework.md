# Finding Adoption Framework

**Version:** 1.0
**Date:** 2026-06-24
**Status:** Awaiting GM Review
**Repository:** TeamAAResearch/AA_Research
**Scope:** GM, AG, Codex, AA Operating Organization

---

## 1. Purpose

This framework defines the formal governance bridge between a validated research Finding and any resulting operational change within the AA trading organization.

It exists to prevent two failure modes:

- **Premature adoption:** Implementing a change before the Finding is sufficiently validated.
- **Finding inertia:** A validated Finding sitting idle because no adoption process exists.

**Canonical rule:**

> Finding ≠ Automatic Change

Every Finding, regardless of strength, must pass through the Adoption Review process before any operational behavior is modified.

---

## 2. Definitions

**Finding:**
A research claim that has survived contradiction testing, is supported by sufficient evidence, cites known limitations, and has been formally promoted by GM into the Findings Register.

**Adoption Review:**
A structured evaluation of whether and how an approved Finding should be translated into an operational change.

**Implementation Decision:**
The formal authorization (or rejection) of a proposed operational change derived from an Adoption Review.

**Controlled Rollout:**
A limited, time-bounded implementation of an approved change, designed to allow monitoring before permanent adoption.

**Permanent Adoption:**
The integration of a change into the AA operating baseline following a successful Controlled Rollout and Validation.

**Reversal:**
The withdrawal of an implemented change following adverse monitoring outcomes.

---

## 3. Finding Types

Not all Findings require operational change. Every Finding must first be classified by type before an Adoption Review is triggered.

| Type | Description | Example | Requires Operational Change? |
|---|---|---|---|
| **Research-Only** | Deepens organizational understanding but does not prescribe a change. | "Blocked signals have worse MFE than admitted signals on average." | No |
| **Mentoring** | Pertains to AA's learning or progression evaluation. | "AA has not demonstrated repeatable edge over N=100 trades." | No (unless GM escalates) |
| **Organizational** | Pertains to team structure, roles, or governance process. | "Evidence Review is operating without a formal submission standard." | Organizational change only |
| **Systems** | Pertains to infrastructure, data pipelines, or evidence collection. | "aa_journal parsing is incomplete, causing evidence gaps." | Systems change only |
| **Risk** | Pertains to AA's risk control behavior. | "Downside Limit freezes are costing more than they protect." | Requires full Adoption Review |
| **Portfolio** | Pertains to concentration limits or exposure rules. | "Correlation limit of 3 pairs is suppressing profitable flow." | Requires full Adoption Review |
| **Strategy** | Pertains to signal generation, admission logic, or thresholds. | "Momentum threshold is blocking high-expectancy setups." | Requires full Adoption Review |
| **Execution** | Pertains to trade management, exit rules, or entry timing. | "Exit management is leaking MFE consistently." | Requires full Adoption Review |

---

## 4. Adoption Workflow

```
Finding (Findings Register)
        │
        ▼
[1] Finding Classification
        │
        ▼
[2] Adoption Review
        │
   ┌────┴────┐
   │         │
[3a] Adopt  [3b] Defer / Reject
   │
   ▼
[4] Implementation Decision
        │
        ▼
[5] Controlled Rollout
        │
        ▼
[6] Monitoring Period
        │
   ┌────┴────┐
   │         │
[7a] Validate [7b] Reverse
   │
   ▼
[8] Permanent Adoption → Codex records in Findings Register
```

### Stage Detail

**[1] Finding Classification**
- Codex assigns a Finding Type from Section 3.
- Research-Only and Mentoring findings are archived; no adoption process triggered.
- All other types proceed to Adoption Review.

**[2] Adoption Review**
- Lead: Helena Ward (Governance / Chair)
- Support: Sofia Chen (Team Architect), Evelyn Cross (Mentor)
- Purpose: Evaluate whether the Finding warrants an operational change and whether organizational readiness exists.
- Output: Adoption Review Memo (committed to `governance/adoption_reviews/`)
- Duration: Defined per Finding; GM may set a deadline.

**[3a/3b] Adopt or Defer / Reject**
- Decision authority: GM (see Section 5).
- Deferral requires a condition: "Adopt when X additional evidence is available."
- Rejection requires a reason recorded in the Findings Register.

**[4] Implementation Decision**
- Owner: Kenny (Owner / Investment Committee) for Risk, Portfolio, Strategy, Execution findings.
- Owner: GM for Organizational and Systems findings.
- A formal Implementation Decision Memo is committed to `governance/implementation_decisions/`.
- The memo must state: what changes, what does not change, rollout duration, success criteria, reversal trigger.

**[5] Controlled Rollout**
- Owner: Relevant department head (see Section 6).
- Duration: Minimum 5 trading days unless GM grants exception.
- Scope: Changes apply to Challenger (paper trading) first. Live AA behavior changes require separate Kenny authorization.
- Codex records the rollout start in the Findings Register.

**[6] Monitoring Period**
- Owner: Mason Vale (Risk), Vera Lin (Execution), Theo Park (Systems) — depending on Finding type.
- Monitoring criteria are defined in the Implementation Decision Memo.
- Daily ledger updates continue throughout monitoring.

**[7a] Validate**
- Validation criteria defined in advance in the Implementation Decision Memo.
- Validation requires GM review of monitoring data.
- Evelyn Cross provides a learning assessment.

**[7b] Reverse**
- Reversal trigger is defined in advance in the Implementation Decision Memo.
- Reversal authority: GM, or Kenny if the change touched live AA behavior.
- Codex records the reversal and its reason in the Findings Register.

**[8] Permanent Adoption**
- Codex updates the Findings Register to mark the Finding as "Permanently Adopted."
- Codex commits the updated organizational charter or policy document reflecting the permanent change.

---

## 5. Approval Authority

| Decision | Authority | Cannot Be Delegated To |
|---|---|---|
| Promote a Finding into the Findings Register | GM | AG, Codex, AA Operating Team |
| Classify Finding type | Codex (with GM confirmation) | AG alone |
| Initiate Adoption Review | GM | Any team member |
| Approve Adoption Review outcome | GM | Helena Ward alone |
| Authorize Implementation for Organizational / Systems findings | GM | Any team member |
| Authorize Implementation for Risk / Portfolio / Strategy / Execution findings | Kenny | GM alone |
| Approve Controlled Rollout start | GM | Any team member |
| Validate successful rollout | GM | Any team member |
| Approve Permanent Adoption | Kenny (Risk/Portfolio/Strategy/Execution), GM (Org/Systems) | Any other entity |
| Authorize Reversal | GM (Org/Systems), Kenny (Risk/Portfolio/Strategy/Execution) | Any team member |
| Request additional evidence before decision | GM, Helena Ward, Evelyn Cross | No restriction |

---

## 6. Departmental Ownership by Finding Type

| Finding Type | Adoption Review Lead | Implementation Owner | Monitoring Owner |
|---|---|---|---|
| Research-Only | Not triggered | Not applicable | Not applicable |
| Mentoring | Evelyn Cross | Not applicable | Evelyn Cross |
| Organizational | Helena Ward | Sofia Chen | Helena Ward |
| Systems | Theo Park | Theo Park | Vera Lin |
| Risk | Helena Ward | Mason Vale | Mason Vale |
| Portfolio | Helena Ward | Clara Stone | Mason Vale |
| Strategy | Helena Ward | Ari Axelrod | Rowan Pierce |
| Execution | Helena Ward | Vera Lin | Vera Lin |

---

## 7. Guardrails

**Finding ≠ Automatic Change**

The following are explicitly prohibited at every stage:

- Implementing any operational change without a completed Adoption Review.
- Treating an Observation or Hypothesis as a Finding for adoption purposes.
- Implementing a Risk, Portfolio, Strategy, or Execution change without Kenny's written authorization.
- Bypassing the Controlled Rollout phase for any Risk, Portfolio, Strategy, or Execution finding.
- Changing live AA trading behavior during the current governance freeze without explicit Kenny authorization.

**The governance freeze remains in effect.**
This framework is designed for when the freeze is selectively lifted. The framework itself does not lift the freeze.

---

## 8. Repository Structure

The following directories support this framework:

```
governance/
    finding_adoption_framework.md       <- This document
    adoption_reviews/                   <- One memo per Finding undergoing review
    implementation_decisions/           <- One memo per approved Implementation Decision

findings/
    findings_register.md                <- Master record of all Findings and their adoption status
```

---

## 9. Roles Summary

| Entity | Role in Adoption Process |
|---|---|
| **GM** | Initiates Adoption Reviews; approves Organizational and Systems implementations; validates rollouts; approves Permanent Adoption for Org/Systems. |
| **Kenny** | Authorizes all Risk, Portfolio, Strategy, and Execution implementations; approves Permanent Adoption for those types. |
| **AG** | Provides additional evidence if requested during Adoption Review; does not vote on adoption decisions. |
| **Codex** | Classifies Finding type; maintains Findings Register; commits all Adoption Review memos and Implementation Decision memos; records rollout status, validation, and reversal. |
| **Helena Ward** | Leads Adoption Reviews; enforces evidence standards; can request more evidence before any decision. |
| **Evelyn Cross** | Provides learning assessment during Adoption Review; leads Mentoring Finding reviews. |
| **Sofia Chen** | Supports Adoption Review as Team Architect; ensures the correct problem is being solved; flags scope creep. |
| **Ari Axelrod** | Implementation owner for Strategy findings; provides trading-behavior context during Adoption Review. |
| **Mason Vale** | Implementation and monitoring owner for Risk findings; provides risk-control context during Adoption Review. |
| **Relevant departments** | Provide domain context during Adoption Review; own implementation execution when assigned. |

---

## 10. Operating Principle

The Finding Adoption Framework exists to protect the organization from two equal and opposite risks:

1. Acting too fast on insufficient evidence.
2. Failing to act on validated evidence.

The framework resolves both by requiring a structured, time-bounded, authorized process — independent of urgency or enthusiasm.

> Evidence owns the organization.
> Not AG. Not Codex. Not GM. Not AA. Not Kenny.

**GM Review Required**
