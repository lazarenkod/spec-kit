---
description: Execute the implementation plan, generate documentation (RUNNING.md, README.md), and validate with self-review. Enforces Quality Gates (QG-001 pre-implement gate, QG-004 to QG-009 post-implement gates). See `memory/domains/quality-gates.md` for gate definitions.
persona: developer-agent
handoff:
  requires: handoffs/tasks-to-implement.md
  template: templates/handoff-template.md
handoffs:
  - label: QA Verification
    agent: speckit.analyze
    prompt: |
      Run post-implementation QA analysis (QA mode):
      - Verify build succeeds and tests pass
      - Check code traceability (@speckit annotations)
      - Validate security (dependency audit, secret detection)
      - Generate QA Verification Report with verdict

      Validates Quality Gates QG-004 to QG-009 (post-implement gates):
      - QG-004: Test Coverage >= 80%
      - QG-005: Type Coverage >= 95%
      - QG-006: Lint Cleanliness (0 errors)
      - QG-007: Performance Baseline (Lighthouse >= 90)
      - QG-008: Accessibility Compliance (WCAG 2.1 AA)
      - QG-009: Documentation Coverage (100% public APIs)

      See memory/domains/quality-gates.md for gate details.
    auto: true
    condition:
      - "All P1 tasks marked [X] in tasks.md"
      - "Implementation phase completed"
    gates:
      - name: "Implementation Complete Gate"
        check: "No incomplete P1 tasks in tasks.md"
        block_if: "P1 tasks remain [ ]"
        message: "Complete all P1 tasks before QA verification"
      - name: "Build Artifacts Gate"
        check: "Implementation produced runnable code"
        block_if: "No source files created or modified"
        message: "No implementation detected - verify tasks were executed"
      - name: "QG-004: Test Coverage Gate"
        check: "Test coverage >= 80%"
        block_if: "Coverage < 80%"
        message: "Test coverage below 80% threshold"
        domain_ref: "QG-004"
      - name: "QG-005: Type Coverage Gate"
        check: "Type coverage >= 95%"
        block_if: "Type coverage < 95%"
        message: "Type coverage below 95% threshold"
        domain_ref: "QG-005"
      - name: "QG-006: Lint Gate"
        check: "Lint errors == 0"
        block_if: "Lint errors > 0"
        message: "Lint errors must be resolved"
        domain_ref: "QG-006"
    post_actions:
      - "log: Implementation complete, running QA verification"
  - label: Comprehensive Verification
    agent: speckit.verify
    prompt: |
      Run comprehensive post-implementation verification:
      - Acceptance Criteria: Verify all AS-xxx scenarios implemented and passing
      - API Contracts: Validate endpoints match spec.md definitions
      - Visual Verification: UI matches Visual YAML specs (screenshots + pixelmatch)
      - Behavior: E2E user flows work as specified
      - NFRs: Performance, accessibility, security thresholds met

      Generates detailed report with auto-fix suggestions for common issues.
      Requires 90% overall pass rate to proceed.

      Note: This is a comprehensive alternative to /speckit.analyze that includes
      visual regression testing and behavior verification.
    auto: false
    condition:
      - "All waves completed"
      - "User wants comprehensive validation"
      - "Visual or behavioral verification needed"
  - label: Fix QA Issues
    agent: speckit.implement
    prompt: Address issues identified in QA verification report
    auto: false
    condition:
      - "QA report shows CRITICAL or HIGH issues"
      - "QA Verdict == FAIL"
    gates:
      - name: "QA Issues Exist Gate"
        check: "QA Verdict != PASS"
        block_if: "QA Verdict == PASS"
        message: "No QA issues to fix - all checks passed"
  - label: Update Tasks
    agent: speckit.tasks
    prompt: Regenerate or update tasks based on implementation learnings
    auto: false
    condition:
      - "Implementation revealed missing tasks"
      - "Scope changed during implementation"
  - label: Update Spec
    agent: speckit.specify
    prompt: Update specification to reflect implementation decisions
    auto: false
    condition:
      - "Implementation required spec deviations"
      - "New requirements discovered during implementation"
inline_gates:
  enabled: true
  skip_flag: "--skip-gates"
  strict_flag: "--strict-gates"
  full_flag: "--full-gates"
  mode: progressive
  on_failure: block
  # Pre-implementation gates (run before Wave 1)
  pre_gates:
    - id: IG-IMPL-001
      name: "Tasks Exist"
      tier: 1
      check: "tasks.md exists in FEATURE_DIR"
      threshold: 0
      severity: CRITICAL
      message: "Run /speckit.tasks first to generate task breakdown"
    - id: IG-IMPL-002
      name: "Plan Exists"
      tier: 1
      check: "plan.md exists in FEATURE_DIR"
      threshold: 0
      severity: CRITICAL
      message: "Run /speckit.plan first to generate implementation plan"
    - id: IG-IMPL-003
      name: "Staging Ready"
      ref: QG-STAGING-001
      tier: 1
      threshold: 0
      severity: CRITICAL
      message: "Staging environment not healthy - run docker compose up"
    - id: IG-IMPL-004
      name: "SQS Threshold"
      ref: QG-001
      tier: 3
      threshold: 80
      severity: HIGH
      message: "SQS below 80 - improve spec quality first"
    - id: IG-IMPL-005
      name: "Test Framework Ready"
      ref: QG-TEST-002
      tier: 1
      threshold: 0
      severity: CRITICAL
      auto_remediation:
        enabled: true
        skip_flag: "--no-auto-framework"
        agent: framework-installer
        timeout: 180000  # 3 minutes
      message: |
        Test framework not configured. Auto-installing...
        To skip: use --no-auto-framework flag
    - id: IG-IMPL-006
      name: "Properties Available"
      tier: 1
      check: "properties.md exists in FEATURE_DIR"
      info_only: true
      on_exists: "PBT JIT mode enabled"
      on_missing: "No properties.md - PBT JIT disabled"
  # Post-implementation gates (run after Wave 4)
  post_gates:
    - id: IG-IMPL-101
      name: "Build Success"
      pass: R
      tier: 1
      threshold: 0
      severity: CRITICAL
      message: "Build failed"
    - id: IG-IMPL-102
      name: "Tests Pass"
      pass: S
      tier: 2
      threshold: 0
      severity: CRITICAL
      message: "Tests failing"
    - id: IG-IMPL-103
      name: "Coverage Threshold"
      pass: T
      ref: QG-004
      tier: 2
      threshold: 80
      severity: HIGH
      message: "Test coverage below 80%"
    - id: IG-IMPL-104
      name: "Lint Clean"
      pass: U
      ref: QG-006
      tier: 2
      threshold: 0
      severity: HIGH
      message: "Lint errors present"
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
artifact_extraction:
  enabled: true
  skip_flag: "--full-context"
  framework: templates/shared/artifact-extraction.md
  spec_fields:
    - fr_list               # FR-001, FR-002, ...
    - as_list               # AS-1A, AS-1B, ...
    - ec_list               # EC-001, EC-002, ...
    - sc_list               # SC-001, SC-002, ...
    - story_priorities      # {US1: P1a, ...}
    - component_registry    # UI components
    - screen_registry       # Screens for [VR:] validation
    - fr_summaries
    - as_summaries
  plan_fields:
    - tech_stack            # Language, framework, database
    - dependencies          # Package list with versions
    - phases                # Implementation phases
    - adr_decisions         # ADR summaries
    - file_structure        # Directory layout
    - dependency_registry   # API docs URLs for [DEP:] markers
  task_fields:
    - task_summary          # Task IDs, names, priorities
    - dependency_graph      # Task dependencies for batching
    - wave_grouping         # Wave assignments (0-5)
    - test_markers          # [TEST:AS-xxx] references
    - fr_markers            # [FR:FR-xxx] references
    - vr_markers            # [VR:VR-xxx] for vision validation
    - wire_markers          # [WIRE:COMP→SCR] for component wiring
  properties_fields:        # If properties.md exists
    - property_list         # PROP-001, PROP-002, ...
    - prop_mappings         # PROP → FR/AS mapping
auto_fix_rules:
  enabled: true
  skip_flag: "--no-auto-fix"
  max_iterations: 3
  rules:
    - id: AF-001
      name: "Missing @speckit annotations"
      trigger: "SR-IMPL-05 or SR-IMPL-06 FAIL"
      action: insert_annotation
      source: "task markers [FR:FR-xxx], [TEST:AS-xxx]"
    - id: AF-002
      name: "TODO/FIXME/HACK comments"
      trigger: "SR-IMPL-04 FAIL"
      action: convert_to_issue
      target: ".speckit/issues.md"
    - id: AF-003
      name: "Lint warnings (fixable)"
      trigger: "Lint check with fixable errors"
      action: run_auto_formatter
      commands:
        javascript: "npx eslint --fix OR npx prettier --write"
        python: "ruff format . OR black ."
        rust: "cargo fmt"
        go: "gofmt -w ."
    - id: AF-004
      name: "Missing .env.example"
      trigger: "SR-IMPL-13 FAIL"
      action: generate_env_example
    - id: AF-005
      name: "Debug statements"
      trigger: "SR-IMPL-09 FAIL"
      action: remove_debug_statements
    - id: AF-006
      name: "Hardcoded hex color to CSS variable"
      trigger: "SR-IMPL-18 FAIL"
      action: replace_hardcoded_color
      patterns:
        - "#[0-9A-Fa-f]{6}"
        - "#[0-9A-Fa-f]{3}"
      transform: "Match to closest design token, replace with var(--token-name)"
    - id: AF-007
      name: "Custom component to library import"
      trigger: "SR-IMPL-19 FAIL"
      action: suggest_library_component
      source: "constitution.md design_system.components mapping"
    - id: AF-008
      name: "Hardcoded font-size to typography token"
      trigger: "SR-IMPL-20 FAIL"
      action: replace_hardcoded_typography
      patterns:
        - "font-size:\\s*\\d+px"
        - "fontSize:\\s*\\d+"
      transform: "Map px to typography scale token"
build_error_patterns:
  enabled: true
  max_build_attempts: 3
  skip_flag: "--no-build-fix"
  # Performance optimization: See templates/shared/implement/build-optimizer.md
  precompile_patterns: true  # Pre-compile regex patterns at session start
  smart_retry: true          # Use progressive timeout strategy (30s→20s→15s)
  patterns:
    typescript:
      - pattern: "Cannot find module '(.+)'"
        rule: BF-001
        action: add_import
      - pattern: "'(.+)' is declared but its value is never read"
        rule: BF-002
        action: prefix_unused
      - pattern: "Property '(.+)' does not exist on type"
        rule: BF-003
        action: add_type_annotation
    react:
      - pattern: "Each child in a list should have a unique \"key\" prop"
        rule: BF-004
        action: add_key_prop
      - pattern: "React Hook .+ is called conditionally"
        rule: BF-005
        action: move_hook_to_top
    python:
      - pattern: "ModuleNotFoundError: No module named '(.+)'"
        rule: BF-001
        action: add_import
      - pattern: "NameError: name '(.+)' is not defined"
        rule: BF-006
        action: add_import_or_define
    go:
      - pattern: "undefined: (.+)"
        rule: BF-001
        action: add_import
      - pattern: "(.+) declared but not used"
        rule: BF-002
        action: prefix_unused
    rust:
      - pattern: "cannot find .+ `(.+)` in this scope"
        rule: BF-001
        action: add_use_statement
      - pattern: "unused variable: `(.+)`"
        rule: BF-002
        action: prefix_unused
    eslint:
      - pattern: "'(.+)' is defined but never used"
        rule: BF-002
        action: prefix_unused
    kotlin:
      - pattern: "Unresolved reference: (.+)"
        rule: BF-001
        action: add_import
      - pattern: "Variable '(.+)' is never used"
        rule: BF-002
        action: prefix_unused
      - pattern: "Type mismatch: inferred type is .+ but (.+) was expected"
        rule: BF-003
        action: add_type_annotation
      - pattern: "Classifier '(.+)' does not have a companion object"
        rule: BF-007
        action: add_companion_object
      - pattern: "'(.+)' is a suspend function"
        rule: BF-008
        action: wrap_in_coroutine_scope
    kotlin_compose:
      - pattern: "@Composable invocations can only happen"
        rule: BF-009
        action: add_composable_annotation
      - pattern: "Modifier parameter should be the first"
        rule: BF-010
        action: reorder_modifier_param
    java:
      - pattern: "cannot find symbol.*symbol:\\s*class (.+)"
        rule: BF-001
        action: add_import
      - pattern: "cannot find symbol.*symbol:\\s*variable (.+)"
        rule: BF-006
        action: add_import_or_define
      - pattern: "variable (.+) is never used"
        rule: BF-002
        action: prefix_unused
      - pattern: "package (.+) does not exist"
        rule: BF-001
        action: add_import
      - pattern: "incompatible types: (.+) cannot be converted"
        rule: BF-003
        action: add_type_cast
      - pattern: "non-static method .+ cannot be referenced from a static context"
        rule: BF-011
        action: add_instance_or_static
