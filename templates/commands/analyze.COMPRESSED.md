---
description: Cross-artifact consistency, traceability, and QA analysis
persona: qa-agent
handoffs:
  - label: Fix Spec Issues
    agent: speckit.specify
    auto: false
    condition: ["CRITICAL/HIGH in spec.md", "Requirement ambiguities"]
  - label: Update Plan
    agent: speckit.plan
    auto: false
    condition: ["Architectural inconsistencies", "Plan revision needed"]
  - label: Regenerate Tasks
    agent: speckit.tasks
    auto: false
    condition: ["Traceability gaps (FR without tasks)", "Dependency restructuring"]
  - label: Proceed to Implementation
    agent: speckit.implement
    auto: true
    condition: ["Pre-impl mode complete", "CRITICAL=0", "SQS>=80"]
    gates: [VG-SQS, VG-CRITICAL, VG-DEPS]
  - label: Fix QA Issues
    agent: speckit.implement
    auto: false
    condition: ["QA mode FAIL", "Tests/build broken"]
  - label: QA Complete
    agent: none
    auto: true
    condition: ["QA Verdict PASS/CONCERNS"]
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
claude_code:
  model: sonnet
  reasoning_mode: extended
  thinking_budget: 12000
  subagents:
    - role: spec-validator
      parallel: true
      trigger: "validating spec artifacts"
    - role: code-validator
      parallel: true
      trigger: "validating implementation coverage"
    - role: consistency-checker
      parallel: true
      depends_on: [spec-validator, code-validator]
    - role: code-explorer
      parallel: true
      trigger: "tracing implementation"
---

## Input
```text
$ARGUMENTS
```

---

## Init [REF:INIT-002]

Minimal init for analysis context:
```text
EXECUTE workspace-detection → WORKSPACE_MODE
LOAD feature context from manifest
SET MODE = detect_analysis_mode()
```

---

## Validation Profiles

| Profile | Passes | Gates | Timeout | Use Case |
|---------|--------|-------|---------|----------|
| spec_validate | B, D | VG-004 (0), VG-005 (5) | 30s | Pre-plan spec gating |
| plan_validate | D, F, V | VG-004 (0), tech_consistency | 45s | Pre-task plan check |
| tasks_validate | G, H, J | no_circular_deps, fr_coverage | 60s | Pre-impl task check |
| sqs | D, E, H, N | SQS >= 80 | 45s | Quality scoring |
| quality_gates | D, E, H, W | All QG gates | 60s | Gate validation |
| pre_deploy | R, S, U | build, tests, security | 90s | Pre-merge checks |
| full | A-Q | All [REF:VG-*] | 180s | Complete analysis |
| qa | R-U | Build, Tests, Perf, Security | 120s | Post-impl QA |

**Auto-Detection**:
```text
IF --profile provided → use specified
ELIF tasks.md has [X] completed AND from /speckit.implement → qa
ELIF from /speckit.specify → spec_validate
ELIF from /speckit.plan → plan_validate
ELIF from /speckit.tasks → tasks_validate
ELSE → full
```

---

## Detection Passes (A-Z)

### Pre-Implementation Passes (A-Q)

| Pass | Name | Severity | Description |
|------|------|----------|-------------|
| A | Duplication Detection | MEDIUM | Cross-artifact duplicate requirements (Jaccard >0.85) |
| B | Ambiguity Detection | HIGH | Vague terms: "appropriate", "as needed", "etc.", pronouns without antecedents |
| C | Underspecification | MEDIUM | Missing AS for FR, empty sections, undefined edge cases |
| D | Constitution Alignment | CRITICAL | Violations of /memory/constitution.md principles [REF:VG-004] |
| E | Cross-Artifact Coverage | HIGH | FR→plan→task coverage gaps |
| F | Inconsistency Detection | MEDIUM | Terminology drift, conflicting statements |
| G | Dependency Graph | CRITICAL | Circular deps, invalid refs, orphan tasks |
| H | Traceability Coverage | HIGH | FR/US without tasks, untraceable requirements |
| I | Concept Coverage | MEDIUM | spec.md coverage of concept.md features (if exists) |
| J | RTM Validation | MEDIUM | Requirements Traceability Matrix completeness |
| K | System Spec Impact | LOW | Cross-feature impact on system specs |
| L | Lineage Validation | MEDIUM | Feature extension chains (/speckit.extend) |
| M | Impact Analysis | MEDIUM | Downstream artifact cascade effects |
| N | Code Traceability | MEDIUM | @speckit annotations in generated code |
| O | Annotation Freshness | LOW | Stale annotations (>30 days unchanged) |
| P | Brownfield Consistency | MEDIUM | baseline.md CB-xxx reference alignment |
| Q | Migration Validation | HIGH | Migration step coverage for brownfield |

