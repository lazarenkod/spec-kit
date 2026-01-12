# `/speckit.verify` - Post-Implementation Verification

---
description: "Verify implementation against specification after /speckit.implement"
persona: qa-agent
handoff:
  requires:
    - specs/[feature]/spec.md
    - specs/[feature]/tasks.md
    - specs/[feature]/plan.md
  generates:
    - reports/verify-report.md
    - reports/verify-summary.json
  template: templates/verify-report-template.md
handoffs:
  - label: "Re-implement Fixes"
    agent: speckit.implement
    prompt: "Fix failed verification issues: {{failures}}"
    auto: false
    condition:
      - "Verification score < 90%"
      - "Auto-fix failed or disabled"
  - label: "Full QA Audit"
    agent: speckit.analyze
    prompt: "Run comprehensive quality audit with --profile qa"
    auto: false
    condition:
      - "Verification score >= 90%"
      - "User wants deeper analysis"
inline_gates:
  enabled: true
  skip_flag: "--skip-gates"
  mode: progressive
  on_failure: block
  pre_gates:
    - id: IG-VERIFY-001
      name: "Implementation Complete"
      tier: 1
      threshold: 0
      severity: CRITICAL
      message: "Cannot verify: implementation not complete. Run /speckit.implement first."
      check: |
        - tasks.md exists
        - All tasks have status: completed or skipped
        - No tasks with status: in_progress or blocked
    - id: IG-VERIFY-002
      name: "Staging Available"
      tier: 1
      threshold: 0
      severity: HIGH
      message: "Staging environment not available. Run /speckit.staging first."
      check: |
        - Docker services healthy (postgres, redis) OR
        - Remote staging URL configured
    - id: IG-VERIFY-003
      name: "Test Framework Ready"
      tier: 1
      threshold: 0
      severity: CRITICAL
      message: "Test framework not configured. Check QG-TEST-002."
      check: |
        - Test framework detected (from test-framework-registry.md)
        - Test command runs (even if tests fail)
  post_gates:
    - id: IG-VERIFY-101
      name: "Verification Threshold"
      tier: 1
      threshold: 90
      severity: CRITICAL
      message: "Verification score {{score}}% below 90% threshold. See report for failures."
      check: |
        - Overall verification score >= 90%
    - id: IG-VERIFY-102
      name: "Critical Failures"
      tier: 1
      threshold: 0
      severity: CRITICAL
      message: "{{count}} critical failures found. Must fix to proceed."
      check: |
        - No failures with severity: CRITICAL
scripts:
  sh: scripts/bash/verify-prerequisites.sh
  ps: scripts/powershell/verify-prerequisites.ps1
