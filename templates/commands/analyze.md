---
description: Perform a non-destructive cross-artifact consistency, traceability, dependency, and system spec analysis across concept.md, spec.md, plan.md, tasks.md, and system specs.
handoffs:
  - label: Fix Spec Issues
    agent: speckit.specify
    prompt: Update the specification to address the identified issues
    auto: false
    condition:
      - "Analysis found CRITICAL or HIGH issues in spec.md"
      - "Requirement ambiguities or duplications detected"
  - label: Update Plan
    agent: speckit.plan
    prompt: Revise the plan to address architectural issues
    auto: false
    condition:
      - "Analysis found architectural inconsistencies"
      - "Plan sections need revision based on findings"
  - label: Regenerate Tasks
    agent: speckit.tasks
    prompt: Regenerate tasks with corrected traceability
    auto: false
    condition:
      - "Traceability gaps (FR without tasks) detected"
      - "Dependency issues require task restructuring"
  - label: Proceed to Implementation
    agent: speckit.implement
    prompt: Start implementation (only if no CRITICAL issues)
    auto: true
    condition:
      - "Analysis completed successfully"
      - "All CRITICAL issues resolved"
    gates:
      - name: "No Critical Issues Gate"
        check: "CRITICAL issue count == 0"
        block_if: "CRITICAL > 0"
        message: "Cannot proceed to implementation: resolve all CRITICAL issues first"
      - name: "Dependency Graph Valid Gate"
        check: "Dependency Graph Status == VALID or WARNINGS"
        block_if: "Dependency Graph Status == INVALID"
        message: "Resolve circular dependencies or invalid references before implementation"
    post_actions:
      - "log: Analysis passed, transitioning to implementation"
claude_code:
  reasoning_mode: extended
  thinking_budget: 12000
  subagents:
    - role: code-explorer
      trigger: "when tracing implementation coverage or validating file references"
      prompt: "Explore codebase for {PATTERN} to validate implementation coverage"
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Identify inconsistencies, duplications, ambiguities, underspecified items, **dependency cycles**, and **traceability gaps** across project artifacts before implementation. This command validates:

1. **Cross-artifact consistency** (spec.md ↔ plan.md ↔ tasks.md)
2. **Concept coverage** (concept.md → spec.md, if concept exists)
3. **Dependency graph validity** (no cycles, valid references)
4. **Requirements traceability** (FR → Tasks, AS → Tests)
5. **Coverage completeness** (all requirements have implementation tasks)
6. **System spec impact** (System Spec Impact section ↔ specs/system/)
7. **System spec integrity** (dependency graph, deprecation, drift detection)

This command MUST run only after `/speckit.tasks` has successfully produced a complete `tasks.md`.

## Operating Constraints

**STRICTLY READ-ONLY**: Do **not** modify any files. Output a structured analysis report. Offer an optional remediation plan (user must explicitly approve before any follow-up editing commands would be invoked manually).

**Constitution Authority**: The project constitution (`/memory/constitution.md`) is **non-negotiable** within this analysis scope. Constitution conflicts are automatically CRITICAL and require adjustment of the spec, plan, or tasks—not dilution, reinterpretation, or silent ignoring of the principle. If a principle itself needs to change, that must occur in a separate, explicit constitution update outside `/speckit.analyze`.

## Execution Steps

### 1. Initialize Analysis Context

Run `{SCRIPT}` once from repo root and parse JSON for FEATURE_DIR and AVAILABLE_DOCS. Derive absolute paths:

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md
- CONCEPT = specs/concept.md (optional, check if exists)

Abort with an error message if any required file is missing (instruct the user to run missing prerequisite command).
For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

### 2. Load Artifacts (Progressive Disclosure)

Load only the minimal necessary context from each artifact:

**From concept.md (if exists):**

- Feature Hierarchy (EPIC-NNN.FNN.SNN IDs)
- User Journeys (J001, J002)
- Cross-Feature Dependencies matrix
- Traceability Skeleton (which stories have specs)
- Ideas Backlog (for completeness check)

**From spec.md:**

