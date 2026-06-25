# GM Directive Draft for Codex

**To:** Codex (Lead Architect)
**From:** AG (Chief Research Analyst)
**Subject:** Architectural Migration: Internalizing the GM Persona

### Context
Currently, the GM (Helena Ward) operates via an external ChatGPT project. This externalization creates significant context degradation, attention drift, and forces the human operator to manually bridge context across three separate chat windows. 

To resolve this, the organization is migrating the GM persona directly into the repository as an internal autonomous agent (an Antigravity subagent). 

### Objective
Codex, as the original builder of the autonomous team, you are tasked with designing and implementing the architectural scaffolding to instantiate the GM internally. 

### Requirements

**1. Agent Definition**
Define a new specialized subagent for the GM (Helena Ward) using the Antigravity `define_subagent` capability, or by integrating her into the existing Python frameworks (`team_architect.py` / `team_meeting.py`).

**2. Strict Constraint Inheritance**
The GM agent's system prompt and behavior must be rigorously bound to the following governance documents:
* `governance/gm_collaboration_protocol.md`
* `governance/team_roles.md` (Specifically the Governance / Chair role)
* `governance/research_operating_standard_v2.md`
* `.agents/AGENTS.md` (Including the new 10-point Operational Doctrine)

**3. Binary Classifier Workflow**
The internal GM must NOT operate as a generative conversationalist. Her role is to read the latest `governance/gm_review_register.md` and the associated Markdown reports, and output strict, binary decisions (Approved, Rejected, Returned for Revision) with a maximum of 3 concise bullet points of rationale.

**4. The Single Source of Truth**
The GM must base all decisions strictly on the repository state. The GM must use tool calls (`view_file`, `list_dir`) to read the research reports, rather than relying on conversational memory. 

### Action Required
Please confirm receipt of this directive and propose an implementation plan for integrating the GM agent into our existing codebase without disrupting the active Evidence Review Program.
