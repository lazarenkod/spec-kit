# Spec-Driven Development Metrics Report

**Feature**: {{FEATURE_NAME}}
**Spec File**: {{SPEC_FILE}}
**Generated**: {{DATE}}
**Session Duration**: {{SESSION_DURATION}}

---

## Executive Summary

| Metric Category | Score | Status |
|-----------------|-------|--------|
| **Spec Quality (SQS)** | {{SQS}}/100 | {{SQS_STATUS}} |
| **Velocity** | {{VELOCITY_SCORE}}/4 targets met | {{VELOCITY_STATUS}} |
| **Cost Efficiency** | ${{TOTAL_COST}} ({{COST_VS_TARGET}}% of target) | {{COST_STATUS}} |

**Overall Assessment**: {{OVERALL_ASSESSMENT}}

---

## 1. Spec Quality Score (SQS)

### Score Breakdown (25-Checkpoint Rubric v2.0)

**Formula**: `SQS = Clarity + Completeness + Testability + Traceability + NoAmbiguity`

| Dimension | Score | Max | Key Checkpoints | Status |
|-----------|-------|-----|-----------------|--------|
| **Clarity** | {{SQS_CLARITY}} | 25 | RFC keywords, specificity, measurability | {{CLARITY_STATUS}} |
| **Completeness** | {{SQS_COMPLETE}} | 25 | FRs, NFRs, edge cases, dependencies | {{COMPLETE_STATUS}} |
| **Testability** | {{SQS_TEST}} | 25 | ACs, scenarios, performance metrics | {{TEST_STATUS}} |
| **Traceability** | {{SQS_TRACE}} | 15 | IDs, cross-refs, FR→AC→Test chain | {{TRACE_STATUS}} |
| **No Ambiguity** | {{SQS_AMBIG}} | 10 | No hedge words, terms defined, scope explicit | {{AMBIG_STATUS}} |
| **SQS Total** | **{{SQS}}** | **100** | | **{{SQS_LEVEL}}** |

### Checkpoint Details

```
Clarity:      [{{CL01}}][{{CL02}}][{{CL03}}][{{CL04}}][{{CL05}}] = {{SQS_CLARITY}}/25
Completeness: [{{CM01}}][{{CM02}}][{{CM03}}][{{CM04}}][{{CM05}}] = {{SQS_COMPLETE}}/25
Testability:  [{{TS01}}][{{TS02}}][{{TS03}}][{{TS04}}][{{TS05}}] = {{SQS_TEST}}/25
Traceability: [{{TR01}}][{{TR02}}][{{TR03}}][{{TR04}}][{{TR05}}] = {{SQS_TRACE}}/15
No Ambiguity: [{{AM01}}][{{AM02}}][{{AM03}}][{{AM04}}][{{AM05}}] = {{SQS_AMBIG}}/10
```

**Full Rubric**: See [templates/shared/quality/sqs-rubric.md](../shared/quality/sqs-rubric.md)

### Quality Level

| Level | Threshold | Your Score | Result |
|-------|-----------|------------|--------|
| Below MVP | < 80 | {{SQS}} | {{BELOW_MVP_CHECK}} |
| MVP Ready | 80-89 | {{SQS}} | {{MVP_CHECK}} |
| Full Feature | 90-99 | {{SQS}} | {{FULL_CHECK}} |
| Production Ready | 100 | {{SQS}} | {{PROD_CHECK}} |

**Quality Gate**: {{QUALITY_GATE_RESULT}}

### Component Analysis

