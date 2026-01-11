---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
persona: architect-agent
handoff:
  requires: handoffs/specify-to-plan.md
  generates: handoffs/plan-to-tasks.md
  template: templates/handoff-template.md
inline_gates:
  enabled: true
  skip_flag: "--skip-gates"
  strict_flag: "--strict-gates"
  full_flag: "--full-gates"
  mode: progressive
  on_failure: block
  gates:
    - id: IG-PLAN-001
      name: "Constitution Alignment"
      pass: D
      tier: 2
      threshold: 0
      severity: CRITICAL
      message: "Plan violates project constitution"
    - id: IG-PLAN-002
      name: "Tech Consistency"
      pass: F
      tier: 2
      threshold: 0
      severity: HIGH
      message: "Terminology inconsistent between spec and plan"
    - id: IG-PLAN-003
      name: "Spec Alignment"
      checks: [SR-PLAN-07]
      tier: 2
      threshold: 0
      severity: HIGH
      message: "Plan references undefined spec elements"
    - id: IG-PLAN-004
      name: "Dependencies Verified"
      checks: [SR-PLAN-03, SR-PLAN-04]
      tier: 2
      threshold: 0
      severity: MEDIUM
      message: "External dependencies not verified"
    - id: IG-PLAN-005
      name: "Strategic Narrative Present"
      checks: [SR-PLAN-14]
      tier: 2
      threshold: 0
      severity: HIGH
      message: "Plan missing Strategic Narrative (Working Backwards) section"
    - id: IG-PLAN-006
      name: "Pre-Mortem Coverage"
      checks: [SR-PLAN-15, SR-PLAN-16, SR-PLAN-27]
      tier: 2
      threshold: 0
      severity: HIGH
      message: "Pre-Mortem analysis incomplete (need 3+ scenarios, Tech+Integration coverage, kill criteria)"
    - id: IG-PLAN-007
      name: "NFR Definition"
      checks: [SR-PLAN-17, SR-PLAN-18]
      tier: 2
      threshold: 0
      severity: CRITICAL
      message: "NFRs not defined (need P95/P99 latency and availability targets)"
    - id: IG-PLAN-008
      name: "RTM Coverage"
      checks: [SR-PLAN-19, SR-PLAN-20]
      tier: 2
      threshold: 0
      severity: HIGH
      message: "Requirements Traceability incomplete (coverage <90% or orphans exist)"
    - id: IG-PLAN-009
      name: "Brainstorm-Curate Enforcement"
      checks: [SR-PLAN-21, SR-PLAN-22]
      tier: 2
      threshold: 0
      severity: HIGH
      message: "Brainstorm-Curate protocol not applied or scoring matrix not visible for non-trivial decisions"
    - id: IG-PLAN-010
      name: "Observability Defined"
      checks: [SR-PLAN-23, SR-PLAN-24]
      tier: 2
      threshold: 0
      severity: MEDIUM
      message: "Observability plan incomplete (need SLIs/SLOs and alerts with runbooks)"
    - id: IG-PLAN-011
      name: "Scalability Planned"
      checks: [SR-PLAN-25, SR-PLAN-26]
      tier: 2
      threshold: 0
      severity: MEDIUM
      message: "Scalability strategy incomplete (need capacity baseline and scaling triggers)"
    - id: IG-PLAN-012
      name: "Plan Mode Exploration Complete"
      checks: [PM-001, PM-002]
      tier: 1
      threshold: 0
      severity: CRITICAL
      message: "Plan Mode exploration phase incomplete"
      condition: "plan_mode.enabled AND plan_mode.depth_level >= 1"
    - id: IG-PLAN-013
      name: "Plan Mode Review Pass"
      checks: [PM-004, PM-005]
      tier: 2
      threshold: 0
      severity: HIGH
      message: "Plan Mode review detected critical issues"
      condition: "plan_mode.enabled AND plan_mode.depth_level >= 2"
    - id: IG-PLAN-014
      name: "Plan Mode Quality Threshold"
      checks: [PM-006]
      tier: 3
      threshold: 80
      severity: CRITICAL
      message: "Aggregate quality score below threshold (PQS < 80)"
      condition: "plan_mode.enabled AND plan_mode.depth_level >= 2"
handoffs:
  - label: Create Tasks
    agent: speckit.tasks
    prompt: Break the plan into tasks
    auto: true
    condition:
      - "plan.md completed with all phases"
      - "research.md exists (Phase 0 complete)"
      - "All [NEEDS CLARIFICATION] resolved"
      - "Inline gates passed (IG-PLAN-*)"
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
plan_mode:
  enabled: auto  # auto (depth-based), explicit depth level, or legacy flags

  # Default depth levels by complexity tier
  depth_defaults:
    TRIVIAL: 0   # 0-25: Standard mode
    SIMPLE: 0    # 26-50: Standard mode
    MODERATE: 1  # 51-70: Lite exploration
    COMPLEX: 2   # 71+: Moderate (exploration + constitution review)

  # Depth level definitions
  depth_levels:
    0:  # Standard
      name: "Standard"
      exploration: false
      review_passes: []
    1:  # Lite
      name: "Lite"
      exploration:
        agents: [pattern-researcher, constraint-mapper]
        budget_s: 90
      review_passes: []
    2:  # Moderate
      name: "Moderate"
      exploration:
        agents: [pattern-researcher, alternative-analyzer, constraint-mapper, best-practice-synthesizer]
        budget_s: 180
      review_passes: [constitution_alignment]
      budget_s: 210  # 180 + 30
    3:  # Full
      name: "Full"
      exploration:
        agents: [pattern-researcher, alternative-analyzer, constraint-mapper, best-practice-synthesizer]
        budget_s: 180
      review_passes: [constitution_alignment, completeness_check, edge_case_detection, testability_audit]
      budget_s: 300  # 180 + 120

  # Keyword triggers upgrade depth level by +1 (max 3)
  keyword_triggers:
    - distributed
    - multi-service
    - migration
    - security-critical
    - real-time
    - high-availability
    - microservices
    - event-driven
    - data-intensive

  flags:
    depth: "--depth-level <0-3>"  # Primary flag
    enable: "--plan-mode"         # Alias for --depth-level 3
    disable: "--no-plan-mode"     # Alias for --depth-level 0
