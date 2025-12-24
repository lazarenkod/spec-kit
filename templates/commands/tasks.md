---
description: Generate an actionable, dependency-ordered tasks.md with full traceability to spec requirements and acceptance scenarios.
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
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Parse Traceability IDs from spec.md**:

   ```
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

   ```
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

   ```
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

   ```
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
   ```
   MANIFEST_FILE = specs/features/.manifest.md
   FEATURE_ID = extract from current branch/feature (first 3 digits)

   IF exists(MANIFEST_FILE):
     Find row where ID = FEATURE_ID
     Update Status column: PLANNED → TASKED
     Update "Last Updated" column: today's date
   ```

10. **Report**: Output path to generated tasks.md and summary:
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

```
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

```
Build directed graph from [DEP:] markers
Run topological sort
If cycle detected:
  - Report cycle path: T005 → T012 → T014 → T005
  - Suggest resolution: Remove weakest dependency
  - Block tasks.md generation until resolved
```

### FR/AS Mapping Logic

**Linking tasks to requirements**:

```
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

```
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
