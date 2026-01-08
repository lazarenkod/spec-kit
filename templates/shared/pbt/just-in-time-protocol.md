# PBT Just-in-Time Protocol

This protocol defines how Property-Based Tests are executed incrementally during `/speckit.implement` to provide immediate feedback on implementation correctness.

## Overview

```
                    /speckit.properties
                           │
                           ▼
                    properties.md
                    (PROP-001..N)
                           │
                           ▼
                  /speckit.implement
                           │
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
    ▼                      ▼                      ▼
 TASK-001              TASK-002              TASK-003
    │                      │                      │
    ▼                      ▼                      ▼
 pbt-jit-runner        pbt-jit-runner        pbt-jit-runner
 (if maps to PROP)     (if maps to PROP)     (if maps to PROP)
    │                      │                      │
    ├─ PASS → continue     ├─ PASS → continue     ├─ FAIL
    └─ FAIL → auto-fix     └─ FAIL → auto-fix     │
                                                  ▼
                                            Auto-Fix Loop
                                            (max 3 attempts)
                                                  │
                                            ┌─────┴─────┐
                                            │           │
                                         SUCCESS     BLOCK
                                            │           │
                                            ▼           ▼
                                         continue   report to user
```

## Task-to-Property Mapping

### Traceability Chain

```
PROP-xxx ──traces-to──► FR-xxx / AS-xxx
                              │
                              ▼
TASK-xxx ──implements──► FR-xxx / AS-xxx
```

Properties in `properties.md` trace to specification requirements (FR-xxx) and acceptance scenarios (AS-xxx). Tasks in `tasks.md` implement those same requirements. The JIT runner uses this traceability to determine which properties to validate after each task.

### Mapping Algorithm

```yaml
for each completed_task in tasks.md:
  task_implements = extract_traceability(task)  # e.g., [FR-001, AS-1A, AS-1B]

  for each property in properties.md:
    prop_sources = property.source_artifacts  # e.g., [FR-001, AS-1A]

    if intersection(task_implements, prop_sources) is not empty:
      add_to_validation_queue(property, completed_task)
```

### Example

```markdown
# tasks.md
## TASK-005: Implement user authentication flow
- Implements: FR-001, AS-1A, AS-1B
- Status: completed

# properties.md
## PROP-001: Password Strength Invariant
- Source Artifacts: FR-001, AS-1A
- Property: password_strength(password) >= MIN_STRENGTH

→ After TASK-005 completes, run PROP-001
```

## Execution Commands

### Per-Language Test Commands

```yaml
python:
  single_prop: pytest tests/properties/ -k "prop_NNN" -v --hypothesis-show-statistics
  all_props: pytest tests/properties/ -v --hypothesis-show-statistics

typescript:
  single_prop: npm test -- --testPathPattern=property --testNamePattern="PROP-NNN"
  all_props: npm run test:properties

go:
  single_prop: go test -v -run TestPropNNN ./...
  all_props: go test -v -run TestProperty ./... -rapid.checks=100

java:
  single_prop: mvn test -Dtest=*PropertyTest#prop*NNN*
  all_props: mvn test -Dtest=*Property* -Djqwik.reporting.onlyFailures=false

kotlin:
  single_prop: gradle test --tests '*PropertyTest.prop*NNN*'
  all_props: gradle test --tests '*Property*' --info
```

### Test File Conventions

| Language | Test File Pattern | Property Function Pattern |
|----------|-------------------|---------------------------|
| Python | `tests/properties/test_*_properties.py` | `def test_prop_NNN_*` |
| TypeScript | `tests/property/*.property.test.ts` | `it('PROP-NNN: ...')` |
| Go | `*_property_test.go` | `func TestPropNNN*` |
| Java | `*PropertyTest.java` | `@Property void propNNN*` |
| Kotlin | `*PropertyTest.kt` | `@Property fun propNNN*` |

## Auto-Fix Loop

### Loop Structure

```
attempt = 0
max_attempts = 3

WHILE test_fails AND attempt < max_attempts:
    1. Run property test
    2. IF test passes:
         break (success)
    3. Capture shrunk counterexample
    4. Analyze failure type
    5. Apply fix strategy based on type
    6. Increment attempt

IF attempt >= max_attempts AND still_failing:
    block_task_completion()
    report_to_user()
```

### Failure Type Classification

| Type | Description | Action |
|------|-------------|--------|
| `IMPLEMENTATION_BUG` | Code logic error exposed by counterexample | Auto-fix implementation |
| `PROPERTY_TOO_STRICT` | Property over-constrained for requirements | Flag for `/speckit.clarify` |
| `GENERATOR_ISSUE` | Test generator produces invalid data | Skip (not impl problem) |
| `ENVIRONMENT_ERROR` | Database/service unavailable | Retry with backoff |

### Classification Heuristics

