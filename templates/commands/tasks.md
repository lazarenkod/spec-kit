---
description: Generate an actionable, dependency-ordered tasks.md with full traceability to spec requirements and acceptance scenarios.
persona: decomposer-agent
handoff:
  requires: handoffs/plan-to-tasks.md
  generates: handoffs/tasks-to-implement.md
  template: templates/handoff-template.md
inline_gates:
  enabled: true
  skip_flag: "--skip-gates"
  strict_flag: "--strict-gates"
  full_flag: "--full-gates"
  mode: progressive
  on_failure: block
  gates:
    - id: IG-TASK-001
      name: "Dependency Graph Valid"
      pass: G
      tier: 1
      threshold: 0
      severity: CRITICAL
      message: "Circular dependencies detected in task graph"
    - id: IG-TASK-002
      name: "FR Coverage"
      pass: H
      tier: 2
      threshold: 0
      severity: HIGH
      message: "Functional requirements without implementation tasks"
    - id: IG-TASK-003
      name: "RTM Validity"
      pass: J
      tier: 2
      threshold: 0
      severity: MEDIUM
      message: "Requirements Traceability Matrix inconsistent"
    - id: IG-TASK-004
      name: "Test Coverage"
      ref: QG-TEST-001
      tier: 2
      threshold: 0
      severity: HIGH
      message: "Acceptance scenarios missing test tasks"
handoffs:
  - label: Full Audit (Optional)
    agent: speckit.analyze
    prompt: Run comprehensive project analysis with full profile
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
      - "Inline gates passed (IG-TASK-*)"
    gates:
      - name: "Tasks Ready Gate"
        check: "All P1 tasks have file paths and dependencies defined"
        block_if: "P1 tasks missing file paths or have invalid [DEP:] references"
        message: "Ensure all P1 tasks are fully specified before implementation"
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
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 6000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
      pro:
        thinking_budget: 12000
        max_parallel: 4
        batch_delay: 4000
        wave_overlap_threshold: 0.80
      max:
        thinking_budget: 24000
        max_parallel: 8
        batch_delay: 1500
        wave_overlap_threshold: 0.65
  cache_control:
    system_prompt: ephemeral
    constitution: ephemeral
    templates: ephemeral
    artifacts: ephemeral
    ttl: session
  semantic_cache:
    enabled: true
    encoder: all-MiniLM-L6-v2
    similarity_threshold: 0.95
    cache_scope: session
    cacheable_fields: [user_input, feature_description]
    ttl: 3600
  cache_hierarchy: full
  orchestration:
    max_parallel: 8
    role_isolation: true
  operation_batching:
    enabled: true
    skip_flag: "--sequential"
    framework: templates/shared/operation-batching.md
    strategies:
      context_reads: true    # Batch context file reads
      prefetch: true         # Speculative parallel load
      validations: true      # Batch inline gate checks
    subagent_batching:
      enabled: true
      parallel_mappers: [dependency-analyzer, fr-mapper]  # Run in parallel
      sequential_mappers: [as-mapper]                     # Depends on fr-mapper
  artifact_extraction:
    enabled: true
    skip_flag: "--full-context"
    framework: templates/shared/artifact-extraction.md
    spec_fields:
      - fr_list           # FR-001, FR-002, ...
      - as_list           # AS-1A, AS-1B, ...
      - ec_list           # EC-001, EC-002, ...
      - story_priorities  # {US1: P1a, ...}
      - component_registry
      - fr_summaries      # [{id, summary}, ...]
      - as_summaries      # [{id, name}, ...]
    plan_fields:
      - tech_stack
      - dependencies
      - phases
      - adr_decisions
  subagents:
    - role: dependency-analyzer
      role_group: INFRA
      parallel: true
      depends_on: []
      priority: 9
      trigger: "when analyzing task dependencies and build order"
      context_injection: extracted  # Use PLAN_DATA instead of full plan.md
      prompt: |
        Analyze dependencies between components to determine optimal task ordering.

        Phases: {PLAN_DATA.phases}
        Dependencies: {PLAN_DATA.dependencies}
        ADR Decisions: {PLAN_DATA.adr_decisions}
      model_override: haiku
    - role: fr-mapper
      role_group: BACKEND
      parallel: true
      depends_on: []
      priority: 8
      trigger: "when mapping functional requirements to implementation tasks"
      context_injection: extracted  # Use SPEC_DATA instead of full spec.md
      prompt: |
        Map functional requirements to concrete implementation tasks.

        FR List ({len(SPEC_DATA.fr_list)} items):
        {format_as_list(SPEC_DATA.fr_summaries)}

        Tech Stack: {PLAN_DATA.tech_stack}
        Story Priorities: {SPEC_DATA.story_priorities}
    - role: as-mapper
      role_group: TESTING
      parallel: true
      depends_on: [fr-mapper]
      priority: 7
      trigger: "when mapping acceptance scenarios to test tasks"
      context_injection: extracted  # Use SPEC_DATA instead of full spec.md
      prompt: |
        Map acceptance scenarios to test implementation tasks.

        AS List ({len(SPEC_DATA.as_list)} items):
        {format_as_list(SPEC_DATA.as_summaries)}

        EC List: {SPEC_DATA.ec_list}
        FR-to-Task mapping from fr-mapper: {FR_MAPPER_OUTPUT}
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

0. **Prefetch Phase** [REF:PF-001]:

   **Speculative parallel load** of all potentially-needed files BEFORE any conditional logic:

   ```text
   # PREFETCH BATCH (single message, all Read calls in parallel)
   Read IN PARALLEL:
   - `memory/constitution.md`
   - `templates/tasks-template.md`
   - `templates/shared/core/language-loading.md`
   - `templates/shared/complexity-scoring.md`
   - `templates/shared/core/brownfield-detection.md`
   - `specs/concept.md` (if exists)
   - `FEATURE_DIR/spec.md` (required - will be resolved after script runs)
   - `FEATURE_DIR/plan.md` (required - will be resolved after script runs)

   CACHE all results with session lifetime.
   REPORT: "Prefetched {N} files in {T}ms"
   ```

   **Artifact Extraction** (reduces subagent context by ~95%):

   ```text
   IF artifact_extraction.enabled AND NOT "--full-context" IN ARGS:

     IMPORT: templates/shared/artifact-extraction.md

     # Extract structured data from artifacts
     SPEC_DATA = EXTRACT_SPEC(FEATURE_DIR/spec.md)
     PLAN_DATA = EXTRACT_PLAN(FEATURE_DIR/plan.md)
     CONCEPT_DATA = EXTRACT_CONCEPT(specs/concept.md)  # May be null

     PRINT "📊 Artifact extraction complete:"
     PRINT "├── spec: {len(SPEC_DATA.fr_list)} FRs, {len(SPEC_DATA.as_list)} ASs, {len(SPEC_DATA.ec_list)} ECs"
     PRINT "├── plan: {len(PLAN_DATA.phases)} phases, {len(PLAN_DATA.adr_decisions)} ADRs"
     PRINT "└── Context reduction: ~{SPEC_DATA._original_size_kb + PLAN_DATA._original_size_kb}KB → ~15KB"

     # Store for subagent injection
     SESSION_CACHE["SPEC_DATA"] = SPEC_DATA
     SESSION_CACHE["PLAN_DATA"] = PLAN_DATA

   ELSE:
     LOG "⚠️ Full context mode: using complete artifacts (higher token usage)"
   ```

