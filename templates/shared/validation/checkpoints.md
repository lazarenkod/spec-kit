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

---

## Progressive Validation

> **Purpose**: Replace blocking validation with a 4-tier pipeline for faster feedback and better UX. Saves 5-10s per command through early exits and non-blocking quality scoring.

### Why Progressive Validation?

| Traditional Validation | Progressive Validation |
|------------------------|------------------------|
| All checks run sequentially | Fast checks first, slow checks later |
| 20-30s blocking at end | 3-8s typical (early exit) |
| Pass/fail binary | Tiered: block → warn → score → async |
| No confidence tracking | 95% confidence skips expensive checks |

### 4-Tier Validation Model

```text
┌─────────────────────────────────────────────────────────────────┐
│                    PROGRESSIVE VALIDATION PIPELINE               │
├────────────────┬───────────────┬───────────────┬────────────────┤
│   TIER 1       │   TIER 2      │   TIER 3      │   TIER 4       │
│   SYNTAX       │   SEMANTIC    │   QUALITY     │   DEEP         │
│   < 1s         │   1-5s        │   5-15s       │   15-30s       │
│   BLOCKING     │   BLOCK ERR   │   NON-BLOCK   │   ASYNC        │
├────────────────┼───────────────┼───────────────┼────────────────┤
│ • MD syntax    │ • AC complete │ • SRS Score   │ • LLM review   │
│ • Section IDs  │ • Schema OK   │ • CQS Score   │ • Conflicts    │
│ • Format check │ • Refs valid  │ • Coverage    │ • Suggestions  │
├────────────────┼───────────────┼───────────────┼────────────────┤
│  ✓ PASS → T2   │  ✓ PASS → T3  │  🎯 Score →T4 │  🔄 Background │
│  ✗ FAIL → STOP │  ⚠ WARN → T3  │  (continue)   │  (results cb)  │
└────────────────┴───────────────┴───────────────┴────────────────┘
```

### Tier Classification

```yaml
TIER_1_SYNTAX:  # < 1s, BLOCKING
  - SR-SPEC-01: mandatory_sections_filled
  - SR-PLAN-01: tech_context_complete
  - SR-TASK-01: task_format_valid
  - SR-TASK-02: ids_sequential
  - ID_FORMAT: all IDs match pattern (FR-xxx, AS-xxx, SC-xxx, etc.)

TIER_2_SEMANTIC:  # 1-5s, BLOCKING on errors
  - SR-SPEC-02: no_implementation_details
  - SR-SPEC-03: fr_linked_to_as
  - SR-SPEC-04: as_given_when_then
  - SR-SPEC-08: stories_have_as
  - SR-PLAN-03: dependencies_listed
  - SR-PLAN-07: constitution_checked
  - SR-TASK-07: dep_refs_valid
  - SR-TASK-08: no_circular_deps
  - VG-004: constitution_alignment (CRITICAL)

TIER_3_QUALITY:  # 5-15s, NON-BLOCKING
  - VG-001: SRS_score (Specification Readiness)
  - VG-002: CQS_score (Concept Quality)
  - VG-005: ambiguity_count
  - VG-006: PRS_score (Plan Readiness)
  - VG-007: TRS_score (Task Readiness)
  - TRACEABILITY: coverage_percentage
  - SR-SLOP: anti_slop_checks

TIER_4_DEEP:  # 15-30s, ASYNC BACKGROUND
  - LLM_REVIEW: conflict_detection
  - CONSISTENCY: cross_artifact_analysis
  - SR-READ: reader_testing_checks
  - SUGGESTIONS: improvement_recommendations
```

### Progressive Validation Algorithm