### QA Passes (R-U) - Post-Implementation

| Pass | Name | Checks | Severity |
|------|------|--------|----------|
| R | Build Verification | Compile, lint, format | CRITICAL (fail) / MEDIUM (warn) |
| S | Test Verification | Unit, integration, E2E pass rates | CRITICAL (fail) / HIGH (<80%) |
| T | Performance Baseline | Response time, memory, startup | HIGH (>20% regression) |
| U | Security Scan | Dep vulns, SAST, secrets, OWASP | CRITICAL (critical) / HIGH (high) |

### Specialized Passes (V-Z)

| Pass | Name | Trigger | Checks |
|------|------|---------|--------|
| V | API Documentation | plan.md has API section | Endpoints documented, examples present, error codes |
| W | Test-Spec Coverage | Test files exist | Test→AS mapping, coverage gaps |
| X | UXQ Domain | UXQ domain active | Touch-target sizing, contrast ratios, loading states |
| Y | UX Foundation | design-system.md exists | Accessibility, responsiveness, error states |
| Z | Design System | app-design/ exists | Token compliance, component consistency |

---

## Pass Detection Logic

### A: Duplication Detection
```text
FOR each pair (artifact1, artifact2) IN [concept, spec, plan, tasks]:
  FOR each requirement R1 IN artifact1, R2 IN artifact2:
    similarity = jaccard(normalize(R1), normalize(R2))
    IF similarity > 0.85 AND R1 != R2:
      ADD Finding(DUP-NNN, MEDIUM, R1, R2, similarity)
```

### B: Ambiguity Detection [REF:VG-005]
```text
SCAN for patterns:
  - "appropriate", "as needed", "etc.", "and so on"
  - Pronouns without clear antecedent ("it", "they", "this")
  - Quantifier gaps ("some users", "many requests")
  - Unmeasurable terms ("fast", "user-friendly", "secure")
```

### D: Constitution Alignment [REF:VG-004]
```text
LOAD /memory/constitution.md principles
FOR each principle P IN constitution:
  IF spec/plan violates P:
    ADD Finding(CONST-NNN, CRITICAL, artifact, section, violation)
```

### G: Dependency Graph
```text
BUILD directed graph: tasks → dependencies
DETECT:
  - Circular dependencies (Tarjan SCC)
  - Invalid references (missing targets)
  - Orphan tasks (no incoming/outgoing)
```

### H: Traceability Coverage
```text
FOR each FR-xxx IN spec.md:
  IF NOT exists task with Trace: FR-xxx:
    ADD Finding(TRACE-NNN, HIGH, FR-xxx, "No implementing task")
FR_Coverage = (FRs_with_tasks / Total_FRs) × 100
```

### R-U: QA Verification Mode
```text
TRIGGER: tasks.md has [X] completed tasks
EXECUTE in order:
  R: Build → npm run build / cargo build / go build
  S: Tests → npm test / pytest / go test
  T: Performance → lighthouse / k6 / custom benchmarks
  U: Security → npm audit / snyk / trivy / semgrep
```

---

## Severity Assignment

| Severity | Weight | Criteria |
|----------|--------|----------|
| CRITICAL | 10 | Constitution violations, circular deps, build failures, critical vulns |
| HIGH | 5 | Untraceable FR, ambiguity clusters, test failures, API gaps |
| MEDIUM | 2 | Duplications, terminology drift, performance regression, minor gaps |
| LOW | 1 | Stale annotations, style issues, optional improvements |

---

## Spec Quality Score (SQS)

```text
SQS = (FR_Coverage × 0.3 + AS_Coverage × 0.3 + Traceability × 0.2 + Constitution × 0.2) × 100
```

