---
description: Execute implementation planning workflow
persona: architect-agent
handoffs:
  - label: Create Tasks
    agent: speckit.tasks
    auto: true
    condition: ["plan.md complete", "research.md exists", "no TODO markers"]
    gates: [Constitution Alignment, Tech Consistency, Plan Completeness]
  - label: Create Checklist
    agent: speckit.checklist
    auto: false
  - label: Refine Specification
    agent: speckit.specify
    auto: false
    condition: ["Planning revealed spec gaps"]
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
openapi_generation:
  enabled: true
  skip_flag: "--no-contracts"
  output_path: "contracts/api.yaml"
claude_code:
  model: opus
  reasoning_mode: extended
  thinking_budget: 8000
  cache_control: {system_prompt: ephemeral, constitution: ephemeral, artifacts: ephemeral}
  semantic_cache: {enabled: true, encoder: all-MiniLM-L6-v2, threshold: 0.95, scope: session}
  plan_mode_trigger: true
  subagents: [architecture-specialist, design-researcher]
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
EXECUTE brownfield-detection → BROWNFIELD_MODE

Adapt workflow based on COMPLEXITY_TIER
```

---

## Workflow (5 Steps)

```text
1. Setup: Run {SCRIPT} → FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH
2. Load context: Read FEATURE_SPEC, constitution.md, IMPL_PLAN template
3. Execute plan workflow:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check, evaluate gates
   - Phase 0: Research (resolve clarifications)
   - Phase 0.5: API Verification (Context7)
   - Phase 1: Design (data-model, contracts, quickstart)
   - Re-evaluate Constitution Check post-design
4. Update Feature Manifest (status → PLANNED)
4.5. Generate API Contracts (if enabled)
5. Report: branch, plan path, generated artifacts
```

---

## Phase 0: Outline & Research

### Architecture Decision Protocol [REF:QI-001]

```text
APPLY brainstorm-curate for:
- database selection, caching strategy
- auth approach, deployment architecture
- API design, state management, framework selection

SKIP when: trivial, user-specified, established patterns
```

**Decision Format**:
```text
## [Decision Area]: [Choice]
**Recommendation**: [Chosen approach]
**Why**: 1-3 reasons tied to requirements/constraints
**Alternatives considered**: [Option A: why not, Option B: why not]
**Reversibility**: [High/Medium/Low]
```

**Tasks**:
1. Extract unknowns from Technical Context
2. Dispatch research agents for each unknown
3. Consolidate findings in `research.md`

**Output**: research.md with all NEEDS CLARIFICATION resolved

---

## Phase 0.5: API Verification

```text
FOR EACH dependency in research.md:
  1. Verify package exists in registry
  2. Check latest stable version
  3. Locate official docs URL
  4. Verify key APIs exist in that version
  5. Check deprecation warnings

Tool: Context7 (resolve-library-id → get-library-docs)
```

| Condition | Severity | Action |
|-----------|----------|--------|
| Cannot verify | WARNING | Report, suggest alternatives |
| Deprecated API | ERROR | Block until replacement identified |
| Missing docs URL | WARNING | Require manual verification |
| Version conflict | ERROR | Resolve before proceeding |

**Output**: Populated Dependency Registry in plan.md

---

## Phase 1: Design & Contracts

```text
1. Extract entities → data-model.md
   - Entity name, fields, relationships
   - Validation rules, state transitions

2. Generate API contracts from FRs:
   - "create/add X" → POST /api/v1/{x}s
   - "get/fetch X" → GET /api/v1/{x}s/{id}
   - "list/show X" → GET /api/v1/{x}s
   - "update/modify X" → PUT /api/v1/{x}s/{id}
   - "delete/remove X" → DELETE /api/v1/{x}s/{id}
   Output: contracts/api.yaml

3. Update agent context (run agent script)
```

**Output**: data-model.md, contracts/*, quickstart.md

---

## Self-Review Phase [REF:SR-001]

### Quality Criteria

| ID | Check | Severity |
|----|-------|----------|
| SR-PLAN-01 | Technical Context complete | CRITICAL |
| SR-PLAN-02 | No placeholder markers (TODO/TBD/FIXME) | CRITICAL |
| SR-PLAN-03 | Dependency Registry filled | HIGH |
| SR-PLAN-04 | Dependencies verified (Context7) | HIGH |
| SR-PLAN-05 | Documentation URLs present | MEDIUM |
| SR-PLAN-06 | Research complete (if needed) | HIGH |
| SR-PLAN-07 | Constitution checked | MEDIUM |
| SR-PLAN-08 | Architecture decisions documented | HIGH |
| SR-PLAN-09 | Data model generated (if entities) | MEDIUM |
| SR-PLAN-10 | Contracts generated (if API endpoints) | MEDIUM |

### Dependency Verification

```text
FOR EACH dependency in Dependency Registry:
  Verify: name matches, version exists, docs URL valid, APIs exist
  Result: VERIFIED | UNVERIFIED | DEPRECATED | NOT_FOUND
```

### Verdict Logic

```text
CRITICAL failures → FAIL (fix, retry max 3)
  - TODO markers → research and fill
  - Unverified deps → use Context7 or mark manual
  - Empty sections → generate from spec
2+ HIGH failures → WARN
Quality >= 80% → PASS → auto-handoff
```

---

## Quality Gates

| Gate | Check | Block Condition |
|------|-------|-----------------|
| Constitution Alignment | D pass = 0 violations | violations > 0 |
| Tech Consistency | F pass = 0 inconsistencies | inconsistencies > 0 |
| Plan Completeness | All sections filled | Empty sections or TODO markers |

---

## Output Format

### Quick Summary (Always)

```text
| Aspect | Value |
|--------|-------|
| Feature | {feature_name} |
| Complexity | {TIER} ({score}/100) |
| Phases | {count} implementation phases |
| Dependencies | {external} external, {internal} internal |
| Files to Modify | ~{count} files |
| Status | {PASS|WARN|FAIL} |
| Next Step | → /speckit.tasks |
```

### Output Modes

| Mode | Trigger | Content |
|------|---------|---------|
| COMPACT | TRIVIAL/SIMPLE | Summary + collapsible full plan |
| STANDARD | MODERATE | Summary + plan + collapsible verbose |
| DETAILED | COMPLEX/--verbose | All expanded + self-review + deps |

---

## Report Format

```text
┌─────────────────────────────────────────────────────────────┐
│ /speckit.plan Complete                                       │
├─────────────────────────────────────────────────────────────┤
│ Feature: {feature-name}                                      │
│ Complexity: {TIER}                                           │
│                                                              │
│ Artifacts Generated:                                         │
│   ✓ plan.md    ✓ research.md    ✓ data-model.md             │
│   ✓ contracts/api.yaml                                       │
│                                                              │
│ Dependencies: {verified}/{total} verified                    │
│ Self-Review: {PASS|WARN|FAIL}                               │
└─────────────────────────────────────────────────────────────┘
```

### Next Steps

| Condition | Action |
|-----------|--------|
| All gates pass | → /speckit.tasks (auto) |
| TODO markers remain | Complete research, fill sections |
| Unverified deps | Verify via Context7 or manual check |
| Spec gaps found | → /speckit.specify |

---

## Context

{ARGS}