claude_code:
  model: opus
  reasoning_mode: extended
  # Rate limit tiers (default: max for Claude Code Max $20)
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 8000
        max_parallel: 2
        batch_delay: 8000
        wave_overlap_threshold: 0.90
      pro:
        thinking_budget: 16000
        max_parallel: 4
        batch_delay: 4000
        wave_overlap_threshold: 0.80
      max:
        thinking_budget: 32000
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
  plan_mode_trigger: true
  orchestration:
    max_parallel: 8
    role_isolation: false
  operation_batching:
    enabled: true
    skip_flag: "--sequential"
    framework: templates/shared/operation-batching.md
    strategies:
      context_reads: true    # Batch context file reads
      prefetch: true         # Speculative parallel load
      searches: true         # Batch research searches
      validations: true      # Batch inline gate checks
      sections: true         # Batch plan sections by dependency wave
  artifact_extraction:
    enabled: true
    skip_flag: "--full-context"
    framework: templates/shared/artifact-extraction.md
    spec_fields:
      - fr_list             # FR-001, FR-002, ...
      - as_list             # AS-1A, AS-1B, ...
      - ec_list             # EC-001, EC-002, ...
      - story_priorities    # {US1: P1a, ...}
      - problem_statement   # First paragraph only
      - target_customer     # From personas
      - fr_summaries        # [{id, summary}, ...]
      - as_summaries        # [{id, name}, ...]
    concept_fields:
      - pr_faq_value_prop   # 1-2 sentences
      - mvp_scope           # FR IDs in MVP
      - market_sizing       # {tam, sam, som}
      - epic_ids            # Epic hierarchy
    constitution_fields:
      - domain_type
      - language
      - framework
  section_batching:
    enabled: true
    skip_flag: "--sequential-sections"
    algorithm: templates/shared/operation-batching.md#SECTION_BATCH
    sections:
      # Wave 1: Independent sections (no dependencies, run in parallel)
      - id: strategic_narrative
        name: "Strategic Narrative"
        phase: "-1"
        depends_on: []
        sources: [concept.md, spec.md]
        model: sonnet
      - id: pre_mortem
        name: "Pre-Mortem Analysis"
        phase: "-1"
        depends_on: []
        sources: [concept.md]
        model: sonnet
      - id: technical_context
        name: "Technical Context"
        phase: "0"
        depends_on: []
        sources: [spec.md, constitution.md]
        model: sonnet
      - id: nfr_definition
        name: "NFR Definition"
        phase: "0.75"
        depends_on: []
        sources: [spec.md]
        model: sonnet
      - id: dependency_registry
        name: "Dependency Registry"
        phase: "0.5"
        depends_on: []
        sources: [spec.md]
        model: sonnet
      # Wave 2: Depends on Wave 1
      - id: adrs
        name: "Architecture Decisions (ADRs)"
        phase: "0"
        depends_on: [technical_context, nfr_definition]
        sources: [spec.md, research.md]
        model: sonnet
      # Wave 3: Depends on ADRs or NFRs
      - id: rtm
        name: "Requirements Traceability Matrix"
        phase: "1.75"
        depends_on: [adrs]
        sources: [spec.md]
        model: sonnet
      - id: observability
        name: "Observability & Monitoring Plan"
        phase: "1.5"
        depends_on: [nfr_definition]
        sources: [spec.md]
        model: sonnet
      - id: scalability
        name: "Scalability Strategy"
        phase: "1.5"
        depends_on: [nfr_definition, technical_context]
        sources: [spec.md]
        model: sonnet
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

## Section Batching Execution

**CRITICAL**: When `section_batching.enabled` is true, use wave-based parallel execution instead of sequential phases.