#### FR Coverage ({{FR_COVERAGE}}%)
- **Total FRs**: {{TOTAL_FRS}}
- **FRs with Tasks**: {{FRS_WITH_TASKS}}
- **Unmapped FRs**: {{UNMAPPED_FRS}}
{{#if UNMAPPED_FRS_LIST}}
  - {{UNMAPPED_FRS_LIST}}
{{/if}}

#### AS Coverage ({{AS_COVERAGE}}%)
- **Total Acceptance Scenarios**: {{TOTAL_AS}}
- **AS with Tests**: {{AS_WITH_TESTS}}
- **Untested AS**: {{UNTESTED_AS}}
{{#if UNTESTED_AS_LIST}}
  - {{UNTESTED_AS_LIST}}
{{/if}}

#### Traceability ({{TRACEABILITY}}%)
- **Total Code Files**: {{TOTAL_CODE_FILES}}
- **Files with @speckit Annotations**: {{ANNOTATED_FILES}}
- **Unannotated Files**: {{UNANNOTATED_FILES}}

#### Constitution Compliance ({{CONSTITUTION}}%)
- **Total Principles Checked**: {{TOTAL_PRINCIPLES}}
- **Principles Satisfied**: {{SATISFIED_PRINCIPLES}}
- **Violations**: {{VIOLATIONS_COUNT}}
{{#if VIOLATIONS_LIST}}
  - {{VIOLATIONS_LIST}}
{{/if}}

---

## 2. Velocity Metrics

### Performance Against Targets

| Metric | Value | Target | Delta | Status |
|--------|-------|--------|-------|--------|
| Time to First Working Code | {{TIME_TO_FIRST_CODE}} min | < 10 min | {{TTFC_DELTA}} | {{TTFC_STATUS}} |
| Time to MVP (Wave 1) | {{TIME_TO_MVP}} min | < 30 min | {{TTMVP_DELTA}} | {{TTMVP_STATUS}} |
| Human Intervention Rate | {{HUMAN_INTERVENTION}}% | < 30% | {{HIR_DELTA}} | {{HIR_STATUS}} |
| Auto-Fix Success Rate | {{AUTOFIX_SUCCESS}}% | > 70% | {{AFS_DELTA}} | {{AFS_STATUS}} |

### Velocity Score

**Targets Met**: {{VELOCITY_TARGETS_MET}}/4
**Velocity Rating**: {{VELOCITY_RATING}}

| Rating | Criteria |
|--------|----------|
| Excellent | 4/4 targets met |
| Good | 3/4 targets met |
| Acceptable | 2/4 targets met |
| Needs Improvement | 1/4 or 0/4 targets met |

### Timeline Breakdown

| Phase | Start | End | Duration |
|-------|-------|-----|----------|
| Session Start | {{SESSION_START}} | - | - |
| First Test Pass | {{FIRST_TEST_TIME}} | - | {{TIME_TO_FIRST_CODE}} min |
| Wave 1 Complete | {{WAVE1_COMPLETE}} | - | {{TIME_TO_MVP}} min |
| Session End | - | {{SESSION_END}} | {{SESSION_DURATION}} |

### Intervention Analysis

| Intervention Type | Count | Percentage |
|-------------------|-------|------------|
| Manual Code Edits | {{MANUAL_EDITS}} | {{MANUAL_EDITS_PCT}}% |
| Requirement Clarifications | {{CLARIFICATIONS}} | {{CLARIFICATIONS_PCT}}% |
| Build Fix Overrides | {{BUILD_OVERRIDES}} | {{BUILD_OVERRIDES_PCT}}% |
| Test Fix Overrides | {{TEST_OVERRIDES}} | {{TEST_OVERRIDES_PCT}}% |
| **Total Interventions** | {{TOTAL_INTERVENTIONS}} | {{HUMAN_INTERVENTION}}% |

### Self-Healing Performance

| Metric | Value |
|--------|-------|
| Auto-Fix Attempts | {{AUTOFIX_ATTEMPTS}} |
| Successful Auto-Fixes | {{AUTOFIX_SUCCESSES}} |
| Failed Auto-Fixes | {{AUTOFIX_FAILURES}} |
| **Success Rate** | **{{AUTOFIX_SUCCESS}}%** |

---

## 3. Cost Metrics

### Session Cost Summary

| Category | Tokens | Cost |
|----------|--------|------|
| Input Tokens | {{INPUT_TOKENS}} | ${{INPUT_COST}} |
| Output Tokens | {{OUTPUT_TOKENS}} | ${{OUTPUT_COST}} |
| Cache Write | {{CACHE_WRITE_TOKENS}} | ${{CACHE_WRITE_COST}} |
| Cache Read | {{CACHE_READ_TOKENS}} | ${{CACHE_READ_COST}} |
| **Total** | **{{TOTAL_TOKENS}}** | **${{TOTAL_COST}}** |

### Cost by Phase

| Phase | Model | Input | Output | Cache | Total |
|-------|-------|-------|--------|-------|-------|
| Constitution | {{CONST_MODEL}} | ${{CONST_INPUT}} | ${{CONST_OUTPUT}} | ${{CONST_CACHE}} | ${{CONST_TOTAL}} |
| Specify | {{SPEC_MODEL}} | ${{SPEC_INPUT}} | ${{SPEC_OUTPUT}} | ${{SPEC_CACHE}} | ${{SPEC_TOTAL}} |
| Plan | {{PLAN_MODEL}} | ${{PLAN_INPUT}} | ${{PLAN_OUTPUT}} | ${{PLAN_CACHE}} | ${{PLAN_TOTAL}} |
| Tasks | {{TASKS_MODEL}} | ${{TASKS_INPUT}} | ${{TASKS_OUTPUT}} | ${{TASKS_CACHE}} | ${{TASKS_TOTAL}} |
| Implement | {{IMPL_MODEL}} | ${{IMPL_INPUT}} | ${{IMPL_OUTPUT}} | ${{IMPL_CACHE}} | ${{IMPL_TOTAL}} |
| **Total** | - | **${{TOTAL_INPUT}}** | **${{TOTAL_OUTPUT}}** | **${{TOTAL_CACHE}}** | **${{TOTAL_COST}}** |

### Cost vs Target

| Metric | Value | Target | Variance |
|--------|-------|--------|----------|
| Implement Phase | ${{IMPL_TOTAL}} | $22.00 | {{IMPL_VARIANCE}} |
| Full Workflow | ${{TOTAL_COST}} | $37.00 | {{TOTAL_VARIANCE}} |
| **Optimized Target** | ${{TOTAL_COST}} | $25.00 | {{OPTIMIZED_VARIANCE}} |

### Model Efficiency

| Model | Tokens Used | Cost | Efficiency |
|-------|-------------|------|------------|
| Opus | {{OPUS_TOKENS}} | ${{OPUS_COST}} | {{OPUS_EFFICIENCY}} |
| Sonnet | {{SONNET_TOKENS}} | ${{SONNET_COST}} | {{SONNET_EFFICIENCY}} |
| Haiku | {{HAIKU_TOKENS}} | ${{HAIKU_COST}} | {{HAIKU_EFFICIENCY}} |

---

## 4. Quality Gates Summary

| Gate | Condition | Value | Result |
|------|-----------|-------|--------|
| Pre-Implementation | SQS >= 80 | {{SQS}} | {{PRE_IMPL_GATE}} |
| Post-Implementation | Human Intervention < 50% | {{HUMAN_INTERVENTION}}% | {{POST_IMPL_GATE}} |
| Cost Alert | Phase cost < 150% estimate | {{COST_VS_TARGET}}% | {{COST_GATE}} |

**Gates Passed**: {{GATES_PASSED}}/3

---

## 5. Recommendations

### High Priority
{{#if HIGH_PRIORITY_RECS}}
{{HIGH_PRIORITY_RECS}}
{{else}}
- No high priority recommendations
{{/if}}

### Medium Priority
{{#if MEDIUM_PRIORITY_RECS}}
{{MEDIUM_PRIORITY_RECS}}
{{else}}
- No medium priority recommendations
{{/if}}

### Optimization Opportunities
{{#if OPTIMIZATION_RECS}}
{{OPTIMIZATION_RECS}}
{{else}}
- No optimization recommendations at this time
{{/if}}

---

## 6. Trend Data (Optional)

If tracking metrics across sessions:

### SQS Trend

| Session | Date | SQS | Delta |
|---------|------|-----|-------|
| Current | {{DATE}} | {{SQS}} | - |
| Previous | {{PREV_DATE}} | {{PREV_SQS}} | {{SQS_DELTA}} |

### Cost Trend

| Session | Date | Cost | Delta |
|---------|------|------|-------|
| Current | {{DATE}} | ${{TOTAL_COST}} | - |
| Previous | {{PREV_DATE}} | ${{PREV_COST}} | {{COST_TREND_DELTA}} |

---

## Appendix: Metric Definitions

### SQS Components

| Component | Definition | Calculation |
|-----------|------------|-------------|
| FR Coverage | % of Functional Requirements with mapped tasks | (FRs with tasks / Total FRs) × 100 |
| AS Coverage | % of Acceptance Scenarios with tests | (AS with tests / Total AS) × 100 |
| Traceability | % of code files with @speckit annotations | (Annotated files / Total files) × 100 |
| Constitution Compliance | % of principles without violations | (Satisfied / Total checked) × 100 |

### Velocity Metrics

| Metric | Definition | Measurement Point |
|--------|------------|-------------------|
| Time to First Working Code | Duration from /speckit.implement start to first passing test | First `✅ Test passed` event |
| Time to MVP | Duration from /speckit.specify start to Wave 1 completion | All Wave 1 tasks complete |
| Human Intervention Rate | % of tasks requiring manual edits | (Tasks with edits / Total tasks) × 100 |
| Auto-Fix Success Rate | % of build/test errors auto-fixed | (Successful fixes / Fix attempts) × 100 |

### Cost Metrics

| Token Type | Opus Rate | Sonnet Rate | Haiku Rate |
|------------|-----------|-------------|------------|
| Input | $0.015/1K | $0.003/1K | $0.00025/1K |
| Output | $0.075/1K | $0.015/1K | $0.00125/1K |
| Cache Write | $0.01875/1K | $0.00375/1K | $0.0003/1K |
| Cache Read | $0.0015/1K | $0.0003/1K | $0.000025/1K |

---

**Report Generated By**: Spec-Driven Development Metrics Framework v1.0
**Reference**: See `templates/shared/metrics-framework.md` for full documentation
