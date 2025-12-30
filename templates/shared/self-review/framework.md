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

---

## Universal Quality Checks

These checks apply to ALL artifacts. Import quality modules from `templates/shared/quality/`.

### Anti-Slop Checks (SR-SLOP-01 to SR-SLOP-05)

Reference: `templates/shared/quality/anti-slop.md`

| ID | Name | Description | Severity | Auto-Fix |
|----|------|-------------|----------|----------|
| SR-SLOP-01 | Forbidden Phrases | No cliché AI phrases (e.g., "In today's fast-paced world...") | MEDIUM | ✅ |
| SR-SLOP-02 | Hedge Phrase Density | Less than 2 hedge phrases per section | LOW | ✅ |
| SR-SLOP-03 | Specificity Check | Concrete nouns instead of generic ("users" → persona name) | HIGH | ❌ |
| SR-SLOP-04 | Buzzword Density | Maximum 2 buzzwords per paragraph | MEDIUM | ❌ |
| SR-SLOP-05 | Recommendation Present | Decision sections include clear recommendation | HIGH | ❌ |

```text
ANTI_SLOP_CHECKS = [
  {
    id: "SR-SLOP-01",
    name: "Forbidden Phrases",
    severity: MEDIUM,
    auto_fixable: true,
    check_fn: FUNCTION(artifact):
      LOAD FORBIDDEN_OPENINGS, FORBIDDEN_CONCLUSIONS from anti-slop.md
      matches = SCAN_FOR(artifact.content, FORBIDDEN_OPENINGS + FORBIDDEN_CONCLUSIONS)
      IF matches.length > 0:
        RETURN {status: FAIL, details: "Found: " + matches.join(", ")}
      RETURN {status: PASS}
    fix_fn: FUNCTION(artifact, issue):
      FOR EACH phrase IN issue.matches:
        artifact.content = REMOVE_OR_REWRITE(artifact.content, phrase)
      RETURN artifact
  },

  {
    id: "SR-SLOP-02",
    name: "Hedge Phrase Density",
    severity: LOW,
    auto_fixable: true,
    check_fn: FUNCTION(artifact):
      LOAD HEDGE_PHRASES from anti-slop.md
      sections = SPLIT_BY_SECTIONS(artifact.content)
      FOR EACH section IN sections:
        hedge_count = COUNT_MATCHES(section, HEDGE_PHRASES)
        IF hedge_count >= 2:
          RETURN {status: FAIL, details: "Section '{section.title}' has {hedge_count} hedge phrases"}
      RETURN {status: PASS}
    fix_fn: FUNCTION(artifact, issue):
      # Replace hedge phrases with direct statements or remove
      RETURN REWRITE_HEDGES(artifact)
  },

  {
    id: "SR-SLOP-03",
    name: "Specificity Check",
    severity: HIGH,
    auto_fixable: false,
    check_fn: FUNCTION(artifact):
      GENERIC_TERMS = ["users", "system", "process", "data", "stakeholders", "platform"]
      matches = FIND_GENERIC_USAGE(artifact.content, GENERIC_TERMS)
      IF matches.length > 3:  # Threshold: max 3 generic terms allowed
        RETURN {status: FAIL, details: "Replace generic terms: " + matches.join(", ")}
      RETURN {status: PASS}
  },

  {
    id: "SR-SLOP-04",
    name: "Buzzword Density",
    severity: MEDIUM,
    auto_fixable: false,
    check_fn: FUNCTION(artifact):
      LOAD BUZZWORDS from anti-slop.md
      paragraphs = SPLIT_BY_PARAGRAPHS(artifact.content)
      FOR EACH para IN paragraphs:
        buzz_count = COUNT_MATCHES(para, BUZZWORDS)
        IF buzz_count > 2:
          RETURN {status: FAIL, details: "Paragraph has {buzz_count} buzzwords (max 2)"}
      RETURN {status: PASS}
  },

  {
    id: "SR-SLOP-05",
    name: "Recommendation Present",
    severity: HIGH,
    auto_fixable: false,
    check_fn: FUNCTION(artifact):
      decision_sections = FIND_SECTIONS(artifact, ["Decision", "Approach", "Selection", "Choice"])
      FOR EACH section IN decision_sections:
        IF NOT CONTAINS_RECOMMENDATION(section):
          RETURN {status: FAIL, details: "Section '{section.title}' lists options without recommendation"}
      RETURN {status: PASS}
  }
]
```

### Reader Testing Checks (SR-READ-01 to SR-READ-05)

Reference: `templates/shared/quality/reader-testing.md`

