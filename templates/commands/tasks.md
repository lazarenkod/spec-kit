---
description: Generate an actionable, dependency-ordered tasks.md with full traceability to spec requirements and acceptance scenarios.
persona: decomposer-agent
handoff:
  requires: handoffs/plan-to-tasks.md
  generates: handoffs/tasks-to-implement.md
  template: templates/handoff-template.md
handoffs:
  - label: Analyze For Consistency
    agent: speckit.analyze
    prompt: Run a project analysis for consistency and validate traceability
    auto: false
    condition:
      - "User prefers thorough validation before implementation"
      - "Complex project with many cross-references"
    gates:
      - name: "Tasks Generated Gate"
        check: "tasks.md created with valid structure"
        block_if: "tasks.md missing or malformed"
        message: "Tasks must be generated before analysis"
  - label: Implement Project
    agent: speckit.implement
    prompt: Start the implementation in phases
    auto: true
    condition:
      - "tasks.md generated with valid task structure"
      - "At least one P1 task defined"
      - "No circular dependencies detected"
    pre_handoff_action:
      name: "Tasks Validation"
      invoke: speckit.analyze
      args: "--quiet"  # Profile auto-detected from caller context
      skip_flag: "--skip-validate"
      timeout: 30s
      gates:
        - name: "Circular Dependencies Gate"
          pass: G
          threshold: 0
          severity: CRITICAL
          block_if: "circular dependencies > 0"
          message: "Circular task dependencies detected. Fix before implementation."
        - name: "FR Coverage Gate"
          pass: H
          threshold: 0
          severity: HIGH
          block_if: "FRs without tasks > 0"
          message: "Some requirements have no implementation tasks."
      on_failure:
        action: block
        message: "Tasks validation failed. Review dependency graph and traceability."
    gates:
      - name: "Tasks Ready Gate"
        check: "All P1 tasks have file paths and dependencies defined"
        block_if: "P1 tasks missing file paths or have invalid [DEP:] references"
        message: "Ensure all P1 tasks are fully specified before implementation"
      - name: "Dependency Validity Gate"
        check: "No circular dependencies in task graph"
        block_if: "Circular dependency detected"
        message: "Resolve circular dependencies before proceeding"
    post_actions:
      - "log: Tasks generated, ready for implementation"
  - label: Regenerate Tasks
    agent: speckit.tasks
    prompt: Regenerate tasks with updated plan or spec
    auto: false
    condition:
      - "Plan or spec was modified after initial task generation"
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
claude_code:
  model: sonnet
  reasoning_mode: extended
  thinking_budget: 8000
  orchestration:
    max_parallel: 2
    role_isolation: true
  subagents:
    - role: dependency-analyzer
      role_group: INFRA
      parallel: true
      depends_on: []
      priority: 9
      trigger: "when analyzing task dependencies and build order"
      prompt: "Analyze dependencies between components in plan.md to determine optimal task ordering"
      model_override: haiku
    - role: fr-mapper
      role_group: BACKEND
      parallel: true
      depends_on: []
      priority: 8
      trigger: "when mapping functional requirements to implementation tasks"
      prompt: "Map functional requirements {FR_IDS} to concrete implementation tasks"
    - role: as-mapper
      role_group: TESTING
      parallel: true
      depends_on: [fr-mapper]
      priority: 7
      trigger: "when mapping acceptance scenarios to test tasks"
      prompt: "Map acceptance scenarios {AS_IDS} to test implementation tasks"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

---

## Parallel Execution

{{include: shared/orchestration-instructions.md}}

Execute subagents defined in `claude_code.subagents` using parallel Task calls per wave.
See orchestration settings: `max_parallel: 3`, `wave_overlap.threshold: 0.80`.

---

## Outline