- **Concept Reference**: Source Concept, Concept IDs Covered
- **User Stories**: Priorities (P1a, P1b, P2a), Independent Tests
- **Acceptance Scenarios**: IDs (AS-1A, AS-1B), Given/When/Then tables
- **Functional Requirements**: IDs (FR-001, FR-002), links to AS
- **Edge Cases**: IDs (EC-001, EC-002)
- **Success Criteria**: IDs (SC-001, SC-002)
- **Traceability Summary** table

**From plan.md:**

- Architecture/stack choices
- Data Model references
- Phases
- Technical constraints

**From tasks.md:**

- Task IDs (T001, T002, ...)
- **[DEP:T001,T002]** markers (dependency references)
- **[FR:FR-001]** markers (requirement links)
- **[TEST:AS-1A]** markers (acceptance scenario links)
- **[P]** markers (parallelizable)
- **[USn]** markers (user story assignment)
- Dependency Graph (Mermaid)
- Requirements Traceability Matrix
- Coverage Summary

**From constitution:**

- Load `/memory/constitution.md` for principle validation

### 3. Build Semantic Models

Create internal representations (do not include raw artifacts in output):

- **Requirements inventory**: Each functional + non-functional requirement with a stable key (derive slug based on imperative phrase; e.g., "User can upload file" → `user-can-upload-file`)
- **User story/action inventory**: Discrete user actions with acceptance criteria
- **Task coverage mapping**: Map each task to one or more requirements or stories (inference by keyword / explicit reference patterns like IDs or key phrases)
- **Constitution rule set**: Extract principle names and MUST/SHOULD normative statements

### 4. Detection Passes (Token-Efficient Analysis)

Focus on high-signal findings. Limit to 50 findings total; aggregate remainder in overflow summary.

#### A. Duplication Detection

- Identify near-duplicate requirements
- Mark lower-quality phrasing for consolidation

#### B. Ambiguity Detection

- Flag vague adjectives (fast, scalable, secure, intuitive, robust) lacking measurable criteria
- Flag unresolved placeholders (TODO, TKTK, ???, `<placeholder>`, etc.)

#### C. Underspecification

- Requirements with verbs but missing object or measurable outcome
- User stories missing acceptance criteria alignment
- Tasks referencing files or components not defined in spec/plan

#### D. Constitution Alignment

- Any requirement or plan element conflicting with a MUST principle
- Missing mandated sections or quality gates from constitution

#### E. Coverage Gaps

- Requirements with zero associated tasks
- Tasks with no mapped requirement/story
- Non-functional requirements not reflected in tasks (e.g., performance, security)

#### F. Inconsistency

- Terminology drift (same concept named differently across files)
- Data entities referenced in plan but absent in spec (or vice versa)
- Task ordering contradictions (e.g., integration tasks before foundational setup tasks without dependency note)
- Conflicting requirements (e.g., one requires Next.js while other specifies Vue)

#### G. Dependency Graph Validation

**Parse [DEP:] markers and validate the dependency DAG:**

```
1. Build directed graph:
   FOR EACH task with [DEP:Txxx,Tyyy]:
     Add edges: Txxx → task, Tyyy → task

2. Cycle Detection:
   Run topological sort on graph
   IF cycle detected:
     - Report as CRITICAL: "Circular dependency: T005 → T012 → T014 → T005"
     - Identify weakest link to break cycle

3. Orphan Detection:
   IF task referenced in [DEP:] does not exist:
     - Report as HIGH: "Invalid dependency reference: T099 (not found)"

4. Phase Order Validation:
   IF user story task depends on task from later phase:
     - Report as MEDIUM: "T015 [US1] depends on T025 [US2] - cross-story dependency"
```

#### H. Traceability Validation

**Validate FR → Task → Test chains:**

```
1. FR Coverage Check:
   FOR EACH FR-xxx in spec.md:
     Find tasks with [FR:FR-xxx] marker
     IF no tasks found:
       Report as HIGH: "FR-xxx has no implementation tasks"

2. AS Coverage Check (if tests requested):
   FOR EACH AS-xxx in spec.md:
     Find test tasks with [TEST:AS-xxx] marker
     IF no test found:
       Report as MEDIUM: "AS-xxx has no test task"

3. Orphan Task Check:
   FOR EACH task in User Story phase (not Setup/Foundation/Polish):
     IF task has no [FR:] marker:
       Report as LOW: "T0xx has no requirement link"

4. Bidirectional Validation:
   FOR EACH [FR:] marker in tasks.md:
     Verify FR-xxx exists in spec.md
     IF not found:
       Report as HIGH: "Task references non-existent FR-xxx"
```

