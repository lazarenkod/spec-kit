---
description: Generate actionable, dependency-ordered tasks.md with traceability
persona: decomposer-agent
handoffs:
  - label: Analyze For Consistency
    agent: speckit.analyze
    auto: false
  - label: Implement Project
    agent: speckit.implement
    auto: true
    condition: ["tasks.md valid", "P1 tasks defined", "no circular deps"]
    gates: [Tasks Ready, Dependency Validity]
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
claude_code:
  model: sonnet
  reasoning_mode: extended
  thinking_budget: 6000
  cache_control: {system_prompt: ephemeral, constitution: ephemeral, artifacts: ephemeral}
  subagents: [dependency-analyzer, fr-mapper, as-mapper]
---

## Input
```text
$ARGUMENTS
```

---

## Init [REF:INIT-001]

```text
EXECUTE language-loading → ARTIFACT_LANGUAGE
EXECUTE complexity-scoring → COMPLEXITY_TIER

Adapt task generation:
- TRIVIAL: Max 5 tasks, skip RTM
- SIMPLE: Standard breakdown, RTM if FR > 3
- MODERATE: Full breakdown with RTM
- COMPLEX: Full breakdown + dependency graph + rollback tasks
```

---

## Workflow (11 Steps)

### Steps 1-3: Setup & Parse

```text
1. Run {SCRIPT} → FEATURE_DIR, AVAILABLE_DOCS
2. Load design documents:
   - Required: plan.md, spec.md
   - Optional: data-model.md, contracts/, research.md
3. Parse Traceability IDs from spec.md:
   - FR_LIST = [FR-001, FR-002, ...]
   - AS_LIST = [AS-1A, AS-1B, ...]
   - EC_LIST = [EC-001, ...]
   - STORY_PRIORITIES = {US1: P1a, US2: P1b, ...}
   - CONCEPT_IDS (if from concept.md)
```

### Steps 4-6: Generate & Validate

```text
4. Execute task generation:
   - Map user stories to phases (priority order)
   - Generate [DEP:], [FR:], [TEST:] markers
   - Validate task completeness

5. Generate Dependency Graph:
   - Build directed graph from [DEP:] markers
   - Validate: no cycles, valid refs, correct order
   - Output: Mermaid diagram

6. Generate RTM:
   - FR → Impl Tasks → Test Tasks → Status
   - AS → Test Task → Status
```

### Steps 7-11: Output & Update

```text
7. Generate tasks.md using template
8. Validate Traceability (gaps → warnings)
9. Update Feature Manifest (status → TASKED)
10. Update Concept Traceability (if concept.md)
11. Report: task count, coverage, gaps
```

---

## Task Format (REQUIRED)

```text
- [ ] [TaskID] [P?] [Story?] [DEP:?] [FR:?] [TEST:?] Description with file path
```

