---

description: "Task list template for feature implementation"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] [Markers] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- **[DEP:T001,T002]**: Explicit task dependencies (required before this task)
- **[FR:FR-001]**: Links to Functional Requirements from spec.md
- **[VR:VR-001]**: Links to Visual Requirements from spec.md (for UI features)
- **[IR:IR-001]**: Links to Interaction Requirements from spec.md (for UI features)
- **[TEST:AS-1A]**: Test task links to Acceptance Scenario ID
- Include exact file paths in descriptions

### Marker Examples

```markdown
# Implementation task with dependencies and FR link
- [ ] T014 [US1] [DEP:T012,T013] [FR:FR-001] Implement UserService in src/services/user.py

# Test task linking to Acceptance Scenario
- [ ] T020 [US1] [TEST:AS-1A] Test "user can register with email" in tests/integration/test_registration.py

# Parallel task with no dependencies
- [ ] T012 [P] [US1] [FR:FR-001] Create User model in src/models/user.py
```

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

<!-- 
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.
  
  The /speckit.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/
  
  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment
  
  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 [DEP:T001] Initialize [language] project with [framework] dependencies
- [ ] T003 [P] [DEP:T001] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T004 [DEP:T002] Setup database schema and migrations framework
- [ ] T005 [P] [DEP:T002] Implement authentication/authorization framework
- [ ] T006 [P] [DEP:T002] Setup API routing and middleware structure
- [ ] T007 [DEP:T004] Create base models/entities that all stories depend on
- [ ] T008 [DEP:T002] Configure error handling and logging infrastructure
- [ ] T009 [P] [DEP:T002] Setup environment configuration management

**Checkpoint**: Foundation ready - proceed to Design Foundation (if UI feature) or user stories

---

## Phase 2b: Design Foundation *(for UI features)* 🎨

<!--
  Include this phase ONLY if the feature has significant user interface.
  Skip for API-only, CLI, or backend features.
  Depends on Phase 2 completion.
  Reference: design.md from /speckit.design command
-->

**Purpose**: Visual infrastructure that user stories depend on for consistent UI

**⚠️ CRITICAL FOR UI FEATURES**: No UI component work can begin until design tokens are established

**VR/IR Requirements Covered**: VR-001, VR-002, IR-001, IR-002

### Design Token Tasks

- [ ] T0XX [P] [DEP:T002] Create design tokens in src/styles/tokens.css (colors, spacing, typography)
- [ ] T0XX [P] [DEP:T002] Configure theme provider/context in src/providers/theme.tsx (if applicable)
- [ ] T0XX [DEP:T0XX] Setup CSS variable scoping for light/dark mode support

### Component Foundation Tasks

- [ ] T0XX [P] [DEP:T002] Create component library structure in src/components/ui/
- [ ] T0XX [DEP:T0XX] [VR:VR-001] Create base Button component with all states in src/components/ui/Button.tsx
- [ ] T0XX [DEP:T0XX] [VR:VR-002] Create base Input component with validation states in src/components/ui/Input.tsx
- [ ] T0XX [DEP:T0XX] Create layout primitives (Stack, Grid, Container) in src/components/ui/Layout.tsx
- [ ] T0XX [DEP:T0XX] Configure responsive breakpoints in src/styles/breakpoints.css

### Accessibility Foundation Tasks

- [ ] T0XX [P] [DEP:T002] Setup focus management utilities in src/utils/focus.ts
- [ ] T0XX [P] [DEP:T002] Create skip link component for keyboard navigation
- [ ] T0XX [DEP:T0XX] Configure screen reader live regions

### Animation Foundation Tasks (if applicable)

- [ ] T0XX [P] [DEP:T002] [IR:IR-001] Setup animation utilities/library
- [ ] T0XX [DEP:T0XX] Create transition presets (fade, slide, scale)
- [ ] T0XX [DEP:T0XX] Configure reduced-motion media query support

**Checkpoint**: Design foundation ready - UI feature work can begin with consistent tokens and primitives

---

## Phase 3: User Story 1 - [Title] (Priority: P1a) 🎯 MVP

**Goal**: [Brief description of what this story delivers]

**Concept Reference**: [EPIC-001.F01.S01 or "N/A"]

**Independent Test**: [How to verify this story works on its own]

**Acceptance Scenarios Covered**: AS-1A, AS-1B

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] [TEST:AS-1A] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T011 [P] [US1] [TEST:AS-1B] Integration test for [user journey] in tests/integration/test_[name].py

### Implementation for User Story 1

- [ ] T012 [P] [US1] [FR:FR-001] Create [Entity1] model in src/models/[entity1].py
- [ ] T013 [P] [US1] [FR:FR-001] Create [Entity2] model in src/models/[entity2].py
- [ ] T014 [US1] [DEP:T012,T013] [FR:FR-001,FR-002] Implement [Service] in src/services/[service].py
- [ ] T015 [US1] [DEP:T014] [FR:FR-002] Implement [endpoint/feature] in src/[location]/[file].py
- [ ] T016 [US1] [DEP:T015] [FR:FR-002] Add validation and error handling
- [ ] T017 [US1] [DEP:T015] Add logging for user story 1 operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - [Title] (Priority: P1b)

**Goal**: [Brief description of what this story delivers]

**Concept Reference**: [EPIC-001.F01.S02 or "N/A"]

**Independent Test**: [How to verify this story works on its own]

**Acceptance Scenarios Covered**: AS-2A

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US2] [TEST:AS-2A] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T019 [P] [US2] [TEST:AS-2A] Integration test for [user journey] in tests/integration/test_[name].py

### Implementation for User Story 2