#### I. Concept Coverage (if concept.md exists)

**Validate concept → spec traceability:**

```
1. Story Coverage:
   FOR EACH story ID in concept.md Feature Hierarchy (EPIC-xxx.Fxx.Sxx):
     Check Traceability Skeleton for "Spec Created: [x]"
     IF not checked:
       Report as MEDIUM: "EPIC-001.F01.S03 has no specification"

2. Concept Reference Validation:
   FOR EACH spec.md in specs/NNN-feature/:
     Check "Concept IDs Covered" field
     IF concept.md exists but no Concept IDs:
       Report as LOW: "Spec has no link to concept hierarchy"

3. Ideas Backlog Review:
   Count items in Ideas Backlog
   IF items marked [?] (needs validation) > 10:
     Report as LOW: "N ideas need validation in concept backlog"

4. Journey Coverage:
   FOR EACH User Journey in concept.md:
     Verify all referenced features have specs
     IF feature missing spec:
       Report as MEDIUM: "Journey J001 references unspecified feature"
```

#### J. RTM (Requirements Traceability Matrix) Validation

**Validate the RTM in tasks.md matches reality:**

```
1. RTM Completeness:
   Compare RTM table with actual [FR:] markers in tasks
   IF mismatch:
     Report as LOW: "RTM shows T012 for FR-001 but T012 lacks [FR:FR-001]"

2. Coverage Summary Accuracy:
   Recalculate coverage percentages
   IF difference > 5%:
     Report as LOW: "Coverage Summary outdated (shows 80%, actual 65%)"

3. Gaps Identified Validation:
   Verify "Gaps Identified" section matches actual gaps
   IF gap exists but not listed:
     Report as LOW: "Undocumented gap: EC-003 has no handling"
```

#### K. System Spec Impact Validation

**Validate System Spec Impact section in feature specs:**

```
1. Section Existence:
   IF feature spec lacks "System Spec Impact" section:
     Report as MEDIUM: "Missing System Spec Impact section (required for /speckit.merge)"

2. Creates Validation:
   FOR EACH entry in "Creates" table:
     IF path format invalid (not system/domain/name.md):
       Report as LOW: "Invalid system spec path format: {path}"
     IF system spec already exists at path:
       Report as HIGH: "System spec already exists: {path} - should be in Updates"

3. Updates Validation:
   FOR EACH entry in "Updates" table:
     IF system spec doesn't exist at path:
       Report as HIGH: "System spec not found: {path} - should be in Creates"
     IF no changes described:
       Report as LOW: "Empty changes description for {path}"

4. Breaking Changes Validation:
   FOR EACH entry in "Breaking Changes" table:
     IF no migration path provided:
       Report as HIGH: "Breaking change without migration path: {path}"
     IF system spec not in Updates:
       Report as MEDIUM: "Breaking change for spec not listed in Updates"

5. No Impact Check:
   IF "No Impact" checkboxes are checked AND Creates/Updates have entries:
     Report as MEDIUM: "Contradictory: No Impact checked but specs listed"
   IF neither checkboxes checked NOR tables populated:
     Report as MEDIUM: "System Spec Impact section incomplete"
```

#### L. System Spec Integrity Validation (if specs/system/ exists)

**Validate living system specs for integrity:**

```
1. Dependency Graph:
   FOR EACH system spec in specs/system/:
     Parse "Dependencies" table
     Build directed graph
     IF dependency references non-existent spec:
       Report as HIGH: "Broken dependency: {spec} → {missing_spec}"
     IF circular dependency detected:
       Report as CRITICAL: "Circular system spec dependency: {cycle}"

2. Orphan Detection:
   FOR EACH system spec:
     IF not referenced in any feature's "System Spec Impact":
       IF Spec History has only MAINTENANCE entries:
         Report as LOW: "Orphan system spec: {path} (no features reference it)"

3. Stale Detection:
   FOR EACH system spec:
     Parse "Last Updated" date
     IF last updated > 180 days ago:
       Report as LOW: "Potentially stale system spec: {path} (not updated in 6+ months)"

4. Version Consistency:
   FOR EACH system spec:
     Parse latest version from Spec History
     IF version format inconsistent (mix of 1.0, v1.0, 1.0.0):
       Report as LOW: "Inconsistent version format in {path}"

5. Dependents Accuracy:
   FOR EACH system spec with Dependents table:
     Verify each listed dependent actually has this spec in Dependencies
     IF mismatch:
       Report as LOW: "Dependents table out of sync in {path}"
```

