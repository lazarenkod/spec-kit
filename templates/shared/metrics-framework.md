# Spec-Driven Development Metrics Framework

This document defines the metrics framework for measuring quality, velocity, and cost in Spec-Driven Development workflows.

## Overview

The SDD Metrics Framework provides three pillars of measurement:

1. **Spec Quality Score (SQS)** — Aggregate quality metric (0-100) measuring specification completeness and compliance
2. **Velocity Metrics** — Time and efficiency measurements for implementation speed
3. **Cost Metrics** — Token usage and cost tracking per workflow phase

### Integration Points

| Metric Category | Primary Command | Secondary Commands |
|-----------------|-----------------|-------------------|
| SQS | `/speckit.analyze` | `/speckit.implement` (pre-check) |
| Velocity | `/speckit.implement` | All commands (session tracking) |
| Cost | `/speckit.implement` | All commands (token tracking) |

---

## 1. Spec Quality Score (SQS)

### Formula

```
SQS = (
  FR_Coverage × 0.3 +           # % FRs with mapped tasks
  AS_Coverage × 0.3 +           # % Acceptance Scenarios with tests
  Traceability_Score × 0.2 +    # % code with @speckit annotations
  Constitution_Compliance × 0.2 # % principles without CRITICAL violations
) × 100
```

### Component Definitions

#### FR_Coverage (30% weight)

**Definition**: Percentage of Functional Requirements that have at least one mapped task.

```text
FR_Coverage = (FRs_with_tasks / Total_FRs) × 100

Where:
- FRs_with_tasks = Count of FR-XXX IDs appearing in tasks.md Task→FR column
- Total_FRs = Count of FR-XXX entries in spec.md Functional Requirements
```

**Data Source**: Pass D (Task→FR Mapping) in `/speckit.analyze`

**Thresholds**:
| Score | Interpretation |
|-------|----------------|
| 100% | All FRs have implementation tasks |
| 80-99% | Minor gaps in task coverage |
| 50-79% | Significant gaps — review task breakdown |
| < 50% | Major gaps — regenerate tasks.md |

#### AS_Coverage (30% weight)

**Definition**: Percentage of Acceptance Scenarios that have at least one mapped test.

```text
AS_Coverage = (AS_with_tests / Total_AS) × 100

Where:
- AS_with_tests = Count of AS-XXX IDs appearing in test file @speckit annotations
- Total_AS = Count of AS-XXX entries in spec.md Acceptance Scenarios
```

**Data Source**: Pass L (Test→AS Mapping) in `/speckit.analyze`

**Thresholds**:
| Score | Interpretation |
|-------|----------------|
| 100% | All acceptance scenarios have tests |
| 80-99% | Minor test gaps — acceptable for MVP |
| 50-79% | Significant gaps — add test coverage |
| < 50% | Critical gap — tests required before release |

#### Traceability_Score (20% weight)

**Definition**: Percentage of generated code files containing `@speckit` annotations.

```text
Traceability_Score = (Files_with_annotations / Total_generated_files) × 100

Where:
- Files_with_annotations = Files containing @speckit FR-XXX or @speckit AS-XXX
- Total_generated_files = Files created/modified by /speckit.implement
```

**Data Source**: Pass O (Annotation Verification) in `/speckit.analyze`

**Thresholds**:
| Score | Interpretation |
|-------|----------------|
| 100% | Full traceability — all code linked to specs |
| 80-99% | Good traceability — minor gaps |
| 50-79% | Moderate traceability — review implementation |
| < 50% | Poor traceability — re-run implement with annotations |

#### Constitution_Compliance (20% weight)

**Definition**: Percentage of constitution principles without CRITICAL violations.

```text
Constitution_Compliance = ((Total_principles - CRITICAL_violations) / Total_principles) × 100

Where:
- Total_principles = Count of active principles in constitution (base + domain + project)
- CRITICAL_violations = Principles with CRITICAL severity violations in analysis
```

**Data Source**: Pass P (Constitution Compliance) in `/speckit.analyze`

**Thresholds**:
| Score | Interpretation |
|-------|----------------|
| 100% | Full compliance — all principles satisfied |
| 90-99% | Minor violations — review and fix |
| 70-89% | Moderate violations — blocking for production |
| < 70% | Major violations — blocking for any deployment |

---

### Quality Levels

