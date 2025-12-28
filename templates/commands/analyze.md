---
description: Perform a non-destructive cross-artifact consistency, traceability, dependency, and system spec analysis across concept.md, spec.md, plan.md, tasks.md, and system specs. In QA mode (post-implementation), validates build, tests, coverage, and security.
persona: qa-agent
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
      - "Analysis completed successfully (pre-implementation mode)"
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
  - label: Fix QA Issues
    agent: speckit.implement
    prompt: Address issues identified in QA verification report
    auto: false
    condition:
      - "QA mode analysis found CRITICAL or HIGH issues"
      - "Tests failed or build broken"
    gates:
      - name: "QA Issues Exist Gate"
        check: "QA Verdict == FAIL"
        block_if: "QA Verdict == PASS"
        message: "No QA issues to fix - all checks passed"
  - label: QA Complete
    agent: none
    prompt: QA verification passed - implementation ready for merge
    auto: true
    condition:
      - "QA mode analysis completed"
      - "QA Verdict == PASS or CONCERNS"
    gates:
      - name: "QA Pass Gate"
        check: "No CRITICAL or HIGH issues in QA categories (R-U)"
        block_if: "CRITICAL > 0 OR HIGH > 0 in R-U categories"
        message: "QA failed - fix blocking issues before proceeding"
    post_actions:
      - "log: QA verification passed, ready for merge"
claude_code:
  model: sonnet
  reasoning_mode: extended
  thinking_budget: 12000
  subagents:
    - role: code-explorer
      trigger: "when tracing implementation coverage or validating file references"
      prompt: "Explore codebase for {PATTERN} to validate implementation coverage"
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
validation_profiles:
  spec_validate:
    description: "Lightweight spec validation for auto-gating before plan"
    passes: [B, D]
    gates:
      constitution_alignment:
        pass: D
        threshold: 0
        severity: CRITICAL
      ambiguity_count:
        pass: B
        threshold: 5
        severity: HIGH
    timeout_seconds: 30
    output_mode: compact
  plan_validate:
    description: "Plan consistency validation before task generation"
    passes: [D, F, V]
    gates:
      constitution_alignment:
        pass: D
        threshold: 0
        severity: CRITICAL
      tech_consistency:
        pass: F
        threshold: 0
        severity: HIGH
    timeout_seconds: 45
    output_mode: compact
  tasks_validate:
    description: "Task graph validation before implementation"
    passes: [G, H, J]
    gates:
      no_circular_deps:
        pass: G
        threshold: 0
        severity: CRITICAL
      fr_coverage:
        pass: H
        threshold: 0
        severity: HIGH
    timeout_seconds: 30
    output_mode: compact
  full:
    description: "Complete pre-implementation analysis"
    passes: [A, B, C, D, E, F, G, H, I, J, K, L, L2, M, N, O, P, Q]
    timeout_seconds: 300
    output_mode: detailed
  qa:
    description: "Post-implementation QA verification"
    passes: [A, B, C, D, E, F, G, H, I, J, K, L, L2, M, N, O, P, Q, R, S, T, U, V, W, X, Y]
    timeout_seconds: 600
    output_mode: detailed
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

## Profile-Based Execution

When invoked with `--profile <name>`, analyze runs a lightweight subset of passes optimized for specific validation gates. This enables proactive validation between workflow phases without the overhead of full analysis.

### Profile Detection

Parse `$ARGUMENTS` for profile mode:

```text
IF $ARGUMENTS contains "--profile <name>":
  PROFILE_MODE = true
  ACTIVE_PROFILE = validation_profiles[<name>]
  IF ACTIVE_PROFILE is undefined:
    ERROR: "Unknown profile: <name>. Available: spec_validate, plan_validate, tasks_validate, full, qa"
  ACTIVE_PASSES = ACTIVE_PROFILE.passes
  OUTPUT_MODE = ACTIVE_PROFILE.output_mode (default: compact)
  TIMEOUT = ACTIVE_PROFILE.timeout_seconds
ELSE:
  PROFILE_MODE = false
  ACTIVE_PASSES = [A-Y] (all passes)
  OUTPUT_MODE = detailed
```

### Profile Execution Flow

When `PROFILE_MODE = true`:

1. **Execute only ACTIVE_PASSES** from the Detection Passes section
2. **Skip all other passes** not in the profile
3. **Evaluate gates** defined in ACTIVE_PROFILE.gates:

```text
FOR EACH gate in ACTIVE_PROFILE.gates:
  PASS_RESULT = findings from gate.pass
  ISSUE_COUNT = count(PASS_RESULT where severity >= gate.severity)
  IF ISSUE_COUNT > gate.threshold:
    GATE_STATUS[gate.name] = FAIL
  ELSE:
    GATE_STATUS[gate.name] = PASS
```

4. **Generate compact output** (see Profile Output Format below)

### Profile Output Format (Compact)

When `OUTPUT_MODE = compact`, generate a condensed validation summary:

```markdown
## Validation Profile: {PROFILE_NAME}

| Gate | Pass | Threshold | Actual | Status |
|------|------|-----------|--------|--------|
| Constitution Alignment | D | 0 | {count} | {✅/❌} |
| Ambiguity Count | B | 5 | {count} | {✅/⚠️/❌} |

**Result**: {PASS | FAIL | WARN}

{IF any gates FAIL}
### Blocking Issues

{List only CRITICAL/HIGH findings from failed gates, max 5}

### Recommended Action

→ Auto-invoking `/speckit.clarify` with {N} extracted questions...
{OR}
→ Manual review required. Run `/speckit.clarify` to address ambiguities.
{ENDIF}

{IF all gates PASS}
→ Proceeding to next phase
{ENDIF}
```

### Available Profiles

| Profile | Passes | Use Case | Timeout |
|---------|--------|----------|---------|
| `spec_validate` | B, D | Pre-plan spec validation | 30s |
| `plan_validate` | D, F, V | Pre-tasks plan validation | 45s |
| `tasks_validate` | G, H, J | Pre-implement task validation | 30s |
| `full` | A-Q | Complete pre-implementation analysis | 300s |
| `qa` | A-Y | Post-implementation QA verification | 600s |

### Profile Flags

| Flag | Effect |
|------|--------|
| `--profile <name>` | Run specific validation profile |
| `--quiet` | Suppress non-essential output (only gates + result) |
| `--strict` | Lower thresholds (e.g., ambiguity < 3 instead of 5) |
| `--json` | Output as JSON for programmatic consumption |

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

```text
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

```text
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

```text
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

```text
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

```text
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

```text
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

#### L2. Feature Lineage Validation (if Feature Lineage section exists)

**Validate Feature Lineage for extension features:**