#### M. Impact Analysis (if --impact flag provided)

**When analyzing impact of a specific system spec change:**

```
1. Parse target spec path from arguments
2. Build reverse dependency graph (who depends on this spec)
3. For each dependent:
   - List potential impact
   - Flag active features that reference this spec
4. Output Impact Report:
   - Direct dependents
   - Transitive dependents (2nd degree)
   - Active features affected
   - Suggested review checklist
```

#### N. Code Traceability Validation

**Purpose**: Validate bidirectional links between spec requirements and code annotations.

**Annotation Pattern**: `@speckit:(FR|AS|EC|VR|IR):([A-Z]+-\d+[A-Za-z]?)(,([A-Z]+-\d+[A-Za-z]?))*`

**Scan directories**: `src/`, `backend/`, `frontend/`, `lib/`, `app/`, `tests/`, `test/`
**Scan extensions**: `.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.go`, `.rs`, `.java`, `.kt`, `.swift`, `.rb`, `.cpp`, `.c`, `.h`
**Exclusions**: `node_modules/`, `venv/`, `.git/`, `dist/`, `build/`, `__pycache__/`

```
1. Build Annotation Inventory:
   FOR EACH source file in scan directories:
     Extract @speckit:<TYPE>:<ID> patterns
     Store: {file, line_number, type, ids[], description}

2. Forward Traceability (Spec → Code):
   FOR EACH FR-xxx in spec.md Functional Requirements:
     Search for @speckit:FR:FR-xxx in code inventory
     IF not found:
       → MEDIUM: "FR-xxx has no code annotation"
       → Suggest: "Add @speckit:FR:FR-xxx to implementation file"

3. Backward Traceability (Code → Spec):
   FOR EACH @speckit:FR:FR-xxx annotation in code:
     Verify FR-xxx exists in spec.md
     IF not found:
       → HIGH: "Code references non-existent FR-xxx in {file}:{line}"
       → Suggest: "Remove orphan annotation or add FR-xxx to spec"

4. Task-to-Code Consistency:
   FOR EACH task in tasks.md with [FR:FR-xxx] marker:
     Extract expected file path from task description
     Check if file contains @speckit:FR:FR-xxx
     IF file exists but missing annotation:
       → LOW: "Task T012 claims FR-001 in {file} but no @speckit annotation found"

5. Test Coverage Validation:
   FOR EACH AS-xxx in spec.md Acceptance Scenarios:
     Search for @speckit:AS:AS-xxx in test files
     IF not found:
       → MEDIUM: "AS-xxx has no test annotation"
       → Suggest: "Add @speckit:AS:AS-xxx to test function"

6. Edge Case Coverage:
   FOR EACH EC-xxx in spec.md Edge Cases:
     Search for @speckit:EC:EC-xxx in code
     IF not found:
       → LOW: "EC-xxx has no code annotation"
```

#### O. Annotation Freshness Check

**Purpose**: Detect stale annotations when spec has been modified.

```
1. Get spec modification date from git or file timestamp

2. FOR EACH @speckit annotation in code:
   a) Verify referenced requirement still exists in spec.md
   b) IF requirement was removed from spec:
      → MEDIUM: "Orphan annotation in {file}:{line} - FR-xxx no longer in spec"
   c) IF spec file modified more recently than code file:
      → LOW: "Annotation in {file}:{line} may be stale - spec.md was modified"

3. Orphan Detection Summary:
   Count annotations referencing non-existent requirements
   IF orphan_count > 0:
     → Report total orphan annotations requiring cleanup
```

#### P. Brownfield Consistency Validation *(if Change Specification section exists)*

**Purpose**: Validate brownfield change specifications for completeness and consistency.

