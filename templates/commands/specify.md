---
description: Create or update the feature specification from a natural language feature description. Supports both standalone features and concept-derived specifications with full traceability.
persona: product-agent
handoff:
  generates: handoffs/specify-to-plan.md
  template: templates/handoff-template.md
handoffs:
  - label: Build Technical Plan
    agent: speckit.plan
    prompt: Create a plan for the spec. I am building with...
    auto: true
    condition:
      - "spec.md created and valid"
      - "No unresolved [NEEDS CLARIFICATION] markers"
    pre_handoff_action:
      name: "Spec Validation"
      invoke: speckit.analyze
      args: "--quiet"  # Profile auto-detected from caller context
      skip_flag: "--skip-validate"
      timeout: 30s
      gates:
        - name: "Constitution Alignment Gate"
          pass: D
          threshold: 0
          severity: CRITICAL
          block_if: "constitution violations > 0"
          message: "Spec violates project constitution. Resolve before planning."
        - name: "Ambiguity Gate"
          pass: B
          threshold: 5
          severity: HIGH
          block_if: "ambiguity count > 5"
          message: "Too many ambiguities detected. Clarification required."
      on_failure:
        auto_remediate: speckit.clarify
        inject_context: "extracted_questions_from_validation"
    gates:
      - name: "Spec Quality Gate"
        check: "All checklist items in checklists/requirements.md pass"
        block_if: "Incomplete checklist items > 0"
        message: "Resolve incomplete checklist items before proceeding to planning"
    post_actions:
      - "log: Specification complete, transitioning to planning phase"
  - label: Clarify Spec Requirements
    agent: speckit.clarify
    prompt: Clarify specification requirements
    auto: false
    condition:
      - "[NEEDS CLARIFICATION] markers exist in spec.md"
  - label: Run Traceability Analysis
    agent: speckit.analyze
    prompt: Validate spec completeness and traceability
    auto: false
scripts:
  sh: scripts/bash/create-new-feature.sh --json "{ARGS}"
  ps: scripts/powershell/create-new-feature.ps1 -Json "{ARGS}"
skills:
  - name: ux-audit
    trigger: "Before finalizing spec when UXQ domain is active"
    usage: "Read templates/skills/ux-audit.md to validate specification against UXQ principles"
  - name: code-explore
    trigger: "Brownfield mode - understanding existing codebase"
    usage: "Read templates/skills/code-explore.md to document current behaviors before specification"