0. **Load project context**:

   Read and apply shared modules using **parallel loading** (see `templates/shared/core/parallel-loading.md`):

   ```text
   # PARALLEL BATCH READ (single message, multiple Read tool calls)
   Read IN PARALLEL:
   - `templates/shared/core/language-loading.md`
   - `templates/shared/complexity-scoring.md`
   - `templates/shared/core/brownfield-detection.md`

   # Execute after all loaded
   EXECUTE language-loading.md → ARTIFACT_LANGUAGE
   EXECUTE complexity-scoring.md → COMPLEXITY_TIER, COMPLEXITY_SCORE
   EXECUTE brownfield-detection.md → BROWNFIELD_MODE

   REPORT: "Generating tasks in {LANGUAGE_NAME} ({ARTIFACT_LANGUAGE})..."
   REPORT: "Complexity: {COMPLEXITY_TIER} ({COMPLEXITY_SCORE}/100)"
   ```

   Adapt task generation based on COMPLEXITY_TIER:
   - **TRIVIAL**: Compact task list (max 5 tasks), skip RTM
   - **SIMPLE**: Standard breakdown, include RTM if FR count > 3
   - **MODERATE**: Full breakdown with RTM and regression considerations
   - **COMPLEX**: Full breakdown with dependency graph, [CRITICAL] markers, rollback tasks

1. **Setup**: Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Parse Traceability IDs from spec.md**:

   ```text
   Extract from spec.md:

   a. Concept Reference (if present):
      - Source Concept: specs/concept.md
      - Concept IDs Covered: EPIC-001.F01.S01, EPIC-001.F01.S02

   b. Functional Requirements (FR-NNN):
      - FR-001: System MUST [capability]
      - FR-002: Users MUST be able to [action]
      → Store: FR_LIST = [FR-001, FR-002, ...]

   c. Acceptance Scenarios (AS-[story][letter]):
      - AS-1A: Given X, When Y, Then Z
      - AS-1B: Given A, When B, Then C
      → Store: AS_LIST = [AS-1A, AS-1B, AS-2A, ...]

   d. Edge Cases (EC-NNN):
      - EC-001: [boundary condition]
      → Store: EC_LIST = [EC-001, EC-002, ...]

   e. User Story Priorities (P1a, P1b, P2a):
      → Store: STORY_PRIORITIES = {US1: P1a, US2: P1b, ...}
   ```

4. **Execute task generation workflow**:
   - Load plan.md and extract tech stack, libraries, project structure
   - Load spec.md and extract user stories with their priorities (P1a, P1b, P2a, etc.)
   - If data-model.md exists: Extract entities and map to user stories
   - If contracts/ exists: Map endpoints to user stories
   - If research.md exists: Extract decisions for setup tasks
   - Generate tasks organized by user story (see Task Generation Rules below)
   - **Generate [DEP:] markers** for each task based on dependencies (see Dependency Detection)
   - **Generate [FR:] markers** linking implementation tasks to requirements
   - **Generate [TEST:] markers** linking test tasks to acceptance scenarios
   - Validate task completeness (each user story has all needed tasks, independently testable)

5. **Generate Dependency Graph**:

   ```text
   FOR EACH task with [DEP:Txxx] marker:
     Add edge: Txxx --> current_task

   Validate:
     - No circular dependencies (A → B → C → A)
     - All referenced task IDs exist
     - Foundational tasks (Phase 2) must complete before user stories (Phase 3+)

   Generate Mermaid diagram:
     graph TD
       subgraph Phase1[Setup]
         T001[T001: description]
       end
       T001 --> T002
   ```

6. **Generate Requirements Traceability Matrix (RTM)**:

   ```text
   FOR EACH FR in FR_LIST:
     Find all tasks with [FR:FR-xxx] marker
     Find test tasks that cover this FR's acceptance scenarios
     Add row to RTM: FR → Impl Tasks → Test Tasks → Status

   FOR EACH AS in AS_LIST:
     Find test task with [TEST:AS-xxx] marker
     Add row to AS Coverage: AS → Test Task → Status
   ```

7. **Generate tasks.md**: Use `templates/tasks-template.md` as structure, fill with:
   - Correct feature name from plan.md
   - Phase 1: Setup tasks (project initialization)
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
   - Phase 3+: One phase per user story (in priority order from spec.md)
   - Each phase includes:
     - **Concept Reference**: EPIC-001.F01.S01 (if from concept.md)
     - **Acceptance Scenarios Covered**: AS-1A, AS-1B
     - Story goal, independent test criteria
     - Tests with [TEST:AS-xxx] markers (if requested)
     - Implementation tasks with [FR:FR-xxx] and [DEP:Txxx] markers
   - Final Phase: Polish & cross-cutting concerns
   - **Dependency Graph** (Mermaid)
   - **Requirements Traceability Matrix**
   - **Acceptance Scenario Coverage**
   - **Coverage Summary** with gaps identified
   - Clear file paths for each task
   - Implementation strategy section (MVP first, incremental delivery)

