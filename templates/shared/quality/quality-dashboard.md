# Quality Dashboard

> **Unified quality metrics aggregation across all Spec Kit phases**

---

## Executive Summary

| Metric | Score | Target | Status | Trend |
|--------|-------|--------|--------|-------|
| **CQS** (Concept) | `{{CQS_SCORE}}`/120 | ≥80 | `{{CQS_STATUS}}` | `{{CQS_TREND}}` |
| **SQS** (Specification) | `{{SQS_SCORE}}`/100 | ≥80 | `{{SQS_STATUS}}` | `{{SQS_TREND}}` |
| **Plan Completeness** | `{{PLAN_PCT}}`% | ≥90% | `{{PLAN_STATUS}}` | `{{PLAN_TREND}}` |
| **Tasks INVEST** | `{{TASKS_PCT}}`% | ≥95% | `{{TASKS_STATUS}}` | `{{TASKS_TREND}}` |
| **Implementation Gates** | `{{IMPL_PASS}}`/`{{IMPL_TOTAL}}` | All pass | `{{IMPL_STATUS}}` | `{{IMPL_TREND}}` |

**Overall Readiness**: `{{OVERALL_STATUS}}`

---

## Phase 1: Concept Quality (CQS)

*Source: `/speckit.concept` → `concept.md`*

### CQS Score Breakdown

| Component | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Strategic Clarity | 25% | `{{CQS_STRATEGIC}}`/100 | `{{CQS_STRATEGIC_W}}` |
| Market Validation | 25% | `{{CQS_MARKET}}`/100 | `{{CQS_MARKET_W}}` |
| Technical Feasibility | 20% | `{{CQS_TECHNICAL}}`/100 | `{{CQS_TECHNICAL_W}}` |
| Risk Assessment | 15% | `{{CQS_RISK}}`/100 | `{{CQS_RISK_W}}` |
| Evidence Quality | 15% | `{{CQS_EVIDENCE}}`/100 | `{{CQS_EVIDENCE_W}}` |

### Evidence Tier Distribution

| Tier | Count | Percentage | Quality |
|------|-------|------------|---------|
| Tier 1 (Primary) | `{{T1_COUNT}}` | `{{T1_PCT}}`% | Excellent |
| Tier 2 (Secondary) | `{{T2_COUNT}}` | `{{T2_PCT}}`% | Good |
| Tier 3 (Assumptions) | `{{T3_COUNT}}` | `{{T3_PCT}}`% | Needs Validation |

**CQS Evidence Multiplier**: `{{CQS_MULTIPLIER}}`x

---

## Phase 2: Specification Quality (SQS)

*Source: `/speckit.specify` → `spec.md`*

### SQS Score Breakdown (25-point rubric)

| Dimension | Max | Score | Details |
|-----------|-----|-------|---------|
| **Clarity** | 25 | `{{SQS_CLARITY}}` | RFC keywords, specific numbers, defined failures |
| **Completeness** | 25 | `{{SQS_COMPLETE}}` | FRs, NFRs, edge cases, dependencies, security |
| **Testability** | 25 | `{{SQS_TEST}}` | ACs per FR, concrete scenarios, performance metrics |
| **Traceability** | 15 | `{{SQS_TRACE}}` | Unique IDs, concept links, FR→AC→Test chain |
| **No Ambiguity** | 10 | `{{SQS_AMBIG}}` | No hedge words, terms defined, scope explicit |

### SQS Checkpoint Summary

```
Clarity:      [{{CL01}}][{{CL02}}][{{CL03}}][{{CL04}}][{{CL05}}] = {{SQS_CLARITY}}/25
Completeness: [{{CM01}}][{{CM02}}][{{CM03}}][{{CM04}}][{{CM05}}] = {{SQS_COMPLETE}}/25
Testability:  [{{TS01}}][{{TS02}}][{{TS03}}][{{TS04}}][{{TS05}}] = {{SQS_TEST}}/25
Traceability: [{{TR01}}][{{TR02}}][{{TR03}}][{{TR04}}][{{TR05}}] = {{SQS_TRACE}}/15
No Ambiguity: [{{AM01}}][{{AM02}}][{{AM03}}][{{AM04}}][{{AM05}}] = {{SQS_AMBIG}}/10
─────────────────────────────────────────────────────────
TOTAL SQS:                                              {{SQS_SCORE}}/100
```

### Requirements Coverage

| Category | Count | With AC | Coverage |
|----------|-------|---------|----------|
| Functional (FR) | `{{FR_COUNT}}` | `{{FR_WITH_AC}}` | `{{FR_COV}}`% |
| Non-Functional (NFR) | `{{NFR_COUNT}}` | `{{NFR_WITH_AC}}` | `{{NFR_COV}}`% |
| Edge Cases | `{{EDGE_COUNT}}` | `{{EDGE_WITH_AC}}` | `{{EDGE_COV}}`% |