claude_code:
  model: opus
  reasoning_mode: extended
  thinking_budget: 16000
  cache_control:
    system_prompt: ephemeral
    constitution: ephemeral
    templates: ephemeral
    ttl: session
  semantic_cache:
    enabled: true
    encoder: all-MiniLM-L6-v2
    similarity_threshold: 0.95
    cache_scope: session
    cacheable_fields: [user_input, feature_description]
    ttl: 3600
  cache_hierarchy: full
  orchestration:
    max_parallel: 3
    conflict_resolution: queue
    timeout_per_agent: 300000
    retry_on_failure: 1
    role_isolation: true
    wave_overlap:
      enabled: true
      threshold: 0.80
  subagents:
    # Wave 1: Context Gathering (parallel)
    - role: brownfield-detector
      role_group: ANALYSIS
      parallel: true
      depends_on: []
      priority: 10
      model_override: haiku
      prompt: |
        Detect brownfield mode for this specification.

        Read `templates/shared/core/brownfield-detection.md` and apply the confidence-weighted detection algorithm.

        Check for:
        - Existing baseline.md in specs/
        - Existing codebase patterns
        - User input signals for modification vs new feature

        Output:
        - BROWNFIELD_MODE: true/false
        - BROWNFIELD_CONFIDENCE: 0-100%
        - Baseline file exists: yes/no
        - Suggested Change Type if brownfield

    - role: workspace-analyzer
      role_group: ANALYSIS
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Detect workspace mode for cross-repository specification.

        Read `templates/shared/core/workspace-detection.md` and apply the detection algorithm.

        Check for:
        - .speckit-workspace file in parent directories
        - Multi-repo configuration
        - Repository aliases and relationships

        Output:
        - WORKSPACE_MODE: true/false
        - WORKSPACE_CONTEXT: {current_repo, available_repos} if applicable
        - Cross-repo dependency patterns detected

    - role: concept-loader
      role_group: ANALYSIS
      parallel: true
      depends_on: []
      priority: 10
      model_override: haiku
      prompt: |
        Load concept context for specification.

        Check for `specs/concept.md` in repository root:
        - If exists: Parse Feature Hierarchy, extract matching Concept IDs
        - Calculate Concept Quality Score (CQS)
        - Extract: Vision context, related User Journeys, Dependencies

        Output:
        - CONCEPT_EXISTS: true/false
        - CONCEPT_IDS: matched IDs or "N/A"
        - CQS_SCORE: 0-100 (if concept exists)
        - Priority levels to use (P1a/P1b vs P1/P2/P3)

    # Wave 2: Analysis (depends on context gathering)
    - role: requirement-extractor
      role_group: ANALYSIS
      parallel: true
      depends_on: [brownfield-detector, workspace-analyzer]
      priority: 20
      model_override: opus
      prompt: |
        Extract and structure requirements from user input and gathered context.

        Using BROWNFIELD_MODE and WORKSPACE_MODE context:
        1. Parse user description for key concepts (actors, actions, data, constraints)
        2. Generate concise short name (2-4 words) for branch
        3. Determine complexity tier using complexity-scoring.md
        4. Apply semantic detection for intent and feature name

        If BROWNFIELD_MODE = true:
        - Extract current limitations (CL-xxx)
        - Infer change deltas (CHG-xxx)
        - Identify preserved behaviors (PB-xxx)

        Output:
        - SHORT_NAME: feature branch name
        - COMPLEXITY_TIER: TRIVIAL/SIMPLE/MODERATE/COMPLEX
        - DETECTED_INTENT: feature intent summary
        - Key actors and actions identified
        - Brownfield change analysis (if applicable)

    - role: acceptance-criteria-generator
      role_group: ANALYSIS
      parallel: true
      depends_on: [concept-loader]
      priority: 20
      model_override: sonnet
      prompt: |
        Generate acceptance scenarios using RaT (Refine-and-Thought) prompting.

        Load `templates/shared/quality/edge-case-heuristics.md` for entity-type detection.

        Using CONCEPT_IDS and concept context:

        ## STEP 1: REFINE the User Story

        Filter ambiguous language and redundant information:
        - Replace vague terms ("fast", "secure", "user-friendly") with measurable criteria
        - Remove hedge phrases ("might", "may", "could possibly")
        - Clarify actors (who exactly is performing the action?)
        - Resolve pronouns ("it", "they") to specific entities

        ## STEP 2: THINK through Complete User Journey

        For each user story, systematically consider ALL path types:

        | Classification | What to Consider | Example |
        |----------------|------------------|---------|
        | HAPPY_PATH | Primary success flow, expected journey | User submits valid form → success |
        | ALT_PATH | Alternate valid paths to same outcome | User uses social login instead |
        | ERROR_PATH | Network failures, validation errors, auth failures | Invalid email → error message |
        | BOUNDARY | Min/max values, empty states, edge quantities | Zero items, max 100 chars |
        | SECURITY | Auth bypass, injection, privilege escalation | SQL in username field |

        ## STEP 3: EXTRACT Domain Entities

        Identify entities from the user story and detect their types:

        ```text
        Apply DETECT_ENTITY_TYPE(field_name, context) from edge-case-heuristics.md:
        - email fields → "email" type
        - phone/tel/mobile → "phone" type
        - date/time/timestamp → "date" type
        - amount/price/quantity → "numeric" type
        - password/secret/pin → "password" type
        - file/upload/attachment → "file" type
        - Other text fields → "string" type
        ```

        Mark critical entities (core to the feature's value proposition).

        ## STEP 4: GENERATE Acceptance Scenarios

        Create scenarios with classification in table format:

        | ID | Classification | Given | When | Then | Requires Test |
        |----|----------------|-------|------|------|---------------|
        | AS-1A | HAPPY_PATH | [specific initial state] | [specific action] | [measurable outcome] | YES |
        | AS-1B | ERROR_PATH | [error-triggering state] | [same action] | [error handling] | YES |
        | AS-1C | BOUNDARY | [edge value state] | [action with boundary] | [boundary handling] | YES |

        Rules:
        - Each user story needs at minimum: 1 HAPPY_PATH, 1 ERROR_PATH
        - P1/P1a stories also need: 1 BOUNDARY scenario
        - Security-related stories need: 1 SECURITY scenario

        ## STEP 5: SCORE Completeness

        Calculate scenario completeness score (0.0 - 1.0):

        ```text
        completeness_score = (
          (has_happy_path ? 0.30 : 0) +
          (has_error_path ? 0.25 : 0) +
          (has_boundary ? 0.20 : 0) +
          (has_security IF security_trigger ELSE 0.15 : 0) +
          (all_critical_entities_covered ? 0.10 : 0)
        )
        ```

        **Threshold**: completeness_score >= 0.80 for PASS

        ## OUTPUT

        ```yaml
        refined_stories:
          - id: "Story 1"
            original: "[original story text]"
            refined: "[clarified story without ambiguity]"
            actors_clarified: ["user", "system"]

        entities_detected:
          - name: "email"
            type: "email"
            critical: true
          - name: "amount"
            type: "numeric"
            critical: true

        scenarios:
          - id: "AS-1A"
            classification: "HAPPY_PATH"
            given: "[specific initial state]"
            when: "[specific action]"
            then: "[measurable outcome with criteria]"
            requires_test: true
            linked_fr: "FR-001"
            reasoning: "[why this scenario is essential]"

        completeness:
          score: 0.85
          gaps_identified:
            - "[any missing coverage areas]"
          coverage_by_type:
            HAPPY_PATH: 3
            ERROR_PATH: 2
            BOUNDARY: 1
            SECURITY: 0

        priority_mapping:
          "Story 1": "P1a"
          "Story 2": "P1b"
        ```

    - role: edge-case-detector
      role_group: ANALYSIS
      parallel: true
      depends_on: [acceptance-criteria-generator]
      priority: 25
      model_override: sonnet
      prompt: |
        Systematically discover edge cases using heuristics and security patterns.

        Load and apply:
        - `templates/shared/quality/edge-case-heuristics.md`
        - `templates/shared/quality/security-patterns.md`

        ## INPUT (from acceptance-criteria-generator)

        - entities_detected: list of {name, type, critical}
        - scenarios: existing acceptance scenarios
        - functional_requirements: FR-xxx list from requirement-extractor

        ## STEP 1: Entity-Type Heuristics

        For each detected entity, generate type-specific edge cases:

        ```text
        FOR entity IN entities_detected:
          type = entity.type  # email, phone, date, numeric, string, password, file

          LOAD EDGE_CASES_BY_TYPE[type] from edge-case-heuristics.md

          FOR case IN type_edge_cases:
            # Include HIGH+ severity always, MEDIUM+ for critical entities
            IF case.severity IN ["CRITICAL", "HIGH"] OR entity.critical:
              ADD EdgeCase(
                id: "EC-{NNN}",
                condition: SUBSTITUTE(case.condition, entity.name),
                expected_behavior: case.expected_behavior,
                severity: case.severity,
                category: "validation",
                entity_source: entity.name,
                confidence: 0.90
              )
        ```

        ## STEP 2: Security Pattern Matching

        Scan functional requirements for security triggers:

        ```text
        requirements_text = JOIN(functional_requirements)

        triggers = DETECT_SECURITY_TRIGGERS(requirements_text)
        # Returns: [{category: "auth", keyword: "login", edge_cases: [...]}]

        FOR trigger IN triggers:
          FOR ec IN trigger.edge_cases:
            ADD EdgeCase(
              id: ec.id,  # e.g., EC-SEC-AUTH-001
              condition: ec.condition,
              expected_behavior: ec.expected_behavior,
              severity: "CRITICAL",  # All security EC are CRITICAL
              category: "security",
              owasp_ref: trigger.owasp_ref,
              confidence: 0.95
            )
        ```

        Security trigger categories:
        - **auth**: login, password, token, session, jwt, oauth
        - **input**: form, search, query, filter, user input
        - **access**: permission, role, admin, authorize
        - **file**: upload, attachment, import
        - **api**: endpoint, rate limit, webhook

        ## STEP 3: LLM Gap Analysis

        For complex scenarios not covered by heuristics:

        ```text
        ANALYZE for additional edge cases in:
        - Concurrency: race conditions, parallel access, deadlocks
        - Integration: external API failures, timeout, version mismatch
        - State machine: invalid transitions, orphaned states
        - Performance: large data sets, slow operations
        ```

        Generate with lower confidence (0.60-0.75) for LLM-discovered cases.

        ## STEP 4: Deduplicate and Rank

        ```text
        edge_cases = DEDUPLICATE_BY_CONDITION(all_edge_cases)
        edge_cases = SORT_BY_SEVERITY_DESC(edge_cases)
        ```

        ## OUTPUT

        Enhanced Edge Cases table for spec.md:

        | ID | Condition | Expected Behavior | Severity | Category |
        |----|-----------|-------------------|----------|----------|
        | EC-001 | email: Invalid format (missing @) | Return validation error | HIGH | validation |
        | EC-002 | SQL injection in search field | Sanitize, use parameterized query | CRITICAL | security |
        | EC-003 | amount: Negative value | Return validation error | HIGH | validation |

        Coverage summary:

        ```yaml
        edge_case_coverage:
          total_count: 23
          by_category:
            validation: 12
            security: 8
            boundary: 2
            concurrency: 1
          by_severity:
            CRITICAL: 8
            HIGH: 10
            MEDIUM: 5
          entity_types_covered: [email, numeric, password]
          security_triggers_detected: [auth, input]
          heuristic_count: 15
          security_count: 8
          llm_generated_count: 0
          confidence_avg: 0.91

        gaps_remaining:
          - "[any uncovered areas]"
        ```

    - role: completeness-checker
      role_group: ANALYSIS
      parallel: true
      depends_on: [edge-case-detector]
      priority: 27
      model_override: sonnet
      prompt: |
        Validate specification completeness across multiple dimensions.

        Load and apply: `templates/shared/quality/completeness-checklist.md`

        ## INPUT (from previous stages)

        - functional_requirements: FR-xxx list from requirement-extractor
        - acceptance_scenarios: AS-xxx list from acceptance-criteria-generator
        - edge_cases: EC-xxx list from edge-case-detector
        - has_ui: boolean (detected from requirements)

        ## STEP 1: Error Handling Check

        ```text
        happy_paths = FILTER(acceptance_scenarios, s => "error" NOT IN s.then.lower())
        error_paths = FILTER(acceptance_scenarios, s => "error" IN s.then.lower())

        # Heuristic: Minimum 1 error scenario per 2 happy paths
        expected_error_count = CEIL(happy_paths.length / 2)

        IF error_paths.length < expected_error_count:
          ADD Gap(category: "ERROR_HANDLING", severity: "HIGH")

        # Check for specific error types
        CRITICAL_ERROR_TYPES = ["network", "validation", "auth", "rate_limit", "database"]
        FOR type IN CRITICAL_ERROR_TYPES:
          IF FEATURE_REQUIRES_TYPE(requirements, type) AND NOT HAS_ERROR_SCENARIO(error_paths, type):
            ADD Gap(category: "ERROR_HANDLING", missing: "{type} error", severity: "MEDIUM")
        ```

        ## STEP 2: Security Completeness Check

        ```text
        SECURITY_DIMENSIONS = {
          "authentication": ["login", "auth", "password", "token"],
          "authorization": ["permission", "role", "access", "admin"],
          "input_validation": ["input", "form", "field", "search", "query"],
          "data_protection": ["encrypt", "sensitive", "personal", "pii"],
          "session_management": ["session", "cookie", "logout"]
        }

        FOR dimension, keywords IN SECURITY_DIMENSIONS:
          IF ANY(keyword IN requirements_text FOR keyword IN keywords):
            IF NOT HAS_SECURITY_REQUIREMENT(spec, dimension):
              ADD Gap(
                category: "SECURITY",
                missing: "{dimension} security requirement",
                severity: "CRITICAL",
                owasp: "A01-A10 reference"
              )
        ```

        ## STEP 3: Performance Check

        ```text
        PERFORMANCE_TRIGGERS = {
          "api_latency": ["api", "endpoint", "request", "response"],
          "throughput": ["batch", "bulk", "import", "process"],
          "page_load": ["page", "load", "render"],
          "search": ["search", "filter", "query"]
        }

        FOR trigger, keywords IN PERFORMANCE_TRIGGERS:
          IF ANY(keyword IN requirements_text FOR keyword IN keywords):
            IF NOT HAS_PERFORMANCE_METRIC(spec):
              ADD Gap(
                category: "PERFORMANCE",
                missing: "{trigger} performance requirement",
                severity: "HIGH"
              )
        ```

        ## STEP 4: Observability Check

        ```text
        is_critical_feature = ANY(
          trigger IN requirements_text FOR trigger IN
          ["auth", "payment", "admin", "permission", "security"]
        )

        has_observability = ANY(
          keyword IN requirements_text FOR keyword IN
          ["log", "metric", "monitor", "alert", "trace", "audit"]
        )

        IF is_critical_feature AND NOT has_observability:
          ADD Gap(
            category: "OBSERVABILITY",
            missing: "No observability requirements",
            severity: "MEDIUM"
          )
        ```

        ## STEP 5: Accessibility Check (UI features only)

        ```text
        IF has_ui:
          has_accessibility = HAS_SECTION(spec, "Accessibility") OR
                             ANY("wcag" IN text.lower() OR "a11y" IN text.lower())

          IF NOT has_accessibility:
            ADD Gap(
              category: "ACCESSIBILITY",
              missing: "No WCAG compliance requirements",
              severity: "HIGH"
            )
        ```

        ## STEP 6: Prerequisites Check

        ```text
        DEPENDENCY_PATTERNS = {
          "authentication": ["authenticated user", "logged in", "current user"],
          "database": ["store", "save", "retrieve"],
          "api_client": ["external api", "third-party", "integration"]
        }

        FOR dep_type, keywords IN DEPENDENCY_PATTERNS:
          IF ANY(keyword IN requirements_text FOR keyword IN keywords):
            IF NOT HAS_SECTION(spec, "Technical Dependencies"):
              ADD Gap(
                category: "PREREQUISITES",
                missing: "{dep_type} prerequisite not documented",
                severity: "HIGH"
              )
        ```

        ## STEP 7: LLM Gap Analysis

        ```text
        PROMPT: "What's missing from this specification that would cause
                implementation failures?"

        Consider:
        - Error handling gaps not caught by heuristics
        - Subtle security vulnerabilities
        - Performance bottlenecks
        - Cross-cutting concerns
        - Integration edge cases
        ```

        ## STEP 8: Calculate Completeness Score

        ```text
        CATEGORY_WEIGHTS = {
          ERROR_HANDLING: 0.20,
          PERFORMANCE: 0.15,
          SECURITY: 0.20,
          OBSERVABILITY: 0.10,
          ACCESSIBILITY: 0.10,
          PREREQUISITES: 0.15,
          EDGE_CASES: 0.10
        }

        FOR category IN CATEGORIES:
          category_gaps = FILTER(all_gaps, g => g.category == category)
          IF category_gaps.length == 0:
            category_scores[category] = 1.0
          ELSE:
            deductions = SUM(severity_penalty FOR gap IN category_gaps)
            category_scores[category] = MAX(0.0, 1.0 - deductions)

        completeness_score = WEIGHTED_SUM(category_scores, CATEGORY_WEIGHTS)
        ```

        ## OUTPUT

        Completeness Analysis section for spec.md:

        ```markdown
        ### Completeness Analysis

        | Category | Status | Details |
        |----------|--------|---------|
        | Error Handling | ✅/⚠️/❌ | X error scenarios for Y happy paths |
        | Security | ✅/⚠️/❌ | Auth/Input/Data coverage status |
        | Performance | ✅/⚠️/❌ | Latency/throughput requirements |
        | Observability | ✅/⚠️/❌ | Logging/metrics defined |
        | Accessibility | ✅/⚠️/❌ | WCAG compliance (if UI) |
        | Prerequisites | ✅/⚠️/❌ | Dependencies documented |

        **Completeness Score**: X.XX / 1.00
        ```

        Gaps list for remediation:

        ```yaml
        completeness_result:
          score: 0.XX
          status: "PASS|FAIL"  # >= 0.75 is PASS
          category_scores:
            error_handling: 0.XX
            security: 0.XX
            # ...
          gaps:
            - category: "SECURITY"
              missing_aspect: "input validation requirement"
              severity: "CRITICAL"
              suggested_requirement: "Add input sanitization for search field"
        ```

    # Wave 3: Specification Writing (depends on analysis)
    - role: spec-writer
      role_group: DOCS
      parallel: true
      depends_on: [requirement-extractor, acceptance-criteria-generator, edge-case-detector, completeness-checker]
      priority: 30
      model_override: opus
      prompt: |
        Write the complete feature specification.

        Using all gathered context (brownfield, workspace, concept, requirements, acceptance criteria):

        1. Run create-new-feature script to set up branch and spec file
        2. Load templates/spec-template.md for required sections
        3. Fill all sections with concrete details:
           - Overview and Feature Description
           - User Stories with priorities and concept references
           - Functional Requirements (FR-xxx) with AS links
           - Acceptance Scenarios (AS-xxx) in table format
           - Success Criteria (SC-xxx) - measurable and tech-agnostic
           - Edge Cases (EC-xxx)
           - Traceability Summary table

        If WORKSPACE_MODE = true:
           - Add Cross-Repository Dependencies section

        If BROWNFIELD_MODE = true:
           - Add Change Specification section with deltas

        Apply quality filters:
        - Anti-slop scan (no forbidden phrases)
        - Reader testing (comprehension check)
        - Max 3 [NEEDS CLARIFICATION] markers

        Output:
        - Complete spec.md written to FEATURE_DIR
        - Checklists/requirements.md created
        - Concept traceability updated (if concept exists)

    # Wave 3.5: Quality Scoring (depends on spec writing)
    - role: spec-quality-scorer
      role_group: QUALITY
      parallel: false
      depends_on: [spec-writer, completeness-checker]
      priority: 35
      model_override: sonnet
      prompt: |
        Score specification quality using G-Eval framework.

        Load and apply: `templates/shared/quality/spec-quality-scorer.md`

        ## STEP 1: Evaluate Clarity (25%)
        - Import ambiguity detection from ambiguity-patterns.md
        - Count ambiguities by severity (CRITICAL, HIGH, MEDIUM)
        - Run LLM G-Eval clarity rubric (1-5 scale)
        - Combine: 60% automated + 40% LLM

        ## STEP 2: Evaluate Completeness (25%)
        - Use completeness-checker results (gaps by severity)
        - Apply severity-weighted gap penalty
        - Run LLM G-Eval completeness rubric
        - Combine: 60% automated + 40% LLM

        ## STEP 3: Evaluate Testability (20%)
        - Calculate testable scenario ratio (has measurable criteria)
        - Calculate FR→AS traceability ratio
        - Run LLM G-Eval testability rubric
        - Combine: 60% automated + 40% LLM

        ## STEP 4: Evaluate Consistency (15%)
        - Run LLM contradiction detection
        - Check for logical/semantic/constraint/behavioral/temporal conflicts
        - Calculate penalty from contradiction count and severity
        - Combine LLM score with penalty

        ## STEP 5: Evaluate Traceability (15%)
        - Calculate FR→AS coverage percentage
        - Calculate FR→EC coverage percentage
        - Identify orphan requirements
        - Run LLM G-Eval traceability rubric
        - Combine: 70% automated + 30% LLM

        ## STEP 6: Calculate Overall Score
        - Weighted sum: Clarity×0.25 + Completeness×0.25 + Testability×0.20 + Consistency×0.15 + Traceability×0.15
        - Scale to 0-100
        - Assign grade: A (90+), B (80-89), C (70-79), D (60-69), F (<60)
        - Generate recommendation based on grade and lowest dimensions

        ## STEP 7: Validate Quality Gates
        - SR-SPEC-19: Overall score >= 70 (Grade C+)
        - SR-SPEC-20: All dimensions >= 0.50
        - SR-SPEC-21: No CRITICAL contradictions

        ## OUTPUT FORMAT
        Add "Specification Quality Score" section to spec.md:

        ```markdown
        ### Specification Quality Score

        **Overall Score**: XX.X / 100 (Grade: X)
        **Status**: ✅ PASSED | ❌ FAILED
        **Recommendation**: [Generated recommendation]

        | Dimension | Score | Weight | Explanation |
        |-----------|-------|--------|-------------|
        | Clarity | X.XX | 25% | Ambiguities: N (X critical). LLM: X.XX |
        | Completeness | X.XX | 25% | N gaps (X critical, Y high) |
        | Testability | X.XX | 20% | Testable: X%, FR→AS: Y% |
        | Consistency | X.XX | 15% | N contradictions (X critical) |
        | Traceability | X.XX | 15% | FR→AS: X%, FR→EC: Y%, Orphans: N |

        **Improvement Suggestions**:
        1. [Highest priority suggestion]
        2. [Second suggestion]
        3. [Third suggestion]
        ```

        Return quality score result for validation gates.

    # Wave 4: Validation (depends on spec writing and quality scoring)
    - role: spec-validator
      role_group: VALIDATION
      parallel: true
      depends_on: [spec-writer, spec-quality-scorer]
      priority: 40
      model_override: sonnet
      prompt: |
        Validate specification quality and completeness.

        Read the generated spec.md and perform:

        1. Self-Review Phase:
           - Check all SR-SPEC-01 to SR-SPEC-10 criteria
           - Apply UXQ criteria if domain is active
           - Apply Workspace criteria if WORKSPACE_MODE = true

        2. Quality Validation:
           - Verify no implementation details
           - Confirm all FRs have linked ASs
           - Validate Success Criteria are measurable and tech-agnostic
           - Check edge cases are defined

        3. Checklist Validation:
           - Update checklists/requirements.md with pass/fail status
           - Document any remaining issues

        4. Self-Correction (up to 3 iterations if needed):
           - Fix CRITICAL and HIGH issues
           - Re-validate until PASS or max iterations

        Output:
        - Self-Review Report with verdict (PASS/WARN/FAIL)
        - Updated checklist with validation status
        - Traceability summary (FRs, ASs, ECs counts)
        - Readiness for /speckit.plan handoff
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Prefetch Phase [REF:PF-001]

**Speculative parallel load** of all potentially-needed files BEFORE any conditional logic:

```text
# PREFETCH BATCH (single message, all Read calls in parallel)
Read IN PARALLEL:
- `memory/constitution.md`
- `templates/spec-template.md`
- `templates/shared/core/language-loading.md`
- `templates/shared/complexity-scoring.md`
- `templates/shared/core/brownfield-detection.md`
- `templates/shared/core/workspace-detection.md`

# CONDITIONAL PREFETCH (add to batch if files exist)
IF exists("specs/concept.md") → include in parallel batch
IF exists("memory/baseline.md") OR exists("specs/baseline.md") → include in parallel batch

CACHE all results with session lifetime.
REPORT: "Prefetched {N} files in {T}ms"
```

**Why prefetch?** Loading 6-8 files in parallel (300ms) vs sequential (2-3s) saves 2+ seconds per command invocation.

---

## Brownfield Detection

Read `templates/shared/core/brownfield-detection.md` and apply the confidence-weighted detection algorithm.

```text
DETECTION_INPUT:
  user_input = $ARGUMENTS
  cwd = current working directory

EXECUTE brownfield-detection.md algorithm → BROWNFIELD_MODE, BROWNFIELD_CONFIDENCE

REPORT: "Brownfield mode: {BROWNFIELD_MODE} (confidence: {BROWNFIELD_CONFIDENCE}%)"
```

**When BROWNFIELD_MODE = true**:

1. If baseline.md exists, parse it to auto-populate:

---

## Workspace Detection

Read `templates/shared/core/workspace-detection.md` and apply the confidence-weighted detection algorithm.

```text
EXECUTE workspace-detection.md algorithm → WORKSPACE_MODE, WORKSPACE_CONTEXT

IF WORKSPACE_MODE = true:
  CURRENT_REPO_ALIAS = WORKSPACE_CONTEXT.current_repo
  AVAILABLE_REPOS = WORKSPACE_CONTEXT.repos
  Include "Cross-Repository Dependencies" section
  Use format: `repo-alias:feature-id` for cross-repo references

ELSE:
  Skip "Cross-Repository Dependencies" section
  All feature references are local
```

---

**When BROWNFIELD_MODE = true**:
   - Current State Analysis (CB-xxx entries from baseline components)
   - Current Limitations (infer from user description)
   - Initial Change Delta (infer ADD/MODIFY/REMOVE from user intent)

2. If baseline.md does NOT exist, suggest:
   ```text
   💡 Brownfield project detected. Consider running `/speckit.baseline` first
   to capture current system state for better change traceability.

   Proceed without baseline? (Y/N)
   ```

3. Generate appropriate Change Type from user input:
   - "add feature" → Enhancement
   - "refactor" → Refactor
   - "migrate from X to Y" → Migration
   - "fix bug" → Bugfix
   - "optimize", "performance" → Performance
   - "security", "vulnerability" → Security

---

## Concept Integration

**Check for existing concept document**:

1. Look for `specs/concept.md` in the repository root
2. If concept.md exists:
   - Parse the Feature Hierarchy section to find matching Concept IDs
   - The user input may reference Concept IDs directly (e.g., "EPIC-001.F01.S01")
   - Or the user may describe a feature that matches stories in the concept
   - Extract: Vision context, related User Journeys, Dependencies
   - Set `CONCEPT_REFERENCE` to the matched Concept ID(s)
   - Use the concept's priority levels (P1a, P1b) for User Story prioritization

3. If concept.md does NOT exist:
   - Proceed with standalone specification
   - Set `CONCEPT_REFERENCE` to "N/A"
   - Use simple priorities (P1, P2, P3) or sub-priorities as needed

### Concept Quality Gate (CQS Check)

**If concept.md exists, validate Concept Quality Score before specification**:

```text
# Calculate CQS from concept.md sections (see templates/shared/concept-sections/cqs-score.md)
CQS = calculate_concept_quality_score(concept.md)

# Quality Gate Decision
IF CQS >= 80:
  INFO: "✅ CQS {CQS}/100 — Concept fully validated. Proceeding with specification."
  PROCEED with specification

ELSE IF CQS >= 60:
  WARN: "⚠️ CQS {CQS}/100 — Concept has gaps. Proceed with caution."
  WARN: "Missing components: [list components with score < 60]"
  ASK: "Proceed with specification? Gaps will be flagged in the spec. (Y/N)"
  IF user confirms:
    PROCEED with specification
    FLAG: Add "[CQS GAP]" markers for features lacking validation

ELSE IF CQS < 60:
  ERROR: "⛔ CQS {CQS}/100 — Concept not ready for specification."
  ERROR: "Critical gaps: [list components with score < 40]"
  SUGGEST: "Run `/speckit.concept` to complete discovery before specification."
  ASK: "Override and proceed anyway? (Not recommended) (Y/N)"
  IF user explicitly overrides:
    WARN: "Proceeding without validated concept. High risk of rework."
    PROCEED with specification
  ELSE:
    STOP and recommend `/speckit.concept`
```

**CQS Component Reference**:
| Component | Weight | Low Score Indicators |
|-----------|:------:|---------------------|
| Market Validation | 25% | Missing TAM/SAM/SOM, no competitive analysis |
| Persona Depth | 20% | No JTBD, missing willingness-to-pay |
| Metrics Quality | 15% | No North Star, metrics fail SMART |
| Feature Completeness | 20% | Incomplete hierarchy, no Golden Path |
| Risk Assessment | 10% | <3 risks, no pivot criteria |
| Technical Hints | 10% | No domain entities, no integration assessment |

**Reference**: `templates/shared/concept-sections/cqs-score.md`

**Concept ID Matching Logic**:

```text
IF user input contains pattern "EPIC-\d+\.F\d+\.S\d+":
  CONCEPT_IDS = extract all matching IDs
  Validate each ID exists in concept.md
ELSE:
  Search concept.md Feature Hierarchy for:
    - Story descriptions that match user input keywords
    - Feature names that match user input
  CONCEPT_IDS = matched story IDs (or "N/A" if no match)
```

## Incomplete Feature Check

Before creating a new feature, check for incomplete work in the feature manifest:

```text
MANIFEST_FILE = specs/features/.manifest.md

IF exists(MANIFEST_FILE):
  Parse manifest table
  Find features with status NOT IN [MERGED, ABANDONED]

  IF incomplete_features.count > 0:
    Display warning:

    ⚠️ **Incomplete Features Detected**

    | ID | Name | Status | Last Updated |
    |----|------|--------|--------------|
    | [list each incomplete feature] |

    **Options**:
    1. **Resume existing**: Run `/speckit.switch <ID>` to continue working on an existing feature
    2. **Start new anyway**: Confirm to proceed with creating a new feature
    3. **Abandon old**: Mark incomplete features as ABANDONED first

    **Note**: Proceeding will create a new feature. Incomplete feature(s) above
    will remain accessible via `/speckit.switch`.

    ASK user: "Do you want to proceed with creating a new feature? (yes/no)"

    IF user confirms:
      CONTINUE to branch creation
    ELSE:
      EXIT with suggestion to use /speckit.switch

ELSE:
  # No manifest exists - this is the first feature
  CONTINUE to branch creation
```

---

## Extension Detection

**Detect if user intent suggests extending an existing feature**:

```text
MERGED_FEATURES = get features from manifest where Status = MERGED

IF MERGED_FEATURES.count > 0:
  Analyze user input for extension patterns:

  PATTERN_KEYWORDS = ["add to", "extend", "enhance", "improve", "update", "modify",
                      "fix in", "change", "refactor", "upgrade", "add feature to"]

  FEATURE_REFERENCES = look for:
    - Direct feature IDs: "001", "feature 001", "#001"
    - Feature names: "login", "auth", "payment"
    - System spec references: "login system", "auth module"

  IF user input matches PATTERN_KEYWORDS AND references existing feature:
    EXTENSION_CANDIDATE = find matching merged feature

    Display suggestion:

    💡 **Extension Opportunity Detected**

    Your description suggests modifying the **{EXTENSION_CANDIDATE}** feature
    which was merged on {MERGE_DATE}.

    **Recommendation**: Use `/speckit.extend` instead to:
    - ✅ Preserve Feature Lineage (traceability)
    - ✅ Auto-load parent context
    - ✅ Track System Spec evolution correctly

    **Example**:
    ```
    /speckit.extend {EXTENSION_CANDIDATE_ID} "{USER_DESCRIPTION}"
    ```

    **Options**:
    1. **Use /speckit.extend** (Recommended) - Creates extension with lineage
    2. **Create standalone feature** - Proceed without lineage (loses traceability)

    ASK user: "Would you like to use /speckit.extend instead? (yes/no)"

    IF user says yes:
      Redirect to: /speckit.extend {EXTENSION_CANDIDATE_ID} "{USER_DESCRIPTION}"
      EXIT
    ELSE:
      CONTINUE to branch creation
      Note: Feature will not have Feature Lineage section populated
```

**Relationship Type Detection**:

```text
Based on description keywords, suggest relationship if extending:

"add", "new", "implement", "support", "enable" → EXTENDS
"improve", "enhance", "optimize", "refactor", "clean" → REFINES
"fix", "bug", "issue", "correct", "patch", "resolve" → FIXES
"replace", "remove", "deprecate", "migrate", "sunset" → DEPRECATES
```

---

## Outline

The text the user typed after `/speckit.specify` in the triggering message **is** the feature description. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that feature description, do this:

0. **Load project language and assess complexity**:

   Use **parallel loading** for initialization (see `templates/shared/core/parallel-loading.md`):

   ```text
   # PARALLEL BATCH READ (single message, multiple Read tool calls)
   Read IN PARALLEL:
   - `templates/shared/core/language-loading.md`
   - `templates/shared/complexity-scoring.md`
   - `templates/shared/semantic-detection.md`

   # Execute after all loaded
   EXECUTE language-loading.md → ARTIFACT_LANGUAGE
   EXECUTE complexity-scoring.md → COMPLEXITY_TIER, COMPLEXITY_SCORE
   EXECUTE semantic-detection.md → DETECTED_INTENT, FEATURE_NAME (apply to user input)

   REPORT: "Generating specification in {LANGUAGE_NAME} ({ARTIFACT_LANGUAGE})..."
   REPORT: "Complexity: {COMPLEXITY_TIER} ({COMPLEXITY_SCORE}/100)"
   REPORT: "Detected intent: {DETECTED_INTENT} for '{FEATURE_NAME}'"
   ```

   Adapt workflow based on COMPLEXITY_TIER (see complexity-scoring.md for tier-specific guidelines).

1. **Generate a concise short name** (2-4 words) for the branch:
   - Analyze the feature description and extract the most meaningful keywords
   - Create a 2-4 word short name that captures the essence of the feature
   - Use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug")
   - Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)
   - Keep it concise but descriptive enough to understand the feature at a glance
   - Examples:
     - "I want to add user authentication" → "user-auth"
     - "Implement OAuth2 integration for the API" → "oauth2-api-integration"
     - "Create a dashboard for analytics" → "analytics-dashboard"
     - "Fix payment processing timeout bug" → "fix-payment-timeout"

