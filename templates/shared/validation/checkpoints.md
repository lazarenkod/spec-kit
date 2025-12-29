# Validation Checkpoints

## Purpose

Enable streaming validation during artifact generation. Instead of waiting until the end to validate, checkpoints catch issues early, reducing wasted effort and enabling faster feedback loops.

## Why This Matters

| Traditional Validation | Streaming Validation |
|------------------------|---------------------|
| All validation at end | Checks at each section |
| Late discovery of issues | Early failure on CRITICAL |
| Full regeneration needed | Targeted section fixes |
| Slower feedback | Faster iteration |

## Checkpoint Architecture

```text
┌──────────────────────────────────────────────────────────┐
│                    ARTIFACT GENERATION                    │
├──────────────┬──────────────┬──────────────┬─────────────┤
│  Section 1   │  Section 2   │  Section 3   │  Section N  │
│              │              │              │             │
│  ▼ Checkpoint│  ▼ Checkpoint│  ▼ Checkpoint│  ▼ Final    │
│     CP-01    │     CP-02    │     CP-03    │   Review    │
└──────────────┴──────────────┴──────────────┴─────────────┘

CRITICAL failure at any checkpoint → EARLY STOP
HIGH/MEDIUM issues → LOG and CONTINUE
Final Review → FULL SELF-REVIEW
```

## Checkpoint Definition Format

```text
CHECKPOINT = {
  id: "CP-{CMD}-{NN}",        # e.g., CP-SPEC-01
  trigger: "after_{section}", # When to run
  checks: [SR-xxx-yy, ...],   # Which criteria to check
  early_fail: true | false,   # Stop generation on failure
  parallel: true | false      # Run checks in parallel
}
```

## Command-Specific Checkpoints

### specify.md Checkpoints

```text
CP-SPEC-01: After User Stories
  trigger: after_user_stories
  checks: [SR-SPEC-08]  # Stories have acceptance scenarios?
  early_fail: false
  validation: "Checking user story completeness..."

CP-SPEC-02: After Requirements
  trigger: after_requirements
  checks: [SR-SPEC-01, SR-SPEC-02]  # Sections filled? No impl details?
  early_fail: true  # CRITICAL if impl details found
  validation: "Checking requirement quality..."

CP-SPEC-03: After Scenarios
  trigger: after_scenarios
  checks: [SR-SPEC-03, SR-SPEC-04]  # FR→AS links? AS format?
  early_fail: false
  validation: "Checking scenario coverage..."

CP-SPEC-04: After Success Criteria
  trigger: after_success_criteria
  checks: [SR-SPEC-06, SR-SPEC-07]  # Measurable? Tech-agnostic?
  early_fail: false
  validation: "Checking success criteria quality..."

CP-SPEC-05: Final
  trigger: end_of_generation
  checks: [ALL]  # Full self-review
  early_fail: true
  validation: "Running full self-review..."
```

### plan.md Checkpoints

```text
CP-PLAN-01: After Tech Context
  trigger: after_tech_context
  checks: [SR-PLAN-01]  # Technical context complete?
  early_fail: false
  validation: "Checking technical context..."

CP-PLAN-02: After Dependencies
  trigger: after_dependencies
  checks: [SR-PLAN-03, SR-PLAN-04]  # Dependencies listed? Verified?
  early_fail: false
  validation: "Verifying dependencies..."

CP-PLAN-03: After Architecture
  trigger: after_architecture
  checks: [SR-PLAN-08]  # Architecture defined?
  early_fail: false
  validation: "Checking architecture decisions..."

CP-PLAN-04: After Constitution Check
  trigger: after_constitution_check
  checks: [SR-PLAN-07]  # Constitution checked?
  early_fail: false
  validation: "Verifying constitution alignment..."

CP-PLAN-05: Final
  trigger: end_of_generation
  checks: [ALL]
  early_fail: true
  validation: "Running full self-review..."
```

### tasks.md Checkpoints

```text
CP-TASK-01: After Task List
  trigger: after_task_list
  checks: [SR-TASK-01, SR-TASK-02]  # Format valid? IDs sequential?
  early_fail: true  # Invalid format is CRITICAL
  validation: "Checking task format..."

CP-TASK-02: After Dependencies
  trigger: after_dependencies
  checks: [SR-TASK-07, SR-TASK-08]  # DEP refs valid? No cycles?
  early_fail: true  # Circular deps is CRITICAL
  validation: "Validating dependency graph..."

CP-TASK-03: After Coverage
  trigger: after_coverage
  checks: [SR-TASK-05, SR-TASK-06]  # FR coverage? AS coverage?
  early_fail: false
  validation: "Checking requirement coverage..."

CP-TASK-04: Final
  trigger: end_of_generation
  checks: [ALL]
  early_fail: true
  validation: "Running full self-review..."
```

## Checkpoint Execution Algorithm