```text
IF section_batching.enabled AND NOT "--sequential-sections" IN ARGS:

  IMPORT: templates/shared/operation-batching.md#SECTION_BATCH

  # Parse section config from frontmatter
  sections = PARSE(claude_code.section_batching.sections)

  # Setup wave-based todos (not per-section)
  TodoWrite([
    {content: "Wave 1: Strategic + Pre-Mortem + Context + NFRs + Deps (5 sections)", status: "in_progress", activeForm: "Generating Wave 1 sections in parallel..."},
    {content: "Wave 2: Architecture Decisions (ADRs)", status: "pending", activeForm: "Generating Architecture Decisions..."},
    {content: "Wave 3: RTM + Observability + Scalability (3 sections)", status: "pending", activeForm: "Generating Wave 3 sections in parallel..."},
    {content: "Self-review and validation", status: "pending", activeForm: "Running self-review..."}
  ])

  # Execute SECTION_BATCH algorithm
  section_results = SECTION_BATCH(sections, section_batching)

  # Assemble results into plan.md
  FOR section_id, content IN section_results:
    IF content:
      INSERT content INTO plan.md at appropriate section

  # Mark waves complete and proceed to self-review
  TodoWrite([
    {content: "Wave 1: Strategic + Pre-Mortem + Context + NFRs + Deps", status: "completed", ...},
    {content: "Wave 2: Architecture Decisions (ADRs)", status: "completed", ...},
    {content: "Wave 3: RTM + Observability + Scalability", status: "completed", ...},
    {content: "Self-review and validation", status: "in_progress", ...}
  ])

ELSE:
  # Fallback: sequential phase execution (legacy mode)
  LOG "⚠️ Section batching DISABLED (--sequential-sections flag or config)"
  EXECUTE phases sequentially as defined below
```

### Expected Performance Improvement

| Mode | Waves | Parallel Sections | Time |
|------|-------|-------------------|------|
| Sequential | 9 | 1 per wave | ~90s |
| Batched | 3 | 5, 1, 3 | ~35s |
| **Improvement** | | | **~60% faster** |

---

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

### Phase -1: Strategic Context Import (NEW)

**Prerequisites**: concept.md exists (optional but recommended)

**Purpose**: Import strategic context from concept phase to ensure plan aligns with product vision.

1. **PR/FAQ Import**:
   ```text
   IF concept.md exists AND has PR/FAQ section:
     EXTRACT: Product name, target customer, quantified value proposition
     EXTRACT: MVP scope (what we're building, what we're NOT building)
     EXTRACT: Time to value milestones
     EXTRACT: Go/No-Go criteria

     POPULATE: plan.md "Strategic Narrative" section

     LOG: "Imported PR/FAQ from concept.md"
   ELSE:
     LOG: "No concept.md PR/FAQ found. Generating strategic narrative from spec..."

     GENERATE using spec.md:
       - Product/Feature name from spec title
       - Target customer from personas (if any) or infer from requirements
       - Value proposition from problem statement
       - MVP scope from FR-xxx prioritization
       - Time to value from acceptance criteria complexity

     POPULATE: plan.md "Strategic Narrative" section

     LOG: "Generated strategic narrative from spec.md"
   ```

2. **Pre-Mortem Generation**:
   ```text
   IF concept.md exists AND has Pre-Mortem section:
     EXTRACT: Failure scenarios
     EXTRACT: Early warning signs
     EXTRACT: Kill criteria

     POPULATE: plan.md "Pre-Mortem Analysis" section

     LOG: "Imported Pre-Mortem from concept.md"
   ELSE:
     LOG: "Generating Pre-Mortem analysis..."

     GENERATE minimum 3 failure scenarios covering:
       - Technical failure mode (database, performance, integration)
       - External/Dependency failure mode (third-party APIs, rate limits)
       - Integration failure mode (complexity underestimation, scope creep)

     FOR EACH scenario:
       - Identify early warning signs (metrics, patterns)
       - Define prevention strategy with owners
       - Establish kill criteria with specific thresholds

     POPULATE: plan.md "Pre-Mortem Analysis" section

     LOG: "Generated {N} failure scenarios"
   ```

3. **Go/No-Go Validation**:
   ```text
   EVALUATE Go/No-Go criteria:
     - Technical feasibility: Are all blockers resolved?
     - Dependencies available: Are PKG/API verified?
     - Team capacity: Is sprint allocated?

   IF any criterion NOT met:
     WARN: "Go/No-Go criterion not met: {criterion}"
     ADD to plan.md Go/No-Go table with current status
   ```

**Output**:
- plan.md "Strategic Narrative" section populated
- plan.md "Pre-Mortem Analysis" section populated (minimum 3 scenarios)
- Go/No-Go criteria evaluated

---

### Phase 0.1: Best Practices Loading

**Prerequisites:** spec.md complete

**Purpose:** Load domain best practices before architecture decisions.

This phase ensures that architecture decisions are informed by proven patterns from the domain knowledge base.

**Steps:**

1. **Detect Domain & Technology Stack**:
   ```bash
   # Read from memory/constitution.md
   DOMAIN=$(grep "^domain:" memory/constitution.md | cut -d: -f2 | tr -d ' ')
   TECH_STACK=$(grep "^tech_stack:" memory/constitution.md | cut -d: -f2-)
   ```

2. **Load Best Practices Catalog**:
   - Read `memory/knowledge/best-practices/by-domain/{{DOMAIN}}.md` (if exists)
   - Read `memory/knowledge/best-practices/by-technology/{{TECH}}.md` for each tech in stack (if exists)
   - If files don't exist yet (first run), skip with warning and proceed

3. **Extract Applicable Practices**:
   For each practice in catalog:
   - Match practice applicability against spec requirements
   - Extract: Name, Category, Implementation pattern, Evidence tier, Trade-offs
   - Filter out practices not relevant to this feature

4. **Inject into research.md**:
   Before generating ADRs, add section:
   ```markdown
   ## Applicable Best Practices

   The following domain best practices should inform architecture decisions:

   ### {{PRACTICE_NAME}} ({{CATEGORY}})

   **Evidence**: {{SOURCE}} [{{TIER}}]

   **When to Apply**: {{APPLICABILITY}}

   **Implementation Pattern**:
   {{IMPLEMENTATION_CODE_OR_PATTERN}}

   **Trade-offs**:
   - ✅ Pros: {{BENEFITS}}
   - ❌ Cons: {{COSTS}}

   **Related ADRs**: Will be referenced in ADR-xxx if chosen
   ```