2. **Check for existing branches before creating new one**:

   a. First, fetch all remote branches to ensure we have the latest information:

      ```bash
      git fetch --all --prune
      ```

   b. Find the highest feature number across all sources for the short-name:
      - Remote branches: `git ls-remote --heads origin | grep -E 'refs/heads/[0-9]+-<short-name>$'`
      - Local branches: `git branch | grep -E '^[* ]*[0-9]+-<short-name>$'`
      - Specs directories: Check for directories matching `specs/[0-9]+-<short-name>`

   c. Determine the next available number:
      - Extract all numbers from all three sources
      - Find the highest number N
      - Use N+1 for the new branch number

   d. Run the script `{SCRIPT}` with the calculated number and short-name:
      - Pass `--number N+1` and `--short-name "your-short-name"` along with the feature description
      - Bash example: `{SCRIPT} --json --number 5 --short-name "user-auth" "Add user authentication"`
      - PowerShell example: `{SCRIPT} -Json -Number 5 -ShortName "user-auth" "Add user authentication"`

   **IMPORTANT**:
   - Check all three sources (remote branches, local branches, specs directories) to find the highest number
   - Only match branches/directories with the exact short-name pattern
   - If no existing branches/directories found with this short-name, start with number 1
   - You must only ever run this script once per feature
   - The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for
   - The JSON output will contain BRANCH_NAME and SPEC_FILE paths
   - For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot")

