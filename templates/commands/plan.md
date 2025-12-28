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
      invoke: speckit.analyze
      args: "--profile plan_validate --quiet"
      skip_flag: "--skip-validate"
      timeout: 45s
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
  thinking_budget: 8000
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

## Outline

0. **Load project language setting**:

   Read `/memory/constitution.md` and extract the `language` value from the Project Settings table.

   ```text
   IF Project Settings section exists AND language row found:
     ARTIFACT_LANGUAGE = extracted value (e.g., "ru", "en", "de")
   ELSE:
     ARTIFACT_LANGUAGE = "en" (default)

   Apply language rules from templates/shared/language-context.md:
   - Generate all prose content in ARTIFACT_LANGUAGE
   - Keep IDs, technical terms (API, JWT), and code in English
   ```

   Report: "Generating plan in {LANGUAGE_NAME} ({ARTIFACT_LANGUAGE})..."

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `/memory/constitution.md`. Load IMPL_PLAN template (already copied). Confirm ARTIFACT_LANGUAGE from constitution Project Settings.

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 0.5: Verify APIs and populate Dependency Registry (use Context7)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Update Feature Manifest**: After plan artifacts are generated:
   ```text
   MANIFEST_FILE = specs/features/.manifest.md
   FEATURE_ID = extract from BRANCH (first 3 digits)

   IF exists(MANIFEST_FILE):
     Find row where ID = FEATURE_ID
     Update Status column: SPEC_COMPLETE → PLANNED
     Update "Last Updated" column: today's date
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

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
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

**Output**: research.md with all NEEDS CLARIFICATION resolved

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