5. **Example** (fintech domain):
   For payment processing feature:
   - Practice: "Idempotency Keys for Payments" [AUTHORITATIVE - Stripe docs]
   - Practice: "Daily Payment Reconciliation" [STRONG - IEEE 2023]
   - Practice: "AES-256 Encryption with Key Rotation" [AUTHORITATIVE - PCI-DSS]
   - Practice: "Webhook Signature Verification" [AUTHORITATIVE - Stripe/PayPal]

**Output:**
- `research.md` "Applicable Best Practices" section populated BEFORE ADR generation
- Each ADR can reference relevant best practices with evidence citations
- Prevents reinventing solutions that have authoritative/strong evidence

---

### Phase 0.2: Technical Constraints Loading

**Prerequisites:** Phase 0.1 complete

**Purpose:** Load technical constraints before performance NFRs to prevent impossible requirements.

This phase validates that NFRs don't exceed platform limits.

**Steps:**

1. **Load Constraints Catalog**:
   For each technology in tech stack:
   - Read `memory/knowledge/constraints/platforms/{{TECH}}.md` (if exists)
   - Extract: Rate limits, quotas, timeouts, memory limits, storage limits
   - If file doesn't exist, skip with warning

2. **Build Constraints Profile**:
   ```yaml
   constraints_profile:
     stripe_api:
       rate_limit: 100 req/sec (default), 1000 req/sec (high volume)
       webhook_timeout: 30 seconds
       file_upload_max: 10 MB
       idempotency_key_ttl: 24 hours

     postgresql:
       max_connections: 100 (default)
       statement_timeout: 30 seconds
       max_row_size: 8 KB (without TOAST)
   ```

3. **Validate NFRs Against Constraints**:
   For each NFR-PERF-xxx in spec.md:
   ```python
   IF NFR requires X req/sec:
     AND constraint = Y req/sec:
       IF X > Y:
         FLAG: "NFR-PERF-xxx exceeds {{TECH}} limit ({{Y}} req/sec)"
         SUGGEST: "Use request batching OR rate limiting queue OR request limit increase"
         SEVERITY: HIGH
   ```

4. **Auto-Generate Constraint-Driven NFRs**:
   For each constraint that affects this feature:
   ```markdown
   #### Platform Constraints (Auto-Generated)

   **NFR-PERF-{{TECH}}-XXX**: Handle {{CONSTRAINT_TYPE}} ({{LIMIT}}) [{{PRIORITY}}]
   - Acceptance: {{IMPLEMENTATION_STRATEGY}}
   - Evidence: {{SOURCE}} [{{TIER}}]
   - Constraint: {{LIMIT_VALUE}} per {{SCOPE}}
   - Workaround: {{WORKAROUND_STRATEGY}}
   - Traceability: → FR-{{XXX}}
   ```

5. **Examples**:
   ```markdown
   **NFR-PERF-STRIPE-001**: Handle API rate limit (100 req/sec) [HIGH]
   - Acceptance: Exponential backoff implemented for 429 responses
   - Evidence: Stripe Rate Limits [AUTHORITATIVE]
   - Constraint: 100 req/sec per account (default tier)
   - Workaround: If approaching limit, request increase to 1000 req/sec
   - Traceability: → FR-003 (Process payments via Stripe)

   **NFR-PERF-STRIPE-002**: Webhook response time <10 seconds [MEDIUM]
   - Acceptance: Webhook endpoint responds within 10 seconds (30s hard limit)
   - Evidence: Stripe Webhook Documentation [AUTHORITATIVE]
   - Constraint: 30 second timeout
   - Workaround: Use async queue for long-running webhook processing
   - Traceability: → FR-005 (Receive payment notifications)
   ```

6. **Flag Violations**:
   ```markdown
   ## ⚠️ Constraint Violations

   **VIOLATION-001**: NFR-PERF-001 requires 200 req/sec, but Stripe limit = 100 req/sec
   - Impact: BLOCKING (cannot achieve requirement)
   - Resolution Options:
     1. Request rate limit increase from Stripe (2-4 week lead time)
     2. Implement request batching to reduce API calls by 50%
     3. Revise NFR-PERF-001 target to 80 req/sec (with buffer)
   - Recommendation: Option 2 + Option 3 combined
   ```

**Output:**
- `plan.md` NFR section with validated constraints
- `research.md` with workarounds if constraints violated
- Constraint violation warnings BEFORE implementation starts
- Auto-generated NFRs for known platform limits

---

### Phase 0.3: Standards Verification

**Prerequisites:** Phase 0.2 complete

**Purpose:** Verify architecture against official standards before implementation.

This phase ensures compliance requirements are baked into architecture from the start.

**Steps:**

1. **Load Compliance Requirements**:
   For each standard in COMPLIANCE_REQUIRED (from specify phase):
   - Read `memory/knowledge/standards/compliance/{{STANDARD}}.md`
   - Extract: Critical requirements (CRITICAL), High-priority requirements (HIGH)
   - Build compliance checklist