3. Load `templates/spec-template.md` to understand required sections.

4. Follow this execution flow:

    1. Parse user description from Input
       If empty: ERROR "No feature description provided"

    2. Extract key concepts from description
       Identify: actors, actions, data, constraints

    3. Check Concept Integration (see section above)
       - If concept.md exists: extract CONCEPT_REFERENCE and related context
       - Use concept priorities (P1a, P1b) and dependencies

    4. For unclear aspects:
       - Make informed guesses based on context and industry standards
       - Only mark with [NEEDS CLARIFICATION: specific question] if:
         - The choice significantly impacts feature scope or user experience
         - Multiple reasonable interpretations exist with different implications
         - No reasonable default exists
       - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
       - Prioritize clarifications by impact: scope > security/privacy > user experience > technical details

    5. Fill User Scenarios & Testing section with **sub-priorities**:
       - If no clear user flow: ERROR "Cannot determine user scenarios"
       - Assign priorities using sub-levels: P1a, P1b, P1c (MVP critical path), P2a, P2b (post-MVP)
       - Add **Concept Reference** per User Story linking to CONCEPT_IDS
       - Add **Independent Test** description for each story

    6. Generate **Acceptance Scenarios with IDs** in tabular format:

       **ID Format**: `AS-[story number][scenario letter]`
       - Story 1 scenarios: AS-1A, AS-1B, AS-1C
       - Story 2 scenarios: AS-2A, AS-2B
       - Edge cases: EC-001, EC-002

       **Table Structure**:
       ```markdown
       | ID | Given | When | Then |
       |----|-------|------|------|
       | AS-1A | [initial state] | [action] | [expected outcome] |
       ```

       **IMPORTANT**: These IDs will be referenced in tasks.md for traceability:
       - Test tasks will use [TEST:AS-1A] markers
       - This enables end-to-end traceability: Concept → Spec → Tasks → Tests

    7. Generate Functional Requirements with IDs (FR-001, FR-002)
       - Each requirement must be testable
       - Link each FR to relevant Acceptance Scenarios: `*Acceptance Scenarios*: AS-1A, AS-1B`
       - Use reasonable defaults for unspecified details (document assumptions)

    8. Define Success Criteria (SC-001, SC-002)
       Create measurable, technology-agnostic outcomes
       Include both quantitative metrics (time, performance, volume) and qualitative measures
       Each criterion must be verifiable without implementation details

    9. Identify Key Entities (if data involved)

    10. Generate Traceability Summary table:
        ```markdown
        | Requirement | Acceptance Scenarios | Edge Cases | Status |
        |-------------|---------------------|------------|--------|
        | FR-001 | AS-1A, AS-1B | EC-001 | Defined |
        ```

    11. **IF WORKSPACE_MODE = true**: Generate Cross-Repository Dependencies section:

        a) Identify the current repository alias from workspace config

        b) Analyze feature requirements for cross-repo dependencies:
           - API calls to other services → REQUIRES dependency
           - Shared data models or events → USES dependency
           - Feature extending another repo's capability → EXTENDS dependency
           - Feature implementing a contract from another repo → IMPLEMENTS dependency

        c) Populate "Dependencies on Other Repositories" table:
           ```markdown
           | This Feature | Depends On | Dependency Type | Reason |
           |--------------|------------|-----------------|--------|
           | {CURRENT_REPO}:{FEATURE_ID} | api:002-payment-api | REQUIRES | Needs payment processing |
           ```

        d) Identify potential reverse dependencies:
           - If this feature exposes an API, which repos might consume it?
           - If this feature publishes events, which repos might subscribe?

        e) Suggest cross-repo dependencies based on repository roles:
           - Frontend repos typically REQUIRES backend APIs
           - Mobile repos often USES same APIs as web frontend
           - Shared libraries are typically USED BY multiple consumers

        f) IF no cross-repo dependencies identified:
           - Remove the Cross-Repository Dependencies section from spec
           - Note: "No cross-repository dependencies detected"

    12. **IF BROWNFIELD_MODE = true**: Generate Change Specification section:

        a) Parse baseline.md (if exists) to extract:
           - Component inventory → CB-xxx entries
           - Current behavior descriptions
           - Code locations (file:line references)

        b) Analyze user description to infer:
           - Current Limitations (CL-xxx) from problem statements
           - Change Delta (CHG-xxx) from desired outcomes
           - Preserved Behaviors (PB-xxx) from "keep existing" / "maintain compatibility" phrases

        c) Generate Change Type from keywords:
           ```text
           IF "migrate" OR "move from" OR "upgrade" → Migration
           ELIF "refactor" OR "restructure" → Refactor
           ELIF "fix" OR "bug" OR "issue" → Bugfix
           ELIF "optimize" OR "performance" OR "speed" → Performance
           ELIF "security" OR "vulnerability" OR "CVE" → Security
           ELSE → Enhancement
           ```

        d) Map changes to requirements:
           - Link each CHG-xxx to relevant FR-xxx
           - Ensure every CL-xxx has at least one CHG-xxx addressing it

        e) IF Change Type = Migration:
           - Generate Migration Plan section
           - Suggest migration strategy based on scope
           - Create placeholder deprecation timeline

        f) Generate Rollback Criteria:
           - Add default metrics: error rate, response time
           - Suggest custom metrics based on feature type

    13. Return: SUCCESS (spec ready for planning)

