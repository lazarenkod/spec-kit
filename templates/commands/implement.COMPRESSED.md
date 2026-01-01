---
description: Execute implementation from tasks.md with quality gates
persona: developer-agent
pre_gates:
  tasks_exist:
    check: file_exists(specs/{feature}/tasks.md)
    on_fail: handoff → speckit.tasks
  critical_analysis:
    check: no CRITICAL findings from /speckit.analyze
    on_fail: handoff → speckit.analyze
handoffs:
  - label: QA Verification
    agent: speckit.analyze
    auto: true
    condition: ["All tasks complete", "Build passes"]
  - label: Fix Spec Issues
    agent: speckit.specify
    auto: false
    condition: ["Spec gaps discovered"]
  - label: Update Plan
    agent: speckit.plan
    auto: false
    condition: ["Architectural issues"]
  - label: Regenerate Tasks
    agent: speckit.tasks
    auto: false
    condition: ["Task structure invalid"]
claude_code:
  model: sonnet
  reasoning_mode: extended
  thinking_budget: 16000
  phases: [bootstrap, implement, validate, document]
  subagents:
    wave_1: [spec-analyzer, plan-analyzer, task-reader]
    wave_2: [code-generator, test-generator]
    wave_3: [code-validator, build-runner]
    wave_4: [doc-generator, consistency-checker]
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## Input
```text
$ARGUMENTS
```

---

## Init [REF:INIT-001]

```text
EXECUTE workspace-detection → WORKSPACE_MODE
LOAD feature context from manifest
VALIDATE pre_gates (tasks exist, no CRITICAL)
SET cache_key = hash(spec + plan + tasks)
```

---

## Auto-Fix Rules

| ID | Pattern | Auto-Fix | When |
|----|---------|----------|------|
| AF-001 | Missing @speckit annotation | Add annotation header | After file creation |
| AF-002 | Orphan TODO in code | Convert to task or remove | Build success |
| AF-003 | Lint errors | Run auto-formatter | Before commit |
| AF-004 | Missing imports | Add required imports | On compile error |
| AF-005 | Type errors | Infer/add types | On type check fail |
| AF-006 | Unused variables | Remove or prefix _ | Lint warning |
| AF-007 | Missing test file | Generate test stub | After impl file |
| AF-008 | Stale annotation | Update trace refs | On task complete |

---

## Build Error Patterns

| Language | Pattern | Fix Strategy |
|----------|---------|--------------|
| TypeScript | TS2307 module not found | npm install, check tsconfig paths |
| TypeScript | TS2339 property missing | Add property or fix interface |
| Python | ModuleNotFoundError | pip install, check __init__.py |
| Python | ImportError | Fix relative imports, check PYTHONPATH |
| Rust | E0433 unresolved | cargo add, check mod.rs |
| Go | undefined: X | go get, check imports |
| Java | cannot find symbol | Add import, check classpath |
| C# | CS0246 type not found | Add using, check references |
| Ruby | LoadError | bundle install, check require |
| Swift | No such module | Add to Package.swift |

---

## Vision Validation

```text
IF design.md exists AND has wireframes:
  turbo_mode: false (validate UI against design)
  CAPTURE screenshots at: mobile(375), tablet(768), desktop(1280)
  RUN visual diff against wireframes

  UX_CHECKS:
    - Touch targets ≥ 44x44px
    - Contrast ratio ≥ 4.5:1
    - Focus indicators visible
    - Loading states present
    - Error states handled

ELSE:
  turbo_mode: true (skip visual validation)
```

---

## Workflow (16 Steps)

### Phase 1: Bootstrap

```text
Step 1: Load Implementation Checklist
  READ templates/shared/impl-checklist.md
  LOAD feature-specific DoD from spec.md

Step 2: Load Context (cached)
  IF cache_key matches → use cached context
  ELSE:
    PARALLEL READ: spec.md, plan.md, tasks.md, design.md (if exists)
    CACHE context for session

Step 3: Project Setup Verification
  DETECT project_type from files (package.json, pyproject.toml, etc.)
  VERIFY dependencies installed
  CHECK build tools available

Step 4: Manifest Update
  SET feature status = "IMPLEMENTING"
  RECORD start timestamp
```

### Phase 2: Implementation

```text
Step 5: Concept Traceability (if concept.md exists)
  LOAD EPIC-NNN.FNN references
  TRACK coverage: implemented / total

Step 6: Task Execution Loop
  FOR EACH task IN tasks.md (dependency order):
    6a: Parse task → files, trace refs, DoD
    6b: IF blocked → skip, log, continue
    6c: Generate code with @speckit annotations
    6d: Run lint + format
    6e: Run incremental tests
    6f: Mark task [X] complete
    6g: Update progress (N/M tasks)

  ANNOTATIONS format:
    // @speckit FR-001 US-002 T005
    // @speckit-end
```

### Phase 3: Validation

```text
Step 7: Build Verification
  RUN full build
  IF fails:
    ATTEMPT auto-fix (3 iterations max)
    IF still fails → HALT, report errors

Step 8: Test Execution
  RUN unit tests
  RUN integration tests (if exist)
  COLLECT coverage metrics
  FAIL if coverage < threshold (default 70%)

Step 9: Vision Validation (if design.md exists)
  CAPTURE screenshots
  RUN visual diff
  RUN UX checks
  REPORT deviations
```

### Phase 4: Documentation

