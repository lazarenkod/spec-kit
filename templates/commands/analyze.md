---
description: Perform a non-destructive cross-artifact consistency, traceability, and dependency analysis across concept.md, spec.md, plan.md, and tasks.md.
handoffs:
  - label: Fix Spec Issues
    agent: speckit.specify
    prompt: Update the specification to address the identified issues
  - label: Update Plan
    agent: speckit.plan
    prompt: Revise the plan to address architectural issues
  - label: Regenerate Tasks
    agent: speckit.tasks
    prompt: Regenerate tasks with corrected traceability
  - label: Proceed to Implementation
    agent: speckit.implement
    prompt: Start implementation (only if no CRITICAL issues)
    send: true
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

### 5. Severity Assignment

Use this heuristic to prioritize findings:

- **CRITICAL**:
  - Violates constitution MUST
  - Missing core spec artifact
  - Requirement with zero coverage that blocks baseline functionality
  - **Circular dependency in task graph** (blocks execution)
  - **Invalid dependency reference** (task references non-existent task)

- **HIGH**:
  - Duplicate or conflicting requirement
  - Ambiguous security/performance attribute
  - Untestable acceptance criterion
  - **FR with no implementation tasks** (requirement gap)
  - **Task references non-existent FR** (broken traceability)

- **MEDIUM**:
  - Terminology drift
  - Missing non-functional task coverage
  - Underspecified edge case
  - **AS with no test task** (test gap, if tests requested)
  - **Concept story without specification** (idea loss)
  - **Cross-story dependency** (may affect parallelization)
  - **Journey references unspecified feature** (incomplete planning)

- **LOW**:
  - Style/wording improvements
  - Minor redundancy not affecting execution order
  - **Task missing FR link** (traceability hygiene)
  - **Spec missing concept reference** (traceability hygiene)
  - **RTM accuracy mismatch** (documentation drift)
  - **Coverage summary outdated** (stale metrics)
  - **Undocumented gaps** (incomplete gap tracking)

### 6. Produce Compact Analysis Report

Output a Markdown report (no file writes) with the following structure:

## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | Duplication | HIGH | spec.md:L120-134 | Two similar requirements ... | Merge phrasing; keep clearer version |
| G1 | Dependency | CRITICAL | tasks.md | Circular: T005 → T012 → T005 | Break cycle at T012 → T005 |
| H1 | Traceability | HIGH | spec.md, tasks.md | FR-003 has no tasks | Add [FR:FR-003] to relevant task |

(Add one row per finding; generate stable IDs prefixed by category initial: A=Dup, B=Ambig, C=Underspec, D=Constitution, E=Coverage, F=Inconsist, G=Depend, H=Trace, I=Concept, J=RTM)

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

## Context

{ARGS}
