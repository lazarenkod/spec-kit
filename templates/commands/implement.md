---
description: Execute the implementation plan by processing and executing all tasks defined in tasks.md
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
    post_actions:
      - "log: Implementation complete, running QA verification"
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
pre_gates:
  - name: "Tasks Exist Gate"
    check: "tasks.md exists in FEATURE_DIR"
    block_if: "tasks.md missing"
    message: "Run /speckit.tasks first to generate task breakdown"
  - name: "Required Artifacts Gate"
    check: "plan.md exists in FEATURE_DIR"
    block_if: "plan.md missing"
    message: "Run /speckit.plan first to generate implementation plan"
  - name: "No Critical Issues Gate"
    check: "If analyze was run, CRITICAL == 0"
    block_if: "CRITICAL issues exist from prior analysis"
    message: "Resolve CRITICAL issues before starting implementation"
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

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
     - **STOP** and ask: "Some checklists are incomplete. Do you want to proceed with implementation anyway? (yes/no)"
     - Wait for user response before continuing
     - If user says "no" or "wait" or "stop", halt execution
     - If user says "yes" or "proceed" or "continue", proceed to step 3

   - **If all checklists are complete**:
     - Display the table showing all checklists passed
     - Automatically proceed to step 3

3. Load and analyze the implementation context:
   - **REQUIRED**: Read tasks.md for the complete task list and execution plan
   - **REQUIRED**: Read plan.md for tech stack, architecture, and file structure
   - **IF EXISTS**: Read plan.md Dependency Registry for API documentation references
   - **IF EXISTS**: Read data-model.md for entities and relationships
   - **IF EXISTS**: Read contracts/ for API specifications and test requirements
   - **IF EXISTS**: Read research.md for technical decisions and constraints
   - **IF EXISTS**: Read quickstart.md for integration scenarios

3.5. **API Documentation Verification** (before implementation):

   **Purpose**: Verify API documentation references before coding to prevent hallucinations.

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
        → STOP implementation for this task
        → Report: "⛔ API verification failed: {method} not found in {docs_url}"
        → SUGGEST: "Check dependency version in Dependency Registry"
        → SUGGEST: "Use Context7 to fetch current documentation"
        → ASK user: "Proceed anyway (risky) or fix Dependency Registry first?"
      ```

   e) **Skip conditions**:
      - Tasks without [DEP:] or [APIDOC:] markers
      - Internal project dependencies (no external docs)
      - Setup/configuration tasks

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

6. Parse tasks.md structure and extract:
   - **Task phases**: Setup, Tests, Core, Integration, Polish
   - **Task dependencies**: Sequential vs parallel execution rules
   - **Task details**: ID, description, file paths, parallel markers [P]
   - **Execution flow**: Order and dependency requirements

7. Execute implementation following the task plan:
   - **Phase-by-phase execution**: Complete each phase before moving to the next
   - **Respect dependencies**: Run sequential tasks in order, parallel tasks [P] can run together  
   - **Follow TDD approach**: Execute test tasks before their corresponding implementation tasks
   - **File-based coordination**: Tasks affecting the same files must run sequentially
   - **Validation checkpoints**: Verify each phase completion before proceeding

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

9. Progress tracking and error handling:
   - Report progress after each completed task
   - Halt execution if any non-parallel task fails
   - For parallel tasks [P], continue with successful tasks, report failed ones
   - Provide clear error messages with context for debugging
   - Suggest next steps if implementation cannot proceed
   - **IMPORTANT** For completed tasks, make sure to mark the task off as [X] in the tasks file.

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

---

## Self-Review Phase (MANDATORY)

**Before declaring implementation complete, you MUST perform self-review.**

This phase ensures code quality and catches issues before handoff to QA.

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
└── SR-IMPL-10: ✅ PASS - Naming conventions followed

Summary: CRITICAL=0, HIGH=2, MEDIUM=0, LOW=0
```

### Step 4: Verdict

Determine the self-review verdict:

| Verdict | Condition | Action |
|---------|-----------|--------|
| **PASS** | CRITICAL=0 AND HIGH=0 | Proceed to QA handoff |
| **WARN** | CRITICAL=0 AND HIGH≤2 AND all HIGH are non-blocking | Show warnings, proceed |
| **FAIL** | CRITICAL>0 OR HIGH>2 | Self-correct, re-check |

### Step 5: Self-Correction Loop

**IF verdict is FAIL AND iteration < 3**:
1. Fix each CRITICAL and HIGH issue:
   - Remove TODO/FIXME comments or convert to tracked issues
   - Add missing @speckit annotations
   - Fix any failing tests or build errors
2. Re-run self-review from Step 1
3. Increment iteration counter
4. Report: `Self-Review Iteration 2/3...`

**IF still FAIL after 3 iterations**:
```text
❌ Self-Review FAILED after 3 iterations

Remaining issues:
- SR-IMPL-04: 1 TODO comment in src/api/handler.ts:45
- SR-IMPL-06: Missing @speckit:AS annotation

⛔ BLOCKING: Cannot proceed to QA verification.
   Fix remaining issues or override with user confirmation.

User: Proceed anyway? (yes/no)
```

**IF verdict is PASS or WARN**:
```text
✅ Self-Review PASSED

Summary:
- Auto Checks: PASS
- Quality Criteria: 10/10 passing
- Iterations: 1

→ Proceeding to QA Verification (/speckit.analyze)
```

### Self-Review Report Template

Generate this report before handoff:

```markdown
## Self-Review Report

**Command**: /speckit.implement
**Reviewed at**: {{TIMESTAMP}}
**Iteration**: {{N}}/3

### Auto Checks
| Check | Status | Details |
|-------|--------|---------|
| Build | ✅ PASS | npm run build (0 errors) |
| Lint | ⚠️ WARN | 3 warnings |
| Test | ✅ PASS | 42/42 passing |
| TypeCheck | ✅ PASS | tsc --noEmit |

### Quality Criteria
| ID | Question | Status |
|----|----------|--------|
| SR-IMPL-01 | All P1 tasks complete? | ✅ PASS |
| SR-IMPL-02 | Build passes? | ✅ PASS |
| SR-IMPL-03 | Tests pass? | ✅ PASS |
| SR-IMPL-04 | No TODO/FIXME? | ✅ PASS |
| SR-IMPL-05 | @speckit:FR annotations? | ✅ PASS |
| SR-IMPL-06 | @speckit:AS annotations? | ✅ PASS |
| SR-IMPL-07 | No hardcoded secrets? | ✅ PASS |
| SR-IMPL-08 | Error handling? | ✅ PASS |
| SR-IMPL-09 | No debug statements? | ✅ PASS |
| SR-IMPL-10 | Naming conventions? | ✅ PASS |

### Verdict: ✅ PASS
**Reason**: All criteria met, no blocking issues.

→ Proceeding to handoff: /speckit.analyze (QA mode)
```