5. Write the specification to SPEC_FILE using the template structure, replacing placeholders with concrete details derived from the feature description (arguments) while preserving section order and headings.

5b. **Update Concept Traceability** (if concept.md exists):

   This step ensures the concept document stays in sync with specification progress.

   ```text
   IF exists("specs/concept.md"):
     1. Read concept.md
     2. Find "Traceability Skeleton" section

     3. FOR EACH concept_id in CONCEPT_IDS:
        FIND row WHERE "Concept ID" == concept_id
        UPDATE row:
          - "Spec Created": [x]
          - "Requirements": comma-separated list of FR-xxx IDs from spec.md
          - "Status": "SPECIFIED"

     4. Update "Progress Rollup" section:
        - Decrement "Not started" count
        - Increment "SPECIFIED" count
        - Recalculate percentages

     5. Update "Foundation Progress" section (if applicable):
        FOR EACH concept_id:
          IF concept_id.wave == 1 OR wave == 2:
            Update wave progress counts

     6. Set "Last Updated" field:
        - "[date] by /speckit.specify"

     7. Write updated concept.md

   Report: "Concept traceability updated: {CONCEPT_IDS} → SPECIFIED"
   ```

   **Example update**:
   ```markdown
   ## Traceability Skeleton

   | Concept ID | Wave | Spec Created | Requirements | Tasks | Tests | Status |
   |------------|------|--------------|--------------|-------|-------|--------|
   | EPIC-001.F01.S01 | 1 | [x] | FR-001, FR-002, FR-003 | - | - | SPECIFIED |
   | EPIC-001.F01.S02 | 1 | [x] | FR-004, FR-005 | - | - | SPECIFIED |
   | EPIC-001.F02.S01 | 1 | [ ] | - | - | - | Not started |

   ### Progress Rollup

   | Status | Count | % |
   |--------|-------|---|
   | Not started | 1 | 33% |
   | SPECIFIED | 2 | 67% |
   | TASKED | 0 | 0% |
   | ...

   **Last Updated**: 2025-12-27 by /speckit.specify
   ```

