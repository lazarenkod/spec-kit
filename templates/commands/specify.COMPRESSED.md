---
description: Feature specification from natural language description
persona: product-agent
handoffs:
  - label: Build Technical Plan
    agent: speckit.plan
    auto: true
    gates: [VG-001, VG-003, VG-004, VG-005]
  - label: Clarify Spec Requirements
    agent: speckit.clarify
    auto: false
  - label: Run Traceability Analysis
    agent: speckit.analyze
    auto: false
scripts:
  sh: scripts/bash/create-new-feature.sh --json "{ARGS}"
  ps: scripts/powershell/create-new-feature.ps1 -Json "{ARGS}"
claude_code:
  model: opus
  reasoning_mode: extended
  thinking_budget: 10000
  cache_control: {system_prompt: ephemeral, constitution: ephemeral, templates: ephemeral}
  semantic_cache: {enabled: true, encoder: all-MiniLM-L6-v2, threshold: 0.95, scope: session}
---

## Input
```text
$ARGUMENTS
```

---

## Prefetch Phase [REF:PF-001]

**Speculative parallel load** BEFORE any conditional logic:

```text
# PREFETCH BATCH (single message, all Read calls in parallel)
Read IN PARALLEL:
- `memory/constitution.md`
- `templates/spec-template.md`
- `templates/shared/core/language-loading.md`
- `templates/shared/complexity-scoring.md`
- `templates/shared/core/brownfield-detection.md`
- `templates/shared/core/workspace-detection.md`
- `specs/concept.md` (if exists)

CACHE results. REPORT: "Prefetched {N} files"
```

---

## Init [REF:INIT-001]

Load project context using **parallel loading** (see `templates/shared/core/parallel-loading.md`):

```text
# PARALLEL BATCH READ of shared modules (single message, multiple Read calls)
Read IN PARALLEL: language-loading.md, complexity-scoring.md, brownfield-detection.md

EXECUTE language-loading → ARTIFACT_LANGUAGE
EXECUTE complexity-scoring → COMPLEXITY_TIER, COMPLEXITY_SCORE
EXECUTE brownfield-detection → BROWNFIELD_MODE, BROWNFIELD_CONFIDENCE

REPORT: "Spec in {LANGUAGE_NAME}, Complexity: {COMPLEXITY_TIER} ({SCORE}/100)"
REPORT: "Brownfield: {BROWNFIELD_MODE} (confidence: {BROWNFIELD_CONFIDENCE}%)"
```

**Brownfield Actions**:
- If baseline.md exists → load CB-xxx entries, current limitations
- If no baseline → suggest `/speckit.baseline` first
- Change types: Enhancement | Refactor | Migration | Bugfix | Performance | Security

---

## Workspace Detection

```text
EXECUTE workspace-detection.md → WORKSPACE_MODE, WORKSPACE_CONTEXT

IF WORKSPACE_MODE:
  Set CURRENT_REPO_ALIAS, AVAILABLE_REPOS
  Include "Cross-Repository Dependencies" section
  Use format: `repo-alias:feature-id` for cross-repo refs
```

---

## Concept Integration

Check for `specs/concept.md`:

```text
IF concept.md exists:
  1. Parse Feature Hierarchy for matching Concept IDs
  2. Extract: Vision context, User Journeys, Dependencies
  3. Set CONCEPT_REFERENCE = matched IDs (EPIC-NNN.FNN.SNN)
  4. Use concept priorities (P1a, P1b) for story prioritization
  5. Apply CQS Gate [REF:VG-002]:
     - CQS >= 80 → Proceed
     - CQS 60-79 → Warn, flag gaps with [CQS GAP]
     - CQS < 60 → Block, suggest /speckit.concept

ELSE:
  CONCEPT_REFERENCE = "N/A" (standalone spec)
  Use simple priorities (P1, P2, P3)
```

---

## Pre-Flight Checks

### Incomplete Feature Check
```text
IF manifest exists with incomplete features (status NOT IN [MERGED, ABANDONED]):
  Display warning with options:
  1. Resume existing: /speckit.switch <ID>
  2. Start new: Confirm to proceed
  3. Abandon old: Mark as ABANDONED first
```

### Extension Detection
```text
IF user input matches extension patterns ("add to", "extend", "enhance"):
  AND references merged feature:
    Suggest /speckit.extend for lineage preservation
    Detect relationship: EXTENDS | REFINES | FIXES | DEPRECATES
```