```text
1. Parent Existence:
   FOR EACH feature with "Feature Lineage" section:
     Parse parent feature reference from table
     PARENT_PATH = specs/features/{parent_name}/spec.md

     IF not exists(PARENT_PATH):
       Report as CRITICAL: "Feature Lineage references non-existent parent: {parent_name}"

2. Parent Status:
   FOR EACH parent reference:
     Check if parent feature is MERGED (has .merged marker)

     IF parent is not MERGED:
       Report as HIGH: "Feature Lineage extends non-merged feature: {parent_name}"
       Suggest: "Consider waiting for parent to merge or use standalone feature"

3. System Spec Consistency:
   FOR EACH parent reference:
     Parse "System Specs Affected" from Lineage table
     Parse parent's .merged file for system_specs_created/updated

     IF Lineage refs don't match parent's actual system specs:
       Report as MEDIUM: "System Specs Affected inconsistent with parent's .merged"
       List: Expected: {parent_specs}, Found: {lineage_specs}

4. Relationship Validity:
   FOR EACH Feature Lineage entry:
     Parse Relationship column

     IF Relationship NOT IN [EXTENDS, REFINES, FIXES, DEPRECATES]:
       Report as LOW: "Invalid relationship type: {relationship}"

5. Circular Extension Detection:
   Build extension graph from all Feature Lineage sections:
     FOR EACH feature with lineage:
       Add edge: parent → child

   Run cycle detection:
     IF cycle detected:
       Report as CRITICAL: "Circular feature extension: {cycle_path}"
       Example: "001-login → 015-rate-limiting → 025-auth-v2 → 001-login"

6. Extension Chain Depth:
   FOR EACH feature with lineage:
     Count extension chain depth (follow parent links)

     IF depth > 3:
       Report as LOW: "Deep extension chain ({depth} levels): Consider refactoring"

7. Manifest Consistency:
   IF manifest has "Extends" column:
     FOR EACH feature with Feature Lineage:
       Verify manifest Extends column matches spec's lineage

       IF mismatch:
         Report as MEDIUM: "Manifest Extends column inconsistent with spec's Feature Lineage"
```

**Lineage Tree Visualization (with --lineage flag):**

```text
IF --lineage flag provided:
  Build and display feature evolution tree:

  auth/login.md
  └── 001-login (MERGED) ─────────────── CREATES
      ├── 015-rate-limiting (MERGED) ─── EXTENDS
      │   └── 025-rate-limiting-v2 ───── REFINES
      ├── 018-login-bugfix (MERGED) ──── FIXES
      └── 023-2fa (IMPLEMENTING) ─────── EXTENDS

  Output tree as Mermaid diagram if requested:

  graph TD
    001[001-login] -->|CREATES| login.md
    015[015-rate-limiting] -->|EXTENDS| 001
    025[025-rate-limiting-v2] -->|REFINES| 015
    018[018-login-bugfix] -->|FIXES| 001
    023[023-2fa] -->|EXTENDS| 001
```

#### M. Impact Analysis (if --impact flag provided)

**When analyzing impact of a specific system spec change:**

```text
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

```text
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

```text
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

```text
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

```text
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

---

## QA Mode Categories (Post-Implementation)

The following categories (R-U) are executed when `/speckit.analyze` runs after `/speckit.implement` to perform **Quality Assurance validation**. These categories verify that the implementation meets specifications and quality standards.

**QA Mode Activation**: QA categories are triggered when:
- `tasks.md` contains completed tasks `[X]`
- User explicitly requests QA validation
- Auto-triggered via handoff from `/speckit.implement`

---

#### R. Build Validation

**Purpose**: Verify implementation builds and passes static analysis.

```text
1. Build System Detection:
   Detect build system from project files:
   - package.json → npm/yarn/pnpm build
   - Cargo.toml → cargo build
   - pyproject.toml → python build
   - go.mod → go build
   - Makefile → make
   - build.gradle → gradle build
   - pom.xml → mvn compile

2. Build Check:
   IF project has build system:
     Attempt build command
     IF build fails:
       → CRITICAL: "Build failed: {error_summary}"
       → Include first 10 error lines
     IF build succeeds with warnings > 10:
       → LOW: "Build warnings: {count}"

3. Lint Check:
   Detect linter configuration:
   - .eslintrc*, eslint.config.* → eslint
   - .pylintrc, pyproject.toml [tool.pylint] → pylint
   - .flake8, setup.cfg [flake8] → flake8
   - .rubocop.yml → rubocop
   - .golangci.yml → golangci-lint
   - rustfmt.toml, .rustfmt.toml → cargo fmt --check
   - Cargo.toml → cargo clippy

   IF linter configured:
     Run linter
     IF errors > 0:
       → HIGH: "Lint errors: {count}"
     IF warnings > threshold (default 20):
       → MEDIUM: "Lint warnings: {count} (threshold: {threshold})"

4. Type Check:
   Detect type system:
   - tsconfig.json → tsc --noEmit
   - pyproject.toml [tool.mypy] → mypy
   - py.typed marker → mypy

   IF type checker configured:
     Run type checker
     IF errors > 0:
       → HIGH: "Type errors: {count}"