```
1. Change Specification Section Presence:
   IF spec contains brownfield keywords but no "Change Specification" section:
     → MEDIUM: "Brownfield indicators detected but no Change Specification section"
     → Suggest: "Add Change Specification section or confirm greenfield project"

2. Current State Completeness:
   FOR EACH CB-xxx in Current State Analysis:
     IF Component column is empty:
       → HIGH: "CB-xxx missing component identification"
     IF Current Behavior column is empty:
       → HIGH: "CB-xxx missing behavior description"
     IF Code Location provided AND file doesn't exist:
       → MEDIUM: "CB-xxx references non-existent file: {path}"

3. Limitation-to-Change Linkage:
   FOR EACH CL-xxx in Current Limitations:
     Search Change Delta for CHG-xxx that references CL-xxx
     IF no CHG-xxx addresses this limitation:
       → HIGH: "CL-xxx has no change request addressing it"
       → Suggest: "Add CHG-xxx with 'Addresses Limitation: CL-xxx'"

4. Change Delta Validation:
   FOR EACH CHG-xxx in Change Delta:
     a) IF Delta Type is MODIFY/REPLACE:
        IF From (CB) column is empty or "N/A":
          → HIGH: "CHG-xxx modifies behavior but no current state (CB) reference"
     b) IF Delta Type is ADD:
        IF From (CB) is NOT "N/A":
          → LOW: "CHG-xxx is ADD but references existing CB - should be MODIFY?"
     c) IF Impact Scope is empty:
        → MEDIUM: "CHG-xxx missing impact scope"

5. Delta-to-Requirement Mapping:
   FOR EACH CHG-xxx in Change Delta:
     Search Delta Requirements table
     IF CHG-xxx not in Delta Requirements:
       → HIGH: "CHG-xxx has no functional requirements mapped"
   FOR EACH FR-xxx in Delta Requirements:
     Verify FR-xxx exists in Functional Requirements section
     IF not found:
       → HIGH: "Delta Requirements references non-existent FR-xxx"

6. Preserved Behavior Coverage:
   FOR EACH PB-xxx in Preserved Behaviors:
     IF Current Implementation (CB) column is empty:
       → MEDIUM: "PB-xxx missing CB reference"
     IF Regression Test Required = Yes:
       Search tasks.md for [REG:PB-xxx] marker
       IF not found:
         → HIGH: "PB-xxx requires regression test but no [REG:PB-xxx] task found"

7. Baseline Reference Check:
   IF baseline.md exists in FEATURE_DIR:
     Compare CB-xxx count in spec vs baseline
     IF spec CB count < baseline component count:
       → LOW: "Baseline has more components than documented in spec"
```

#### Q. Migration Validation *(if Change Type = Migration)*

**Purpose**: Validate migration-specific requirements for completeness.

```
1. Migration Plan Presence:
   IF Change Type = Migration AND no Migration Plan section:
     → CRITICAL: "Migration change type requires Migration Plan section"

2. Migration Phase Completeness:
   FOR EACH MIG-xxx in Migration Plan:
     IF Description is empty:
       → HIGH: "MIG-xxx missing description"
     IF Duration is empty:
       → MEDIUM: "MIG-xxx missing duration estimate"
     IF Rollback Plan is empty:
       → CRITICAL: "MIG-xxx missing rollback plan - migrations must be reversible"

3. Dual-Mode Period Validation:
   IF Migration Strategy is "Parallel Run" or "Feature Flag":
     IF Dual-Mode Period not specified:
       → MEDIUM: "Parallel run/feature flag strategy requires dual-mode period"

4. Deprecation Timeline Validation:
   FOR EACH entry in Deprecation Timeline:
     IF Deprecation Date is in past:
       → MEDIUM: "Deprecation date for {component} is in the past"
     IF Removal Date <= Deprecation Date:
       → HIGH: "Removal date must be after deprecation date for {component}"
     IF Migration Path is empty:
       → HIGH: "No migration path for deprecated {component}"

5. Migration Task Coverage:
   FOR EACH MIG-xxx in Migration Plan:
     Search tasks.md for [MIG:MIG-xxx] marker
     IF not found:
       → HIGH: "MIG-xxx has no implementation task"
     Search tasks.md for [ROLLBACK:MIG-xxx] marker
     IF not found:
       → MEDIUM: "MIG-xxx has no rollback task"

6. Rollback Criteria Validation:
   IF Rollback Criteria section is empty:
     → HIGH: "Migration requires rollback criteria"
   FOR EACH criteria:
     IF Threshold is empty:
       → MEDIUM: "Rollback criteria missing threshold"
     IF Action is empty:
       → MEDIUM: "Rollback criteria missing action"

7. Feature Flag Recommendation:
   IF Migration affects > 3 CHG-xxx entries:
     IF Migration Strategy != "Feature Flag":
       → LOW: "Consider Feature Flag strategy for large migrations"
```