| Component | Source Pass | Weight |
|-----------|-------------|--------|
| FR_Coverage | H (FRs with tasks / Total FRs) | 0.3 |
| AS_Coverage | W (AS with tests / Total AS) | 0.3 |
| Traceability | N (Annotated files / Generated files) | 0.2 |
| Constitution | D (Principles - CRITICAL violations / Principles) | 0.2 |

**Quality Levels**:
| SQS | Level | Gate |
|-----|-------|------|
| < 80 | Below MVP | Blocks /speckit.implement |
| 80-89 | MVP Ready | Proceed with warnings |
| 90-99 | Full Feature | Proceed |
| 100 | Production Ready | Full green light |

---

## Report Format

### Summary Table
```markdown
| Metric | Value |
|--------|-------|
| Analysis Mode | {PRE_IMPLEMENTATION | QA_VERIFICATION} |
| Profile | {profile_name} |
| Artifacts Analyzed | {count} |
| Passes Executed | {pass_list} |
| Findings | C:{n} H:{n} M:{n} L:{n} |
| SQS | {score}/100 ({level}) |
| Verdict | {PASS | CONCERNS | FAIL} |
```

### Findings Table (max 50 rows)
```markdown
| ID | Pass | Severity | Artifact | Location | Finding | Recommendation |
```

---

## Quality Gates

| Gate | Check | Block If | Message |
|------|-------|----------|---------|
| VG-CRITICAL | CRITICAL count == 0 | CRITICAL > 0 | Resolve all CRITICAL issues first |
| VG-DEPS | Dep Graph VALID/WARNINGS | INVALID | Resolve circular dependencies |
| VG-SQS | SQS >= 80 | SQS < 80 | SQS below MVP threshold (80) |
| VG-QA | No CRITICAL/HIGH in R-U | CRITICAL/HIGH > 0 | QA failed - fix blocking issues |
| VG-BUILD | Build succeeds | Build fails | Fix build errors |
| VG-TESTS | All tests pass | Failures exist | Fix failing tests |
| VG-SECURITY | No critical vulns | Critical found | Address security vulnerabilities |

---

## Automation Behavior

### Mode Detection
```text
IF tasks.md exists AND has [X] completed:
  IF from /speckit.implement handoff → QA_VERIFICATION
  ELIF user requests QA → QA_VERIFICATION
  ELSE → PRE_IMPLEMENTATION
ELSE → PRE_IMPLEMENTATION
```

### Auto-Transitions

**Pre-Implementation Mode**:
| Condition | Next | Gate |
|-----------|------|------|
| Complete, CRITICAL=0, Deps valid, SQS>=80 | /speckit.implement | VG-CRITICAL, VG-DEPS, VG-SQS |
| CRITICAL>0 OR Deps invalid | Block | Display issues, offer handoffs |

**QA Mode**:
| Verdict | Action |
|---------|--------|
| PASS | Done, ready for merge |
| CONCERNS | Done with warnings |
| FAIL | Handoff to /speckit.implement |

### QA Loop
```text
/speckit.implement → /speckit.analyze (QA) → PASS → Merge
                                    ↓ FAIL
                            Fix → /speckit.analyze (QA) → ...
```

---

## Self-Review [REF:SR-001]

**Criteria**: SR-ANALYZE-01 to SR-ANALYZE-06

| ID | Check | Severity |
|----|-------|----------|
| SR-ANALYZE-01 | All requested passes executed | CRITICAL |
| SR-ANALYZE-02 | Findings have valid IDs | HIGH |
| SR-ANALYZE-03 | Severity assigned correctly | HIGH |
| SR-ANALYZE-04 | SQS calculated (if applicable) | MEDIUM |
| SR-ANALYZE-05 | Recommendations actionable | MEDIUM |
| SR-ANALYZE-06 | No false positives (obvious) | LOW |

---

## Operating Principles

- **Read-only**: NEVER modify files
- **Minimal tokens**: Focus on actionable findings
- **Progressive disclosure**: Load artifacts incrementally
- **Deterministic**: Consistent IDs and counts on rerun
- **Prioritize constitution**: Always CRITICAL severity
- **Limit output**: Max 50 findings in table

---

## Next Actions

At report end:
- CRITICAL exists → "Resolve before /speckit.implement"
- Only LOW/MEDIUM → Improvement suggestions
- Provide explicit commands: `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`
- Offer: "Would you like concrete remediation edits for top N issues?"

---

## Context

{ARGS}
