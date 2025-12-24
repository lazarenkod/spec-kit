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
  reasoning_mode: extended
  thinking_budget: 8000
  plan_mode_trigger: true
  subagents:
    - role: architecture-specialist
      trigger: "when evaluating technology choices or designing system structure"
      prompt: "Analyze architecture options for {REQUIREMENT}: trade-offs, patterns, recommendations"
    - role: design-researcher
      trigger: "when planning UI features requiring design system decisions"
      prompt: "Research design system approaches for {UI_FEATURE}"
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
agent_scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `/memory/constitution.md`. Load IMPL_PLAN template (already copied).

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