1. **Load project context**:

   Execute prefetched modules (already in cache from Step 0):

   ```text
   # Execute cached modules
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

3.5. **Detect UI Test Requirements** [REF:UI-DETECT-001]:

   For each acceptance scenario (AS-xxx), determine if it requires UI testing:

   ```text
   UI_AS_LIST = []
   UI_KEYWORDS = {
     actions: ["click", "tap", "press", "swipe", "scroll", "drag", "type", "select", "submit"],
     elements: ["button", "form", "input", "textfield", "dropdown", "modal", "dialog",
                "checkbox", "radio", "toggle", "slider", "menu", "navbar", "toolbar"],
     states: ["visible", "hidden", "disabled", "enabled", "selected", "checked", "focused"],
     mobile: ["screen", "view", "activity", "fragment", "navigation"],
     web: ["page", "link", "href", "route"]
   }

   FOR EACH as IN AS_LIST:
     # Parse AS content from spec.md
     as_content = EXTRACT_AS_CONTENT(spec.md, as.id)

     # Check for UI keywords
     has_ui_keywords = false
     FOR EACH category IN UI_KEYWORDS:
       FOR EACH keyword IN UI_KEYWORDS[category]:
         IF keyword IN as_content.lower():
           has_ui_keywords = true
           BREAK

     # Tag AS with UI requirement
     IF has_ui_keywords:
       UI_AS_LIST.append({
         id: as.id,
         requires_ui_test: true,
         detected_keywords: [found keywords],
         platform: DETECT_PLATFORM()  # See platform detection below
       })

   # Platform Detection
   DETECT_PLATFORM():
     platforms = []

     # Web detection
     IF package.json contains "react" OR "vue" OR "angular" OR "svelte":
       platforms.append("web")
       framework = "playwright"  # Default for web

     # Mobile detection
     IF EXISTS Xcode project (*.xcodeproj):
       platforms.append("ios")
       framework = "xcuitest"

     IF EXISTS build.gradle with "android":
       platforms.append("android")
       framework = "espresso"

     IF package.json contains "react-native":
       platforms.append("ios", "android")
       framework = "detox"  # Cross-platform

     IF EXISTS pubspec.yaml (Flutter):
       platforms.append("ios", "android")
       framework = "flutter_test"

     IF EXISTS build.gradle.kts with kotlin("multiplatform"):
       platforms.append("ios", "android")
       framework = "maestro"

     # Desktop detection
     IF package.json contains "electron":
       platforms.append("desktop_electron")
       framework = "playwright-electron"

     IF EXISTS src-tauri/ directory:
       platforms.append("desktop_tauri")
       framework = "tauri-webdriver"

     RETURN {
       platforms: platforms,
       framework: framework
     }

   # Generate UI test requirement table
   IF len(UI_AS_LIST) > 0:
     OUTPUT """
     ## UI Test Requirements Detected

     {len(UI_AS_LIST)} acceptance scenarios require E2E UI testing.

     | AS ID | Detected Keywords | Platform | Framework |
     |-------|-------------------|----------|-----------|
     """
     FOR EACH ui_as IN UI_AS_LIST:
       OUTPUT "| {ui_as.id} | {ui_as.detected_keywords} | {ui_as.platform.platforms} | {ui_as.platform.framework} |"

     STORE: "UI_AS_LIST" for use in test task generation (Step 4)
   ELSE:
     OUTPUT "No UI testing requirements detected."
   ```

   **Output**: UI_AS_LIST with platform and framework metadata for E2E test generation.

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

4.5. **Generate Component Wire Tasks** *(for UI features with Component Registry)*:

   ```text
   IF spec.md contains "## UI Component Registry" section:

     # Step 1: Parse Component Registry
     COMPONENT_REGISTRY = []
     FOR EACH row in "UI Component Registry" table:
       comp = {
         id: row.ID,           # e.g., COMP-001
         name: row.Component,  # e.g., FontSizeSliderView
         type: row.Type,       # e.g., Control
         target_screens: parse_csv(row["Target Screens"]),  # e.g., [Settings, ReaderOverlay]
         priority: row.Priority,
         vr_ir_refs: row["VR/IR Refs"]
       }
       COMPONENT_REGISTRY.append(comp)

     # Step 2: Parse Screen Registry
     SCREEN_REGISTRY = []
     FOR EACH row in "Screen Registry" table:
       screen = {
         id: row.ID,           # e.g., SCR-001
         name: row.Screen,     # e.g., Settings
         type: row.Type,       # e.g., Page
         route: row["Route/Navigation"],
         required_components: parse_csv(row["Required Components"])  # e.g., [COMP-001, COMP-002]
       }
       SCREEN_REGISTRY.append(screen)

     # Step 3: Generate Component Creation Tasks (for Phase 2b)
     FOR EACH comp IN COMPONENT_REGISTRY:
       IF NOT exists task with [COMP:{comp.id}]:
         GENERATE task:
           ID: T{next_id}
           Markers: [P] [COMP:{comp.id}] [VR:{comp.vr_ir_refs}]
           Description: "Create {comp.name} in {inferred_path}"
           Subtask: "- **Target Screens**: {comp.target_screens.join(', ')}"
           Subtask: "- **Type**: {comp.type}"

     # Step 4: Generate Screen Implementation Tasks (for story phases)
     FOR EACH screen IN SCREEN_REGISTRY:
       IF NOT exists task with [SCREEN:{screen.id}]:
         GENERATE task:
           ID: T{next_id}
           Markers: [SCREEN:{screen.id}] [DEP:foundation_tasks]
           Description: "Create {screen.name} in {inferred_path}"
           Subtask: "- **Route**: {screen.route}"
           Subtask: "- **Required Components**: {screen.required_components.join(', ')}"

     # Step 5: Generate Wire Tasks (CRITICAL for integration)
     WIRE_TASKS = []
     FOR EACH comp IN COMPONENT_REGISTRY:
       FOR EACH screen_name IN comp.target_screens:
         screen = FIND screen IN SCREEN_REGISTRY WHERE screen.name == screen_name
         IF screen:
           comp_task = FIND task with [COMP:{comp.id}]
           screen_task = FIND task with [SCREEN:{screen.id}]

           wire_task = {
             ID: T{next_id},
             Markers: "[WIRE:{comp.id}→{screen.id}] [DEP:{comp_task.id},{screen_task.id}]",
             Description: "Wire {comp.name} into {screen.name}",
             Subtasks: [
               "- **Component File**: {comp_task.file_path}",
               "- **Screen File**: {screen_task.file_path}",
               "- **Action**: Import component, replace placeholder",
               "- **Verify**: Component renders, is functional in {screen.name}"
             ]
           }
           WIRE_TASKS.append(wire_task)

     # Step 6: Generate CSIM Matrix
     CSIM_ROWS = []
     FOR EACH wire_task IN WIRE_TASKS:
       row = {
         comp_id: wire_task.comp_id,
         comp_name: wire_task.comp_name,
         screen_id: wire_task.screen_id,
         screen_name: wire_task.screen_name,
         wire_task_id: wire_task.ID,
         deps: wire_task.deps,
         status: "[ ]"
       }
       CSIM_ROWS.append(row)

     # Step 7: Validate Coverage (QG-COMP-002)
     EXPECTED_PAIRS = len(COMPONENT_REGISTRY) × avg(len(comp.target_screens))
     ACTUAL_PAIRS = len(WIRE_TASKS)

     IF ACTUAL_PAIRS < EXPECTED_PAIRS:
       ERROR: "QG-COMP-002 FAILED: CSIM coverage {ACTUAL_PAIRS}/{EXPECTED_PAIRS}"
       FOR EACH missing_pair:
         ERROR: "  Missing wire: {comp.id} → {screen.id}"
     ELSE:
       OUTPUT: "QG-COMP-002 PASSED: {ACTUAL_PAIRS} wire tasks for {len(COMPONENT_REGISTRY)} components"

   ELSE:
     SKIP: "No Component Registry found - skipping wire task generation"
   ```

   **Output**: Component-Screen Integration Matrix (CSIM) section added to tasks.md after RTM.

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

   **Cache generated content for Self-Review** (avoids re-reading file):

   ```text
   tasks_content = BUILD_TASKS_CONTENT(...)  # Assembled content
   WRITE(FEATURE_DIR/tasks.md, tasks_content)

   # Cache for Self-Review phase (saves ~50-100KB read)
   SESSION_CACHE["GENERATED_TASKS_CONTENT"] = tasks_content
   LOG "📦 Cached tasks.md content for self-review ({len(tasks_content)} chars)"
   ```

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

**Tests are REQUIRED**: Generate test tasks for ALL acceptance scenarios. This is mandatory for TDD workflow.

- Every AS-xxx with "Requires Test = YES" MUST have a corresponding [TEST:AS-xxx] task
- Test tasks MUST appear BEFORE implementation tasks in each story phase
- No `--skip-tests` flag is available - tests are always generated
- Quality Gate QG-TEST-001 blocks if any AS lacks a test task

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

**UX-Specific Markers** *(for UI features)*:

8. **[STATE-TEST:COMP-xxx:state]**: Links UI state test to component and state
   - Format: `[STATE-TEST:COMP-001:loading]` tests loading state of COMP-001
   - States: default, loading, error, success, empty, disabled
   - Generated from UI State Matrix in spec.md

9. **[RWD-TEST:SCR-xxx:viewport]**: Links responsive layout test to screen and viewport
   - Format: `[RWD-TEST:SCR-001:mobile]` tests mobile layout of SCR-001
   - Viewports: mobile, tablet, desktop
   - Generated from Responsive Acceptance Scenarios

10. **[INT-TEST:AS-INT-xxx]**: Links interaction/animation test to interaction scenario
    - Format: `[INT-TEST:AS-INT-001]` tests specific interaction transition
    - Tests timing, easing, and state changes

11. **[E2E:journey-name]**: End-to-end user journey test
    - Format: `[E2E:login-to-dashboard]` tests complete user flow
    - Generated from User Journey sections in design.md

12. **[VRT:baseline|compare]**: Visual regression test task
    - `[VRT:baseline]` captures baseline screenshots
    - `[VRT:compare]` compares against baseline
    - Used with Playwright/Percy/Chromatic

13. **[A11Y-AUDIT]**: Accessibility audit task
    - Runs axe-core, Lighthouse accessibility checks
    - Validates WCAG compliance level from spec.md

14. **[DS-AUDIT]**: Design system compliance audit
    - Checks token usage (hardcoded colors, spacing)
    - Validates component usage patterns

15. **[TOUCH:gesture]**: Mobile gesture test
    - Format: `[TOUCH:swipe-left]`, `[TOUCH:long-press]`, `[TOUCH:pinch]`
    - Tests mobile-specific interactions

16. **Description**: Clear action with exact file path

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

---

## Task Clarity Requirements

**Purpose**: Ensure tasks are **immediately executable** by weak LLMs (Claude Haiku, GPT-3.5) without requiring additional context or interpretation.

**Core Principle**: Tasks must contain **concrete details**, not placeholders or generic terms. Every task should specify exact file paths, method names, parameters, and test scenarios extracted from spec.md and plan.md.

### Forbidden Patterns

The following patterns are **strictly prohibited** in task descriptions:

| Pattern | Example | Why Forbidden | Extract From |
|---------|---------|---------------|--------------|
| **Placeholder brackets** | `[Entity1]`, `[Entity2]`, `[Service]` | Requires context to resolve | spec.md Domain Model |
| **Generic entity refs** | `[Component]`, `[Model]`, `[Controller]` | Ambiguous, not specific | spec.md UI Components / plan.md Architecture |
| **Vague scenarios** | `[scenario description]`, `[test case]` | No actionable detail | spec.md AS-xxx scenarios |
| **Missing HTTP details** | `[HTTP method]`, `[endpoint]` | Incomplete API specification | spec.md API Requirements |
| **Generic method names** | `[method_name]()`, `[function]()` | No implementation guidance | plan.md Architecture |
| **Placeholder paths** | `src/models/[entity].py` | Cannot create file | Derive from entity name |
| **Generic terms** | "relevant", "appropriate", "necessary" | Subjective, requires judgment | Specify exact requirement |

### Five Extraction Algorithms

Use these algorithms to extract concrete details from spec.md and plan.md:

#### Algorithm 1: Model/Entity Extraction

**Input**: spec.md Domain Model section
**Output**: Entity name + fields with types

**Example**:

```text
FROM spec.md Domain Model:
**User** entity with fields:
- id: UUID (primary key)
- email: string (unique, indexed)
- password_hash: string
- created_at: timestamp
- updated_at: timestamp

