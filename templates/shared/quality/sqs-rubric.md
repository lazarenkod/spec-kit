# SQS (Specification Quality Score) Rubric v2.0

> **Formal definition of the 25-checkpoint specification quality scoring system**

---

## Overview

The Specification Quality Score (SQS) measures specification readiness for implementation across 5 dimensions with 25 individual checkpoints. This rubric ensures specifications meet world-class standards before development begins.

**Formula**: `SQS = Clarity + Completeness + Testability + Traceability + NoAmbiguity`

**Maximum Score**: 100 points

---

## Thresholds

| Score Range | Status | Action Required |
|-------------|--------|-----------------|
| **≥80** | Ready for Implementation | Proceed to `/speckit.plan` |
| **60-79** | Needs Improvement | Run `/speckit.clarify` to address gaps |
| **<60** | Major Rework Required | Block implementation, significant spec revision needed |

---

## Dimension 1: Clarity (25 points)

*Measures how precisely and unambiguously requirements are stated*

| ID | Checkpoint | Points | Scoring Guidance |
|----|------------|--------|------------------|
| CL-01 | **RFC 2119 Keywords Used** | 5 | SHALL/SHOULD/MAY consistently applied to all requirements |
| CL-02 | **No Vague Terms** | 5 | Zero instances of "fast", "easy", "user-friendly", "robust", "scalable" without quantification |
| CL-03 | **Specific Numbers** | 5 | All quantities, limits, thresholds explicitly defined (e.g., "10 items", "<200ms") |
| CL-04 | **Measurable Success** | 5 | Success criteria quantified with specific metrics and targets |
| CL-05 | **Defined Failures** | 5 | Failure scenarios explicitly listed with expected system behavior |

### Scoring Scale (per checkpoint)
- **5 points**: Fully compliant, no issues
- **4 points**: Minor issues (1-2 instances needing fix)
- **3 points**: Moderate issues (3-5 instances)
- **2 points**: Significant issues (6-10 instances)
- **1 point**: Major issues (>10 instances)
- **0 points**: Not addressed at all

### Anti-Patterns

| Bad | Good |
|-----|------|
| "System should be fast" | "API responds in <200ms p95" |
| "User-friendly interface" | "Task completion in ≤3 clicks" |
| "Handle large datasets" | "Process up to 1M records in <30s" |
| "Reasonable timeout" | "Timeout after 30 seconds with retry" |

---

## Dimension 2: Completeness (25 points)

*Measures coverage of all necessary specification aspects*

| ID | Checkpoint | Points | Scoring Guidance |
|----|------------|--------|------------------|
| CM-01 | **Functional Requirements Documented** | 5 | All user-facing functionality has corresponding FR-XXX entries |
| CM-02 | **Non-Functional Requirements Specified** | 5 | ≥3 NFRs with NFR-xxx IDs (MUST include: NFR-PERF-*, NFR-SEC-*, NFR-REL-*) |
| CM-03 | **Edge Cases Listed** | 5 | Boundary conditions, empty states, maximum limits addressed |
| CM-04 | **Dependencies Mapped** | 5 | External services, libraries, APIs explicitly listed with versions |
| CM-05 | **Security Covered** | 5 | Authentication, authorization, data protection requirements specified |

### Scoring Scale (per checkpoint)
- **5 points**: 100% coverage
- **4 points**: 80-99% coverage
- **3 points**: 60-79% coverage
- **2 points**: 40-59% coverage
- **1 point**: 20-39% coverage
- **0 points**: <20% coverage

### Completeness Indicators

| Indicator | Expected |
|-----------|----------|
| FR count | ≥5 for non-trivial features |
| NFR count | ≥3 mandatory (NFR-PERF-*, NFR-SEC-*, NFR-REL-*) + optional categories |
| Edge cases | ≥3 per major flow |
| Dependencies | All external systems listed |

---

## Dimension 3: Testability (25 points)

*Measures whether requirements can be objectively verified*

| ID | Checkpoint | Points | Scoring Guidance |
|----|------------|--------|------------------|
| TS-01 | **Each FR Has Acceptance Criteria** | 5 | Every FR-XXX has at least one AS-XXX scenario |
| TS-02 | **Scenarios Concrete** | 5 | Given/When/Then format with specific values, not placeholders |
| TS-03 | **Performance Metrics Defined** | 5 | Response times, throughput, resource limits specified |
| TS-04 | **Error Conditions Covered** | 5 | All error scenarios have expected behavior defined |
| TS-05 | **Integration Points Specified** | 5 | API contracts, data formats, protocols documented |

### Scoring Scale (per checkpoint)
- **5 points**: All items testable with clear pass/fail criteria
- **4 points**: 90%+ items testable
- **3 points**: 70-89% items testable
- **2 points**: 50-69% items testable
- **1 point**: 30-49% items testable
- **0 points**: <30% items testable

### Testability Examples

| Untestable | Testable |
|------------|----------|
| "System validates input" | "System rejects email without @ symbol with error E-001" |
| "Handles concurrent users" | "Supports 100 concurrent users with <500ms p99 latency" |
| "Secure data transmission" | "All API calls use TLS 1.3, reject TLS <1.2" |

---

## Dimension 4: Traceability (15 points)

*Measures linkage between requirements, acceptance criteria, and implementation*