```text
FUNCTION progressive_validate(artifact, artifact_type):

  # Initialize metrics
  start_time = timestamp()
  validation_result = {}

  # ─────────────────────────────────────────────
  # TIER 1: Syntax (< 1s, BLOCKING)
  # ─────────────────────────────────────────────
  tier_1 = run_tier_1_checks(artifact, artifact_type)

  IF tier_1.has_failures:
    OUTPUT "❌ Tier 1 Syntax: FAIL ({tier_1.duration}ms)"
    FOR failure IN tier_1.failures:
      OUTPUT "   • {failure.id}: {failure.message}"
    RETURN {status: "FAIL", tier: 1, issues: tier_1.failures}

  OUTPUT "✅ Tier 1 Syntax: PASS ({tier_1.duration}ms)"

  # ─────────────────────────────────────────────
  # TIER 2: Semantic (1-5s, BLOCKING on errors)
  # ─────────────────────────────────────────────
  tier_2 = run_tier_2_checks(artifact, artifact_type)

  IF tier_2.has_errors:  # CRITICAL or HIGH severity
    OUTPUT "❌ Tier 2 Semantic: FAIL ({tier_2.duration}ms)"
    FOR error IN tier_2.errors:
      OUTPUT "   • {error.id} [{error.severity}]: {error.message}"
    RETURN {status: "FAIL", tier: 2, issues: tier_2.errors}

  IF tier_2.has_warnings:
    OUTPUT "⚠️ Tier 2 Semantic: {tier_2.warning_count} warnings ({tier_2.duration}ms)"
    FOR warning IN tier_2.warnings:
      OUTPUT "   • {warning.id}: {warning.message}"
  ELSE:
    OUTPUT "✅ Tier 2 Semantic: PASS ({tier_2.duration}ms)"

  # ─────────────────────────────────────────────
  # EARLY EXIT CHECK
  # ─────────────────────────────────────────────
  confidence = calculate_pass_confidence(tier_1, tier_2, artifact_type)

  IF confidence >= 0.95:
    OUTPUT "🚀 High confidence ({confidence:.0%}) — skipping Tier 3-4"

    # Launch Tier 4 async but don't wait
    tier_4_task = launch_tier_4_async(artifact)

    elapsed = timestamp() - start_time
    OUTPUT "⏱️ Validation: {elapsed}ms (early exit saved ~20s)"

    RETURN {
      status: "PASS",
      tier: 2,
      confidence: confidence,
      skipped: [3, 4],
      async_task: tier_4_task
    }

  # ─────────────────────────────────────────────
  # TIER 3: Quality Scoring (5-15s, NON-BLOCKING)
  # ─────────────────────────────────────────────
  tier_3 = run_tier_3_checks(artifact, artifact_type)

  OUTPUT "🎯 Tier 3 Quality ({tier_3.duration}ms):"
  OUTPUT "   • SRS: {tier_3.srs}% (threshold: {tier_3.srs_threshold}%) {✓ IF tier_3.srs >= tier_3.srs_threshold ELSE ⚠}"
  OUTPUT "   • Ambiguity: {tier_3.ambiguity} (max: {tier_3.ambiguity_threshold}) {✓ IF tier_3.ambiguity <= tier_3.ambiguity_threshold ELSE ⚠}"
  OUTPUT "   • Coverage: {tier_3.coverage}%"

  # Always continue regardless of score

  # ─────────────────────────────────────────────
  # TIER 4: Deep Analysis (15-30s, ASYNC)
  # ─────────────────────────────────────────────
  tier_4_task = launch_tier_4_async(artifact)
  OUTPUT "🔄 Tier 4 Deep Analysis: running in background..."

  elapsed = timestamp() - start_time
  OUTPUT "⏱️ Validation: {elapsed}ms"

  RETURN {
    status: "PASS" IF tier_3.meets_all_thresholds ELSE "WARN",
    tier: 3,
    scores: tier_3,
    async_task: tier_4_task
  }
```

### Probabilistic Early Exit

```text
ARTIFACT_PASS_RATES = {
  "spec.md": 0.92,      # 92% of specs pass validation
  "plan.md": 0.88,      # 88% of plans pass
  "tasks.md": 0.95,     # 95% of task breakdowns pass
  "concept.md": 0.85    # 85% of concepts pass
}

FUNCTION calculate_pass_confidence(tier_1, tier_2, artifact_type):

  # Tier 1 passed = high baseline confidence
  IF tier_1.passed AND tier_2.passed:
    base_confidence = 0.80
  ELIF tier_1.passed AND tier_2.warnings_only:
    base_confidence = 0.70
  ELIF tier_1.passed:
    base_confidence = 0.50
  ELSE:
    RETURN 0.0  # Cannot skip if Tier 1 failed

  # Adjust by historical pass rate for this artifact type
  historical_rate = ARTIFACT_PASS_RATES.get(artifact_type, 0.85)

  # Adjust by issue count in Tier 2
  issue_penalty = tier_2.warning_count * 0.05  # -5% per warning

  confidence = base_confidence * historical_rate - issue_penalty

  RETURN clamp(confidence, 0.0, 1.0)
```