2. **Map Requirements to Plan**:
   For EACH requirement:
   ```markdown
   {{STANDARD}} Req {{NUMBER}}: "{{REQUIREMENT_TITLE}}"

   **Mapped to:**
   - FR-{{XXX}}: {{FUNCTIONAL_REQUIREMENT}}
   - NFR-{{XXX}}: {{NON_FUNCTIONAL_REQUIREMENT}}

   **Implementation Strategy:**
   {{HOW_THIS_WILL_BE_IMPLEMENTED}}

   **Verification Method:**
   {{HOW_TO_VERIFY_COMPLIANCE}}

   **Traceability:**
   {{REQUIREMENT}} → FR-{{XXX}} → Implementation in {{FILE}}
   ```

3. **Example** (PCI-DSS for payment feature):
   ```markdown
   ### PCI-DSS Compliance Mapping

   **PCI-DSS Req 3.2**: "Do not store sensitive authentication data (CVV/CVC) after authorization"

   **Mapped to:**
   - FR-003: Process payment via Stripe API
   - NFR-SEC-PCI-001: Do not store CVV/CVC [CRITICAL]

   **Implementation Strategy:**
   - Use Stripe.js to tokenize card on client side (CVV never reaches server)
   - Database schema audit: NO cvv, cvc, cvv2 columns
   - Log sanitization: Strip CVV patterns before logging
   - Code review: Grep for prohibited storage patterns

   **Verification Method:**
   - Schema review: `SHOW COLUMNS FROM payments;` → no CVV fields
   - Code scan: `grep -ri "cvv\|cvc" src/` → no storage patterns
   - Log analysis: Verify no CVV patterns in application logs

   **Traceability:**
   PCI-DSS Req 3.2 → NFR-SEC-PCI-001 → Stripe.js tokenization → src/payments/stripe.ts:45
   ```

4. **Generate Compliance Verification Tasks**:
   Add to tasks.md (will be created in /speckit.tasks):
   ```markdown
   **TASK-SEC-001**: Verify PCI-DSS Req 3.2 compliance [CRITICAL]
   - Type: Security Validation
   - Prerequisites: Payment processing implementation complete
   - Validation Steps:
     1. Run schema audit: Check for prohibited columns
     2. Run code scan: Grep for CVV storage patterns
     3. Review logs: Ensure CVV sanitization
   - Acceptance: All 3 checks pass
   - Traceability: → NFR-SEC-PCI-001, PCI-DSS Req 3.2
   ```

5. **Create Compliance Traceability Matrix**:
   In plan.md, add section:
   ```markdown
   ## Compliance Traceability Matrix

   | Standard | Requirement | FR | NFR | Implementation | Verification | Status |
   |----------|-------------|:--:|:---:|----------------|--------------|:------:|
   | PCI-DSS Req 3.2 | No CVV storage | FR-003 | NFR-SEC-PCI-001 | Stripe.js tokenization | Schema audit + code scan | ⏳ |
   | PCI-DSS Req 3.4 | Encrypt PAN | FR-004 | NFR-SEC-PCI-002 | AES-256 + KMS | Encryption validation | ⏳ |
   | PCI-DSS Req 4.2 | TLS 1.2+ | FR-003 | NFR-SEC-PCI-005 | Nginx TLS config | SSL Labs scan | ⏳ |

   **Legend**: ⏳ Pending | ✅ Verified | ❌ Non-compliant
   ```

6. **Flag Missing Implementations**:
   ```markdown
   ## ⚠️ Compliance Gaps

   **GAP-001**: PCI-DSS Req 6.5.10 (Injection Prevention) not addressed
   - Triggered by: FR-003 (Process payment API)
   - Missing NFR: SQL injection prevention
   - Required Action: Add NFR-SEC-PCI-007 with parameterized queries
   - Severity: CRITICAL
   ```

**Output:**
- `plan.md` "Compliance Verification" section with traceability matrix
- `research.md` with compliance implementation strategies
- Compliance verification tasks flagged for tasks.md
- Gaps identified BEFORE implementation starts

---

### Phase 0: Outline & Research

#### Standard Mode (Default)

Phase 0 runs in Standard Mode when Plan Mode is disabled (depth level 0).

**Architecture Decision Protocol** (ENHANCED):

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

---

#### Plan Mode (Depth Level ≥ 1)

**Trigger Conditions:**
- Auto: Complexity ≥ 71 (COMPLEX tier)
- Auto: Keyword triggers (distributed, microservices, migration, security-critical, real-time, high-availability)
- Manual: `--plan-mode` flag (forces depth level 3)
- Manual: `--depth-level <1-3>` flag (explicit level)

**Depth Level Selection:**
- **Level 1 (Lite)**: MODERATE features (complexity 51-70) - Quick exploration only
- **Level 2 (Moderate)**: COMPLEX features (complexity 71+) - Exploration + constitution review
- **Level 3 (Full)**: Explicit `--plan-mode` - Complete exploration + all review passes

**Budget:** +90s (L1), +210s (L2), +300s (L3)

---

**Phase 0 Exploration (Before Standard Mode)**

When Plan Mode is enabled, Phase 0 begins with a research phase using 4 specialized agents:

**Agent Execution Flow:**