| Level | SQS Threshold | Use Case | Gate Behavior |
|-------|---------------|----------|---------------|
| **Below MVP** | < 80 | Not ready | Blocks `/speckit.implement` |
| **MVP Ready** | 80-89 | Quick iterations, prototypes | Allows implement with warnings |
| **Full Feature** | 90-99 | Production features | Allows implement |
| **Production Ready** | 100 | Critical systems, compliance | Full green light |

### Quality Gates

```text
FUNCTION check_quality_gate(sqs, target_level):

  IF target_level == "mvp" AND sqs < 80:
    RETURN {
      blocked: true,
      message: "SQS {sqs} below MVP threshold (80). Run /speckit.analyze for details."
    }

  IF target_level == "production" AND sqs < 100:
    RETURN {
      blocked: true,
      message: "SQS {sqs} below Production threshold (100). All components must be 100%."
    }

  RETURN { blocked: false }
```

---

## 2. Velocity Metrics

### Metric Definitions

| Metric | ID | Definition | Unit |
|--------|-----|------------|------|
| Time to First Working Code | VEL-001 | Duration from `/speckit.implement` start to first passing test | minutes |
| Time to MVP | VEL-002 | Duration from `/speckit.specify` start to all Wave-1 tasks passing | minutes |
| Human Intervention Rate | VEL-003 | Percentage of tasks requiring manual edits after implement | percentage |
| Auto-Fix Success Rate | VEL-004 | Percentage of build/test errors successfully auto-fixed | percentage |

### Targets and Benchmarks

| Metric | Current Baseline | Target | Lovable Benchmark |
|--------|------------------|--------|-------------------|
| VEL-001: Time to First Code | ~30 min | < 10 min | ~5 min |
| VEL-002: Time to MVP | 2+ hours | < 30 min | ~15 min |
| VEL-003: Human Intervention | ~70% | < 30% | ~15% |
| VEL-004: Auto-Fix Success | ~10% | > 70% | ~80% |

### Calculation Logic

#### VEL-001: Time to First Working Code

```text
FUNCTION calculate_time_to_first_code(session):

  first_test_pass = session.tasks
    .filter(t => t.first_test_pass_at != null)
    .sort_by(t => t.first_test_pass_at)
    .first()

  IF first_test_pass == null:
    RETURN null  # No tests passed yet

  duration_ms = first_test_pass.first_test_pass_at - session.started_at
  RETURN duration_ms / 60000  # Convert to minutes
```

#### VEL-002: Time to MVP

```text
FUNCTION calculate_time_to_mvp(session):

  wave1_tasks = session.tasks.filter(t => t.wave == 1)

  IF NOT all(wave1_tasks, t => t.status == "completed"):
    RETURN null  # MVP not yet complete

  last_wave1_completion = wave1_tasks
    .sort_by(t => t.completed_at)
    .last()
    .completed_at

  # Use specify start if available, else implement start
  start_time = session.specify_started_at ?? session.started_at

  duration_ms = last_wave1_completion - start_time
  RETURN duration_ms / 60000  # Convert to minutes
```

#### VEL-003: Human Intervention Rate

```text
FUNCTION calculate_human_intervention_rate(session):

  total_tasks = session.tasks.length
  tasks_with_manual_edits = session.tasks
    .filter(t => t.human_intervention_required == true)
    .length

  IF total_tasks == 0:
    RETURN 0

  RETURN (tasks_with_manual_edits / total_tasks) × 100
```

#### VEL-004: Auto-Fix Success Rate

```text
FUNCTION calculate_autofix_success_rate(session):

  total_fixes_attempted = sum(session.tasks, t => t.auto_fixes_attempted)
  total_fixes_successful = sum(session.tasks, t => t.auto_fixes_successful)

  IF total_fixes_attempted == 0:
    RETURN 100  # No fixes needed = 100% success

  RETURN (total_fixes_successful / total_fixes_attempted) × 100
```

### Tracking Points

#### At Session Start

```json
{
  "session_id": "uuid-v4",
  "started_at": "2024-01-15T10:30:00Z",
  "command": "/speckit.implement",
  "spec_file": "spec.md",
  "tasks_file": "tasks.md",
  "counters": {
    "tasks_total": 0,
    "tasks_completed": 0,
    "tasks_manual": 0,
    "fixes_attempted": 0,
    "fixes_successful": 0
  }
}
```

#### Per Task