---

## Workflow (13 Steps)

1. **Generate short name**: 2-4 words, action-noun format (e.g., "user-auth", "fix-payment-timeout")

2. **Check existing branches**: Fetch remotes, find highest N for short-name across:
   - Remote branches: `git ls-remote --heads origin`
   - Local branches: `git branch`
   - Spec directories: `specs/[0-9]+-<short-name>`
   Use N+1 for new branch

3. **Run script** with `--number N+1 --short-name "name"` → Get BRANCH_NAME, SPEC_FILE

4. **Load template**: `templates/spec-template.md`

5. **Parse user description** → Extract actors, actions, data, constraints

6. **Concept integration**: Load context from concept.md if exists

7. **Handle unclear aspects**:
   - Make informed guesses (industry standards, common patterns)
   - **Max 3** [NEEDS CLARIFICATION] markers for critical decisions only
   - Priority: scope > security/privacy > UX > technical

8. **Generate User Stories** with sub-priorities (P1a, P1b, P1c for MVP; P2a, P2b post-MVP)
   - Add Concept Reference per story
   - Add Independent Test description

9. **Generate Acceptance Scenarios** with IDs:
   - Format: `AS-[story][letter]` (AS-1A, AS-1B, AS-2A)
   - Edge cases: EC-001, EC-002
   - Table: | ID | Given | When | Then |

10. **Generate Functional Requirements** (FR-001, FR-002):
    - Each must be testable
    - Link to AS: `*Acceptance Scenarios*: AS-1A, AS-1B`

11. **Define Success Criteria** (SC-001, SC-002):
    - Measurable, technology-agnostic, user-focused, verifiable

12. **Generate Traceability Summary**:
    | Requirement | Acceptance Scenarios | Edge Cases | Status |

13. **Conditional sections**:
    - IF WORKSPACE_MODE → Cross-Repository Dependencies table
    - IF BROWNFIELD_MODE → Change Specification (CB-xxx, CL-xxx, CHG-xxx, PB-xxx)

14. **Write spec** to SPEC_FILE, update concept.md traceability if exists

---

## Validation [REF:VG-001..005]

### Spec Quality Checklist
Generate `FEATURE_DIR/checklists/requirements.md`:

**Content Quality**:
- [ ] No implementation details
- [ ] User value focused
- [ ] Non-technical stakeholder readable

**Requirement Completeness**:
- [ ] No [NEEDS CLARIFICATION] markers
- [ ] Testable and unambiguous
- [ ] Measurable success criteria
- [ ] Technology-agnostic SC
- [ ] Scope clearly bounded

**Feature Readiness**:
- [ ] All FR have acceptance criteria
- [ ] User scenarios cover primary flows
- [ ] No implementation details leak

### Validation Loop
```text
FOR iteration IN 1..3:
  Run checklist validation
  IF all items pass → BREAK
  ELIF [NEEDS CLARIFICATION] remains:
    Present max 3 questions with options table
    Wait for user response
    Update spec with answers
  ELSE:
    Fix issues, re-validate

IF still failing after 3 iterations:
  Warn user, document remaining issues
```

---

## Pre-Review Quality Pass [REF:QI-001]

Apply before self-review:

```text
ANTI_SLOP_SCAN: [REF:AS-001]
  - Remove forbidden phrases
  - Fix hedge phrases (max 2/section)
  - Replace generic terms with specifics
  - Reduce buzzwords (max 2/paragraph)

READER_TEST: [REF:RT-001]
  - Fresh reader comprehension (<30s)
  - Actionability for dev/QA
  - Ambiguity scan (vague pronouns, missing baselines)

PROCEED when:
  - Zero forbidden phrases
  - Buzzword density < 2/paragraph
  - No flagged ambiguities
```

---

## Self-Review Phase [REF:SR-001]

**Criteria set**: SR-SPEC-01 to SR-SPEC-10

| ID | Check | Severity |
|----|-------|----------|
| SR-SPEC-01 | All mandatory sections filled | CRITICAL |
| SR-SPEC-02 | No implementation details | HIGH |
| SR-SPEC-03 | Each FR linked to AS | HIGH |
| SR-SPEC-04 | AS use Given/When/Then | MEDIUM |
| SR-SPEC-05 | No [NEEDS CLARIFICATION] (or max 3) | MEDIUM |
| SR-SPEC-06 | SC measurable with metrics | HIGH |
| SR-SPEC-07 | SC technology-agnostic | HIGH |
| SR-SPEC-08 | Stories have clear AS | MEDIUM |
| SR-SPEC-09 | Edge cases identified | MEDIUM |
| SR-SPEC-10 | Traceability table complete | LOW |