| Component | Format | Required |
|-----------|--------|----------|
| Checkbox | `- [ ]` | Always |
| Task ID | T001, T002... | Always |
| [P] | Parallelizable marker | If parallel |
| [Story] | [US1], [US2]... | User story phase only |
| [DEP:T###] | Dependencies | If depends on others |
| [FR:FR-###] | Requirement link | Implementation tasks |
| [TEST:AS-###] | Scenario link | Test tasks |
| File path | Exact path | Implementation tasks |

**Examples**:
- `- [ ] T001 Create project structure per implementation plan`
- `- [ ] T012 [P] [US1] [FR:FR-001] Create User model in src/models/user.py`
- `- [ ] T020 [US1] [TEST:AS-1A] Test registration in tests/test_reg.py`

---

## Phase Structure

| Phase | Content | Story Label |
|-------|---------|-------------|
| 1 | Setup (initialization) | None |
| 2 | Foundational (blocking prereqs) | None |
| 3+ | User Stories (priority order P1a, P1b...) | [US1], [US2]... |
| Final | Polish & cross-cutting | None |

---

## Dependency Detection Rules

| Rule | Pattern | Example |
|------|---------|---------|
| Project Structure | T002 → T001 | Initialize depends on structure |
| Database | Service → Model | UserService [DEP:UserModel] |
| API | Endpoint → Service | /users [DEP:UserService] |
| Test | Test → Implementation | test_reg [DEP:UserService] |
| Cross-Story | US2 entity → US1 model | Minimize these |
| Foundation | All stories → Phase 2 | Implicit |

**Circular Detection**: Build graph → topological sort → if cycle, report path

---

## Traceability Validation

```text
FR Coverage: Every FR-xxx has [FR:FR-xxx] task
AS Coverage: Every AS-xxx has [TEST:AS-xxx] task (if tests requested)
Orphan Check: All impl tasks have FR link
DEP Validity: All [DEP:T###] reference existing tasks
```

---

## Self-Review Phase [REF:SR-001]

### Quality Criteria

| ID | Check | Severity |
|----|-------|----------|
| SR-TASK-01 | Task format valid (`- [ ] T###`) | CRITICAL |
| SR-TASK-02 | Task IDs sequential | HIGH |
| SR-TASK-03 | File paths present | HIGH |
| SR-TASK-04 | Story labels valid | MEDIUM |
| SR-TASK-05 | FR coverage complete | CRITICAL |
| SR-TASK-06 | AS coverage complete (if tests) | HIGH |
| SR-TASK-07 | DEP references valid | CRITICAL |
| SR-TASK-08 | No circular dependencies | CRITICAL |
| SR-TASK-09 | RTM table complete | MEDIUM |
| SR-TASK-10 | Coverage summary present | MEDIUM |

### Tier-based Activation

| Tier | Active Criteria |
|------|-----------------|
| TRIVIAL | SR-TASK-01, 07, 08 only |
| SIMPLE | SR-TASK-01 to 06 |
| MODERATE | All SR-TASK-01 to 10 |
| COMPLEX | All + cross-artifact validation |

### Verdict Logic

```text
CRITICAL failures → FAIL (fix, retry max 3)
2+ HIGH failures → WARN
4+ MEDIUM failures → WARN
Quality >= 80% → PASS → auto-handoff
```

### Common Fixes

| Issue | Fix |
|-------|-----|
| Missing checkbox | Prepend `- [ ]` |
| Missing task ID | Add sequential T### |
| Orphan FR | Add [FR:FR-xxx] to relevant task |
| Dangling DEP | Remove invalid ref or add missing task |
| Cycle detected | Remove weakest dependency edge |

---

## Quality Gates

| Gate | Check | Block Condition |
|------|-------|-----------------|
| Tasks Generated | tasks.md valid structure | Missing or malformed |
| Tasks Ready | P1 tasks have file paths + deps | Missing paths or invalid [DEP:] |
| Dependency Validity | No circular deps | Cycle detected |

---

## Output Format

### Quick Summary (Always)

```text
| Aspect | Value |
|--------|-------|
| Feature | {feature_name} |
| Complexity | {TIER} ({score}/100) |
| Total Tasks | {N} tasks |
| FR Coverage | {covered}/{total} ({pct}%) |
| AS Coverage | {covered}/{total} ({pct}%) |
| Status | {PASS|WARN|FAIL} |
| Next Step | → /speckit.implement |
```

### Output Modes

| Mode | Trigger | Content |
|------|---------|---------|
| COMPACT | TRIVIAL/SIMPLE | Summary + collapsible full list |
| STANDARD | MODERATE | Summary + full content + collapsible RTM |
| DETAILED | COMPLEX/--verbose | All sections expanded + self-review + dep graph |

---

## Report Format

```text
┌─────────────────────────────────────────────────────────────┐
│ /speckit.tasks Complete                                      │
├─────────────────────────────────────────────────────────────┤
│ Feature: {feature-name}                                      │
│ Complexity: {TIER}                                           │
│ Tasks: {total} (Setup: {n}, Foundation: {m}, Stories: {k})  │
│                                                              │
│ Traceability:                                                │
│   FR Coverage: {covered}/{total} ({pct}%)                   │
│   AS Coverage: {covered}/{total} ({pct}%)                   │
│   Gaps: {count}                                              │
│                                                              │
│ Dependencies: {valid} valid, {cycles} cycles                 │
│ Self-Review: {PASS|WARN|FAIL}                               │
└─────────────────────────────────────────────────────────────┘
```

### Next Steps

| Condition | Action |
|-----------|--------|
| All gates pass | → /speckit.implement (auto) |
| Circular deps | Fix dependency graph |
| FR coverage gaps | Add missing [FR:] markers |
| Missing file paths | Add paths to impl tasks |

---

## Context

{ARGS}
