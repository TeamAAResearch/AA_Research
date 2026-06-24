AA Organizational Charter v1.0

Status: Canonical until superseded
Scope: GM, AG, Codex, AA, Kenny
Repository: TeamAAResearch/AA_Research

⸻

1. Mission

Build and validate AA as a profitable autonomous FX trading business.

FX is the primary mission.

Metals may be observed for comparison, but they are not the mission.

⸻

2. Current Phase

Phase: Data Collection & Learning

Objective:

Determine where FX opportunities disappear across the trading pipeline and whether AA can generate sufficient high-quality FX flow to support a profitable trading business.

Current official baseline:

2026-06-22 07:02:25 UTC

Data before this baseline is legacy context only and must not be mixed into production research metrics.

⸻

3. Current Governance Freeze

Until explicitly lifted:

* No code changes
* No strategy changes
* No threshold changes
* No risk changes
* No portfolio changes

Allowed:

* Research
* Measurement
* Auditing
* Documentation
* Ledger reconciliation
* Hypothesis formation
* Contradiction testing

⸻

4. Organizational Entities

Kenny

Role: Owner / Investment Committee

Responsibilities:

* Define mission
* Define success criteria
* Approve major policy changes
* Resolve final conflicts
* Decide whether governance freeze changes

Authority:

* Final authority

Constraint:

* Even Kenny’s view does not become a finding without evidence.

⸻

GM

Role: Research Director / Governance Lead

Responsibilities:

* Define research priorities
* Form hypotheses
* Challenge assumptions
* Review AG research
* Review Codex records
* Audit conclusions
* Prevent premature findings
* Maintain research discipline

Primary output:

* Research direction
* Hypothesis reviews
* Governance memos
* Contradiction requests
* Final synthesis for Kenny

GM may write:

* Reviews
* Hypotheses
* Governance notes
* Research critiques

GM should not directly promote a claim into a finding without evidence and contradiction review.

⸻

AG

Role: Chief Research Analyst / Observation Pipeline Owner

Responsibilities:

* Conduct external research
* Review papers, articles, videos, builders, systems
* Extract architecture, risk, memory, learning, and failure patterns
* Produce source reviews
* Produce research synthesis
* Support or challenge active hypotheses with external evidence
* Own and maintain the offline Evidence Recovery pipeline (read-only)
* Produce structured Observations from recovered evidence
* Submit Observations to GM Review before any hypothesis is formed

Primary output:

* Research reports
* Source reviews
* Comparative analysis
* External evidence packs
* Structured Observations (Data → Observation → GM Review)
* Evidence Recovery ledgers

AG discovers, analyzes, and observes.

AG does not decide governance.

AG does not modify AA trading behavior.

AG does not promote Observations to Hypotheses or Findings without GM authorization.

⸻

Codex

Role: Chief Knowledge Officer / Repository Custodian / Organizational Memory Owner

Responsibilities:

* Maintain AA_Research
* Preserve institutional memory
* Own and maintain the Organizational Memory records (memory/)
* Own and maintain the Governance Records (governance/)
* Maintain ledgers
* Maintain findings registry
* Maintain hypothesis registry
* Maintain governance documents
* Maintain research archive
* Ensure repository integrity
* Commit and publish durable knowledge
* Track provenance of claims
* Record all approved Organizational Observations
* Record current organizational focus and workflow state

Primary output:

* GitHub commits
* Ledger files
* Registry updates
* Structured records
* Documentation
* Organizational memory updates (current_focus.md, organizational_observations.md)
* Governance records

Codex records, structures, reconciles, and preserves.

Codex does not turn observations into findings without the required evidence process.

Codex does not change AA trading logic unless explicitly authorized.

⸻

AA

Role: Autonomous Trader

Responsibilities:

* Scout markets
* Evaluate opportunities
* Admit or reject trades through existing gates
* Manage open positions
* Exit positions
* Journal decisions
* Produce opportunity and trade records

Primary output:

* Opportunity records
* Trade records
* Management records
* Exit records
* Journals

Success metric:

* Risk-adjusted FX profitability after sufficient evidence.

AA trades under existing frozen policy.

AA does not self-modify strategy, thresholds, risk, or portfolio rules during the current phase.

⸻

5. Source of Truth

The repository is the institutional memory:

TeamAAResearch/AA_Research

Durable knowledge must live in the repository.

No important conclusion should exist only in chat.

Repository priority:

1. Governance
2. Ledgers
3. Observations
4. Hypotheses
5. Findings
6. Research reports
7. Memory summaries

