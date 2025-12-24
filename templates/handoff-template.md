# Handoff: {SOURCE_PHASE} → {TARGET_PHASE}

> **Feature**: {FEATURE_ID}-{FEATURE_NAME}
> **Generated**: {DATE}
> **Source Agent**: {SOURCE_PERSONA}
> **Target Agent**: {TARGET_PERSONA}

---

## Summary

<!-- Brief description of what was accomplished in the source phase -->

{SUMMARY}

---

## Key Decisions Made

<!-- Document all significant decisions with rationale and alternatives considered -->

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| {DECISION_1} | {RATIONALE_1} | {ALTERNATIVES_1} |
| {DECISION_2} | {RATIONALE_2} | {ALTERNATIVES_2} |

---

## Constraints for Next Phase

<!-- Constraints that the target agent MUST respect -->

### Technical Constraints
- {TECHNICAL_CONSTRAINT_1}
- {TECHNICAL_CONSTRAINT_2}

### Business Constraints
- {BUSINESS_CONSTRAINT_1}
- {BUSINESS_CONSTRAINT_2}

### Time/Resource Constraints
- {RESOURCE_CONSTRAINT_1}

---

## Risks Identified

<!-- Risks discovered during this phase that affect the next phase -->

| Risk | Severity | Likelihood | Mitigation | Owner |
|------|----------|------------|------------|-------|
| {RISK_1} | HIGH/MEDIUM/LOW | HIGH/MEDIUM/LOW | {MITIGATION_1} | {OWNER_1} |
| {RISK_2} | HIGH/MEDIUM/LOW | HIGH/MEDIUM/LOW | {MITIGATION_2} | {OWNER_2} |

---

## Open Questions

<!-- Questions that could not be resolved in this phase -->

- [ ] {QUESTION_1}
  - **Context**: {CONTEXT_1}
  - **Impact if unresolved**: {IMPACT_1}
  - **Suggested owner**: {OWNER_1}

- [ ] {QUESTION_2}
  - **Context**: {CONTEXT_2}
  - **Impact if unresolved**: {IMPACT_2}
  - **Suggested owner**: {OWNER_2}

---

## Assumptions Made

<!-- Assumptions made during this phase that the next agent should validate -->

| Assumption | Basis | Validation Needed |
|------------|-------|-------------------|
| {ASSUMPTION_1} | {BASIS_1} | {VALIDATION_1} |
| {ASSUMPTION_2} | {BASIS_2} | {VALIDATION_2} |

---

## Phase-Specific Context

<!-- Context specific to the handoff type -->

### For specify-to-plan Handoffs
<!-- Include when SOURCE_PHASE = specify -->

**Domain Context**:
<!-- Industry-specific information (fintech, healthcare, e-commerce, etc.) -->
{DOMAIN_CONTEXT}

**User Value Priorities**:
<!-- Ranked list of what matters most to users -->
1. {PRIORITY_1}
2. {PRIORITY_2}
3. {PRIORITY_3}

**Clarifications Resolved**:
<!-- Q&A that shaped the specification -->
| Question | Answer | Impact on Spec |
|----------|--------|----------------|
| {Q1} | {A1} | {IMPACT_1} |

### For plan-to-tasks Handoffs
<!-- Include when SOURCE_PHASE = plan -->

**Architecture Decisions**:
<!-- Key ADRs that affect task breakdown -->
| Decision | Impact on Tasks |
|----------|-----------------|
| {ADR_1} | {TASK_IMPACT_1} |

**Integration Points**:
<!-- External systems and their constraints -->
| System | Interface | Constraint |
|--------|-----------|------------|
| {SYSTEM_1} | {INTERFACE_1} | {CONSTRAINT_1} |

**Performance Requirements**:
<!-- Non-functional requirements affecting implementation -->
| Metric | Target | Current Baseline |
|--------|--------|------------------|
| {METRIC_1} | {TARGET_1} | {BASELINE_1} |

### For tasks-to-implement Handoffs
<!-- Include when SOURCE_PHASE = tasks -->

**Critical Path**:
<!-- Tasks that determine the minimum completion time -->
{CRITICAL_PATH_SEQUENCE}

**Parallelization Opportunities**:
<!-- Tasks that can run concurrently -->
| Parallel Track | Tasks | Dependencies |
|----------------|-------|--------------|
| {TRACK_A} | {TASKS_A} | After {DEP_A} |

**Common Pitfalls**:
<!-- Known issues from similar implementations -->
| Pitfall | Context | Avoidance Strategy |
|---------|---------|-------------------|
| {PITFALL_1} | {CONTEXT_1} | {STRATEGY_1} |

**Testing Strategy**:
<!-- Overall testing approach -->
| Test Type | Coverage Target | Tools |
|-----------|-----------------|-------|
| Unit | {UNIT_TARGET}% | {UNIT_TOOLS} |
| Integration | {INT_TARGET}% | {INT_TOOLS} |
| E2E | {E2E_SCENARIOS} | {E2E_TOOLS} |

---

## Artifacts Produced

<!-- Files created or modified in this phase -->

| Artifact | Path | Purpose |
|----------|------|---------|
| {ARTIFACT_1} | {PATH_1} | {PURPOSE_1} |
| {ARTIFACT_2} | {PATH_2} | {PURPOSE_2} |

---

## Handoff Validation Checklist

<!-- Source agent confirms completeness before handoff -->

- [ ] All key decisions documented with rationale
- [ ] Risks identified and assessed
- [ ] Open questions listed with context
- [ ] Assumptions explicitly stated
- [ ] Phase-specific context provided
- [ ] Artifacts list is complete

---

## Next Agent Instructions

<!-- Specific guidance for the receiving agent -->

**Primary Focus**: {PRIMARY_FOCUS}

**Start Here**: {STARTING_POINT}

**Watch Out For**: {WARNINGS}

**Success Looks Like**: {SUCCESS_CRITERIA}

---

<!--
HANDOFF PROTOCOL:

1. Source agent completes their phase work
2. Source agent fills this template with phase-specific details
3. Source agent marks the handoff validation checklist
4. Target agent reads this document BEFORE starting their phase
5. Target agent validates assumptions and resolves open questions
6. Target agent proceeds with their phase work
-->