### 5. Severity Assignment

Use this heuristic to prioritize findings:

- **CRITICAL**:
  - Violates constitution MUST
  - Missing core spec artifact
  - Requirement with zero coverage that blocks baseline functionality
  - **Circular dependency in task graph** (blocks execution)
  - **Invalid dependency reference** (task references non-existent task)
  - **Circular system spec dependency** (blocks merge)
  - **Migration without Migration Plan** (brownfield Migration type)
  - **Migration phase without rollback plan** (MIG-xxx missing rollback)

- **HIGH**:
  - Duplicate or conflicting requirement
  - Ambiguous security/performance attribute
  - Untestable acceptance criterion
  - **FR with no implementation tasks** (requirement gap)
  - **Task references non-existent FR** (broken traceability)
  - **System spec already exists** (Creates lists existing spec)
  - **System spec not found** (Updates lists non-existent spec)
  - **Breaking change without migration path** (incomplete documentation)
  - **Broken system spec dependency** (missing referenced spec)
  - **Code references non-existent requirement** (orphan @speckit annotation)
  - **CB-xxx missing behavior description** (brownfield current state incomplete)
  - **CL-xxx has no change addressing it** (limitation without resolution)
  - **CHG-xxx modifies without CB reference** (change without baseline)
  - **CHG-xxx has no requirements mapped** (untracked change)
  - **PB-xxx requires regression but no [REG:] task** (unprotected behavior)
  - **MIG-xxx has no implementation task** (migration gap)
  - **Removal/Deprecation date order invalid** (timeline error)

- **MEDIUM**:
  - Terminology drift
  - Missing non-functional task coverage
  - Underspecified edge case
  - **AS with no test task** (test gap, if tests requested)
  - **Concept story without specification** (idea loss)
  - **Cross-story dependency** (may affect parallelization)
  - **Journey references unspecified feature** (incomplete planning)
  - **Missing System Spec Impact section** (required for merge)
  - **Breaking change for unlisted spec** (inconsistent documentation)
  - **Contradictory No Impact** (checkbox conflicts with tables)
  - **FR with no code annotation** (forward traceability gap)
  - **AS with no test annotation** (test coverage gap)
  - **Orphan annotation** (spec requirement removed)
  - **Brownfield indicators without Change Specification** (mode mismatch)
  - **CB-xxx references non-existent file** (invalid code location)
  - **CHG-xxx missing impact scope** (incomplete change definition)
  - **PB-xxx missing CB reference** (preserved behavior not linked)
  - **MIG-xxx missing rollback task** (incomplete migration)
  - **Dual-mode period not specified** (parallel run/feature flag)
  - **Deprecation date is in the past** (outdated timeline)
  - **Rollback criteria missing threshold/action** (incomplete safety)

- **LOW**:
  - Style/wording improvements
  - Minor redundancy not affecting execution order
  - **Task missing FR link** (traceability hygiene)
  - **Spec missing concept reference** (traceability hygiene)
  - **RTM accuracy mismatch** (documentation drift)
  - **Coverage summary outdated** (stale metrics)
  - **Undocumented gaps** (incomplete gap tracking)
  - **Invalid system spec path format** (naming convention)
  - **Empty changes description** (incomplete documentation)
  - **Orphan system spec** (no features reference it)
  - **Stale system spec** (not updated in 6+ months)
  - **Inconsistent version format** (version hygiene)
  - **Dependents table out of sync** (cross-reference accuracy)
  - **Task claims file but no annotation** (documentation hygiene)
  - **EC with no annotation** (edge case not marked)
  - **Potentially stale annotation** (spec modified since annotation)
  - **CHG-xxx ADD but references CB** (should be MODIFY?)
  - **Baseline has more components than spec CB count** (incomplete mapping)
  - **Consider Feature Flag for large migrations** (>3 CHG-xxx)