```text
EXECUTE_CHECKPOINT(checkpoint, artifact_state):

  OUTPUT: "📋 {checkpoint.validation}"

  # Run checks (parallel if enabled)
  IF checkpoint.parallel:
    results = PARALLEL_RUN(checkpoint.checks, artifact_state)
  ELSE:
    results = SEQUENTIAL_RUN(checkpoint.checks, artifact_state)

  # Collect failures
  failures = filter(results, status = FAIL)
  critical_failures = filter(failures, severity = CRITICAL)

  # Report results
  IF len(failures) == 0:
    OUTPUT: "  ✅ Checkpoint passed"
    RETURN {status: PASS, continue: true}

  ELIF checkpoint.early_fail AND len(critical_failures) > 0:
    OUTPUT: "  ❌ CRITICAL failure - stopping generation"
    FOR failure IN critical_failures:
      OUTPUT: "     - {failure.id}: {failure.description}"

    ASK_USER: "Fix issues and retry, or abort?"
    IF user_chooses_abort:
      RETURN {status: FAIL, continue: false}
    ELSE:
      # User wants to fix
      RETURN {status: FAIL, continue: false, retry: true}

  ELSE:
    OUTPUT: "  ⚠️ {len(failures)} issues found (continuing)"
    FOR failure IN failures:
      OUTPUT: "     - {failure.id} [{failure.severity}]: {failure.description}"

    # Log for final review
    APPEND_TO_ISSUE_LOG(failures)

    RETURN {status: WARN, continue: true}
```

## Parallel Validation

For performance, independent checks can run in parallel:

```text
PARALLEL_GROUPS:

  specify.md:
    group_1: [SR-SPEC-01, SR-SPEC-02]  # Section checks
    group_2: [SR-SPEC-03, SR-SPEC-04]  # Scenario checks
    sequential: [SR-SPEC-05]           # Cross-reference check

  plan.md:
    group_1: [SR-PLAN-01, SR-PLAN-03]  # Content checks
    group_2: [SR-PLAN-04, SR-PLAN-05]  # Dependency checks
    sequential: [SR-PLAN-07]           # Constitution check

  tasks.md:
    group_1: [SR-TASK-01, SR-TASK-02]  # Format checks
    group_2: [SR-TASK-05, SR-TASK-06]  # Coverage checks
    sequential: [SR-TASK-07, SR-TASK-08]  # Dependency graph (must be sequential)
```

## Issue Logging

All checkpoint issues are logged for the final self-review:

```text
ISSUE_LOG = {
  checkpoint_issues: [
    {checkpoint: "CP-SPEC-02", id: "SR-SPEC-02", issue: "Found 'PostgreSQL' in FR-003"},
    {checkpoint: "CP-SPEC-03", id: "SR-SPEC-03", issue: "FR-005 has no linked AS"}
  ],
  first_seen_at: "CP-SPEC-02",
  still_unresolved: true
}
```

## Checkpoint Report Format

```markdown
## Checkpoint Summary

| Checkpoint | Status | Issues | Action |
|------------|--------|--------|--------|
| CP-SPEC-01 | ✅ PASS | 0 | Continued |
| CP-SPEC-02 | ⚠️ WARN | 1 | Logged for review |
| CP-SPEC-03 | ✅ PASS | 0 | Continued |
| CP-SPEC-04 | ✅ PASS | 0 | Continued |
| CP-SPEC-05 | ⚠️ WARN | 2 | Self-review triggered |

**Early Stops**: 0
**Total Issues Logged**: 3
**Final Verdict**: See Self-Review Report
```

## Integration with Complexity Tiers

Checkpoint behavior adapts to complexity:

| Tier | Checkpoints Active | Early Fail Behavior |
|------|-------------------|---------------------|
| TRIVIAL | CP-*-01, CP-*-Final only | Only CRITICAL |
| SIMPLE | All checkpoints | Only CRITICAL |
| MODERATE | All + extra validation | CRITICAL + 3+ HIGH |
| COMPLEX | All + concept validation | CRITICAL + 2+ HIGH |

## Usage in Commands

Add checkpoint calls during generation:

```markdown
## Step N: Generate User Stories

... generate user stories ...

### Checkpoint: User Stories
Read `templates/shared/validation/checkpoints.md` and execute:
- CHECKPOINT = CP-SPEC-01
- ARTIFACT_STATE = current spec.md content

IF checkpoint.status = FAIL AND checkpoint.retry:
  FIX_ISSUES and RETRY from Step N
ELIF checkpoint.status = FAIL:
  ABORT generation
```

## Performance Optimization

```text
CHECKPOINT_CACHING:
  # Cache check results for unchanged sections
  cache_key = section_content_hash
  IF cache_key in CHECKPOINT_CACHE:
    RETURN CHECKPOINT_CACHE[cache_key]
  ELSE:
    result = RUN_CHECK(...)
    CHECKPOINT_CACHE[cache_key] = result
    RETURN result

EXPECTED_PERFORMANCE:
  Without checkpoints: 105s total validation at end
  With checkpoints: 70s distributed + 20s final = 90s total
  Net savings: ~15% faster with better UX (early feedback)
```