---

## Phase 3: Plan Quality

*Source: `/speckit.plan` → `plan.md`*

### Plan Completeness

| Section | Status | Notes |
|---------|--------|-------|
| Technical Context | `{{PLAN_CONTEXT}}` | Dependencies, constraints |
| Architecture Decisions | `{{PLAN_ARCH}}` | ADRs with rationale |
| Phase Breakdown | `{{PLAN_PHASES}}` | Clear milestones |
| Pre-Mortem | `{{PLAN_PREMORTEM}}` | Risk scenarios |
| RACI Matrix | `{{PLAN_RACI}}` | Accountability assigned |

### Clarification Status

| Total Markers | Resolved | Remaining |
|---------------|----------|-----------|
| `{{CLARIFY_TOTAL}}` | `{{CLARIFY_DONE}}` | `{{CLARIFY_REMAIN}}` |

**[NEEDS CLARIFICATION]** markers remaining: `{{CLARIFY_REMAIN}}`

---

## Phase 4: Tasks Quality

*Source: `/speckit.tasks` → `tasks.md`*

### INVEST Compliance

| Criteria | Compliant | Total | Percentage |
|----------|-----------|-------|------------|
| **I**ndependent | `{{INV_I}}` | `{{TASK_TOTAL}}` | `{{INV_I_PCT}}`% |
| **N**egotiable | `{{INV_N}}` | `{{TASK_TOTAL}}` | `{{INV_N_PCT}}`% |
| **V**aluable | `{{INV_V}}` | `{{TASK_TOTAL}}` | `{{INV_V_PCT}}`% |
| **E**stimable | `{{INV_E}}` | `{{TASK_TOTAL}}` | `{{INV_E_PCT}}`% |
| **S**mall | `{{INV_S}}` | `{{TASK_TOTAL}}` | `{{INV_S_PCT}}`% |
| **T**estable | `{{INV_T}}` | `{{TASK_TOTAL}}` | `{{INV_T_PCT}}`% |

### Task Size Distribution

| Size | Count | Percentage | Recommendation |
|------|-------|------------|----------------|
| XS (1-2h) | `{{SIZE_XS}}` | `{{SIZE_XS_PCT}}`% | Ideal for quick wins |
| S (2-4h) | `{{SIZE_S}}` | `{{SIZE_S_PCT}}`% | Good granularity |
| M (4-8h) | `{{SIZE_M}}` | `{{SIZE_M_PCT}}`% | Standard task size |
| L (8-16h) | `{{SIZE_L}}` | `{{SIZE_L_PCT}}`% | Consider splitting |
| XL (16-32h) | `{{SIZE_XL}}` | `{{SIZE_XL_PCT}}`% | Should split |
| XXL (32h+) | `{{SIZE_XXL}}` | `{{SIZE_XXL_PCT}}`% | MUST split |

### Definition of Done Coverage

| Task Type | With DoD | Without DoD |
|-----------|----------|-------------|
| Implementation | `{{DOD_IMPL}}` | `{{DOD_IMPL_NO}}` |
| Test | `{{DOD_TEST}}` | `{{DOD_TEST_NO}}` |
| Design | `{{DOD_DESIGN}}` | `{{DOD_DESIGN_NO}}` |

---

## Phase 5: Implementation Quality

*Source: `/speckit.implement` → implementation artifacts*

### Quality Gate Status

| Gate | ID | Status | Details |
|------|----|----- --|---------|
| Spec Complete | QG-002 | `{{QG002}}` | SQS ≥ 80 |
| Plan Approved | QG-003 | `{{QG003}}` | Pre-mortem done |
| Tasks Ready | QG-004 | `{{QG004}}` | INVEST ≥ 95% |
| Test Coverage | QG-007 | `{{QG007}}` | Coverage target met |
| Lint/Type | QG-008 | `{{QG008}}` | Zero critical issues |
| Security | QG-009 | `{{QG009}}` | OWASP check passed |
| Performance | QG-010 | `{{QG010}}` | NFR benchmarks met |
| Accessibility | QG-011 | `{{QG011}}` | A11y level achieved |

### Implementation Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Test Coverage | `{{IMPL_COV}}`% | `{{IMPL_COV_TARGET}}`% | `{{IMPL_COV_STATUS}}` |
| Type Coverage | `{{IMPL_TYPE}}`% | `{{IMPL_TYPE_TARGET}}`% | `{{IMPL_TYPE_STATUS}}` |
| Lint Errors | `{{IMPL_LINT}}` | 0 critical | `{{IMPL_LINT_STATUS}}` |
| Bundle Size | `{{IMPL_BUNDLE}}` | `{{IMPL_BUNDLE_TARGET}}` | `{{IMPL_BUNDLE_STATUS}}` |