### 6. Produce Compact Analysis Report

Output a Markdown report (no file writes) with the following structure:

## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | Duplication | HIGH | spec.md:L120-134 | Two similar requirements ... | Merge phrasing; keep clearer version |
| G1 | Dependency | CRITICAL | tasks.md | Circular: T005 → T012 → T005 | Break cycle at T012 → T005 |
| H1 | Traceability | HIGH | spec.md, tasks.md | FR-003 has no tasks | Add [FR:FR-003] to relevant task |

(Add one row per finding; generate stable IDs prefixed by category initial: A=Dup, B=Ambig, C=Underspec, D=Constitution, E=Coverage, F=Inconsist, G=Depend, H=Trace, I=Concept, J=RTM, K=SysImpact, L=SysInteg, M=Impact, N=CodeTrace, O=Freshness, P=Brownfield, Q=Migration)

**Dependency Graph Status:**

```
Status: ✅ VALID | ⚠️ WARNINGS | ❌ INVALID
Cycles: [count] | Orphan Refs: [count] | Cross-Story Deps: [count]
```

**Traceability Coverage:**

| Type | Total | Covered | Coverage | Gaps |
|------|-------|---------|----------|------|
| Functional Requirements (FR) | N | M | X% | FR-003, FR-007 |
| Acceptance Scenarios (AS) | N | M | X% | AS-2B |
| Edge Cases (EC) | N | M | X% | EC-003 |

**Concept Coverage:** (if concept.md exists)

| Type | Total | Specified | Coverage |
|------|-------|-----------|----------|
| Stories (EPIC-x.Fx.Sx) | N | M | X% |
| Journeys (J00x) | N | M | X% |
| Ideas Backlog | N | N validated | - |

**System Spec Status:** (if specs/system/ exists)

```
System Specs: N total | N active | N deprecated
Dependency Graph: ✅ VALID | ⚠️ WARNINGS | ❌ INVALID
Stale Specs: N (>6 months without update)
```

| System Spec | Status | Version | Last Feature | Issues |
|-------------|--------|---------|--------------|--------|
| `system/auth/login.md` | ACTIVE | 1.1 | 009-2fa | - |
| `system/auth/2fa.md` | ACTIVE | 1.0 | 009-2fa | - |

**System Spec Impact Analysis:** (current feature)

| Action | System Spec | Valid? | Issues |
|--------|-------------|--------|--------|
| CREATE | `system/auth/sso.md` | ✅ | - |
| UPDATE | `system/auth/login.md` | ✅ | - |

**Code Traceability Status:** (if code exists)

```
Annotations Scanned: N across M files
Forward Coverage (Spec→Code): X% (N/M FRs annotated)
Backward Validation: ✅ VALID | ⚠️ N orphan annotations
Test Annotations: N covering X% (N/M) AS scenarios
Edge Case Annotations: N covering X% (N/M) EC scenarios
```

| Requirement | Type | Task | File | Line | Status |
|-------------|------|------|------|------|--------|
| FR-001 | FR | T012 | src/models/user.py | 15 | ✅ OK |
| FR-002 | FR | T014 | - | - | ❌ GAP |
| AS-1A | AS | T020 | tests/test_auth.py | 42 | ✅ OK |
| EC-001 | EC | T025 | - | - | ⚠️ MISSING |

**Brownfield Status:** *(if Change Specification section exists)*

```
Mode: BROWNFIELD | Change Type: [Enhancement|Refactor|Migration|...]
Baseline: [baseline.md exists | not generated]
```

| Category | Total | Validated | Coverage |
|----------|-------|-----------|----------|
| Current Behaviors (CB) | N | M | X% |
| Limitations (CL) | N | M addressed | X% |
| Changes (CHG) | N | M with FR | X% |
| Preserved Behaviors (PB) | N | M with [REG:] | X% |

**Change Traceability Chain:**

| Limitation | Change | Delta Type | Requirements | Tasks | Status |
|------------|--------|------------|--------------|-------|--------|
| CL-001 | CHG-001 | ADD | FR-001, FR-002 | T012, T014 | ✅ Complete |
| CL-002 | CHG-002 | MODIFY | FR-003 | - | ❌ No tasks |