| ID | Name | Description | Severity | Auto-Fix |
|----|------|-------------|----------|----------|
| SR-READ-01 | Fresh Reader Comprehension | New team member can understand in 30 seconds | HIGH | ❌ |
| SR-READ-02 | Role Actionability | Clear next steps for PM, Dev, Designer, QA | MEDIUM | ❌ |
| SR-READ-03 | Ambiguity Detection | No sentence interpretable 2+ ways | HIGH | ❌ |
| SR-READ-04 | Acronym Definitions | All acronyms defined on first use | LOW | ✅ |
| SR-READ-05 | Assumptions Stated | Implicit assumptions made explicit | MEDIUM | ❌ |

```text
READER_TEST_CHECKS = [
  {
    id: "SR-READ-01",
    name: "Fresh Reader Comprehension",
    severity: HIGH,
    auto_fixable: false,
    check_fn: FUNCTION(artifact):
      # Run comprehension check from reader-testing.md
      LOAD COMPREHENSION_QUESTIONS from reader-testing.md
      score = EVALUATE_COMPREHENSION(artifact, COMPREHENSION_QUESTIONS)
      IF score < 0.80:  # 80% threshold
        RETURN {status: FAIL, details: "Comprehension score {score*100}% (need 80%)"}
      RETURN {status: PASS, details: "Comprehension score {score*100}%"}
  },

  {
    id: "SR-READ-02",
    name: "Role Actionability",
    severity: MEDIUM,
    auto_fixable: false,
    check_fn: FUNCTION(artifact):
      LOAD ROLE_CONFIDENCE_CHECKS from reader-testing.md
      relevant_roles = DETERMINE_RELEVANT_ROLES(artifact.type)
      FOR EACH role IN relevant_roles:
        IF NOT ROLE_HAS_CLEAR_NEXT_STEPS(artifact, role):
          RETURN {status: FAIL, details: "{role} cannot determine next steps from this artifact"}
      RETURN {status: PASS}
  },

  {
    id: "SR-READ-03",
    name: "Ambiguity Detection",
    severity: HIGH,
    auto_fixable: false,
    check_fn: FUNCTION(artifact):
      LOAD AMBIGUITY_TRIGGERS from reader-testing.md
      ambiguous = []
      FOR EACH sentence IN artifact.sentences:
        IF CONTAINS_AMBIGUITY(sentence, AMBIGUITY_TRIGGERS):
          ambiguous.push({sentence, trigger: IDENTIFY_TRIGGER(sentence)})
      IF ambiguous.length > 0:
        RETURN {status: FAIL, details: "Found {ambiguous.length} ambiguous statements", issues: ambiguous}
      RETURN {status: PASS}
  },

  {
    id: "SR-READ-04",
    name: "Acronym Definitions",
    severity: LOW,
    auto_fixable: true,
    check_fn: FUNCTION(artifact):
      acronyms = FIND_ALL_ACRONYMS(artifact.content)
      undefined = []
      FOR EACH acronym IN acronyms:
        IF NOT DEFINED_BEFORE_USE(artifact, acronym):
          undefined.push(acronym)
      IF undefined.length > 0:
        RETURN {status: FAIL, details: "Undefined acronyms: " + undefined.join(", ")}
      RETURN {status: PASS}
    fix_fn: FUNCTION(artifact, issue):
      FOR EACH acronym IN issue.undefined:
        definition = LOOKUP_DEFINITION(acronym)
        artifact = INSERT_DEFINITION(artifact, acronym, definition)
      RETURN artifact
  },

  {
    id: "SR-READ-05",
    name: "Assumptions Stated",
    severity: MEDIUM,
    auto_fixable: false,
    check_fn: FUNCTION(artifact):
      implicit_assumptions = DETECT_IMPLICIT_ASSUMPTIONS(artifact)
      IF implicit_assumptions.length > 2:  # Allow 1-2 minor assumptions
        RETURN {status: FAIL, details: "Implicit assumptions not stated: " + implicit_assumptions.join(", ")}
      # Check if Assumptions section exists when needed
      IF implicit_assumptions.length > 0 AND NOT HAS_SECTION(artifact, "Assumptions"):
        RETURN {status: FAIL, details: "Add Assumptions section to document: " + implicit_assumptions.join(", ")}
      RETURN {status: PASS}
  }
]
```

### Applying Universal Checks

```text
UNIVERSAL_CHECKS = ANTI_SLOP_CHECKS + READER_TEST_CHECKS

# These checks run AFTER command-specific checks
# They apply to ALL artifact types

RUN_SELF_REVIEW(artifact, command_criteria):
  command_results = RUN_CHECKS(artifact, command_criteria)
  universal_results = RUN_CHECKS(artifact, UNIVERSAL_CHECKS)
  all_results = command_results + universal_results
  RETURN CALCULATE_VERDICT(all_results)
```

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