```json
{
  "task_id": "T-001",
  "wave": 1,
  "started_at": "2024-01-15T10:32:00Z",
  "completed_at": "2024-01-15T10:35:00Z",
  "first_test_pass_at": "2024-01-15T10:34:30Z",
  "auto_fixes_attempted": 2,
  "auto_fixes_successful": 1,
  "human_intervention_required": false,
  "build_errors_encountered": 3,
  "test_failures_encountered": 1
}
```

#### At Session End

```json
{
  "session_id": "uuid-v4",
  "completed_at": "2024-01-15T11:15:00Z",
  "velocity": {
    "time_to_first_code_min": 4.5,
    "time_to_mvp_min": 28.0,
    "human_intervention_rate_pct": 25.0,
    "auto_fix_success_rate_pct": 66.7
  },
  "targets": {
    "vel_001_met": true,
    "vel_002_met": true,
    "vel_003_met": true,
    "vel_004_met": false
  }
}
```

---

## 3. Cost Metrics

### Model Pricing

Current pricing per 1,000 tokens (as of 2024):

| Model | Input | Output | Cache Write | Cache Read |
|-------|-------|--------|-------------|------------|
| **Opus** | $0.015 | $0.075 | $0.01875 | $0.0015 |
| **Sonnet** | $0.003 | $0.015 | $0.00375 | $0.0003 |
| **Haiku** | $0.00025 | $0.00125 | $0.0003 | $0.000025 |

### Per-Phase Cost Estimates

Reference costs for a typical feature (50 FRs, 200 tasks):

| Phase | Command | Recommended Model | Est. Tokens | Est. Cost |
|-------|---------|-------------------|-------------|-----------|
| Constitution | `/speckit.constitution` | Opus | 25K | $0.68 |
| Concept | `/speckit.concept` | Opus | 70K | $2.25 |
| Specify | `/speckit.specify` | Opus | 130K | $3.75 |
| Clarify | `/speckit.clarify` | Sonnet | 95K | $0.47 |
| Plan | `/speckit.plan` | Opus | 160K | $4.80 |
| Tasks | `/speckit.tasks` | Sonnet | 200K | $1.20 |
| Design | `/speckit.design` | Opus | 85K | $2.55 |
| Implement | `/speckit.implement` | Opus/Sonnet | 1.5M | $22.00 |
| QA | `/speckit.analyze` | Sonnet | 350K | $1.65 |
| **Total** | | | ~2.6M | **~$39** |

**Optimization Target**: $20-25 (35-50% reduction via caching and model routing)

### Cost Calculation

```text
FUNCTION calculate_cost(tokens, model):

  pricing = MODEL_PRICING[model]

  input_cost = (tokens.input / 1000) × pricing.input
  output_cost = (tokens.output / 1000) × pricing.output
  cache_write_cost = (tokens.cache_write / 1000) × pricing.cache_write
  cache_read_cost = (tokens.cache_read / 1000) × pricing.cache_read

  total_cost = input_cost + output_cost + cache_write_cost + cache_read_cost

  RETURN {
    input_cost: input_cost,
    output_cost: output_cost,
    cache_write_cost: cache_write_cost,
    cache_read_cost: cache_read_cost,
    total_cost: total_cost
  }
```

### Cost Tracking Schema

#### Per Command

```json
{
  "command": "/speckit.implement",
  "model": "opus",
  "tokens": {
    "input": 45000,
    "output": 12000,
    "cache_write": 5000,
    "cache_read": 30000
  },
  "cost": {
    "input_cost": 0.675,
    "output_cost": 0.900,
    "cache_write_cost": 0.094,
    "cache_read_cost": 0.045,
    "total_cost": 1.714
  }
}
```

#### Session Aggregate

```json
{
  "session_id": "uuid-v4",
  "phases": [
    { "command": "/speckit.specify", "cost": 3.75 },
    { "command": "/speckit.plan", "cost": 4.80 },
    { "command": "/speckit.tasks", "cost": 1.20 },
    { "command": "/speckit.implement", "cost": 22.00 }
  ],
  "total_tokens": 2150000,
  "total_cost": 31.75,
  "target_cost": 25.00,
  "cost_efficiency": 0.79
}
```

### Cost Alerts

| Condition | Alert Level | Action |
|-----------|-------------|--------|
| Phase cost > 100% estimate | INFO | Log for tracking |
| Phase cost > 150% estimate | WARNING | Display warning, suggest model routing |
| Session cost > 200% estimate | ERROR | Require user confirmation to continue |