```text
Step 10: Generate RUNNING.md
  CREATE local development guide:
    - Prerequisites
    - Install commands
    - Run commands
    - Test commands
    - Environment variables

Step 11: Update README.md (if exists)
  ADD feature documentation section
  UPDATE usage examples
  PRESERVE existing content

Step 12: Update Concept Traceability (if concept.md)
  UPDATE status: EPIC-NNN.FNN → "Implemented"
  RECORD implementation date
```

---

## Definition of Done

```text
TASK DoD (per task):
- [ ] Code written with @speckit annotations
- [ ] Tests pass (unit + integration)
- [ ] Lint clean
- [ ] task.md marked [X]

FEATURE DoD (all tasks):
- [ ] All tasks complete
- [ ] Build passes
- [ ] Coverage ≥ threshold
- [ ] RUNNING.md generated
- [ ] No CRITICAL issues
```

---

## Self-Healing Engine

```text
ON build_error:
  MATCH error against Build Error Patterns
  IF match found:
    APPLY fix strategy
    RE-RUN build (max 3 attempts)
  ELSE:
    LOG error, continue or halt based on severity

ON test_failure:
  ANALYZE failure (assertion vs runtime vs timeout)
  IF fixable → apply fix, re-run
  ELSE → log, mark task blocked
```

---

## Self-Review Phase [REF:SR-001]

### Step 0.5: Build-Until-Works Loop

```text
FOR attempt IN 1..5:
  RUN build
  IF success → BREAK
  ELSE:
    PARSE errors
    APPLY auto-fixes
    CONTINUE

IF still failing after 5 → HALT with diagnostics
```

### Quality Criteria

| ID | Check | Severity |
|----|-------|----------|
| SR-IMPL-01 | All tasks marked complete | CRITICAL |
| SR-IMPL-02 | Build passes | CRITICAL |
| SR-IMPL-03 | Tests pass | CRITICAL |
| SR-IMPL-04 | @speckit annotations present | HIGH |
| SR-IMPL-05 | Coverage ≥ threshold | HIGH |
| SR-IMPL-06 | No TODO in committed code | MEDIUM |
| SR-IMPL-07 | Lint clean | MEDIUM |
| SR-IMPL-08 | RUNNING.md generated | HIGH |
| SR-IMPL-09 | Concept traceability updated | MEDIUM |
| SR-IMPL-10 | No orphan files | LOW |
| SR-IMPL-11 | API contracts match plan | HIGH |
| SR-IMPL-12 | Error handling implemented | HIGH |
| SR-IMPL-13 | Edge cases covered | MEDIUM |
| SR-IMPL-14 | Performance within bounds | MEDIUM |
| SR-IMPL-15 | Security patterns applied | HIGH |
| SR-IMPL-16 | Accessibility met (if UX) | HIGH |
| SR-IMPL-17 | Documentation accurate | MEDIUM |
| SR-IMPL-18 | Dependencies minimal | LOW |
| SR-IMPL-19 | No hardcoded secrets | CRITICAL |
| SR-IMPL-20 | Rollback path exists (brownfield) | HIGH |

### UXQ Checks (if design.md exists)

| Check | Threshold |
|-------|-----------|
| Touch targets | ≥ 44x44px |
| Contrast ratio | ≥ 4.5:1 (AA) |
| Focus visible | All interactive |
| Loading states | Present for async |
| Error feedback | Clear + actionable |
| Keyboard nav | Full support |

### Verdict Logic

```text
PASS: CRITICAL=0 AND HIGH≤2 AND build+tests pass
  → Auto-handoff to /speckit.analyze (QA mode)

WARN: CRITICAL=0 AND HIGH≤5
  → Proceed with documented issues

FAIL: CRITICAL>0 OR build fails OR tests fail
  → Self-correct (max 3 iterations)
  → If still failing → HALT, manual intervention
```

---

## Automation Behavior

### Task Selection

```text
IF --task T005 → execute single task
ELIF --from T003 → execute T003 onwards
ELIF --retry-failed → re-execute [X] with errors
ELSE → execute all pending tasks in order
```

### Progress Tracking

```text
UPDATE manifest.features[].progress:
  - tasks_total: N
  - tasks_complete: M
  - coverage: X%
  - last_task: TXXX
  - status: IMPLEMENTING | BLOCKED | COMPLETE
```

### Cross-Repo (if WORKSPACE_MODE)

```text
FOR EACH cross_repo_dep IN spec.md:
  VERIFY dependency available
  IF not → WARN, document assumption
  TRACK as external dependency
```

---

## Report Format

```text
┌─────────────────────────────────────────────────────────────┐
│ /speckit.implement Complete                                  │
├─────────────────────────────────────────────────────────────┤
│ Feature: {feature-name}                                      │
│ Tasks: {completed}/{total} ({percentage}%)                   │
│ Coverage: {coverage}%                                        │
│ Build: {PASS|FAIL}    Tests: {PASS|FAIL}                    │
│ Self-Review: {PASS|WARN|FAIL}                               │
│                                                              │
│ Files Created: {N}    Files Modified: {M}                    │
│ Annotations: {count} @speckit tags                           │
│                                                              │
│ Duration: {time}                                             │
└─────────────────────────────────────────────────────────────┘
```

### Task Summary Table

| Task | Status | Trace | Files |
|------|--------|-------|-------|
| T001 | ✓ | FR-001, AS-1A | src/auth.ts |
| T002 | ✓ | FR-002 | src/api.ts, tests/api.test.ts |
| ... | | | |

### Next Steps

| Condition | Action |
|-----------|--------|
| All pass | → /speckit.analyze (QA mode) |
| Build fails | Fix errors, re-run |
| Test fails | Fix tests, re-run |
| Coverage low | Add tests for uncovered paths |

---

## Context

{ARGS}