GENERATE TASK:
✅ Create User model in src/models/user.py with fields: id (UUID), email (unique, indexed), password_hash, created_at, updated_at

❌ NOT: Create [Entity1] model in src/models/[entity1].py
```

**Fallback**: If fields not specified → use ⚠️ warning:
```
⚠️ Create User model in src/models/user.py (fields not specified in spec, using common defaults: id, created_at, updated_at)
```

---

#### Algorithm 2: Service/Business Logic Extraction

**Input**: plan.md Architecture or spec.md Functional Requirements
**Output**: Service name + specific methods with signatures

**Example**:

```text
FROM plan.md Architecture:
**UserService** (src/services/user_service.py):
- register(email: string, password: string) → userId: UUID
- authenticate(email: string, password: string) → token: string
- resetPassword(email: string) → void

GENERATE TASK:
✅ Implement UserService in src/services/user_service.py with methods: register(email, password) returns userId, authenticate(email, password) returns token, resetPassword(email) sends reset link

❌ NOT: Implement [Service] in src/services/[service].py
```

**Fallback**: If methods not specified → extract from FR:
```
✅ Implement UserService in src/services/user_service.py with CRUD operations for User entity (FR-001, FR-002)
```

---

#### Algorithm 3: API Endpoint Extraction

**Input**: spec.md API Requirements / Contracts
**Output**: HTTP method + path + handler + expected I/O

**Example**:

```text
FROM spec.md API Requirements:
**POST /api/v1/auth/register**
- Handler: register_user()
- Request: { email: string, password: string }
- Response: { userId: UUID, token: string }
- Status: 201 Created

GENERATE TASK:
✅ Implement POST /api/v1/auth/register endpoint in src/api/auth.py with register_user() handler (expects: email, password; returns: userId, token; status: 201)