### Tier 4 Async Callback

```text
FUNCTION launch_tier_4_async(artifact):

  task = Task(
    subagent_type: "code-reviewer",
    model: "haiku",
    run_in_background: true,
    prompt: "
      Perform deep analysis on the artifact:
      1. Check for conflicts with existing codebase patterns
      2. Verify cross-artifact consistency
      3. Run reader testing checks (SR-READ-01 to SR-READ-05)
      4. Generate improvement suggestions

      Artifact: {artifact.path}
      Type: {artifact.type}
    "
  )

  RETURN task.id


FUNCTION check_tier_4_results(task_id):

  result = TaskOutput(task_id, block: false)

  IF result.status == "completed":
    OUTPUT "📋 Tier 4 Deep Analysis Complete:"
    OUTPUT "   • Conflicts: {result.conflicts_found}"
    OUTPUT "   • Consistency: {result.consistency_score}%"
    OUTPUT "   • Suggestions: {result.suggestion_count}"

    IF result.has_critical_issues:
      OUTPUT "   ⚠️ Review recommended before proceeding"

  ELIF result.status == "running":
    OUTPUT "🔄 Tier 4 still running..."

  RETURN result
```

### Integration with Final Checkpoints

Replace CP-*-Final checkpoints with progressive mode:

```text
# specify.md
CP-SPEC-05: Final (Progressive)
  trigger: end_of_generation
  mode: progressive
  tiers:
    1: [SR-SPEC-01]
    2: [SR-SPEC-02, SR-SPEC-03, SR-SPEC-04, SR-SPEC-08]
    3: [VG-001, VG-003, VG-005]
    4: [LLM_REVIEW, CONSISTENCY]
  early_exit_threshold: 0.95

# plan.md
CP-PLAN-05: Final (Progressive)
  trigger: end_of_generation
  mode: progressive
  tiers:
    1: [SR-PLAN-01]
    2: [SR-PLAN-03, SR-PLAN-04, SR-PLAN-07]
    3: [VG-006]
    4: [LLM_REVIEW, CONSISTENCY]
  early_exit_threshold: 0.95

# tasks.md
CP-TASK-04: Final (Progressive)
  trigger: end_of_generation
  mode: progressive
  tiers:
    1: [SR-TASK-01, SR-TASK-02]
    2: [SR-TASK-07, SR-TASK-08]
    3: [VG-007, TRACEABILITY]
    4: [LLM_REVIEW]
  early_exit_threshold: 0.95
```

### Output Format

```text
📋 Progressive Validation
├── Tier 1 Syntax (< 1s)
│   └── ✅ PASS: 5 checks, 0 issues (234ms)
├── Tier 2 Semantic (1-5s)
│   └── ⚠️ WARN: 8 checks, 2 warnings (2.1s)
│       • SR-SPEC-03: FR-005 missing AS link
│       • SR-SPEC-08: Story 3 has no scenarios
├── Tier 3 Quality (5-15s)
│   └── 🎯 SCORES:
│       • SRS: 82% (threshold: 75%) ✓
│       • Ambiguity: 3 (threshold: 5) ✓
│       • Coverage: 94%
└── Tier 4 Deep Analysis
    └── 🔄 Running in background (results via callback)

⏱️ Validation: 7.3s (saved ~18s via progressive exit)
```

### Skip Flags

```text
IF "--skip-validation" IN ARGS:
  OUTPUT "⏭️ Validation skipped (--skip-validation)"
  RETURN {status: "SKIPPED"}

IF "--fast" IN ARGS:
  # Run only Tier 1-2, skip Tier 3-4
  OUTPUT "⚡ Fast mode: Tier 1-2 only"
  SKIP_TIERS = [3, 4]

IF "--full-validation" IN ARGS:
  # Disable early exit, run all tiers
  OUTPUT "🔬 Full validation mode"
  early_exit_threshold = 1.1  # Never triggers
```

### Expected Performance

| Scenario | Before | After | Savings |
|----------|--------|-------|---------|
| Clean artifact (95%+ confidence) | 25s | 3s (T1+T2 + early exit) | **22s** |
| Minor warnings (T3 needed) | 25s | 8s (T1+T2+T3) | **17s** |
| Issues found (full pipeline) | 25s | 25s (all tiers) | 0s |

**Average savings**: 5-10s per command
