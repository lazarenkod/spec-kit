---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
persona: architect-agent
handoff:
  requires: handoffs/specify-to-plan.md
  generates: handoffs/plan-to-tasks.md
  template: templates/handoff-template.md
handoffs:
  - label: Create Tasks
    agent: speckit.tasks
    prompt: Break the plan into tasks
    auto: true
    condition:
      - "plan.md completed with all phases"
      - "research.md exists (Phase 0 complete)"
      - "All [NEEDS CLARIFICATION] resolved"
    pre_handoff_action:
      name: "Plan Validation"
      mode: progressive  # 4-tier validation (see templates/shared/validation/checkpoints.md)
      invoke: speckit.analyze
      args: "--quiet"  # Profile auto-detected from caller context
      skip_flag: "--skip-validate"
      fast_flag: "--fast"  # Tier 1-2 only
      timeout: 45s
      early_exit_threshold: 0.95  # Skip Tier 3-4 at high confidence
      gates:
        - name: "Constitution Alignment Gate"
          pass: D
          threshold: 0
          severity: CRITICAL
          block_if: "constitution violations > 0"
          message: "Plan violates project constitution. Resolve before task generation."
        - name: "Tech Consistency Gate"
          pass: F
          threshold: 0
          severity: HIGH
          block_if: "terminology inconsistencies > 0"
          message: "Technical inconsistencies between spec and plan detected."
      on_failure:
        action: block
        message: "Plan validation failed. Review findings and update plan.md."
    gates:
      - name: "Plan Completeness Gate"
        check: "Technical Context filled, Architecture defined, Phases outlined"
        block_if: "Empty sections or TODO markers remain"
        message: "Complete all plan sections before generating tasks"
    post_actions:
      - "log: Plan complete, transitioning to task generation"
  - label: Create Checklist
    agent: speckit.checklist
    prompt: Create a checklist for the following domain...
    auto: false
  - label: Refine Specification
    agent: speckit.specify
    prompt: Update specification based on planning insights
    auto: false
    condition:
      - "Planning revealed spec gaps or ambiguities"