```text
# Depth Level 1 (Lite) - 90s
EMIT SINGLE MESSAGE with 2 parallel Task calls:
  Task(role="pattern-researcher", subagent_type="Explore", model="haiku", timeout=45s)
  Task(role="constraint-mapper", subagent_type="Explore", model="haiku", timeout=45s)
  ↓ (wait for both, 45s wall time)
Total: 90s

# Depth Level 2-3 (Moderate/Full) - 180s
EMIT SINGLE MESSAGE with 3 parallel Task calls:
  Task(role="pattern-researcher", subagent_type="Explore", model="haiku", timeout=45s)
  Task(role="alternative-analyzer", subagent_type="general-purpose", model="haiku", timeout=45s)
  Task(role="constraint-mapper", subagent_type="Explore", model="haiku", timeout=45s)
  ↓ (wait for all 3, 45s wall time)

EMIT Task(role="best-practice-synthesizer", subagent_type="general-purpose", model="sonnet", timeout=60s)
  ↓ (wait, 60s wall time)
Total: 180s
```

**Agent Specifications:**

1. **pattern-researcher** (haiku, 45s, parallel)
   - Search codebase for similar implementations (Glob + Read)
   - Extract architectural patterns (layering, error handling)
   - Document conventions (naming, file structure)
   - Output: Existing Patterns section in research.md

2. **alternative-analyzer** (haiku, 45s, parallel) - *Only Depth 2+*
   - Generate 3-5 alternatives (Conventional, Minimal, Future-Proof, Unconventional)
   - Score each: Complexity (1-5), Testability (1-5), Maintainability (1-5), Performance (1-5), Constitution Alignment (1-5)
   - Recommend highest-scoring approach (or justify deviation)
   - Output: Alternative Approaches with scoring matrix

3. **constraint-mapper** (haiku, 45s, parallel)
   - Extract NFRs from spec.md (performance, security, scalability)
   - Map each NFR → implementation constraint
   - Detect conflicts (e.g., performance vs. security)
   - Flag unconstrained areas
   - Output: Constraint Map with conflict resolutions

4. **best-practice-synthesizer** (sonnet, 60s, sequential) - *Only Depth 2+*
   - Synthesize findings from above 3 agents
   - Reconcile alternatives with patterns
   - Apply constraint filters
   - Provide final recommendation with edge case analysis
   - Output: Synthesis & Recommendation section

**Output Artifact:** `research.md` in feature directory

**research.md Structure:**

```markdown
# Research Findings

## Existing Patterns

- **Pattern 1**: [description]
- **Pattern 2**: [description]

## Alternative Approaches

| Approach | Complexity | Testability | Maintainability | Performance | Alignment | Total |
|----------|-----------|------------|-----------------|-------------|-----------|-------|
| Conventional | 4 | 4 | 4 | 3 | 5 | 20/25 |
| Minimal | 5 | 3 | 3 | 4 | 3 | 18/25 |
| Future-Proof | 2 | 5 | 5 | 3 | 4 | 19/25 |

**Recommended:** Conventional (20/25)
- Pros: Aligns with constitution, well-tested pattern
- Cons: Slightly lower performance
- Justification: Team expertise + maintainability priority

## Constraint Map

| NFR | Constraint | Conflict | Resolution |
|-----|-----------|----------|------------|
| NFR-001 (P95 <100ms) | Use Redis cache | Conflicts with NFR-003 (security) | Encrypt cache at rest |
| NFR-002 (99.9% availability) | Multi-region deployment | None | Implement in Phase 3 |

## Synthesis & Recommendation

[Synthesized findings with final approach recommendation and edge case analysis]
```

**Context Injection:**

Exploration findings are prepended to all subsequent phase prompts:

```text
# Original prompt (Phase 1 agent)
Design the API layer for {feature}.

# Enhanced prompt (with Plan Mode context)
🔍 **Plan Mode Context:**
- Recommended Approach: OAuth 2.0 + JWT (scored 22/25)
- Key Constraint: P95 <100ms → Use Redis cache
- Edge Cases Identified: Rate limiting, token rotation

Design the API layer for {feature}. Consider the exploration findings above.
```

**Graceful Fallback:**

```text
IF exploration_phase_fails:
  LOG: "⚠️ Plan Mode exploration failed, falling back to Standard Mode"
  DISABLE_PLAN_MODE = true
  CONTINUE with Standard Mode (Architecture Decision Protocol)
```

**Quality Gates:**

Exploration phase is validated by IG-PLAN-012:
- PM-001: All required agents completed (CRITICAL)
- PM-002: ≥3 alternatives with scoring matrix (CRITICAL, depth 2+ only)

---

**Phase 0 Standard Mode Execution (After Exploration)**

After exploration (or if Plan Mode disabled), execute the standard Architecture Decision Protocol documented above, enriched with exploration context if available.

---

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

---

### Phase 0.75: NFR Definition (NEW)

**Prerequisites**: Phase 0.5 (API Verification) complete

**Purpose**: Define measurable NFRs with specific targets BEFORE implementation.

1. **Performance NFR Generation**:
   ```text
   FOR EACH api_endpoint IN contracts/api.yaml (or inferred from spec):
     DEFINE NFR-PERF-xxx:
       - P50, P95, P99, P99.9 latency targets
       - Throughput requirements (RPS)
       - Measurement method (OTel traces, load test)

     LINK to ADR if performance drove architecture decision

   EXAMPLE:
     NFR-PERF-001: API Response Time
       P50: <50ms, P95: <200ms, P99: <500ms, P99.9: <1000ms
       Measurement: OTel traces with load test validation

   LOG: "Defined {N} performance NFRs"
   ```

