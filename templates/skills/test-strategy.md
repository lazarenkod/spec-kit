---
description: Generate comprehensive test strategy and test plan from specification
---

## User Input

```text
$ARGUMENTS
```

## Purpose

This skill generates a comprehensive test strategy and test plan from a feature specification. It identifies test scenarios, coverage requirements, and creates a structured testing approach aligned with the spec.

## When to Use

- After `/speckit.specify` to plan testing approach
- Before `/speckit.implement` to define acceptance criteria
- When QA needs formal test documentation
- For regulated environments requiring test traceability

## Execution Steps

### 1. Load Specification

Read the target specification:

```text
1. If argument provided: use that path
2. Otherwise: find most recent spec in specs/[feature]/spec.md
3. Parse:
   - Functional Requirements (FR-xxx)
   - Non-Functional Requirements (NFR-xxx)
   - Acceptance Scenarios (AS-xxx)
   - Error Scenarios (ERR-xxx)
   - Security Requirements (from constitution)
```

### 2. Analyze Testability

For each requirement, assess:

```text
Testability Checklist:
- [ ] Has clear acceptance criteria
- [ ] Has measurable success condition
- [ ] Has defined inputs and outputs
- [ ] Error cases specified
- [ ] Edge cases identifiable

IF requirement is not testable:
  → Flag with: "FR-xxx needs testable criteria"
  → Suggest: specific acceptance criteria format
```

### 3. Generate Test Categories

Map requirements to test types:

```markdown
## Test Category Mapping

| Requirement | Unit | Integration | E2E | Performance | Security |
|-------------|------|-------------|-----|-------------|----------|
| FR-001 | ✓ | ✓ | ✓ | - | - |
| FR-002 | ✓ | ✓ | - | - | ✓ |
| NFR-001 | - | - | - | ✓ | - |
| NFR-002 | - | - | - | - | ✓ |
```

### 4. Design Test Scenarios

For each requirement, generate scenarios:

```markdown
## Test Scenarios

### FR-001: [Requirement Name]

#### Happy Path
| ID | Scenario | Given | When | Then | Priority |
|----|----------|-------|------|------|----------|
| TS-001-01 | [Name] | [precondition] | [action] | [expected] | P1 |
| TS-001-02 | [Name] | [precondition] | [action] | [expected] | P1 |

#### Edge Cases
| ID | Scenario | Given | When | Then | Priority |
|----|----------|-------|------|------|----------|
| TS-001-E01 | [Edge case] | [precondition] | [action] | [expected] | P2 |

#### Error Cases
| ID | Scenario | Given | When | Then | Priority |
|----|----------|-------|------|------|----------|
| TS-001-ERR01 | [Error scenario] | [precondition] | [action] | [expected error] | P1 |
```

### 5. Coverage Analysis

Calculate coverage requirements:

```markdown
## Coverage Requirements

### Code Coverage Targets
| Type | Target | Rationale |
|------|--------|-----------|
| Line Coverage | 80% | Constitution QUA-001 |
| Branch Coverage | 75% | Critical path completeness |
| Function Coverage | 90% | API surface coverage |

### Requirement Coverage
| Category | Total | With Tests | Coverage |
|----------|-------|------------|----------|
| Functional (FR) | [N] | [N] | [%] |
| Non-Functional (NFR) | [N] | [N] | [%] |
| Acceptance (AS) | [N] | [N] | [%] |

### Risk-Based Coverage
| Risk Level | Requirements | Min Coverage |
|------------|--------------|--------------|
| High | FR-001, FR-003 | 95% |
| Medium | FR-002, FR-004 | 80% |
| Low | FR-005 | 60% |
```

### 6. Test Environment Requirements

Document environment needs:

```markdown
## Test Environment

### Dependencies
| Dependency | Test Strategy | Mock/Real |
|------------|---------------|-----------|
| Database | In-memory DB | Mock |
| External API | Stub server | Mock |
| Auth Service | Test tokens | Real (staging) |

### Test Data
| Data Set | Purpose | Generation Method |
|----------|---------|-------------------|
| Users | Auth tests | Fixture factory |
| [Entity] | CRUD tests | Builder pattern |

### Configuration
| Environment | Purpose | Key Differences |
|-------------|---------|-----------------|
| Unit | Isolated component tests | All external mocked |
| Integration | Service interaction | Real DB, mocked external |
| E2E | User flow validation | Staging environment |
```

### 7. Generate Test Plan Document

Create `specs/[feature]/test-plan.md`:

```markdown
# Test Plan: [Feature Name]

**Spec**: [spec.md path]
**Date**: [DATE]
**Author**: Claude Code (test-strategy skill)

## Overview

**Scope**: [What is being tested]
**Out of Scope**: [What is NOT being tested]
**Approach**: [Testing methodology]

## Test Summary

| Metric | Value |
|--------|-------|
| Total Test Scenarios | [N] |
| P1 (Critical) | [N] |
| P2 (Important) | [N] |
| P3 (Nice-to-have) | [N] |
| Estimated Effort | [X hours/days] |

## Requirement Traceability

| Requirement | Test Scenarios | Coverage Status |
|-------------|----------------|-----------------|
| FR-001 | TS-001-01, TS-001-02, TS-001-E01 | ✓ Complete |
| FR-002 | TS-002-01 | ⚠ Partial (missing edge cases) |

## Test Scenarios by Priority

### P1 - Must Pass for Release
[List critical scenarios]

### P2 - Should Pass
[List important scenarios]

### P3 - Nice to Have
[List optional scenarios]

## Test Data Requirements

[Data setup instructions]

## Environment Setup

[Environment configuration]

## Automation Recommendations

| Test Type | Framework | Files to Create |
|-----------|-----------|-----------------|
| Unit | [jest/pytest/etc] | [file patterns] |
| Integration | [supertest/etc] | [file patterns] |
| E2E | [playwright/cypress] | [file patterns] |

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk] | High/Med/Low | High/Med/Low | [Action] |

## Exit Criteria

- [ ] All P1 scenarios pass
- [ ] Code coverage ≥ [X]%
- [ ] No open critical bugs
- [ ] Performance within NFR limits
- [ ] Security scan clean
```

### 8. Generate Test Stubs (Optional)

If requested, generate test file stubs:

```text
IF user requests "--generate-stubs":
  FOR EACH test scenario:
    Generate test stub in appropriate format:
    - Jest/Vitest for JS/TS
    - pytest for Python
    - JUnit for Java/Kotlin

  Example output:
  - tests/unit/[feature].test.ts
  - tests/integration/[feature].integration.test.ts
  - tests/e2e/[feature].spec.ts
```

## Output

1. Test plan saved to `specs/[feature]/test-plan.md`
2. Summary of test scenarios by priority
3. Coverage gaps identified
4. Optional: test stub files generated

## Integration with Spec Kit

Feeds into:
- `/speckit.implement` → Developers know what tests to write
- `/speckit.analyze` QA mode → Validates test coverage
- QA Agent persona → Verification checklist

## Quick Mode

For rapid test scenario generation:

```text
/speckit.test-strategy --quick

Outputs:
- Test scenario list (Given/When/Then)
- Priority assignments
- Basic coverage check

Skips:
- Full test plan document
- Environment details
- Automation recommendations
```