claude_code:
  model: sonnet
  reasoning_mode: extended
  rate_limits:
    default_tier: max
    tiers:
      free:
        thinking_budget: 4000
        max_parallel: 2
        batch_delay: 5000
      pro:
        thinking_budget: 6000
        max_parallel: 4
        batch_delay: 4000
      max:
        thinking_budget: 8000
        max_parallel: 6
        batch_delay: 3000
  orchestration:
    max_parallel: 5
    role_isolation: true
  artifact_extraction:
    enabled: true
    skip_flag: "--full-context"
    spec_fields:
      - fr_list
      - as_list
      - nfr_list
      - api_contracts
      - visual_acceptance_criteria
    tasks_fields:
      - test_markers  # [TEST:AS-xxx]
    plan_fields:
      - tech_stack
      - dependencies
  subagents:
    - role: ac-verifier
      role_group: VERIFY_FUNCTIONAL
      parallel: true
      priority: 10
      model_override: sonnet
      prompt: |
        Verify all acceptance criteria from spec.md are implemented and passing.

        ## INPUT
        - spec.md: acceptance_criteria (Gherkin scenarios with AS-xxx IDs)
        - tasks.md: test tasks with [TEST:AS-xxx] markers
        - Test results: from test run output

        ## PROCESS

        1. **Extract AS-xxx scenarios** from spec.md
        2. **Find corresponding tests** in tasks.md (look for [TEST:AS-xxx])
        3. **Run tests** and parse results
        4. **Match results to scenarios**:
           - ✅ PASS: Test exists and passes
           - ❌ FAIL: Test exists but fails
           - ⚠️ MISSING: No test found for scenario
        5. **Calculate coverage**: (PASS + FAIL) / total scenarios

        ## OUTPUT

        ```yaml
        ac_verification:
          total_scenarios: 8
          tested: 7
          passing: 6
          failing: 1
          missing: 1
          coverage: 87.5%  # (7/8)
          pass_rate: 75%   # (6/8)

          results:
            - id: AS-1A
              requirement: REQ-001
              scenario: "Login success"
              status: PASS
              test_file: "tests/auth.test.ts"
              assertions_passed: 5
              assertions_failed: 0

            - id: AS-1B
              requirement: REQ-001
              scenario: "Login failure"
              status: PASS

            - id: AS-1C
              requirement: REQ-001
              scenario: "Account lockout"
              status: FAIL
              test_file: "tests/auth.test.ts"
              error: "Expected lockout after 5 attempts, got 3"
              fix_suggestion:
                file: "src/services/auth.ts"
                line: 45
                current: "MAX_ATTEMPTS = 3"
                fix: "MAX_ATTEMPTS = 5"
                reasoning: "Spec AS-1C requires 5 failed attempts before lockout"

            - id: AS-1D
              requirement: REQ-001
              scenario: "Password reset"
              status: MISSING
              fix_suggestion:
                action: "Create test"
                file: "tests/auth.test.ts"
                template: |
                  test('AS-1D: Password reset', async () => {
                    // Given user exists
                    // When reset requested
                    // Then email sent with reset link
                  });
        ```

    - role: contract-verifier
      role_group: VERIFY_FUNCTIONAL
      parallel: true
      priority: 10
      model_override: sonnet
      prompt: |
        Verify API contracts match spec.md definitions.

        ## INPUT
        - spec.md: api_contracts or infer from Gherkin When steps
        - Actual API: running application (staging or local)

        ## PROCESS

        1. **Extract API contracts** from spec.md:
           - Parse Gherkin "When I [METHOD] [ENDPOINT]" steps
           - Extract request/response tables
           - Build expected contract schema

        2. **Test each endpoint**:
           - Send request with spec data
           - Capture actual response
           - Compare schema (fields, types, nested structure)

        3. **Detect drift**:
           - Missing fields in response
           - Extra fields not in spec
           - Type mismatches
           - Status code differences

        ## OUTPUT

        ```yaml
        contract_verification:
          total_endpoints: 4
          compliant: 3
          drift: 1
          compliance_rate: 75%

          results:
            - endpoint: "POST /api/auth/login"
              method: POST
              spec_status: 200
              actual_status: 200
              spec_response:
                - accessToken: string
                - refreshToken: string
              actual_response:
                - accessToken: string (✅ match)
                - refreshToken: string (✅ match)
              status: PASS

            - endpoint: "POST /api/auth/register"
              method: POST
              spec_status: 201
              actual_status: 201
              spec_response:
                - user: object
              actual_response:
                - user: object (✅ match)
                - createdAt: string (⚠️ drift - not in spec)
              status: DRIFT
              fix_suggestion:
                action: "Update spec.md to include createdAt field"
                file: "specs/[feature]/spec.md"
                section: "API Contract: POST /api/auth/register"
                add: "- createdAt: ISO 8601 timestamp"
        ```

    - role: visual-verifier
      role_group: VERIFY_UI
      parallel: true
      priority: 15
      depends_on: [ac-verifier]  # UI tests may depend on functional tests passing
      model_override: sonnet
      prompt: |
        Verify UI visually matches Visual YAML specs using Playwright + pixelmatch.

        ## INPUT
        - spec.md: visual_acceptance_criteria (YAML section)
        - Baseline screenshots: .verify/baselines/
        - Application: running on staging/localhost

        ## PROCESS

        1. **Parse Visual YAML**:
           - Extract screens/components
           - Get state definitions (loading, error, success, empty)
           - Get responsive breakpoints (mobile, tablet, desktop)

        2. **Generate test scenarios**:
           - For each screen × state × breakpoint
           - Create Playwright test

        3. **Capture screenshots**:
           ```typescript
           await page.goto('/login');
           await page.screenshot({ path: 'current/login-initial-desktop.png' });
           ```

        4. **Compare with baselines**:
           - Use pixelmatch for pixel comparison
           - Generate diff images with highlights
           - Calculate diff percentage

        5. **Apply thresholds**:
           - 0-1%: PASS (negligible diff)
           - 1-5%: WARN (minor drift, may be acceptable)
           - >5%: FAIL (significant visual change)

        ## OUTPUT

        ```yaml
        visual_verification:
          total_screens: 3
          total_comparisons: 9  # 3 screens × 3 states
          passing: 7
          warnings: 1
          failing: 1
          pass_rate: 77.7%

          results:
            - screen: login_page
              state: initial
              viewport: desktop (1440x900)
              baseline: ".verify/baselines/login-initial-desktop.png"
              current: ".verify/current/login-initial-desktop.png"
              diff: ".verify/diffs/login-initial-desktop.png"
              diff_percentage: 0.1%
              status: PASS

            - screen: dashboard
              state: loaded
              viewport: desktop
              diff_percentage: 12%
              status: FAIL
              differences:
                - element: "user avatar in header"
                  expected: present
                  actual: missing
                  fix_suggestion:
                    file: "src/components/Header.tsx"
                    issue: "Avatar component not rendering"
                    hint: "Check if user.avatarUrl is undefined"

                - element: "sidebar width"
                  expected: 250px
                  actual: 280px
                  fix_suggestion:
                    file: "src/styles/globals.css"
                    line: 45
                    current: "width: 280px;"
                    fix: "width: 250px;"

                - element: "title font-size"
                  expected: 20px
                  actual: 24px
                  fix_suggestion:
                    file: "src/components/Dashboard.tsx"
                    line: 12
                    current: "className=\"text-2xl\""
                    fix: "className=\"text-xl\""
        ```

    - role: behavior-verifier
      role_group: VERIFY_E2E
      parallel: true
      priority: 20
      depends_on: [ac-verifier, contract-verifier]
      model_override: sonnet
      prompt: |
        Verify end-to-end user behaviors match spec.md flows.

        ## INPUT
        - spec.md: user stories with Gherkin scenarios
        - E2E test results (Playwright, Cypress, etc.)

        ## PROCESS

        1. **Extract user flows** from spec.md:
           - Multi-step scenarios (Given → When → Then → And)
           - Cross-page navigation
           - State changes across actions

        2. **Run E2E tests**:
           - Execute existing E2E tests
           - Parse test results

        3. **Verify behaviors**:
           - Redirects work as expected
           - State persists across pages
           - Multi-step flows complete successfully

        ## OUTPUT

        ```yaml
        behavior_verification:
          total_behaviors: 4
          passing: 3
          failing: 1
          pass_rate: 75%

          results:
            - behavior: "Login redirect"
              expected: "→ /dashboard"
              actual: "→ /dashboard"
              status: PASS

            - behavior: "Add to cart"
              expected: "Updates cart count"
              actual: "Updates cart count"
              status: PASS

            - behavior: "Checkout flow"
              expected: "4 steps"
              actual: "3 steps"
              status: FAIL
              error: "Payment step missing from checkout flow"
              fix_suggestion:
                file: "src/pages/checkout/index.tsx"
                issue: "PaymentStep component not included in steps array"
                hint: "Add <PaymentStep /> between ShippingStep and ConfirmationStep"
        ```

    - role: nfr-verifier
      role_group: VERIFY_QUALITY
      parallel: true
      priority: 25
      depends_on: [behavior-verifier]  # NFRs tested after functional correctness
      model_override: sonnet
      prompt: |
        Verify non-functional requirements (performance, accessibility, security).

        ## INPUT
        - spec.md: nfr_list with targets (e.g., "Login latency p99 < 500ms")
        - Lighthouse reports
        - Test coverage reports
        - Bundle analysis

        ## PROCESS

        1. **Performance**:
           - Run Lighthouse on key pages
           - Check LCP, FCP, TBT, CLS
           - Measure API latencies (if instrumented)
           - Check bundle size

        2. **Accessibility**:
           - Run axe-core
           - Check WCAG 2.1 AA compliance
           - Verify keyboard navigation

        3. **Security**:
           - Dependency audit (npm audit, pip-audit)
           - Check for exposed secrets
           - Validate HTTPS usage

        4. **Coverage**:
           - Parse coverage reports
           - Check against 80% threshold

        ## OUTPUT

        ```yaml
        nfr_verification:
          total_nfrs: 4
          passing: 1
          failing: 3
          pass_rate: 25%

          results:
            - nfr: "NFR-PERF-001"
              requirement: "Login latency p99 < 500ms"
              target: 500ms
              actual: 320ms
              status: PASS

            - nfr: "NFR-PERF-002"
              requirement: "Page load LCP < 2.5s"
              target: 2.5s
              actual: 3.1s
              status: FAIL
              lighthouse_score: 78
              fix_suggestion:
                issue: "Large bundle size causing slow LCP"
                file: "src/pages/_app.tsx"
                hint: "Lazy load non-critical components, optimize images"

            - nfr: "NFR-PERF-003"
              requirement: "Lighthouse performance > 90"
              target: 90
              actual: 78
              status: FAIL

            - nfr: "NFR-PERF-004"
              requirement: "Bundle size < 500KB"
              target: 500KB
              actual: 620KB
              status: FAIL
              fix_suggestion:
                file: "package.json or imports"
                issue: "Importing entire lodash library"
                current: "import _ from 'lodash';"
                fix: "import debounce from 'lodash/debounce';"
                impact: "Saves ~200KB"
        ```

    - role: report-aggregator
      role_group: VERIFY_REPORT
      parallel: false
      priority: 30
      depends_on: [ac-verifier, contract-verifier, visual-verifier, behavior-verifier, nfr-verifier]
      model_override: sonnet
      prompt: |
        Aggregate verification results into comprehensive report.

        ## INPUT
        - Results from all 5 verifier agents
        - Auto-fix suggestions from each agent

        ## PROCESS

        1. **Calculate scores**:
           - Functional: (AC pass + Contract pass + Behavior pass) / 3
           - Visual: Visual pass rate
           - Quality: NFR pass rate
           - Overall: Weighted average

        2. **Prioritize failures**:
           - CRITICAL: Blocking issues (AC fail, missing tests)
           - HIGH: Contract drift, visual fail, behavior fail
           - MEDIUM: NFR fail (performance, bundle size)
           - LOW: Warnings, minor drift

        3. **Group auto-fixes**:
           - By file (cluster fixes to same file)
           - By priority (critical first)
           - By complexity (simple fixes first)

        4. **Generate report**:
           - Executive summary with overall score
           - Breakdown by category
           - Detailed findings with diffs
           - Auto-fix suggestions

        ## OUTPUT

        Generate `reports/verify-report.md` using template from `templates/verify-report-template.md`:

        - Executive summary with overall score table
        - Section 1: Acceptance Criteria Verification (table with REQ | AC | Status | Details)
        - Section 2: API Contract Verification (table with Endpoint | Spec | Actual | Status)
        - Section 3: Visual Verification (table with Screen | Expected | Actual | Diff)
        - Section 4: Behavior Verification (table with Behavior | Expected | Actual | Status)
        - Section 5: NFR Verification (table with Requirement | Target | Actual | Status)
        - Summary section with overall score breakdown
        - Auto-fix suggestions grouped by priority (Critical, High, Medium)

        Also generate JSON summary at `reports/verify-summary.json`:

        ```json
        {
          "timestamp": "2026-01-10T16:30:00Z",
          "feature": "[feature-name]",
          "overall_score": 64,
          "threshold": 90,
          "status": "FAIL",
          "categories": {
            "functional": {"score": 80, "pass": 4, "fail": 1},
            "api": {"score": 75, "pass": 3, "fail": 1},
            "visual": {"score": 67, "pass": 2, "fail": 1},
            "behavior": {"score": 75, "pass": 3, "fail": 1},
            "nfr": {"score": 25, "pass": 1, "fail": 3}
          },
          "critical_failures": 2,
          "high_failures": 3,
          "auto_fixes_available": 6
        }
        ```

    - role: auto-fixer
      role_group: VERIFY_REMEDIATION
      parallel: false
      priority: 40
      depends_on: [report-aggregator]
      skip_if: "--no-auto-fix flag present"
      model_override: sonnet
      prompt: |
        Apply auto-fix suggestions from verification report.

        ## INPUT
        - Auto-fix suggestions from report (critical + high priority)
        - Original source files

        ## PROCESS

        1. **Filter applicable fixes**:
           - Only fixes with file:line references
           - Only simple fixes (constant changes, imports, small edits)
           - Skip complex refactors (require human judgment)

        **Eligibility Criteria**:
        - Has precise location (file path + line number)
        - Simple change type:
          - Constant value change (e.g., `MAX_ATTEMPTS = 3` → `5`)
          - Import statement change (e.g., full lodash → specific function)
          - CSS property change (e.g., `width: 280px` → `250px`)
          - Class name change (e.g., `text-2xl` → `text-xl`)
        - Low risk (no logic changes, no new dependencies)
        - Testable (can verify by re-running specific test)

        **Ineligible for Auto-Fix**:
        - Adding new components or files
        - Refactoring multi-line logic
        - Changing function signatures
        - Database migrations
        - Complex state management changes

        2. **Group by file**:
           - Apply all fixes to same file in one operation
           - Avoid conflicts between fixes

        3. **Apply fixes**:
           - Use Edit tool for each fix
           - Validate syntax after each edit

        4. **Re-run tests**:
           - Run affected tests
           - Check if fixes resolved issues

        5. **Report results**:
           - Fixed: Issue resolved
           - Partial: Issue improved but not fully resolved
           - Failed: Fix didn't work or caused new issue

        ## OUTPUT

        ```yaml
        auto_fix_results:
          attempted: 6
          successful: 4
          failed: 2

          fixes:
            - issue: "AS-1C: Lockout threshold wrong"
              file: "src/services/auth.ts"
              line: 45
              change: "MAX_ATTEMPTS = 3 → MAX_ATTEMPTS = 5"
              status: FIXED
              verification: "Test AS-1C now passes"

            - issue: "NFR-PERF-004: Bundle size"
              file: "src/utils/helpers.ts"
              line: 1
              change: "import _ from 'lodash' → import debounce from 'lodash/debounce'"
              status: FIXED
              verification: "Bundle reduced from 620KB to 450KB"

            - issue: "Visual: Dashboard sidebar width"
              file: "src/styles/globals.css"
              line: 45
              change: "width: 280px → width: 250px"
              status: FIXED
              verification: "Visual diff now 0.5%"

            - issue: "Behavior: Checkout missing payment step"
              file: "src/pages/checkout/index.tsx"
              status: FAILED
              reason: "Complex refactor required - needs manual implementation"
              suggestion: "Add PaymentStep component between steps 2 and 3"
        ```