claude_code:
  model: opus
  reasoning_mode: extended
  thinking_budget: 16000
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
  plan_mode_trigger: true
  orchestration:
    max_parallel: 2
    role_isolation: false
  subagents:
    - role: architecture-specialist
      role_group: REVIEW
      parallel: true
      depends_on: []
      priority: 8
      trigger: "when evaluating technology choices or designing system structure"
      prompt: "Analyze architecture options for {REQUIREMENT}: trade-offs, patterns, recommendations"
    - role: design-researcher
      role_group: REVIEW
      parallel: true
      depends_on: []
      priority: 7
      trigger: "when planning UI features requiring design system decisions"
      prompt: "Research design system approaches for {UI_FEATURE}"
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
agent_scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
openapi_generation:
  enabled: true
  skip_flag: "--no-contracts"
  output_path: "contracts/api.yaml"
  openapi_version: "3.0.3"
  extract_from:
    - "FR-xxx with API/endpoint/request/response keywords"
    - "Technical Dependencies → External API Dependencies"
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
   - `templates/plan-template.md`
   - `templates/shared/core/language-loading.md`
   - `templates/shared/complexity-scoring.md`
   - `templates/shared/core/brownfield-detection.md`
   - `specs/concept.md` (if exists)

   CACHE all results with session lifetime.
   REPORT: "Prefetched {N} files in {T}ms"
   ```

1. **Load project context**:

   Execute prefetched modules (already in cache from Step 0):

   ```text
   # Execute cached modules
   EXECUTE language-loading.md → ARTIFACT_LANGUAGE
   EXECUTE complexity-scoring.md → COMPLEXITY_TIER, COMPLEXITY_SCORE
   EXECUTE brownfield-detection.md → BROWNFIELD_MODE

   REPORT: "Generating plan in {LANGUAGE_NAME} ({ARTIFACT_LANGUAGE})..."
   REPORT: "Complexity: {COMPLEXITY_TIER} ({COMPLEXITY_SCORE}/100)"
   ```

   Adapt workflow based on COMPLEXITY_TIER (see complexity-scoring.md for tier-specific guidelines).

2. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

3. **Load context**: Read IN PARALLEL: FEATURE_SPEC, `/memory/constitution.md`, and IMPL_PLAN template. Confirm ARTIFACT_LANGUAGE from constitution Project Settings.

4. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 0.5: Verify APIs and populate Dependency Registry (use Context7)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

5. **Update Feature Manifest**: After plan artifacts are generated:
   ```text
   Read `templates/shared/core/manifest-update.md` and apply with:
   - NEW_STATUS = "PLANNED"
   - CALLER_COMMAND = "plan"

   EXECUTE manifest-update.md algorithm
   LOG: "Feature manifest updated: SPEC_COMPLETE → PLANNED"
   ```

4.5. **Generate API Contracts** (Optional):

   ```text
   IF openapi_generation.enabled AND NOT --no-contracts flag:

     1. Parse spec.md for API-related FRs:
        KEYWORDS = ["API", "endpoint", "request", "response", "POST", "GET", "PUT", "DELETE", "REST", "webhook"]

        FOR EACH FR in spec.md Functional Requirements:
          IF FR.description contains any KEYWORD:
            Extract: FR-ID, inferred HTTP method, path pattern, schema hints
            ADD to API_FRS[]

     2. Parse plan.md Dependency Registry (if exists):
        - API-xxx entries → External API references (don't regenerate, link only)
        - PKG-xxx with HTTP clients → SDK integrations to document

     3. Infer endpoints from API_FRS[]:
        MAPPING_RULES (from templates/shared/openapi-generation.md):
        - "create/add/register {X}" → POST /api/v1/{x}s
        - "get/fetch/retrieve {X}" → GET /api/v1/{x}s/{id}
        - "list/show all {X}" → GET /api/v1/{x}s
        - "update/modify/edit {X}" → PUT /api/v1/{x}s/{id}
        - "delete/remove {X}" → DELETE /api/v1/{x}s/{id}

     4. Generate contracts/api.yaml:
        ```yaml
        openapi: 3.0.3
        info:
          title: "{PROJECT_NAME} API"
          version: "1.0.0"
          description: "Auto-generated from spec.md FR-xxx requirements"
        servers:
          - url: /api/v1
        paths:
          /{resource}:
            {method}:
              operationId: "{FR-ID}"
              summary: "{FR description}"
              tags: ["{domain}"]
              requestBody:
                content:
                  application/json:
                    schema: {inferred_schema}
              responses:
                '200': {success_schema}
                '400': {error_schema}
        ```

     5. Validate generated contract:
        - All API_FRS[] have corresponding paths
        - No duplicate operationIds
        - Request/response schemas are consistent
        - Authentication requirements documented (if any)

     6. Update plan.md with API Contracts section:
        | Contract | Path | Source FRs | Status |
        |----------|------|------------|--------|
        | Main API | contracts/api.yaml | {FR_IDS} | GENERATED |

     7. Output CONTRACTS_GENERATED_REPORT

   ELSE:
     LOG "OpenAPI generation disabled or --no-contracts flag set"
   ```

   Read `templates/shared/openapi-generation.md` for FR-to-endpoint mapping rules.

5. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Quality Imports for Architecture Decisions

```text
IMPORT: templates/shared/quality/brainstorm-curate.md
IMPORT: templates/shared/quality/anti-slop.md

FOR architecture_decision IN [database, caching, auth, deployment, framework]:
  IF decision is non-trivial:
    APPLY brainstorm_curate_protocol
    DOCUMENT chosen approach with reasoning in research.md
```

### Phase 0: Outline & Research

**Architecture Decision Protocol** (NEW):

For each technology decision in Technical Context:

1. **Identify if Brainstorm-Curate applies**:
   ```text
   APPLY_BRAINSTORM_CURATE = [
     "database selection",
     "caching strategy",
     "authentication approach",
     "deployment architecture",
     "API design pattern",
     "state management",
     "message queue selection",
     "framework/library selection",
     "build vs buy decisions"
   ]

   SKIP_WHEN = [
     "Decision trivial (single obvious answer)",
     "User already specified the technology",
     "Following established project patterns",
     "Industry standard with no real alternatives"
   ]
   ```

2. **For non-trivial decisions**:
   - Generate 3-5 genuinely different options
   - Include: Conventional, Minimal, Unconventional
   - Score against: Team expertise, Maintenance cost, Scalability, Time to implement
   - Document decision and alternatives in research.md

3. **ADR Generation Protocol**:

   FOR EACH significant decision:

   ```text
   # Step 1: Assign ADR identifier
   ADR_NUMBER = next sequential number (ADR-001, ADR-002, etc.)
   ADR_SLUG = slugify(decision_title)  # e.g., "database-selection"

   # Step 2: Link to requirements
   LINKED_REQUIREMENTS = extract FR-xxx and NFR-xxx that drive this decision
   IMPACT = assess_impact(decision)  # High | Medium | Low

   # Step 3: Determine if full ADR file needed
   CREATE_FULL_ADR = (
     alternatives_count >= 2 OR
     IMPACT == "High" OR
     trade_offs are non-trivial
   )
   ```

4. **ADR Documentation Format** (inline in plan.md):
   ```markdown
   ### ADR-{NUMBER}: {Decision Title}

   **Status**: Accepted
   **Impact**: {High | Medium | Low}
   **Linked Requirements**: {FR-xxx, NFR-xxx}
   **Decision Date**: {YYYY-MM-DD}

   **Decision**:
   {One clear sentence describing what was decided}

   **Context**:
   {2-3 sentences: What problem does this solve? What constraints exist?}

   **Rationale**:
   {2-4 sentences: Why this approach? What makes it the best option?}

   **Alternatives Considered**:
   - **Option A**: {description} — Rejected because {reason}
   - **Option B**: {chosen} — Selected because {reason}

   **Trade-offs**:
   - ✅ **Pros**: {benefits}
   - ❌ **Cons**: {drawbacks}
   - ⚠️ **Risks**: {what could go wrong}

   **Implementation Notes**:
   {Guidance for developers}

   **Full ADR**: {link to adrs/ADR-xxx-slug.md if CREATE_FULL_ADR}
   ```

5. **Full ADR File Generation** (when threshold met):
   ```text
   IF CREATE_FULL_ADR:
     # Create adrs/ directory if not exists
     mkdir -p specs/[feature]/adrs

     # Generate full ADR using template
     TEMPLATE = memory/knowledge/templates/adr-template.md
     OUTPUT = specs/[feature]/adrs/ADR-{NUMBER}-{SLUG}.md

     # Populate template with:
     - Full context from research
     - Complete alternatives analysis
     - Detailed consequences (positive, negative, neutral)
     - Implementation guidance
     - Linked requirements section

     # Update ADR index
     UPDATE specs/[feature]/adrs/README.md with new entry
   ```

6. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**:
- `research.md` with all NEEDS CLARIFICATION resolved
- `plan.md` Architecture Decisions section populated with inline ADRs
- `specs/[feature]/adrs/ADR-xxx-slug.md` files for complex decisions (if threshold met)
- `specs/[feature]/adrs/README.md` ADR index (if any full ADRs generated)

### Phase 0.5: API Verification

**Prerequisites:** `research.md` complete

**Purpose**: Verify all external dependencies and APIs before design decisions.
This phase prevents AI agents from hallucinating non-existent APIs.

1. **Dependency Audit**:

   ```text
   FOR EACH dependency identified in research.md:
     1. Verify package exists in registry (npm, PyPI, crates.io, etc.)
     2. Check latest stable version and compatibility
     3. Locate official documentation URL
     4. Verify key APIs/methods exist in that version
     5. Check for deprecation warnings
   ```

   **Tool**: Use Context7 MCP (`resolve-library-id` → `get-library-docs`) to fetch current documentation.

2. **API Documentation Verification**:

   ```text
   FOR EACH external API to be used (Stripe, AWS, Firebase, etc.):
     1. Confirm API version is current (not sunset)
     2. Verify endpoint signatures match documentation
     3. Document authentication requirements
     4. Note rate limits and quotas
     5. Check for breaking changes in recent versions
   ```

3. **Framework Version Check**:

   ```text
   FOR EACH framework dependency:
     1. Identify features required by spec
     2. Verify features exist in specified version
     3. Check for deprecated patterns to avoid
     4. Document minimum version requirements
   ```

4. **Populate Dependency Registry**:
   - Fill `plan.md` Dependency Registry section with verified data
   - Each entry MUST have documentation URL
   - Each entry MUST have locked version with rationale
   - Document key APIs/methods to be used

**Validation Gate**:

| Condition | Severity | Action |
|-----------|----------|--------|
| Dependency cannot be verified | WARNING | Report and suggest alternatives |
| Deprecated API detected | ERROR | BLOCK until replacement identified |
| Missing documentation URL | WARNING | Require manual verification |
| Version conflict detected | ERROR | Resolve before proceeding |

**Output**: Populated Dependency Registry in plan.md, verified API references

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `{AGENT_SCRIPT}`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications

## Automation Behavior

When this command completes successfully, the following automation rules apply:

### Auto-Transitions

| Condition | Next Phase | Gate |
|-----------|------------|------|
| plan.md complete, research.md exists, no TODO markers | `/speckit.tasks` | Plan Completeness Gate |

### Quality Gates

| Gate | Check | Block Condition | Message |
|------|-------|-----------------|---------|
| Plan Completeness Gate | All sections filled, architecture defined | Empty sections or TODO markers | "Complete all plan sections before generating tasks" |

### Gate Behavior

**If all conditions pass and no gates block:**
- Automatically proceed to `/speckit.tasks` with the implementation plan
- Log transition for audit trail

**If gates block:**
- Display blocking message to user
- List incomplete sections or unresolved items
- Wait for user to complete planning
- Offer handoff to `/speckit.specify` if spec updates needed

### Manual Overrides

Users can always choose to:
- Run `/speckit.checklist` to create domain-specific checklists first
- Skip automation by selecting a different handoff option
- Return to `/speckit.specify` to refine requirements

---

## Self-Review Phase (MANDATORY)

**Before declaring plan.md complete, you MUST perform self-review.**

Read `templates/shared/self-review/framework.md` for the complete self-review algorithm.
Read `templates/shared/validation/checkpoints.md` for checkpoint definitions.

```text
SELF_REVIEW_INPUT:
  ARTIFACTS = [plan.md, research.md, data-model.md, contracts/*]
  COMPLEXITY_TIER = from step 0
  CRITERIA_SET = SR-PLAN-01 to SR-PLAN-13

EXECUTE self-review framework with up to 3 iterations
GENERATE Self-Review Report
```

This ensures the implementation plan is complete, verified, and ready for task generation.

### Step 1: Re-read Generated Artifacts

Read the artifacts you created:
- `FEATURE_DIR/plan.md` (main plan)
- `FEATURE_DIR/research.md` (if generated)
- `FEATURE_DIR/data-model.md` (if generated)
- `FEATURE_DIR/contracts/*` (if generated)

### Step 2: Quality Criteria

Answer each question by validating against the artifacts:

| ID | Criterion | Check | Severity |
|----|-----------|-------|----------|
| SR-PLAN-01 | Technical Context Complete | All sections filled (Stack, Framework, Database, etc.) | CRITICAL |
| SR-PLAN-02 | No Placeholder Markers | No TODO, TBD, FIXME, or [NEEDS CLARIFICATION] remain | CRITICAL |
| SR-PLAN-03 | Dependency Registry Filled | All dependencies listed with versions | HIGH |
| SR-PLAN-04 | Dependencies Verified | Each dependency verified via Context7 or official docs | HIGH |
| SR-PLAN-05 | Documentation URLs Present | Each dependency has official documentation link | MEDIUM |
| SR-PLAN-06 | Research Complete | research.md exists if NEEDS CLARIFICATION was present | HIGH |
| SR-PLAN-07 | Constitution Checked | Constitution Check section filled, violations justified | MEDIUM |
| SR-PLAN-08 | Architecture Defined | Architecture decisions documented with rationale | HIGH |
| SR-PLAN-09 | Data Model Generated | data-model.md exists (if entities in spec) | MEDIUM |
| SR-PLAN-10 | Contracts Generated | API contracts in /contracts/ (if API endpoints in spec) | MEDIUM |
| SR-PLAN-11 | ADR Coverage | All significant decisions have ADR-xxx | HIGH |
| SR-PLAN-12 | ADR Traceability | All ADRs linked to ≥1 requirement | MEDIUM |
| SR-PLAN-13 | Full ADR Files | High-impact decisions have full ADR | MEDIUM |

### Step 3: Dependency Verification

For each entry in Dependency Registry, verify:

```text
FOR EACH dependency in plan.md Dependency Registry:
  1. Package name matches official name (case-sensitive)
  2. Version exists in package registry
  3. Documentation URL is valid and accessible
  4. Key APIs listed actually exist in that version

  IF Context7 available:
    Use resolve-library-id → get-library-docs to verify
  ELSE:
    Flag for manual verification

  Result: VERIFIED | UNVERIFIED | DEPRECATED | NOT_FOUND
```

### Step 4: Completeness Scan

Scan plan.md for incomplete sections:

```text
INCOMPLETE_MARKERS = [
  "TODO", "TBD", "FIXME", "XXX",
  "[NEEDS CLARIFICATION]", "[RESEARCH NEEDED]",
  "???", "...", "< fill in >", "< TBD >"
]

FOR EACH section in plan.md:
  FOR EACH marker in INCOMPLETE_MARKERS:
    IF section contains marker:
      ERROR: "Section '{section}' contains incomplete marker: {marker}"
      Add to issues

FOR EACH required_section in [Technical Context, Dependency Registry, Architecture]:
  IF section is empty OR section contains only headers:
    ERROR: "Required section '{section}' is empty"
    Add to issues
```

### Step 5: Verdict

Based on validation results:

- **PASS**: All CRITICAL/HIGH criteria pass, dependencies verified → proceed to handoff
- **FAIL**: Any CRITICAL issue → self-correct and re-check (max 3 iterations)
  - Incomplete markers → research and fill in
  - Unverified dependencies → use Context7 or mark for manual check
  - Empty sections → generate content from spec
- **WARN**: Only MEDIUM issues → show warnings, proceed

### Step 6: Self-Correction Loop

```text
IF issues found AND iteration < 3:
  1. Fix each issue:
     - Replace TODO/TBD markers with researched answers
     - Verify dependencies via Context7
     - Fill empty sections from spec requirements
     - Generate missing research.md if needed
  2. Re-run self-review from Step 1
  3. Report: "Self-review iteration {N}: Fixed {issues}, re-validating..."

IF still failing after 3 iterations:
  - STOP
  - Report blocking issues to user
  - List unresolved items requiring human decision
  - Do NOT auto-transition to /speckit.tasks
```

### Step 7: Self-Review Report

After passing self-review, output:

```text
## Self-Review Complete ✓

**Artifact**: FEATURE_DIR/plan.md
**Iterations**: {N}

### Validation Results

| Check | Result |
|-------|--------|
| Technical Context | ✓ All sections filled |
| Incomplete Markers | ✓ None found |
| Dependency Registry | ✓ {N} dependencies listed |
| Dependencies Verified | ✓ {verified}/{total} via Context7 |
| Research Complete | ✓ research.md generated |
| Architecture | ✓ Decisions documented |

### Dependency Verification

| Package | Version | Status | Docs |
|---------|---------|--------|------|
| {package} | {version} | ✓ Verified | [link]({url}) |
| {package} | {version} | ⚠ Manual check needed | [link]({url}) |

### Generated Artifacts

- [x] plan.md (updated)
- [x] research.md
- [x] data-model.md
- [x] contracts/api.yaml

### Ready for Task Generation

All quality gates passed. Auto-transitioning to `/speckit.tasks`.
```

### Common Planning Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| TODO markers | Regex scan for TODO/TBD/FIXME | Research answer and replace |
| Unverified dependency | No Context7 confirmation | Query Context7 or note "manual verification required" |
| Empty section | Section has only header | Generate content from spec or mark as N/A with reason |
| Missing research.md | NEEDS CLARIFICATION was present but no research.md | Generate research.md with findings |
| Deprecated package | Context7 shows deprecation | Find replacement, document migration |
| Version mismatch | Specified version doesn't exist | Use latest stable or document constraint |

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
# Implementation Plan Complete

## Quick Summary

| Aspect | Value |
|--------|-------|
| **Feature** | {feature_name} |
| **Complexity** | {COMPLEXITY_TIER} ({complexity_score}/100) |
| **Phases** | {phase_count} implementation phases |
| **Dependencies** | {dep_count} external, {internal_count} internal |
| **Files to Modify** | ~{file_count} files |
| **Status** | {status_badge} |
| **Next Step** | {next_step} |

### Implementation Phases

1. **Phase 1**: {phase_1_name} ({file_count} files)
2. **Phase 2**: {phase_2_name} ({file_count} files)
3. **Phase 3**: {phase_3_name} ({file_count} files)

### Key Dependencies

| Package | Version | Verified |
|---------|---------|----------|
| {package_1} | {version} | ✓ |
| {package_2} | {version} | ✓ |
```

### Format Full Content

```text
IF MODE == COMPACT:
  OUTPUT: Quick Summary (above)
  OUTPUT: <details><summary>📄 View Full Plan</summary>
  OUTPUT: {full_plan_content}
  OUTPUT: </details>

ELIF MODE == STANDARD:
  OUTPUT: Quick Summary (above)
  OUTPUT: ---
  OUTPUT: {full_plan_content with collapsible verbose sections}

ELIF MODE == DETAILED:
  OUTPUT: Quick Summary (above)
  OUTPUT: ---
  OUTPUT: {full_plan_content all sections expanded}
  OUTPUT: ---
  OUTPUT: {self_review_report}
  OUTPUT: {dependency_verification_details}
```

### Update Artifact Registry

```text
Read `templates/shared/traceability/artifact-registry.md` and apply:

UPDATE_REGISTRY("plan", "FEATURE_DIR/plan.md", {
  parent_spec_version: registry.artifacts.spec.version,
  phase_count: {phase_count}
})

# Check cascade impact
IF registry was updated:
  staleness = CHECK_STALENESS(registry)
  IF staleness.tasks_stale:
    OUTPUT: "Note: tasks.md may need refresh after plan changes."
```