❌ NOT: Implement [HTTP method] [endpoint] in src/api/[module].py
```

**Fallback**: If handler name missing → derive from endpoint:
```
✅ Implement POST /api/v1/auth/register endpoint in src/api/auth.py with handler (expects: email, password; returns: userId, token)
```

---

#### Algorithm 4: Test Scenario Extraction

**Input**: spec.md Acceptance Scenarios (AS-xxx)
**Output**: GIVEN/WHEN/THEN → specific test with concrete values

**Example**:

```text
FROM spec.md AS-001:
**AS-001: User can register with valid email**
GIVEN: valid email "<test@example.com>" and strong password "SecurePass123!"
WHEN: POST /api/v1/auth/register
THEN: returns 201 status, userId in response, confirmation email sent to <test@example.com>

GENERATE TASK:
✅ [TEST:AS-001] Test user registration with valid email (<test@example.com>, SecurePass123!) expects 201 status, userId in response, and confirmation email sent

❌ NOT: Test [scenario description] with [test type]
```

**Test Types**: Map from AS context:
- Unit test: Service/model logic scenarios
- Integration test: API endpoint scenarios
- E2E test: User journey scenarios

**Fallback**: If test values missing → use realistic defaults with ⚠️:
```
⚠️ [TEST:AS-001] Test user registration with valid email (<test@example.com>, default password) expects 201 status (concrete values not in spec, using defaults)
```

---

#### Algorithm 5: UI Component Extraction

**Input**: spec.md UI Components / design.md
**Output**: Component name + props + states

**Example**:

```text
FROM spec.md UI Components:
**LoginForm** component (src/components/LoginForm.tsx):
- Props: onSubmit (function), initialEmail (string, optional)
- States: isLoading (boolean), errorMessage (string|null), isPasswordVisible (boolean)
- Events: handleSubmit, togglePasswordVisibility

GENERATE TASK:
✅ Create LoginForm component in src/components/LoginForm.tsx with props (onSubmit, initialEmail) and states (isLoading, errorMessage, isPasswordVisible)

❌ NOT: Create [Component] component in src/components/[component].tsx
```

**Fallback**: If props/states not specified → extract from FR/AS:
```
✅ Create LoginForm component in src/components/LoginForm.tsx with authentication functionality (FR-001) - props and states derived from login flow requirements
```

---

### Tiered Fallback Strategy

When extraction algorithms cannot find complete details:

#### Tier 1: 1-2 Missing Details → Reasonable Defaults with ⚠️

Apply when most details are present but minor elements are missing.

**Actions**:
- Use reasonable defaults based on domain knowledge
- Add ⚠️ warning prefix to task
- Document assumption in parentheses
- Continue with task generation

**Examples**:

```markdown
⚠️ Create User model in src/models/user.py (fields not specified, using: id, email, created_at, updated_at)

⚠️ Implement UserService in src/services/user_service.py with CRUD operations (method signatures not specified, deriving from FR-001, FR-002)

⚠️ [TEST:AS-001] Test registration with valid email (<test@example.com>) expects 201 status (test password not specified, using: SecurePass123!)
```

**When to Use**:
- Missing: field types, method return types, test input values
- Present: entity names, file paths, core functionality
- Context: Enough spec detail to infer reasonable defaults

---

#### Tier 2: 3+ Missing Details → BLOCK and Request Clarification

Apply when critical details are missing, making task ambiguous.

**Actions**:
- **BLOCK** task generation
- Generate error message listing missing details
- Suggest running `/speckit.clarify` or updating spec.md
- Do NOT generate placeholder task

**Error Message Template**:

```text
❌ BLOCKED: Cannot generate task - insufficient details