**Domain criteria** (if applicable):
- SR-UXQ-01..10 when UXQ domain active
- SR-WS-01..05 when WORKSPACE_MODE

**Verdict logic**:
- PASS: CRITICAL=0 AND HIGH=0 → Proceed to /speckit.plan
- WARN: CRITICAL=0 AND HIGH≤2 → Proceed with caution
- FAIL: CRITICAL>0 OR HIGH>2 → Self-correct, re-check (max 3 iterations)

**Self-correction fixes**:
| Issue | Fix |
|-------|-----|
| "PostgreSQL" in FR | → "persistent data storage" |
| "API response < 200ms" | → "Users see results instantly" |
| Missing AS link | → Add `*Acceptance Scenarios*: AS-xxx` |
| Vague SC | → Add specific metric |

---

## Spec Validation Phase (Auto-Triggered)

Pre-handoff action uses **Progressive Validation** (see `templates/shared/validation/checkpoints.md`):

**4-Tier Pipeline**:
| Tier | Checks | Time | Behavior |
|------|--------|------|----------|
| 1 | Syntax: sections, IDs | < 1s | BLOCKING |
| 2 | Semantic: VG-004 (constitution), links | 1-5s | BLOCKING on errors |
| 3 | Quality: VG-001 (SRS), VG-005 (ambiguity) | 5-15s | NON-BLOCKING |
| 4 | Deep: LLM review, consistency | 15-30s | ASYNC background |

**Early Exit**: At 95%+ confidence after Tier 2, skip Tier 3-4 (saves ~20s)

**Flow**:
```text
IF tier_1.fails → STOP, fix syntax issues
IF tier_2.errors → STOP, fix semantic issues (constitution violations)
IF tier_2.warnings → CONTINUE, log for review
IF confidence >= 0.95 → EARLY EXIT, proceed to /speckit.plan
ELSE → Run Tier 3-4, display scores, proceed
```

Skip with `--skip-validate` or `--fast` (Tier 1-2 only)

---

## Manifest Update

```text
EXECUTE manifest-update.md:
  NEW_STATUS = "SPEC_COMPLETE"
  CALLER_COMMAND = "specify"
```

---

## Output Phase

### Quick Summary (always shown)
| Aspect | Value |
|--------|-------|
| Feature | {name} |
| Complexity | {TIER} ({score}/100) |
| User Stories | {count} |
| Requirements | {fr_count} FR, {nfr_count} NFR |
| Scenarios | {as_count} AS |
| Status | {badge} |
| Next Step | {next} |

### Output Mode
```text
COMPACT (TRIVIAL/SIMPLE): Quick Summary + collapsible full spec
STANDARD (MODERATE): Quick Summary + full spec with collapsible verbose
DETAILED (COMPLEX/--verbose): All expanded + self-review report
```

### Artifact Registry Update
```text
UPDATE_REGISTRY("spec", "FEATURE_DIR/spec.md", {
  parent_concept_version: ...,
  fr_count: N,
  as_count: N
})
CHECK_STALENESS → Report downstream impact
```

---

## Completion Report

Output includes:
- Branch name, spec file path
- Checklist results (pass/fail count)
- Traceability summary: Concept Reference, AS count, FR count, EC count
- Brownfield summary (if applicable): Change Type, CB/CL/CHG/PB counts
- Workspace summary (if applicable): Cross-repo dependencies
- Next phase readiness: /speckit.clarify or /speckit.plan

---

## Guidelines

**Focus**: WHAT users need, WHY — not HOW
**Audience**: Business stakeholders, not developers
**Defaults**: Use industry standards, document assumptions
**Clarifications**: Max 3, only for critical decisions without reasonable defaults

**Good SC examples**:
- "Users complete checkout in under 3 minutes"
- "System supports 10,000 concurrent users"
- "95% of searches return in under 1 second"

**Bad SC examples** (implementation-focused):
- "API response < 200ms" → use "instant results"
- "Redis cache hit > 80%" → use user-facing metric