```

#### S. Test Execution Validation

**Purpose**: Verify tests exist and pass.

```text
1. Test Discovery:
   Scan for test files in standard locations:
   - tests/, test/, __tests__/, spec/
   - *_test.*, test_*.*, *.test.*, *.spec.*

   Count test files and estimate test functions:
   - Python: def test_*, class Test*
   - JavaScript/TypeScript: describe(, it(, test(
   - Go: func Test*
   - Rust: #[test], #[cfg(test)]
   - Ruby: describe, it, context

   IF test_file_count == 0:
     → MEDIUM: "No test files found in standard locations"
     → Suggest: "Add tests in tests/ directory"

2. Test Runner Detection:
   Detect test runner from project configuration:
   - package.json scripts.test → npm test
   - pytest.ini, pyproject.toml [tool.pytest] → pytest
   - Cargo.toml → cargo test
   - go.mod → go test ./...
   - Gemfile (rspec) → rspec
   - jest.config.* → jest

3. Test Execution:
   IF test runner configured:
     Run test suite with timeout (5 min default)
     Parse test results:
     - passed: count
     - failed: count
     - skipped: count
     - total: count

     IF failures > 0:
       → CRITICAL: "Tests failed: {failed}/{total}"
       → List first 5 failed test names
     IF all pass:
       → Report: "Tests passed: {passed}/{total}"
     IF skipped > total * 0.2:
       → MEDIUM: "High skip rate: {skipped}/{total} tests skipped"

4. Coverage Check:
   Detect coverage configuration:
   - .coveragerc, pyproject.toml [tool.coverage] → coverage
   - package.json (nyc, c8, jest --coverage) → coverage
   - Cargo.toml → cargo tarpaulin or llvm-cov

   IF coverage tool configured:
     Get coverage percentage from report
     Extract threshold from spec.md NFRs or constitution
     Default threshold: 70%

     IF coverage < threshold:
       → HIGH: "Coverage {actual}% below required {threshold}%"
     IF coverage >= threshold:
       → Report: "Coverage: {actual}% (threshold: {threshold}%)"

5. Test-to-Scenario Mapping:
   FOR EACH AS-xxx in spec.md:
     Search for @speckit:AS:AS-xxx in test files
     IF test with annotation found:
       Verify test is in passed list
       IF test failed:
         → CRITICAL: "Acceptance scenario AS-xxx test failed"
```

#### T. Performance Baseline Validation

**Purpose**: Verify performance against spec NFRs.

```text
1. NFR Extraction:
   Parse Non-Functional Requirements from spec.md:
   - Response time thresholds (e.g., "< 200ms p99")
   - Throughput requirements (e.g., "> 1000 req/s")
   - Memory limits (e.g., "< 512MB")
   - Startup time (e.g., "< 5s cold start")

   Store as NFR_THRESHOLDS = {metric: value}

2. Performance Test Detection:
   Look for performance test configurations:
   - k6.js, k6.config.js → k6
   - locustfile.py → locust
   - artillery.yml → artillery
   - benchmark tests in test suite
   - package.json scripts (bench, perf)

3. Baseline Check:
   IF quickstart.md exists AND has performance scenarios:
     Extract documented performance baselines
     Compare against NFR thresholds

     FOR EACH nfr in NFR_THRESHOLDS:
       IF baseline exists for metric:
         IF baseline violates threshold:
           → HIGH: "Performance NFR violated: {metric} = {actual} (required: {threshold})"
       ELSE:
         → LOW: "No baseline measurement for NFR: {metric}"

4. Performance Regression:
   IF previous baseline exists (baseline.md or prior run):
     Compare current vs previous
     IF regression > 10%:
       → MEDIUM: "Performance regression: {metric} degraded by {percent}%"

5. Resource Utilization:
   IF spec.md specifies resource limits:
     Check application startup resource usage if measurable
     IF exceeds limits:
       → MEDIUM: "Resource limit exceeded: {resource} = {actual} (limit: {threshold})"
```

#### U. Security Validation

**Purpose**: Basic security checks for common vulnerabilities.

```text
1. Dependency Audit:
   Detect package manager:
   - package-lock.json, yarn.lock, pnpm-lock.yaml → npm audit / yarn audit
   - Pipfile.lock, requirements.txt → pip-audit, safety
   - Cargo.lock → cargo audit
   - go.sum → govulncheck
   - Gemfile.lock → bundle audit

   IF package manager detected:
     Run audit command
     Parse vulnerability report:
     - critical: count
     - high: count
     - moderate: count
     - low: count

     IF critical > 0:
       → CRITICAL: "Critical vulnerabilities: {count}"
       → List CVE IDs for critical
     IF high > 0:
       → HIGH: "High vulnerabilities: {count}"
     IF moderate > 10:
       → MEDIUM: "Moderate vulnerabilities: {count}"

2. Secret Detection:
   Scan source files for potential secrets:
   Patterns to detect:
   - API keys: /[A-Za-z0-9_]{20,}/
   - AWS keys: /AKIA[A-Z0-9]{16}/
   - Private keys: /-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----/
   - Passwords in code: /password\s*=\s*["'][^"']+["']/i
   - Connection strings: /mongodb(\+srv)?:\/\/[^@]+@/
   - JWT tokens: /eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*/

   Exclusions: test files, mock data, example configs

   IF potential secret found:
     → CRITICAL: "Potential secret in code: {file}:{line}"
     → Suggest: "Move to environment variable or secrets manager"

3. Security Headers (if web app):
   IF project is web application:
     Check for security middleware/headers configuration:
     - Content-Security-Policy
     - X-Frame-Options
     - X-Content-Type-Options
     - Strict-Transport-Security

     IF missing common security headers:
       → MEDIUM: "Missing security headers configuration"

4. Input Validation:
   Scan for common vulnerability patterns:
   - SQL injection: string concatenation in SQL queries
   - XSS: innerHTML without sanitization
   - Command injection: shell execution with user input

   IF vulnerability pattern detected:
     → HIGH: "Potential {vulnerability_type} in {file}:{line}"

5. OWASP Top 10 Quick Check:
   Scan for patterns matching OWASP Top 10:
   - A01: Broken Access Control (missing auth checks)
   - A02: Cryptographic Failures (weak algorithms, hardcoded keys)
   - A03: Injection (as above)
   - A04: Insecure Design (documented in spec analysis)
   - A07: Auth Failures (default credentials, weak password policy)

   Report as advisory findings with educational context.
```

---

#### V. API Documentation Validation

**Purpose**: Verify all API references are valid and documented to prevent AI hallucinations.

```text
1. Dependency Registry Completeness:
   IF plan.md exists:
     FOR EACH entry in Dependency Registry:
       IF Documentation URL is empty or invalid:
         → HIGH: "Missing documentation URL for dependency: {dependency}"
       IF Version is "latest" or unspecified:
         → MEDIUM: "Unversioned dependency: {dependency} - pin to specific version"
       IF Key APIs Used is empty:
         → LOW: "No specific APIs documented for: {dependency}"

2. Task-to-Dependency Linkage:
   FOR EACH task in tasks.md with external integration indicators:
     Indicators: "API", "fetch", "request", "client", "SDK", "service" in description
     OR file paths matching: services/, api/, integrations/, clients/

     IF task lacks [DEP:xxx] marker:
       → MEDIUM: "Task {task_id} appears to use external API but has no [DEP:] marker"
     IF [DEP:xxx] references non-existent dependency in Registry:
       → HIGH: "Task {task_id} references undefined dependency: {dep_id}"

3. API Documentation Reference Check:
   FOR EACH [APIDOC:url] marker in tasks.md:
     IF URL format is not valid HTTP(S):
       → LOW: "Invalid APIDOC URL format in task {task_id}: {url}"
     SUGGEST: "Verify URL is accessible and points to correct API version"

4. Version Constraint Validation:
   FOR EACH [VERSION:x.y.z] marker in tasks.md:
     Look up dependency in Dependency Registry
     IF version constraint conflicts with Registry:
       → MEDIUM: "Version mismatch in {task_id}: task specifies {task_ver}, registry has {reg_ver}"

5. Deprecated API Detection:
   FOR EACH dependency in Dependency Registry:
     IF spec.md "Deprecated API Warnings" section mentions this dependency:
       Search tasks.md for deprecated method names
       IF found:
         → HIGH: "Task {task_id} may use deprecated API: {method}"
         → SUGGEST: "Replace with {replacement} per {migration_docs}"

6. External API Consistency:
   FOR EACH API-xxx in Dependency Registry:
     IF API Version not specified:
       → MEDIUM: "External API {name} missing version specification"
     IF Auth method not documented:
       → HIGH: "External API {name} missing authentication documentation"
     IF Rate Limits not documented:
       → LOW: "External API {name} missing rate limit documentation"

7. Context7 Verification (optional):
   IF Context7 MCP available AND --verify-docs flag provided:
     FOR EACH PKG-xxx in Dependency Registry:
       Call resolve-library-id with package name
       IF library not found:
         → HIGH: "Package {name} not found in Context7 registry"
       IF found:
         Call get-library-docs for key APIs
         FOR EACH API in "Key APIs Used":
           IF API not found in docs:
             → HIGH: "API {method} not found in {package} v{version} docs"
             → SUGGEST: "Verify method name or check for deprecation"
```

---

#### W. Test Specification Coverage

**Purpose**: Enforce bidirectional traceability between specs and tests, ensuring every testable scenario has coverage.

```text
1. Acceptance Scenario Test Coverage:
   FOR EACH AS-xxx in spec.md Acceptance Scenarios table:
     Extract "Requires Test" column value
     IF "Requires Test" = YES:
       Search tasks.md for [TEST:AS-xxx] marker
       IF not found:
         Search tasks.md TTM for AS-xxx row
         IF TTM row has "⏭️" status (skipped):
           Search for [NO-TEST:AS-xxx] justification
           IF justification empty or missing:
             → MEDIUM: "AS-xxx skipped without justification in TTM"
           ELSE:
             → INFO: "AS-xxx intentionally skipped: {justification}"
         ELSE:
           → HIGH: "AS-xxx requires test but no [TEST:AS-xxx] task found"
       IF found:
         → OK: "AS-xxx covered by test task"
     IF "Requires Test" = NO:
       IF [TEST:AS-xxx] exists:
         → INFO: "AS-xxx has test despite 'Requires Test = NO' (extra coverage)"

2. Test Task Validity:
   FOR EACH [TEST:xxx] marker in tasks.md:
     Extract spec ID (AS-xxx or EC-xxx)
     IF spec ID format invalid:
       → MEDIUM: "Invalid test marker format: [TEST:{marker}]"
     Search spec.md for matching AS-xxx or EC-xxx
     IF not found:
       → HIGH: "Test task references non-existent spec ID: {spec_id}"
     IF found:
       → OK: "Test task valid: covers {spec_id}"

3. Explicit Skip Validation:
   FOR EACH [NO-TEST:xxx] marker in tasks.md:
     Extract spec ID and justification
     IF justification missing or less than 10 characters:
       → MEDIUM: "[NO-TEST:{spec_id}] requires meaningful justification"
     IF justification present:
       Search TTM for matching row with "⏭️" status
       IF not found:
         → LOW: "[NO-TEST:{spec_id}] not reflected in TTM"
       → INFO: "Intentionally skipped: {spec_id} - {justification}"

4. Critical Edge Case Coverage:
   FOR EACH EC-xxx in spec.md Edge Cases table:
     IF Priority = "CRITICAL" OR Security-related (keywords: auth, inject, XSS, SQL, CSRF):
       Search tasks.md for [TEST:EC-xxx] marker
       IF not found:
         → HIGH: "Critical edge case EC-xxx has no test task"
       IF found:
         → OK: "Critical edge case EC-xxx covered"
     ELSE:
       IF [TEST:EC-xxx] not found:
         → LOW: "Non-critical edge case EC-xxx has no test"

5. TTM Completeness:
   IF TTM section exists in tasks.md:
     Count total AS-xxx with "Requires Test = YES" in spec.md
     Count AS-xxx rows in TTM
     IF counts differ:
       → MEDIUM: "TTM incomplete: {ttm_count}/{spec_count} testable AS documented"

     FOR EACH row in TTM:
       IF Status = "❌" AND Impl Task has completed status:
         → HIGH: "Implementation complete but test not written: {spec_id}"
       IF Test File column is "tests/..." (placeholder):
         IF Status = "✅":
           → MEDIUM: "Test marked passing but file path is placeholder: {spec_id}"

     Calculate coverage metrics:
       AS_YES_count = AS with Requires Test = YES
       AS_covered = AS_YES with Status ∈ {✅, 🔄}
       Coverage = AS_covered / AS_YES_count * 100
       IF Coverage < 100%:
         → MEDIUM: "Test coverage: {coverage}% ({AS_covered}/{AS_YES_count} AS)"

6. Test-Implementation Pairing:
   FOR EACH story in tasks.md User Stories:
     Collect test tasks [TEST:] in story
     Collect implementation tasks in story
     IF implementation tasks exist AND test tasks empty:
       IF any related AS has "Requires Test = YES":
         → HIGH: "Story {story_id} has implementation but no test tasks for required AS"

7. Annotation Reminder (advisory):
   FOR EACH test file in TTM with non-placeholder path:
     IF file exists on disk:
       Search file for @speckit:AS: or @speckit:EC: annotations
       IF not found:
         → LOW: "Test file {file} missing @speckit annotations for traceability"
```

**Severity Summary for Pass W:**
| Condition | Severity |
|-----------|----------|
| AS requires test but no [TEST:] task | HIGH |
| Test references non-existent spec ID | HIGH |
| Critical EC without test | HIGH |
| Implementation complete but test missing | HIGH |
| Story has impl but no tests for required AS | HIGH |
| [NO-TEST:] without justification | MEDIUM |
| TTM incomplete | MEDIUM |
| Invalid test marker format | MEDIUM |
| Test marked passing but placeholder path | MEDIUM |
| Non-critical EC without test | LOW |
| [NO-TEST:] not in TTM | LOW |
| Missing @speckit annotations | LOW |

---

#### X. UXQ Domain Validation *(if UXQ domain active)*

**Purpose**: Validate User Experience Quality principles when UXQ domain is active.

**Activation Check**:

```text
IF memory/constitution.domain.md exists:
  Read file content
  IF content references "uxq.md" OR contains "UXQ-":
    UXQ_DOMAIN_ACTIVE = true
  ELSE:
    UXQ_DOMAIN_ACTIVE = false
ELSE:
  UXQ_DOMAIN_ACTIVE = false

IF NOT UXQ_DOMAIN_ACTIVE:
  SKIP this validation pass
```

**1. UXQ Section Presence**:

```text
IF spec.md exists:
  Search for "## User Experience Quality" OR "## UXQ" section
  IF section not found:
    → CRITICAL: "UXQ domain active but spec.md missing UXQ section"
    → Suggest: "Add User Experience Quality section per UXQ domain requirements"

  IF section found:
    Verify subsections exist:
    - "Jobs to Be Done" OR "JTBD"
    - "User Mental Model"
    - "First-Time User Experience" OR "FTUE"
    - "Friction Points"

    FOR EACH missing subsection:
      → HIGH: "UXQ section missing required subsection: {name}"
```

**2. Jobs-to-Be-Done Traceability (UXQ-008)**:

```text
IF JTBD table exists in spec.md:
  FOR EACH JTBD-xxx entry:
    IF Job Statement column empty:
      → HIGH: "JTBD-xxx missing job statement"
    IF Job Statement not in format "When [situation], I want to [motivation], so I can [outcome]":
      → MEDIUM: "JTBD-xxx job statement not in standard format"
    IF Related FRs column empty:
      → HIGH: "JTBD-xxx has no related FRs"

  FOR EACH FR-xxx in Functional Requirements:
    Search JTBD table "Related FRs" columns for FR-xxx reference
    IF not found:
      → HIGH: "FR-xxx has no JTBD traceability (violates UXQ-008)"
      → Suggest: "Add JTBD entry for FR-xxx or link to existing JTBD"
```

**3. Friction Justification Validation (UXQ-003)**:

```text
IF Friction Points table exists:
  FOR EACH FP-xxx entry:
    IF Friction Point column empty:
      → HIGH: "FP-xxx missing friction point description"
    IF Type column NOT IN [SECURITY, LEGAL, DATA QUALITY, INTENTIONAL, TECHNICAL]:
      → LOW: "FP-xxx has non-standard friction type: {type}"
    IF Justification column empty:
      → CRITICAL: "FP-xxx has no justification (violates UXQ-003 MUST)"
      → Suggest: "Every friction point MUST document: why it exists, what value it provides"
    IF Mitigation column empty:
      → HIGH: "FP-xxx missing mitigation strategy"

ELSE:
  # Check if spec has friction indicators without table
  Search spec.md for friction keywords:
  - "user must wait", "requires confirmation", "additional step"
  - "verification", "manual", "delay", "approval needed"

  IF friction indicators found AND no Friction Points table:
    → MEDIUM: "Potential friction points detected but no Friction Points table"
    → Suggest: "Document friction points in Friction Points table with justifications"
```

**4. FTUE Documentation (UXQ-006)**:

```text
IF "First-Time User Experience" OR "FTUE" section exists:
  IF section content < 50 characters:
    → MEDIUM: "FTUE section is stub (too brief)"

  Search for FTUE elements:
  - Empty state handling
  - Progressive disclosure
  - Onboarding guidance
  - First meaningful action

  IF none found:
    → HIGH: "FTUE section lacks specific guidance (violates UXQ-006)"
    → Suggest: "Document: empty states, progressive disclosure, first meaningful action"

ELSE:
  → HIGH: "Missing FTUE section (violates UXQ-006 MUST)"
```

**5. Mental Model Alignment (UXQ-001)**:

```text
IF "User Mental Model" section exists:
  IF section content < 100 characters:
    → MEDIUM: "Mental Model section is too brief"

  # Check for jargon vs user vocabulary
  Search spec.md for technical jargon markers:
  - Database table names (snake_case, ALL_CAPS)
  - Technical acronyms not in Glossary
  - Implementation terms ("repository", "service layer", "controller")

  IF technical jargon found in user-facing descriptions:
    → MEDIUM: "Technical jargon in user-facing content (violates UXQ-001)"
    → Suggest: "Replace '{jargon}' with user vocabulary"

ELSE:
  → HIGH: "Missing User Mental Model section (violates UXQ-001)"
```

**6. Error Empathy Check (UXQ-005)**:

```text
Search spec.md for error handling sections:
- "Error Handling", "Error Messages", "Edge Cases"

FOR EACH error scenario found:
  Check if error description includes:
  - User perspective explanation (what went wrong for user)
  - Action guidance (what user can do)

  IF error is system-centric only ("500 Internal Server Error", "Database timeout"):
    → MEDIUM: "Error scenario lacks user empathy (violates UXQ-005)"
    → Suggest: "Reframe error from user perspective with actionable guidance"
```

**7. Accessibility Empowerment (UXQ-010)**:

```text
IF spec.md contains accessibility sections (A11y, Accessibility, WCAG):
  Check framing:
  - "compliance" only → MEDIUM: "Accessibility framed as compliance, not empowerment"
  - "checklist" only → MEDIUM: "Accessibility is checkbox, not user value"
  - "meets requirements" → MEDIUM: "Accessibility lacks empowerment framing"

  Check specificity:
  - IF no WCAG level specified:
    → MEDIUM: "Accessibility section missing WCAG conformance level"
  - IF no specific assistive tech mentioned:
    → LOW: "Consider specifying screen reader or keyboard navigation support"

IF UXQ domain active AND no accessibility mention:
  → HIGH: "UXQ domain requires accessibility documentation (UXQ-010)"
```

**8. Delight Opportunities (UXQ-004)**:

```text
IF "Delight" section OR "Success States" section exists:
  IF content describes positive feedback/celebration:
    → OK: "Delight moments documented"
  ELSE:
    → LOW: "Delight section present but lacks specific opportunities"

IF neither section exists:
  # Advisory only - UXQ-004 is SHOULD
  → LOW: "Consider adding Delight Opportunities section (UXQ-004 SHOULD)"
```

**9. Emotional Journey (UXQ-002)**:

```text
IF "Emotional Journey" OR "User Journey" section has emotional annotations:
  → OK: "Emotional journey documented"

IF user journey exists WITHOUT emotional states:
  → LOW: "User journey missing emotional state annotations (UXQ-002 SHOULD)"
  → Suggest: "Add emotional states (frustration, confidence, delight) at journey steps"
```

**10. Persona Integration (UXQ-009)**:

```text
IF spec.md references personas by name OR role:
  FOR EACH feature/FR:
    Check if persona context mentioned
    IF feature lacks persona reference:
      → LOW: "Feature {id} has no persona context (UXQ-009 SHOULD)"

IF no persona references in spec.md:
  → LOW: "Consider adding persona references for user-centered design (UXQ-009)"
```

**Severity Summary for Pass X:**

| Condition | Severity |
|-----------|----------|
| UXQ active but missing UXQ section | CRITICAL |
| Friction point without justification | CRITICAL |
| FR has no JTBD traceability | HIGH |
| Missing FTUE section | HIGH |
| Missing User Mental Model section | HIGH |
| Missing accessibility documentation | HIGH |
| UXQ subsection missing | HIGH |
| JTBD missing job statement or FRs | HIGH |
| FTUE lacks specific guidance | HIGH |
| Friction missing mitigation | HIGH |
| JTBD format non-standard | MEDIUM |
| FTUE section is stub | MEDIUM |
| Mental model too brief | MEDIUM |
| Technical jargon in user content | MEDIUM |
| Error lacks user empathy | MEDIUM |
| A11y framed as compliance only | MEDIUM |
| A11y missing WCAG level | MEDIUM |
| Friction indicators without table | MEDIUM |
| No delight opportunities | LOW |
| No emotional journey annotations | LOW |
| Feature lacks persona context | LOW |
| No persona references | LOW |
| Non-standard friction type | LOW |
| No assistive tech specified | LOW |

---

#### Y. UX Foundation Validation *(if concept.md exists with UX Foundation Layer)*

**Purpose**: Validate UX Foundation Layer completeness, wave ordering, and Golden Path testability.

**Activation Check**:

```text
IF exists("specs/concept.md"):
  Read file content
  IF content contains "## UX Foundation Layer" OR "## Execution Order":
    UX_FOUNDATION_ACTIVE = true
  ELSE:
    UX_FOUNDATION_ACTIVE = false
ELSE:
  UX_FOUNDATION_ACTIVE = false

IF NOT UX_FOUNDATION_ACTIVE:
  SKIP this validation pass
```

**1. Foundation Coverage Validation**:

```text
IF "Required Foundations" table exists:
  FOR EACH foundation row where Status = "[ ] Needed":
    IF Stories column is empty or "-":
      → HIGH: "Foundation {name} marked as needed but has no stories defined"
      → Suggest: "Add stories to cover {foundation} scenarios"

  FOR EACH foundation row where Status = "[x] Covered":
    Verify referenced stories exist in Feature Hierarchy
    IF stories not found:
      → MEDIUM: "Foundation {name} references non-existent stories: {story_ids}"
```

**2. Foundation Scenario Traceability**:

```text
IF "Foundation Scenarios" section exists:
  FOR EACH UXF-xxx scenario in Foundation Scenarios tables:
    Extract "Defined In" column (e.g., "[EPIC-001.F01.S01]")
    IF Defined In is empty or placeholder:
      → HIGH: "UXF-{id} has no story definition"
      → Suggest: "Map scenario to existing story or create new story"

    IF Defined In references story ID:
      Verify story exists in Feature Hierarchy section
      IF not found:
        → HIGH: "UXF-{id} references non-existent story: {story_id}"

  Load ux-foundations.md from memory/knowledge/frameworks/
  Compare required scenarios for detected project type
  FOR EACH required scenario NOT in Foundation Scenarios:
    → MEDIUM: "Missing required scenario for project type: UXF-{id}"
```

**3. Wave Order Validation**:

```text
IF "Execution Order" section exists:
  # Validate Wave 1 completion gates
  FOR EACH feature in "Wave 1: Foundation Layer" table:
    IF Status = "[ ]" (not complete):
      Check if any Wave 3+ feature depends on it
      IF dependent features found with Status != "[ ]":
        → CRITICAL: "Wave 3 feature {id} progressing before Wave 1 foundation {id}"

  # Validate Wave 2 prerequisites
  FOR EACH feature in "Wave 2: Experience Layer" table:
    IF Status != "[ ]" (in progress or complete):
      Check Wave 1 features for same epic
      IF any Wave 1 features still "[ ]":
        → HIGH: "Wave 2 feature {id} started before Wave 1 complete"

  # Validate Wave 3+ dependencies
  FOR EACH feature in "Wave 3+: Business Features" table:
    Parse "Depends On" column
    FOR EACH dependency:
      Look up dependency Wave
      IF dependency Wave >= current feature Wave:
        → MEDIUM: "Feature {id} depends on same-or-later Wave feature: {dep_id}"
```

**4. Golden Path Validation**:

```text
IF "Golden Path" section exists:
  FOR EACH step in Golden Path table:
    IF Feature column is empty:
      → MEDIUM: "Golden Path step {N} has no implementing feature"

    IF Feature references EPIC-xxx.Fxx:
      Verify feature exists in Feature Hierarchy
      IF not found:
        → HIGH: "Golden Path references non-existent feature: {feature_id}"

    IF Wave column value exists:
      IF Wave value > 2:
        → LOW: "Golden Path step {N} uses Wave {W} feature (should be Wave 1-2 only)"

  # Check Golden Path Status accuracy
  Count Wave 1 features with Status = "[x]"
  Count Wave 2 features with Status = "[x]"

  IF all Wave 1 complete AND all Wave 2 complete:
    IF Golden Path Status shows "[ ] Not testable":
      → MEDIUM: "Golden Path should be testable - Wave 1-2 complete"
  ELSE:
    IF Golden Path Status shows "[x] Testable":
      → HIGH: "Golden Path marked testable but Wave 1-2 incomplete"

ELSE:
  IF UX_FOUNDATION_ACTIVE:
    → MEDIUM: "UX Foundation Layer present but no Golden Path defined"
    → Suggest: "Add Golden Path section (J000) covering Wave 1-2 features"
```

**5. Entry Point Completeness**:

```text
FOR EACH story in Feature Hierarchy (non-foundation stories):
  # Foundation detection: check if story is in Wave 1-2 or matches foundation patterns
  IF story NOT in Wave 1 OR Wave 2 foundations:
    Search Acceptance Scenarios or story description for:
    - Entry point (how user navigates here)
    - Auth context (GUEST | AUTHENTICATED | ADMIN)
    - Exit point (where user goes next)

    IF entry point not documented:
      → LOW: "Story {story_id} missing entry point documentation"

    IF auth context not clear:
      → LOW: "Story {story_id} missing auth context"
```

**6. Traceability Skeleton Validation**:

```text
IF "Traceability Skeleton" section exists:
  FOR EACH row in skeleton table:
    IF Wave column exists:
      Verify Wave assignment is consistent with feature's Execution Order placement
      IF mismatch:
        → LOW: "Traceability Skeleton Wave mismatch for {concept_id}"

    IF Status = "Not started" AND Spec Created = "[x]":
      → MEDIUM: "Inconsistent state: spec created but status 'Not started'"

    IF Status = "IMPLEMENTED" AND Tests column is empty:
      → MEDIUM: "Implemented story {concept_id} has no test results"

  # Progress Rollup accuracy
  IF "Progress Rollup" section exists:
    Recount statuses from skeleton table
    Compare with rollup totals
    IF counts differ:
      → LOW: "Progress Rollup counts outdated"

  # Foundation Progress accuracy
  IF "Foundation Progress" section exists:
    Recount Wave 1 and Wave 2 implemented counts
    Compare with Foundation Progress table
    IF counts differ:
      → LOW: "Foundation Progress counts outdated"
```

**7. Orphan Feature Detection**:

```text
FOR EACH feature in Feature Hierarchy:
  Search Execution Order section for feature ID
  IF not found in any Wave table:
    → MEDIUM: "Feature {feature_id} not assigned to any Wave"
    → Suggest: "Add feature to appropriate Wave in Execution Order"
```

**Severity Summary for Pass Y:**

| Condition | Severity |
|-----------|----------|
| Wave 3 feature progressing before Wave 1 foundation | CRITICAL |
| Foundation scenario references non-existent story | HIGH |
| UXF-xxx has no story definition | HIGH |
| Wave 2 started before Wave 1 complete | HIGH |
| Golden Path references non-existent feature | HIGH |
| Golden Path marked testable but Wave 1-2 incomplete | HIGH |
| Foundation marked needed but has no stories | HIGH |
| Foundation references non-existent stories | MEDIUM |
| Missing required scenario for project type | MEDIUM |
| Feature depends on same-or-later Wave | MEDIUM |
| Golden Path step has no implementing feature | MEDIUM |
| Golden Path should be testable but marked not | MEDIUM |
| No Golden Path defined | MEDIUM |
| Inconsistent spec/status state | MEDIUM |
| Implemented story has no test results | MEDIUM |
| Feature not assigned to any Wave | MEDIUM |
| Golden Path uses Wave 3+ feature | LOW |
| Story missing entry point documentation | LOW |
| Story missing auth context | LOW |
| Traceability Skeleton Wave mismatch | LOW |
| Progress Rollup counts outdated | LOW |
| Foundation Progress counts outdated | LOW |

---

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
  - **Build failed** (QA: project does not compile)
  - **Tests failed** (QA: acceptance scenarios not passing)
  - **Critical vulnerabilities** (QA: security audit found critical CVEs)
  - **Potential secret in code** (QA: hardcoded credentials detected)
  - **UXQ section missing** (UXQ domain active but spec.md lacks UXQ section)
  - **Friction without justification** (UXQ: violates UXQ-003 MUST)

- **HIGH**:
  - Duplicate or conflicting requirement
  - Ambiguous security/performance attribute
  - Untestable acceptance criterion
  - **FR with no implementation tasks** (requirement gap)
  - **Task references non-existent FR** (broken traceability)
  - **Missing documentation URL for dependency** (API: unverifiable API usage)
  - **Task references undefined dependency** (API: broken [DEP:] reference)
  - **External API missing auth documentation** (API: security risk)
  - **Task may use deprecated API** (API: code will fail)
  - **API method not found in docs** (API: Context7 verification failed)
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
  - **Lint errors** (QA: code style violations blocking merge)
  - **Type errors** (QA: type checker failures)
  - **Coverage below threshold** (QA: insufficient test coverage)
  - **High vulnerabilities** (QA: security audit found high CVEs)
  - **Potential vulnerability pattern** (QA: SQL injection, XSS, etc.)
  - **AS requires test but no [TEST:] task** (Test-Spec: AS with "Requires Test = YES" has no coverage)
  - **Test references non-existent spec ID** (Test-Spec: orphan test task)
  - **Critical EC without test task** (Test-Spec: security-critical edge case uncovered)
  - **Implementation complete but test not written** (Test-Spec: TTM shows impl done, test missing)
  - **Story has impl but no tests for required AS** (Test-Spec: user story test gap)
  - **FR has no JTBD traceability** (UXQ: violates UXQ-008 MUST)
  - **Missing FTUE section** (UXQ: violates UXQ-006 MUST)
  - **Missing User Mental Model section** (UXQ: violates UXQ-001 MUST)
  - **Missing accessibility documentation** (UXQ: violates UXQ-010 MUST)
  - **UXQ subsection missing** (UXQ: required subsection not present)
  - **JTBD missing job statement or FRs** (UXQ: incomplete traceability)
  - **FTUE lacks specific guidance** (UXQ: empty states, progressive disclosure missing)
  - **Friction missing mitigation** (UXQ: friction point lacks mitigation strategy)

- **MEDIUM**:
  - Terminology drift
  - Missing non-functional task coverage
  - Underspecified edge case
  - **Unversioned dependency** (API: reproducibility risk)
  - **Task uses external API without [DEP:] marker** (API: traceability gap)
  - **Version mismatch between task and registry** (API: inconsistency)
  - **External API missing version specification** (API: breaking change risk)
  - **[NO-TEST:] without justification** (Test-Spec: explicit skip requires reason)
  - **TTM incomplete** (Test-Spec: testable AS not in matrix)
  - **Invalid test marker format** (Test-Spec: malformed [TEST:] marker)
  - **Test marked passing but placeholder path** (Test-Spec: TTM shows ✅ but no actual file)
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
  - **No test files found** (QA: missing test infrastructure)
  - **Lint warnings above threshold** (QA: code quality degradation)
  - **High test skip rate** (QA: >20% tests skipped)
  - **Performance regression** (QA: >10% degradation from baseline)
  - **Resource limit exceeded** (QA: memory/CPU above spec limits)
  - **Missing security headers** (QA: web app security configuration)
  - **Moderate vulnerabilities** (QA: security audit found >10 moderate CVEs)
  - **JTBD format non-standard** (UXQ: job statement not in When/Want/So format)
  - **FTUE section is stub** (UXQ: too brief to be useful)
  - **Mental model too brief** (UXQ: insufficient detail)
  - **Technical jargon in user content** (UXQ: violates UXQ-001)
  - **Error lacks user empathy** (UXQ: system-centric error message)
  - **A11y framed as compliance only** (UXQ: not empowerment-framed)
  - **A11y missing WCAG level** (UXQ: no conformance level specified)
  - **Friction indicators without table** (UXQ: undocumented friction)

- **LOW**:
  - Style/wording improvements
  - Minor redundancy not affecting execution order
  - **No specific APIs documented for dependency** (API: documentation hygiene)
  - **Invalid APIDOC URL format** (API: broken reference)
  - **External API missing rate limit documentation** (API: operational risk)
  - **Task missing FR link** (traceability hygiene)
  - **Non-critical EC without test** (Test-Spec: optional test coverage)
  - **[NO-TEST:] not in TTM** (Test-Spec: documentation consistency)
  - **Missing @speckit annotations in test file** (Test-Spec: traceability hygiene)
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
  - **Build warnings** (QA: minor compilation warnings)
  - **No baseline measurement for NFR** (QA: performance untested)
  - **No delight opportunities** (UXQ: UXQ-004 SHOULD not met)
  - **No emotional journey annotations** (UXQ: UXQ-002 SHOULD not met)
  - **Feature lacks persona context** (UXQ: UXQ-009 SHOULD not met)
  - **No persona references** (UXQ: missing user-centered context)
  - **Non-standard friction type** (UXQ: friction type not in standard list)
  - **No assistive tech specified** (UXQ: missing screen reader/keyboard nav)

### 6. Produce Compact Analysis Report

Output a Markdown report (no file writes) with the following structure:

## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | Duplication | HIGH | spec.md:L120-134 | Two similar requirements ... | Merge phrasing; keep clearer version |
| G1 | Dependency | CRITICAL | tasks.md | Circular: T005 → T012 → T005 | Break cycle at T012 → T005 |
| H1 | Traceability | HIGH | spec.md, tasks.md | FR-003 has no tasks | Add [FR:FR-003] to relevant task |

(Add one row per finding; generate stable IDs prefixed by category initial: A=Dup, B=Ambig, C=Underspec, D=Constitution, E=Coverage, F=Inconsist, G=Depend, H=Trace, I=Concept, J=RTM, K=SysImpact, L=SysInteg, M=Impact, N=CodeTrace, O=Freshness, P=Brownfield, Q=Migration, R=Build, S=Tests, T=Perf, U=Security, V=APIDocs, W=TestSpec, X=UXQ)

**Dependency Graph Status:**

```text
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

**UXQ Domain Status:** *(if UXQ domain active)*

```text
Domain: UXQ | Status: ACTIVE
Constitution Layer: memory/constitution.domain.md
```

| UXQ Component | Status | Issues |
|---------------|--------|--------|
| Jobs to Be Done (JTBD) | ✅/❌ | {FR coverage}% traced |
| User Mental Model | ✅/❌ | {notes} |
| FTUE Documentation | ✅/❌ | {completeness} |
| Friction Points | ✅/❌ | {unjustified count} unjustified |
| Delight Opportunities | ✅/⚠️ | {count} documented |
| Accessibility | ✅/❌ | {WCAG level or missing} |

| Principle | Level | Compliance | Issues |
|-----------|-------|------------|--------|
| UXQ-001 Mental Model | MUST | ✅/❌ | {details} |
| UXQ-003 Friction | MUST | ✅/❌ | {details} |
| UXQ-005 Error Empathy | MUST | ✅/❌ | {details} |
| UXQ-006 FTUE | MUST | ✅/❌ | {details} |
| UXQ-008 JTBD | MUST | ✅/❌ | {details} |
| UXQ-010 A11y | MUST | ✅/❌ | {details} |

**System Spec Status:** (if specs/system/ exists)

```text
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

```text
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

```text
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

```text
Strategy: [Big Bang|Parallel Run|Strangler Fig|Feature Flag]
Phases: N total | N with tasks | N with rollback
Dual-Mode Period: [specified/not specified]
```

| Phase | MIG ID | Implementation | Rollback | Status |
|-------|--------|----------------|----------|--------|
| Phase 1 | MIG-001 | T040, T041 | T045 | ✅ Complete |
| Phase 2 | MIG-002 | - | - | ❌ No tasks |

**QA Verification Report:** *(if QA mode - post-implementation)*

```text
Mode: QA VERIFICATION | Implementation: X% complete
Triggered: [auto from /speckit.implement | manual request]
```

| Check | Status | Details |
|-------|--------|---------|
| Build | ✅/❌ | {output summary} |
| Lint | ✅/⚠️/❌ | {errors}/{warnings} |
| Type Check | ✅/❌ | {error count} |
| Tests | ✅/❌ | {passed}/{total} ({failed} failed) |
| Coverage | ✅/❌ | {actual}% (threshold: {threshold}%) |
| Security Audit | ✅/⚠️/❌ | {critical}/{high}/{moderate} vulns |
| Secrets Scan | ✅/❌ | {count} potential secrets |

**Test Results Summary:**

| Category | Passed | Failed | Skipped | Coverage |
|----------|--------|--------|---------|----------|
| Unit | N | N | N | X% |
| Integration | N | N | N | X% |
| E2E | N | N | N | - |

**Security Audit Summary:**

| Severity | Count | Top CVEs |
|----------|-------|----------|
| Critical | N | CVE-xxxx, CVE-yyyy |
| High | N | CVE-zzzz |
| Moderate | N | - |

**QA Verdict:**

```text
🟢 PASS - All checks passed, ready for merge
🟡 CONCERNS - Non-blocking issues found (N MEDIUM, M LOW)
🔴 FAIL - Blocking issues found (N CRITICAL, M HIGH)
```

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

### Analysis Modes

| Mode | Trigger | Categories | Purpose |
|------|---------|------------|---------|
| Pre-Implementation | Default, before `/speckit.implement` | A-Q | Validate spec artifacts, traceability, dependencies |
| QA Verification | After `/speckit.implement`, tasks.md has [X] completed | A-Q + R-U | Verify build, tests, coverage, security |

**Mode Detection:**
```text
IF tasks.md exists AND has completed tasks [X]:
  IF triggered from /speckit.implement handoff:
    MODE = QA_VERIFICATION
  ELSE IF user explicitly requests QA:
    MODE = QA_VERIFICATION
  ELSE:
    MODE = PRE_IMPLEMENTATION
ELSE:
  MODE = PRE_IMPLEMENTATION
```

### Auto-Transitions (Pre-Implementation Mode)

| Condition | Next Phase | Gate |
|-----------|------------|------|
| Analysis complete, no CRITICAL issues, dependency graph valid | `/speckit.implement` | No Critical Issues Gate, Dependency Graph Valid Gate |

### Auto-Transitions (QA Mode)

| Condition | Next Phase | Gate |
|-----------|------------|------|
| QA Verdict == PASS | Done (ready for merge) | QA Pass Gate |
| QA Verdict == CONCERNS | Done with warnings | - |
| QA Verdict == FAIL | Fix QA Issues | - |

### Quality Gates

| Gate | Check | Block Condition | Message |
|------|-------|-----------------|---------|
| No Critical Issues Gate | CRITICAL issue count == 0 | CRITICAL > 0 | "Cannot proceed to implementation: resolve all CRITICAL issues first" |
| Dependency Graph Valid Gate | Dependency Graph Status == VALID or WARNINGS | Status == INVALID | "Resolve circular dependencies or invalid references before implementation" |
| QA Pass Gate | No CRITICAL or HIGH in R-U categories | CRITICAL > 0 OR HIGH > 0 in R-U | "QA failed - fix blocking issues before proceeding" |
| Build Pass Gate | Build succeeds (Category R) | Build fails | "Fix build errors before proceeding" |
| Tests Pass Gate | All tests pass (Category S) | Test failures | "Fix failing tests" |
| Security Gate | No critical vulnerabilities (Category U) | Critical vulns found | "Address security vulnerabilities" |

### QA Loop

```text
/speckit.implement → /speckit.analyze (QA mode) → PASS → Done/Merge
                                       ↓
                                     FAIL
                                       ↓
                            Fix Issues (/speckit.implement)
                                       ↓
                            /speckit.analyze (QA mode) → ...
```

### Gate Behavior

**Pre-Implementation Mode:**

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

**QA Mode:**

**If QA Verdict == PASS:**
- Log: "QA verification passed, ready for merge"
- Implementation is complete and verified

**If QA Verdict == CONCERNS:**
- Log: "QA passed with warnings (N MEDIUM, M LOW issues)"
- Implementation can proceed but improvements recommended
- List non-blocking issues for future attention

**If QA Verdict == FAIL:**
- Display blocking message with specific failures
- Offer handoff to `/speckit.implement` to fix issues
- List all CRITICAL/HIGH issues from categories R-U
- Wait for user to fix and re-run QA analysis

### Manual Overrides

Users can always choose to:
- Fix specific issues and re-run `/speckit.analyze`
- Skip to specific handoff for targeted fixes
- Proceed manually (not recommended if CRITICAL issues exist)
- Return to earlier phases if fundamental issues found

## Context

{ARGS}