Task Intent: [Brief description of what was attempted]
Missing Details:
  - [Detail 1]: [What's missing and where it should be]
  - [Detail 2]: [What's missing and where it should be]
  - [Detail 3+]: [What's missing and where it should be]

Resolution:
1. Run /speckit.clarify to identify and fill gaps
2. Update spec.md [Section Name] with [Specific Details Needed]
3. Re-run /speckit.tasks to regenerate

Example: If generating service task, need:
  - Service name (spec.md Domain Model or plan.md Architecture)
  - Method names and signatures (plan.md Architecture)
  - File path structure (plan.md Directory Structure)
```

**Examples**:

```text
❌ BLOCKED: Cannot generate service task - insufficient details

Task Intent: Implement business logic service
Missing Details:
  - Service name (not found in plan.md Architecture)
  - Method names and signatures (not found in FR-001, FR-002)
  - File path (directory structure not specified)

Resolution:
1. Run /speckit.clarify to specify service architecture
2. Update plan.md Architecture section with service design
3. Re-run /speckit.tasks

❌ BLOCKED: Cannot generate API endpoint task - insufficient details

Task Intent: Create REST endpoint
Missing Details:
  - HTTP method (GET/POST/PUT/DELETE not specified)
  - Endpoint path (URL structure not defined)
  - Request/response schema (not in spec.md Contracts)
  - Handler location (plan.md Architecture missing)

Resolution:
1. Update spec.md API Requirements with endpoint specification
2. Define request/response schemas in Contracts
3. Re-run /speckit.tasks
```

**When to Use**:
- Missing: entity names, service names, endpoint paths, file locations
- Critical ambiguity: Cannot determine what needs to be built
- Multiple interpretations possible: Task would be guesswork

---

### Self-Validation Checklist

Before generating tasks.md, validate ALL tasks against these criteria:

#### ✅ Validation Checks

- [ ] **No placeholder brackets**: Zero matches for `\[(Entity|Service|Component|scenario|test|method)\d*\]`
- [ ] **No generic terms**: No "relevant", "appropriate", "necessary" without specifics
- [ ] **Concrete file paths**: All paths like `src/models/user.py`, not `src/models/[entity].py`
- [ ] **Specific method names**: All methods like `register()`, `authenticate()`, not `[method_name]()`
- [ ] **Complete HTTP details**: All API tasks have method + path + handler (e.g., "POST /api/v1/users endpoint with createUser() handler")
- [ ] **Specific test scenarios**: All test tasks reference AS-xxx and have concrete test values (e.g., "<test@example.com>, SecurePass123!")

#### ⚠️ Warning Indicators

Count of tasks with ⚠️ warnings should be **< 20%** of total tasks. If ≥ 20%:
- STOP generation
- Recommend running `/speckit.clarify` to fill specification gaps
- List all areas needing clarification

#### 🔍 Specificity Ratio

Calculate: `(Concrete nouns) / (Total nouns)` in task descriptions

**Target**: ≥ 60% concrete nouns (entity names, file paths, method names)
**Fail**: < 40% concrete nouns → Tasks too abstract, re-extract from spec/plan

**Example Analysis**:

```markdown
❌ BAD (33% concrete):
"Implement [Service] with [methods] in src/services/[service].py"
Concrete: 1 (src/services/)
Total: 3 (Service, methods, service)
Ratio: 33%

✅ GOOD (75% concrete):
"Implement UserService with register(), authenticate() methods in src/services/user_service.py"
Concrete: 6 (UserService, register, authenticate, methods, src/services/user_service.py)
Total: 8
Ratio: 75%
```

---

### Integration with Quality Gates

This section works with:
- **IG-TASK-005**: Inline gate that enforces no placeholders (HIGH severity)
- **SR-TASK-11 to SR-TASK-15**: Self-review criteria for task quality

See `templates/shared/validation/inline-gates.md` for gate definitions.

---

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
  - **Step 2.5: Platform Integration Tasks** (auto-injected if platform detected)
  - **Phase 2b: Design Foundation** (auto-injected when design.md exists)
  - **Phase 2d-UX: UX Validation Foundation** (auto-injected when UI State Matrix exists in spec.md)
- **Phase 3+**: User Stories in priority order (P1a, P1b, P2a, P2b, P3...)
  - Within each story: Tests (if requested) → Models → Services → Endpoints → Integration
  - Each phase should be a complete, independently testable increment
- **Final Phase**: Polish & Cross-Cutting Concerns

### Platform Integration Task Injection (Step 2.5)

**Trigger**: Execute when cross-platform framework is detected in constitution or codebase.

**Detection**: Use `templates/shared/platform-detection.md` algorithm:
```text
1. Check constitution.md for Technology Stack section with platform keywords
2. Check codebase for platform markers:
   - KMP: build.gradle.kts with kotlin("multiplatform")
   - Flutter: pubspec.yaml with flutter:
   - React Native: package.json with react-native dependency
```

**Injection Process**:
```text
IF PLATFORM_DETECTED != null:
  1. LOAD checklist from templates/shared/platforms/{platform}-integration-checklist.md
  2. PARSE tasks from ### Mandatory Tasks sections
  3. ASSIGN task IDs:
     - If no existing tasks: Start from T001
     - If tasks exist: Continue after last Task ID
  4. ADD markers to all tasks:
     - [CRITICAL] for iOS/Android integration tasks
     - [PLATFORM:{platform}] for traceability
  5. INSERT into Phase 2 (Foundational) BEFORE story tasks
  6. ADD implicit dependency: All Phase 3+ tasks depend on platform verification tasks

  OUTPUT: "Platform integration tasks injected: {count} tasks for {platform}"
```

**Platform Checklist Files**:

| Platform | Checklist | Task Prefix | Task Count |
|----------|-----------|-------------|------------|
| kmp | `kmp-integration-checklist.md` | T-KMP-* | ~11 tasks |
| flutter | `flutter-integration-checklist.md` | T-FLT-* | ~11 tasks |
| react_native | `rn-integration-checklist.md` | T-RN-* | ~14 tasks |

**Task Format (Platform Tasks)**:
```markdown
- [ ] T### [CRITICAL] [PLATFORM:kmp] [DEP:T###] Description
  - File: path/to/file
  - Command: specific command
  - Verify: success criteria
```

**Quality Gates (Platform)**:
- QG-PLATFORM-001: All platform tasks marked [CRITICAL] must complete before Phase 3
- QG-PLATFORM-002: Platform verification tasks must pass before story implementation

### Mobile Agent Integration (Step 2.6)

**Trigger**: Execute when any mobile platform is detected (KMP, Flutter, React Native, Native iOS/Android).

**Purpose**: Load specialized mobile development expertise via `mobile-developer-agent` persona and platform-specific skills.

**Activation Process**:
```text
IF PLATFORM_DETECTED in [kmp, flutter, react-native, ios-native, android-native]:
  1. LOAD persona: templates/personas/mobile-developer-agent.md
  2. LOAD skill: templates/skills/mobile-architecture.md
  3. LOAD skill: templates/skills/mobile-performance.md
  4. LOAD skill: templates/skills/mobile-testing.md

  THEN based on platform:
    IF platform == "kmp":
      LOAD skill: templates/skills/kmp-expert.md
    ELSE IF platform == "flutter":
      LOAD skill: templates/skills/flutter-expert.md
    ELSE IF platform == "react-native":
      LOAD skill: templates/skills/react-native-expert.md

  OUTPUT: "📱 Mobile Agent activated: {persona} with {skills}"
```

**MQS Pre-calculation**:
```text
CALCULATE preliminary MQS to identify task priorities:
  - Architecture score → Generate architecture setup tasks
  - Performance score → Generate optimization tasks if score < 15/20
  - Testing score → Ensure binding test tasks injected
  - Accessibility score → Generate a11y remediation tasks if score < 10/15

ADD to task metadata:
  - [MQS-ARCH] for architecture improvement tasks
  - [MQS-PERF] for performance optimization tasks
  - [MQS-TEST] for testing coverage tasks
  - [MQS-A11Y] for accessibility improvement tasks
```

**Task Enrichment**:
```text
FOR EACH task in Phase 2-3:
  IF task relates to mobile component:
    APPLY platform-specific patterns from loaded skill
    ADD implementation hints in task description
    REFERENCE skill section for detailed guidance

FOR EACH ViewModel/BLoC/Store detected:
  IF platform is cross-platform (KMP, Flutter, RN):
    INJECT binding test tasks (Phase 2e-BINDING)
    VERIFY 100% method coverage required
```

**Quality Gate (Mobile)**:
- QG-MQS: Mobile Quality Score ≥ 75 required for release (validated after implementation)
- QG-PLATFORM-003: iOS and Android builds must succeed

### Phase 2d-UX: UX Validation Foundation (for UI features) 🎯

**Trigger**: Execute when ANY of the following conditions are met:
- spec.md contains UI State Matrix section
- spec.md contains Component Registry section
- spec.md contains AS-UI-xxx or AS-RWD-xxx or AS-INT-xxx scenarios
- design.md exists in feature directory or specs/app-design/

**Purpose**: Establish UX testing infrastructure before user story implementation. Validates that all UI states, responsive layouts, and interactions have test coverage.

**Detection**:
```text
1. Check spec.md for "### UI State Matrix" section
2. Check spec.md for "### Component Registry" section
3. Check spec.md for AS-UI-xxx, AS-RWD-xxx, or AS-INT-xxx scenario IDs
4. Check for design.md in FEATURE_DIR or specs/app-design/
5. If ANY condition met → inject Phase 2d-UX tasks
```

**Quality Gates (UX)**:
- QG-STATE-001: All components have UI state scenarios (100% coverage)
- QG-RWD-001: All screens have responsive scenarios (mobile/tablet/desktop)
- QG-INT-001: All interactive components have interaction scenarios
- QG-CSTM-001: Component-Scenario Traceability Matrix shows 100% coverage

**Task Generation Process**:

```text
# Step 1: Infrastructure Tasks
GENERATE tasks:
  - [ ] T### [P] [A11Y] Setup axe-core for automated accessibility testing in tests/a11y/
  - [ ] T### [P] [VRT:baseline] Setup visual regression baseline (Playwright screenshots) in tests/visual/
  - [ ] T### [P] Configure viewport testing matrix in tests/config/viewports.ts

# Step 2: State Testing Tasks (auto-generated from UI State Matrix)
FOR EACH component IN UI_STATE_MATRIX:
  FOR EACH state IN component.applicable_states:
    GENERATE task:
      - [ ] T### [STATE-TEST:{component.id}:{state}] [TEST:{component.as_ui_id}] Test {component.name} {state} state

# Step 3: Responsive Testing Tasks (auto-generated from AS-RWD)
FOR EACH as_rwd IN RESPONSIVE_ACCEPTANCE_SCENARIOS:
  GENERATE task:
    - [ ] T### [RWD-TEST:{as_rwd.screen}:{as_rwd.viewport}] [TEST:{as_rwd.id}] Test {as_rwd.screen} {as_rwd.viewport} layout

# Step 4: Interaction Testing Tasks (auto-generated from AS-INT)
FOR EACH as_int IN INTERACTION_STATE_SCENARIOS:
  GENERATE task:
    - [ ] T### [INT-TEST:{as_int.id}] Test {as_int.component} {as_int.trigger} transition ({as_int.duration}, {as_int.easing})

# Step 5: Accessibility Audit Task
GENERATE task:
  - [ ] T### [A11Y-AUDIT] Run full accessibility audit before implementation
    - axe-core on all screens
    - Keyboard navigation test
    - Screen reader announcement test (from AS-INT a11y columns)
    - Color contrast validation
```

**Example Output (Phase 2d-UX)**:

```markdown
## Phase 2d-UX: UX Validation Foundation 🎯

**Purpose**: Establish UX testing infrastructure before user story implementation

**Quality Gates**: QG-STATE-001, QG-RWD-001, QG-INT-001, QG-CSTM-001

### UX Test Infrastructure

- [ ] T020 [P] [A11Y] Setup axe-core accessibility testing in tests/a11y/setup.ts
- [ ] T021 [P] [VRT:baseline] Setup Playwright visual regression in tests/visual/config.ts
- [ ] T022 [P] Configure viewport matrix: mobile (375px), tablet (768px), desktop (1280px) in tests/config/viewports.ts

### State Testing Tasks

- [ ] T023 [STATE-TEST:COMP-001:loading] [TEST:AS-UI-002] Test Button loading state renders spinner
- [ ] T024 [STATE-TEST:COMP-001:error] [TEST:AS-UI-003] Test Button error state shows error styling
- [ ] T025 [STATE-TEST:COMP-001:disabled] [TEST:AS-UI-005] Test Button disabled state prevents interaction
- [ ] T026 [STATE-TEST:COMP-002:loading] [TEST:AS-UI-011] Test Form loading state shows overlay
- [ ] T027 [STATE-TEST:COMP-002:error] [TEST:AS-UI-012] Test Form error state highlights invalid fields

### Responsive Testing Tasks

- [ ] T028 [RWD-TEST:SCR-001:mobile] [TEST:AS-RWD-001] Test Settings mobile layout (hamburger nav, single column)
- [ ] T029 [RWD-TEST:SCR-001:tablet] [TEST:AS-RWD-002] Test Settings tablet layout (collapsed sidebar)
- [ ] T030 [RWD-TEST:SCR-001:desktop] [TEST:AS-RWD-003] Test Settings desktop layout (full sidebar)

### Interaction Testing Tasks

- [ ] T031 [INT-TEST:AS-INT-001] Test Button hover transition (150ms, ease-out)
- [ ] T032 [INT-TEST:AS-INT-006] Test Input error state with shake animation (200ms)
- [ ] T033 [INT-TEST:AS-INT-008] Test Form success state with fade animation (300ms)

### Accessibility Baseline

- [ ] T034 [A11Y-AUDIT] Run axe-core audit on all screens (0 critical, ≤5 warnings)
- [ ] T035 [A11Y] Keyboard navigation test: Tab through all interactive elements
- [ ] T036 [A11Y] Screen reader test: Verify announcements match AS-INT specs

**Checkpoint**: UX validation foundation ready - user story implementation can begin
```

**Design Integration (when design.md and .preview/ exist)**:

```text
IF .preview/ directory exists:
  # Load MQS report
  MQS_REPORT = READ .preview/reports/mqs-score.json

  IF MQS_REPORT.score < 80:
    WARN "MQS score {score} < 80 threshold. Implementation may have design issues."

  # Generate tasks from accessibility issues
  FOR EACH issue IN MQS_REPORT.accessibility_issues:
    IF issue.severity == 'critical':
      GENERATE task:
        - [ ] T### [A11Y] [FIX:MQS-A11Y] Fix accessibility issue: {issue.description}
        Priority: P1

  # Generate tasks from touch target violations
  FOR EACH violation IN READ .preview/reports/touch-targets.md:
    GENERATE task:
      - [ ] T### [A11Y] [TOUCH] Fix touch target: {violation.component} ({violation.size} → 44px)

  # Generate tasks from token compliance issues
  FOR EACH issue IN READ .preview/reports/token-compliance.md:
    IF issue.type == 'hardcoded_color' OR issue.type == 'hardcoded_spacing':
      GENERATE task:
        - [ ] T### [DS-AUDIT] Replace hardcoded {issue.type}: {issue.location}
```

**E2E Journey Tests (auto-generated from design.md journeys)**:

```text
IF design.md contains User Journey sections
   OR journeys/ directory exists in FEATURE_DIR
   OR specs/app-design/journeys/ directory exists:
  FOR EACH journey:
    GENERATE task:
      - [ ] T### [E2E:{journey.slug}] End-to-end test: {journey.name}
        - Entry: {journey.entry_point}
        - Steps: {journey.steps}
        - Exit criteria: {journey.exit_criteria}
        - Error paths: {journey.error_paths}
```

**Example E2E Tasks**:

```markdown
### E2E Journey Tests

- [ ] T040 [E2E:login-to-dashboard] End-to-end test: Login → Dashboard flow
  - Entry: /login page
  - Steps: Enter credentials → Submit → Redirect → Load dashboard
  - Exit criteria: Dashboard fully rendered with user data
  - Error paths: Invalid credentials, network failure, session expired

- [ ] T041 [E2E:settings-update] End-to-end test: Settings modification flow
  - Entry: Settings page via navigation
  - Steps: Change setting → Save → Confirm → Reload
  - Exit criteria: Setting persisted and reflected in UI
  - Error paths: Validation failure, save failure, concurrent edit
```

### Phase 2e-BINDING: Platform Binding Verification (for KMP) 🔗

**Trigger**: Execute when platform is KMP (detected via platform-detection.md)

**Purpose**: Verify that platform UI (SwiftUI/Compose) correctly binds to shared Kotlin ViewModels. Prevents bugs where shared Kotlin code works but platform UI has TODO/stub implementations.

**Detection**:
```text
1. Check for shared/ directory with Kotlin ViewModels (*ViewModel.kt)
2. Check for iosApp/ with SwiftUI files (*.swift)
3. Check for androidApp/ with Compose files (*Screen.kt, *Activity.kt)
4. If KMP detected → inject Phase 2e-BINDING tasks
```

**Task Generation**:

```text
FOR EACH ViewModel in shared/src/commonMain/**/*ViewModel.kt:
  PARSE public methods and StateFlow properties

  FOR EACH public method:
    GENERATE task:
      - [ ] T### [BINDING-TEST:{ViewModel}:{method}] Verify platform UI calls {ViewModel}.{method}()
        - iOS: Test SwiftUI wrapper calls Kotlin method
        - Android: Test Compose calls Kotlin method
        - Mock ViewModel, verify correct parameters passed

  FOR EACH StateFlow property:
    GENERATE task:
      - [ ] T### [BINDING-TEST:{ViewModel}:{property}] Verify platform UI observes {ViewModel}.{property}
        - iOS: Test .sink/.assign receives state updates
        - Android: Test .collectAsState() receives state updates
        - Verify UI re-renders on state change
```

**Quality Gates (Binding)**:
- QG-BIND-001: All ViewModel public methods have platform binding tests (100% coverage)
- QG-BIND-002: All StateFlow properties are observed in platform UI (100% coverage)
- QG-BIND-003: Zero TODO/FIXME/stub comments in platform binding code

**Example Output (Phase 2e-BINDING)**:

```markdown
## Phase 2e-BINDING: Platform Binding Verification 🔗

**Purpose**: Verify SwiftUI/Compose correctly binds to shared Kotlin ViewModels

**Quality Gates**: QG-BIND-001, QG-BIND-002, QG-BIND-003

### ReaderViewModel Binding Tests

- [ ] T050 [BINDING-TEST:ReaderViewModel:goToPage] Verify platform UI calls goToPage(page: Int)
  - iOS: ReaderViewModelWrapper.goToPage() → Kotlin ReaderViewModel.goToPage()
  - Android: ReaderScreen calls viewModel.goToPage()
  - Mock: Verify page parameter passed correctly

- [ ] T051 [BINDING-TEST:ReaderViewModel:setFontSize] Verify platform UI calls setFontSize(size: Int)
  - iOS: ReaderViewModelWrapper.setFontSize() → Kotlin ReaderViewModel.setFontSize()
  - Android: SettingsScreen calls viewModel.setFontSize()
  - Mock: Verify size persisted to repository

- [ ] T052 [BINDING-TEST:ReaderViewModel:currentPage] Verify platform UI observes currentPage StateFlow
  - iOS: Test .sink receives page updates
  - Android: Test .collectAsState() receives page updates
  - Verify: Page indicator UI updates on state change

- [ ] T053 [BINDING-TEST:ReaderViewModel:tableOfContents] Verify platform UI observes tableOfContents StateFlow
  - iOS: Test .sink receives TOC from ViewModel (not hardcoded)
  - Android: Test .collectAsState() receives TOC
  - Verify: No hardcoded chapter values in platform code

### SettingsViewModel Binding Tests

- [ ] T054 [BINDING-TEST:SettingsViewModel:fontSize] Verify platform UI observes fontSize StateFlow
- [ ] T055 [BINDING-TEST:SettingsViewModel:setFontSize] Verify platform UI calls setFontSize()

**Checkpoint**: All platform bindings verified - no TODO/stub code in platform layer
```

### Test Task Generation (Enhanced)

**When tests are requested**, generate detailed test task descriptions using the following process:

#### Context
Generate detailed test task descriptions from acceptance scenarios in the feature specification.

#### Inputs
- `acceptance_scenarios`: Array of scenarios from spec.md with Given/When/Then
- `edge_cases`: Array of suggested edge cases (suggested_edge_cases from section 1.1, if available)
- `technical_plan`: Implementation plan details (API endpoints, functions, components from plan.md)
- `project_language`: Primary programming language (detected from language-loading.md)

#### Process Steps

**STEP 1: Classify Test Type per Scenario**

For each acceptance scenario, determine optimal test type based on classification:

```
scenario.classification == "HAPPY_PATH":
  test_type: "Integration Test"
  scope: "End-to-end flow with real dependencies"
  reasoning: "Validates complete user journey through system"

scenario.classification == "ERROR_PATH":
  test_type: "Unit Test + Contract Test"
  scope: "Error handling logic + API error response"
  reasoning: "Error paths typically isolated to validation/error handling logic"

scenario.classification == "BOUNDARY":
  test_type: "Unit Test"
  scope: "Edge case validation"
  reasoning: "Boundary conditions test specific validation rules"

scenario.classification == "SECURITY":
  test_type: "Security Test"
  scope: "Auth bypass, injection, XSS, CSRF"
  reasoning: "Security scenarios require dedicated security test suite"

scenario.classification == "ALT_PATH":
  test_type: "Unit Test"
  scope: "Alternative logic branches"
  reasoning: "Alternative paths test conditional logic"
```

**STEP 2: Map Given/When/Then to Test Structure**

For each scenario, generate test structure mapping from Given/When/Then to ARRANGE/ACT/ASSERT:

```
GIVEN → Test Setup (Arrange):
  - Extract preconditions from Given clause
  - Identify required mocks, database seeds, auth setup
  - Suggest specific setup code patterns

WHEN → Test Execution (Act):
  - Extract action from When clause
  - Identify API endpoint, function call, or user interaction
  - Suggest specific invocation pattern

THEN → Assertions (Assert):
  - Extract expected outcomes from Then clause
  - Generate specific assertions (status codes, response fields, side effects)
  - Suggest assertion patterns for the detected language
```

**STEP 3: Generate Test Data Suggestions**

For each entity detected in the scenario, suggest test data patterns based on entity type and project language:

**Python**:
```
email → "Use faker.email() for random valid emails. Avoid hardcoded <test@example.com>."
password → "Use factory helper: generate_secure_password(). Never hardcode passwords."
numeric (ID) → "Use factory_boy for realistic IDs. For boundary tests: -1, 0, sys.maxsize"
date → "Use datetime.now() + timedelta for relative dates. Avoid hardcoded dates."
```

**TypeScript**:
```
email → "Use faker.internet.email() for random emails. Avoid hardcoded <test@example.com>."
password → "Use helper: generateSecurePassword(). Never commit hardcoded passwords."
numeric (ID) → "Use factories (factory-bot). For boundary: Number.MIN_SAFE_INTEGER, Number.MAX_SAFE_INTEGER"
date → "Use new Date() for relative dates. Avoid hardcoded ISO strings."
```

**Go**:
```
email → "Use faker.Email() for random emails. Avoid hardcoded <test@example.com>."
password → "Use helper: generateSecurePassword(). Never hardcode passwords."
numeric (ID) → "Use factories or fixture builders. For boundary: math.MinInt64, math.MaxInt64"
date → "Use time.Now() for relative dates. Avoid hardcoded RFC3339 strings."
```

**STEP 4: Generate Edge Case Test Tasks**

For each edge case from spec.md's `suggested_edge_cases` field (from section 1.1):

1. Check if edge case is already covered by an existing ERROR_PATH or BOUNDARY scenario
2. If not covered, generate dedicated edge case test task
3. Use [TEST:AS-xxx:EDGE-n] marker to link edge case test to parent scenario

**Output Format**:
```markdown
#### Test: Edge Case - {edge_case_description}

**Edge Case**: {specific_condition}

**Test Structure**:
```{language}
# ARRANGE
{specific_edge_case_setup}

# ACT
{action_that_triggers_edge_case}

# ASSERT
{expected_error_or_boundary_behavior}
```

**Estimated Effort**: {minutes_or_hours}
```

**STEP 4.5: Generate UI E2E Test Tasks** [REF:UI-TEST-GEN-001]

For acceptance scenarios in UI_AS_LIST (detected in Step 3.5), generate E2E UI test tasks:

```text
FOR EACH ui_as IN UI_AS_LIST:
  # Extract scenario details
  scenario = FIND AS in AS_LIST WHERE as.id == ui_as.id
  platform = ui_as.platform
  framework = platform.framework

  # Determine test file path based on framework
  test_file_path = GENERATE_TEST_PATH(framework, ui_as.id)

  # Generate E2E test task
  GENERATE task:
    ID: T{next_id}
    Markers: [E2E-TEST:{ui_as.id}] [TEST:{ui_as.id}]
    Description: "E2E test for {scenario.summary} using {framework}"
    File: {test_file_path}
    Subtasks:
      - **Framework**: {framework}
      - **Platform**: {', '.join(platform.platforms)}
      - **Scenario**: {scenario.given_when_then}
      - **Selectors**: testId-first, fallback to aria-label
      - **Auto-fix**: Basic mode (2 attempts) - retry + fallback selectors
      - **Quality Gate**: QG-UI-002 (test must pass after auto-fix)

# Test file path generation
GENERATE_TEST_PATH(framework, as_id):
  IF framework == "playwright":
    RETURN "tests/e2e/{as_id.lower()}.spec.ts"
  ELSE IF framework == "playwright-electron":
    RETURN "tests/e2e/electron/{as_id.lower()}.spec.ts"
  ELSE IF framework == "xcuitest":
    RETURN "UITests/{as_id}Test.swift"
  ELSE IF framework == "espresso":
    RETURN "app/src/androidTest/java/{package}/{as_id}Test.kt"
  ELSE IF framework == "maestro":
    RETURN ".maestro/{as_id.lower()}.yaml"
  ELSE IF framework == "detox":
    RETURN "e2e/{as_id.lower()}.e2e.ts"
  ELSE IF framework == "tauri-webdriver":
    RETURN "tests/e2e/tauri/{as_id.lower()}.spec.ts"
  ELSE:
    RETURN "tests/e2e/{as_id.lower()}.test.js"

# Generate scaffold template reference
FOR EACH ui_test_task:
  ADD note: "Scaffold: templates/shared/test-scaffolds/{framework}-scaffold.md"

# Validate QG-UI-001 (100% UI AS coverage)
ui_test_count = len([task for task in TASKS if "[E2E-TEST:" in task.markers])
ui_as_count = len(UI_AS_LIST)

IF ui_test_count < ui_as_count:
  FAIL QG-UI-001:
    message: "QG-UI-001 FAILED: {ui_as_count - ui_test_count} UI scenarios lack E2E tests"
    missing: [as.id for as in UI_AS_LIST if not has_e2e_test(as.id)]
ELSE:
  LOG "QG-UI-001 PASSED: {ui_test_count}/{ui_as_count} UI scenarios have E2E tests"
```

**Test Task Example** (Playwright Web):
```markdown
- [ ] T025 [US2] [E2E-TEST:AS-2A] [TEST:AS-2A] E2E test: User can submit form with valid data

**Framework**: Playwright (Web)
**Platform**: web
**Scenario**: AS-2A - Given user is on form page, When user fills all required fields and clicks submit, Then form is submitted successfully and confirmation is shown
**Selectors**: testId-first (`data-testid="submit-button"`), fallback to `button[aria-label="Submit"]`
**Auto-fix**: Basic mode (2 attempts: retry with explicit wait, fallback selector)
**File**: tests/e2e/as-2a.spec.ts
**Scaffold**: templates/shared/test-scaffolds/playwright-web-scaffold.md
```

**Test Task Example** (XCUITest iOS):
```markdown
- [ ] T032 [US3] [E2E-TEST:AS-3B] [TEST:AS-3B] E2E test: User can navigate to settings screen

**Framework**: XCUITest (iOS)
**Platform**: ios
**Scenario**: AS-3B - Given user is on home screen, When user taps settings button, Then settings screen is displayed
**Selectors**: Accessibility identifier first, fallback to label
**Auto-fix**: Basic mode (2 attempts: waitForExistence, scrollIntoView)
**File**: UITests/AS3BTest.swift
**Scaffold**: templates/shared/test-scaffolds/xcuitest-scaffold.md
```

**Output**: E2E test tasks for all UI scenarios with framework-specific paths and scaffold references.

**STEP 5: Suggest Property-Based Testing (Optional)**

For scenarios matching PBT criteria, suggest using `/speckit.properties`:
- BOUNDARY classification + numeric/string entities
- SECURITY classification + user input
- High entity cardinality (many possible input values)

**Suggestion Format**:
```markdown
💡 **Consider Property-Based Testing**: Run `/speckit.properties` for this scenario

**Property**: {property_description}
**Framework**: {Hypothesis|fast-check|rapid|jqwik|kotest (based on language)}
**Why PBT**: {reasoning_for_property_based_approach}
**Alternative**: Implement explicit test cases if PBT overhead too high for this feature
```

**STEP 6: Format Test Task Description**

Combine all components into detailed test task with rich structure:

**For each test task, use this format**:

```markdown
#### Test: {test_type} - {scenario_summary}

**Scenario**: AS-{id} - {scenario_description}

**Test Structure**:
```{language}
# ARRANGE (Given: {given_clause})
{setup_code_suggestions}

# ACT (When: {when_clause})
{action_code_suggestion}

# ASSERT (Then: {then_clause})
{assertion_code_suggestions}
```

**Test Data Suggestions**:
- {entity_1}: {suggestion_1}
- {entity_2}: {suggestion_2}
- {entity_3}: {suggestion_3}

{IF edge_cases_exist:}
**Edge Cases to Cover**: See edge case tests below (T###-T###)

{IF pbt_applicable:}
{pbt_suggestion_block}

**Estimated Effort**: {effort_hours_or_minutes}
```

#### Output

When generating test tasks, produce:
- Main test task with [TEST:AS-xxx] marker
- Detailed test structure with ARRANGE/ACT/ASSERT mapping
- Test data suggestions specific to project language
- Edge case test tasks with [TEST:AS-xxx:EDGE-n] markers
- Optional PBT suggestions for applicable scenarios

**Integration with existing workflow**:
- Test tasks still follow checklist format: `- [ ] T### [P?] [US#] [TEST:AS-xxx] Description`
- Test tasks still appear BEFORE implementation tasks in each story phase (TDD approach)
- Test Traceability Matrix still tracks [TEST:] markers for coverage validation

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

2. AS Coverage (MANDATORY - QG-TEST-001):
   FOR EACH AS in spec.md WHERE "Requires Test = YES":
     - MUST have at least one test task with [TEST:AS-xxx] marker
     - If no test found: BLOCK with "QG-TEST-001 FAILED: AS-xxx has no test task"

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

### Step 1: Load Generated Artifact (In-Memory Preferred)

**Use in-memory content to avoid re-reading the file** (saves ~50-100KB tokens):

```text
IF GENERATED_TASKS_CONTENT exists IN SESSION_CACHE:
  tasks_content = SESSION_CACHE["GENERATED_TASKS_CONTENT"]
  LOG "📦 Using in-memory tasks content (saved file read)"
ELSE:
  tasks_content = READ(FEATURE_DIR/tasks.md)
  LOG "📖 Reading tasks.md from disk"
```

Parse the content to extract:
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
| SR-TASK-06 | AS Coverage Complete | Every AS-xxx from spec.md has at least one [TEST:AS-xxx] task (MANDATORY) | CRITICAL |
| SR-TASK-07 | DEP References Valid | All [DEP:T###] reference existing task IDs | CRITICAL |
| SR-TASK-08 | No Circular Dependencies | Dependency graph has no cycles | CRITICAL |
| SR-TASK-09 | RTM Table Complete | Requirements Traceability Matrix lists all FRs with linked tasks | MEDIUM |
| SR-TASK-10 | Coverage Summary Present | Coverage Summary section shows FR/AS coverage stats | MEDIUM |
| SR-TASK-11 | Component Markers Present | Phase 2b component tasks have [COMP:COMP-xxx] markers (UI features) | HIGH |
| SR-TASK-12 | Wire Tasks Complete | Every (Component, Target Screen) pair has [WIRE:] task (QG-COMP-002) | CRITICAL |
| SR-TASK-13 | CSIM Matrix Complete | Component-Screen Integration Matrix shows 100% coverage (UI features) | HIGH |

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