2. **Reliability NFR Generation**:
   ```text
   DEFINE availability_target with justification:

   OPTIONS:
     - 99.9% (Three 9s) = 43.8 min/month downtime
     - 99.95% (3.5 9s) = 21.9 min/month downtime
     - 99.99% (Four 9s) = 4.4 min/month downtime

   SELECT based on:
     - Business criticality (revenue impact per minute of downtime)
     - User expectations (B2B vs B2C, async vs real-time)
     - Cost implications (geo-redundancy, hot standby)

   DOCUMENT justification: "Why this target, why not higher/lower"

   DEFINE MTTR and MTBF targets:
     - MTTR (Mean Time to Recovery): Target recovery time
     - MTBF (Mean Time Between Failures): Expected stability

   LOG: "Availability target: {target} with {justification}"
   ```

3. **Observability NFR Generation**:
   ```text
   DEFINE NFR-OBS-xxx for:
     - Trace coverage: 100% of API endpoints (OTel auto-instrumentation)
     - Log correlation: Trace ID in all logs (structured logging)
     - Metric cardinality: <10K unique series (label constraints)
     - Alert coverage: All NFR-PERF metrics monitored

   LOG: "Defined {N} observability NFRs"
   ```

4. **Security NFR Generation**:
   ```text
   DEFINE NFR-SEC-xxx based on spec requirements:
     - Authentication method: OAuth2/JWT/Session
     - Encryption: TLS 1.3 in transit, AES-256 at rest
     - Input validation: OWASP Top 10 compliance

   LOG: "Defined {N} security NFRs"
   ```

5. **Load Profile Definition**:
   ```text
   EXTRACT from spec or estimate:
     - Peak concurrent users
     - Request rate at peak (RPS)
     - Data volume (records, storage)
     - Growth rate (monthly % increase)

   POPULATE: plan.md NFR "Load Profile" section

   LOG: "Load profile: {users} users, {rps} RPS, {growth}% monthly growth"
   ```

**Validation Gate**:

| Condition | Severity | Action |
|-----------|----------|--------|
| No NFR-PERF-xxx defined | CRITICAL | Block until P95/P99 targets set |
| No availability target | HIGH | Block until justified target set |
| Missing load profile | MEDIUM | Warn and use defaults |

**Output**:
- plan.md "Non-Functional Requirements (NFRs)" section fully populated
- Each NFR linked to relevant ADR (if applicable)
- Measurement methods specified
- Load profile defined

---

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

---

### Phase 1.5: Observability & Scalability Planning (NEW)

**Prerequisites**: Phase 1 (Design & Contracts) complete

**Purpose**: Define monitoring, alerting, and scaling strategy BEFORE implementation.

1. **SLI/SLO Definition**:
   ```text
   FOR EACH NFR-PERF-xxx and NFR-REL-xxx:
     DEFINE corresponding SLI:
       - Name and definition
       - Good event criteria
       - Valid event criteria

     DEFINE corresponding SLO:
       - Target percentage (e.g., 99.5%)
       - Measurement window (e.g., 30 days)
       - Error budget calculation
       - Alert threshold (e.g., 50% budget consumed)

   EXAMPLE:
     SLI-001: Request Latency
       Good event: response_time < 500ms
       Valid event: All HTTP 2xx/4xx requests

     SLO-001: 99.5% of requests < 500ms over 30 days
       Error budget: 0.5% = 3.6 hours
       Alert: Trigger at 50% budget consumed

   LOG: "Defined {N} SLIs and {N} SLOs"
   ```

2. **Dashboard Specification**:
   ```text
   DEFINE dashboards:
     - Overview: Health at a glance (SLO status, error rate, P50/P99)
     - Performance: Deep dive (latency histogram, throughput, saturation)
     - Business: Feature adoption (DAU, usage, conversion)
     - Dependency: External health (API latency, errors, rate limits)

   FOR EACH dashboard:
     - List key panels with metrics
     - Specify refresh rate (10s/30s/5m)
     - Define target audience (on-call, developers, product)

   LOG: "Specified {N} dashboards"
   ```

3. **Alert Definition**:
   ```text
   FOR EACH SLO:
     DEFINE alert:
       - Condition: metric threshold and duration
       - Severity: WARNING or CRITICAL
       - Runbook link: REQUIRED (no alert without runbook)
       - Notification channel: Slack, PagerDuty, email

   VALIDATION: Every alert MUST have a runbook reference

   CREATE runbook stubs in specs/[feature]/runbooks/:
     - runbooks/latency.md
     - runbooks/errors.md
     - runbooks/slo-budget.md
     - runbooks/database.md

   LOG: "Defined {N} alerts, created {N} runbook stubs"
   ```

4. **Scalability Analysis**:
   ```text
   FOR EACH component (API, Database, Cache, Queue, Storage):
     ANALYZE:
       - Current capacity
       - Projected need (6 months)
       - Projected need (12 months)
       - Scaling strategy (horizontal/vertical)

     DEFINE scaling_triggers:
       - Warning threshold (e.g., CPU > 60%)
       - Scale threshold (e.g., CPU > 80%)
       - Scale action (add instance, increase size)
       - Cooldown period

     IDENTIFY bottlenecks:
       - Current limit
       - Risk level (High/Medium/Low)
       - Mitigation strategy
       - When to implement

   LOG: "Analyzed {N} components, identified {N} bottlenecks"
   ```

