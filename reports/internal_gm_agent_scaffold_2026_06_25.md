# Internal GM Agent Scaffold

**Date:** 2026-06-25  
**Owner:** Codex  
**Status:** Implemented for review  
**Classification:** Infrastructure / Governance scaffold  

---

## Purpose

Instantiate Helena Ward as an internal repository-bound GM classifier.

This scaffold is designed to reduce external window management and keep GM decisions anchored to repository state rather than chat memory.

---

## Scope Implemented

Created:

- `saxo_trader/gm_agent.py`
- `tests/test_gm_agent.py`

Integrated:

- `saxo_trader/team_meeting.py` now exposes the internal GM manifest under `internal_gm_agent`.
- `tests/test_team_meeting.py` verifies the meeting framework recognizes Helena Ward as the repository-only classifier.

The scaffold provides:

- Internal GM manifest for Helena Ward.
- Strict decision labels:
  - `Approved`
  - `Rejected`
  - `Returned for Revision`
- Repository-only artifact review.
- Required governance-source checks.
- Report structure checks.
- Prohibited operational-change language checks.
- Maximum three rationale bullets.

---

## Governance Sources Bound

The scaffold requires these repository files to exist before review:

- `governance/gm_collaboration_protocol.md`
- `governance/team_roles.md`
- `governance/research_operating_standard_v2.md`

---

## Behavior Boundary

The internal GM scaffold:

- Reviews repository artifacts.
- Classifies review readiness.
- Returns concise rationale.
- Does not rely on chat memory.
- Does not generate free-form strategy advice.
- Does not authorize AA trading behavior changes.
- Does not modify code, strategy, thresholds, risk, portfolio, or execution logic.

---

## Non-Changes

No change was made to:

- AA trading logic
- Entry logic
- Exit logic
- Risk gates
- Portfolio rules
- Saxo order logic
- Runner behavior
- Dashboard behavior

---

## Validation

Tests added cover:

- GM manifest definition.
- Approved complete report.
- Returned-for-revision incomplete report.
- Rejected operational-change language.
- Path traversal protection.
- Required governance-source checks.
- Team meeting manifest integration.

Latest test result:

- `122 passed`

---

## GM Review Required