8. **Validate Traceability**:

   ```text
   Check for gaps:
   - [ ] Every FR has at least one implementation task
   - [ ] Every AS has at least one test task (if tests requested)
   - [ ] Every EC has handling (implementation or documented exclusion)
   - [ ] No orphan tasks (tasks without FR/AS link)

   If gaps found:
     - Add to "Gaps Identified" section
     - Warn user but continue generation
   ```

9. **Update Feature Manifest**: After tasks.md is generated:

   Read `templates/shared/core/manifest-update.md` and apply with:
   - `CALLER` = "tasks"
   - `NEW_STATUS` = "TASKED"
   - `REQUIRED_CURRENT_STATUS` = "PLANNED"

   This updates the feature manifest to reflect task generation completion.

10. **Update Concept Traceability** (if concept.md exists):

   ```text
   IF exists("specs/concept.md"):
     1. Read concept.md
     2. Find "Traceability Skeleton" section

     3. Extract CONCEPT_IDS from spec.md (parsed in Step 3):
        - Concept IDs Covered: EPIC-001.F01.S01, EPIC-001.F01.S02

     4. FOR EACH concept_id in CONCEPT_IDS:
        Find row in Traceability Skeleton where Concept ID = concept_id
        UPDATE row:
          - "Tasks": Count of tasks or range (e.g., "T001-T015" or "15 tasks")
          - "Status": "TASKED"

     5. Update "Progress Rollup" section:
        - Recount statuses across all rows
        - Update percentages

     6. Update "Foundation Progress" section:
        - Check if this feature is in Wave 1 or Wave 2
        - Update Wave completion counts if applicable

     7. Set "Last Updated": "{today's date} by /speckit.tasks"

     8. Write updated concept.md
   ```

   Report: "Concept traceability updated: {CONCEPT_IDS} → TASKED ({task_count} tasks)"

11. **Report**: Output path to generated tasks.md and summary:
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - **Traceability coverage**:
     - FR coverage: N/M requirements have implementation tasks
     - AS coverage: N/M scenarios have test tasks
     - Gap count and details
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1)
   - Format validation: Confirm ALL tasks follow the checklist format

Context for task generation: {ARGS}

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

**Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

### Checklist Format (REQUIRED)

Every task MUST strictly follow this format:

```text
- [ ] [TaskID] [P?] [Story?] [DEP:?] [FR:?] [TEST:?] Description with file path
```

**Format Components**:

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
2. **Task ID**: Sequential number (T001, T002, T003...) in execution order
3. **[P] marker**: Include ONLY if task is parallelizable (different files, no dependencies on incomplete tasks)
4. **[Story] label**: REQUIRED for user story phase tasks only
   - Format: [US1], [US2], [US3], etc. (maps to user stories from spec.md)
   - Setup phase: NO story label
   - Foundational phase: NO story label
   - User Story phases: MUST have story label
   - Polish phase: NO story label
5. **[DEP:T001,T002]**: Explicit dependencies on other tasks
   - List all task IDs that MUST complete before this task
   - Validated for circular dependencies by /speckit.analyze
6. **[FR:FR-001,FR-002]**: Links to Functional Requirements from spec.md
   - Implementation tasks SHOULD reference the FR they fulfill
   - Enables RTM (Requirements Traceability Matrix) generation
7. **[TEST:AS-1A]**: Links test task to Acceptance Scenario
   - Test tasks SHOULD reference the AS they verify
   - Enables Acceptance Scenario Coverage tracking
8. **Description**: Clear action with exact file path

**Examples**:

- ✅ CORRECT: `- [ ] T001 Create project structure per implementation plan`
- ✅ CORRECT: `- [ ] T005 [P] [DEP:T002] Implement authentication middleware in src/middleware/auth.py`
- ✅ CORRECT: `- [ ] T012 [P] [US1] [FR:FR-001] Create User model in src/models/user.py`
- ✅ CORRECT: `- [ ] T014 [US1] [DEP:T012,T013] [FR:FR-001,FR-002] Implement UserService in src/services/user_service.py`
- ✅ CORRECT: `- [ ] T020 [US1] [TEST:AS-1A] Test "user can register" in tests/integration/test_registration.py`
- ❌ WRONG: `- [ ] Create User model` (missing ID and Story label)
- ❌ WRONG: `T001 [US1] Create model` (missing checkbox)
- ❌ WRONG: `- [ ] [US1] Create User model` (missing Task ID)
- ❌ WRONG: `- [ ] T001 [US1] Create model` (missing file path)

### Task Organization

1. **From User Stories (spec.md)** - PRIMARY ORGANIZATION:
   - Each user story (P1, P2, P3...) gets its own phase
   - Map all related components to their story:
     - Models needed for that story
     - Services needed for that story
     - Endpoints/UI needed for that story
     - If tests requested: Tests specific to that story
   - Mark story dependencies (most stories should be independent)

2. **From Contracts**:
   - Map each contract/endpoint → to the user story it serves
   - If tests requested: Each contract → contract test task [P] before implementation in that story's phase

3. **From Data Model**:
   - Map each entity to the user story(ies) that need it
   - If entity serves multiple stories: Put in earliest story or Setup phase
   - Relationships → service layer tasks in appropriate story phase

4. **From Setup/Infrastructure**:
   - Shared infrastructure → Setup phase (Phase 1)
   - Foundational/blocking tasks → Foundational phase (Phase 2)
   - Story-specific setup → within that story's phase

### Phase Structure

- **Phase 1**: Setup (project initialization)
- **Phase 2**: Foundational (blocking prerequisites - MUST complete before user stories)
- **Phase 3+**: User Stories in priority order (P1a, P1b, P2a, P2b, P3...)
  - Within each story: Tests (if requested) → Models → Services → Endpoints → Integration
  - Each phase should be a complete, independently testable increment
- **Final Phase**: Polish & Cross-Cutting Concerns

### Dependency Detection Logic

**Automatic [DEP:] generation based on file/component relationships**:

```text
Rule 1: Project Structure Dependencies
  - T002 (initialize project) depends on T001 (project structure)
  - All other tasks depend on T002

Rule 2: Database Dependencies
  - Service tasks depend on Model tasks for same entity
  - Example: UserService [DEP:UserModel]

Rule 3: API Dependencies
  - Endpoint tasks depend on Service tasks
  - Example: /users endpoint [DEP:UserService]

Rule 4: Test Dependencies
  - Test tasks depend on implementation tasks they test
  - Example: test_registration [DEP:UserService, UserEndpoint]

Rule 5: Cross-Story Dependencies
  - If US2 uses entity from US1, add [DEP:] to US1's model task
  - Prefer minimal cross-story dependencies to maintain independence

Rule 6: Foundation to Story Dependencies
  - All story tasks implicitly depend on Phase 2 completion
  - Explicit [DEP:] only needed for specific foundational tasks
```

**Circular Dependency Detection**:

```text
Build directed graph from [DEP:] markers
Run topological sort
If cycle detected:
  - Report cycle path: T005 → T012 → T014 → T005
  - Suggest resolution: Remove weakest dependency
  - Block tasks.md generation until resolved
```

### FR/AS Mapping Logic

**Linking tasks to requirements**:

```text
FOR EACH implementation task:
  1. Identify which FR(s) this task fulfills:
     - Model tasks → FR about data entities
     - Service tasks → FR about business logic
     - Endpoint tasks → FR about user interactions
  2. Add [FR:FR-xxx] marker(s)

FOR EACH test task:
  1. Identify which AS this test verifies:
     - Match test description to AS Given/When/Then
     - One test may verify multiple AS (if closely related)
  2. Add [TEST:AS-xxx] marker
```

### Traceability Validation Rules

Before completing tasks.md generation, validate:

```text
1. FR Coverage:
   FOR EACH FR in spec.md:
     - At least one task has [FR:FR-xxx] marker
     - If no task found: Add to "Gaps Identified"

2. AS Coverage (if tests requested):
   FOR EACH AS in spec.md:
     - At least one test task has [TEST:AS-xxx] marker
     - If no test found: Add to "Gaps Identified"

3. Orphan Task Check:
   FOR EACH implementation task in User Story phase:
     - Task has at least one [FR:] marker
     - If no FR link: Warning "Task T0xx has no FR link"

4. Dependency Validity:
   FOR EACH [DEP:Txxx] reference:
     - Txxx exists in tasks.md
     - Txxx appears before current task
     - No circular dependencies
```

## Automation Behavior

When this command completes successfully, the following automation rules apply:

### Auto-Transitions

| Condition | Next Phase | Gate |
|-----------|------------|------|
| tasks.md generated, valid structure, P1 tasks defined, no circular deps | `/speckit.implement` | Tasks Ready Gate, Dependency Validity Gate |

### Quality Gates

| Gate | Check | Block Condition | Message |
|------|-------|-----------------|---------|
| Tasks Generated Gate | tasks.md created with valid structure | tasks.md missing or malformed | "Tasks must be generated before analysis" |
| Tasks Ready Gate | All P1 tasks have file paths and dependencies defined | P1 tasks missing file paths or invalid [DEP:] references | "Ensure all P1 tasks are fully specified before implementation" |
| Dependency Validity Gate | No circular dependencies in task graph | Circular dependency detected | "Resolve circular dependencies before proceeding" |

### Gate Behavior

**If all conditions pass and no gates block:**
- Automatically proceed to `/speckit.implement` with the generated tasks
- Log transition for audit trail

**If gates block:**
- Display blocking message to user
- List specific issues (missing file paths, circular dependencies, etc.)
- Wait for user to resolve issues
- Offer handoff to `/speckit.analyze` for thorough validation

### Manual Overrides

Users can always choose to:
- Run `/speckit.analyze` first to validate traceability and consistency
- Skip automation by selecting a different handoff option
- Return to `/speckit.plan` if tasks reveal planning gaps
- Run `/speckit.tasks` again to regenerate with updated plan

---

## Self-Review Phase (MANDATORY)

**Before declaring tasks.md complete, you MUST perform self-review.**

Read `templates/shared/self-review/framework.md` for the unified self-review system.
Read `templates/shared/validation/checkpoints.md` for streaming validation during generation.

This ensures the generated tasks are valid, traceable, and ready for implementation.

### Framework Integration

Apply the self-review framework with:
- `COMMAND` = "tasks"
- `ARTIFACT` = `FEATURE_DIR/tasks.md`
- `CRITERIA_FILE` = criteria below (SR-TASK-01 to SR-TASK-10)
- `COMPLEXITY_TIER` = from complexity-scoring.md (determined in Step 0)
- `MAX_ITERATIONS` = 3

### Step 1: Re-read Generated Artifact

Read the tasks.md file you just created:
- `FEATURE_DIR/tasks.md`

Parse the file to extract:
- All task IDs (T001, T002, ...)
- All [DEP:] references
- All [FR:] markers
- All [TEST:] markers
- RTM table entries

### Step 2: Quality Criteria

Apply criteria based on complexity tier (from framework.md):

| Tier | Active Criteria |
|------|-----------------|
| TRIVIAL | SR-TASK-01, SR-TASK-07, SR-TASK-08 only |
| SIMPLE | SR-TASK-01 to SR-TASK-06 |
| MODERATE | All SR-TASK-01 to SR-TASK-10 |
| COMPLEX | All + cross-artifact validation |

**Full Criteria (for MODERATE/COMPLEX):**