5. **Growth Milestones**:
   ```text
   DEFINE growth milestones with architecture triggers:
     - Launch (100 users, 10 RPS): Current architecture
     - Early Adoption (1K users, 100 RPS): Add auto-scaling
     - Growth (10K users, 1K RPS): Add replicas, CDN
     - Scale (100K users, 10K RPS): Sharding, microservices

   LOG: "Defined {N} growth milestones"
   ```

**Output**:
- plan.md "Observability & Monitoring Plan" section populated
- plan.md "Scalability Strategy" section populated
- Runbook stubs created in specs/[feature]/runbooks/
- SLIs/SLOs defined and linked to NFRs

---

### Phase 1.75: RTM Generation (NEW)

**Prerequisites**: Phase 1.5 complete, all ADRs documented

**Purpose**: Generate bidirectional traceability matrix for validation.

1. **FR Coverage Matrix**:
   ```text
   FOR EACH FR-xxx IN spec.md:
     FIND linked ADR-xxx:
       - Search ADR.Linked_Requirements for FR-xxx
       - Record all ADRs that reference this FR

     PLAN task references:
       - Placeholder TASK-xxx entries for /speckit.tasks
       - Based on FR complexity and ADR implications

     DETERMINE coverage status:
       - ✓ Covered: Has ADR and planned tasks
       - ⚠ No ADR: Has tasks but no architecture decision
       - ✗ Orphan: No ADR and no tasks

     ADD row to FR Coverage Matrix

   CALCULATE: FR Coverage = (Covered + No ADR) / Total
   TARGET: ≥90% coverage

   LOG: "FR Coverage: {covered}/{total} ({percentage}%)"
   ```

2. **NFR Coverage Matrix**:
   ```text
   FOR EACH NFR-xxx:
     FIND linked ADR-xxx
     FIND monitoring reference:
       - Dashboard panel
       - Alert definition
     DETERMINE coverage status

     ADD row to NFR Coverage Matrix

   CALCULATE: NFR Coverage percentage

   LOG: "NFR Coverage: {covered}/{total} ({percentage}%)"
   ```

3. **Gap Detection**:
   ```text
   IDENTIFY gaps:
     orphan_frs = FRs without ADR or Task plan
     orphan_adrs = ADRs without FR linkage
     missing_tests = FRs without expected test coverage
     missing_monitoring = NFRs without alert/dashboard

   FOR EACH gap:
     ADD to "Traceability Gaps" table:
       - Gap type
       - Item ID
       - Issue description
       - Recommended resolution

   LOG: "Detected {N} traceability gaps"

   IF gaps detected:
     WARN: "Traceability gaps found - review before proceeding"
   ```

4. **Impact Analysis**:
   ```text
   GENERATE impact analysis matrix:

   FOR EACH FR-xxx:
     DETERMINE downstream impacts:
       - Which ADRs would need revision if FR changes
       - Which tasks would be affected
       - Which tests would need updates

   FOR EACH NFR-xxx:
     DETERMINE downstream impacts:
       - Monitoring configurations
       - Alert thresholds
       - Scaling triggers

   POPULATE "Impact Analysis" table

   LOG: "Generated impact analysis for {N} requirements"
   ```

**Validation Gate**:

| Condition | Severity | Action |
|-----------|----------|--------|
| FR Coverage < 90% | HIGH | Warn and list uncovered FRs |
| Orphan FRs exist | HIGH | Recommend creating tasks or ADRs |
| Orphan ADRs exist | MEDIUM | Recommend linking to FRs |
| NFR without monitoring | MEDIUM | Recommend adding alerts |

**Output**:
- plan.md "Requirements Traceability Matrix" section populated
- FR Coverage percentage calculated
- NFR Coverage percentage calculated
- Gaps identified for resolution
- Impact analysis generated

---

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
| SR-PLAN-14 | Strategic Narrative Present | "Strategic Narrative" section exists with MVP scope | HIGH |
| SR-PLAN-15 | Pre-Mortem Coverage | At least 3 failure scenarios documented | HIGH |
| SR-PLAN-16 | Pre-Mortem Categories | Technical + Integration categories covered | MEDIUM |
| SR-PLAN-17 | NFR Performance Defined | At least 1 NFR-PERF-xxx with P95/P99 targets | CRITICAL |
| SR-PLAN-18 | NFR Reliability Defined | Availability target with justification | HIGH |
| SR-PLAN-19 | RTM FR Coverage | FR Coverage ≥ 90% | CRITICAL |
| SR-PLAN-20 | RTM No Orphans | No orphan FRs or ADRs | HIGH |
| SR-PLAN-21 | Brainstorm-Curate Applied | All non-trivial ADRs have scoring matrix | HIGH |
| SR-PLAN-22 | Brainstorm-Curate Visible | Scoring matrix visible (not in collapsed section) | MEDIUM |
| SR-PLAN-23 | SLI/SLO Defined | At least 2 SLIs with corresponding SLOs | HIGH |
| SR-PLAN-24 | Alerts Have Runbooks | Every ALERT-xxx has runbook link | MEDIUM |
| SR-PLAN-25 | Scalability Baseline | Capacity baseline table populated | MEDIUM |
| SR-PLAN-26 | Scaling Triggers Defined | At least 2 scaling triggers defined | MEDIUM |
| SR-PLAN-27 | Kill Criteria Present | At least 1 kill criterion in Pre-Mortem | HIGH |

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