---

## Red Flags

*Issues requiring immediate attention*

### Critical (Block Release)

| Flag | Severity | Location | Action |
|------|----------|----------|--------|
<!-- markdownlint-disable-next-line MD055 -->
{{#RED_FLAGS_CRITICAL}}
| `{{FLAG_ID}}` | CRITICAL | `{{FLAG_LOC}}` | `{{FLAG_ACTION}}` |
<!-- markdownlint-disable-next-line MD055 -->
{{/RED_FLAGS_CRITICAL}}

### Warning (Address Before GA)

| Flag | Severity | Location | Action |
|------|----------|----------|--------|
<!-- markdownlint-disable-next-line MD055 -->
{{#RED_FLAGS_WARNING}}
| `{{FLAG_ID}}` | WARNING | `{{FLAG_LOC}}` | `{{FLAG_ACTION}}` |
<!-- markdownlint-disable-next-line MD055 -->
{{/RED_FLAGS_WARNING}}

### Red Flag Triggers

| Signal | Threshold | Current | Status |
|--------|-----------|---------|--------|
| SQS Score | <60 | `{{SQS_SCORE}}` | `{{SQS_RF}}` |
| Unresolved Clarifications | >5 | `{{CLARIFY_REMAIN}}` | `{{CLARIFY_RF}}` |
| Missing Pre-Mortem | Any | `{{PREMORTEM_RF}}` | `{{PREMORTEM_STATUS}}` |
| XXL Tasks | >0 | `{{SIZE_XXL}}` | `{{XXL_RF}}` |
| Tier 3 Evidence on P0 | >0 | `{{T3_P0_COUNT}}` | `{{T3_P0_RF}}` |
| Missing DoD | >0 | `{{DOD_MISSING}}` | `{{DOD_RF}}` |
| No Rollout Plan | Any | `{{ROLLOUT_RF}}` | `{{ROLLOUT_STATUS}}` |

---

## Trend Analysis

*Quality metrics over time (if historical data available)*

### Score History

| Date | CQS | SQS | Plan | Tasks | Impl |
|------|-----|-----|------|-------|------|
<!-- markdownlint-disable-next-line MD055 -->
{{#HISTORY}}
| `{{DATE}}` | `{{H_CQS}}` | `{{H_SQS}}` | `{{H_PLAN}}` | `{{H_TASKS}}` | `{{H_IMPL}}` |
<!-- markdownlint-disable-next-line MD055 -->
{{/HISTORY}}

### Improvement Velocity

- **SQS Delta**: `{{SQS_DELTA}}` points since last assessment
- **Clarifications Resolved**: `{{CLARIFY_RESOLVED}}` in last 7 days
- **Tasks Completed**: `{{TASKS_DONE}}`/`{{TASK_TOTAL}}`

---

## Recommendations

### Immediate Actions

{{#RECOMMENDATIONS}}
1. **`{{REC_TITLE}}`**: `{{REC_DESC}}`
   - Impact: `{{REC_IMPACT}}`
   - Effort: `{{REC_EFFORT}}`
{{/RECOMMENDATIONS}}

### Quality Improvement Roadmap

| Priority | Action | Target Score | Effort |
|----------|--------|--------------|--------|
| P0 | `{{P0_ACTION}}` | `{{P0_TARGET}}` | `{{P0_EFFORT}}` |
| P1 | `{{P1_ACTION}}` | `{{P1_TARGET}}` | `{{P1_EFFORT}}` |
| P2 | `{{P2_ACTION}}` | `{{P2_TARGET}}` | `{{P2_EFFORT}}` |

---

## Quick Commands

```bash
# Generate this dashboard
/speckit.analyze --profile quality_dashboard

# Individual phase assessments
/speckit.analyze --profile cqs      # Concept Quality
/speckit.analyze --profile sqs      # Specification Quality
/speckit.analyze --profile plan     # Plan Completeness
/speckit.analyze --profile tasks    # Task INVEST Compliance
/speckit.analyze --profile impl     # Implementation Gates

# Full analysis
/speckit.analyze --profile full
```

---

## Dashboard Metadata

| Field | Value |
|-------|-------|
| Generated | `{{GENERATED_AT}}` |
| Feature | `{{FEATURE_NAME}}` |
| Version | `{{SPEC_VERSION}}` |
| Analyzer | Spec Kit Quality Framework v2.0 |

---

*Quality Dashboard v2.0 | Part of Spec Kit Quality Framework*