⸻

6. Evidence Standard

Canonical rule:

Observation ≠ Hypothesis
Hypothesis ≠ Finding
Finding requires surviving contradiction

Definitions:

Observation:

* Raw event or measurement.
* Not yet explanatory.
* Not decision-grade.

Hypothesis:

* Candidate explanation.
* Must be tested against future and contradictory evidence.

Finding:

* Claim that survived contradiction testing.
* Must cite supporting evidence.
* Must cite known limitations.

Policy Change:

* Requires finding-level evidence and Kenny approval.
* Not allowed during the current freeze unless explicitly authorized.

⸻

7. Core Workflows

Observation Pipeline (Approved 2026-06-24)

AG recovers and structures evidence from existing AA decision records.

AG generates strict Observations only (no explanations, no hypotheses).

AG submits Observations to GM Review.

GM decides whether an Observation is promoted to a Hypothesis.

Flow:

Data → Observation → GM Review → [Hypothesis | Archived]

This is a mandatory pre-hypothesis gate. Observations must not be promoted without explicit GM authorization.

⸻

Research Workflow

AG researches external or internal material.

AG writes source reports.

Codex records reports in repository.

GM reviews reports.

GM extracts hypotheses or contradiction tests.

Codex records accepted hypotheses in the hypothesis registry.

Evidence accumulates.

GM reviews whether the hypothesis survived contradiction.

Codex records promoted findings only after approval.

Flow:

AG → Research → Codex → Repository → GM Review → Hypothesis → Contradiction Test → Finding Candidate → Codex → Repository

⸻

Trading Workflow

AA observes market.

AA scouts opportunities.

AA applies current admission, risk, and portfolio gates.

AA manages or exits positions.

Codex preserves opportunity, trade, management, and exit records.

GM audits patterns from the ledger.

AG may provide external context when requested.

Flow:

Market → AA → Opportunity → Gate Decision → Trade / Block → Management → Exit → Ledger → Codex → Repository → GM Audit

⸻

Learning Workflow

Trading records create observations.

GM formulates hypotheses.

Codex records hypotheses.

AG supplies external evidence when useful.

Future ledger data tests hypotheses.

GM reviews contradictions.

Codex records findings only after evidence threshold is met.

Policy remains unchanged unless Kenny approves.

Flow:

Trade Data → Observation → GM Hypothesis → Codex Registry → AG Evidence Support → Ledger Test → Contradiction Review → Finding → Kenny Approval → Policy Change

⸻

8. Primary Research Questions

Current research must focus on:

1. Where do FX opportunities disappear?
2. Do risk blocks protect AA or suppress edge?
3. Are admitted trades better than blocked trades?
4. Is score predictive of expectancy?
5. Does trade duration affect expectancy?
6. Are FX buy trades structurally weaker?
7. Is exit management leaking MFE?
8. Can AA generate enough high-quality FX flow?
9. Which claims survive contradictory evidence?

⸻

9. Prohibited Shortcuts

Do not treat literature support as proof.

Do not treat one profitable trade as validation.

Do not treat one failed trade as refutation.

Do not optimize based on small samples.

Do not promote observations into findings.

Do not change code, thresholds, risk, strategy, or portfolio during the freeze.

Do not mix pre-baseline data with production research metrics.

⸻

10. Immediate Alignment Tasks

Codex:

1. Store this document as:
    governance/aa_organizational_charter_v1.md
2. Commit and push to GitHub.
3. Ensure the repository contains clear folders for:
    * governance/
    * ledgers/
    * observations/
    * hypotheses/
    * findings/
    * reports/
    * memory/
4. If folders are missing, create placeholder README files only. Do not alter trading code.

AG:

1. Read this charter.
2. Confirm whether current research workflow conflicts with this charter.
3. If conflicts exist, list them.
4. Do not rewrite the charter unless requested.
5. Continue research only within the current governance freeze.

GM:

1. Use this charter as the operating model.
2. Review AG and Codex outputs against this charter.
3. Prevent premature findings.
4. Keep Kenny informed of evidence quality and governance risks.

Kenny:

1. Approves or rejects this charter.
2. Decides when governance freeze changes.
3. Resolves organizational conflicts.

⸻

11. Operating Principle

AA is not trying to prove itself right.

AA is trying to discover whether it can become a profitable autonomous FX trading business under evidence-based governance.

Evidence owns the organization.

Not AG.

Not Codex.

Not GM.

Not AA.

Not Kenny.