- [ ] T020 [P] [US2] [FR:FR-003] Create [Entity] model in src/models/[entity].py
- [ ] T021 [US2] [DEP:T020] [FR:FR-003] Implement [Service] in src/services/[service].py
- [ ] T022 [US2] [DEP:T021] [FR:FR-003] Implement [endpoint/feature] in src/[location]/[file].py
- [ ] T023 [US2] [DEP:T022,T015] Integrate with User Story 1 components (if needed)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - [Title] (Priority: P2a)

**Goal**: [Brief description of what this story delivers]

**Concept Reference**: [EPIC-001.F02.S01 or "N/A"]

**Independent Test**: [How to verify this story works on its own]

**Acceptance Scenarios Covered**: AS-3A

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T024 [P] [US3] [TEST:AS-3A] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T025 [P] [US3] [TEST:AS-3A] Integration test for [user journey] in tests/integration/test_[name].py

### Implementation for User Story 3

- [ ] T026 [P] [US3] [FR:FR-004] Create [Entity] model in src/models/[entity].py
- [ ] T027 [US3] [DEP:T026] [FR:FR-004] Implement [Service] in src/services/[service].py
- [ ] T028 [US3] [DEP:T027] [FR:FR-004] Implement [endpoint/feature] in src/[location]/[file].py

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] TXXX [P] Documentation updates in docs/
- [ ] TXXX Code cleanup and refactoring
- [ ] TXXX Performance optimization across all stories
- [ ] TXXX [P] Additional unit tests (if requested) in tests/unit/
- [ ] TXXX Security hardening
- [ ] TXXX Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **Design Foundation (Phase 2b)**: *For UI features* - Depends on Phase 2, BLOCKS UI component work
- **User Stories (Phase 3+)**: All depend on Foundational phase completion (and Design Foundation for UI features)
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for [endpoint] in tests/contract/test_[name].py"
Task: "Integration test for [user journey] in tests/integration/test_[name].py"

# Launch all models for User Story 1 together:
Task: "Create [Entity1] model in src/models/[entity1].py"
Task: "Create [Entity2] model in src/models/[entity2].py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

---

## Dependency Graph

<!--
  This graph is auto-generated by /speckit.tasks from [DEP:] markers.
  It shows the task execution order and parallel opportunities.
-->

```mermaid
graph TD
    subgraph Phase1[Phase 1: Setup]
        T001[T001: Project structure]
        T002[T002: Initialize project]
        T003[T003: Linting]
    end

    subgraph Phase2[Phase 2: Foundation]
        T004[T004: Database schema]
        T005[T005: Auth framework]
        T006[T006: API routing]
        T007[T007: Base models]
    end

    subgraph Phase3[Phase 3: US1]
        T012[T012: Entity1 model]
        T013[T013: Entity2 model]
        T014[T014: Service]
        T015[T015: Endpoint]
        T010[T010: Test AS-1A]
        T011[T011: Test AS-1B]
    end

    T001 --> T002
    T001 --> T003
    T002 --> T004
    T002 --> T005
    T002 --> T006
    T004 --> T007
    T007 --> T012
    T007 --> T013
    T012 --> T014
    T013 --> T014
    T014 --> T015
    T015 --> T010
    T015 --> T011
```

---

## Requirements Traceability Matrix (RTM)

<!--
  This matrix links:
  - Functional Requirements (FR) from spec.md
  - Implementation tasks that fulfill each FR
  - Test tasks that verify acceptance scenarios

  Status: ❌ Not started | 🔄 In progress | ✅ Complete
-->

| Requirement | Description | Impl Tasks | Test Tasks | Status |
|-------------|-------------|------------|------------|--------|
| FR-001 | [System MUST...] | T012, T013, T014 | T010 | ❌ |
| FR-002 | [System MUST...] | T014, T015, T016 | T011 | ❌ |
| FR-003 | [Users MUST...] | T020, T021, T022 | T018, T019 | ❌ |
| FR-004 | [System MUST...] | T026, T027, T028 | T024, T025 | ❌ |

---

## Acceptance Scenario Coverage

<!--
  Maps each Acceptance Scenario (AS) to its test task.
  Ensures every AS has explicit test coverage.
-->

| Scenario ID | Description | Test Task | Status |
|-------------|-------------|-----------|--------|
| AS-1A | [Given/When/Then summary] | T010 | ❌ |
| AS-1B | [Given/When/Then summary] | T011 | ❌ |
| AS-2A | [Given/When/Then summary] | T018, T019 | ❌ |
| AS-3A | [Given/When/Then summary] | T024, T025 | ❌ |

---

## Coverage Summary

<!--
  Auto-calculated by /speckit.analyze
-->

| Metric | Count | Covered | Coverage |
|--------|-------|---------|----------|
| Functional Requirements | 4 | 0 | 0% |
| Acceptance Scenarios | 4 | 0 | 0% |
| Edge Cases | 2 | 0 | 0% |
| Total Tasks | 28 | 0 | 0% |

**Gaps Identified**:
- [ ] EC-001: [Edge case] - No test task assigned
- [ ] EC-002: [Edge case] - No test task assigned

---

## Notes

- **[P]** tasks = different files, no dependencies
- **[Story]** label maps task to specific user story for traceability
- **[DEP:T001,T002]** = explicit dependencies, validated for cycles by /speckit.analyze
- **[FR:FR-001]** = links to Functional Requirement for traceability
- **[VR:VR-001]** = links to Visual Requirement for UI traceability (from design.md)
- **[IR:IR-001]** = links to Interaction Requirement for animation/behavior traceability
- **[TEST:AS-1A]** = test task covers specific Acceptance Scenario
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Run `/speckit.analyze` to validate dependency graph (no cycles) and coverage gaps
- For UI features: Ensure design tokens are established before component work begins