vision_validation:
  enabled: true
  skip_flag: "--no-vision"
  trigger: "UI_FEATURE"  # Only for tasks with [VR:VR-xxx] markers or role_group = FRONTEND
  # Performance optimization: See templates/shared/implement/vision-turbo.md
  turbo_mode:
    enabled: true
    skip_flag: "--no-turbo"
    max_parallel_contexts: 3
    fallback_on_error: sequential
  screenshots:
    tool: "playwright_mcp"
    viewports:
      - { name: "mobile", width: 375, height: 812 }
      - { name: "tablet", width: 768, height: 1024 }
      - { name: "desktop", width: 1440, height: 900 }
    states:
      - default
      - loading
      - error
      - empty
      - success
  validation:
    frameworks:
      - "memory/domains/uxq.md"
      - "memory/knowledge/frameworks/nielsen-heuristics.md"
    anti_patterns:
      - "memory/knowledge/anti-patterns/ux.md"
    severity_threshold: "HIGH"  # Block on CRITICAL
    max_issues: 10
  output:
    report_path: "specs/{feature}/ux-audit.md"
    template: "templates/ux-audit-template.md"
    format: "markdown"
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
        timeout_per_agent: 180000
        retry_on_failure: 1
      pro:
        thinking_budget: 16000
        max_parallel: 4
        batch_delay: 4000
        wave_overlap_threshold: 0.80
        timeout_per_agent: 300000
        retry_on_failure: 2
      max:
        thinking_budget: 32000
        max_parallel: 8
        batch_delay: 1500
        wave_overlap_threshold: 0.65
        timeout_per_agent: 900000
        retry_on_failure: 3
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
  phases:
    setup:
      model: haiku
      reasoning_mode: normal
      thinking_budget: 4000  # Max tier
      description: "Project init, deps, ignore files"
    core:
      model: opus
      reasoning_mode: extended
      thinking_budget: 20000  # Max tier
      description: "Business logic, services, models"
    tests:
      model: sonnet
      reasoning_mode: normal
      thinking_budget: 8000  # Max tier
      description: "Test code generation"
    self_review:
      model: haiku
      reasoning_mode: normal
      thinking_budget: 4000  # Max tier
      description: "Auto-fix, annotations, formatting"
  orchestration:
    max_parallel: 8
    conflict_resolution: queue
    timeout_per_agent: 900000
    retry_on_failure: 3
    role_isolation: true
    # Performance optimization: See templates/shared/implement/wave-overlap.md
    wave_overlap:
      enabled: true
      skip_flag: "--sequential-waves"
      # Wave-specific thresholds for aggressive parallelization (v0.0.104)
      wave_thresholds:
        wave_0_to_1: 1.0   # Staging MUST complete 100% (QG-STAGING-001)
        wave_1_to_2: 0.60  # Infrastructure mostly ready before tests
        wave_2_to_3: 0.40  # AGGRESSIVE: Start impl when 40% tests written
        wave_3_to_4: 0.50  # Start verification at 50% implementation
        wave_4_to_5: 0.70  # Conservative: tests are critical for review
      conservative_mode_flag: "--conservative-overlap"  # Use 0.65 for all waves
      critical_deps_only: true
    # Parallel test execution (v0.0.104)
    test_parallelization:
      enabled: true
      skip_flag: "--sequential-tests"
      parallel_suites: [unit, integration]  # Run in parallel
      sequential_suites: [e2e]              # Run after parallel complete
    # Task-level batching: Group independent tasks for parallel execution (v0.0.110)
    # See templates/shared/implement/task-batching.md for full algorithm
    task_batching:
      enabled: true
      skip_flag: "--sequential-tasks"
      max_batch_size: 8                     # Max tasks per batch (rate limit safe)
      batch_by: dependency_level            # Group by topological level
      file_conflict_resolution: queue       # Same-file tasks → sequential
      parallel_marker: "[P]"                # Explicit parallel marker (optional)
      model_per_task: true                  # Select model per task complexity
    # PBT Just-in-Time testing: Run property tests after each related task
    pbt_jit:
      enabled: true
      skip_flag: "--skip-pbt-jit"
      trigger: "after each task that maps to PROP-xxx"
      max_fix_attempts: 3
      auto_fix: true
      block_on_failure: true
      metrics:
        - properties_validated
        - auto_fixes_applied
        - shrunk_examples_found
    # Auto-provision staging: Automatically invoke /speckit.staging if needed
    staging_auto_provision:
      enabled: true
      skip_flag: "--no-auto-staging"
      timeout: 120000  # 2 min for docker services to start
      retry_on_failure: 1
      fallback: "block_and_prompt"
      detection:
        check_files:
          - ".speckit/staging/docker-compose.yaml"
          - ".speckit/staging/test-config.env"
        require_keywords_in_tasks:
          - "[TEST:AS-"
          - "integration"
          - "e2e"
        skip_if_flag: "--skip-tests"
    # Task status enforcement: Ensure tasks.md is updated after each task
    task_status_enforcement:
      enabled: true
      trigger: "after each Wave 3 task completion"
      blocking: true
      action: |
        AFTER completing any implementation task:
        1. STOP before proceeding to next task
        2. Read tasks.md
        3. Find the task ID (T001, T002, etc.) that was just completed
        4. Change `- [ ] T00x...` → `- [X] T00x...`
        5. Save tasks.md
        6. ONLY THEN proceed to next task
      enforcement: "Each subagent MUST update tasks.md before returning"
    # Changelog update: Ensure CHANGELOG.md is updated after feature completion
    changelog_update:
      enabled: true
      trigger: "after code review in Wave 5"
      skip_markers: ["[INTERNAL]", "[NO-CHANGELOG]"]
      skip_waves: [1, 2]  # Infrastructure-only waves don't need changelog
      format: "keep-a-changelog"  # https://keepachangelog.com
  # Complexity-adaptive model selection: See templates/shared/implement/model-selection.md
  model_selection:
    enabled: true
    skip_flag: "--no-adaptive-model"
    complexity_tier: "${COMPLEXITY_TIER}"  # TRIVIAL, SIMPLE, MODERATE, COMPLEX
  # Autonomous execution mode: Skip all user prompts for unattended runs
  autonomous_mode:
    enabled: false
    flag: "--autonomous"
    alias: "--auto"
    description: "Run without user prompts, auto-proceed on all validation gates"
    behavior:
      checklist_incomplete: "proceed_with_warning"
      staging_missing: "auto_provision_then_soft_fail"  # Try auto-staging first, soft fail if Docker unavailable
      api_verification_fail: "proceed_with_warning"
  # Continuous execution: Complete all waves without pausing
  execution_mode:
    mode: "continuous"  # Options: interactive (default), continuous
    description: "Control execution flow between waves and tasks"
    continuous_behavior:
      pause_between_waves: false
      pause_between_tasks: false
      summary_timing: "end_only"  # Options: per_wave, per_task, end_only
      confirmation_requests: "none"  # Options: all, errors_only, none
  subagents:
    # Wave 0: Staging Validation (verify test infrastructure is ready)
    - role: staging-validator
      role_group: INFRA
      parallel: false
      depends_on: []
      priority: 11
      trigger: "before any implementation starts"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Staging: .speckit/staging/docker-compose.yaml
        Auto-provision: enabled (unless --no-auto-staging flag set)

        ## Task
        Validate or provision staging environment for TDD:

        ### Step 1: Check staging status
        ```bash
        if [ -f ".speckit/staging/docker-compose.yaml" ]; then
          echo "Staging config exists, checking health..."
          docker-compose -f .speckit/staging/docker-compose.yaml ps
        else
          echo "Staging config not found"
        fi
        ```

        ### Step 2: Auto-provision if needed
        IF staging config does NOT exist AND `--no-auto-staging` is NOT set:
        1. LOG: "⚙️ Auto-provisioning staging environment..."
        2. Execute /speckit.staging workflow:
           - Read templates/commands/staging.md
           - Generate docker-compose.yaml based on spec.md/tasks.md requirements
           - Start services with `docker-compose up -d --wait`
           - Wait for health checks (max 2 minutes)
        3. Verify QG-STAGING-001 passes
        4. IF failed after timeout:
           - LOG: "❌ Auto-staging failed"
           - BLOCK with instructions

        ### Step 3: Verify health (if staging exists)
        IF staging config exists:
        1. Check all containers are running and healthy
        2. Validate database is accessible (port 5433)
        3. Validate redis if enabled (port 6380)
        4. Pass QG-STAGING-001

        ## Success Criteria
        - docker-compose.yaml exists (auto-created if needed)
        - All staging services pass health checks
        - QG-STAGING-001: PASSED
        - Test database is accessible

        ## On Failure
        - IF auto-provision was attempted AND failed:
          - LOG: "❌ Auto-staging failed. Check Docker is running."
          - Output: "Run `/speckit.staging --reset` to troubleshoot"
          - Block implementation
        - IF `--no-auto-staging` flag is set AND staging not found:
          - Output: "Run /speckit.staging to provision test infrastructure"
          - Block implementation until staging is ready
        - IF `--autonomous` flag is set AND staging still unhealthy:
          - Log warning: "⚠️ AUTONOMOUS MODE: Staging not validated (QG-STAGING-001 skipped)"
          - Continue to Wave 1 (soft fail - tests may fail later)
      model_override: haiku

    # Wave 0.5: Mobile Architecture Review (if mobile platform detected)
    - role: mobile-architecture-reviewer
      role_group: VALIDATION
      parallel: false
      depends_on: []
      priority: 5
      trigger: "when mobile platform detected (KMP, Flutter, React Native, Native)"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Platform: {{PLATFORM_DETECTED}}

        ## Purpose
        Review mobile architecture BEFORE implementation to ensure patterns align with platform best practices. This catches architectural issues early, preventing costly refactoring later.

        ## Task
        Load and apply mobile expertise:

        1. **Load Mobile Agent**:
           - Persona: mobile-developer-agent
           - Skills: mobile-architecture, mobile-performance, mobile-testing
           - Platform skill: {{PLATFORM}}-expert (kmp-expert, flutter-expert, react-native-expert)

        2. **Architecture Pre-Check**:
           - Verify layer separation in plan.md (Presentation → Domain → Data)
           - Check DI framework configuration planned
           - Validate offline-first strategy (if user data involved)
           - Review state management approach

        3. **Calculate Preliminary MQS**:
           - Estimate architecture score based on plan
           - Identify potential performance concerns
           - Flag missing test coverage areas
           - Note accessibility requirements

        4. **Generate Architecture Recommendations**:
           IF any issues found:
             - Create memory/mobile-architecture-recommendations.md
             - List required changes before implementation
             - Provide code patterns from loaded skill

        ## Success Criteria
        - Mobile agent loaded and skills activated
        - Architecture alignment verified (or recommendations generated)
        - Preliminary MQS score estimated
        - No blocking architectural issues

        ## Output
        ```text
        📱 Mobile Architecture Review

        Platform: {platform}
        Skills: mobile-architecture, {platform}-expert

        Architecture Alignment:
        ✅ Layer separation planned correctly
        ✅ Koin DI configured for KMP
        ⚠️ Missing offline cache for user annotations
        ✅ ViewModel with StateFlow pattern

        Preliminary MQS Estimate: 75-85 (target: ≥75)

        Recommendations:
        - Add offline cache for annotations in ReaderRepository
        - Include binding tests for all ViewModels

        Proceeding to Wave 1...
        ```
      model_override: haiku
      skip_when: "platform not in [kmp, flutter, react-native, ios-native, android-native]"

    # Framework Installer Agent (Universal Auto-Remediation)
    # This agent is automatically invoked when QG-TEST-002 fails during pre-gates check.
    # It uses the Test Framework Registry for universal framework installation.
    - role: framework-installer
      role_group: AUTO_REMEDIATION
      parallel: false
      depends_on: []
      priority: 5  # Runs before Wave 1 if triggered
      trigger: "on QG-TEST-002 FAIL (auto-remediation)"
      model_override: haiku  # Fast, cost-efficient for installation tasks
      timeout: 180000  # 3 minutes
      prompt: |
        ## Context
        QG-TEST-002 quality gate failed: Test framework not properly configured.

        This agent provides universal auto-remediation for ANY test framework using the
        Test Framework Registry (memory/domains/test-framework-registry.md).

        ## Task
        Automatically detect and install appropriate test frameworks for all testing layers.

        ### Step 1: Load Registry & Detect Strategy

        **Load the Test Framework Registry:**
        ```bash
        Read: memory/domains/test-framework-registry.md
        ```

        **Run Detection Engine** (4-priority system):

        **Priority 1: Explicit Markers**
        - Read tasks.md → search for patterns:
          * "Test Framework: Jest"
          * "Test Framework: Playwright, Cypress"
          * "Test Framework: Maestro (iOS/Android), XCUITest (iOS)"
        - Read plan.md → section "Testing Strategy" or "Test Frameworks"
        - Parse comma-separated lists

        **Priority 2: Project Structure**
        - Scan for existing framework configs:
          * jest.config.js, jest.config.ts
          * pytest.ini, pyproject.toml
          * playwright.config.ts
          * .maestro/, .detoxrc.js
          * go.mod (go test), Cargo.toml (cargo test)
        - Check dependencies in package.json/pyproject.toml/build.gradle.kts
        - If framework already configured → keep it (verify only)

        **Priority 3: Constitution.md**
        - Extract: language, platform (web/mobile/desktop), tech_stack
        - Examples:
          * language=typescript, platform=web, tech_stack=react → Jest (90) + Playwright (95)
          * language=typescript, platform=web, tech_stack=vite → Vitest (95) + Playwright (95)
          * language=python, platform=web, tech_stack=fastapi → pytest (95) + Playwright (95)
          * language=swift, platform=ios → XCTest (85) + XCUITest (95)
          * language=kotlin, platform=android → JUnit5 (90) + Espresso (95)
          * language=dart, platform=mobile, tech_stack=flutter → flutter_test (95)
          * language=go, platform=backend → go-test (100) + httptest (95)
          * language=rust, platform=any → cargo-test (100)

        **Priority 4: Best Practice Defaults**
        - IF no unit framework specified:
          * JavaScript/TypeScript + Vite → Vitest (priority 95)
          * JavaScript/TypeScript + other → Jest (priority 90)
          * Python → pytest (priority 95)
          * Go → go-test (priority 100, built-in)
          * Rust → cargo-test (priority 100, built-in)
          * Java/Kotlin → JUnit5 (priority 90)
          * Swift → XCTest (priority 85, built-in)
          * Ruby → RSpec (priority 90)
          * C#/F# → xUnit (priority 85)

        - IF web platform AND no E2E framework:
          * Default → Playwright (priority 95)

        - IF mobile platform AND no E2E framework:
          * iOS → XCUITest (priority 95, requires Xcode)
          * Android → Espresso (priority 95, requires Android SDK)
          * React Native → Maestro (priority 90) or Detox (priority 90)
          * Flutter → flutter_test (priority 95, built-in)

        - IF has API endpoints (detect routes/controllers) AND no API test framework:
          * Node.js → Supertest (priority 90)
          * Python → requests-mock (priority 85)
          * Java/Kotlin → REST Assured (priority 90)
          * Go → httptest (priority 95, built-in)

        **Output: Test Strategy**
        ```json
        {
          "unit": ["jest"],
          "integration": ["jest"],
          "e2e_web": ["playwright"],
          "e2e_mobile": ["maestro", "xcuitest"],
          "api": ["supertest"],
          "performance": [],
          "visual": [],
          "contract": []
        }
        ```

        ### Step 2: Install Missing Frameworks (Universal Loop)

        FOR EACH category IN test_strategy:
          FOR EACH framework_id IN category:

            # Load framework metadata from registry
            framework = REGISTRY.get(framework_id)

            # Check if already installed (run verification command)
            is_installed = false
            FOR EACH verification IN framework.verification:
              TRY:
                result = run(verification.command, timeout=10)
                IF result.returncode == verification.expected_exit_code:
                  is_installed = true
                  BREAK
              CATCH:
                CONTINUE

            IF is_installed:
              LOG: "✅ {framework.name} already installed"
              CONTINUE

            LOG: "📦 Installing {framework.name} for {category} testing..."

            # Detect package manager
            package_manager = detect_package_manager()
            # npm/yarn/pnpm for Node
            # pip/poetry for Python
            # cargo for Rust
            # go for Go
            # gradle/maven for JVM
            # etc.

            # Check prerequisites (platform-specific)
            IF framework.prerequisites:
              FOR EACH prereq IN framework.prerequisites:
                IF NOT check_prerequisite(prereq):
                  ERROR: "{framework.name} requires {prereq}"
                  LOG: "⚠️  Cannot auto-install {framework.name}"
                  LOG: "Manual steps: {framework.installation.manual_steps}"
                  # Don't block entirely - continue to next framework
                  CONTINUE TO NEXT FRAMEWORK

            # Get installation command for detected package manager
            install_config = framework.installation.get(package_manager)

            IF NOT install_config:
              ERROR: "No installation method for {package_manager}"
              LOG: "Supported: {framework.installation.keys()}"
              CONTINUE TO NEXT FRAMEWORK

            # Execute installation
            TRY:
              run(install_config.command, timeout=120)

              # Run config generator if specified
              IF install_config.config_gen:
                run(install_config.config_gen, timeout=30)

              # Apply configuration template if specified
              IF framework.configuration.template:
                copy_template(
                  src=framework.configuration.template,
                  dest=framework.configuration.required_files[0]
                )

            CATCH Exception as e:
              ERROR: "❌ Failed to install {framework.name}: {e}"
              LOG: "Manual installation:"
              LOG: "  Command: {install_config.command}"
              IF framework.installation.manual_steps:
                LOG: "  Steps: {framework.installation.manual_steps}"
              LOG: "  Docs: {framework.docs_url}"
              # Continue to next framework (don't block entirely)
              CONTINUE TO NEXT FRAMEWORK

            # Verify installation
            verified = false
            FOR EACH verification IN framework.verification:
              TRY:
                result = run(verification.command, timeout=10, capture_output=true)

                # Check exit code
                IF result.returncode != verification.expected_exit_code:
                  RAISE VerificationError()

                # Check output if specified
                IF verification.expected_output_contains:
                  FOR EACH expected IN verification.expected_output_contains:
                    IF expected NOT IN result.stdout:
                      RAISE VerificationError()

                verified = true
                LOG: "✅ {framework.name} verified successfully"
                BREAK

              CATCH VerificationError:
                ERROR: "⚠️  {framework.name} installed but verification failed"
                LOG: "Verification command: {verification.command}"
                LOG: "Expected exit code: {verification.expected_exit_code}"

            IF NOT verified:
              LOG: "⚠️  {framework.name} installation uncertain - manual verification recommended"

        ### Step 3: Generate test-strategy.json

        Create .speckit/test-strategy.json:
        ```json
        {
          "generated_at": "<ISO8601 timestamp>",
          "detected_by": "framework-installer",
          "project_info": {
            "language": "<detected-language>",
            "platform": "<detected-platform>",
            "tech_stack": "<detected-stack>"
          },
          "test_strategy": {
            "unit": ["<framework-ids>"],
            "integration": ["<framework-ids>"],
            "e2e_web": ["<framework-ids>"],
            "e2e_mobile": ["<framework-ids>"],
            "e2e_desktop": [],
            "api": ["<framework-ids>"],
            "performance": [],
            "visual": [],
            "contract": []
          },
          "installed_frameworks": {
            "<framework-id>": {
              "version": "<detected-version>",
              "installed_at": "<ISO8601 timestamp>",
              "verified": true|false
            }
          }
        }
        ```

        ### Step 4: Re-validate QG-TEST-002

        Run QG-TEST-002 validation for each installed framework:

        **Unit/Integration frameworks:**
        - Jest: `npm test -- --passWithNoTests`
        - Vitest: `npx vitest --run --reporter=verbose --passWithNoTests`
        - pytest: `pytest --collect-only`
        - go-test: `go test ./... -count=0`
        - cargo-test: `cargo test --no-run`
        - JUnit5: `./gradlew test --dry-run` OR `mvn test -DskipTests`
        - XCTest: `xcodebuild test -scheme <scheme> -destination 'platform=iOS Simulator' -dry-run`

        **E2E Web frameworks:**
        - Playwright: `npx playwright --version`
        - Cypress: `npx cypress --version`
        - Selenium: `node -e "require('selenium-webdriver')"`

        **E2E Mobile frameworks:**
        - Maestro: `maestro --version`
        - XCUITest: `xcodebuild -list | grep -i test`
        - Espresso: `./gradlew tasks | grep connectedAndroidTest`
        - Detox: `npx detox --version`
        - flutter_test: `flutter test --version`

        **API frameworks:**
        - Supertest: `npm list supertest`
        - REST Assured: `./gradlew dependencies | grep rest-assured`
        - httptest: `go doc net/http/httptest`

        IF all validation commands pass:
          RETURN {status: "SUCCESS", message: "QG-TEST-002 now passes"}

        IF any critical framework (unit, integration) fails validation:
          RETURN {
            status: "FAILED",
            message: "Critical frameworks failed validation",
            failed_frameworks: [<list>]
          }

        IF only optional frameworks fail:
          RETURN {
            status: "PARTIAL",
            message: "Some optional frameworks failed, but continuing",
            failed_frameworks: [<list>]
          }

        ### Step 5: Output Summary

        ```
        ╔══════════════════════════════════════════════════════════════╗
        ║           Test Framework Installation Summary               ║
        ╠══════════════════════════════════════════════════════════════╣
        ║ Unit Testing:         ✅ Jest v29.7.0                       ║
        ║ Integration Testing:  ✅ Jest v29.7.0                       ║
        ║ E2E Web Testing:      ✅ Playwright v1.40.0                 ║
        ║ E2E Mobile Testing:   ✅ Maestro v1.36.0                    ║
        ║                       ⚠️  XCUITest (requires manual setup)  ║
        ║ API Testing:          ✅ Supertest v6.3.3                   ║
        ╠══════════════════════════════════════════════════════════════╣
        ║ QG-TEST-002 Status:   ✅ PASS                               ║
        ║ Ready for Wave 2:     ✅ YES                                ║
        ╚══════════════════════════════════════════════════════════════╝
        ```

        ## Platform-Specific Handling

        **XCUITest (iOS):**
        - Requires: macOS + Xcode
        - Check: `xcodebuild -version`
        - Cannot auto-install Xcode
        - Manual steps: Install from App Store
        - Graceful degradation: Continue without iOS E2E tests

        **Espresso (Android):**
        - Requires: Android SDK + $ANDROID_HOME
        - Check: `echo $ANDROID_HOME && adb --version`
        - Cannot auto-install SDK
        - Manual steps: Install Android Studio
        - Graceful degradation: Continue without Android E2E tests

        **Maestro (Cross-platform):**
        - Network installation: `curl -Ls "https://get.maestro.mobile.dev" | bash`
        - Add to PATH: `export PATH=$PATH:$HOME/.maestro/bin`

        **Flutter test:**
        - Requires: Flutter SDK
        - Check: `flutter --version`
        - Cannot auto-install Flutter
        - Manual steps: Install from flutter.dev

        **Built-in frameworks (no installation):**
        - go-test (Go stdlib)
        - cargo-test (Rust toolchain)
        - unittest (Python stdlib)
        - httptest (Go stdlib)
        - XCTest (Xcode)

        ## Success Criteria
        - All critical frameworks (unit, integration) installed and verified
        - Optional frameworks (e2e, api) installed when possible
        - QG-TEST-002 re-validation passes
        - .speckit/test-strategy.json generated
        - Ready for Wave 2 (Test Scaffolding)

        ## On Failure (Universal Error Handling)

        ```
        ❌ Auto-installation failed for {framework.name}

        Category: {framework.category}
        Languages: {", ".join(framework.languages)}
        Platforms: {", ".join(framework.platforms)}

        Attempted command:
          {install_config.command}

        Error:
          {error_message}

        Manual installation steps:
          1. {framework.installation.manual_steps or "See official docs"}
          2. Verify: {framework.verification[0].command}
          3. Re-run /speckit.implement

        Alternative frameworks:
          {", ".join(framework.alternative_to)}

        Documentation:
          {framework.docs_url}

        To skip auto-framework installation:
          /speckit.implement --no-auto-framework
        ```

        **Exit Codes:**
        - Exit 0: All critical frameworks installed successfully
        - Exit 1: Critical framework (unit/integration) failed installation
        - Exit 0 with warnings: Optional frameworks failed but can continue

    # Wave 1: Infrastructure (no deps)
    - role: project-scaffolder
      role_group: INFRA
      parallel: true
      depends_on: []
      priority: 10
      trigger: "during setup phase"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Plan: {{FEATURE_DIR}}/plan.md

        ## Task
        Create project structure per plan.md:
        1. Create all directories specified in the plan
        2. Generate .gitignore with language-specific patterns
        3. Create base config files (tsconfig.json, pyproject.toml, etc.)
        4. Set up folder structure matching the architecture

        ## Success Criteria
        - All directories from plan exist
        - Config files are valid JSON/YAML (parseable)
        - .gitignore includes node_modules, __pycache__, .env, etc.
      model_override: haiku
    - role: dependency-installer
      role_group: INFRA
      parallel: true
      depends_on: [project-scaffolder]
      priority: 9
      trigger: "after project structure exists"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Plan: {{FEATURE_DIR}}/plan.md
        Tasks: {{FEATURE_DIR}}/tasks.md
        Constitution: memory/constitution.md
        Dependency Registry: memory/domains/dependency-registry.md
        Test Framework Registry: memory/domains/test-framework-registry.md

        ## Task
        Universal test framework detection and installation for all project types,
        followed by regular dependency installation.

        ### PART 1: Test Framework Installation (Universal)

        ## Step 1: Load Test Framework Registry

        Read: memory/domains/test-framework-registry.md

        This registry contains metadata for ALL supported test frameworks:
        - Unit/Integration: Jest, Vitest, pytest, Go test, cargo test, JUnit5, TestNG, RSpec, xUnit, NUnit, Mocha, unittest
        - E2E Web: Playwright, Cypress, Selenium, Puppeteer, WebdriverIO
        - E2E Mobile: Maestro, XCUITest, Espresso, Detox, Flutter test, Appium, XCTest
        - E2E Desktop: Tauri test, Spectron, WebdriverIO Electron
        - API Testing: Supertest, REST Assured, Newman, requests-mock, httptest
        - Performance: k6, Artillery, Locust, JMeter
        - Visual Regression: Percy, Chromatic, BackstopJS, Playwright Visual
        - Contract Testing: Pact, Spring Cloud Contract

        ## Step 2: Detect Test Strategy (4-Priority Detection Engine)

        Run detection engine to determine which test frameworks are needed for this project.

        ### Priority 1: Explicit Markers (Highest Priority)

        Read tasks.md → look for "Test Framework: {name}" patterns:
        - Single framework: "Test Framework: Jest"
        - Multiple frameworks: "Test Framework: Jest, Playwright, Supertest"
        - Platform-specific: "Test Framework: Maestro (iOS/Android), XCUITest (iOS), Espresso (Android)"

        Read plan.md → section "Testing Strategy" or "Test Frameworks"
        - Parse any explicit framework mentions
        - Look for patterns like "We will use {framework} for testing"

        Parse comma-separated lists into framework names.

        ### Priority 2: Project Structure Analysis

        Scan for existing framework configurations:

        **JavaScript/TypeScript:**
        - jest.config.js, jest.config.ts, package.json contains "jest" → Jest
        - vitest.config.ts, vite.config.ts exists → Vitest
        - playwright.config.ts, package.json contains "@playwright/test" → Playwright
        - cypress.config.ts, package.json contains "cypress" → Cypress
        - .mocharc.json, package.json contains "mocha" → Mocha
        - package.json contains "supertest" → Supertest
        - .detoxrc.js, package.json contains "detox" → Detox

        **Python:**
        - pytest.ini, pyproject.toml contains "[tool.pytest" → pytest
        - requirements.txt contains "pytest" → pytest
        - requirements.txt contains "requests-mock" → requests-mock

        **Go:**
        - go.mod exists → go-test (built-in)
        - Any *_test.go files → go-test

        **Rust:**
        - Cargo.toml exists → cargo-test (built-in)

        **Java/Kotlin:**
        - build.gradle.kts contains "junit-jupiter" → JUnit5
        - build.gradle.kts contains "testng" → TestNG
        - build.gradle.kts contains "rest-assured" → REST Assured
        - build.gradle.kts contains "espresso-core" → Espresso

        **Swift:**
        - *.xcodeproj exists → XCTest (built-in)

        **Flutter:**
        - pubspec.yaml contains "flutter_test" → flutter_test (built-in)
        - pubspec.yaml contains "integration_test" → flutter_test

        **Mobile:**
        - .maestro/ directory exists → Maestro

        IF framework config detected → Mark as "existing" (verify only, don't reinstall)

        ### Priority 3: Constitution.md Context

        Read memory/constitution.md and extract:
        - language (javascript, typescript, python, go, rust, java, kotlin, swift, dart, ruby, csharp)
        - platform (web, mobile, desktop, backend, fullstack, cli)
        - tech_stack (react, vue, angular, vite, next, nest, fastapi, django, flask, spring, etc.)

        Map to frameworks:

        **Web Projects:**
        - language=typescript, tech_stack=vite → Vitest (95) + Playwright (95)
        - language=typescript, tech_stack=react → Jest (90) + Playwright (95)
        - language=typescript, tech_stack=next → Jest (90) + Playwright (95)
        - language=python, tech_stack=fastapi → pytest (95) + Playwright (95)
        - language=python, tech_stack=django → pytest (95) + Playwright (95)

        **Mobile Projects:**
        - language=swift, platform=ios → XCTest (85) + XCUITest (95)
        - language=kotlin, platform=android → JUnit5 (90) + Espresso (95)
        - language=dart, tech_stack=flutter → flutter_test (95)
        - language=typescript, tech_stack=react-native → Jest (90) + Maestro (90) + Detox (90)

        **Backend Projects:**
        - language=go, platform=backend → go-test (100) + httptest (95)
        - language=rust, platform=backend → cargo-test (100)
        - language=java, tech_stack=spring → JUnit5 (90) + REST Assured (90)
        - language=python, platform=backend → pytest (95) + requests-mock (85)

        **Desktop Projects:**
        - tech_stack=tauri → Tauri test (90) + cargo-test (100)
        - tech_stack=electron → Spectron (80) OR WebdriverIO Electron (85)

        ### Priority 4: Best Practice Defaults

        IF no unit/integration framework specified after Priority 1-3:

        **By Language:**
        - JavaScript/TypeScript (no Vite) → Jest (90)
        - JavaScript/TypeScript + Vite detected → Vitest (95)
        - Python → pytest (95)
        - Go → go-test (100)
        - Rust → cargo-test (100)
        - Java/Kotlin → JUnit5 (90)
        - Swift → XCTest (85)
        - Ruby → RSpec (90)
        - C#/F# → xUnit (85)

        **By Platform:**

        IF platform=web AND no E2E framework:
        → Playwright (95)

        IF platform=mobile AND no E2E framework:
        - iOS → XCUITest (95)
        - Android → Espresso (95)
        - React Native → Maestro (90)
        - Flutter → flutter_test (95)

        IF platform=desktop AND no E2E framework:
        - Tauri → Tauri test (90)
        - Electron → WebdriverIO Electron (85)

        IF has_api_endpoints AND no API framework:
        (Detect: routes/, controllers/, api/, server.ts, app.py patterns)
        - Node.js → Supertest (90)
        - Python → requests-mock (85)
        - Java/Kotlin → REST Assured (90)
        - Go → httptest (95)

        ### Prioritize Frameworks (When Multiple Candidates)

        IF multiple frameworks fit the same category:
        - Sort by priority field (higher = better)
        - Select framework(s) with highest priority

        Example: TypeScript + Vite project
        - Candidates: Vitest (95), Jest (90)
        - Winner: Vitest (higher priority)

        ### Output: Test Strategy

        Generate test strategy structure:
        ```json
        {
          "unit": ["jest"],
          "integration": ["jest"],
          "e2e_web": ["playwright"],
          "e2e_mobile": ["maestro", "xcuitest"],
          "e2e_desktop": [],
          "api": ["supertest"],
          "performance": [],
          "visual": [],
          "contract": []
        }
        ```

        ## Step 3: Install Frameworks by Category

        FOR EACH category IN [unit, integration, e2e_web, e2e_mobile, e2e_desktop, api, performance, visual, contract]:

          frameworks = test_strategy[category]

          IF frameworks is empty:
            CONTINUE

          FOR EACH framework_id IN frameworks:

            # Load framework metadata from registry
            framework = REGISTRY.get(framework_id)

            IF framework NOT FOUND:
              ERROR: "Framework {framework_id} not in registry"
              CONTINUE

            LOG: "📦 Processing {framework.name} for {category} testing..."

            # Check if already installed (Priority 2 detected it)
            IF framework marked as "existing":
              # Verify it works
              FOR EACH verification IN framework.verification:
                TRY:
                  result = run(verification.command, timeout=10)
                  IF result.returncode == verification.expected_exit_code:
                    LOG: "✅ {framework.name} already installed and verified"
                    installed_frameworks[framework_id] = {
                      "version": extract_version(result.stdout),
                      "verified": true,
                      "source": "existing"
                    }
                    CONTINUE TO NEXT FRAMEWORK
                CATCH:
                  WARN: "⚠️ {framework.name} config exists but verification failed"
                  # Fall through to installation

            # Check prerequisites (platform-specific)
            IF framework.prerequisites:
              FOR EACH prereq IN framework.prerequisites:
                TRY:
                  check_prerequisite(prereq)
                CATCH:
                  ERROR: "❌ {framework.name} requires {prereq}"
                  LOG: "Cannot auto-install {framework.name}"
                  IF framework.installation.manual_steps:
                    LOG: "Manual steps: {framework.installation.manual_steps}"
                  LOG: "Docs: {framework.docs_url}"

                  # Critical vs Optional handling
                  IF category IN ["unit", "integration"]:
                    ERROR: "CRITICAL: Unit/integration framework missing"
                    BLOCK_WAVE_2 = true
                  ELSE:
                    WARN: "Optional framework skipped: {framework.name}"

                  CONTINUE TO NEXT FRAMEWORK

            # Detect package manager
            package_manager = detect_package_manager()
            # npm (package.json + package-lock.json)
            # yarn (package.json + yarn.lock)
            # pnpm (package.json + pnpm-lock.yaml)
            # pip (requirements.txt)
            # poetry (pyproject.toml + poetry.lock)
            # cargo (Cargo.toml)
            # go (go.mod)
            # gradle (build.gradle.kts)
            # maven (pom.xml)

            # Get installation command for package manager
            install_config = framework.installation.get(package_manager)

            IF NOT install_config:
              ERROR: "No installation method for {package_manager}"
              LOG: "Supported: {framework.installation.keys()}"
              LOG: "Manual install: see {framework.docs_url}"
              CONTINUE TO NEXT FRAMEWORK

            # Execute installation
            LOG: "⏳ Installing {framework.name}..."
            LOG: "Command: {install_config.command}"

            TRY:
              run(install_config.command, timeout=120)

              # Run config generator if specified
              IF install_config.config_gen:
                LOG: "⚙️  Generating config..."
                run(install_config.config_gen, timeout=30)

              # Apply configuration template if specified
              IF framework.configuration.template:
                LOG: "📝 Applying config template..."
                copy_template(
                  src=framework.configuration.template,
                  dest=framework.configuration.required_files[0]
                )

            CATCH Exception as e:
              ERROR: "❌ Failed to install {framework.name}: {e}"
              LOG: "Attempted: {install_config.command}"
              IF framework.installation.manual_steps:
                LOG: "Manual steps: {framework.installation.manual_steps}"
              LOG: "Docs: {framework.docs_url}"

              # Critical vs Optional handling
              IF category IN ["unit", "integration"]:
                ERROR: "CRITICAL: Unit/integration framework installation failed"
                BLOCK_WAVE_2 = true
              ELSE:
                WARN: "Optional framework installation failed: {framework.name}"

              CONTINUE TO NEXT FRAMEWORK

            # Verify installation
            verified = false
            version = "unknown"

            FOR EACH verification IN framework.verification:
              TRY:
                result = run(verification.command, timeout=10, capture_output=true)

                # Check exit code
                IF result.returncode != verification.expected_exit_code:
                  CONTINUE

                # Check output if specified
                IF verification.expected_output_contains:
                  FOR EACH expected IN verification.expected_output_contains:
                    IF expected NOT IN result.stdout:
                      CONTINUE

                # Success
                verified = true
                version = extract_version(result.stdout)
                LOG: "✅ {framework.name} v{version} verified"

                installed_frameworks[framework_id] = {
                  "version": version,
                  "verified": true,
                  "source": "installed"
                }

                BREAK

              CATCH:
                CONTINUE

            IF NOT verified:
              WARN: "⚠️ {framework.name} installed but verification uncertain"
              installed_frameworks[framework_id] = {
                "version": "unknown",
                "verified": false,
                "source": "installed"
              }

        ## Step 4: Generate test-strategy.json

        Create .speckit/test-strategy.json:
        ```json
        {
          "generated_at": "<ISO8601 timestamp>",
          "detected_by": "dependency-installer",
          "project_info": {
            "language": "<from constitution>",
            "platform": "<from constitution>",
            "tech_stack": "<from constitution>"
          },
          "test_strategy": {
            "unit": ["<framework-ids>"],
            "integration": ["<framework-ids>"],
            "e2e_web": ["<framework-ids>"],
            "e2e_mobile": ["<framework-ids>"],
            "e2e_desktop": ["<framework-ids>"],
            "api": ["<framework-ids>"],
            "performance": ["<framework-ids>"],
            "visual": ["<framework-ids>"],
            "contract": ["<framework-ids>"]
          },
          "installed_frameworks": {
            "<framework-id>": {
              "version": "<version>",
              "installed_at": "<ISO8601>",
              "verified": true|false,
              "source": "existing"|"installed"
            }
          },
          "blocked": false|true,
          "block_reason": "<reason if blocked>"
        }
        ```

        ## Step 5: Verify QG-TEST-002

        Run simplified test command for each installed framework:

        **Unit/Integration:**
        - Jest: `npm test -- --passWithNoTests`
        - Vitest: `npx vitest --run --passWithNoTests`
        - pytest: `pytest --collect-only`
        - go-test: `go test ./... -count=0`
        - cargo-test: `cargo test --no-run`
        - JUnit5: `./gradlew test --dry-run` OR `mvn test -DskipTests`
        - RSpec: `rspec --dry-run`
        - XCTest: `xcodebuild test -scheme <app> -destination 'platform=iOS Simulator' -dry-run`

        **E2E Web:**
        - Playwright: `npx playwright --version` (already verified in Step 3)
        - Cypress: `npx cypress --version`
        - Selenium: verified in Step 3

        **E2E Mobile:**
        - Maestro: `maestro --version` (already verified)
        - XCUITest: `xcodebuild -list | grep -i test`
        - Espresso: `./gradlew tasks | grep connectedAndroidTest`
        - Detox: `npx detox --version`
        - flutter_test: `flutter test --version`

        **API:**
        - Supertest: `npm list supertest`
        - REST Assured: `./gradlew dependencies | grep rest-assured`
        - httptest: `go doc net/http/httptest`

        IF any CRITICAL framework (unit, integration) verification fails:
          ERROR: "QG-TEST-002 failed: {framework} not properly configured"
          SET test-strategy.json blocked=true
          BLOCK Wave 2

        IF only optional framework verification fails:
          WARN: "Optional framework verification failed: {framework}"
          Continue (don't block)

        ### PART 2: Regular Dependencies

        ## Step 6: Install Production & Dev Dependencies

        Read plan.md → extract dependencies:
        - Production dependencies (runtime libraries, frameworks)
        - Dev dependencies (linting, formatting, types, build tools)

        Read memory/domains/dependency-registry.md for library-specific guidance.

        **For Node.js:**
        ```bash
        npm install <prod-deps>
        npm install -D <dev-deps>
        npm install -D typescript @types/node
        npm install -D eslint prettier
        ```

        **For Python:**
        ```bash
        pip install <prod-deps>
        pip install <dev-deps>
        pip install black mypy ruff
        ```

        **For Go:**
        ```bash
        go get <dependencies>
        go mod tidy
        ```

        **For Rust:**
        ```bash
        cargo add <dependencies>
        cargo add --dev <dev-dependencies>
        ```

        **For Java/Kotlin:**
        Update build.gradle.kts with dependencies from plan.md

        ## Step 7: Generate Lock Files

        **Node.js:**
        - package-lock.json (npm)
        - yarn.lock (yarn)
        - pnpm-lock.yaml (pnpm)

        **Python:**
        - poetry.lock (poetry lock)
        - pip: requirements.txt already is the lock

        **Go:**
        - go.sum (auto-generated by go mod tidy)

        **Rust:**
        - Cargo.lock (auto-generated by cargo build)

        ## Success Criteria

        **Test Frameworks:**
        - All frameworks from test_strategy installed successfully
        - Critical frameworks (unit, integration) verified
        - test-strategy.json generated
        - QG-TEST-002 validation passes for critical frameworks

        **Regular Dependencies:**
        - All production dependencies installed without conflicts
        - All dev dependencies installed
        - Lock file generated (package-lock.json, poetry.lock, go.sum, Cargo.lock)
        - No critical security vulnerabilities in dependencies

        ## On Failure

        **Critical Framework Failure:**
        ```
        ❌ BLOCKING: Critical test framework installation failed

        Framework: {framework.name}
        Category: {category}
        Error: {error_message}

        Attempted: {install_config.command}

        Manual installation:
        1. {framework.installation.manual_steps}
        2. Verify: {framework.verification[0].command}
        3. Re-run /speckit.implement

        Alternatives:
        {", ".join(framework.alternative_to)}

        Documentation: {framework.docs_url}

        BLOCKED: Cannot proceed to Wave 2 (Test Scaffolding) without {category} framework.
        ```

        **Optional Framework Failure:**
        ```
        ⚠️ WARNING: Optional test framework installation failed

        Framework: {framework.name}
        Category: {category}
        Error: {error_message}

        Continuing with available frameworks.
        To install manually: see {framework.docs_url}
        ```

        **Dependency Conflict:**
        ```
        ❌ Dependency installation failed: {error}

        Check:
        1. Package versions in plan.md
        2. Compatibility with existing dependencies
        3. Lock file conflicts

        Try:
        - Remove lock file and reinstall
        - Update conflicting packages
        - Check dependency-registry.md for known issues
        ```

      model_override: haiku
    # Wave 2: Test Scaffolding - TDD Red Phase (create failing tests FIRST)
    - role: test-scaffolder
      role_group: TESTING
      parallel: true
      depends_on: [staging-validator, dependency-installer]
      priority: 9
      trigger: "after dependencies installed, before implementation"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        Tasks: {{FEATURE_DIR}}/tasks.md
        Staging Config: .speckit/staging/test-config.env
        Test Framework Registry: memory/domains/test-framework-registry.md
        Test Strategy: .speckit/test-strategy.json

        ## ⚠️ CRITICAL: Framework Pre-Check (Universal)

        Before creating tests, verify ALL required frameworks are installed.

        ### Step 1: Load Test Strategy

        Read: .speckit/test-strategy.json (generated by dependency-installer)

        IF file does not exist:
          ERROR: "test-strategy.json missing - dependency-installer didn't run"
          BLOCK

        Extract test_strategy object from JSON.

        ### Step 2: Verify Frameworks for Unit/Integration Testing

        **Required categories for this scaffolder:**
        - "unit"
        - "integration"

        required_frameworks = test_strategy["unit"] + test_strategy["integration"]

        IF required_frameworks is empty:
          ERROR: "No unit/integration frameworks specified in test strategy"
          LOG: "Expected frameworks detected during dependency installation"
          BLOCK

        ### Step 3: Run Verification Commands (Registry-Driven)

        Read: memory/domains/test-framework-registry.md

        missing_frameworks = []

        FOR EACH framework_id IN required_frameworks:
          # Load framework metadata from registry
          framework = REGISTRY.get(framework_id)

          IF framework NOT FOUND:
            ERROR: "Framework {framework_id} not in registry"
            missing_frameworks.append(framework_id)
            CONTINUE

          LOG: "🔍 Verifying {framework.name}..."

          # Run verification commands
          verified = false

          FOR EACH verification IN framework.verification:
            TRY:
              result = run(verification.command, timeout=10, capture_output=true)

              IF result.returncode == verification.expected_exit_code:
                # Check output if specified
                IF verification.expected_output_contains:
                  all_found = true
                  FOR EACH expected IN verification.expected_output_contains:
                    IF expected NOT IN result.stdout:
                      all_found = false
                      BREAK
                  IF all_found:
                    verified = true
                    BREAK
                ELSE:
                  verified = true
                  BREAK

            CATCH Exception as e:
              CONTINUE

          IF verified:
            LOG: "✅ {framework.name} verified"
          ELSE:
            ERROR: "❌ {framework.name} verification failed"
            missing_frameworks.append(framework)

        ### Step 4: Auto-Remediation on Missing Framework

        IF missing_frameworks:
          LOG: "🔧 Attempting automatic installation of missing frameworks..."

          # This scaffolder is in Wave 2, so if frameworks are missing here,
          # it means both Wave 0 pre-gate AND Wave 1 dependency-installer failed.
          # This is the LAST RESORT attempt.

          FOR EACH framework IN missing_frameworks:
            LOG: "⚠️  Last resort installation attempt for {framework.name}..."

            # Detect package manager
            package_manager = detect_package_manager()

            # Get installation config
            install_config = framework.installation.get(package_manager)

            IF NOT install_config:
              ERROR: "Cannot auto-install {framework.name} - no method for {package_manager}"
              CONTINUE

            # Check prerequisites
            IF framework.prerequisites:
              prereq_met = true
              FOR EACH prereq IN framework.prerequisites:
                IF NOT check_prerequisite(prereq):
                  ERROR: "{framework.name} requires {prereq}"
                  prereq_met = false
                  BREAK

              IF NOT prereq_met:
                LOG: "Manual installation required:"
                LOG: "  {framework.installation.manual_steps}"
                LOG: "  Docs: {framework.docs_url}"
                CONTINUE

            # Attempt installation
            TRY:
              LOG: "Running: {install_config.command}"
              run(install_config.command, timeout=120)

              # Config generation
              IF install_config.config_gen:
                run(install_config.config_gen, timeout=30)

              # Verify
              FOR EACH verification IN framework.verification:
                result = run(verification.command, timeout=10)
                IF result.returncode == verification.expected_exit_code:
                  LOG: "✅ {framework.name} installed successfully"
                  # Remove from missing list
                  missing_frameworks.remove(framework)
                  BREAK

            CATCH Exception as e:
              ERROR: "Failed to install {framework.name}: {e}"

        ### Step 5: Final Check - Block if Still Missing

        IF missing_frameworks:
          ERROR_MESSAGE = """
╔═══════════════════════════════════════════════════════════════╗
║  ❌ Test Framework Missing for UNIT/INTEGRATION Testing      ║
╠═══════════════════════════════════════════════════════════════╣
║ Required frameworks: {required_frameworks}                    ║
║ Missing: {[f.name for f in missing_frameworks]}               ║
╠═══════════════════════════════════════════════════════════════╣
║ BLOCKED: Cannot create tests without framework                ║
║                                                                ║
║ This means:                                                    ║
║ 1. Wave 0 pre-gate (IG-IMPL-005) failed or was skipped        ║
║ 2. Wave 1 dependency-installer failed to install              ║
║ 3. Wave 2 last-resort installation also failed                ║
║                                                                ║
║ Options:                                                       ║
║ 1. Install manually:                                          ║
          """

          FOR EACH framework IN missing_frameworks:
            ERROR_MESSAGE += f"""
║    {framework.name}:                                           ║
║      Command: {framework.installation[package_manager].command}║
║      Verify: {framework.verification[0].command}               ║
║      Docs: {framework.docs_url}                                ║
          """

          ERROR_MESSAGE += """
║                                                                ║
║ 2. Re-run with auto-install:                                  ║
║    /speckit.implement                                         ║
║    (remove --no-auto-framework if present)                    ║
║                                                                ║
║ 3. Alternative frameworks:                                     ║
          """

          FOR EACH framework IN missing_frameworks:
            IF framework.alternative_to:
              ERROR_MESSAGE += f"""
║    Instead of {framework.name}: {", ".join(framework.alternative_to)}║
          """

          ERROR_MESSAGE += """
╚═══════════════════════════════════════════════════════════════╝
          """

          PRINT ERROR_MESSAGE
          EXIT(1)  # BLOCK

        LOG: "✅ All unit/integration frameworks verified - proceeding to test creation"

        ---

        ## Task - TDD RED PHASE
        Create failing test scaffolds BEFORE implementation:
        1. Read tasks.md for all [TEST:AS-xxx] markers
        2. Create test files with proper structure but failing assertions
        3. Configure test framework to use staging database (port 5433)
        4. Run tests - they MUST FAIL (validates TDD approach)

        ## Test File Structure
        For each AS-xxx with "Requires Test = YES":
        1. Create test file at path from tasks.md
        2. Add describe/it blocks matching AS Given/When/Then
        3. Add @speckit:AS-xxx annotation for traceability
        4. Write assertions that WILL FAIL until implementation

        ## Success Criteria (QG-TEST-003)
        - All AS-xxx with tests have corresponding test files
        - Test command runs successfully (npm test / pytest)
        - 100% of new tests FAIL (TDD red phase verified)
        - Tests connect to staging database correctly

        ## Output
        - Test files created in tests/ directory
        - Test run summary: X tests, X failures (expected)
        - QG-TEST-003: PASSED (tests fail as expected)
      model_override: sonnet
    - role: e2e-test-scaffolder
      role_group: TESTING
      parallel: true
      depends_on: [staging-validator, dependency-installer]
      priority: 9
      trigger: "when feature has e2e/playwright tests"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        Tasks: {{FEATURE_DIR}}/tasks.md
        Playwright Container: speckit-playwright
        Test Framework Registry: memory/domains/test-framework-registry.md
        Test Strategy: .speckit/test-strategy.json

        ## ⚠️ CRITICAL: Framework Pre-Check (Universal)

        Before creating E2E tests, verify required frameworks are installed.

        ### Step 1: Load Test Strategy

        Read: .speckit/test-strategy.json

        IF file does not exist:
          WARN: "test-strategy.json missing - detecting E2E frameworks manually"
          # Fallback detection
          required_frameworks = detect_e2e_frameworks_from_tasks()

        ELSE:
          required_frameworks = test_strategy["e2e_web"]

        ### Step 2: Check if E2E Web Tests Needed

        IF required_frameworks is empty:
          LOG: "⚠️  No E2E web frameworks specified in test strategy"
          LOG: "Checking tasks.md for E2E test requirements..."

          # Check if tasks.md mentions e2e, playwright, cypress, selenium
          has_e2e_tests = check_tasks_for_e2e_markers()

          IF NOT has_e2e_tests:
            LOG: "No E2E web tests required - skipping E2E test scaffolding"
            EXIT(0)  # Graceful skip

          ELSE:
            WARN: "E2E tests mentioned in tasks.md but no framework in strategy"
            LOG: "Defaulting to Playwright (best practice)"
            required_frameworks = ["playwright"]

        ### Step 3: Run Verification Commands

        Read: memory/domains/test-framework-registry.md

        missing_frameworks = []

        FOR EACH framework_id IN required_frameworks:
          framework = REGISTRY.get(framework_id)

          IF NOT framework:
            missing_frameworks.append(framework_id)
            CONTINUE

          LOG: "🔍 Verifying {framework.name} for E2E web testing..."

          verified = false
          FOR EACH verification IN framework.verification:
            TRY:
              result = run(verification.command, timeout=10)
              IF result.returncode == verification.expected_exit_code:
                verified = true
                LOG: "✅ {framework.name} verified"
                BREAK
            CATCH:
              CONTINUE

          IF NOT verified:
            ERROR: "❌ {framework.name} verification failed"
            missing_frameworks.append(framework)

        ### Step 4: Auto-Remediation (Last Resort)

        IF missing_frameworks:
          LOG: "🔧 Last resort installation attempt..."

          FOR EACH framework IN missing_frameworks:
            package_manager = detect_package_manager()
            install_config = framework.installation.get(package_manager)

            IF NOT install_config:
              ERROR: "Cannot auto-install {framework.name}"
              CONTINUE

            # Check prerequisites
            IF framework.prerequisites:
              prereqs_met = True
              FOR EACH prereq IN framework.prerequisites:
                IF NOT check_prerequisite(prereq):
                  ERROR: "{framework.name} requires {prereq}"
                  prereqs_met = False
                  BREAK
              IF NOT prereqs_met:
                CONTINUE

            # Install
            TRY:
              run(install_config.command, timeout=120)

              # Special handling for Playwright browser installation
              IF framework_id == "playwright":
                LOG: "📥 Installing Playwright browsers..."
                run("npx playwright install chromium", timeout=120)

              # Verify
              FOR EACH verification IN framework.verification:
                result = run(verification.command, timeout=10)
                IF result.returncode == verification.expected_exit_code:
                  LOG: "✅ {framework.name} installed"
                  missing_frameworks.remove(framework)
                  BREAK

            CATCH Exception as e:
              ERROR: "Failed: {e}"

        ### Step 5: Final Check

        IF missing_frameworks:
          WARN_MESSAGE = """
⚠️  E2E Web Framework Missing

Required: {[f.name for f in required_frameworks]}
Missing: {[f.name for f in missing_frameworks]}

E2E web tests will be SKIPPED.

To install manually:
          """

          FOR EACH framework IN missing_frameworks:
            WARN_MESSAGE += f"""
  {framework.name}:
    {framework.installation[package_manager].command}
    Verify: {framework.verification[0].command}
    Docs: {framework.docs_url}
          """

          WARN_MESSAGE += """
Alternatives:
          """

          FOR EACH framework IN missing_frameworks:
            IF framework.alternative_to:
              WARN_MESSAGE += f"  {', '.join(framework.alternative_to)}\n"

          PRINT WARN_MESSAGE

          # E2E web tests are optional - don't block, just skip
          LOG: "Skipping E2E web test scaffolding (framework missing)"
          EXIT(0)  # Graceful skip

        LOG: "✅ E2E web frameworks verified - proceeding to test creation"

        ---

        ## Task - E2E Test Scaffolding
        Create Playwright test scaffolds:
        1. Find AS-xxx requiring e2e/playwright tests
        2. Create test files in tests/e2e/ or e2e/
        3. Configure Playwright to use staging services
        4. Create page objects for main screens

        ## Playwright Config
        ```typescript
        // playwright.config.ts
        export default defineConfig({
          use: {
            baseURL: process.env.BASE_URL || 'http://localhost:3000',
          },
          projects: [
            { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
          ],
        });
        ```

        ## Success Criteria
        - E2E test files created with proper structure
        - Playwright config uses staging services
        - Tests can be run in CI mode
      model_override: sonnet
    - role: mobile-test-scaffolder
      role_group: TESTING
      parallel: true
      depends_on: [staging-validator, dependency-installer]
      priority: 9
      trigger: "when platform is flutter/react_native/kmp/swift/kotlin_android"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        Tasks: {{FEATURE_DIR}}/tasks.md
        Constitution: memory/constitution.md
        Staging Config: .speckit/staging/test-config.env
        Test Framework Registry: memory/domains/test-framework-registry.md
        Test Strategy: .speckit/test-strategy.json

        ## ⚠️ CRITICAL: Framework Pre-Check (Universal)

        Before creating mobile tests, verify required frameworks are installed.

        ### Step 1: Load Test Strategy

        Read: .speckit/test-strategy.json

        IF file does not exist:
          WARN: "test-strategy.json missing - detecting mobile frameworks manually"
          required_frameworks = detect_mobile_frameworks_from_platform()

        ELSE:
          required_frameworks = test_strategy["e2e_mobile"]

        ### Step 2: Check if Mobile Tests Needed

        IF required_frameworks is empty:
          LOG: "⚠️  No mobile test frameworks specified in test strategy"
          LOG: "Checking if mobile platform is detected..."

          # Detect platform
          platform = detect_mobile_platform()
          # Check: pubspec.yaml, package.json (react-native), *.xcodeproj, app/build.gradle

          IF platform is None:
            LOG: "No mobile platform detected - skipping mobile test scaffolding"
            EXIT(0)  # Graceful skip

          ELSE:
            LOG: "Mobile platform detected: {platform}"
            LOG: "But no test framework in strategy - checking tasks.md..."

            has_mobile_tests = check_tasks_for_mobile_test_markers()

            IF NOT has_mobile_tests:
              LOG: "No mobile tests mentioned in tasks.md - skipping"
              EXIT(0)  # Graceful skip

            ELSE:
              WARN: "Mobile tests required but no framework in strategy"
              # Default based on platform
              IF platform == "flutter":
                required_frameworks = ["flutter-test"]
              ELIF platform == "ios":
                required_frameworks = ["xcuitest"]
              ELIF platform == "android":
                required_frameworks = ["espresso"]
              ELIF platform == "react-native":
                required_frameworks = ["maestro"]  # Cross-platform
              ELSE:
                required_frameworks = ["maestro"]  # Universal default

        ### Step 3: Run Verification Commands

        Read: memory/domains/test-framework-registry.md

        missing_frameworks = []

        FOR EACH framework_id IN required_frameworks:
          framework = REGISTRY.get(framework_id)

          IF NOT framework:
            missing_frameworks.append(framework_id)
            CONTINUE

          LOG: "🔍 Verifying {framework.name} for mobile testing..."

          verified = false
          FOR EACH verification IN framework.verification:
            TRY:
              result = run(verification.command, timeout=10)
              IF result.returncode == verification.expected_exit_code:
                verified = true
                LOG: "✅ {framework.name} verified"
                BREAK
            CATCH:
              CONTINUE

          IF NOT verified:
            ERROR: "❌ {framework.name} verification failed"
            missing_frameworks.append(framework)

        ### Step 4: Auto-Remediation (Last Resort)

        IF missing_frameworks:
          LOG: "🔧 Last resort installation attempt for mobile frameworks..."

          FOR EACH framework IN missing_frameworks:
            LOG: "Attempting to install {framework.name}..."

            # Check prerequisites FIRST (mobile frameworks often have platform requirements)
            IF framework.prerequisites:
              prereqs_met = True
              missing_prereqs = []

              FOR EACH prereq IN framework.prerequisites:
                IF NOT check_prerequisite(prereq):
                  missing_prereqs.append(prereq)
                  prereqs_met = False

              IF NOT prereqs_met:
                WARN: """
⚠️  {framework.name} requires prerequisites:
  Missing: {', '.join(missing_prereqs)}

  {framework.installation.manual_steps}

  Docs: {framework.docs_url}

Cannot auto-install - manual setup required.
                """
                CONTINUE  # Skip to next framework

            # Prerequisites met - attempt installation
            package_manager = detect_package_manager()
            install_config = framework.installation.get(package_manager)

            IF NOT install_config:
              ERROR: "No installation method for {package_manager}"
              CONTINUE

            TRY:
              run(install_config.command, timeout=180)  # Mobile tools can be slow

              # Config generation
              IF install_config.config_gen:
                run(install_config.config_gen, timeout=30)

              # Verify
              FOR EACH verification IN framework.verification:
                result = run(verification.command, timeout=10)
                IF result.returncode == verification.expected_exit_code:
                  LOG: "✅ {framework.name} installed successfully"
                  missing_frameworks.remove(framework)
                  BREAK

            CATCH Exception as e:
              ERROR: "Failed to install {framework.name}: {e}"

        ### Step 5: Final Check - Handle Platform-Specific Constraints

        IF missing_frameworks:
          WARN_MESSAGE = """
⚠️  Mobile Test Framework Missing

Required: {[f.name for f in required_frameworks]}
Missing: {[f.name for f in missing_frameworks]}

Platform-specific requirements:
          """

          FOR EACH framework IN missing_frameworks:
            WARN_MESSAGE += f"""
  {framework.name}:
    Prerequisites: {', '.join(framework.prerequisites) if framework.prerequisites else 'None'}
          """

            IF framework.prerequisites:
              WARN_MESSAGE += f"""
    Manual setup required:
      {framework.installation.manual_steps}
              """
            ELSE:
              WARN_MESSAGE += f"""
    Install command:
      {framework.installation[package_manager].command if install_config else 'See docs'}
              """

            WARN_MESSAGE += f"""
    Verify: {framework.verification[0].command}
    Docs: {framework.docs_url}
          """

          WARN_MESSAGE += """
Mobile tests will be SKIPPED.

Common issues:
- XCUITest: Requires macOS + Xcode (install from App Store)
- Espresso: Requires Android SDK + $ANDROID_HOME set
- Maestro: Requires network access for installation script
- Flutter test: Requires Flutter SDK installed

Alternatives:
          """

          FOR EACH framework IN missing_frameworks:
            IF framework.alternative_to:
              WARN_MESSAGE += f"  Instead of {framework.name}: {', '.join(framework.alternative_to)}\n"

          PRINT WARN_MESSAGE

          # Mobile tests are optional - don't block, just skip
          LOG: "Skipping mobile test scaffolding (framework missing or prerequisites not met)"
          EXIT(0)  # Graceful skip

        LOG: "✅ Mobile frameworks verified - proceeding to test creation"

        ---

        ## Platform Detection
        Detect mobile platform from project files:
        - Flutter: pubspec.yaml exists
        - React Native: package.json contains "react-native"
        - KMP: build.gradle.kts contains kotlin("multiplatform")
        - Native iOS: *.xcodeproj exists
        - Native Android: app/build.gradle exists without React Native

        ## Task - Mobile Test Scaffolding (TDD Red Phase)
        Create mobile test scaffolds based on detected platform:

        ### Flutter
        1. Create integration_test/ directory
        2. Add integration_test/app_test.dart:
           ```dart
           import 'package:flutter_test/flutter_test.dart';
           import 'package:integration_test/integration_test.dart';
           import 'package:{{app_name}}/main.dart' as app;

           void main() {
             IntegrationTestWidgetsFlutterBinding.ensureInitialized();
             // AS-xxx: [scenario description]
             testWidgets('AS-xxx: test description', (tester) async {
               app.main();
               await tester.pumpAndSettle();
               // TODO: Implement test - must FAIL initially
               expect(find.text('Expected'), findsOneWidget);
             });
           }
           ```

        ### React Native - Detox
        IF .detoxrc.js exists OR package.json has "detox":
        1. Create e2e/ directory
        2. Add e2e/firstTest.e2e.js:
           ```javascript
           describe('Feature Tests', () => {
             beforeAll(async () => {
               await device.launchApp();
             });
             // AS-xxx: [scenario description]
             it('AS-xxx: test description', async () => {
               // TODO: Implement test - must FAIL initially
               await expect(element(by.id('expected-element'))).toBeVisible();
             });
           });
           ```

        ### React Native - Maestro
        IF .maestro/ exists OR package.json has "maestro":
        1. Create .maestro/ directory
        2. Add .maestro/feature-flow.yaml:
           ```yaml
           appId: com.example.app
           ---
           # AS-xxx: [scenario description]
           - launchApp
           - assertVisible: "Expected Text"
           # TODO: Complete flow - must FAIL initially
           ```

        ### Native iOS (XCUITest)
        1. Create UITests target if not exists
        2. Add FeatureUITests.swift:
           ```swift
           import XCTest
           class FeatureUITests: XCTestCase {
               // AS-xxx: [scenario description]
               func testASxxx() throws {
                   let app = XCUIApplication()
                   app.launch()
                   // TODO: Implement test - must FAIL initially
                   XCTAssertTrue(app.staticTexts["Expected"].exists)
               }
           }
           ```

        ### Native Android (Espresso)
        1. Create androidTest directory if not exists
        2. Add FeatureTest.kt:
           ```kotlin
           @RunWith(AndroidJUnit4::class)
           class FeatureTest {
               @get:Rule
               val activityRule = ActivityScenarioRule(MainActivity::class.java)

               // AS-xxx: [scenario description]
               @Test
               fun testASxxx() {
                   // TODO: Implement test - must FAIL initially
                   onView(withText("Expected")).check(matches(isDisplayed()))
               }
           }
           ```

        ## TDD Red Phase Requirements
        - ALL tests MUST be created with assertions that WILL FAIL
        - Map each test to AS-xxx from spec.md
        - Include @speckit:AS-xxx annotations in comments

        ## iOS Simulator Handling
        - IF macOS: Configure tests for iOS Simulator
        - IF NOT macOS: Skip iOS tests with warning, create Android-only tests
        - Log: "iOS tests skipped - requires macOS host"

        ## Success Criteria (QG-MOB-001 Validation)
        - Mobile test files created for detected platform
        - Tests reference AS-xxx from spec
        - Tests can connect to mobile staging (emulator/simulator)
        - ALL tests FAIL initially (TDD red verified)

        ## Output
        - Test files created in appropriate directories
        - Mobile test run summary: X tests created, X failures (expected)
        - Platform detected: [flutter|react_native|kmp|ios_native|android_native]
      model_override: sonnet
    - role: binding-test-scaffolder
      role_group: TESTING
      parallel: true
      depends_on: [mobile-test-scaffolder]
      priority: 9
      trigger: "when platform is kmp"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        Tasks: {{FEATURE_DIR}}/tasks.md
        Platform: KMP (Kotlin Multiplatform)

        ## Task - Platform Binding Test Scaffolding (TDD Red Phase)
        Generate binding verification tests for KMP platform layer.
        These tests verify that platform UI (SwiftUI/Compose) correctly calls shared Kotlin code.

        ## Step 1: Analyze Shared ViewModels
        FOR EACH ViewModel in shared/src/commonMain/**/*ViewModel.kt:
          PARSE public methods (fun methodName(...))
          PARSE StateFlow properties (val propertyName: StateFlow<...>)
          PARSE SharedFlow properties (val propertyName: SharedFlow<...>)

        ## Step 2: Generate iOS Binding Tests
        IF iosApp/ exists:
          CREATE iosApp/iosAppTests/binding/{ViewModel}BindingTests.swift:
          ```swift
          import XCTest
          @testable import iosApp
          @testable import shared

          class {ViewModel}BindingTests: XCTestCase {

              // BINDING-TEST:{ViewModel}:{method}
              func test_{method}_callsViewModel() {
                  // Arrange - Create mock or spy ViewModel
                  let viewModel = {ViewModel}()
                  let wrapper = {ViewModel}Wrapper(viewModel: viewModel)

                  // Act - Call wrapper method
                  wrapper.{method}({testParams})

                  // Assert - Verify Kotlin method was called
                  // TODO: Implement assertion - must FAIL initially
                  XCTFail("Binding test not implemented")
              }

              // BINDING-TEST:{ViewModel}:{stateFlowProperty}
              func test_{stateFlowProperty}_observesStateFlow() {
                  // Arrange
                  let viewModel = {ViewModel}()
                  let expectation = expectation(description: "StateFlow observed")

                  // Act - Subscribe to StateFlow
                  var receivedValue: {Type}?
                  viewModel.{stateFlowProperty}.collect { value in
                      receivedValue = value
                      expectation.fulfill()
                  }

                  // Assert
                  // TODO: Implement assertion - must FAIL initially
                  XCTFail("StateFlow observation test not implemented")
              }
          }
          ```

        ## Step 3: Generate Android Binding Tests
        IF androidApp/ exists:
          CREATE androidApp/src/androidTest/kotlin/binding/{ViewModel}BindingTest.kt:
          ```kotlin
          package com.example.app.binding

          import io.mockk.*
          import kotlinx.coroutines.flow.first
          import kotlinx.coroutines.test.runTest
          import org.junit.Test
          import org.junit.Assert.*

          class {ViewModel}BindingTest {

              // BINDING-TEST:{ViewModel}:{method}
              @Test
              fun `{method} calls ViewModel correctly`() = runTest {
                  // Arrange - Create mock ViewModel
                  val viewModel = mockk<{ViewModel}>(relaxed = true)

                  // Act - Simulate UI calling the method
                  viewModel.{method}({testParams})

                  // Assert - Verify method was called
                  // TODO: Implement assertion - must FAIL initially
                  fail("Binding test not implemented")
              }

              // BINDING-TEST:{ViewModel}:{stateFlowProperty}
              @Test
              fun `{stateFlowProperty} StateFlow is collected by UI`() = runTest {
                  // Arrange
                  val viewModel = {ViewModel}()

                  // Act - Collect StateFlow
                  val value = viewModel.{stateFlowProperty}.first()

                  // Assert
                  // TODO: Implement assertion - must FAIL initially
                  fail("StateFlow collection test not implemented")
              }
          }
          ```

        ## Step 4: Generate Binding Coverage Report
        CREATE .speckit/binding-coverage.json:
        ```json
        {
          "viewModels": [
            {
              "name": "{ViewModel}",
              "methods": ["{method1}", "{method2}"],
              "stateFlows": ["{property1}", "{property2}"],
              "iosTests": "iosApp/iosAppTests/binding/{ViewModel}BindingTests.swift",
              "androidTests": "androidApp/src/androidTest/kotlin/binding/{ViewModel}BindingTest.kt"
            }
          ],
          "coverage": {
            "methodsCovered": 0,
            "methodsTotal": X,
            "stateFlowsCovered": 0,
            "stateFlowsTotal": Y
          }
        }
        ```

        ## Success Criteria (QG-BIND-001 Validation)
        - Binding test files created for all ViewModels
        - Each public method has a binding test
        - Each StateFlow has an observation test
        - ALL tests FAIL initially (TDD red verified)
        - Binding coverage report generated

        ## Output
        - iOS binding tests: iosApp/iosAppTests/binding/*.swift
        - Android binding tests: androidApp/src/androidTest/kotlin/binding/*.kt
        - Coverage report: .speckit/binding-coverage.json
      model_override: sonnet
    # Wave 3: Core Implementation - TDD Green Phase (make tests pass)
    - role: data-layer-builder
      role_group: BACKEND
      parallel: true
      depends_on: [test-scaffolder]
      priority: 8
      trigger: "when implementing data models"
      prompt: |
        ═══════════════════════════════════════════════════════════════
        ⚠️  TASK STATUS UPDATE PROTOCOL - MANDATORY ⚠️
        ═══════════════════════════════════════════════════════════════

        AFTER EACH TASK YOU COMPLETE:
          1. ✅ Complete the implementation work
          2. ✅ Edit tasks.md: change `- [ ] T00x...` → `- [X] T00x...`
          3. ✅ Verify the edit succeeded
          4. ✅ ONLY THEN proceed to next task

        ⛔ BLOCKER: If you skip the update, the entire workflow FAILS ⛔

        ═══════════════════════════════════════════════════════════════

        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        Data Model: {{FEATURE_DIR}}/data-model.md (if exists)

        ## Task
        Build data layer from specification:
        1. Create database models/schemas per spec requirements
        2. Implement data access layer (repositories, DAOs)
        3. Generate migrations if applicable
        4. Add data validation and type safety

        ## Success Criteria
        - All entities from spec.md have corresponding models
        - Relationships match data-model.md
        - Types are fully annotated (@speckit:FR-xxx)
    - role: ui-foundation-builder
      role_group: FRONTEND
      parallel: true
      depends_on: [test-scaffolder]
      priority: 8
      trigger: "when implementing UI foundation"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        Design System: specs/app-design/design_system.md

        ## Task
        Build UX foundation:
        1. Set up layout components (Header, Footer, Sidebar)
        2. Implement navigation structure per sitemap
        3. Create error boundary and loading states
        4. Build authentication UI if spec requires

        ## Success Criteria
        - Layout renders without errors
        - Navigation works between routes
        - Error handling catches and displays errors gracefully
    - role: api-builder
      role_group: BACKEND
      parallel: true
      depends_on: [data-layer-builder]
      priority: 7
      trigger: "when implementing API endpoints"
      prompt: |
        ═══════════════════════════════════════════════════════════════
        ⚠️  TASK STATUS UPDATE PROTOCOL - MANDATORY ⚠️
        ═══════════════════════════════════════════════════════════════

        AFTER EACH TASK YOU COMPLETE:
          1. ✅ Complete the implementation work
          2. ✅ Edit tasks.md: change `- [ ] T00x...` → `- [X] T00x...`
          3. ✅ Verify the edit succeeded
          4. ✅ ONLY THEN proceed to next task

        ⛔ BLOCKER: If you skip the update, the entire workflow FAILS ⛔

        ═══════════════════════════════════════════════════════════════

        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        API Contracts: contracts/ (if exists)
        Data Layer: (from data-layer-builder)

        ## Task
        Build API endpoints:
        1. Create REST/GraphQL endpoints per contracts
        2. Connect endpoints to data layer
        3. Implement request validation
        4. Add proper error responses (400, 401, 404, 500)

        ## Success Criteria
        - All spec FRs have corresponding endpoints
        - Endpoints return correct status codes
        - Request/response types match contracts
    - role: ui-feature-builder
      role_group: FRONTEND
      parallel: true
      depends_on: [ui-foundation-builder, api-builder]
      priority: 6
      trigger: "when implementing feature UI"
      prompt: |
        ═══════════════════════════════════════════════════════════════
        ⚠️  TASK STATUS UPDATE PROTOCOL - MANDATORY ⚠️
        ═══════════════════════════════════════════════════════════════

        AFTER EACH TASK YOU COMPLETE:
          1. ✅ Complete the implementation work
          2. ✅ Edit tasks.md: change `- [ ] T00x...` → `- [X] T00x...`
          3. ✅ Verify the edit succeeded
          4. ✅ ONLY THEN proceed to next task

        ⛔ BLOCKER: If you skip the update, the entire workflow FAILS ⛔

        ═══════════════════════════════════════════════════════════════

        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        User Stories: (from spec.md)
        API Endpoints: (from api-builder)

        ## Task
        Build feature UI components:
        1. Create feature-specific components per user stories
        2. Connect components to API endpoints
        3. Implement form handling and validation
        4. Add loading, error, and success states

        ## Success Criteria
        - Each user story has corresponding UI
        - Forms validate input before submission
        - API errors display user-friendly messages
    - role: component-wire-builder
      role_group: FRONTEND
      parallel: true
      depends_on: [ui-foundation-builder, ui-feature-builder]
      priority: 5
      trigger: "when wiring components into screens (UI features with Component Registry)"
      skip_if: "spec.md does not contain '## UI Component Registry' section"
      prompt: |
        ═══════════════════════════════════════════════════════════════
        ⚠️  TASK STATUS UPDATE PROTOCOL - MANDATORY ⚠️
        ═══════════════════════════════════════════════════════════════

        AFTER EACH TASK YOU COMPLETE:
          1. ✅ Complete the implementation work
          2. ✅ Edit tasks.md: change `- [ ] T00x...` → `- [X] T00x...`
          3. ✅ Verify the edit succeeded
          4. ✅ ONLY THEN proceed to next task

        ⛔ BLOCKER: If you skip the update, the entire workflow FAILS ⛔

        ═══════════════════════════════════════════════════════════════

        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md (contains Component Registry, Screen Registry)
        Tasks: {{FEATURE_DIR}}/tasks.md (contains CSIM matrix)

        ## Pre-Check: Component Registry Detection
        1. Read spec.md
        2. VERIFY: Contains "## UI Component Registry" section
        3. IF NOT FOUND: Skip this role (not a component-based UI feature)

        ## Task: Wire Components into Screens

        Execute all [WIRE:COMP-xxx→SCR-yyy] tasks from tasks.md:

        ```
        FOR EACH task WITH marker [WIRE:COMP-xxx→SCR-yyy]:

          1. **Extract References**:
             - component_id = COMP-xxx (from marker)
             - screen_id = SCR-yyy (from marker)
             - Look up [COMP:COMP-xxx] task → get component file path
             - Look up [SCREEN:SCR-yyy] task → get screen file path

          2. **Verify Prerequisites**:
             - CONFIRM [COMP:COMP-xxx] task is marked [X]
             - CONFIRM [SCREEN:SCR-yyy] task is marked [X] OR screen file exists
             - IF NOT: Log dependency and skip (will retry in next pass)

          3. **Wire Component**:
             a. Read screen file
             b. Add import statement for component
             c. Find placeholder (Text("..."), TODO, etc.) or insertion point
             d. Replace placeholder with component instantiation
             e. Pass required props/parameters

          4. **Verify Integration**:
             - Component import exists in screen file
             - Component is instantiated in render/compose function
             - No placeholder text remains for this component

          5. **Update Tasks**:
             - Mark wire task [X] in tasks.md
             - Update CSIM matrix: Status = [X] for this pair
        ```

        ## Platform-Specific Patterns

        ### Swift/SwiftUI
        ```swift
        // Before (placeholder)
        Text("Settings")

        // After (wired)
        import SharedUI  // or specific component path

        struct SettingsScreen: View {
            var body: some View {
                VStack {
                    FontSizeSliderView()
                    ThemeSwitcherView()
                }
            }
        }
        ```

        ### Kotlin/Compose
        ```kotlin
        // Before (placeholder)
        Text("Settings")

        // After (wired)
        import com.app.ui.components.FontSizeSlider
        import com.app.ui.components.ThemeSwitcher

        @Composable
        fun SettingsScreen() {
            Column {
                FontSizeSlider()
                ThemeSwitcher()
            }
        }
        ```

        ### React/React Native
        ```tsx
        // Before (placeholder)
        <Text>Settings</Text>

        // After (wired)
        import { FontSizeSlider } from '@/components/FontSizeSlider';
        import { ThemeSwitcher } from '@/components/ThemeSwitcher';

        export function SettingsScreen() {
            return (
                <View>
                    <FontSizeSlider />
                    <ThemeSwitcher />
                </View>
            );
        }
        ```

        ### Flutter
        ```dart
        // Before (placeholder)
        Text('Settings')

        // After (wired)
        import 'package:app/widgets/font_size_slider.dart';
        import 'package:app/widgets/theme_switcher.dart';

        class SettingsScreen extends StatelessWidget {
          @override
          Widget build(BuildContext context) {
            return Column(
              children: [
                FontSizeSlider(),
                ThemeSwitcher(),
              ],
            );
          }
        }
        ```

        ## Success Criteria
        - Every [WIRE:] task has been executed
        - Component imports exist in target screen files
        - Components are instantiated (not placeholders)
        - CSIM matrix shows 100% completion for this feature
        - No orphan components (created but not wired)
      model_override: sonnet
    # Wave 3.5: PBT Just-in-Time Validation (if properties.md exists)
    - role: pbt-jit-runner
      role_group: IMPLEMENT_VALIDATION
      parallel: false
      depends_on: [data-layer-builder, api-builder, ui-feature-builder]
      priority: 5
      trigger: "after Wave 3 tasks that map to PROP-xxx (if properties.md exists)"
      skip_if: "properties.md does not exist in FEATURE_DIR"
      prompt: |
        ## PBT Just-in-Time Runner

        ### Pre-check
        1. Verify properties.md exists at {{FEATURE_DIR}}/properties.md
        2. If not exists → skip this role entirely (no PBT for this feature)

        ### Task-to-Property Mapping
        Build mapping from completed Wave 3 tasks to PROP-xxx:
        1. Read tasks.md to get completed tasks with their [FR:xxx] and [AS:xxx] markers
        2. Read properties.md to get PROP-xxx with source_artifacts
        3. For each completed task:
           - Find matching PROP-xxx where source_artifacts overlaps with task markers
           - Add to validation queue

        ### Property Validation Loop
        ```
        FOR EACH prop IN validation_queue:
          attempt = 0
          WHILE attempt < 3:
            1. Run property test:
               python: pytest tests/properties/ -k "prop_{prop.id}" -v
               typescript: npm test -- --testPathPattern=property --testNamePattern="{prop.id}"
               go: go test -v -run TestProp{prop.id}
               java: mvn test -Dtest=*PropertyTest#prop*{prop.id}*
               kotlin: gradle test --tests '*PropertyTest.prop*{prop.id}*'

            2. IF test PASSES:
               - Log: "✓ {prop.id} validated for {task.id}"
               - BREAK (continue to next property)

            3. IF test FAILS:
               a. Capture shrunk counterexample
               b. Analyze failure:
                  - PROPERTY_TOO_STRICT: Log warning, flag for /speckit.clarify, continue
                  - IMPLEMENTATION_BUG: Apply auto-fix, increment attempt
                  - GENERATOR_ISSUE: Log warning, continue (not impl problem)
               c. IF IMPLEMENTATION_BUG AND attempt < 3:
                  - Read counterexample details
                  - Identify failing code path in implementation
                  - Apply targeted fix
                  - Re-run test
               d. attempt++

            4. IF attempt >= 3:
               - Block: "❌ {prop.id} failed after 3 fix attempts"
               - Report counterexample to user
               - Suggest: Manual review or /speckit.clarify
        ```

        ### Auto-Fix Strategies
        Based on counterexample analysis:
        - **Off-by-one errors**: Adjust boundary conditions
        - **Missing validation**: Add input validation
        - **Null/undefined handling**: Add null checks
        - **Type mismatches**: Fix type coercion
        - **State mutation bugs**: Fix immutability issues

        ### Metrics Output
        ```yaml
        pbt_jit_results:
          properties_validated: N
          properties_passed: N
          auto_fixes_applied: N
          shrunk_examples_found: N
          failures_requiring_manual_review: N
        ```

        ### Success Criteria
        - All mapped PROP-xxx tests pass (or flagged for clarify)
        - No unresolved IMPLEMENTATION_BUG failures
        - Shrunk examples saved to properties.md

        ### On Complete
        - Update properties.md with new shrunk examples (if any)
        - Proceed to Wave 4 test verification
      model_override: sonnet
    # Wave 3.6: Task Status Enforcement Checkpoint
    - role: task-status-enforcer
      role_group: ORCHESTRATION
      parallel: false
      depends_on: [data-layer-builder, api-builder, ui-feature-builder, pbt-jit-runner]
      priority: 10
      trigger: "Wave 3 completion checkpoint"
      prompt: |
        ## Task Status Enforcer - Wave 3 Checkpoint

        ### Your Role
        You are the mandatory checkpoint that ensures tasks.md is fully up to date
        before proceeding to Wave 4 (testing).

        ### Action
        1. Read tasks.md from {{FEATURE_DIR}}/tasks.md
        2. Identify all Wave 3 tasks (infrastructure, data, API, UI)
        3. For EACH task that should be completed by now:
           - Check if it shows `[X]` (completed)
           - If still shows `[ ]` but work was done, update to `[X]`
        4. Report summary

        ### Verification Criteria
        - All data layer tasks: [X]
        - All API endpoint tasks: [X]
        - All UI component tasks: [X]
        - All foundation/setup tasks: [X]

        ### Output Format
        ```
        Task Status Checkpoint Report:
        - Total Wave 3 tasks: N
        - Already marked [X]: N
        - Fixed in this checkpoint: N
        - Tasks fixed: T001, T003, T005 (if any)
        ```

        ### CRITICAL
        If you find tasks marked `[ ]` that were clearly completed:
        - Update them immediately using Edit tool
        - Change `- [ ] T00x...` → `- [X] T00x...`
        - This ensures accurate progress tracking

        ### On Complete
        - Confirm all Wave 3 tasks are marked [X]
        - Proceed to Wave 4 test verification
      model_override: haiku
    - role: platform-todo-detector
      role_group: QUALITY
      parallel: false
      depends_on: [component-wiring-implementer]
      priority: 5
      trigger: "after Wave 3 implementation, before Wave 4"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Platform: (auto-detected)

        ## Task - Platform Code Completeness Check (CRITICAL)
        Scan platform-specific files for TODO/stub patterns that indicate incomplete implementation.
        This check BLOCKS Wave 4 progression if violations found.

        ## Critical File Patterns (KMP Projects)
        CRITICAL_FILES = [
          "iosApp/**/*.swift",
          "androidApp/**/*Activity.kt",
          "androidApp/**/*Fragment.kt",
          "androidApp/**/*Screen.kt",
          "androidApp/**/*Composable.kt",
          "**/ui/**/*.swift",
          "**/ui/**/*.kt",
          "**/*Wrapper.swift",
          "**/*ViewModelWrapper.swift"
        ]

        ## Stub/TODO Patterns to Detect
        PATTERNS = [
          "// TODO:",
          "// FIXME:",
          "// HACK:",
          "/* TODO",
          "// TODO: Pass to",
          "// TODO: Implement",
          "fatalError(\"Not implemented\")",
          "fatalError(\"TODO\")",
          "throw NotImplementedError()",
          "TODO(\"",
          "FIXME(\"",
          "pass  # TODO",
          "raise NotImplementedError"
        ]

        ## Hardcoded Value Patterns (KMP-specific)
        HARDCODED_PATTERNS = [
          "\"Chapter 1\"",
          "\"Chapter 2\"",
          "listOf(\"Chapter",
          "arrayOf(\"Chapter",
          "[\"Chapter 1\",",
          "// Hardcoded",
          "// TEMP:",
          "// Temporary"
        ]

        ## Detection Process
        FOR EACH file matching CRITICAL_FILES:
          FOR EACH line in file:
            IF line contains any PATTERN or HARDCODED_PATTERN:
              RECORD violation:
                - file: path
                - line: number
                - content: line content
                - pattern: matched pattern
                - severity: CRITICAL

        ## Severity Rules
        - ANY TODO/FIXME in platform UI code = CRITICAL (blocks Wave 4)
        - ANY hardcoded value that should come from ViewModel = CRITICAL
        - Threshold: 0 violations allowed

        ## Output Format
        IF violations found:
          ```
          ═══════════════════════════════════════════════════════════════
          ❌ PLATFORM CODE COMPLETENESS CHECK FAILED
          ═══════════════════════════════════════════════════════════════

          Found {count} critical violations in platform code:

          1. iosApp/iosApp/ReaderViewModelWrapper.swift:42
             Pattern: // TODO: Pass to settings repository
             → Must implement actual repository call

          2. iosApp/iosApp/ReaderView.swift:381
             Pattern: "Chapter 1" (hardcoded)
             → Must use ViewModel.tableOfContents StateFlow

          ═══════════════════════════════════════════════════════════════
          ⛔ BLOCKING: Fix all TODO/stub code before Wave 4
          ═══════════════════════════════════════════════════════════════
          ```
          EXIT with error - do not proceed to Wave 4

        IF no violations:
          ```
          ✅ Platform code completeness check passed
          No TODO/stub patterns found in platform files
          Proceeding to Wave 4...
          ```

        ## Quality Gate
        - QG-BIND-003: Zero TODO/FIXME/stub comments in platform binding code
        - Severity: CRITICAL
        - Action on failure: BLOCK Wave 4, require fix
      model_override: haiku
    # Wave 4: Test Verification - TDD Green Phase (verify tests pass after implementation)
    # NOTE: Unit and integration tests run in PARALLEL by default (v0.0.104)
    # Use --sequential-tests flag to run sequentially
    - role: unit-test-verifier
      role_group: TESTING
      parallel: true  # Runs in parallel with integration-test-verifier
      depends_on: [data-layer-builder, api-builder, task-status-enforcer]
      priority: 5
      trigger: "after core implementation complete"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        Tests: tests/unit/ (created in Wave 2)
        Staging: .speckit/staging/test-config.env

        ## Task - UNIT TEST VERIFICATION (TDD Green Phase)
        Run unit tests and verify implementation makes them pass:
        1. Load staging environment variables
        2. Run unit tests only (npm test:unit / pytest tests/unit)
        3. Verify tests that failed in Wave 2 now PASS
        4. Calculate unit test coverage

        ## Success Criteria
        - All unit tests from Wave 2 now pass
        - Unit test coverage >= 80%
        - No test regressions

        ## Output
        - Test run summary: X unit tests, X passed, 0 failed
        - Coverage report: XX% line coverage (unit only)
      model_override: sonnet
    - role: integration-test-verifier
      role_group: TESTING
      parallel: true  # Runs in parallel with unit-test-verifier
      depends_on: [ui-feature-builder, api-builder, task-status-enforcer]
      priority: 5
      trigger: "after core implementation complete"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        Tests: tests/integration/ (created in Wave 2)
        Staging: .speckit/staging/test-config.env

        ## Task - INTEGRATION TEST VERIFICATION (TDD Green Phase)
        Run integration tests and verify implementation makes them pass:
        1. Load staging environment variables
        2. Run integration tests only (npm test:integration / pytest tests/integration)
        3. Use staging database for database tests
        4. Verify API integration works correctly

        ## Success Criteria
        - All integration tests from Wave 2 now pass
        - Database/API integration verified
        - No flaky tests

        ## Output
        - Test run summary: X integration tests, X passed, 0 failed
        - Integration points validated
      model_override: sonnet
    - role: e2e-test-verifier
      role_group: TESTING
      parallel: false  # Sequential AFTER unit/integration complete
      depends_on: [unit-test-verifier, integration-test-verifier]
      priority: 4
      trigger: "after unit and integration tests pass"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        Tests: tests/e2e/ (created in Wave 2)
        Staging: .speckit/staging/test-config.env

        ## Task - E2E TEST VERIFICATION (TDD Green Phase)
        Run e2e tests after unit/integration tests pass:
        1. Load staging environment variables
        2. Run e2e tests (playwright / cypress)
        3. Verify complete user journeys work

        ## Success Criteria
        - All e2e tests from Wave 2 now pass
        - User journeys verified end-to-end
        - No flaky tests (retry logic if needed)

        ## Output
        - Test run summary: X e2e tests, X passed, 0 failed
        - QG-TEST-004: PASSED if overall coverage >= 80%
      model_override: sonnet
    - role: mobile-test-verifier
      role_group: TESTING
      parallel: false  # Sequential AFTER e2e tests complete
      depends_on: [e2e-test-verifier]
      priority: 3
      trigger: "when platform is flutter/react_native/kmp/swift/kotlin_android"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        Tasks: {{FEATURE_DIR}}/tasks.md
        Mobile Tests: (created in Wave 2 by mobile-test-scaffolder)
        Staging Config: .speckit/staging/test-config.env

        ## Platform Detection
        Same as mobile-test-scaffolder:
        - Flutter: pubspec.yaml exists
        - React Native: package.json contains "react-native"
        - KMP: build.gradle.kts contains kotlin("multiplatform")
        - Native iOS: *.xcodeproj exists
        - Native Android: app/build.gradle exists

        ## Task - Mobile Test Verification (TDD Green Phase)
        Run mobile tests after e2e tests pass:

        ### Flutter
        ```bash
        # Check for connected devices/emulators
        flutter devices

        # Run integration tests on Android emulator
        flutter test integration_test/ --device-id=emulator-5554

        # Run on iOS Simulator (macOS only)
        if [[ "$(uname)" == "Darwin" ]]; then
          flutter test integration_test/ --device-id="iPhone 15 Pro"
        fi
        ```

        ### React Native - Detox
        ```bash
        # Build and test Android
        detox build --configuration android.emu.debug
        detox test --configuration android.emu.debug

        # Build and test iOS (macOS only)
        if [[ "$(uname)" == "Darwin" ]]; then
          detox build --configuration ios.sim.debug
          detox test --configuration ios.sim.debug
        fi
        ```

        ### React Native - Maestro
        ```bash
        # Run Maestro flows
        maestro test .maestro/

        # Or specific flow
        maestro test .maestro/feature-flow.yaml
        ```

        ### Native iOS (XCUITest)
        ```bash
        # macOS only
        if [[ "$(uname)" == "Darwin" ]]; then
          xcodebuild test \
            -scheme Runner \
            -destination 'platform=iOS Simulator,name=iPhone 15 Pro'
        else
          echo "WARN: iOS tests skipped - requires macOS"
        fi
        ```

        ### Native Android (Espresso)
        ```bash
        # Ensure emulator is running (from staging)
        adb devices | grep emulator

        # Run instrumented tests
        ./gradlew connectedAndroidTest
        ```

        ## Cross-Platform Verification (QG-MOB-003)
        - IF both Android AND iOS supported:
          - Run tests on BOTH platforms
          - Both must pass for QG-MOB-003
        - IF macOS not available:
          - Run Android tests only
          - Log warning: "iOS tests skipped - requires macOS host"
          - QG-MOB-003 passes with Android-only if explicitly --android-only

        ## Coverage Check (QG-MOB-002)
        - Flutter: `flutter test --coverage`
        - React Native: Check Jest coverage from Detox
        - Native: Use platform-specific coverage tools
        - Threshold: >= 70% mobile test coverage

        ## Device Profile Validation (QG-MOB-004)
        Verify tests run on at least one device per category:
        - Android: emulator OR physical device
        - iOS: simulator OR physical device (macOS only)

        ## Success Criteria
        - All mobile tests from Wave 2 now PASS
        - QG-MOB-002: Mobile coverage >= 70%
        - QG-MOB-003: Tests pass on all available platforms
        - QG-MOB-004: At least 1 device per platform tested

        ## Output
        - Test run summary per platform:
          - Android: X tests, X passed, 0 failed
          - iOS: X tests, X passed, 0 failed (or "skipped")
        - QG-MOB-002: PASSED/FAILED (coverage: XX%)
        - QG-MOB-003: PASSED/FAILED (platforms: android, ios)
        - QG-MOB-004: PASSED/FAILED (devices tested: N)
      model_override: sonnet

# Wave 4.5: MQS Validation (Mobile Quality Score)
    - role: mqs-validator
      role_group: VALIDATION
      parallel: false
      depends_on: [mobile-test-verifier, binding-test-scaffolder]
      priority: 4
      trigger: "when mobile platform detected AND Wave 4 mobile tests complete"
      skip_if: "no mobile platform detected"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Platform: {{MOBILE_PLATFORM}} (kmp, flutter, react-native, ios-native, android-native)
        Persona: mobile-developer-agent
        Skills: mobile-architecture, mobile-performance, mobile-testing, {{PLATFORM}}-expert

        ## Purpose
        Calculate final Mobile Quality Score (MQS) and validate against threshold.
        MQS gates release readiness for mobile applications.

        ## MQS Calculation

        ```text
        MQS = architecture_score     # 0-25 points
            + performance_score      # 0-20 points
            + parity_score          # 0-20 points
            + testing_score         # 0-20 points
            + accessibility_score   # 0-15 points
                                    # Total: 0-100 points
        ```

        ### Architecture Score (0-25)

        | Criteria | Points | Check |
        |----------|--------|-------|
        | Clean layer separation | 8 | presentation/domain/data layers exist |
        | DI configured | 7 | Koin/GetIt/Hilt modules registered |
        | Shared code ratio | 5 | ≥70% code in shared modules (cross-platform) |
        | State management | 5 | ViewModel/BLoC unidirectional flow |

        ### Performance Score (0-20)

        | Criteria | Points | Check |
        |----------|--------|-------|
        | Cold start time | 6 | < 2s measured or estimated |
        | Frame rate | 6 | 60 FPS, no jank in lists |
        | Memory usage | 4 | Peak < 150MB |
        | Battery impact | 4 | No polling, efficient background |

        ### Platform Parity Score (0-20) - Cross-Platform Only

        | Criteria | Points | Check |
        |----------|--------|-------|
        | Feature parity | 10 | Same features on all platforms |
        | UX adaptation | 5 | HIG on iOS, Material on Android |
        | Platform bugs | 5 | No platform-specific bugs |

        For native-only projects, award full 20 points.

        ### Testing Score (0-20)

        | Criteria | Points | Check |
        |----------|--------|-------|
        | Unit coverage | 8 | ≥80% coverage |
        | Binding tests | 6 | 100% ViewModel methods tested |
        | E2E coverage | 6 | Critical paths covered |

        ### Accessibility Score (0-15)

        | Criteria | Points | Check |
        |----------|--------|-------|
        | A11y labels | 5 | All interactive elements labeled |
        | Screen reader | 5 | VoiceOver/TalkBack navigation works |
        | Touch targets | 5 | ≥44pt iOS / ≥48dp Android |

        ## Validation

        ```text
        CALCULATE scores:
          FOR EACH dimension:
            - Analyze codebase against criteria
            - Award points based on compliance
            - Note gaps and recommendations

        EVALUATE threshold:
          IF MQS >= 75:
            STATUS = "✅ Production Ready"
            ALLOW release
          ELSE:
            STATUS = "❌ Below Threshold"
            BLOCK release (unless --skip-mqs flag)
            GENERATE improvement_plan.md
        ```

        ## Quality Gates

        | Gate ID | Purpose | Threshold | Severity |
        |---------|---------|-----------|----------|
        | QG-MQS-001 | Architecture | ≥ 20/25 | HIGH |
        | QG-MQS-002 | Performance | ≥ 15/20 | HIGH |
        | QG-MQS-003 | Platform Parity | ≥ 15/20 | HIGH |
        | QG-MQS-004 | Testing | ≥ 15/20 | CRITICAL |
        | QG-MQS-005 | Accessibility | ≥ 10/15 | MEDIUM |
        | QG-MQS | Total Score | ≥ 75/100 | CRITICAL |

        ## Output

        Generate MQS report:

        ```text
        ┌─────────────────────────────────────────────────────────────┐
        │                   MOBILE QUALITY SCORE                       │
        ├─────────────────────────────────────────────────────────────┤
        │  Architecture    ████████████████████░░░░░  20/25           │
        │  Performance     ████████████████░░░░░░░░░  16/20           │
        │  Platform Parity ████████████████████░░░░░  18/20           │
        │  Testing         ████████████████████░░░░░  18/20           │
        │  Accessibility   ████████████░░░░░░░░░░░░░  12/15           │
        ├─────────────────────────────────────────────────────────────┤
        │  TOTAL                                       84/100  ✅     │
        │  Status: Production Ready                                   │
        └─────────────────────────────────────────────────────────────┘

        Recommendations:
        1. [HIGH] Increase touch targets for 3 buttons
        2. [MEDIUM] Add lazy Koin initialization
        3. [LOW] Improve cold start by 200ms
        ```

        IF MQS < 75:
          - Create memory/mqs-improvements.md with prioritized fixes
          - Block Wave 5 (polish) until fixed or --skip-mqs used

        ## Success Criteria
        - MQS calculated for all 5 dimensions
        - QG-MQS: Total score ≥ 75/100 (CRITICAL)
        - QG-MQS-004: Testing score ≥ 15/20 (CRITICAL)
        - All binding tests pass (QG-BIND-001/002/003)
        - Improvement recommendations generated if score < 90
      model_override: sonnet

    - role: unit-test-generator
      role_group: TESTING
      parallel: true
      depends_on: [unit-test-verifier, integration-test-verifier, e2e-test-verifier, mobile-test-verifier]
      priority: 4
      trigger: "when adding additional unit tests for coverage"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        Acceptance Scenarios: AS-xxx from spec.md
        Current Coverage: (from test-verifier)

        ## Task
        Add unit tests to improve coverage:
        1. Identify untested code paths from coverage report
        2. Add tests for edge cases and error conditions
        3. Mock external dependencies
        4. Add @speckit:AS-xxx annotations for traceability

        ## Success Criteria
        - Coverage >= 80% for new code
        - All public methods have tests
        - Tests are isolated (no side effects)
      model_override: sonnet
    - role: integration-test-generator
      role_group: TESTING
      parallel: true
      depends_on: [ui-feature-builder, api-builder]
      priority: 4
      trigger: "when generating integration tests"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        User Journeys: (from spec.md)

        ## Task
        Generate integration/e2e tests:
        1. Test complete user journeys end-to-end
        2. Test API endpoints with real database
        3. Test UI flows with simulated user interaction
        4. Add @speckit:AS-xxx annotations

        ## Success Criteria
        - Each user journey has e2e test
        - Tests run in CI environment
        - No flaky tests (deterministic)
      model_override: sonnet
    - role: property-test-generator
      role_group: TESTING
      parallel: true
      depends_on: [data-layer-builder, api-builder, pbt-jit-runner]
      priority: 4
      trigger: "when running final property validation (full suite after JIT)"
      skip_if: "properties.md does not exist in FEATURE_DIR"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        Properties: {{FEATURE_DIR}}/properties.md

        ## Pre-check
        IF properties.md does not exist:
          - Log: "No properties.md - skipping final PBT validation"
          - Skip this role

        ## Purpose
        This is FINAL VALIDATION after JIT mode ran incremental tests.
        - JIT already validated individual properties after each task
        - Final validation catches cross-property interactions
        - Full shrinking and comprehensive statistics

        ## Task
        Run complete property test suite:
        1. Execute ALL property tests from properties.md
        2. Collect cross-property statistics
        3. Capture any new counterexamples found
        4. Validate shrunk examples still trigger failures
        5. Generate final PQS (Property Quality Score) report

        ## Execution Commands
        ```yaml
        python: |
          pytest tests/properties/ -v --hypothesis-show-statistics
          # Full suite, not filtered by PROP-xxx
        typescript: |
          npm run test:properties
          # fast-check with all properties
        go: |
          go test -v ./... -run TestProperty -rapid.checks=100
        java: |
          mvn test -Dtest=*Property* -Djqwik.reporting.onlyFailures=false
        kotlin: |
          gradle test --tests '*Property*' --info
        ```

        ## On Failure
        - Capture counterexample with full shrinking output
        - Update shrunk examples in properties.md
        - Flag for PGS iteration if invariant violated
        - Report: "Final PBT validation failed - review cross-property interactions"

        ## Success Criteria
        - All properties pass with 100+ examples
        - No new counterexamples discovered
        - Shrunk examples documented if found
        - PQS maintained at >= 80

        ## Metrics Output
        ```
        Final PBT Validation Report:
        - Total properties: N
        - JIT-validated: N (from pbt-jit-runner)
        - Final-validated: N
        - New counterexamples: N
        - Cross-property issues: N
        - Final PQS: NN
        ```
      model_override: sonnet
    # Wave 4: Review (sequential)
    - role: component-integration-verifier
      role_group: REVIEW
      parallel: false
      depends_on: [component-wire-builder]
      priority: 4
      trigger: "after component wiring (UI features with Component Registry)"
      skip_if: "spec.md does not contain '## UI Component Registry' section"
      prompt: |
        ## Component Integration Verifier (QG-COMP-004)

        ### Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        Tasks: {{FEATURE_DIR}}/tasks.md

        ### Pre-Check
        1. Read spec.md
        2. VERIFY: Contains "## UI Component Registry" section
        3. IF NOT FOUND: Skip this role (not a component-based UI feature)

        ### Verification Protocol

        Execute QG-COMP-004 validation:

        ```
        orphan_components = []
        incomplete_wires = []
        placeholder_warnings = []

        FOR EACH wire_task marked [X] in tasks.md:

          1. **Extract Files**:
             - Parse [WIRE:COMP-xxx→SCR-yyy] marker
             - Look up component_file from [COMP:COMP-xxx] task
             - Look up screen_file from [SCREEN:SCR-yyy] task

          2. **Verify Import**:
             - Read screen_file
             - SCAN for import of component (by filename, class name, or module)
             - IF NOT FOUND:
               incomplete_wires.append({
                 wire_task: task_id,
                 component: COMP-xxx,
                 screen: SCR-yyy,
                 issue: "Missing import"
               })

          3. **Verify Usage**:
             - SCAN screen_file for component instantiation
             - Look for: ComponentName(), <ComponentName />, ComponentName{}
             - IF NOT FOUND:
               orphan_components.append({
                 component: COMP-xxx,
                 screen_file: screen_file,
                 issue: "Component imported but not used"
               })

          4. **Placeholder Detection**:
             - SCAN screen_file for patterns:
               - Text("placeholder")
               - Text("Settings")  # generic labels where component should be
               - TODO:, FIXME:, HACK: in render/compose
               - EmptyView(), Spacer() with comments indicating missing component
             - IF FOUND in area where component should be:
               placeholder_warnings.append({
                 file: screen_file,
                 pattern: matched_pattern,
                 suggestion: "Replace with {component_name}"
               })
        ```

        ### Failure Handling

        ```
        IF orphan_components.length > 0 OR incomplete_wires.length > 0:

          1. **Revert Task Status**:
             FOR EACH issue IN (orphan_components + incomplete_wires):
               - Find wire task [WIRE:COMP-xxx→SCR-yyy]
               - Change [X] back to [ ] in tasks.md
               - Update CSIM matrix: Status = [ ]

          2. **Report**:
             ERROR: "Component Integration Incomplete"
             - Orphan components: {count}
             - Incomplete wires: {count}
             - Details: {list each issue}

          3. **Action**:
             - Log for component-wire-builder to retry
             - Block proceeding to code-reviewer

        IF placeholder_warnings.length > 0:
          WARNING: "Potential placeholder remnants detected"
          - {list each warning}
          - Action: Review manually, may be intentional
        ```

        ### Success Report

        ```
        ✅ Component Integration Verified (QG-COMP-004)

        Wire Tasks Validated: {count}
        ┌──────────┬─────────────────────┬─────────────┬────────┐
        │ COMP     │ Component           │ Screen      │ Status │
        ├──────────┼─────────────────────┼─────────────┼────────┤
        │ COMP-001 │ FontSizeSliderView  │ Settings    │ ✅     │
        │ COMP-001 │ FontSizeSliderView  │ ReaderOverlay│ ✅    │
        │ COMP-002 │ ThemeSwitcherView   │ Settings    │ ✅     │
        │ COMP-002 │ ThemeSwitcherView   │ ReaderOverlay│ ✅    │
        └──────────┴─────────────────────┴─────────────┴────────┘

        Orphan Components: 0
        Placeholder Warnings: 0

        → Proceeding to code review
        ```

        ### Success Criteria
        - All [WIRE:] tasks marked [X] are verified in code
        - Component imports exist in target screens
        - Component instantiations exist in render/compose
        - No orphan components (imported but not used)
        - Placeholder warnings reviewed
      model_override: sonnet
    - role: code-reviewer
      role_group: REVIEW
      parallel: false
      depends_on: [unit-test-generator, integration-test-generator, property-test-generator]
      priority: 3
      trigger: "when reviewing implementation"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        Tasks: {{FEATURE_DIR}}/tasks.md

        ## Task
        Review implementation quality:
        1. Check @speckit annotations are present
        2. Verify no TODO/FIXME/HACK comments remain
        3. Run linter and fix warnings
        4. Check DoD compliance per tasks.md

        ## Success Criteria
        - All FRs traceable via @speckit:FR-xxx
        - Lint passes with 0 errors
        - No security vulnerabilities (no hardcoded secrets)
    - role: changelog-updater
      role_group: DOCUMENTATION
      parallel: false
      depends_on: [code-reviewer]
      priority: 2
      trigger: "after code review passes"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        Tasks: {{FEATURE_DIR}}/tasks.md

        ## Your Role
        You ensure CHANGELOG.md is updated with the completed feature.

        ## Pre-check
        1. Read spec.md to get feature title and acceptance scenarios (AS-xxx)
        2. Read tasks.md to get story ID and FR-xxx markers
        3. Check if CHANGELOG.md exists at project root

        ## Skip Conditions
        Return early if ANY of these conditions are met:
        - Story title contains [INTERNAL] or [NO-CHANGELOG]
        - All tasks are Wave 1-2 only (infrastructure tasks)
        - No FR-xxx markers found in tasks.md

        ## Action
        1. IF CHANGELOG.md does not exist:
           - Create it with Keep a Changelog header:
             ```markdown
             # Changelog

             All notable changes to this project will be documented in this file.

             The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
             and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

             ## [Unreleased]
             ```

        2. Extract from artifacts:
           - Story ID and title from tasks.md header
           - AS-xxx descriptions from spec.md acceptance scenarios
           - FR-xxx markers from completed tasks

        3. Generate entry under ## [Unreleased] → ### Added:
           ```markdown
           - **[{story_id}] {story_title}** (spec: {feature_dir}/spec.md)
             - {AS-1A description}
             - {AS-1B description}
             - Implements: FR-001, FR-002
             - Tests: AS-1A ✅, AS-1B ✅
           ```

        4. Prepend to existing ### Added section (or create section if missing)

        ## Success Criteria
        - CHANGELOG.md exists with valid Keep a Changelog format
        - New feature entry appears under ## [Unreleased] → ### Added
        - Entry includes story ID, title, AS-xxx descriptions, and FR-xxx markers

        ## Output
        Report one of:
        ```
        📝 Changelog Updated:
        - Feature: {story_title}
        - Acceptance scenarios: N
        - Requirements: FR-001, FR-002
        → CHANGELOG.md updated ✅
        ```

        OR if skipped:
        ```
        📝 Changelog Skipped:
        - Reason: {reason}
        ```
      model_override: haiku
    - role: documentation-generator
      role_group: DOCS
      parallel: true
      depends_on: [code-reviewer, changelog-updater]
      priority: 2
      trigger: "when generating documentation"
      prompt: |
        ## Context
        Feature: {{FEATURE_DIR}}
        Spec: {{FEATURE_DIR}}/spec.md
        Plan: {{FEATURE_DIR}}/plan.md
        Constitution: memory/constitution.md
        Implementation: (from all builders)

        ## Task - Comprehensive Documentation Generation

        Generate multi-role documentation from implementation artifacts:

        ### Core Documentation (existing functionality)
        1. **RUNNING.md**: Startup instructions and developer setup
        2. **README.md**: Feature description and quick start
        3. **.env.example**: Required environment variables with descriptions
        4. **API Documentation**: OpenAPI specs (if applicable)

        ### User-Facing Documentation (new)
        5. **User Guide Expansion**:
           - Read docs/user-guide/outline.md (generated by /speckit.specify)
           - Read templates/docs/user-guide-section.md for structure
           - FOR EACH feature in outline:
             - Extract implementation details from code
             - Extract examples from Acceptance Scenarios (AS-xxx)
             - Generate docs/user-guide/{feature-slug}.md with:
               * Prerequisites
               * Step-by-step instructions with code examples
               * Screenshots/diagrams placeholders (mark [TODO: Screenshot])
               * Common use cases
               * Tips and best practices
               * Related features links

        6. **FAQ Expansion**:
           - Read docs/faq/seeds.md (generated by /speckit.specify)
           - Read templates/docs/faq-template.md for structure
           - FOR EACH FAQ seed:
             - Expand with detailed step-by-step solutions
             - Add code examples from implementation
             - Link to related troubleshooting docs
           - Generate docs/faq/index.md (full FAQ)

        ### Admin/Operations Documentation (new)
        7. **Installation Guide**:
           - Read templates/docs/installation-guide.md for structure
           - Extract setup steps from RUNNING.md
           - Extract system requirements from memory/constitution.md (if specified)
           - Extract infrastructure dependencies from plan.md
           - Generate docs/installation/detailed-setup.md with:
             * System prerequisites
             * Three installation methods: Quick Start (Docker), Development Setup, Production Deployment
             * Verification steps
             * Troubleshooting common setup issues

        8. **Troubleshooting Guide**:
           - Read templates/docs/troubleshooting-section.md for structure
           - Analyze implemented error handling code for common error patterns
           - Extract error scenarios from spec.md Acceptance Scenarios (ERROR_PATH, BOUNDARY)
           - Extract validation errors and their messages
           - Generate docs/troubleshooting/common-issues.md with:
             * Quick diagnostic checks
             * Common errors with solutions
             * Diagnostic tools and commands
             * Error reference table

        ### Developer Documentation (new)
        9. **Contributing Guidelines**:
           - Read templates/docs/contributing-template.md for structure
           - Extract principles from memory/constitution.md
           - Extract code style from code analysis (naming conventions, patterns)
           - Extract testing requirements from plan.md and test setup
           - Extract git workflow from repository patterns
           - Generate docs/contributing/guidelines.md with:
             * Code of conduct (from constitution values)
             * Development workflow (setup, branch naming, commit format)
             * Coding standards (style guide, linting rules)
             * Testing requirements (coverage, test types)
             * Pull request process

        ### Documentation Index (new)
        10. **Generate Documentation Index**:
            - Create docs/README.md as documentation hub:
              ```markdown
              # {Project Name} Documentation

              > **Last Updated**: {timestamp}
              > **Version**: {version}

              ## Documentation by Role

              ### 👤 End Users
              - [User Guide](./user-guide/) - Feature tutorials and guides
              - [FAQ](./faq/index.md) - Frequently asked questions
              - [Glossary](./glossary/index.md) - Terms and definitions

              ### 🔧 Administrators
              - [Installation](./installation/detailed-setup.md) - Setup instructions
              - [Deployment](./admin-guide/deployment.md) - Production deployment
              - [Troubleshooting](./troubleshooting/common-issues.md) - Problem diagnosis

              ### 💻 Developers
              - [Architecture](./architecture/overview.md) - System design
              - [API Reference](./api-reference/index.md) - API documentation
              - [Contributing](./contributing/guidelines.md) - Development guide

              ## Quick Start

              {Extract quick start from README.md}

              ## Need Help?

              - **Issues**: [Report bugs]({issues_url})
              - **Discussions**: [Ask questions]({discussions_url})
              - **Documentation**: [Full documentation]({docs_url})
              ```

        ## Generation Strategy

        **Use template-based generation**:
        - Read template files from templates/docs/*.md
        - Extract structured data from spec.md, plan.md, constitution.md
        - Fill template placeholders with actual project data
        - Maintain consistent formatting across all docs

        **Preserve manual edits**:
        - Check for `<!-- MANUAL SECTION -->` markers
        - Preserve content between markers when regenerating
        - Only update sections marked with `<!-- speckit:auto:* -->` markers

        **Cross-reference linking**:
        - Link related documentation (User Guide ↔ FAQ ↔ Troubleshooting)
        - Link to code examples in repository
        - Link glossary terms on first mention
        - Use relative paths for internal links

        ## Success Criteria
        - ✅ RUNNING.md has complete setup steps
        - ✅ README.md reflects new features
        - ✅ All env vars documented in .env.example
        - ✅ User guides expanded with step-by-step instructions
        - ✅ FAQ has detailed answers with code examples
        - ✅ Installation guide covers all setup methods
        - ✅ Troubleshooting guide covers common errors
        - ✅ Contributing guide reflects constitution principles
        - ✅ Documentation index (docs/README.md) created
        - ✅ All documentation cross-referenced

        ## Output Summary

        Log documentation generation results:
        ```text
        📚 Documentation Generated:

        Core:
        ✅ RUNNING.md (developer setup)
        ✅ README.md (project overview)
        ✅ .env.example ({var_count} variables)

        User-Facing:
        ✅ docs/user-guide/ ({feature_count} feature guides)
        ✅ docs/faq/index.md ({question_count} questions)

        Admin/Operations:
        ✅ docs/installation/detailed-setup.md (3 methods)
        ✅ docs/troubleshooting/common-issues.md ({error_count} errors)

        Developer:
        ✅ docs/contributing/guidelines.md

        Index:
        ✅ docs/README.md (documentation hub)

        💡 All documentation ready for review
        ```
      model_override: haiku
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
- `templates/shared/core/language-loading.md`
- `templates/shared/complexity-scoring.md`
- `FEATURE_DIR/tasks.md` (required - will be resolved after script runs)
- `FEATURE_DIR/plan.md` (required - will be resolved after script runs)
- `FEATURE_DIR/spec.md` (if exists)
- `FEATURE_DIR/checklists/*.md` (if directory exists)

CACHE all results with session lifetime.
REPORT: "Prefetched {N} files in {T}ms"
```

**Why prefetch?** Loading 5-8 files in parallel (300ms) vs sequential (2-3s) saves 2+ seconds per command invocation.

---

## Outline

### Performance Optimizations Summary

This command includes multiple performance optimizations for 50-65% faster execution:

| Optimization | Module | Savings | Skip Flag |
|--------------|--------|---------|-----------|
| **Task-Level Batching** | `templates/shared/implement/task-batching.md` | **60-75%** | `--sequential-tasks` |
| **Parallel Agent Orchestration** | `templates/shared/orchestration-instructions.md` | 20-30% | `--sequential` |
| Vision Turbo Mode | `templates/shared/implement/vision-turbo.md` | 75-80% | `--no-turbo` |
| API Batch Verification | `templates/shared/implement/api-batch.md` | 70% | `--no-batch-verify` |
| Wave Overlap Execution | `templates/shared/implement/wave-overlap.md` | 25-30% | `--sequential-waves` |
| Build Optimizer | `templates/shared/implement/build-optimizer.md` | 50% | `--no-build-fix` |
| Model Selection | `templates/shared/implement/model-selection.md` | 60-90% cost | `--no-adaptive-model` |
| **Streaming Output** | `orchestration-instructions.md` → "Streaming Output" | Real-time visibility | `--no-streaming` or `--quiet` |
| File Caching | Inline (Step 3) | 85% | N/A |
| **Auto Staging** | `staging_auto_provision` | Skip manual staging setup | Default ON, `--no-auto-staging` to disable |
| **Autonomous Mode** | Inline (below) | Unattended execution | Default OFF, `--autonomous` to enable |

{{include: shared/orchestration-instructions.md}}

### AUTONOMOUS EXECUTION MODE

> **⚠️ MANDATORY BEHAVIOR WHEN `--autonomous` OR `--auto` FLAG IS SET**
>
> This section defines REQUIRED behavior for Claude Code CLI. Violations break user trust.
> These rules OVERRIDE default Claude Code behavior for summaries, todos, and pauses.

#### Tool Restrictions in Autonomous Mode

| Tool | Allowed | Notes |
|------|---------|-------|
| **TodoWrite** | ❌ FORBIDDEN | Do NOT create or update todos - track progress internally only |
| **AskUserQuestion** | ❌ FORBIDDEN | Do NOT ask questions or request confirmation |
| **Text summaries** | ❌ FORBIDDEN | Do NOT output multi-line summaries between waves |
| **Progress indicators** | ✅ REQUIRED | Single-line only: `✓ Wave N complete (X/Y tasks)` |
| **Final summary** | ✅ REQUIRED | Only after ALL waves complete (Wave 5) |

#### Execution Pattern

```text
START → Wave0 → Wave1 → Wave2 → Wave3 → Wave3.5 → Wave4 → Wave5 → SUMMARY → END
         │        │       │        │         │         │        │
      (silent) (silent) (silent) (silent) (silent) (silent) (silent)
         │        │       │        │         │         │        │
         └────────┴───────┴────────┴─────────┴─────────┴────────┘
                         NO PAUSES, NO SUMMARIES
```

#### DO NOT (Autonomous Mode):

- ❌ Pause between waves for any reason
- ❌ Generate summaries or status updates between waves
- ❌ Use TodoWrite tool to track progress
- ❌ Ask for confirmation before proceeding
- ❌ Output reflection, planning, or thinking text
- ❌ Create intermediate "progress reports"
- ❌ Wait for user response at any point

#### DO (Autonomous Mode):

- ✅ Execute waves sequentially without stopping
- ✅ Emit ONLY single-line progress after each wave: `✓ Wave 2 complete (5/5 tasks)`
- ✅ Continue immediately to next wave after progress line
- ✅ Output comprehensive summary ONLY after Wave 5 completes
- ✅ Handle errors silently with auto-recovery when possible
- ✅ Log errors to implementation log, continue execution

#### Only Stop Execution For:

- Critical errors that cannot be auto-recovered
- Blocking quality gate failures (when configured to block)
- Build/test failures that require human intervention
- Explicit user interruption (Ctrl+C)

#### Autonomous Mode Summary Format

When `--autonomous` flag was set, output this format ONLY at the END:

```markdown
## Implementation Complete (Autonomous Mode)

**Duration**: Xm Ys | **Waves**: 6/6 | **Tasks**: N/N

| Wave | Tasks | Status |
|------|-------|--------|
| 0 - Staging | 2/2 | ✓ |
| 1 - Infrastructure | 3/3 | ✓ |
| 2 - Test Scaffolding | 5/5 | ✓ |
| 3 - Core Implementation | 8/8 | ✓ |
| 3.5 - PBT Validation | 2/2 | ✓ |
| 4 - Test Verification | 3/3 | ✓ |
| 5 - Polish | 2/2 | ✓ |

**Files modified**: X | **Tests added**: Y | **Coverage**: Z%

### Changes Summary
[Detailed implementation summary here]
```

### Wave Execution with Streaming

During parallel execution, apply streaming output for real-time visibility:

1. **Before wave**: Emit wave header with agent list and progress bar
2. **During wave**: Emit checkpoint after each agent completes (✓/✗ status)
3. **At 80% threshold**: Announce overlap trigger if wave overlap enabled
4. **After wave**: Emit collapsed summary, proceed to next wave

**Output format** (per checkpoint):
```text
🌊 Wave 2/4 - Core Implementation
├── Progress: [████████████░░░░░░░░] 60%
├── Agents: 3/5
├── Elapsed: 45s | Tokens: 89,230
│
├── ✓ data-layer-builder [sonnet]: 22s
├── ✓ api-builder [sonnet]: 35s
├── ⏳ ui-feature-builder [sonnet]: running...
├── ⏸ state-manager: waiting
```

**Reference**: See `templates/shared/orchestration-instructions.md` → "Streaming Output" section for full format.

**Expected Impact** (MODERATE complexity feature):
- Sequential time: 400s → Optimized: ~180s (55% faster)
- Cost: $18.50 → ~$6.20 (66% savings with adaptive models)

---

<!-- ═══════════════════════════════════════════════════════════════════════════
     AUTONOMOUS MODE REMINDER: If --autonomous/--auto flag is set:
     • DO NOT use TodoWrite
     • DO NOT output summaries between waves
     • DO NOT pause or ask questions
     • ONLY emit: "✓ Wave N complete (X/Y tasks)"
     • ONLY output full summary after Wave 5 completes
     ═══════════════════════════════════════════════════════════════════════════ -->

1. Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Check checklists status** (if FEATURE_DIR/checklists/ exists):
   - Scan all checklist files in the checklists/ directory
   - For each checklist, count:
     - Total items: All lines matching `- [ ]` or `- [X]` or `- [x]`
     - Completed items: Lines matching `- [X]` or `- [x]`
     - Incomplete items: Lines matching `- [ ]`
   - Create a status table:

     ```markdown
     | Checklist | Total | Completed | Incomplete | Status |
     |-----------|-------|-----------|------------|--------|
     | ux.md     | 12    | 12        | 0          | ✓ PASS |
     | test.md   | 8     | 5         | 3          | ✗ FAIL |
     | security.md | 6   | 6         | 0          | ✓ PASS |
     ```

   - Calculate overall status:
     - **PASS**: All checklists have 0 incomplete items
     - **FAIL**: One or more checklists have incomplete items

   - **If any checklist is incomplete**:
     - Display the table with incomplete item counts
     - **IF `--autonomous` flag is set**:
       - Log warning: "⚠️ AUTONOMOUS MODE: Proceeding with {N} incomplete checklist items"
       - Automatically proceed to step 3 (no user prompt)
     - **ELSE (interactive mode)**:
       - **STOP** and ask: "Some checklists are incomplete. Do you want to proceed with implementation anyway? (yes/no)"
       - Wait for user response before continuing
       - If user says "no" or "wait" or "stop", halt execution
       - If user says "yes" or "proceed" or "continue", proceed to step 3

   - **If all checklists are complete**:
     - Display the table showing all checklists passed
     - Automatically proceed to step 3

3. Load and analyze the implementation context:

   **File Caching Strategy** (reduces redundant reads by 85%):
   ```text
   ON_FIRST_READ(file_path):
     content = read_file(file_path)
     MEMORY_CACHE[file_path] = {content, mtime: get_mtime(file_path)}
     RETURN content

   ON_SUBSEQUENT_READ(file_path):
     IF file_path IN MEMORY_CACHE:
       IF get_mtime(file_path) == MEMORY_CACHE[file_path].mtime:
         RETURN MEMORY_CACHE[file_path].content  # Cache hit
     RETURN ON_FIRST_READ(file_path)  # Cache miss or stale

   ON_FILE_EDIT(file_path):
     INVALIDATE MEMORY_CACHE[file_path]  # Clear on write
   ```

   - **REQUIRED**: Read tasks.md for the complete task list and execution plan
   - **REQUIRED**: Read plan.md for tech stack, architecture, and file structure
   - **IF EXISTS**: Read plan.md Dependency Registry for API documentation references
   - **IF EXISTS**: Read data-model.md for entities and relationships
   - **IF EXISTS**: Read contracts/ for API specifications and test requirements
   - **IF EXISTS**: Read research.md for technical decisions and constraints
   - **IF EXISTS**: Read quickstart.md for integration scenarios

3.5. **API Documentation Verification** (before implementation):

   **Purpose**: Verify API documentation references before coding to prevent hallucinations.

   **Performance Optimization**: Read `templates/shared/implement/api-batch.md` for batched verification.
   - Batch all [DEP:] and [APIDOC:] markers for parallel verification
   - Use session cache (`.cache/api-verification.yaml`) with 1-hour TTL
   - Expected savings: 70% (25-40s → 8-12s)

   **For each task with [DEP:xxx] or [APIDOC:url] marker:**

   a) **Retrieve documentation context**:
      - IF [APIDOC:url] present: Use WebFetch to retrieve documentation section
      - IF [DEP:xxx] present: Look up Dependency Registry in plan.md for docs URL
      - IF Context7 MCP available: Use `resolve-library-id` → `get-library-docs`

   b) **Pre-flight verification**:
      ```text
      FOR EACH method/endpoint referenced in task:
        1. Search documentation for method signature
        2. Verify parameters match expected usage
        3. Check for deprecation notices
        4. Note any version-specific behavior
      ```

   c) **Pre-flight check output**:
      ```text
      Task T025 [DEP:API-001] API Verification:
      ✓ Stripe charges.create() - Verified in API v2024-12-18
      ✓ Parameters: amount, currency, source - All valid
      ⚠ Note: 'source' deprecated in favor of 'payment_method' (2024+)

      Task T030 [DEP:PKG-002] API Verification:
      ✓ react-query useQuery() - Verified in v5.x docs
      ✓ Options: queryKey, queryFn - Valid
      ```

   d) **Block on verification failure**:
      ```text
      IF API/method not found in documentation:
        → Report: "⛔ API verification failed: {method} not found in {docs_url}"
        → IF `--autonomous` flag is set:
          → Log warning: "⚠️ AUTONOMOUS MODE: Proceeding with unverified API ({method})"
          → CONTINUE implementation (risky, no user prompt)
        → ELSE:
          → STOP implementation for this task
          → SUGGEST: "Check dependency version in Dependency Registry"
          → SUGGEST: "Use Context7 to fetch current documentation"
          → ASK user: "Proceed anyway (risky) or fix Dependency Registry first?"
      ```

   e) **Skip conditions**:
      - Tasks without [DEP:] or [APIDOC:] markers
      - Internal project dependencies (no external docs)
      - Setup/configuration tasks

3.6. **Design System Context Loading** (if `design_system` configured):

   **Purpose**: Load design system tokens and component library context to enforce DSS principles during code generation.

   **Activation check**:
   ```text
   IF exists(design_system block in constitution.md) AND enforcement_level != "off":
     LOAD design system context
   ELSE:
     SKIP this step
   ```

   **Context loading steps**:

   a) **Parse design_system configuration**:
      ```text
      1. Read memory/constitution.md
      2. Extract design_system YAML block
      3. IF preset specified:
         - Load preset from templates/shared/design-system-presets.md
         - Merge with any custom overrides
      4. Validate required fields: framework, enforcement_level
      ```

   b) **Prepare framework documentation context**:
      ```text
      IF component_library_url is specified:
        - IF Context7 MCP available:
          → resolve-library-id for framework
          → get-library-docs with topic="components"
        - ELSE:
          → Store URL for reference in agent prompts
      ```

   c) **Inject design system context into agents**:
      ```text
      FOR EACH subagent WITH role_group = FRONTEND:
        APPEND to agent prompt:
          "## Design System Tokens (from constitution.md)
           Framework: {framework}
           Enforcement: {enforcement_level}

           ### Color Tokens - USE THESE, NOT HARDCODED VALUES
           {colors as CSS variables or theme object}

           ### Typography Tokens
           {typography scale}

           ### Component Library
           {component_library_url}
           Prefer library components over custom implementations.

           ### DSS Enforcement Rules
           - DSS-001: Use library components before custom
           - DSS-002: All colors via tokens (MUST)
           - DSS-003: Typography via scale tokens (SHOULD)"
      ```

   d) **Set enforcement instructions based on level**:
      ```text
      IF enforcement_level == "strict":
        INSTRUCT agents: "BLOCK on any DSS violation. Do not proceed with hardcoded colors."
      ELIF enforcement_level == "warn":
        INSTRUCT agents: "WARN on DSS violations but continue. Flag for self-review."
      ```

   e) **Report context loaded**:
      ```text
      📐 Design System Context Loaded:
      ├── Framework: {framework}
      ├── Enforcement: {enforcement_level}
      ├── Color tokens: {count} defined
      ├── Typography scale: {count} sizes
      ├── Component library docs: {loaded|not available}
      └── Agents updated: FRONTEND role_group
      ```

   **Skip conditions**:
   - No `design_system` block in constitution.md
   - `enforcement_level: "off"`
   - Feature has no FRONTEND role_group tasks

3.7. **Apply Adaptive Model Routing**:

   **Purpose**: Dynamically select optimal model (haiku/sonnet/opus) per subagent based on feature complexity.

   **Skip flag**: `--no-adaptive-model`

   **Execution**:
   ```text
   IF "--no-adaptive-model" NOT in user input:

     1. Execute determine_complexity_tier(FEATURE_DIR)
        → Analyze spec.md for user stories, FRs, APIs, tech signals
        → Calculate score (0-100)
        → Determine tier: TRIVIAL/SIMPLE/MODERATE/COMPLEX

     2. Execute apply_model_routing(subagents, tier)
        → Apply MODEL_ROUTING_MATRIX[tier][role_group] to each subagent
        → Respect explicit model_override (skip routing for those)
        → Set model_override on remaining subagents

     3. Execute report_routing(assignments, tier, score)
        → Display model distribution and cost savings
        → Show per-agent assignments with reasoning

   ELSE:
     LOG "⚡ Adaptive routing DISABLED (using template defaults)"
   ```

   **Expected Output**:
   ```text
   🎯 Adaptive Model Routing
   ├── Complexity: SIMPLE (score: 38/100)
   ├── Models: haiku(4) sonnet(5) opus(1)
   ├── Assignments:
   │   └── project-scaffolder: haiku (SIMPLE/INFRA)
   │   └── dependency-installer: haiku (SIMPLE/INFRA)
   │   └── data-layer-builder: sonnet (SIMPLE/BACKEND)
   │   └── api-builder: sonnet (SIMPLE/BACKEND)
   │   └── ui-foundation-builder: sonnet (SIMPLE/FRONTEND)
   │   └── unit-test-generator: haiku (SIMPLE/TESTING)
   │   └── self-reviewer: sonnet (SIMPLE/REVIEW)
   │   └── documentation-generator: haiku (explicit)
   ├── Cost: $0.089 (vs $0.600 all-opus)
   └── Savings: $0.511 (85%)
   ```

   **Reference**: See `templates/shared/orchestration-instructions.md` → "Adaptive Model Routing" section for full algorithm.

4. **Project Setup Verification**:
   - **REQUIRED**: Create/verify ignore files based on actual project setup:

   **Detection & Creation Logic**:
   - Check if the following command succeeds to determine if the repository is a git repo (create/verify .gitignore if so):

     ```sh
     git rev-parse --git-dir 2>/dev/null
     ```

   - Check if Dockerfile* exists or Docker in plan.md → create/verify .dockerignore
   - Check if .eslintrc* exists → create/verify .eslintignore
   - Check if eslint.config.* exists → ensure the config's `ignores` entries cover required patterns
   - Check if .prettierrc* exists → create/verify .prettierignore
   - Check if .npmrc or package.json exists → create/verify .npmignore (if publishing)
   - Check if terraform files (*.tf) exist → create/verify .terraformignore
   - Check if .helmignore needed (helm charts present) → create/verify .helmignore

   **If ignore file already exists**: Verify it contains essential patterns, append missing critical patterns only
   **If ignore file missing**: Create with full pattern set for detected technology

   **Common Patterns by Technology** (from plan.md tech stack):
   - **Node.js/JavaScript/TypeScript**: `node_modules/`, `dist/`, `build/`, `*.log`, `.env*`
   - **Python**: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/`, `*.egg-info/`
   - **Java**: `target/`, `*.class`, `*.jar`, `.gradle/`, `build/`
   - **C#/.NET**: `bin/`, `obj/`, `*.user`, `*.suo`, `packages/`
   - **Go**: `*.exe`, `*.test`, `vendor/`, `*.out`
   - **Ruby**: `.bundle/`, `log/`, `tmp/`, `*.gem`, `vendor/bundle/`
   - **PHP**: `vendor/`, `*.log`, `*.cache`, `*.env`
   - **Rust**: `target/`, `debug/`, `release/`, `*.rs.bk`, `*.rlib`, `*.prof*`, `.idea/`, `*.log`, `.env*`
   - **Kotlin**: `build/`, `out/`, `.gradle/`, `.idea/`, `*.class`, `*.jar`, `*.iml`, `*.log`, `.env*`
   - **C++**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.so`, `*.a`, `*.exe`, `*.dll`, `.idea/`, `*.log`, `.env*`
   - **C**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.a`, `*.so`, `*.exe`, `Makefile`, `config.log`, `.idea/`, `*.log`, `.env*`
   - **Swift**: `.build/`, `DerivedData/`, `*.swiftpm/`, `Packages/`
   - **R**: `.Rproj.user/`, `.Rhistory`, `.RData`, `.Ruserdata`, `*.Rproj`, `packrat/`, `renv/`
   - **Universal**: `.DS_Store`, `Thumbs.db`, `*.tmp`, `*.swp`, `.vscode/`, `.idea/`

   **Tool-Specific Patterns**:
   - **Docker**: `node_modules/`, `.git/`, `Dockerfile*`, `.dockerignore`, `*.log*`, `.env*`, `coverage/`
   - **ESLint**: `node_modules/`, `dist/`, `build/`, `coverage/`, `*.min.js`
   - **Prettier**: `node_modules/`, `dist/`, `build/`, `coverage/`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - **Terraform**: `.terraform/`, `*.tfstate*`, `*.tfvars`, `.terraform.lock.hcl`
   - **Kubernetes/k8s**: `*.secret.yaml`, `secrets/`, `.kube/`, `kubeconfig*`, `*.key`, `*.crt`

5. **Update Feature Manifest** (mark as IMPLEMENTING):
   ```text
   MANIFEST_FILE = specs/features/.manifest.md
   FEATURE_ID = extract from current branch/feature (first 3 digits)

   IF exists(MANIFEST_FILE):
     Find row where ID = FEATURE_ID
     IF Status != IMPLEMENTING:
       Update Status column: TASKED → IMPLEMENTING
       Update "Last Updated" column: today's date
   ```

5.5. **Update Concept Traceability - IMPLEMENTING** (if concept.md exists):

   ```text
   IF exists("specs/concept.md"):
     1. Read concept.md
     2. Find "Traceability Skeleton" section

     3. Extract CONCEPT_IDS from spec.md (via tasks.md traceability headers):
        - Source: "Concept IDs Covered" in tasks.md or spec.md

     4. FOR EACH concept_id in CONCEPT_IDS:
        Find row in Traceability Skeleton where Concept ID = concept_id
        IF Status != "IMPLEMENTING" AND Status != "IMPLEMENTED":
          UPDATE row:
            - "Status": "IMPLEMENTING"

     5. Update "Progress Rollup" section:
        - Recount statuses across all rows
        - Update percentages

     6. Set "Last Updated": "{today's date} by /speckit.implement (start)"

     7. Write updated concept.md
   ```

   Report: "Concept traceability updated: {CONCEPT_IDS} → IMPLEMENTING"

6. Parse tasks.md structure and extract:
   - **Task phases**: Setup, Tests, Core, Integration, Polish
   - **Task dependencies**: Sequential vs parallel execution rules
   - **Task details**: ID, description, file paths, parallel markers [P]
   - **Execution flow**: Order and dependency requirements

7. Execute implementation following the task plan:

   **Performance Optimizations**:
   - **Task-Level Batching** (PRIMARY): Read `templates/shared/implement/task-batching.md`
     - Group independent tasks into batches (4-8 tasks per batch)
     - Execute ALL tasks in batch as parallel Task tool calls in **SINGLE message**
     - Expected savings: 60-75% (N round-trips → N/4-8 round-trips)
     - Skip with `--sequential-tasks` flag
   - **Wave Overlap**: Read `templates/shared/implement/wave-overlap.md` for speculative execution
     - Start Wave N+1 when Wave N is 80% complete (not 100%)
     - Expected savings: 25-30% (220-340s → 160-250s)
   - **Complexity-Adaptive**: Read `templates/shared/implement/model-selection.md`
     - Select model (haiku/sonnet/opus) based on complexity tier
     - TRIVIAL: Skip vision validation, use haiku (90% cost savings)
     - SIMPLE: Single viewport, abbreviated review (60-80% savings)
     - MODERATE/COMPLEX: Full workflow with opus

   - **Batch-first execution**: Group tasks by topological level, execute batches
   - **Respect dependencies**: Tasks with [DEP:Txxx] wait for dependency completion
   - **Follow TDD approach**: Execute test tasks before their corresponding implementation tasks
   - **File-based coordination**: Tasks affecting the same files must run sequentially
   - **Validation checkpoints**: Use progressive validation (Tier 1-2 BLOCKING, Tier 3-4 non-blocking/async). See `templates/shared/validation/checkpoints.md`
   - **⚠️ MANDATORY**: After completing each task, IMMEDIATELY mark it as `[X]` in tasks.md (see Step 9)

8. Implementation execution rules:
   - **Setup first**: Initialize project structure, dependencies, configuration
   - **Tests before code**: If you need to write tests for contracts, entities, and integration scenarios
   - **Core development**: Implement models, services, CLI commands, endpoints
   - **Integration work**: Database connections, middleware, logging, external services
   - **Polish and validation**: Unit tests, performance optimization, documentation

   **Traceability Annotations (AUTO-GENERATED)**:

   When creating or modifying code for a task, automatically add `@speckit` annotations to enable bidirectional traceability between specifications and code:

   a) **For tasks with [FR:FR-xxx] marker**:
      - Add `# @speckit:FR:FR-xxx` comment ABOVE the primary function/class/component
      - If multiple FRs: `# @speckit:FR:FR-001,FR-002`
      - Include brief description: `# @speckit:FR:FR-001 - User authentication handler`

   b) **For tasks with [TEST:AS-xxx] marker**:
      - Add `# @speckit:AS:AS-xxx` comment ABOVE the test function
      - Reference scenario: `# @speckit:AS:AS-1A - Given valid credentials, When login, Then success`

   c) **For tasks with edge case handling [EC:EC-xxx] marker**:
      - Add `# @speckit:EC:EC-xxx` comment at edge case handling location

   d) **For tasks with [VR:VR-xxx] or [IR:IR-xxx] markers** (UI features):
      - Add `# @speckit:VR:VR-xxx` or `# @speckit:IR:IR-xxx` above UI component

   **Annotation Placement Guidelines**:
   - Place immediately ABOVE function/method/class definition (not inside)
   - For multi-file implementations: annotate the primary entry point
   - For React/Vue components: annotate the component definition
   - For tests: annotate each test function separately
   - Use language-appropriate comment syntax: `#` (Python, Ruby), `//` (JS, Go, Rust, C), `--` (SQL, Lua)

   **Examples by Language**:
   ```python
   # @speckit:FR:FR-001,FR-002 - User authentication handler
   def authenticate_user(email: str, password: str) -> User:
       pass

   # @speckit:AS:AS-1A - Given valid credentials, When login, Then success
   def test_login_success():
       pass
   ```
   ```typescript
   // @speckit:FR:FR-003 - Payment processing service
   export class PaymentService {
   ```
   ```go
   // @speckit:EC:EC-001 - Handle empty password edge case
   func validatePassword(password string) error {
   ```

9. **Task Completion Protocol** (⛔ BLOCKING ⛔):

   ┌──────────────────────────────────────────────────────────────┐
   │  🚨 THIS IS THE MOST IMPORTANT STEP - DO NOT SKIP  🚨        │
   │                                                              │
   │  After completing EACH task, you MUST:                       │
   │  1. ✅ Complete the task implementation                      │
   │  2. ✅ Edit tasks.md: `[ ]` → `[X]`                          │
   │  3. ✅ Verify the edit succeeded                             │
   │  4. ✅ Report completion (see mode below)                    │
   │  5. ⚠️  ONLY THEN proceed to next task                       │
   │                                                              │
   │  ⛔ NEVER proceed without updating tasks.md first ⛔          │
   │                                                              │
   │  📌 AUTONOMOUS MODE (--auto): Skip step 4, continue silently │
   │     - Do NOT output per-task progress reports                │
   │     - Do NOT use TodoWrite tool                              │
   │     - Continue immediately to next task                      │
   └──────────────────────────────────────────────────────────────┘

   a) **Mark task as complete**:
      ```text
      BEFORE: - [ ] T005 Implement user authentication service [FR:FR-001]
      AFTER:  - [X] T005 Implement user authentication service [FR:FR-001]
      ```

   b) **Update sequence** (after each task):
      1. Complete the task implementation
      2. Verify the task works (compile/test if applicable)
      3. **IMMEDIATELY** edit tasks.md to change `[ ]` → `[X]`
      4. Report progress to user
      5. Proceed to next task

   c) **Progress report format** (after marking task):

      **Interactive mode** (default):
      ```text
      ✓ T005 [FR:FR-001] Implement user authentication service - DONE
        Files: src/services/auth.ts, src/models/user.ts
        Progress: 5/12 tasks complete (42%)
      ```

      **Autonomous mode** (`--auto`): NO per-task output. Continue silently.

   d) **Error handling**:
      - Halt execution if any non-parallel task fails
      - For parallel tasks [P], continue with successful tasks, report failed ones
      - Provide clear error messages with context for debugging
      - If task cannot be completed, mark with `[!]` and explain:
        ```text
        - [!] T005 Implement user authentication service [FR:FR-001]
          ⚠️ BLOCKED: Missing database schema, need T003 first
        ```

   e) **Verification checkpoint** (every 3-5 tasks):

      **Interactive mode** (default):
      ```text
      📊 Progress Check:
      ├── Completed: T001, T002, T003, T004, T005 (5 tasks)
      ├── Remaining: T006, T007, T008... (7 tasks)
      ├── Blocked: none
      └── Next: T006 - Create API endpoints
      ```

      **Autonomous mode** (`--auto`): Skip checkpoints. Only emit wave completion:
      `✓ Wave 2 complete (5/5 tasks)`

10. **Definition of Done (DoD)** — Per User Story:

   Before marking a user story as complete, verify ALL of the following:

   **Test Coverage**:
   - [ ] All `[TEST:AS-xxx]` tasks for this story are marked `[X]`
   - [ ] All tests pass locally (run test command for story)
   - [ ] No `[TEST:AS-xxx]` tasks skipped without `[NO-TEST:]` justification

   **Traceability**:
   - [ ] `@speckit:AS:AS-xxx` annotations present in test code
   - [ ] `@speckit:FR:FR-xxx` annotations present in implementation code
   - [ ] TTM in tasks.md updated with test file paths

   **Validation Gate**:
   ```text
   IF story has AS with "Requires Test = YES" in spec.md:
     IF [TEST:AS-xxx] task not marked [X]:
       → BLOCK story completion
       → Message: "Story cannot proceed: test for AS-xxx not complete"
     IF tests fail:
       → BLOCK story completion
       → Message: "Story cannot proceed: tests failing"
   ```

   **DoD Checklist** (display after each story completion):
   ```text
   📋 Definition of Done - User Story 1:
   ✓ All implementation tasks [X]
   ✓ All test tasks [X] (T010, T011)
   ✓ Tests pass locally
   ✓ @speckit annotations added
   → Story COMPLETE ✅
   ```

   **Changelog Update** (after DoD passes):

   After a user story passes DoD validation, update `CHANGELOG.md`:

   a) **Check** if `CHANGELOG.md` exists at project root
      - If not exists: Create with standard header (Keep a Changelog format)

   b) **Extract** from completed story:
      - Story ID and title from tasks.md heading
      - Acceptance Scenarios (AS-xxx) descriptions from spec.md
      - Functional Requirements (FR-xxx) implemented (from task markers)
      - Feature directory path for spec reference

   c) **Generate** changelog entry under `## [Unreleased]` → `### Added`:
      ```markdown
      - **[{story_id}] {story_title}** (spec: {feature_dir}/spec.md)
        - {acceptance_scenario_1_description} (AS-1A)
        - {acceptance_scenario_2_description} (AS-1B)
        - Implements: FR-001, FR-002, FR-003
        - Tests: AS-1A ✅, AS-1B ✅
      ```

   d) **Append** entry preserving existing content (prepend to `### Added` section)

   **Skip changelog update if:**
   - Story is infrastructure/foundation (Wave 1-2) without user-facing behavior
   - Story marked as `[INTERNAL]` or `[NO-CHANGELOG]` in tasks.md
   - All tasks are setup/config tasks (no FR-xxx markers)

   **Example output:**
   ```text
   📝 Changelog Updated:
   Added entry for [US1] User Registration
   - 2 acceptance scenarios documented
   - 3 functional requirements linked
   → CHANGELOG.md updated ✅
   ```

11. Completion validation:
   - Verify all required tasks are completed
   - Check that implemented features match the original specification
   - Validate that tests pass and coverage meets requirements
   - Confirm the implementation follows the technical plan
   - Report final status with summary of completed work

12. **Traceability Verification** (after each phase completion):

    After completing implementation tasks in a phase, verify @speckit annotations are present:

    a) **Scan newly created/modified files** for @speckit annotations
    b) **Compare against tasks** completed in this phase that have [FR:], [TEST:], [EC:], [VR:], [IR:] markers
    c) **Report any missing annotations**:
       ```text
       ⚠️ Traceability Warning:
       - T012 [FR:FR-001] completed but src/models/user.py missing @speckit annotation
       - T020 [TEST:AS-1A] completed but tests/test_auth.py missing @speckit annotation

       Suggested fixes:
       - Add "# @speckit:FR:FR-001 - User data model" above User class
       - Add "# @speckit:AS:AS-1A - Valid login flow" above test_login_success()
       ```
    d) **Self-correct** by adding missing annotations before proceeding to next phase

    **Validation Regex** (for scanning code):
    ```text
    @speckit:(FR|AS|EC|VR|IR):([A-Z]+-\d+[A-Za-z]?)(,([A-Z]+-\d+[A-Za-z]?))*
    ```

    **When to skip**: Setup and Foundation phases typically don't have FR/AS markers, so traceability verification focuses on User Story phases.

13. **Test Validation Checkpoint** (per story, after all test tasks):

    After completing test tasks for a user story, validate tests are functional:

    a) **Run tests for story**:
       ```bash
       # Detect test framework from plan.md or package.json/pyproject.toml
       IF pytest: pytest -k "AS_1A or AS_1B" --tb=short
       IF jest: npm test -- --testPathPattern="AS.1A|AS.1B"
       IF vitest: vitest run --reporter=verbose --grep="AS.1A|AS.1B"
       ```

    b) **Validation logic**:
       ```text
       IF any test fails:
         → DO NOT proceed to next story
         → Display failing test details
         → Mark test task as [!] (needs attention) in tasks.md
         → Message: "Fix failing tests before proceeding"

       IF all tests pass:
         → Update TTM status to "✅ Passing"
         → Update test file path in TTM if placeholder
         → Proceed to next story
       ```

    c) **TTM Update** (automatic):
       ```text
       After test validation, update tasks.md TTM:
       | AS-1A | AS | YES | T010 | T003-T005 | tests/auth/test_login.py | ✅ |
       ```

    **Output Format**:
    ```text
    🧪 Test Checkpoint - User Story 1:
    Running: pytest -k "AS_1A or AS_1B"
    ✓ test_login_success (AS-1A) - PASSED
    ✓ test_login_failure (AS-1B) - PASSED
    → All 2 tests passing ✅

    TTM Updated:
    - AS-1A: ❌ → ✅ (tests/auth/test_login.py)
    - AS-1B: ❌ → ✅ (tests/auth/test_login.py)
    ```

14. **Documentation Generation** (after implementation complete):

    Create or update run instructions in `RUNNING.md` at repository root:

    a) **Detect project type and generate instructions**:
       ```text
       Analyze project structure from plan.md and package files:
       - package.json → Node.js/npm/yarn/pnpm commands
       - pyproject.toml/setup.py → Python/pip/uv commands
       - Cargo.toml → Rust/cargo commands
       - go.mod → Go commands
       - pom.xml/build.gradle → Java/Maven/Gradle commands
       - Gemfile → Ruby/bundler commands
       - docker-compose.yml → Docker commands
       ```

    b) **RUNNING.md structure**:
       ```markdown
       # Running the Application

       ## Prerequisites

       - [Runtime version from plan.md, e.g., Node.js 20+, Python 3.11+]
       - [Package manager, e.g., npm, uv, cargo]
       - [External dependencies, e.g., PostgreSQL, Redis] (from INFRA-xxx in plan.md)

       ## Installation

       ```bash
       # Clone and install dependencies
       [detected install command: npm install / uv sync / cargo build]
       ```

       ## Configuration

       Required environment variables:
       | Variable | Description | Default |
       |----------|-------------|---------|
       | DATABASE_URL | Database connection string | - |
       | ... | (extracted from code/plan.md) | ... |

       Copy `.env.example` to `.env` and configure:
       ```bash
       cp .env.example .env
       # Edit .env with your values
       ```

       ## Running

       ### Development
       ```bash
       [detected dev command: npm run dev / python -m app / cargo run]
       ```

       ### Production
       ```bash
       [detected prod command: npm start / gunicorn / cargo run --release]
       ```

       ### With Docker
       ```bash
       docker-compose up -d
       # or
       docker build -t app . && docker run -p 8080:8080 app
       ```

       ## Testing

       ```bash
       [detected test command: npm test / pytest / cargo test]
       ```

       ## Common Issues

       ### [Issue 1 - detected from implementation]
       **Symptom**: [description]
       **Solution**: [fix]

       ---
       *Auto-generated by Spec Kit /speckit.implement*
       ```

    c) **Update logic**:
       ```text
       IF RUNNING.md exists:
         - Parse existing sections
         - Update only sections that changed (preserve custom additions)
         - Add new sections for newly discovered requirements
         - Mark auto-generated sections with <!-- speckit:auto --> comments
       ELSE:
         - Create new RUNNING.md from template
       ```

    d) **Environment file generation**:
       ```text
       IF .env.example does not exist:
         - Scan code for environment variable references
         - Scan plan.md Infrastructure Dependencies for connection strings
         - Generate .env.example with placeholder values
       ```

15. **README.md Auto-Update** (after documentation generation):

    Create or update `README.md` at repository root:

    a) **Source data extraction**:
       ```text
       FROM spec.md:
         - Title: Feature name
         - Description: Objective section
         - Features: Functional Requirements list (FR-xxx)
         - User Stories: AS-xxx summaries

       FROM plan.md:
         - Tech Stack: Language/Version, Primary Dependencies
         - Architecture: Project Structure section
         - Infrastructure: INFRA-xxx dependencies

       FROM RUNNING.md:
         - Quick Start: Installation + Running sections
         - Prerequisites: Requirements section
       ```

    b) **README.md structure**:
       ```markdown
       # [Project Name]

       > [One-line description from spec.md Objective]

       ## Features

       - ✅ [FR-001 description]
       - ✅ [FR-002 description]
       - ... (from spec.md Functional Requirements)

       ## Tech Stack

       - **Runtime**: [from plan.md]
       - **Framework**: [from plan.md Primary Dependencies]
       - **Database**: [from plan.md INFRA-xxx]
       - **Cache**: [from plan.md INFRA-xxx]

       ## Quick Start

       ### Prerequisites

       - [from RUNNING.md Prerequisites]

       ### Installation

       ```bash
       [from RUNNING.md Installation]
       ```

       ### Running

       ```bash
       [from RUNNING.md Development command]
       ```

       ## Development

       See [RUNNING.md](./RUNNING.md) for detailed development instructions.

       ## Testing

       ```bash
       [from RUNNING.md Testing]
       ```

       ## Project Structure

       ```
       [from plan.md Project Structure, simplified]
       ```

       ## Documentation

       - [Specification](./specs/[feature]/spec.md)
       - [Implementation Plan](./specs/[feature]/plan.md)
       - [Task Breakdown](./specs/[feature]/tasks.md)

       ## License

       [Detect from LICENSE file or default to project standard]

       ---
       *Generated with [Spec Kit](https://github.com/sddevelopment-be/spec-kit) - Spec-Driven Development Toolkit*
       ```

    c) **Update strategy**:
       ```text
       IF README.md exists:
         - Detect sections marked with <!-- speckit:auto --> or <!-- speckit:managed -->
         - Update ONLY auto-managed sections
         - Preserve all custom sections (Contributing, Authors, Badges, etc.)
         - Add new auto sections if missing

       Section markers:
         <!-- speckit:auto:features --> ... <!-- /speckit:auto:features -->
         <!-- speckit:auto:quickstart --> ... <!-- /speckit:auto:quickstart -->
         <!-- speckit:auto:techstack --> ... <!-- /speckit:auto:techstack -->

       ELSE:
         - Create new README.md with full template
         - All sections marked as auto-managed
       ```

    d) **Multi-feature support**:
       ```text
       IF multiple features implemented (specs/features/001-*, 002-*, ...):
         - README Features section aggregates all feature FRs
         - Documentation section links to all feature specs
         - Quick Start uses most recent/primary feature setup
       ```

    e) **Output confirmation**:
       ```text
       📝 Documentation Updated:
       ├── RUNNING.md: Created/Updated (Prerequisites, Installation, Running, Testing)
       ├── .env.example: Created (12 environment variables)
       └── README.md: Updated (Features: +3, Tech Stack: synced)
       ```

16. **Update Concept Traceability - IMPLEMENTED** (after all P1 tasks complete):

   ```text
   IF exists("specs/concept.md"):
     1. Read concept.md
     2. Find "Traceability Skeleton" section

     3. Extract CONCEPT_IDS from spec.md (via tasks.md traceability headers)

     4. Gather test results from implementation:
        - Count passing tests for each story
        - Count total tests for each story
        - Determine overall test status

     5. FOR EACH concept_id in CONCEPT_IDS:
        Find row in Traceability Skeleton where Concept ID = concept_id
        UPDATE row:
          - "Tests": "{passing}/{total}" (e.g., "5/5" or "3/5")
          - "Status": "IMPLEMENTED"

     6. Update "Progress Rollup" section:
        - Recount statuses across all rows
        - Update percentages
        - Calculate: "N of M stories IMPLEMENTED"

     7. Update "Foundation Progress" section:
        - Check if all Wave 1 features are now IMPLEMENTED → mark Wave 1 complete
        - Check if all Wave 2 features are now IMPLEMENTED → mark Wave 2 complete
        - IF both Wave 1 and Wave 2 complete:
          → Update "Golden Path Status": "[x] Testable"

     8. Set "Last Updated": "{today's date} by /speckit.implement (complete)"

     9. Write updated concept.md
   ```

   Report summary:
   ```text
   📊 Concept Traceability Updated:
   ├── Stories: {CONCEPT_IDS} → IMPLEMENTED
   ├── Tests: {passing}/{total} passing
   ├── Wave Progress:
   │   ├── Wave 1: {implemented}/{total} ({percentage}%)
   │   ├── Wave 2: {implemented}/{total} ({percentage}%)
   │   └── Wave 3+: {implemented}/{total} ({percentage}%)
   └── Golden Path: {testable_status}
   ```

Note: This command assumes a complete task breakdown exists in tasks.md. If tasks are incomplete or missing, suggest running `/speckit.tasks` first to regenerate the task list.

## Automation Behavior

This command has **pre-implementation gates** that must pass before execution begins:

### Pre-Implementation Gates

| Gate | Check | Block Condition | Message |
|------|-------|-----------------|---------|
| Tasks Exist Gate | tasks.md exists in FEATURE_DIR | tasks.md missing | "Run /speckit.tasks first to generate task breakdown" |
| Required Artifacts Gate | plan.md exists in FEATURE_DIR | plan.md missing | "Run /speckit.plan first to generate implementation plan" |
| No Critical Issues Gate | If analyze was run, CRITICAL == 0 | CRITICAL issues exist from prior analysis | "Resolve CRITICAL issues before starting implementation" |

### Gate Behavior

**Before execution begins:**
- All pre_gates are evaluated
- If any gate fails, display blocking message and suggest corrective action
- Wait for user to resolve and re-invoke `/speckit.implement`

**During execution:**
- Checklist validation (step 2) acts as runtime gate
- If checklists incomplete, prompt user for confirmation before proceeding

### Post-Implementation Flow

When all P1 tasks are marked `[X]`, implementation **auto-transitions to QA verification**:

| Condition | Next Phase | Gate |
|-----------|------------|------|
| All P1 tasks completed | `/speckit.analyze` (QA mode) | Implementation Complete Gate |

### QA Loop

```text
/speckit.implement
        │
        ▼ (auto: P1 tasks complete)
/speckit.analyze (QA mode)
        │
    ┌───┴───┐
    │       │
  PASS    FAIL
    │       │
    ▼       ▼
  Done   Fix Issues
 /merge  (implement)
            │
            └────────▶ /speckit.analyze (QA mode) ─▶ ...
```

### QA Handoffs

| Condition | Handoff | Auto |
|-----------|---------|------|
| P1 tasks complete | QA Verification (`/speckit.analyze`) | ✅ Yes |
| User wants comprehensive verification | Comprehensive Verification (`/speckit.verify`) | ❌ No |
| QA Verdict == FAIL | Fix QA Issues (`/speckit.implement`) | ❌ No |
| Found missing tasks | Update Tasks (`/speckit.tasks`) | ❌ No |
| Discovered spec gaps | Update Spec (`/speckit.specify`) | ❌ No |

### Manual Overrides

Users can always choose to:
- Skip checklist validation (with explicit confirmation)
- Pause implementation and update artifacts
- Re-run specific phases if issues discovered
- Skip QA verification (not recommended)
- Manually trigger QA at any point
- Run `/speckit.verify` for comprehensive verification (includes visual regression and behavioral testing)

---

## Self-Review Phase (MANDATORY)

**Before declaring implementation complete, you MUST perform self-review.**

This phase ensures code quality and catches issues before handoff to QA.

### Step 0.5: Build-Until-Works Loop

**Purpose**: Iteratively fix common compilation errors before proceeding to full validation.

**Performance Optimization**: Read `templates/shared/implement/build-optimizer.md` and apply.
- Pre-compile all regex patterns at session start (not per-build)
- Use smart retry strategy with progressive timeouts (30s → 20s → 15s)
- Expected savings: 50% (15-45s → 10-20s)

**When**: After initial code generation, before running auto checks.

**Skip flag**: Pass `--no-build-fix` to disable build error auto-fixing.

**Execution**:

```text
FUNCTION build_until_works():
  IF "--no-build-fix" in ARGS:
    RETURN SKIP  # Proceed to Step 1 without build loop

  build_cmd = detect_build_command()  # npm run build, cargo build, python -m py_compile, go build

  FOR iteration IN range(1, max_build_attempts + 1):
    build_result = run_command(build_cmd)

    IF build_result.exit_code == 0:
      LOG "✅ Build successful on attempt {iteration}"
      RETURN SUCCESS

    errors = parse_build_errors(build_result.stderr)
    fixes_applied = 0

    FOR EACH error IN errors:
      FOR EACH lang_patterns IN build_error_patterns.patterns:
        FOR EACH pattern IN lang_patterns:
          match = regex_match(pattern.pattern, error.message)
          IF match:
            SWITCH pattern.action:
              CASE "add_import":
                module = match.group(1)
                insert_import_statement(error.file, module)
                fixes_applied++

              CASE "prefix_unused":
                var_name = match.group(1)
                rename_variable(error.file, var_name, "_" + var_name)
                fixes_applied++

              CASE "add_type_annotation":
                property = match.group(1)
                add_interface_property(error.file, property)
                fixes_applied++

              CASE "add_key_prop":
                insert_key_prop(error.file, error.line, "index")
                fixes_applied++

              CASE "move_hook_to_top":
                refactor_hook_to_component_top(error.file)
                fixes_applied++

              CASE "add_use_statement":
                item = match.group(1)
                insert_rust_use_statement(error.file, item)
                fixes_applied++

              CASE "add_import_or_define":
                name = match.group(1)
                IF is_standard_library(name):
                  insert_import_statement(error.file, name)
                ELSE:
                  suggest_definition(error.file, name)
                fixes_applied++

              # Kotlin-specific actions
              CASE "add_companion_object":
                class_name = match.group(1)
                add_companion_object_block(error.file, class_name)
                fixes_applied++

              CASE "wrap_in_coroutine_scope":
                wrap_suspend_call_in_scope(error.file, error.line)
                fixes_applied++

              # Kotlin Compose-specific actions
              CASE "add_composable_annotation":
                add_annotation(error.file, error.line, "@Composable")
                fixes_applied++

              CASE "reorder_modifier_param":
                move_modifier_to_first_optional(error.file, error.line)
                fixes_applied++

              # Java-specific actions
              CASE "add_type_cast":
                target_type = match.group(2)
                insert_cast(error.file, error.line, target_type)
                fixes_applied++

              CASE "add_instance_or_static":
                make_method_static_or_create_instance(error.file, error.line)
                fixes_applied++

            BREAK  # Pattern matched, move to next error

    IF fixes_applied == 0:
      LOG "⚠️ No auto-fixes available for {len(errors)} errors"
      RETURN BLOCKED  # Escalate to human

    LOG "🔧 Applied {fixes_applied} fixes, retrying build..."

  LOG "❌ Max attempts ({max_build_attempts}) reached"
  RETURN BLOCKED
```

**Build-Until-Works Output Format**:

```text
🔨 Build-Until-Works Loop
├── Attempt 1/3
│   ├── Build: FAILED (5 errors)
│   ├── Patterns Matched: 4
│   ├── Fixes Applied:
│   │   ├── BF-001: Added import for 'lodash' in src/utils.ts
│   │   ├── BF-002: Prefixed '_unused' in src/types.ts:45
│   │   ├── BF-004: Added key={item.id} in src/List.tsx:23
│   │   └── BF-004: Added key={index} in src/Grid.tsx:67
│   └── Retrying build...
├── Attempt 2/3
│   ├── Build: SUCCESS ✅
│   └── All compilation errors resolved
└── Status: READY for Step 1

OR (if blocked):

🔨 Build-Until-Works Loop
├── Attempt 1/3
│   ├── Build: FAILED (3 errors)
│   ├── Patterns Matched: 0
│   └── ⚠️ Unrecognized errors - escalating to human
└── Status: BLOCKED - manual fix required

Unresolved Build Errors:
  1. src/api.ts:34 - Type 'Promise<void>' is not assignable to type 'Response'
  2. src/utils.ts:12 - Argument of type 'string' is not assignable to parameter of type 'number'
  3. src/hooks.ts:8 - Cannot use namespace 'React' as a type
```

**On BLOCKED**: Report unresolved errors and suggest manual fixes before continuing.

### Step 1: Run Auto Checks

Execute these checks from the project root:

| Check | Command | Required | On Failure |
|-------|---------|----------|------------|
| **Build** | Detect from `package.json`/`Cargo.toml`/`pyproject.toml`/`go.mod`/`pom.xml` and run appropriate build command | YES | STOP |
| **Lint** | Detect from `.eslintrc*`/`.pylintrc`/`rustfmt.toml` and run linter | NO | WARN |
| **Test** | Run test suite for modified code | YES | STOP |
| **TypeCheck** | If TypeScript/mypy configured, run type checker | NO | WARN |

**Auto-detection logic**:
```text
IF package.json exists:
  Build: npm run build OR yarn build OR pnpm build
  Lint: npm run lint (if script exists)
  Test: npm test
  TypeCheck: npx tsc --noEmit (if tsconfig.json exists)

IF Cargo.toml exists:
  Build: cargo build
  Lint: cargo clippy
  Test: cargo test

IF pyproject.toml OR setup.py exists:
  Build: pip install -e . OR python setup.py build
  Lint: ruff check . OR pylint
  Test: pytest
  TypeCheck: mypy . (if configured)

IF go.mod exists:
  Build: go build ./...
  Lint: golangci-lint run
  Test: go test ./...
```

**Output format**:
```text
🔍 Self-Review: Auto Checks
├── Build:     ✅ PASS (npm run build - 0 errors)
├── Lint:      ⚠️ WARN (3 warnings, 0 errors)
├── Test:      ✅ PASS (42 tests, 0 failures)
└── TypeCheck: ✅ PASS (tsc --noEmit)

Auto Checks: PASS (1 warning)
```

**On REQUIRED check failure**: STOP immediately, display error, do not proceed.

### Step 1.5: Self-Healing Engine

**Purpose**: Automatically fix common issues before manual intervention to reduce iteration cycles.

**Skip flag**: Pass `--no-auto-fix` to disable self-healing and use manual fixes only.

**Auto-Fix Rules**:

| Rule ID | Issue | Action | Maps To |
|---------|-------|--------|---------|
| AF-001 | Missing `@speckit:FR:` annotations | Insert from task markers `[FR:FR-xxx]` | SR-IMPL-05 |
| AF-001 | Missing `@speckit:AS:` annotations | Insert from task markers `[TEST:AS-xxx]` | SR-IMPL-06 |
| AF-002 | `TODO`/`FIXME`/`HACK` comments | Convert to `.speckit/issues.md` entries | SR-IMPL-04 |
| AF-003 | Lint warnings (fixable) | Run auto-formatter for detected language | Lint check |
| AF-004 | Missing `.env.example` | Generate from `process.env`/`os.getenv` scans | SR-IMPL-13 |
| AF-005 | Debug statements | Remove `console.log`/`print` statements | SR-IMPL-09 |

**Build Error Auto-Fix Rules** (triggered by build stderr parsing):

| Rule ID | Language | Error Pattern | Action |
|---------|----------|---------------|--------|
| BF-001 | TS/Py/Go/Rust/Kt/Java | Missing module/import | Auto-add import statement |
| BF-002 | TS/ESLint/Go/Rust/Kt/Java | Unused variable | Prefix with `_` or remove |
| BF-003 | TS/Kt/Java | Type mismatch | Add type annotation or cast |
| BF-004 | React | Missing key prop | Add `key={index}` or `key={item.id}` |
| BF-005 | React | Conditional hook call | Move hook before conditions |
| BF-006 | Python/Java | Undefined name/symbol | Add import or define variable |
| BF-007 | Kotlin | Missing companion object | Add `companion object {}` block |
| BF-008 | Kotlin | Suspend outside coroutine | Wrap in `runBlocking {}` or `launch {}` |
| BF-009 | Compose | Missing @Composable | Add `@Composable` annotation |
| BF-010 | Compose | Modifier wrong position | Reorder to first optional param |
| BF-011 | Java | Static context error | Add instance or make method static |

**Non-Auto-Fixable Issues** (require human judgment):

| Issue | Reason |
|-------|--------|
| Complex build failures | When BF-xxx patterns don't match (type logic, async errors) |
| Test failures (SR-IMPL-03) | May indicate real bugs |
| Hardcoded secrets (SR-IMPL-07) | Security-critical decision |
| Error handling (SR-IMPL-08) | Requires domain knowledge |

**Self-Healing Execution**:

```text
FUNCTION execute_self_healing(failed_criteria):
  IF "--no-auto-fix" in ARGS:
    RETURN {applied: [], skipped: failed_criteria}

  applied_fixes = []
  remaining_issues = []

  FOR EACH criterion in failed_criteria:
    rule = match_auto_fix_rule(criterion.id)

    IF rule IS NULL:
      remaining_issues.append(criterion)
      CONTINUE

    SWITCH rule.action:
      CASE "insert_annotation":
        # Extract task markers from tasks.md
        markers = extract_task_markers(TASKS_FILE)
        FOR EACH file in criterion.affected_files:
          FOR EACH marker in markers WHERE marker.file == file:
            IF marker.type == "FR":
              insert_comment(file, marker.line, "@speckit:FR:{marker.id}")
            ELIF marker.type == "TEST":
              insert_comment(file, marker.line, "@speckit:AS:{marker.id}")
        applied_fixes.append({rule: "AF-001", count: len(markers)})

      CASE "convert_to_issue":
        # Convert TODO/FIXME to tracked issues
        issues_file = ".speckit/issues.md"
        ensure_file_exists(issues_file)
        FOR EACH todo in criterion.items:
          append_to_file(issues_file, format_issue(todo))
          remove_line(todo.file, todo.line)
        applied_fixes.append({rule: "AF-002", count: len(criterion.items)})

      CASE "run_auto_formatter":
        # Detect language and run appropriate formatter
        lang = detect_project_language()
        cmd = get_formatter_command(lang)  # From auto_fix_rules.rules[2].commands
        run_command(cmd)
        applied_fixes.append({rule: "AF-003", files: count_formatted_files()})

      CASE "generate_env_example":
        # Scan for environment variable usage
        env_vars = []
        FOR EACH file in project_files:
          env_vars.extend(extract_env_vars(file))  # process.env.X, os.getenv("X")
        generate_env_example(env_vars)
        applied_fixes.append({rule: "AF-004", variables: len(env_vars)})

      CASE "remove_debug_statements":
        # Remove console.log/print debug statements
        patterns = ["console.log(", "console.debug(", "print(", "println!", "fmt.Println("]
        FOR EACH file in criterion.affected_files:
          remove_matching_lines(file, patterns)
        applied_fixes.append({rule: "AF-005", count: lines_removed})

  RETURN {applied: applied_fixes, remaining: remaining_issues}
```

**Self-Healing Output Format**:

```text
🔧 Self-Healing Report
├── Fixes Applied: {N}
│   ├── AF-001: Added {X} @speckit annotations
│   ├── AF-002: Converted {Y} TODOs to issues
│   ├── AF-003: Auto-formatted {Z} files
│   ├── AF-004: Generated .env.example ({V} variables)
│   └── AF-005: Removed {W} debug statements
├── Fixes Failed: {M}
│   └── {reason}
└── Status: {N} issues auto-resolved, {M} require manual fix

→ Re-running self-review with fixes applied...
```

### Step 1.7: Vision-Powered UX Validation (Conditional)

**Purpose**: Automatically validate UI implementation against UX quality principles using screenshot analysis.

**Performance Optimization**: Read `templates/shared/implement/vision-turbo.md` and apply parallel capture.
- Parallel browser contexts for simultaneous viewport capture (3 contexts)
- Expected savings: 75-80% (120-240s → 35-50s)
- Fallback to sequential on error

**Trigger Conditions**: Execute ONLY if ALL conditions are met:
1. `vision_validation.enabled = true` in YAML config
2. `--no-vision` flag is NOT passed
3. Task has `[VR:VR-xxx]` markers OR `role_group = FRONTEND` in tasks.md
4. Playwright MCP server is available

**Skip Conditions**:
- API-only or backend features (no UI)
- CLI tools without graphical interface
- Tasks without `[VR:]` markers AND no frontend components

**Execution Flow**:

```text
FUNCTION execute_vision_validation():
  IF "--no-vision" in ARGS:
    LOG "Vision validation skipped (--no-vision flag)"
    RETURN SKIP

  ui_tasks = filter_tasks(markers=["VR:VR-xxx"] OR role_group="FRONTEND")
  IF ui_tasks.empty:
    LOG "Vision validation skipped (no UI tasks detected)"
    RETURN SKIP

  # 1. Identify Screens to Capture
  screens = []
  FOR EACH task in ui_tasks:
    IF task.marker matches "[VR:VR-xxx]":
      screen = extract_screen_from_marker(task)
      screens.append({
        id: screen.id,
        path: infer_route_from_task(task),
        component: extract_component_name(task),
        states: ["default", "loading", "error", "empty", "success"]
      })

  # 2. Capture Screenshots (Playwright MCP)
  screenshots = []
  FOR EACH screen in screens:
    FOR EACH viewport in [mobile: 375x812, tablet: 768x1024, desktop: 1440x900]:
      FOR EACH state in screen.states:
        # Navigate and trigger state
        browser_navigate(screen.path)
        trigger_state(state)  # Mock API response for state

        # Capture screenshot
        filename = "screenshots/{screen.id}_{viewport.name}_{state}.png"
        browser_take_screenshot(filename)
        screenshots.append({
          screen: screen.id,
          viewport: viewport.name,
          state: state,
          file: filename
        })

  # 3. Vision Analysis (Claude Opus with vision)
  violations = []
  FOR EACH screenshot in screenshots:
    analysis = analyze_with_vision(screenshot.file, VISION_PROMPT)
    violations.extend(analysis.violations)

  # 4. Generate UX Audit Report
  report = generate_ux_audit_report(violations, screenshots)
  write_file("specs/{feature}/ux-audit.md", report)

  # 5. Apply Gate
  critical_violations = filter(violations, severity="CRITICAL")
  IF critical_violations.count > 0:
    BLOCK deployment
    ERROR "UX validation failed. {N} critical issues must be resolved:"
    FOR EACH violation in critical_violations:
      PRINT "  - [{violation.id}] {violation.issue}"
      PRINT "    Suggestion: {violation.suggestion}"
    RETURN FAIL

  IF violations.count > vision_validation.max_issues:
    WARN "UX validation found {N} issues. Review recommended."

  RETURN PASS
```

**Vision Analysis Prompt** (sent with each screenshot):

```text
Analyze this UI screenshot against UX quality principles.

## UXQ Principles to Check (from memory/domains/uxq.md)
- UXQ-001: Mental Model Alignment (no jargon, intuitive labels)
- UXQ-003: Friction Justification (every step must add value)
- UXQ-005: Error Empathy (helpful messages, not blaming)
- UXQ-006: FTUE Clear Guidance (onboarding clarity)
- UXQ-010: Accessibility (contrast, touch targets)

## Nielsen Heuristics to Check (from memory/knowledge/frameworks/nielsen-heuristics.md)
- H1: Visibility of System Status (feedback, loading indicators)
- H2: Match Between System and Real World (familiar terms)
- H4: Consistency and Standards (UI patterns)
- H6: Recognition Rather Than Recall (visible options)
- H8: Aesthetic and Minimalist Design (no clutter)

## Anti-Patterns to Detect (from memory/knowledge/anti-patterns/ux.md)
- UX-001: Modal Overload (too many popups)
- UX-003: Form Abandonment Design (hostile forms)
- UX-005: Cognitive Overload (too much at once)
- UX-007: Mobile Neglect (touch targets, responsive)

Output as JSON:
{
  "screen": "{screen_name}",
  "viewport": "{viewport}",
  "state": "{state}",
  "violations": [
    {
      "id": "UXQ-xxx / H-x / UX-xxx",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "element": "description of UI element",
      "issue": "what's wrong",
      "suggestion": "how to fix"
    }
  ],
  "score": 0-100
}
```

**Severity Classification**:

| Severity | Criteria | Examples | Action |
|----------|----------|----------|--------|
| CRITICAL | Blocks core task, accessibility barrier | Missing form labels, <3:1 contrast, no error message | BLOCK deploy |
| HIGH | Significant usability issue | Confusing labels, hidden actions, no loading state | WARN, recommend fix |
| MEDIUM | Minor friction | Inconsistent spacing, verbose text | Log for backlog |
| LOW | Polish opportunity | Could be more delightful | Optional |

**Output Format**:

```text
👁️ Vision-Powered UX Validation
├── Screens Analyzed: {N}
├── Screenshots Captured: {N} (across 3 viewports × 5 states)
├── Violations Found:
│   ├── CRITICAL: {count}
│   ├── HIGH: {count}
│   ├── MEDIUM: {count}
│   └── LOW: {count}
├── Overall UX Score: {score}/100
└── Report: specs/{feature}/ux-audit.md

{IF CRITICAL > 0}
⛔ DEPLOYMENT BLOCKED - Critical UX issues must be resolved:
  - [UXQ-010] Form input missing label (accessibility)
  - [H1] No loading indicator on submit button
{ENDIF}
```

**Reference Documentation**:
- Vision validation guide: `templates/shared/vision-validation.md`
- UX audit template: `templates/ux-audit-template.md`
- UXQ domain: `memory/domains/uxq.md`
- Nielsen heuristics: `memory/knowledge/frameworks/nielsen-heuristics.md`

### Step 2: Re-read Modified Files

Review the files you created/modified in this implementation:
1. List all files touched during implementation
2. For each significant file, scan for obvious issues

### Step 3: Quality Criteria

Answer each question by examining the implementation:

| ID | Question | Severity |
|----|----------|----------|
| SR-IMPL-01 | All P1 tasks marked `[X]` in tasks.md? | CRITICAL |
| SR-IMPL-02 | Build passes without errors? | CRITICAL |
| SR-IMPL-03 | All tests pass? | CRITICAL |
| SR-IMPL-04 | No `TODO`, `FIXME`, `HACK` comments left in new code? | HIGH |
| SR-IMPL-05 | `@speckit:FR:` annotations present in implementation code? | MEDIUM |
| SR-IMPL-06 | `@speckit:AS:` annotations present in test code? | HIGH |
| SR-IMPL-07 | No hardcoded secrets, API keys, or credentials? | CRITICAL |
| SR-IMPL-08 | Error handling present for external calls? | HIGH |
| SR-IMPL-09 | No console.log/print debug statements left? | MEDIUM |
| SR-IMPL-10 | File/function naming follows project conventions? | LOW |
| SR-IMPL-11 | RUNNING.md exists and has valid run commands? | HIGH |
| SR-IMPL-12 | README.md exists and reflects implemented features? | HIGH |
| SR-IMPL-13 | .env.example exists if env vars are used? | MEDIUM |
| SR-IMPL-14 | UI renders correctly across viewports (mobile, tablet, desktop)? | HIGH |
| SR-IMPL-15 | No CRITICAL UX violations detected by vision analysis? | CRITICAL |
| SR-IMPL-16 | Loading, error, and empty states implemented for UI components? | HIGH |
| SR-IMPL-17 | Visual accessibility checks pass (contrast, touch targets)? | HIGH |
| SR-IMPL-18 | No hardcoded colors in UI code (DSS-002)? | HIGH |
| SR-IMPL-19 | Component library used where equivalent exists (DSS-001)? | MEDIUM |
| SR-IMPL-20 | Typography tokens used instead of hardcoded values (DSS-003)? | MEDIUM |

**Design System Criteria (SR-IMPL-18/19/20)**: Only evaluated when `design_system` is configured in constitution.md and `enforcement_level != "off"`. Mark as `N/A` if design system enforcement is disabled.

**Evaluation**:
```text
🔍 Self-Review: Quality Criteria
├── SR-IMPL-01: ✅ PASS - 12/12 P1 tasks complete
├── SR-IMPL-02: ✅ PASS - Build successful
├── SR-IMPL-03: ✅ PASS - 42/42 tests passing
├── SR-IMPL-04: ⚠️ HIGH - Found 2 TODO comments in src/api/handler.ts
├── SR-IMPL-05: ✅ PASS - 8 @speckit:FR annotations found
├── SR-IMPL-06: ⚠️ HIGH - Missing @speckit:AS in tests/auth.test.ts
├── SR-IMPL-07: ✅ PASS - No secrets detected
├── SR-IMPL-08: ✅ PASS - Error handling present
├── SR-IMPL-09: ✅ PASS - No debug statements
├── SR-IMPL-10: ✅ PASS - Naming conventions followed
├── SR-IMPL-11: ✅ PASS - RUNNING.md exists
├── SR-IMPL-12: ✅ PASS - README.md updated
├── SR-IMPL-13: ✅ PASS - .env.example exists
├── SR-IMPL-14: ✅ PASS - UI renders across viewports (vision check)
├── SR-IMPL-15: ✅ PASS - No critical UX violations
├── SR-IMPL-16: ⚠️ HIGH - Missing loading state in checkout form
├── SR-IMPL-17: ✅ PASS - Accessibility visual checks pass
├── SR-IMPL-18: ⚠️ HIGH - Found 2 hardcoded colors in src/Button.tsx (DSS-002)
├── SR-IMPL-19: ✅ PASS - Library components used (DSS-001)
└── SR-IMPL-20: ✅ PASS - Typography tokens used (DSS-003)

Summary: CRITICAL=0, HIGH=4, MEDIUM=0, LOW=0
```

### Step 4: Verdict

Determine the self-review verdict:

| Verdict | Condition | Action |
|---------|-----------|--------|
| **PASS** | CRITICAL=0 AND HIGH=0 | Proceed to QA handoff |
| **WARN** | CRITICAL=0 AND HIGH≤2 AND all HIGH are non-blocking | Show warnings, proceed |
| **FAIL** | CRITICAL>0 OR HIGH>2 | Self-correct, re-check |

### Step 5: Self-Correction Loop (with Self-Healing)

**IF verdict is FAIL AND iteration < 3**:

1. **Attempt Auto-Fix First** (if `--no-auto-fix` not passed):
   ```text
   failed_criteria = collect_failed_criteria(SR-IMPL-*)
   healing_result = execute_self_healing(failed_criteria)

   IF healing_result.applied.length > 0:
     Display Self-Healing Report (see Step 1.5 output format)
   ```

2. **Recalculate Verdict**:
   - Re-run quality criteria checks for auto-fixed issues only
   - Update criterion status: `❌ FAIL → ✅ FIXED (AF-XXX)`
   - Recalculate: `CRITICAL_COUNT`, `HIGH_COUNT`

3. **Manual Fix Remaining Issues**:
   - For each issue in `healing_result.remaining`:
     - Non-auto-fixable (build, test, secrets, error handling): Apply manual fix
     - Auto-fix failed: Investigate and fix manually
   - Fix any failing tests or build errors (requires human judgment)

4. **Re-run Self-Review**:
   - Execute from Step 1 with updated code
   - Increment iteration counter
   - Report: `Self-Review Iteration 2/3 (Auto-fixed: {N}, Manual: {M})...`

**IF still FAIL after 3 iterations**:
```text
❌ Self-Review FAILED after 3 iterations

Self-Healing Summary:
├── Auto-fixes attempted: {total_attempts}
├── Auto-fixes successful: {successful}
└── Auto-fixes failed: {failed}

Remaining issues (require human intervention):
- SR-IMPL-02: Build failure in src/api/handler.ts (non-auto-fixable)
- SR-IMPL-03: Test failure in tests/auth.test.ts (non-auto-fixable)

⛔ BLOCKING: Cannot proceed to QA verification.
   These issues require manual code changes.

User: Proceed anyway? (yes/no)
```

**IF verdict is PASS or WARN**:
```text
✅ Self-Review PASSED

Summary:
- Auto Checks: PASS
- Quality Criteria: {passing}/{total} passing
- Self-Healing: {auto_fixed} issues auto-resolved
- Iterations: {N}
- Estimated time saved: ~{minutes} minutes

→ Proceeding to QA Verification (/speckit.analyze)
```

### Self-Review Report Template

Generate this report before handoff:

```markdown
## Self-Review Report

**Command**: /speckit.implement
**Reviewed at**: {{TIMESTAMP}}
**Iteration**: {{N}}/3
**Self-Healing**: {{ENABLED|DISABLED}}

### Auto Checks
| Check | Status | Details |
|-------|--------|---------|
| Build | ✅ PASS | npm run build (0 errors) |
| Lint | ✅ FIXED | 3 warnings → 0 (AF-003 applied) |
| Test | ✅ PASS | 42/42 passing |
| TypeCheck | ✅ PASS | tsc --noEmit |

### Quality Criteria
| ID | Question | Initial | After Auto-Fix |
|----|----------|---------|----------------|
| SR-IMPL-01 | All P1 tasks complete? | ✅ PASS | — |
| SR-IMPL-02 | Build passes? | ✅ PASS | — |
| SR-IMPL-03 | Tests pass? | ✅ PASS | — |
| SR-IMPL-04 | No TODO/FIXME? | ❌ FAIL | ✅ FIXED (AF-002) |
| SR-IMPL-05 | @speckit:FR annotations? | ❌ FAIL | ✅ FIXED (AF-001) |
| SR-IMPL-06 | @speckit:AS annotations? | ❌ FAIL | ✅ FIXED (AF-001) |
| SR-IMPL-07 | No hardcoded secrets? | ✅ PASS | — |
| SR-IMPL-08 | Error handling? | ✅ PASS | — |
| SR-IMPL-09 | No debug statements? | ❌ FAIL | ✅ FIXED (AF-005) |
| SR-IMPL-10 | Naming conventions? | ✅ PASS | — |
| SR-IMPL-11 | RUNNING.md exists? | ✅ PASS | — |
| SR-IMPL-12 | README.md updated? | ✅ PASS | — |
| SR-IMPL-13 | .env.example exists? | ❌ FAIL | ✅ FIXED (AF-004) |
| SR-IMPL-14 | UI renders across viewports? | ✅ PASS | — |
| SR-IMPL-15 | No critical UX violations? | ✅ PASS | — |
| SR-IMPL-16 | Loading/error/empty states? | ⚠️ HIGH | (manual fix needed) |
| SR-IMPL-17 | Accessibility visual checks? | ✅ PASS | — |

### Self-Healing Summary
| Rule | Action | Count | Status |
|------|--------|-------|--------|
| AF-001 | Insert @speckit annotations | 8 | ✅ Applied |
| AF-002 | Convert TODOs to issues | 2 | ✅ Applied |
| AF-003 | Run auto-formatter | 5 files | ✅ Applied |
| AF-004 | Generate .env.example | 12 vars | ✅ Applied |
| AF-005 | Remove debug statements | 3 | ✅ Applied |

### Self-Healing Metrics
| Metric | Value |
|--------|-------|
| Issues initially failing | 5 |
| Issues auto-fixed | 5 |
| Issues requiring manual fix | 0 |
| Iterations required | 1 |
| Estimated time saved | ~15 minutes |

### Velocity Metrics
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Time to First Code | {{TIME_TO_FIRST_CODE}} min | < 10 min | ✅/❌ |
| Time to MVP (Wave 1) | {{TIME_TO_MVP}} min | < 30 min | ✅/❌ |
| Human Intervention Rate | {{HUMAN_INTERVENTION}}% | < 30% | ✅/❌ |
| Auto-Fix Success Rate | {{AUTOFIX_SUCCESS}}% | > 70% | ✅/❌ |

**Velocity Calculation Notes:**
- Time to First Code = First passing test timestamp - Session start timestamp
- Human Intervention = Tasks with manual edits / Total tasks
- Auto-Fix Success = Auto-fixes successful / Auto-fixes attempted

### Cost Metrics
| Phase | Model | Tokens | Cost |
|-------|-------|--------|------|
| Implement | {{MODEL}} | {{TOKENS}}K | ${{COST}} |

| Token Type | Count | Rate | Subtotal |
|------------|-------|------|----------|
| Input | {{INPUT_TOKENS}} | ${{INPUT_RATE}}/1K | ${{INPUT_COST}} |
| Output | {{OUTPUT_TOKENS}} | ${{OUTPUT_RATE}}/1K | ${{OUTPUT_COST}} |
| Cache Write | {{CACHE_WRITE}} | ${{CACHE_WRITE_RATE}}/1K | ${{CACHE_WRITE_COST}} |
| Cache Read | {{CACHE_READ}} | ${{CACHE_READ_RATE}}/1K | ${{CACHE_READ_COST}} |
| **Total** | | | **${{TOTAL_COST}}** |

**Cost Benchmark:** Target ~$22 for implement phase (50 FRs, 200 tasks reference)

### Documentation
| File | Status | Sections |
|------|--------|----------|
| RUNNING.md | ✅ Created | Prerequisites, Installation, Running, Testing |
| README.md | ✅ Updated | Features (+3), Tech Stack, Quick Start |
| .env.example | ✅ Generated | 12 variables (via AF-004) |
| .speckit/issues.md | ✅ Created | 2 tracked issues (via AF-002) |

### Verdict: ✅ PASS
**Reason**: All criteria met (5 via self-healing), documentation generated.

→ Proceeding to handoff: /speckit.analyze (QA mode)
```