---

## 4. Quality Gates

### Pre-Implementation Gate

**Trigger**: Before `/speckit.implement` execution

```text
FUNCTION pre_implement_gate(sqs, target):

  IF sqs < 80:
    BLOCK with message:
      "Implementation blocked: SQS {sqs}/100 below MVP threshold (80).
       Run /speckit.analyze to identify gaps, then fix before implementing."

  IF sqs < 90 AND target == "production":
    BLOCK with message:
      "Production target requires SQS ≥ 90. Current: {sqs}/100.
       Fix gaps or lower target to 'mvp'."
```

### Post-Implementation Gate

**Trigger**: After `/speckit.implement` completion

```text
FUNCTION post_implement_gate(velocity):

  alerts = []

  IF velocity.human_intervention_rate > 50:
    alerts.push({
      level: "WARNING",
      message: "High human intervention ({rate}%). Review self-healing configuration."
    })

  IF velocity.auto_fix_success < 50:
    alerts.push({
      level: "WARNING",
      message: "Low auto-fix success ({rate}%). Check error patterns and fix templates."
    })

  IF velocity.time_to_mvp > 60:  # 60 minutes
    alerts.push({
      level: "INFO",
      message: "Time to MVP exceeded 1 hour. Consider breaking into smaller features."
    })

  RETURN alerts
```

### Cost Gate

**Trigger**: During command execution when cost threshold exceeded

```text
FUNCTION cost_gate(current_cost, estimated_cost, phase):

  ratio = current_cost / estimated_cost

  IF ratio > 2.0:
    PAUSE with confirmation:
      "Cost for {phase} is {ratio}x estimate (${current} vs ${estimated}).
       Continue? [y/N]"

  IF ratio > 1.5:
    WARN:
      "Cost alert: {phase} at {ratio}x estimate. Consider using Sonnet/Haiku for routine tasks."
```

---

## 5. Reporting Format

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "generated_at": { "type": "string", "format": "date-time" },
    "session_id": { "type": "string" },
    "project": { "type": "string" },
    "sqs": {
      "type": "object",
      "properties": {
        "score": { "type": "number", "minimum": 0, "maximum": 100 },
        "quality_level": { "enum": ["Below MVP", "MVP Ready", "Full Feature", "Production Ready"] },
        "components": {
          "type": "object",
          "properties": {
            "fr_coverage": { "type": "number" },
            "as_coverage": { "type": "number" },
            "traceability": { "type": "number" },
            "constitution_compliance": { "type": "number" }
          }
        }
      }
    },
    "velocity": {
      "type": "object",
      "properties": {
        "time_to_first_code_min": { "type": ["number", "null"] },
        "time_to_mvp_min": { "type": ["number", "null"] },
        "human_intervention_rate_pct": { "type": "number" },
        "auto_fix_success_rate_pct": { "type": "number" }
      }
    },
    "cost": {
      "type": "object",
      "properties": {
        "total_tokens": { "type": "integer" },
        "total_cost_usd": { "type": "number" },
        "phases": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "command": { "type": "string" },
              "model": { "type": "string" },
              "tokens": { "type": "integer" },
              "cost_usd": { "type": "number" }
            }
          }
        }
      }
    }
  }
}
```

### Markdown Report Template

See `templates/metrics-report-template.md` for the human-readable report format.

---

## 6. Implementation Notes

### Data Persistence

Metrics data should be stored in `.speckit/metrics.json` for session continuity:

```json
{
  "sessions": [
    {
      "session_id": "abc123",
      "started_at": "2024-01-15T10:00:00Z",
      "completed_at": "2024-01-15T11:30:00Z",
      "sqs": { "score": 87.5, "..." },
      "velocity": { "..." },
      "cost": { "..." }
    }
  ],
  "aggregates": {
    "avg_sqs": 85.2,
    "avg_time_to_mvp": 35.5,
    "total_cost": 156.80,
    "sessions_count": 5
  }
}
```

### Error Handling

When metric calculation fails:

1. Log the error with context
2. Set the metric value to `null` (not zero)
3. Continue with other metrics
4. Report partial metrics with warnings

### Backward Compatibility

For projects without metrics tracking:

1. SQS components default to analyzing current state (no historical comparison)
2. Velocity metrics show "N/A" for time-based metrics on first run
3. Cost metrics start fresh from current session

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-15 | Initial metrics framework |