6. **Specification Quality Validation**: After writing the initial spec, validate it against quality criteria:

   a. **Create Spec Quality Checklist**: Generate a checklist file at `FEATURE_DIR/checklists/requirements.md` using the checklist template structure with these validation items:

      ```markdown
      # Specification Quality Checklist: [FEATURE NAME]
      
      **Purpose**: Validate specification completeness and quality before proceeding to planning
      **Created**: [DATE]
      **Feature**: [Link to spec.md]
      
      ## Content Quality
      
      - [ ] No implementation details (languages, frameworks, APIs)
      - [ ] Focused on user value and business needs
      - [ ] Written for non-technical stakeholders
      - [ ] All mandatory sections completed
      
      ## Requirement Completeness
      
      - [ ] No [NEEDS CLARIFICATION] markers remain
      - [ ] Requirements are testable and unambiguous
      - [ ] Success criteria are measurable
      - [ ] Success criteria are technology-agnostic (no implementation details)
      - [ ] All acceptance scenarios are defined
      - [ ] Edge cases are identified
      - [ ] Scope is clearly bounded
      - [ ] Dependencies and assumptions identified
      
      ## Feature Readiness
      
      - [ ] All functional requirements have clear acceptance criteria
      - [ ] User scenarios cover primary flows
      - [ ] Feature meets measurable outcomes defined in Success Criteria
      - [ ] No implementation details leak into specification
      
      ## Notes
      
      - Items marked incomplete require spec updates before `/speckit.clarify` or `/speckit.plan`
      ```

   b. **Run Validation Check**: Review the spec against each checklist item:
      - For each item, determine if it passes or fails
      - Document specific issues found (quote relevant spec sections)

   c. **Handle Validation Results**:

      - **If all items pass**: Mark checklist complete and proceed to step 6

      - **If items fail (excluding [NEEDS CLARIFICATION])**:
        1. List the failing items and specific issues
        2. Update the spec to address each issue
        3. Re-run validation until all items pass (max 3 iterations)
        4. If still failing after 3 iterations, document remaining issues in checklist notes and warn user

      - **If [NEEDS CLARIFICATION] markers remain**:
        1. Extract all [NEEDS CLARIFICATION: ...] markers from the spec
        2. **LIMIT CHECK**: If more than 3 markers exist, keep only the 3 most critical (by scope/security/UX impact) and make informed guesses for the rest
        3. For each clarification needed (max 3), present options to user in this format:

           ```markdown
           ## Question [N]: [Topic]
           
           **Context**: [Quote relevant spec section]
           
           **What we need to know**: [Specific question from NEEDS CLARIFICATION marker]
           
           **Suggested Answers**:
           
           | Option | Answer | Implications |
           |--------|--------|--------------|
           | A      | [First suggested answer] | [What this means for the feature] |
           | B      | [Second suggested answer] | [What this means for the feature] |
           | C      | [Third suggested answer] | [What this means for the feature] |
           | Custom | Provide your own answer | [Explain how to provide custom input] |
           
           **Your choice**: _[Wait for user response]_
           ```

        4. **CRITICAL - Table Formatting**: Ensure markdown tables are properly formatted:
           - Use consistent spacing with pipes aligned
           - Each cell should have spaces around content: `| Content |` not `|Content|`
           - Header separator must have at least 3 dashes: `|--------|`
           - Test that the table renders correctly in markdown preview
        5. Number questions sequentially (Q1, Q2, Q3 - max 3 total)
        6. Present all questions together before waiting for responses
        7. Wait for user to respond with their choices for all questions (e.g., "Q1: A, Q2: Custom - [details], Q3: B")
        8. Update the spec by replacing each [NEEDS CLARIFICATION] marker with the user's selected or provided answer
        9. Re-run validation after all clarifications are resolved

   d. **Update Checklist**: After each validation iteration, update the checklist file with current pass/fail status

7. Report completion with:
   - Branch name and spec file path
   - Checklist results
   - **Traceability summary**:
     - Concept Reference: [CONCEPT_IDS or "Standalone spec"]
     - Acceptance Scenarios created: N (AS-1A to AS-Nx)
     - Functional Requirements: N (FR-001 to FR-00N)
     - Edge Cases: N (EC-001 to EC-00N)
   - **Brownfield summary** (if BROWNFIELD_MODE = true):
     - Change Type: [Enhancement | Refactor | Migration | Bugfix | Performance | Security]
     - Current Behaviors documented: N (CB-001 to CB-00N)
     - Current Limitations identified: N (CL-001 to CL-00N)
     - Change Deltas specified: N (CHG-001 to CHG-00N)
     - Preserved Behaviors: N (PB-001 to PB-00N)
     - Migration Phases: N (if applicable)
     - Baseline used: [Yes - baseline.md | No - manual entry]
   - **Workspace summary** (if WORKSPACE_MODE = true):
     - Workspace: [workspace name]
     - Current Repository: [repo-alias]
     - Cross-Repository Dependencies: N
       - REQUIRES: N
       - EXTENDS: N
       - USES: N
     - Features Depending on This: N (if identified)
   - Readiness for the next phase (`/speckit.clarify` or `/speckit.plan`)

**NOTE:** The script creates and checks out the new branch and initializes the spec file before writing.

## Concept-to-Spec Workflow

When `specs/concept.md` exists, follow this enhanced workflow:

```text
1. User runs: /speckit.specify EPIC-001.F01.S01, EPIC-001.F01.S02

2. Agent reads concept.md and extracts:
   - Stories: EPIC-001.F01.S01, EPIC-001.F01.S02
   - Parent Feature: EPIC-001.F01 (description, priority, dependencies)
   - Parent Epic: EPIC-001 (goal, context)
   - Related User Journeys (J001, J002 that reference these features)
   - Dependencies from Cross-Feature Dependencies matrix

3. Agent creates spec.md with:
   - **Source Concept**: specs/concept.md
   - **Concept IDs Covered**: EPIC-001.F01.S01, EPIC-001.F01.S02
   - User Stories populated from concept story descriptions
   - Priorities inherited from concept (P1a, P1b)
   - Acceptance Scenarios generated with IDs (AS-1A, AS-1B)

4. Agent updates concept.md Traceability Skeleton:
   | Concept ID | Spec Created | Spec Requirements | Status |
   |------------|--------------|-------------------|--------|
   | EPIC-001.F01.S01 | [x] | FR-001, FR-002 | Specified |
   | EPIC-001.F01.S02 | [x] | FR-003 | Specified |
```

**Benefits**:
- No idea loss: all concept stories are tracked
- Priorities flow from concept to spec
- Dependencies are visible across specs
- Full traceability from Vision → Spec → Tasks → Tests

## General Guidelines

## Quick Guidelines

- Focus on **WHAT** users need and **WHY**.
- Avoid HOW to implement (no tech stack, APIs, code structure).
- Written for business stakeholders, not developers.
- DO NOT create any checklists that are embedded in the spec. That will be a separate command.

### Section Requirements

- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation

When creating this spec from a user prompt:

1. **Make informed guesses**: Use context, industry standards, and common patterns to fill gaps
2. **Document assumptions**: Record reasonable defaults in the Assumptions section
3. **Limit clarifications**: Maximum 3 [NEEDS CLARIFICATION] markers - use only for critical decisions that:
   - Significantly impact feature scope or user experience
   - Have multiple reasonable interpretations with different implications
   - Lack any reasonable default