**Migration Status:** *(if Change Type = Migration)*

```
Strategy: [Big Bang|Parallel Run|Strangler Fig|Feature Flag]
Phases: N total | N with tasks | N with rollback
Dual-Mode Period: [specified/not specified]
```

| Phase | MIG ID | Implementation | Rollback | Status |
|-------|--------|----------------|----------|--------|
| Phase 1 | MIG-001 | T040, T041 | T045 | ✅ Complete |
| Phase 2 | MIG-002 | - | - | ❌ No tasks |

**Requirements Coverage:**

| Requirement Key | Has Task? | Task IDs | Has Test? | Test IDs | Notes |
|-----------------|-----------|----------|-----------|----------|-------|
| FR-001 | ✅ | T012, T013 | ✅ | T020 | - |
| FR-002 | ✅ | T014 | ❌ | - | Missing test |

**Constitution Alignment Issues:** (if any)

**Unmapped Tasks:** (if any)

**Metrics:**

| Category | Count |
|----------|-------|
| Total Requirements (FR) | N |
| Total Acceptance Scenarios (AS) | N |
| Total Tasks | N |
| FR Coverage % | X% |
| AS Coverage % | X% |
| Dependency Cycles | 0 |
| Invalid References | 0 |
| Ambiguity Count | N |
| Duplication Count | N |
| Critical Issues | N |
| High Issues | N |
| Medium Issues | N |
| Low Issues | N |

### 7. Provide Next Actions

At end of report, output a concise Next Actions block:

- If CRITICAL issues exist: Recommend resolving before `/speckit.implement`
- If only LOW/MEDIUM: User may proceed, but provide improvement suggestions
- Provide explicit command suggestions: e.g., "Run /speckit.specify with refinement", "Run /speckit.plan to adjust architecture", "Manually edit tasks.md to add coverage for 'performance-metrics'"

### 8. Offer Remediation

Ask the user: "Would you like me to suggest concrete remediation edits for the top N issues?" (Do NOT apply them automatically.)

## Operating Principles

### Context Efficiency

- **Minimal high-signal tokens**: Focus on actionable findings, not exhaustive documentation
- **Progressive disclosure**: Load artifacts incrementally; don't dump all content into analysis
- **Token-efficient output**: Limit findings table to 50 rows; summarize overflow
- **Deterministic results**: Rerunning without changes should produce consistent IDs and counts

### Analysis Guidelines

- **NEVER modify files** (this is read-only analysis)
- **NEVER hallucinate missing sections** (if absent, report them accurately)
- **Prioritize constitution violations** (these are always CRITICAL)
- **Use examples over exhaustive rules** (cite specific instances, not generic patterns)
- **Report zero issues gracefully** (emit success report with coverage statistics)

## Automation Behavior

When this command completes successfully, the following automation rules apply:

### Auto-Transitions

| Condition | Next Phase | Gate |
|-----------|------------|------|
| Analysis complete, no CRITICAL issues, dependency graph valid | `/speckit.implement` | No Critical Issues Gate, Dependency Graph Valid Gate |

### Quality Gates

| Gate | Check | Block Condition | Message |
|------|-------|-----------------|---------|
| No Critical Issues Gate | CRITICAL issue count == 0 | CRITICAL > 0 | "Cannot proceed to implementation: resolve all CRITICAL issues first" |
| Dependency Graph Valid Gate | Dependency Graph Status == VALID or WARNINGS | Status == INVALID | "Resolve circular dependencies or invalid references before implementation" |

### Gate Behavior

**If all conditions pass and no gates block:**
- Automatically proceed to `/speckit.implement`
- Log transition for audit trail

**If gates block:**
- Display blocking message to user
- List all CRITICAL issues requiring resolution
- Offer handoffs to fix issues:
  - `/speckit.specify` for spec issues
  - `/speckit.plan` for architectural issues
  - `/speckit.tasks` for traceability issues
- Wait for user to resolve and re-run analysis

### Manual Overrides

Users can always choose to:
- Fix specific issues and re-run `/speckit.analyze`
- Skip to specific handoff for targeted fixes
- Proceed manually (not recommended if CRITICAL issues exist)
- Return to earlier phases if fundamental issues found

## Context

{ARGS}
