# Self-Review Framework

## Purpose

Unified self-review system for all Spec Kit commands. Provides consistent quality checks, verdict logic, and reporting across specification, planning, and task generation phases.

## Why This Matters

| Without Self-Review | With Self-Review |
|---------------------|------------------|
| Quality issues found in later phases | Issues caught at source |
| Inconsistent artifact quality | Consistent quality gates |
| Manual review burden | Automated first-pass review |
| No iteration tracking | Up to 3 auto-fix attempts |

## Self-Review Lifecycle

```text
GENERATE_ARTIFACT → SELF_REVIEW → [FIX_ISSUES] → SELF_REVIEW → ... → VERDICT
                         ↓              ↑
                    (max 3 iterations)
```

## Framework Structure

### Severity Levels

```text
SEVERITY_LEVELS = {
  CRITICAL: {
    weight: 10,
    auto_fail: true,
    description: "Blocks artifact completion. Must be fixed."
  },
  HIGH: {
    weight: 5,
    auto_fail: false,
    warn_threshold: 2,  # 2+ HIGH issues = WARN
    description: "Significant quality issue. Should be fixed."
  },
  MEDIUM: {
    weight: 2,
    auto_fail: false,
    warn_threshold: 4,  # 4+ MEDIUM issues = WARN
    description: "Quality improvement. Fix if possible."
  },
  LOW: {
    weight: 1,
    auto_fail: false,
    description: "Nice to have. Optional fix."
  }
}
```

### Verdict Logic

```text
CALCULATE_VERDICT(check_results):

  critical_fails = count(results WHERE severity = CRITICAL AND status = FAIL)
  high_fails = count(results WHERE severity = HIGH AND status = FAIL)
  medium_fails = count(results WHERE severity = MEDIUM AND status = FAIL)
  low_fails = count(results WHERE severity = LOW AND status = FAIL)

  # Calculate quality score (0-100)
  total_weight = sum(SEVERITY_LEVELS[r.severity].weight FOR r IN results)
  failed_weight = sum(SEVERITY_LEVELS[r.severity].weight FOR r IN results WHERE status = FAIL)
  QUALITY_SCORE = round(100 * (1 - failed_weight / total_weight))

  # Determine verdict
  IF critical_fails > 0:
    VERDICT = "FAIL"
    VERDICT_REASON = "CRITICAL issues must be resolved"

  ELIF high_fails >= 2:
    VERDICT = "WARN"
    VERDICT_REASON = "{high_fails} HIGH severity issues detected"

  ELIF medium_fails >= 4:
    VERDICT = "WARN"
    VERDICT_REASON = "{medium_fails} MEDIUM severity issues detected"

  ELIF QUALITY_SCORE >= 80:
    VERDICT = "PASS"
    VERDICT_REASON = "Quality score {QUALITY_SCORE}% meets threshold"

  ELSE:
    VERDICT = "WARN"
    VERDICT_REASON = "Quality score {QUALITY_SCORE}% below 80% threshold"

  RETURN {verdict: VERDICT, reason: VERDICT_REASON, score: QUALITY_SCORE}
```

### Iteration Logic

```text
MAX_ITERATIONS = 3

FOR iteration IN 1..MAX_ITERATIONS:

  # Run all checks
  check_results = RUN_CHECKS(artifact, criteria)

  # Calculate verdict
  verdict_result = CALCULATE_VERDICT(check_results)

  IF verdict_result.verdict == "PASS":
    OUTPUT: "✅ Self-Review PASSED (iteration {iteration}/{MAX_ITERATIONS})"
    OUTPUT: "Quality Score: {verdict_result.score}%"
    BREAK

  ELIF iteration < MAX_ITERATIONS:
    # Attempt auto-fix
    fixable_issues = filter(check_results, status = FAIL AND auto_fixable = true)
    OUTPUT: "🔧 Attempting auto-fix for {len(fixable_issues)} issues..."

    FOR issue IN fixable_issues:
      APPLY_FIX(artifact, issue)

    OUTPUT: "Self-Review Iteration {iteration+1}/{MAX_ITERATIONS}..."

  ELSE:
    # Max iterations reached
    IF verdict_result.verdict == "FAIL":
      OUTPUT: "❌ Self-Review FAILED after {MAX_ITERATIONS} iterations"
      OUTPUT: "Unresolved CRITICAL issues:"
      FOR issue IN filter(check_results, severity = CRITICAL AND status = FAIL):
        OUTPUT: "  - {issue.id}: {issue.description}"
      ASK_USER: "Proceed anyway? (Not recommended)"

    ELSE:  # WARN
      OUTPUT: "⚠️ Self-Review completed with warnings"
      OUTPUT: "Quality Score: {verdict_result.score}%"
      OUTPUT: "Unresolved issues:"
      FOR issue IN filter(check_results, status = FAIL):
        OUTPUT: "  - {issue.id} [{issue.severity}]: {issue.description}"
```