| ID | Checkpoint | Points | Scoring Guidance |
|----|------------|--------|------------------|
| TR-01 | **Unique IDs Assigned** | 3 | Every FR, NFR, AS has unique identifier (FR-001, AS-001-01) |
| TR-02 | **Concept Cross-References** | 3 | Features link back to concept.md personas/goals/metrics |
| TR-03 | **Feature Dependencies** | 3 | Dependencies between features explicitly documented |
| TR-04 | **FR→AC→Test Chain** | 3 | Clear mapping: Requirement → Acceptance → Test case |
| TR-05 | **No Orphans** | 3 | Every requirement has implementation task, every AC has test |

### Scoring Scale (per checkpoint)
- **3 points**: 100% compliant
- **2 points**: 80-99% compliant
- **1 point**: 50-79% compliant
- **0 points**: <50% compliant

### Traceability Matrix Example

```markdown
| FR ID | Description | AS IDs | Test IDs | Status |
|-------|-------------|--------|----------|--------|
| FR-001 | User login | AS-001-01, AS-001-02 | T-001, T-002 | Ready |
| FR-002 | Password reset | AS-002-01 | T-003 | Ready |
```

---

## Dimension 5: No Ambiguity (10 points)

*Measures elimination of interpretation variance*

| ID | Checkpoint | Points | Scoring Guidance |
|----|------------|--------|------------------|
| AM-01 | **No Hedge Words** | 2 | Zero "might", "could", "possibly", "maybe", "sometimes" |
| AM-02 | **Terms Defined** | 2 | Glossary includes all domain-specific terms |
| AM-03 | **Clarifications Resolved** | 2 | No `[NEEDS CLARIFICATION]` markers remaining |
| AM-04 | **Scope Explicit** | 2 | In-scope and out-of-scope clearly listed |
| AM-05 | **Assumptions Documented** | 2 | All assumptions explicitly stated |

### Scoring Scale (per checkpoint)
- **2 points**: Fully compliant
- **1 point**: Minor issues (1-2 items)
- **0 points**: Significant issues (3+ items)

### Ambiguity Triggers (Flag for Review)

| Pattern | Issue |
|---------|-------|
| "etc.", "and so on" | Incomplete enumeration |
| "as needed", "when appropriate" | Undefined trigger |
| "similar to", "like" | Vague reference |
| "best practices" | Unspecified standard |
| "reasonable", "adequate" | Subjective judgment |

---

## SQS Calculation Worksheet

```markdown
## SQS Score Calculation

### Clarity (max 25)
- [ ] CL-01 RFC 2119 Keywords: __/5
- [ ] CL-02 No Vague Terms: __/5
- [ ] CL-03 Specific Numbers: __/5
- [ ] CL-04 Measurable Success: __/5
- [ ] CL-05 Defined Failures: __/5
**Clarity Total**: __/25

### Completeness (max 25)
- [ ] CM-01 FRs Documented: __/5
- [ ] CM-02 NFRs Specified: __/5
- [ ] CM-03 Edge Cases: __/5
- [ ] CM-04 Dependencies: __/5
- [ ] CM-05 Security: __/5
**Completeness Total**: __/25

### Testability (max 25)
- [ ] TS-01 FRs Have ACs: __/5
- [ ] TS-02 Concrete Scenarios: __/5
- [ ] TS-03 Performance Metrics: __/5
- [ ] TS-04 Error Conditions: __/5
- [ ] TS-05 Integration Points: __/5
**Testability Total**: __/25

### Traceability (max 15)
- [ ] TR-01 Unique IDs: __/3
- [ ] TR-02 Concept Cross-refs: __/3
- [ ] TR-03 Feature Dependencies: __/3
- [ ] TR-04 FR→AC→Test Chain: __/3
- [ ] TR-05 No Orphans: __/3
**Traceability Total**: __/15

### No Ambiguity (max 10)
- [ ] AM-01 No Hedge Words: __/2
- [ ] AM-02 Terms Defined: __/2
- [ ] AM-03 Clarifications Resolved: __/2
- [ ] AM-04 Scope Explicit: __/2
- [ ] AM-05 Assumptions Documented: __/2
**No Ambiguity Total**: __/10

---

## TOTAL SQS: __/100

**Status**: [ ] Ready (≥80) | [ ] Needs Work (60-79) | [ ] Block (<60)
```

---

## Evidence Requirements

For P0/P1 features, evidence must support quantified requirements:

| Evidence Tier | Quality Level | Required For | Example |
|---------------|---------------|--------------|---------|
| **Tier 1** | Primary research, direct measurements | All P0 features | User testing data, APM metrics |
| **Tier 2** | Industry benchmarks, studies | All P1 features | Gartner reports, academic papers |
| **Tier 3** | Assumptions (MUST FLAG) | Needs validation before dev | Market estimates, extrapolations |

Requirements backed by Tier 3 evidence MUST include `[ASSUMPTION]` tag and validation plan.

---

## Integration

### With /speckit.specify
The specify command SHOULD generate specifications that score ≥80 SQS by default.

### With /speckit.clarify
Running clarify targets specific checkpoint failures:
- CL-* failures → Precision clarification questions
- CM-* failures → Completeness gap analysis
- TS-* failures → Testability enhancement
- TR-* failures → Traceability audit
- AM-* failures → Ambiguity resolution

### With /speckit.analyze
```bash
/speckit.analyze --profile sqs
```
Generates full SQS assessment with per-checkpoint scores.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v2.0 | 2026-01-03 | 25-checkpoint rubric, replaces 4-factor formula |
| v1.0 | 2025-XX-XX | Original 4-factor formula |

---

*SQS Rubric v2.0 | Part of Spec Kit Quality Framework*