flags:
  max_model: "--max-model <opus|sonnet|haiku>"  # Override model cap
---

## Command Overview

The `/speckit.verify` command performs comprehensive post-implementation verification across 5 layers:

1. **Acceptance Criteria** - All AS-xxx scenarios have tests and pass
2. **API Contracts** - Endpoints match spec.md definitions
3. **Visual Verification** - UI matches Visual YAML specs (Playwright + pixelmatch)
4. **Behavior** - E2E user flows work as specified
5. **NFRs** - Performance, accessibility, security metrics meet targets

**Success Criteria**: 90% overall pass rate (configurable with `--threshold` flag)

## Command Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--no-auto-fix` | Disable automatic fix application (report only) | `false` |
| `--threshold N` | Override pass threshold (0-100) | `90` |
| `--skip-visual` | Skip visual regression testing | `false` |
| `--skip-nfr` | Skip NFR verification | `false` |
| `--baseline` | Update visual baselines instead of comparing | `false` |
| `--json` | Output JSON summary only (no markdown report) | `false` |
| `--ci` | CI mode: no interactive prompts, fail on threshold | `false` |
| `--fix-and-verify` | Apply fixes and re-run verification automatically | `false` |
| `--skip-gates` | Skip all inline quality gates | `false` |

## Usage Examples