4. **Prioritize clarifications**: scope > security/privacy > user experience > technical details
5. **Think like a tester**: Every vague requirement should fail the "testable and unambiguous" checklist item
6. **Common areas needing clarification** (only if no reasonable default exists):
   - Feature scope and boundaries (include/exclude specific use cases)
   - User types and permissions (if multiple conflicting interpretations possible)
   - Security/compliance requirements (when legally/financially significant)

**Examples of reasonable defaults** (don't ask about these):

- Data retention: Industry-standard practices for the domain
- Performance targets: Standard web/mobile app expectations unless specified
- Error handling: User-friendly messages with appropriate fallbacks
- Authentication method: Standard session-based or OAuth2 for web apps
- Integration patterns: RESTful APIs unless specified otherwise

### Success Criteria Guidelines

Success criteria must be:

1. **Measurable**: Include specific metrics (time, percentage, count, rate)
2. **Technology-agnostic**: No mention of frameworks, languages, databases, or tools
3. **User-focused**: Describe outcomes from user/business perspective, not system internals
4. **Verifiable**: Can be tested/validated without knowing implementation details

**Good examples**:

- "Users can complete checkout in under 3 minutes"
- "System supports 10,000 concurrent users"
- "95% of searches return results in under 1 second"
- "Task completion rate improves by 40%"

**Bad examples** (implementation-focused):

- "API response time is under 200ms" (too technical, use "Users see results instantly")
- "Database can handle 1000 TPS" (implementation detail, use user-facing metric)
- "React components render efficiently" (framework-specific)
- "Redis cache hit rate above 80%" (technology-specific)

## Automation Behavior

When this command completes successfully, the following automation rules apply:

### Auto-Transitions

| Condition | Next Phase | Gate |
|-----------|------------|------|
| spec.md valid, no [NEEDS CLARIFICATION] | `/speckit.plan` | Spec Quality Gate |

### Quality Gates

| Gate | Check | Block Condition | Message |
|------|-------|-----------------|---------|
| Spec Quality Gate | All checklists/requirements.md items pass | Incomplete items > 0 | "Resolve incomplete checklist items before proceeding" |

### Gate Behavior

**If all conditions pass and no gates block:**
- Automatically proceed to `/speckit.plan` with the created specification
- Log transition for audit trail

**If gates block:**
- Display blocking message to user
- List incomplete checklist items
- Wait for user to resolve issues
- Offer handoff options for manual intervention

### Manual Overrides

Users can always choose to:
- Skip automation by selecting a different handoff option
- Force proceed (with acknowledgment of incomplete items)
- Run `/speckit.clarify` to address [NEEDS CLARIFICATION] markers first

---

## Pre-Review Quality Pass (NEW)

**Before formal self-review, apply quality filters to catch common issues.**

**Quality Imports**:
```text
IMPORT: templates/shared/quality/anti-slop.md
IMPORT: templates/shared/quality/reader-testing.md
```

### Step 1: Anti-Slop Scan

Scan all prose content against forbidden phrases:

```text
ANTI_SLOP_SCAN:
  SCAN spec.md FOR FORBIDDEN_OPENINGS + FORBIDDEN_CONCLUSIONS + HEDGE_PHRASES

  IF matches found:
    FOR EACH match:
      IF auto_fixable:
        REWRITE with specific, concrete language
      ELSE:
        FLAG for manual review

  BUZZWORD_CHECK:
    FOR EACH paragraph:
      IF buzzword_count > 2:
        REWRITE with specific technical terms

  SPECIFICITY_CHECK:
    FLAG uses of generic terms: ["users", "system", "process", "data"]
    SUGGEST replacements with concrete nouns
```

### Step 2: Reader Testing

Run fresh reader simulation:

```text
READER_TEST:
  PERSPECTIVE: "New team member reading this spec for the first time"

  COMPREHENSION_CHECK:
    - Can they understand WHAT is being built in <30 seconds?
    - Is the core problem stated with specific examples?
    - Are all acronyms defined on first use?

  ACTIONABILITY_CHECK:
    - Would a developer know where to start coding?
    - Would QA know what to test?
    - Are edge cases explicit?

  AMBIGUITY_SCAN:
    - List sentences with vague pronouns ("it", "this", "that")
    - List comparisons without baselines ("faster", "better", "easier")
    - List conditionals without criteria ("if needed", "when appropriate")

  IF issues found:
    FIX in-place before formal self-review
```

### Step 3: Proceed to Self-Review

Only proceed when:
- Zero forbidden phrases remain
- Buzzword density < 2 per paragraph
- No flagged ambiguities

---

## Self-Review Phase (MANDATORY)

**Before declaring the specification complete, you MUST perform self-review.**

Read `templates/shared/self-review/framework.md` for the complete self-review algorithm.
Read `templates/shared/validation/checkpoints.md` for checkpoint definitions.

**Note**: Universal quality checks (SR-SLOP-*, SR-READ-*) are now included in the self-review framework.

```text
SELF_REVIEW_INPUT:
  ARTIFACT = FEATURE_DIR/spec.md
  COMPLEXITY_TIER = from step 0
  CRITERIA_SET = SR-SPEC-01 to SR-SPEC-10 (+ domain-specific if applicable)

EXECUTE self-review framework with up to 3 iterations
GENERATE Self-Review Report
```

### Step 1: Re-read Your Output

Read the spec.md file you just created:
1. Open `FEATURE_DIR/spec.md`
2. Read through all sections completely
3. Check for consistency and completeness

### Step 2: Quality Criteria

Criteria active based on COMPLEXITY_TIER:
- **TRIVIAL**: SR-SPEC-01, 02, 03 only
- **SIMPLE**: SR-SPEC-01 to 06
- **MODERATE/COMPLEX**: All SR-SPEC-01 to 10

Answer each question by examining the specification:

| ID | Question | Severity |
|----|----------|----------|
| SR-SPEC-01 | All mandatory sections filled (Overview, User Stories, FR, AS, SC)? | CRITICAL |
| SR-SPEC-02 | No implementation details (frameworks, APIs, databases, languages)? | HIGH |
| SR-SPEC-03 | Each FR has at least one linked AS? | HIGH |
| SR-SPEC-04 | All AS follow Given/When/Then format? | MEDIUM |
| SR-SPEC-05 | No [NEEDS CLARIFICATION] markers remain (or max 3 critical ones)? | MEDIUM |
| SR-SPEC-06 | Success Criteria are measurable with specific metrics? | HIGH |
| SR-SPEC-07 | Success Criteria are technology-agnostic? | HIGH |
| SR-SPEC-08 | User Stories have clear acceptance scenarios? | MEDIUM |
| SR-SPEC-09 | Edge cases (EC-xxx) identified for error scenarios? | MEDIUM |
| SR-SPEC-10 | Traceability Summary table complete and accurate? | LOW |

**UXQ Domain Criteria** *(apply when UXQ domain is active)*:

Check if `memory/constitution.domain.md` references UXQ domain. If yes, also validate:

| ID | Question | Severity |
|----|----------|----------|
| SR-UXQ-01 | Jobs to Be Done documented with proper format (When/Want/So)? | HIGH |
| SR-UXQ-02 | Each FR traces to at least one JTBD? | HIGH |
| SR-UXQ-03 | User Mental Model section describes user expectations? | MEDIUM |
| SR-UXQ-04 | FTUE section documents first-time user flow separately? | HIGH |
| SR-UXQ-05 | All friction points have type AND justification? | HIGH |
| SR-UXQ-06 | No unjustified friction remains in the list? | CRITICAL |
| SR-UXQ-07 | Delight opportunities identified for success states? | LOW |
| SR-UXQ-08 | Emotional journey maps key steps with design responses? | MEDIUM |
| SR-UXQ-09 | Accessibility framed as empowerment (not just compliance)? | HIGH |
| SR-UXQ-10 | Error messages documented from user perspective (UXQ-005)? | HIGH |

**Workspace Criteria** *(apply when WORKSPACE_MODE = true)*:

Check if `.speckit-workspace` exists in parent directories. If yes, also validate:

| ID | Question | Severity |
|----|----------|----------|
| SR-WS-01 | Cross-Repository Dependencies section present (if dependencies exist)? | MEDIUM |
| SR-WS-02 | All cross-repo references use valid `repo-alias:feature-id` format? | HIGH |
| SR-WS-03 | Referenced repository aliases exist in workspace config? | HIGH |
| SR-WS-04 | Dependency types are valid (REQUIRES, BLOCKS, EXTENDS, IMPLEMENTS, USES)? | MEDIUM |
| SR-WS-05 | No self-referential dependencies (feature depending on itself)? | HIGH |

**Evaluation format**:
```text
🔍 Self-Review: Specification Quality
├── SR-SPEC-01: ✅ PASS - All 5 mandatory sections present
├── SR-SPEC-02: ⚠️ HIGH - Found "PostgreSQL" in FR-003
├── SR-SPEC-03: ✅ PASS - 8/8 FRs linked to AS
├── SR-SPEC-04: ✅ PASS - All AS use Given/When/Then
├── SR-SPEC-05: ✅ PASS - 0 unresolved markers
├── SR-SPEC-06: ✅ PASS - All SC have metrics
├── SR-SPEC-07: ⚠️ HIGH - SC-002 mentions "API response time"
├── SR-SPEC-08: ✅ PASS - All stories have AS
├── SR-SPEC-09: ✅ PASS - 4 edge cases defined
└── SR-SPEC-10: ✅ PASS - Traceability table complete

Summary: CRITICAL=0, HIGH=2, MEDIUM=0, LOW=0
```

### Step 3: Verdict

Determine the self-review verdict:

| Verdict | Condition | Action |
|---------|-----------|--------|
| **PASS** | CRITICAL=0 AND HIGH=0 | Proceed to /speckit.plan handoff |
| **WARN** | CRITICAL=0 AND HIGH≤2 | Show warnings, proceed with caution |
| **FAIL** | CRITICAL>0 OR HIGH>2 | Self-correct, re-check |

### Step 4: Self-Correction Loop

**IF verdict is FAIL AND iteration < 3**:
1. Fix each CRITICAL and HIGH issue:
   - Remove implementation details (replace with technology-agnostic language)
   - Add missing FR→AS links
   - Rewrite SC to remove technical metrics
   - Resolve or reduce [NEEDS CLARIFICATION] markers
2. Re-run self-review from Step 1
3. Increment iteration counter
4. Report: `Self-Review Iteration 2/3...`

**Common fixes**:
| Issue | Fix |
|-------|-----|
| "PostgreSQL" in FR | Replace with "persistent data storage" |
| "API response < 200ms" | Replace with "Users see results instantly" |
| Missing AS link | Add `*Acceptance Scenarios*: AS-xxx` to FR |
| Vague SC | Add specific metric: "completion rate", "time", "error rate" |

**IF still FAIL after 3 iterations**:
```text
❌ Self-Review FAILED after 3 iterations

Remaining issues:
- SR-SPEC-02: Implementation detail in FR-003 ("uses WebSocket")
- SR-SPEC-07: SC-002 still mentions "API latency"

⛔ BLOCKING: Cannot proceed to planning.
   Fix remaining issues or override with user confirmation.

User: Proceed anyway? (yes/no)
```

**IF verdict is PASS or WARN**:
```text
✅ Self-Review PASSED

Summary:
- Quality Criteria: 10/10 passing
- Iterations: 1
- Traceability: 8 FRs → 12 AS → 4 EC

→ Proceeding to handoff: /speckit.plan
```

### Self-Review Report Template

Generate this report before handoff:

```markdown
## Self-Review Report

**Command**: /speckit.specify
**Artifact**: spec.md
**Reviewed at**: {{TIMESTAMP}}
**Iteration**: {{N}}/3

### Quality Criteria
| ID | Question | Status |
|----|----------|--------|
| SR-SPEC-01 | All mandatory sections? | ✅ PASS |
| SR-SPEC-02 | No implementation details? | ✅ PASS |
| SR-SPEC-03 | FR→AS links complete? | ✅ PASS |
| SR-SPEC-04 | AS format correct? | ✅ PASS |
| SR-SPEC-05 | Clarifications resolved? | ✅ PASS |
| SR-SPEC-06 | SC measurable? | ✅ PASS |
| SR-SPEC-07 | SC tech-agnostic? | ✅ PASS |
| SR-SPEC-08 | Stories have AS? | ✅ PASS |
| SR-SPEC-09 | Edge cases defined? | ✅ PASS |
| SR-SPEC-10 | Traceability complete? | ✅ PASS |

### Traceability Summary
- Functional Requirements: 8 (FR-001 to FR-008)
- Acceptance Scenarios: 12 (AS-1A to AS-4C)
- Edge Cases: 4 (EC-001 to EC-004)
- Concept Reference: EPIC-001.F01.S01 (or "Standalone")

### Verdict: ✅ PASS
**Reason**: All criteria met, specification ready for planning.

→ Proceeding to handoff: /speckit.plan
```

## Manifest Update

After Self-Review passes, update the feature manifest:

```text
Read `templates/shared/core/manifest-update.md` and apply with:
- NEW_STATUS = "SPEC_COMPLETE"
- CALLER_COMMAND = "specify"

EXECUTE manifest-update.md algorithm
LOG: "Feature manifest updated: DRAFT → SPEC_COMPLETE"
```

---

## Spec Validation Phase (Auto-Triggered)

After Self-Review passes, the `pre_handoff_action` automatically triggers spec validation before handing off to `/speckit.plan`. This catches constitution violations and ambiguities early.

### Validation Flow

```text
1. Self-Review completes with PASS verdict
2. pre_handoff_action triggers:
   - Invoke: /speckit.analyze --profile spec_validate --quiet
   - Timeout: 30 seconds
3. Evaluate validation gates:
   - Constitution Alignment (Pass D): threshold 0, severity CRITICAL
   - Ambiguity Count (Pass B): threshold 5, severity HIGH
4. On gate status:
   - ALL PASS → Proceed to /speckit.plan
   - ANY FAIL → Auto-remediate via /speckit.clarify
```

### Validation Output (Compact)

When spec validation runs, display compact gate results:

```markdown
## Spec Validation Complete

| Gate | Pass | Threshold | Actual | Status |
|------|------|-----------|--------|--------|
| Constitution Alignment | D | 0 | 0 | ✅ |
| Ambiguity Count | B | 5 | 3 | ✅ |

**Result**: PASS

→ Proceeding to handoff: /speckit.plan
```

### On Validation Failure

When gates fail, block handoff and auto-invoke clarify:

```markdown
## Spec Validation BLOCKED

| Gate | Pass | Threshold | Actual | Status |
|------|------|-----------|--------|--------|
| Constitution Alignment | D | 0 | 2 | ❌ FAIL |
| Ambiguity Count | B | 5 | 7 | ⚠️ WARN |

**Result**: FAIL

### Blocking Issues

1. **[CRITICAL] Constitution Violation**: FR-003 conflicts with principle "No External Dependencies Without Approval"
2. **[CRITICAL] Constitution Violation**: AS-2B implies server-side storage, violates "Privacy First" principle

### Extracted Clarification Questions

1. FR-003 references "cloud sync" - does this require explicit user opt-in per constitution?
2. AS-2B stores user data server-side - what anonymization is required?
3. [Plus 5 ambiguity-derived questions from Pass B]

→ Auto-invoking `/speckit.clarify` with 7 extracted questions...
```

### Skip Validation

To bypass spec validation (not recommended):

```bash
# Skip validation gate
/speckit.specify --skip-validate

# Equivalent short form
/speckit.specify --fast
```

When skipped, log warning:

```text
⚠️ Spec validation skipped (--skip-validate). Constitution and ambiguity gates not enforced.
→ Proceeding to handoff: /speckit.plan (unvalidated)
```

### Post-Clarification Loop

After `/speckit.clarify` resolves issues, re-run validation:

```text
1. clarify completes
2. Re-invoke: /speckit.analyze --profile spec_validate --quiet
3. If gates pass → Resume handoff to /speckit.plan
4. If gates fail → Repeat clarification (max 3 iterations)
5. After 3 iterations → Require manual intervention
```

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
# Specification Complete

## Quick Summary

| Aspect | Value |
|--------|-------|
| **Feature** | {feature_name} |
| **Complexity** | {COMPLEXITY_TIER} ({complexity_score}/100) |
| **User Stories** | {story_count} stories |
| **Requirements** | {fr_count} functional, {nfr_count} non-functional |
| **Scenarios** | {as_count} acceptance scenarios |
| **Status** | {status_badge} |
| **Next Step** | {next_step} |

### Key Requirements

1. **{FR-001}**: {brief_description}
2. **{FR-002}**: {brief_description}
3. **{FR-003}**: {brief_description}

### Scope Boundaries

- **In Scope**: {in_scope_summary}
- **Out of Scope**: {out_scope_summary}
```

### Format Full Content

```text
IF MODE == COMPACT:
  OUTPUT: Quick Summary (above)
  OUTPUT: <details><summary>📄 View Full Specification</summary>
  OUTPUT: {full_spec_content}
  OUTPUT: </details>

ELIF MODE == STANDARD:
  OUTPUT: Quick Summary (above)
  OUTPUT: ---
  OUTPUT: {full_spec_content with collapsible verbose sections}

ELIF MODE == DETAILED:
  OUTPUT: Quick Summary (above)
  OUTPUT: ---
  OUTPUT: {full_spec_content all sections expanded}
  OUTPUT: ---
  OUTPUT: {self_review_report}
```

### Update Artifact Registry

```text
Read `templates/shared/traceability/artifact-registry.md` and apply:

UPDATE_REGISTRY("spec", "FEATURE_DIR/spec.md", {
  parent_concept_version: registry.artifacts.concept.version OR null,
  fr_count: {fr_count},
  as_count: {as_count}
})

# Check cascade impact
IF registry was updated:
  staleness = CHECK_STALENESS(registry)
  IF staleness.any_downstream_affected:
    OUTPUT: "Note: Downstream artifacts may need refresh."
```