| ID | Criterion | Check | Severity |
|----|-----------|-------|----------|
| SR-TASK-01 | Task Format Valid | Every task line starts with `- [ ] T###` pattern | CRITICAL |
| SR-TASK-02 | Task IDs Sequential | T001, T002, T003... with no gaps or duplicates | HIGH |
| SR-TASK-03 | File Paths Present | Implementation tasks include file paths | HIGH |
| SR-TASK-04 | Story Labels Valid | User story phase tasks have [US#] markers | MEDIUM |
| SR-TASK-05 | FR Coverage Complete | Every FR-xxx from spec.md has at least one [FR:FR-xxx] task | CRITICAL |
| SR-TASK-06 | AS Coverage Complete | Every AS-xxx from spec.md has at least one [TEST:AS-xxx] task (if tests requested) | HIGH |
| SR-TASK-07 | DEP References Valid | All [DEP:T###] reference existing task IDs | CRITICAL |
| SR-TASK-08 | No Circular Dependencies | Dependency graph has no cycles | CRITICAL |
| SR-TASK-09 | RTM Table Complete | Requirements Traceability Matrix lists all FRs with linked tasks | MEDIUM |
| SR-TASK-10 | Coverage Summary Present | Coverage Summary section shows FR/AS coverage stats | MEDIUM |

### Step 3: Dependency Validation

Build dependency graph and validate:

```text
TASK_GRAPH = {}
ALL_TASK_IDS = set()

FOR EACH task in tasks.md:
  Extract task_id (e.g., T001)
  ALL_TASK_IDS.add(task_id)

  Extract dep_list from [DEP:T###,T###]
  FOR EACH dep_id in dep_list:
    IF dep_id NOT IN ALL_TASK_IDS (defined before current):
      ERROR: "Task {task_id} references undefined dependency {dep_id}"
    TASK_GRAPH[task_id].depends_on(dep_id)

# Detect cycles using topological sort
IF topological_sort(TASK_GRAPH) fails:
  Extract cycle path
  ERROR: "Circular dependency detected: {cycle_path}"
```

### Step 4: Traceability Validation

Cross-reference with spec.md:

```text
# Load from spec.md (already parsed in Step 3 of main workflow)
FR_LIST = [FR-001, FR-002, ...]
AS_LIST = [AS-1A, AS-1B, ...]

# Extract from tasks.md
TASK_FR_MARKERS = extract all [FR:FR-xxx] references
TASK_AS_MARKERS = extract all [TEST:AS-xxx] references

# Validate FR coverage
FOR EACH fr in FR_LIST:
  IF fr NOT IN TASK_FR_MARKERS:
    WARN: "FR {fr} has no implementation task"
    Add to gaps

# Validate AS coverage (if tests requested)
FOR EACH as in AS_LIST:
  IF as NOT IN TASK_AS_MARKERS:
    WARN: "AS {as} has no test task"
    Add to gaps
```

### Step 5: Verdict

Apply verdict logic from `templates/shared/self-review/framework.md`:

```text
CALCULATE_VERDICT(check_results):
  - CRITICAL failures → FAIL (must fix)
  - 2+ HIGH failures → WARN
  - 4+ MEDIUM failures → WARN
  - Quality score >= 80% → PASS
```

**Task-specific fix guidance:**
- **FAIL**: Any CRITICAL issue → self-correct and re-check (max 3 iterations)
  - Missing FR coverage → add missing [FR:] markers to appropriate tasks
  - Invalid DEP references → fix task IDs or add missing tasks
  - Circular dependency → break the cycle by removing weakest dependency
- **WARN**: Only MEDIUM issues (missing story labels, incomplete RTM) → show warnings, proceed
- **PASS**: All CRITICAL criteria pass, no circular dependencies, FR coverage complete → proceed to handoff

### Step 6: Self-Correction Loop

```text
IF issues found AND iteration < 3:
  1. Fix each issue in tasks.md:
     - Add missing [FR:] markers
     - Fix [DEP:] references
     - Break circular dependencies
     - Add missing tasks for uncovered FRs
     - Complete RTM table
  2. Re-run self-review from Step 1
  3. Report: "Self-review iteration {N}: Fixed {issues}, re-validating..."

IF still failing after 3 iterations:
  - STOP
  - Report blocking issues to user
  - Do NOT auto-transition to /speckit.implement
```

### Step 7: Self-Review Report

After passing self-review, output:

```text
## Self-Review Complete ✓

**Artifact**: FEATURE_DIR/tasks.md
**Iterations**: {N}

### Validation Results

| Check | Result |
|-------|--------|
| Task Format | ✓ All {N} tasks follow format |
| Task IDs | ✓ Sequential T001-T{N} |
| Dependencies | ✓ {N} valid, 0 circular |
| FR Coverage | ✓ {N}/{M} FRs have [FR:] tasks |
| AS Coverage | ✓ {N}/{M} ASs have [TEST:] tasks |
| RTM Complete | ✓ {N} rows |

### Coverage Summary

- **Functional Requirements**: {covered}/{total} ({percentage}%)
- **Acceptance Scenarios**: {covered}/{total} ({percentage}%)
- **Gaps Identified**: {count}

{IF gaps exist:}
### Gaps (documented in Coverage Summary section)
- FR-xxx: No implementation task
- AS-xxx: No test task

### Ready for Implementation

All quality gates passed. Auto-transitioning to `/speckit.implement`.
```

### Common Task Generation Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| Missing checkbox | Task doesn't start with `- [ ]` | Prepend `- [ ]` to task line |
| Missing task ID | No T### pattern after checkbox | Add sequential T### ID |
| Orphan FR | FR-xxx not in any [FR:] marker | Add [FR:FR-xxx] to most relevant task |
| Dangling DEP | [DEP:T999] references non-existent task | Remove invalid reference or add missing task |
| Cycle detected | Topological sort fails | Remove one edge to break cycle |
| Missing file path | Implementation task has no path | Add target file path to description |
| Wrong story label | [US5] but only 3 user stories | Fix to match spec.md story numbers |

---

## Output Phase

Read `templates/shared/output/progressive-modes.md` and apply.
Read `templates/shared/traceability/artifact-registry.md` and apply.

### Determine Output Mode

```text
MODE = SELECT_OUTPUT_MODE(COMPLEXITY_TIER, user_flags)

# COMPACT for TRIVIAL/SIMPLE
# STANDARD for MODERATE (default)
# DETAILED for COMPLEX or --verbose
```

### Generate Quick Summary

Always output the Quick Summary first, regardless of mode:

```markdown
# Task Breakdown Complete

## Quick Summary

| Aspect | Value |
|--------|-------|
| **Feature** | {feature_name} |
| **Complexity** | {COMPLEXITY_TIER} ({complexity_score}/100) |
| **Total Tasks** | {task_count} tasks |
| **By Story** | {story_1}: {n} tasks, {story_2}: {m} tasks |
| **Parallel Opportunities** | {parallel_count} tasks can run in parallel |
| **FR Coverage** | {fr_covered}/{fr_total} ({fr_pct}%) |
| **AS Coverage** | {as_covered}/{as_total} ({as_pct}%) |
| **Status** | {status_badge} |
| **Next Step** | {next_step} |

### Task Distribution

| Story | Tasks | Priority Range |
|-------|-------|----------------|
| US1: {story_name} | {count} | P1-P2 |
| US2: {story_name} | {count} | P2-P3 |

### MVP Scope (Story 1)

- T001: {brief_description}
- T002: {brief_description}
- T003: {brief_description}
```

### Format Full Content

```text
IF MODE == COMPACT:
  OUTPUT: Quick Summary (above)
  OUTPUT: <details><summary>📄 View Full Task List</summary>
  OUTPUT: {full_tasks_content}
  OUTPUT: </details>

ELIF MODE == STANDARD:
  OUTPUT: Quick Summary (above)
  OUTPUT: ---
  OUTPUT: {full_tasks_content with collapsible RTM}

ELIF MODE == DETAILED:
  OUTPUT: Quick Summary (above)
  OUTPUT: ---
  OUTPUT: {full_tasks_content all sections expanded}
  OUTPUT: ---
  OUTPUT: {self_review_report}
  OUTPUT: {dependency_graph_visualization}
```

### Update Artifact Registry

```text
Read `templates/shared/traceability/artifact-registry.md` and apply:

UPDATE_REGISTRY("tasks", "FEATURE_DIR/tasks.md", {
  parent_plan_version: registry.artifacts.plan.version,
  parent_spec_version: registry.artifacts.spec.version,
  task_count: {task_count},
  fr_coverage: {covered: fr_covered, total: fr_total, percentage: fr_pct},
  as_coverage: {covered: as_covered, total: as_total, percentage: as_pct}
})

OUTPUT: "Artifact registry updated. Full traceability chain established."
```

### Traceability Chain Complete

When tasks.md is generated, the full traceability chain is established:

```text
concept.md (if exists)
    └── spec.md (v{spec_version})
        └── plan.md (v{plan_version})
            └── tasks.md (v{tasks_version})

Registry Status:
- All parent versions recorded
- Checksums calculated
- Staleness detection enabled
```