### Basic Usage (After Implementation)

```bash
/speckit.verify

# Output:
# ✅ Acceptance Criteria: 80% (4/5 pass)
# ✅ API Contracts: 75% (3/4 match)
# ⚠️ Visual: 67% (2/3 pass)
# ✅ Behavior: 75% (3/4 pass)
# ❌ Performance: 25% (1/4 pass)
#
# Overall: 64% ❌ FAIL (threshold: 90%)
#
# Apply auto-fixes? [y/n]: y
#
# Applying 4 fixes...
# ✅ Fixed: AS-1C lockout threshold
# ✅ Fixed: Bundle size (lodash import)
# ✅ Fixed: Sidebar width
# ✅ Fixed: Title font-size
#
# Re-running verification...
# Overall: 82% ⚠️ WARN (threshold: 90%)
```

### CI/CD Mode

```bash
# In GitHub Actions
/speckit.verify --ci --no-auto-fix --json

# Exit code: 1 (below threshold)
# Output: reports/verify-summary.json
```

### Visual Baseline Update

```bash
# After intentional UI changes, update baselines
/speckit.verify --baseline

# Output:
# Updated 12 visual baselines
# Next run will compare against these new references
```

### Skip Sections

```bash
# Skip slow visual regression tests during iteration
/speckit.verify --skip-visual --skip-nfr

# Focus on functional correctness only
```

