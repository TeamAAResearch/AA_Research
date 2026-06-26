# AA Work Log Standard

**Status:** Active standard
**Effective Date:** 2026-06-26
**Owner:** Codex, maintained for GM review

## Purpose

Create concise, decision-useful work logs that explain not only what changed, but why it mattered.

Work logs should preserve institutional memory without turning observations into conclusions too early.

## Standard Sections

Each material work log should use the following structure where applicable:

1. **Observation**
   - What was noticed?
   - What evidence triggered the work?

2. **Research / Baseline**
   - What data, source, or analysis supported the work?
   - What assumptions were replaced or confirmed?

3. **Logic of Decisions**
   - Why was this path chosen?
   - What alternatives were rejected or deferred?

4. **Engineering Execution**
   - What files or systems were changed?
   - Who executed the change?
   - What tests or checks were run?

5. **Deployment / Operational State**
   - Was anything restarted, bounced, enabled, disabled, or left untouched?
   - What is the current live state?

6. **Strategic Roadmap / Open Questions**
   - What remains unresolved?
   - What belongs to future research rather than immediate action?

7. **Next Steps**
   - What should be observed, reviewed, or decided next?

## Attribution Rules

- Attribute execution precisely.
- Do not write that Codex, AG, GM, or Ari performed an action unless that action is evidenced.
- Separate research work from engineering work.
- Separate implementation from deployment.
- Separate dashboard viewing or server startup from dashboard code changes.

## Governance Rules

- Observation does not equal hypothesis.
- Hypothesis does not equal finding.
- Findings require surviving contradiction.
- Evidence alone does not authorize change.
- Recommendations require explicit GM request regardless of evidence strength.

## Classification Labels

Each work log should include one of:

- `Observation`
- `Research Report`
- `Engineering Execution`
- `Deployment Record`
- `Incident Report`
- `Simulation Observation`
- `Governance Decision`

## Required Integrity Checks

Before treating a work log as final, verify:

- Test results are stated if code changed.
- Runner state is stated if deployment changed.
- Source data is identified if research was performed.
- Uncertainty is preserved where evidence is incomplete.
- Any unverified claim is marked as unverified.

## Current Reference

AG's `reports/daily_report_2026_06_26.md` establishes the preferred narrative structure:

Observation -> Research -> Logic of Decisions -> Engineering Execution -> Deployment -> Roadmap -> Next Steps

This standard adopts that structure with stricter attribution and governance controls.