```yaml
IMPLEMENTATION_BUG:
  - Counterexample is valid input per spec
  - Code throws unexpected exception
  - Business invariant violated
  - Edge case not handled

PROPERTY_TOO_STRICT:
  - Counterexample is actually valid per requirements
  - Property asserts undocumented behavior
  - Spec ambiguity exposed

GENERATOR_ISSUE:
  - Generated data violates preconditions
  - Test setup fails before property check
  - Arbitrary instance invalid for domain

ENVIRONMENT_ERROR:
  - Connection refused/timeout
  - Service unhealthy
  - Docker container not running
```

## Auto-Fix Strategies

### Common Bug Patterns and Fixes

```yaml
off_by_one:
  detection: "boundary value fails, adjacent passes"
  fix_pattern: "Adjust boundary check: < to <=, > to >="

null_pointer:
  detection: "null/undefined in counterexample triggers crash"
  fix_pattern: "Add null check or use optional chaining"

type_coercion:
  detection: "string '0' or empty string causes issue"
  fix_pattern: "Use strict equality, explicit type conversion"

async_race:
  detection: "intermittent failures with same input"
  fix_pattern: "Add await, use mutex, reorder operations"

overflow:
  detection: "large numbers cause unexpected results"
  fix_pattern: "Use BigInt, add bounds checking"

encoding:
  detection: "Unicode characters cause failure"
  fix_pattern: "Use proper encoding, normalize strings"
```

### Fix Application Flow

```
1. Parse counterexample to extract failing input
2. Identify code path that processes this input
3. Detect bug pattern from error type + input
4. Generate fix code based on pattern
5. Apply fix using Edit tool
6. Re-run test to verify
```

## Metrics Collection

### JIT Metrics Output Format

```yaml
# After each JIT run
jit_validation:
  task: TASK-005
  properties_checked: [PROP-001, PROP-003]
  results:
    - property: PROP-001
      status: pass
      examples_tested: 100
    - property: PROP-003
      status: fixed
      attempts: 2
      fix_type: off_by_one
      shrunk_example: "age = -1"

# Aggregate metrics
pbt_jit_summary:
  total_tasks: 15
  tasks_with_pbt: 8
  properties_validated: 12
  auto_fixes_applied: 3
  shrunk_examples_captured: 5
  blocked_tasks: 0
```

## Block Conditions

The JIT runner blocks task completion when:

1. **Max attempts exceeded**: Property still fails after 3 fix attempts
2. **Critical invariant violated**: Business rule marked as `critical: true`
3. **Regression detected**: Previously passing property now fails
4. **Data corruption risk**: Counterexample shows data integrity issue

### Block Report Format

```markdown
## PBT JIT Block Report

**Task**: TASK-005 - Implement user authentication
**Property**: PROP-001 - Password Strength Invariant
**Status**: BLOCKED after 3 fix attempts

### Counterexample
```
password = ""  # Empty string
expected: strength >= 3
actual: strength = 0
```

### Fix Attempts
1. Added null check → Still fails
2. Added empty string check → Still fails
3. Added whitespace trim → Still fails

### Root Cause Analysis
Property expects minimum strength of 3, but implementation
allows empty passwords through. Spec ambiguity: FR-001 doesn't
explicitly require non-empty password.

### Recommended Actions
1. Run `/speckit.clarify` to resolve spec ambiguity
2. Update FR-001 with explicit password requirements
3. Re-generate property after clarification
```

## Integration with property-test-generator

The `pbt-jit-runner` runs incrementally during Wave 3 (Implementation). After all tasks complete, `property-test-generator` runs the final validation in Wave 4:

```
Wave 3: Implementation
  ├── TASK-001 → pbt-jit-runner (PROP-001)
  ├── TASK-002 → pbt-jit-runner (PROP-002)
  ├── TASK-003 → pbt-jit-runner (PROP-001, PROP-003)
  └── ...

Wave 4: Testing
  └── property-test-generator (ALL properties)
      ├── Catch cross-property interactions
      ├── Full shrinking statistics
      └── Final PQS calculation
```

## Skip Conditions

JIT mode is automatically disabled when:

- `properties.md` does not exist in `FEATURE_DIR`
- `--skip-pbt-jit` flag passed to implement
- Task has no traceability to any property
- Property test file does not exist yet

## Error Handling

### Graceful Degradation

```yaml
on_test_file_missing:
  action: "skip property, log warning"
  message: "PROP-xxx test not found - skipping JIT validation"

on_test_framework_error:
  action: "retry once, then skip"
  message: "Test framework error - continuing without PBT"

on_docker_unavailable:
  action: "skip properties requiring database"
  message: "Docker services unavailable - skipping DB properties"
```

### Recovery Strategies

```yaml
transient_failure:
  max_retries: 2
  backoff: exponential

persistent_failure:
  escalation: "block and report"
  preserve_context: true
```