## Check Definition Format

Each command defines its checks using this format:

```text
CHECK_DEFINITION = {
  id: "SR-{CMD}-{NN}",        # e.g., SR-SPEC-01, SR-PLAN-05
  name: "Check Name",
  description: "What this check validates",
  severity: CRITICAL | HIGH | MEDIUM | LOW,
  auto_fixable: true | false,
  check_fn: FUNCTION(artifact) → {status: PASS|FAIL, details: string},
  fix_fn: FUNCTION(artifact, issue) → artifact  # Only if auto_fixable
}
```

## Command-Specific Criteria

### Criteria for specify.md (SR-SPEC-01 to SR-SPEC-10)

See `templates/shared/self-review/criteria-spec.md`

### Criteria for plan.md (SR-PLAN-01 to SR-PLAN-10)

See `templates/shared/self-review/criteria-plan.md`

### Criteria for tasks.md (SR-TASK-01 to SR-TASK-10)

See `templates/shared/self-review/criteria-tasks.md`

### Criteria for concept.md (SR-CONC-01 to SR-CONC-10)

| ID | Name | Description | Severity |
|----|------|-------------|----------|
| SR-CONC-01 | CQS Score Met | Concept Quality Score >= 60 (or 80 for COMPLEX) | CRITICAL |
| SR-CONC-02 | Vision Defined | Vision Statement section complete | HIGH |
| SR-CONC-03 | Golden Path Complete | Golden Path has all 5 phases | HIGH |
| SR-CONC-04 | Personas Defined | At least 2 personas with JTBD | MEDIUM |
| SR-CONC-05 | Metrics Defined | Success metrics with baselines | MEDIUM |
| SR-CONC-06 | Feature Hierarchy | At least one EPIC with features | HIGH |
| SR-CONC-07 | Waves Assigned | All features assigned to waves | MEDIUM |
| SR-CONC-08 | Risks Identified | At least 3 risks in matrix | MEDIUM |
| SR-CONC-09 | No Placeholders | No TODO, TBD, FIXME markers | HIGH |
| SR-CONC-10 | Traceability Skeleton | Skeleton has spec/plan/tasks placeholders | LOW |

## Adaptive Criteria by Complexity

Based on `templates/shared/complexity-scoring.md` tier:

| Tier | Active Criteria | CQS Requirement |
|------|-----------------|-----------------|
| TRIVIAL | SR-*-01, 02, 03 only | Not applicable |
| SIMPLE | SR-*-01 to 06 | Not applicable |
| MODERATE | SR-*-01 to 10 | CQS >= 60 |
| COMPLEX | SR-*-01 to 10 + concept alignment | CQS >= 80 |

## Self-Review Report Template

```markdown
## Self-Review Report

**Artifact**: {artifact_name}
**Iteration**: {current}/{max}
**Quality Score**: {score}%
**Verdict**: {PASS | WARN | FAIL}

### Check Results

| ID | Name | Status | Details |
|----|------|--------|---------|
| {id} | {name} | ✅ PASS / ⚠️ WARN / ❌ FAIL | {details} |

### Unresolved Issues

{IF any issues with status = FAIL}
| ID | Severity | Issue | Suggested Fix |
|----|----------|-------|---------------|
| {id} | {severity} | {description} | {suggestion} |
{ELSE}
No unresolved issues.
{END}

### Quality Trend

{IF iteration > 1}
- Iteration 1: {score_1}% → Iteration 2: {score_2}%
- Fixed: {fixed_count} issues
- Remaining: {remaining_count} issues
{END}
```

## Usage in Commands

Add to command's final phase:

```markdown
## Self-Review Phase (MANDATORY)

Read `templates/shared/self-review/framework.md` and apply with:
- CRITERIA_FILE = "templates/shared/self-review/criteria-{command}.md"
- COMPLEXITY_TIER = from complexity-scoring.md

Execute self-review loop:
1. Run all applicable criteria checks
2. Calculate verdict
3. If FAIL and iteration < 3: attempt auto-fix and retry
4. Generate Self-Review Report
5. If final verdict = FAIL: ask user to proceed or abort
```

## Integration with Validation Checkpoints

Self-review can be combined with streaming validation checkpoints:

```text
STREAMING_MODE:
  - Run subset of checks after each major section
  - Early fail on CRITICAL issues
  - Full self-review at end catches cross-section issues

CHECKPOINT_CHECKS:
  after_user_stories: [SR-SPEC-08]
  after_requirements: [SR-SPEC-01, SR-SPEC-02]
  after_scenarios: [SR-SPEC-03, SR-SPEC-04]
  final: [ALL]
```

See `templates/shared/validation/checkpoints.md` for checkpoint definitions.