## Verification Sequence

```text
Phase 1: Prerequisites Check
├─ IG-VERIFY-001: Implementation complete
├─ IG-VERIFY-002: Staging available
└─ IG-VERIFY-003: Test framework ready
    ↓
Phase 2: Parallel Verification (5 agents)
├─ ac-verifier (priority 10)
├─ contract-verifier (priority 10)
├─ visual-verifier (priority 15, depends: ac-verifier)
├─ behavior-verifier (priority 20, depends: ac-verifier, contract-verifier)
└─ nfr-verifier (priority 25, depends: behavior-verifier)
    ↓
Phase 3: Report Aggregation
└─ report-aggregator (priority 30, depends: all verifiers)
    ↓
Phase 4: Auto-Fix (if enabled)
└─ auto-fixer (priority 40, depends: report-aggregator)
    ↓
Phase 5: Exit with Status
├─ If score >= 90%: Exit 0 (success)
├─ If 80% <= score < 90%: Exit 0 with warning
└─ If score < 80%: Exit 1 (failure)
```

## Output

- **reports/verify-report.md** - Comprehensive markdown report with tables
- **reports/verify-summary.json** - JSON summary for CI/CD pipelines
- **.verify/current/** - Latest screenshots (if visual verification enabled)
- **.verify/diffs/** - Diff images highlighting visual changes

## Integration

### After `/speckit.implement`

```bash
/speckit.implement
# ... implementation completes ...

/speckit.verify
# If failures: auto-fix or manually fix
# Re-run until score >= 90%
```

### Before `/speckit.merge`

```bash
/speckit.verify --threshold 95

# If pass:
/speckit.merge
```

## Exit Codes

- **0** - Verification passed (score >= threshold)
- **1** - Verification failed (score < threshold or critical failures)

## References

- **Quality Gates**: QG-VERIFY-001 through QG-VERIFY-006 in `memory/domains/quality-gates.md`
- **Report Template**: `templates/verify-report-template.md`
- **Prerequisites**: `scripts/bash/verify-prerequisites.sh`, `scripts/powershell/verify-prerequisites.ps1`
