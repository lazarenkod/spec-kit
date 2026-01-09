# Domain Extension: Quality Gates (Layer 1)

**Extends**: constitution.base.md v1.0
**Regulatory Context**: CI/CD pipelines, code quality standards, deployment safety
**Typical Projects**: All production software requiring automated quality enforcement
**Philosophy**: "Quality is not a phase, it's a gate at every transition"

---

## Key Concepts

| Concept | Definition |
|---------|------------|
| **Quality Gate** | A checkpoint that must pass before workflow proceeds to next phase |
| **Pre-Implement Gate** | Validates spec/plan quality before code generation begins |
| **Post-Implement Gate** | Validates code quality after implementation completes |
| **Pre-Deploy Gate** | Validates production readiness before deployment |
| **SQS** | Spec Quality Score (0-100) measuring specification quality via 25-checkpoint rubric across 5 dimensions (Clarity, Completeness, Testability, Traceability, No Ambiguity). See [sqs-rubric.md](../../templates/shared/quality/sqs-rubric.md) |
| **DQS** | Design Quality Score (0-100) measuring design specification quality via 25-checkpoint rubric across 5 dimensions (Visual Hierarchy, Consistency, Accessibility, Responsiveness, Interaction Design). See [dqs-rubric.md](../../templates/shared/quality/dqs-rubric.md) |
| **Coverage** | Percentage of code exercised by tests (line, branch, path) |
| **Type Coverage** | Percentage of code with static type annotations |

---

## Gate Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRE-IMPLEMENT GATES                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ QG-001: SQS  │  │ QG-002: Sec  │  │ QG-003: Deps │          │
│  │   >= 80      │  │  Scan Pass   │  │  No Critical │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    /speckit.implement
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    POST-IMPLEMENT GATES                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ QG-004: Test │  │ QG-005: Type │  │ QG-006: Lint │          │
│  │ Coverage 80% │  │ Coverage 95% │  │  Zero Errors │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ QG-007: Perf │  │ QG-008: A11y │  │ QG-009: Docs │          │
│  │ Lighthouse 90│  │  WCAG 2.1 AA │  │ API Documented│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                      Pre-Deploy Check
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     PRE-DEPLOY GATES                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ QG-010: All  │  │ QG-011: No   │  │ QG-012: Env  │          │
│  │ Tests Pass   │  │ Console Logs │  │Vars Documented│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Strengthened Principles

These principles from `constitution.base.md` are elevated for quality-gated projects:

| Base ID | Original | New Level | Rationale |
|---------|----------|-----------|-----------|
| QUA-001 | SHOULD (unit) | MUST (80%+) | Coverage gate requires enforcement |
| QUA-003 | MUST | MUST (blocking) | Code review MUST block non-compliant PRs |
| QUA-004 | SHOULD | MUST | Formatter/linter MUST run in CI |
| TST-001 | SHOULD | MUST | Tests MUST map to acceptance scenarios |
| SEC-001 | MUST | MUST (scanned) | Secrets MUST be detected via automated scanning |

---

## Design Quality Gates (QG-DQS-xxx)

> **Design Quality Score (DQS)** gates ensure design specifications meet quality standards before implementation.
> See `templates/shared/quality/dqs-rubric.md` for full rubric.

### QG-DQS-001: Minimum Design Quality Score

**Level**: MUST (for UI-heavy features)
**Applies to**: All `/speckit.implement` invocations with design.md artifacts

Design implementation MUST NOT begin until Design Quality Score (DQS) reaches minimum threshold.

**Threshold**: DQS >= 70

**DQS Rubric v1.0** (25 checkpoints across 5 dimensions):

| Dimension | Points | Key Checkpoints |
|-----------|--------|-----------------|
| **Visual Hierarchy** | 25 | Clear CTAs, heading levels, white space, visual weight, content scanning |
| **Consistency** | 20 | Token usage, component reuse, naming conventions, interaction patterns, icon system |
| **Accessibility** | 25 | Color contrast, touch targets, focus indicators, screen reader support, reduced motion |
| **Responsiveness** | 15 | Breakpoints, layout adaptation, touch vs pointer, content priority, image optimization |
| **Interaction Design** | 15 | State definitions, animation timing, loading states, error handling, success feedback |

**Formula**: `DQS = VisualHierarchy + Consistency + Accessibility + Responsiveness + InteractionDesign`

**Full Rubric**: See [templates/shared/quality/dqs-rubric.md](../../templates/shared/quality/dqs-rubric.md)

**Validation**:
```bash
/speckit.analyze --profile dqs
# Output: DQS: 85/100 (Visual: 22, Consist: 18, A11y: 23, Resp: 12, Interact: 10)
```

**Thresholds**:
- **≥70**: Ready for implementation
- **50-69**: Needs improvement (iterate on design)
- **<50**: Major rework required (block implementation)

**Violations**: HIGH - Design not ready, implementation will have UX issues

---

### QG-DQS-002: Accessibility Compliance

**Level**: MUST
**Applies to**: All UI features

Design MUST pass accessibility dimension with minimum score.

**Threshold**: Accessibility dimension >= 60% (15/25 points)

**Key Checks**:
- Color contrast ratios (4.5:1 text, 3:1 UI)
- Touch targets (44×44px minimum)
- Focus indicators defined
- Screen reader support documented
- Reduced motion alternatives

**Validation**:
```bash
/speckit.analyze --profile dqs --dimension accessibility
```

**Violations**: CRITICAL - Accessibility barriers for users

---

### QG-DQS-003: WCAG Compliance

**Level**: MUST
**Applies to**: All public-facing web applications

Design MUST have zero WCAG 2.1 AA violations in color contrast.

**Threshold**: All text colors meet WCAG 2.1 AA contrast requirements

**Validation**:
- Normal text: >= 4.5:1 contrast ratio
- Large text (18px+ or 14px+ bold): >= 3:1 contrast ratio
- UI components: >= 3:1 contrast ratio

**Violations**: CRITICAL - Legal compliance risk, accessibility barriers

---

## Test-First Development Gates (QG-STAGING-xxx, QG-TEST-xxx)

> **Test-First Development** gates ensure staging infrastructure is ready and tests exist before implementation.
> Tests MUST exist and FAIL before code is written (TDD).

### QG-STAGING-001: Staging Environment Ready

**Level**: MUST
**Applies to**: All `/speckit.implement` invocations
**Phase**: Pre-Implement

Local staging environment MUST be provisioned and healthy before implementation begins.

**Threshold**: All staging services pass health checks

**Validation**:
```bash
docker-compose -f .speckit/staging/docker-compose.yaml ps --format json
# All services must show "running" and "healthy"
```

**Required Services**:
| Service | Health Check | Required |
|---------|-------------|----------|
| test-db (postgres) | `pg_isready` | YES |
| test-redis | `redis-cli ping` | YES |
| playwright | Container running | For E2E features |

**Violations**: CRITICAL - Cannot run tests without infrastructure

---

### QG-TEST-001: Test Completeness

**Level**: MUST
**Applies to**: All `/speckit.tasks` outputs
**Phase**: Pre-Implement

Every Acceptance Scenario (AS-xxx) marked "Requires Test = YES" MUST have a corresponding test task.

**Threshold**: 100% coverage of required test scenarios

**Validation**:
```bash
/speckit.analyze --profile test-completeness
# Parses tasks.md TTM, compares against spec.md AS list
```

**Formula**:
```
Test Completeness = (AS with [TEST:] markers) / (AS with "Requires Test = YES") × 100
```

**Thresholds**:
- **100%**: Ready for implementation
- **<100%**: BLOCK - Add missing test tasks

**Violations**: CRITICAL - Untested acceptance scenarios

---

### QG-TEST-002: Test Infrastructure Ready

**Level**: MUST
**Applies to**: All `/speckit.implement` invocations
**Phase**: Pre-Implement

Test framework MUST be configured and executable before implementation begins.

**Threshold**: Test command runs successfully (even with 0 tests)

**Validation by Language**:

| Language | Package File | Test Command | Config File |
|----------|-------------|--------------|-------------|
| TypeScript | package.json | `npm test` | jest.config.js / vitest.config.ts |
| Python | pyproject.toml | `pytest` | pytest.ini / pyproject.toml |
| Go | go.mod | `go test ./...` | - |

**Implementation**:
```bash
# Node.js
npm test -- --passWithNoTests --coverage

# Python
pytest --collect-only || pytest --co

# Go
go test ./... -count=0
```

**Violations**: CRITICAL - Cannot verify implementation without test infrastructure

---

### QG-TEST-003: TDD Red-Green Verification

**Level**: MUST
**Applies to**: Wave 2 (Test Scaffolding) completion
**Phase**: During-Implement

All test tasks MUST have tests that FAIL initially (Red phase of TDD).

**Threshold**: 100% of new tests fail on first run (before implementation)

**Validation**:
```bash
# Run tests expecting failures
npm test -- --passWithNoTests=false
# Expected: All tests fail

# After implementation
npm test
# Expected: All tests pass
```

**Rationale**: Confirms tests are actually testing new functionality, not passing trivially.

**Violations**: HIGH - Tests may not be testing real behavior

---

### QG-TEST-004: Per-Story Test Coverage

**Level**: MUST
**Applies to**: Each story phase completion
**Phase**: Post-Story

Code coverage MUST meet minimum threshold after each story implementation.

**Threshold**: >= 80% line coverage for new code

**Validation**:
```bash
# Jest
jest --coverage --coverageThreshold='{"global":{"lines":80}}'

# Pytest
pytest --cov=src --cov-fail-under=80

# Go
go test -coverprofile=coverage.out && go tool cover -func=coverage.out
```

**Per-Story Tracking**:
| Story | Files Changed | Coverage Before | Coverage After | Delta |
|-------|--------------|-----------------|----------------|-------|
| US1 | 5 | N/A | 85% | +85% |
| US2 | 3 | 85% | 82% | -3% |

**Violations**: CRITICAL if < 70%, HIGH if 70-80%

---

## Component Integration Gates (QG-COMP-xxx)

> **Component Integration Quality Gates** ensure UI components are not just created but actually integrated into all target screens.
> Prevents "orphan components" - components that exist but are never used in navigation.

### QG-COMP-001: Component Registration

**Level**: MUST (for UI features with Component Registry)
**Applies to**: All `/speckit.tasks` outputs for features with UI Component Registry
**Phase**: Pre-Implement

Every component creation task in Phase 2b MUST have a `[COMP:COMP-xxx]` marker linking to Component Registry.

**Threshold**: 100% of Phase 2b component tasks have [COMP:] markers

**Validation**:
```bash
# Parse tasks.md Phase 2b, extract component creation tasks
# Verify each has [COMP:COMP-xxx] marker
# Verify COMP-xxx exists in spec.md Component Registry
```

**Implementation**:
```
FOR EACH task IN Phase_2b_tasks:
  IF task.description contains "Create.*Component" OR ".*View" OR ".*Button":
    IF NOT task.markers contains "[COMP:COMP-xxx]":
      ERROR: "Component task missing [COMP:] marker: {task}"
    IF NOT Component_Registry contains task.COMP_id:
      ERROR: "COMP-{id} not found in Component Registry"
```

**Violations**: HIGH - Component not traceable to spec

---

### QG-COMP-002: Wire Task Coverage

**Level**: MUST (for UI features with Component Registry)
**Applies to**: All `/speckit.tasks` outputs for features with UI Component Registry
**Phase**: Pre-Implement

Every (Component, Target Screen) pair from Component Registry MUST have a corresponding wire task.

**Threshold**: 100% of (Component, Target Screen) pairs have [WIRE:] tasks

**Validation**:
```bash
/speckit.analyze --profile component-coverage
# Output: CSIM coverage: X/Y pairs have wire tasks (Z%)
```

**Implementation**:
```
FOR EACH comp IN Component_Registry:
  FOR EACH screen_id IN comp.Target_Screens:
    FIND task with marker "[WIRE:{comp.id}→{screen_id}]"
    IF NOT FOUND:
      ERROR: "Missing wire task: {comp.id} → {screen_id}"
      ERROR: "Add: - [ ] TXXX [WIRE:{comp.id}→{screen_id}] Wire {comp.name} into {screen.name}"
```

**CSIM Matrix Validation**:
```
CSIM_PAIRS = Component_Registry × Screen_Registry (via Target_Screens)
WIRE_TASKS = tasks with [WIRE:*] markers
COVERAGE = len(WIRE_TASKS) / len(CSIM_PAIRS) × 100

IF COVERAGE < 100%:
  BLOCK: "CSIM coverage {COVERAGE}% < 100%. Missing wire tasks for:"
  FOR EACH missing_pair:
    OUTPUT: "  - {comp.name} → {screen.name}"
```

**Violations**: CRITICAL - Components will not appear in navigation screens

---

### QG-COMP-003: Screen Component Completeness

**Level**: MUST (for UI features with Screen Registry)
**Applies to**: All `/speckit.tasks` outputs for features with Screen Registry
**Phase**: Pre-Implement

Every screen MUST have wire tasks for ALL its Required Components (from Screen Registry).

**Threshold**: 100% of screens have wire tasks for all Required Components

**Validation**:
```bash
/speckit.analyze --profile screen-completeness
# Output: Screen coverage: X/Y screens fully wired (Z%)
```

**Implementation**:
```
FOR EACH screen IN Screen_Registry:
  FOR EACH comp_id IN screen.Required_Components:
    FIND task with marker "[WIRE:{comp_id}→{screen.id}]"
    IF NOT FOUND:
      ERROR: "{screen.name} missing wire task for {comp_id}"
```

**Violations**: CRITICAL - Screen will show placeholders instead of components

---

### QG-COMP-004: No Orphan Components (Post-Implement)

**Level**: MUST (for UI features)
**Applies to**: `/speckit.analyze` QA mode after implementation
**Phase**: Post-Implement

Every completed wire task MUST result in actual component usage in the screen file.

**Threshold**: 100% of completed [WIRE:] tasks have import AND usage in screen

**Validation**:
```bash
/speckit.analyze --profile qa --check orphan-components
# Output: Orphan detection: X/Y wire tasks verified (Z%)
```

**Implementation** (code-level validation):
```
FOR EACH wire_task WHERE status = "[x]":
  comp_file = resolve from [COMP:{comp_id}] task
  screen_file = resolve from [SCREEN:{screen_id}] task

  # Check import
  SCAN screen_file for import of comp_file
  IF NOT FOUND:
    CRITICAL: "Missing import: {comp_name} not imported in {screen_file}"

  # Check usage
  SCAN screen_file for usage of component (function call, JSX tag, Compose call)
  IF NOT FOUND:
    CRITICAL: "Orphan component: {comp_name} imported but not used in {screen_file}"

  # Check for placeholders
  SCAN screen_file for placeholder patterns:
    - Text("...placeholder...")
    - Text("{screen_name}")  # e.g., Text("Settings")
    - TODO:, FIXME: in render body
    - EmptyView(), Spacer() where component should be
  IF FOUND:
    WARNING: "Placeholder detected in {screen_file}: {pattern}"
```

**Violations**: CRITICAL - Tasks marked complete but integration not done

---

### Component Integration Gates Summary

| Gate ID | Phase | Level | Threshold | Validation | Violation |
|---------|-------|-------|-----------|------------|-----------|
| QG-COMP-001 | Pre-Implement | MUST | 100% markers | [COMP:] check | HIGH |
| QG-COMP-002 | Pre-Implement | MUST | 100% pairs | CSIM coverage | CRITICAL |
| QG-COMP-003 | Pre-Implement | MUST | 100% screens | Screen completeness | CRITICAL |
| QG-COMP-004 | Post-Implement | MUST | 100% wired | Orphan detection | CRITICAL |

---

## Pre-Implement Gates

### QG-001: Minimum Spec Quality Score

**Level**: MUST
**Applies to**: All `/speckit.implement` invocations

Implementation MUST NOT begin until Spec Quality Score (SQS) reaches minimum threshold.

**Threshold**: SQS >= 80

**SQS Rubric v2.0** (25 checkpoints across 5 dimensions):

| Dimension | Points | Key Checkpoints |
|-----------|--------|-----------------|
| **Clarity** | 25 | RFC 2119 keywords, no vague terms, specific numbers, measurable success, defined failures |
| **Completeness** | 25 | FRs documented, NFRs specified, edge cases, dependencies, security |
| **Testability** | 25 | Each FR has AC, concrete scenarios, performance metrics, error conditions, integration points |
| **Traceability** | 15 | Unique IDs, concept cross-refs, feature dependencies, FR→AC→Test chain, no orphans |
| **No Ambiguity** | 10 | No hedge words, terms defined, clarifications resolved, scope explicit, assumptions documented |

**Formula**: `SQS = Clarity + Completeness + Testability + Traceability + NoAmbiguity`

**Full Rubric**: See [templates/shared/quality/sqs-rubric.md](../../templates/shared/quality/sqs-rubric.md)

**Validation**:
```bash
/speckit.analyze --profile sqs
# Output: SQS: 85/100 (Clarity: 22, Complete: 23, Test: 20, Trace: 12, Ambig: 8)
```

**Thresholds**:
- **≥80**: Ready for implementation
- **60-79**: Needs improvement (run `/speckit.clarify`)
- **<60**: Major rework required (block implementation)

**Violations**: CRITICAL - Spec not ready, implementation will fail or drift

---

### QG-002: Security Scan Pass

**Level**: MUST
**Applies to**: All projects with dependencies

All dependencies MUST pass security vulnerability scan with no critical or high severity issues.

**Threshold**: 0 critical/high vulnerabilities

**Implementation**:
```bash
# Node.js
npm audit --audit-level=high

# Python
pip-audit --strict

# Go
govulncheck ./...
```

**Validation**: Exit code 0 from security scanner
**Violations**: CRITICAL - Known vulnerabilities before implementation

---

### QG-003: Dependency Freshness

**Level**: SHOULD
**Applies to**: All projects with external dependencies

Dependencies SHOULD NOT be more than 2 major versions behind current stable release.

**Threshold**: No critical dependencies > 2 major versions behind

**Implementation**:
```bash
# Node.js
npx npm-check-updates

# Python
pip list --outdated

# Check for critical deps only (React, Express, Django, etc.)
```

**Validation**: Review output for major version gaps
**Violations**: HIGH - Technical debt, missing security patches

---

## Post-Implement Gates

### QG-004: Test Coverage

**Level**: MUST
**Applies to**: All production code

Code MUST have minimum test coverage threshold enforced in CI.

**Threshold**: >= 80% line coverage

**Implementation**:
```bash
# Jest (Node.js)
jest --coverage --coverageThreshold='{"global":{"lines":80}}'

# Pytest (Python)
pytest --cov=src --cov-fail-under=80

# Go
go test -coverprofile=coverage.out && go tool cover -func=coverage.out
```

**Coverage Report Parsing**:
```typescript
// Parse lcov or coverage-summary.json
const coverage = JSON.parse(fs.readFileSync('coverage/coverage-summary.json'));
if (coverage.total.lines.pct < 80) {
  throw new Error(`Coverage ${coverage.total.lines.pct}% below 80% threshold`);
}
```

**Validation**: Coverage report shows >= 80%
**Violations**: CRITICAL - Untested code paths may contain bugs

---

### QG-005: Type Coverage

**Level**: MUST
**Applies to**: TypeScript, Python with type hints

Code MUST have static type annotations covering specified threshold.

**Threshold**: >= 95% type coverage

**Implementation**:
```bash
# TypeScript
npx type-coverage --at-least 95

# Python (mypy)
mypy src/ --strict --ignore-missing-imports

# Python (pyright)
pyright --verifytypes src
```

**Validation**: Type coverage tool reports >= 95%
**Violations**: HIGH - Runtime type errors risk

---

### QG-006: Lint Cleanliness

**Level**: MUST
**Applies to**: All source code

Code MUST pass linting with zero errors and minimal warnings.

**Threshold**: 0 errors, < 10 warnings

**Implementation**:
```bash
# TypeScript/JavaScript
eslint src/ --max-warnings 10

# Python
ruff check src/ --fix

# Go
golangci-lint run
```

**Validation**: Linter exit code 0 with warning count < 10
**Violations**: HIGH - Code quality issues, inconsistent style

---

### QG-007: Performance Baseline

**Level**: SHOULD
**Applies to**: User-facing web applications

Web applications SHOULD meet Lighthouse performance score threshold.

**Threshold**: Lighthouse Performance >= 90

**Implementation**:
```bash
# Lighthouse CI
lighthouse http://localhost:3000 --only-categories=performance --output=json

# Parse result
jq '.categories.performance.score * 100' lighthouse-report.json
```

**Metrics Checked**:
- First Contentful Paint < 1.8s
- Largest Contentful Paint < 2.5s
- Total Blocking Time < 200ms
- Cumulative Layout Shift < 0.1

**Validation**: Lighthouse performance score >= 90
**Violations**: MEDIUM - Poor user experience, SEO impact

---

### QG-008: Accessibility Compliance

**Level**: SHOULD
**Applies to**: User-facing web applications

Web applications SHOULD meet WCAG 2.1 Level AA accessibility standards.

**Threshold**: Zero WCAG 2.1 AA violations

**Implementation**:
```bash
# axe-core via CLI
npx @axe-core/cli http://localhost:3000

# Lighthouse accessibility
lighthouse http://localhost:3000 --only-categories=accessibility

# Playwright with axe
await expect(page).toHaveNoViolations();
```

**Key Checks**:
- Color contrast ratios
- Keyboard navigation
- Screen reader compatibility
- Focus management
- Alt text for images

**Validation**: axe-core or Lighthouse reports 0 violations
**Violations**: MEDIUM - Accessibility barriers for users

---

### QG-009: Documentation Coverage

**Level**: SHOULD
**Applies to**: Public APIs and library code

All public APIs SHOULD have documentation coverage.

**Threshold**: 100% of public exports documented

**Implementation**:
```bash
# TypeScript (TypeDoc)
typedoc --validation.notDocumented

# Python (pydocstyle)
pydocstyle src/ --convention=google

# JSDoc coverage
npx jsdoc-coverage src/
```

**Documentation Requirements**:
- Function/method descriptions
- Parameter types and descriptions
- Return value documentation
- Usage examples for complex APIs

**Validation**: Documentation coverage tool reports 100% public API coverage
**Violations**: LOW - Maintainability and onboarding impact

---

## Pre-Deploy Gates

### QG-010: All Tests Pass

**Level**: MUST
**Applies to**: All deployments

Deployment MUST NOT proceed if any test fails.

**Threshold**: 100% test pass rate

**Implementation**:
```bash
# Run full test suite
npm test
pytest
go test ./...

# Check exit code
if [ $? -ne 0 ]; then
  echo "Tests failed - blocking deployment"
  exit 1
fi
```

**Test Categories**:
- Unit tests
- Integration tests
- E2E tests (if applicable)
- Contract tests (if applicable)

**Validation**: Test runner exit code 0
**Violations**: CRITICAL - Broken functionality will reach production

---

### QG-011: No Debug Artifacts

**Level**: MUST
**Applies to**: Production builds

Production code MUST NOT contain debug statements or development artifacts.

**Threshold**: 0 debug artifacts found

**Forbidden Patterns**:
```bash
# JavaScript/TypeScript
console.log
console.debug
console.warn (review case-by-case)
debugger
alert(

# Python
print(  # in non-CLI code
pdb.set_trace()
breakpoint()
import pdb

# General
TODO
FIXME
HACK
XXX
```

**Implementation**:
```bash
# Check for debug statements
grep -rn "console\.log\|debugger" src/ --include="*.ts" --include="*.tsx"

# Check for development markers
grep -rn "TODO\|FIXME\|HACK\|XXX" src/
```

**Validation**: grep returns no matches
**Violations**: HIGH - Information leakage, unfinished code in production

---

### QG-012: Environment Documentation

**Level**: MUST
**Applies to**: All deployable applications

All required environment variables MUST be documented in `.env.example`.

**Threshold**: 100% env var documentation coverage

**Implementation**:
```bash
#!/bin/bash
# scripts/check-env-coverage.sh

# Find all env var references in code
CODE_ENVS=$(grep -roh "process\.env\.\w\+" src/ | sort -u | sed 's/process\.env\.//')

# Find documented env vars
DOC_ENVS=$(grep -oh "^\w\+=" .env.example | sed 's/=//' | sort -u)

# Find undocumented
UNDOC=$(comm -23 <(echo "$CODE_ENVS") <(echo "$DOC_ENVS"))

if [ -n "$UNDOC" ]; then
  echo "Undocumented environment variables:"
  echo "$UNDOC"
  exit 1
fi
```

**Documentation Format** (`.env.example`):
```bash
# Database connection (required)
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# Redis cache (optional, defaults to in-memory)
REDIS_URL=

# Feature flags
FEATURE_NEW_UI=false
```

**Validation**: All runtime env vars present in .env.example
**Violations**: HIGH - Deployment failures, configuration drift

---

## Security Gates (QG-SEC-xxx)

> **Security by Design** gates ensure security is embedded throughout the development lifecycle.
> See `memory/domains/security.md` for full Security by Design framework.

### QG-SEC-001: Threat Model Required

**Level**: MUST (for Confidential+ data classification)
**Applies to**: Features handling Confidential or Restricted data

A threat model MUST be completed before implementation begins for features handling sensitive data.

**Threshold**: `threat-model.md` exists with all STRIDE categories addressed

**Implementation**:
```bash
# Check threat model exists
ls .speckit/threat-model.md

# Validate STRIDE coverage
grep -c "### 4\.[1-6]" .speckit/threat-model.md  # Should return 6
```

**Validation**: Threat model file exists with complete STRIDE analysis
**Violations**: CRITICAL - Unknown security risks will reach production

---

### QG-SEC-002: OWASP Top 10 Addressed

**Level**: MUST
**Applies to**: All web applications and APIs

All applicable OWASP Top 10 vulnerabilities MUST have documented mitigations.

**Threshold**: Security checklist 100% complete for applicable items

**Implementation**:
```bash
# Check OWASP checklist completion
grep -c "\[x\]" .speckit/security-checklist.md
grep -c "\[ \]" .speckit/security-checklist.md  # Should be 0
```

**Validation**: All applicable OWASP checklist items marked complete
**Violations**: CRITICAL - Known vulnerability patterns not addressed

---

### QG-SEC-003: Dependency Scan Clean

**Level**: MUST
**Applies to**: All projects with dependencies

All dependencies MUST pass security vulnerability scan with no critical or high severity issues.

**Threshold**: 0 critical/high vulnerabilities

**Implementation**:
```bash
# Node.js
npm audit --audit-level=high

# Python
pip-audit --strict

# Go
govulncheck ./...

# Multi-language
snyk test --severity-threshold=high
```

**Validation**: Security scanner exit code 0
**Violations**: CRITICAL - Known vulnerable dependencies

---

### QG-SEC-004: Secret Scanning

**Level**: MUST
**Applies to**: All repositories

Codebase MUST NOT contain hardcoded secrets, API keys, or credentials.

**Threshold**: 0 secrets found in codebase

**Implementation**:
```bash
# Gitleaks
gitleaks detect --source . --verbose

# TruffleHog
trufflehog filesystem --directory=. --only-verified

# GitHub (if using)
gh secret scanning alerts list
```

**Validation**: Secret scanner reports 0 findings
**Violations**: CRITICAL - Credentials exposed in version control

---

### QG-SEC-005: Security Testing

**Level**: SHOULD
**Applies to**: Features with authentication or authorization

Security-critical flows SHOULD have dedicated security tests.

**Threshold**: Auth/authz tests exist and pass

**Implementation**:
```bash
# Check for security tests
find tests/ -name "*auth*" -o -name "*security*" | wc -l

# Run security-focused tests
npm test -- --grep "security\|auth"
pytest -k "security or auth"
```

**Coverage Requirements**:
- Authentication flows (login, logout, session)
- Authorization checks (role-based access)
- Input validation (injection prevention)
- Rate limiting behavior

**Validation**: Security tests exist and pass
**Violations**: MEDIUM - Untested security controls

---

## Gate Enforcement Matrix

| Gate | Phase | Level | Threshold | Validation Command | Severity |
|------|-------|-------|-----------|-------------------|----------|
| QG-COMP-001 | Pre-Implement | MUST | 100% markers | `/speckit.analyze --profile component-coverage` | HIGH |
| QG-COMP-002 | Pre-Implement | MUST | 100% pairs | `/speckit.analyze --profile component-coverage` | CRITICAL |
| QG-COMP-003 | Pre-Implement | MUST | 100% screens | `/speckit.analyze --profile screen-completeness` | CRITICAL |
| QG-COMP-004 | Post-Implement | MUST | 100% wired | `/speckit.analyze --profile qa --check orphan-components` | CRITICAL |
| QG-DQS-001 | Pre-Implement | MUST | DQS >= 70 | `/speckit.analyze --profile dqs` | HIGH |
| QG-DQS-002 | Pre-Implement | MUST | A11y >= 60% | `/speckit.analyze --profile dqs --dimension accessibility` | CRITICAL |
| QG-DQS-003 | Pre-Implement | MUST | WCAG AA | Contrast ratio validation | CRITICAL |
| QG-001 | Pre-Implement | MUST | SQS >= 80 | `/speckit.analyze --profile sqs` | CRITICAL |
| QG-002 | Pre-Implement | MUST | 0 critical | `npm audit --audit-level=high` | CRITICAL |
| QG-003 | Pre-Implement | SHOULD | < 2 major | `npx npm-check-updates` | HIGH |
| QG-004 | Post-Implement | MUST | >= 80% | `jest --coverage` | CRITICAL |
| QG-005 | Post-Implement | MUST | >= 95% | `npx type-coverage` | HIGH |
| QG-006 | Post-Implement | MUST | 0 errors | `npm run lint` | HIGH |
| QG-007 | Post-Implement | SHOULD | >= 90 | `lighthouse` | MEDIUM |
| QG-008 | Post-Implement | SHOULD | WCAG AA | `axe-core` | MEDIUM |
| QG-009 | Post-Implement | SHOULD | 100% public | TypeDoc coverage | LOW |
| QG-010 | Pre-Deploy | MUST | 100% pass | `npm test` | CRITICAL |
| QG-011 | Pre-Deploy | MUST | 0 found | grep patterns | HIGH |
| QG-012 | Pre-Deploy | MUST | 100% | env coverage script | HIGH |
| QG-SEC-001 | Pre-Implement | MUST | threat-model.md | STRIDE coverage check | CRITICAL |
| QG-SEC-002 | Pre-Implement | MUST | 100% checklist | OWASP checklist | CRITICAL |
| QG-SEC-003 | Pre-Deploy | MUST | 0 critical/high | `npm audit` / `pip-audit` | CRITICAL |
| QG-SEC-004 | Pre-Deploy | MUST | 0 secrets | `gitleaks` / `trufflehog` | CRITICAL |
| QG-SEC-005 | Post-Implement | SHOULD | tests exist | security test grep | MEDIUM |

---

## Migration Gates (QG-MIG-xxx)

> **Migration Quality Gates** ensure migration plans are safe and reversible before execution.
> See `templates/commands/migrate.md` for migration planning command.

### QG-MIG-001: Rollback Plan Required

**Level**: MUST
**Applies to**: All `/speckit.migrate` generated plans

Every migration phase (MIG-xxx) MUST have a documented rollback strategy.

**Threshold**: 100% of MIG-xxx phases have rollback procedures

**Validation**:
```bash
/speckit.analyze --profile migration
# Validates: Each MIG-xxx has rollback_strategy defined
```

**Rollback Types**:
| Type | Duration | Use Case |
|------|----------|----------|
| IMMEDIATE | < 5 min | Config changes, feature flags |
| GRADUAL | 10-30 min | Traffic shifting, API versioning |
| FULL | 30-60 min | Data migrations, schema changes |

**Violations**: CRITICAL - Migration without rollback is unrecoverable

---

### QG-MIG-002: Risk Mitigation Required

**Level**: MUST
**Applies to**: All migration plans with HIGH or CRITICAL risks

All HIGH (score ≥ 10) and CRITICAL (score ≥ 15) risks MUST have documented mitigations.

**Threshold**: 100% of HIGH+ risks have mitigation strategies

**Risk Score Calculation**: `probability (1-5) × impact (1-5)`

**Severity Levels**:
| Score | Severity | Mitigation Required |
|-------|----------|---------------------|
| 15-25 | CRITICAL | MUST (blocks planning) |
| 10-14 | HIGH | MUST (blocks planning) |
| 5-9 | MEDIUM | SHOULD |
| 1-4 | LOW | Optional |

**Validation**:
```bash
/speckit.analyze --profile migration-risks
# Validates: All RISK-MIG-xxx with score >= 10 have mitigation field
```

**Violations**: CRITICAL - High-risk migration without mitigation

---

### QG-MIG-003: Coupling Analysis Complete

**Level**: MUST
**Applies to**: All `--from monolith` migrations

Coupling analysis MUST be completed before phase planning for monolith decomposition.

**Threshold**: All modules analyzed with instability index calculated

**Required Metrics**:
- Afferent coupling (Ca) - modules that depend on this
- Efferent coupling (Ce) - modules this depends on
- Instability index I = Ce / (Ca + Ce)
- Coupling classification (TIGHT ≥ 10, LOOSE 3-9, MINIMAL 0-2)

**Validation**:
```bash
/speckit.analyze --profile coupling
# Output: N modules analyzed, M% classified as TIGHT
```

**Violations**: HIGH - Extraction order undefined, risk of cascading failures

---

### Migration Gate Summary

| Gate ID | Phase | Level | Threshold | Validation | Violation |
|---------|-------|-------|-----------|------------|-----------|
| QG-MIG-001 | Pre-Plan | MUST | 100% phases | rollback check | CRITICAL |
| QG-MIG-002 | Pre-Plan | MUST | HIGH+ mitigated | risk check | CRITICAL |
| QG-MIG-003 | Pre-Plan | MUST | all modules | coupling check | HIGH |

---

## Property-Based Testing Gates

| Gate ID | Name | Threshold | Severity | Description |
|---------|------|-----------|----------|-------------|
| VG-PROP | Property Coverage | ≥80% | CRITICAL | FR/AS requirements covered by properties |
| VG-PROP-SEC | Security Property Coverage | ≥95% | CRITICAL | EC-SEC-* covered by security properties |
| VG-PROP-BOUND | Boundary Property Coverage | ≥90% | HIGH | EC-* edge cases covered |
| VG-EARS | EARS Transformation | ≥85% | HIGH | Requirements in EARS canonical form |
| VG-SHRUNK | Shrunk Examples | ≥3 per property | MEDIUM | Minimal counterexamples preserved |
| VG-PGS | PGS Resolution | 100% | CRITICAL | All PGS iterations resolved |
| VG-PQS | Property Quality Score | ≥70 | HIGH | Overall PBT quality metric |

### PQS Calculation

```
PQS = (
  Requirement_Coverage × 0.30 +
  Type_Diversity × 0.20 +
  Generator_Quality × 0.20 +
  Shrunk_Examples × 0.15 +
  EARS_Alignment × 0.15
) × 100
```

### Gate Enforcement

- **VG-PROP < 80%**: Block merge, require property addition
- **VG-PROP-SEC < 95%**: Block merge, security review required
- **VG-PGS < 100%**: Block merge, resolve counterexamples first
- **VG-PQS < 70**: Warning, suggest improvements

---

## Summary

| Type | Count |
|------|-------|
| Component Integration Gates | 4 |
| Design Quality Gates | 3 |
| Test-First Development Gates | 4 |
| Pre-Implement Gates | 5 |
| Post-Implement Gates | 7 |
| Pre-Deploy Gates | 5 |
| Security Gates | 5 |
| Migration Gates | 3 |
| Property-Based Testing Gates | 7 |
| **Total QG Principles** | **38** |
| MUST level | 27 |
| SHOULD level | 4 |

---

## When to Use

Apply this domain extension when:
- Building production software with CI/CD pipelines
- Requiring automated quality enforcement
- Working in teams with code review requirements
- Deploying to environments with quality SLAs
- Following DevOps/SRE best practices

---

## Combining with Other Domains

| Combined With | Notes |
|---------------|-------|
| **Production** | Recommended - adds observability on top of quality gates |
| **SaaS** | Multi-tenant: gates apply per-tenant deployment |
| **FinTech** | Strengthen coverage to 90%, add compliance gates |
| **Healthcare** | Add HIPAA-specific security scanning gates |
| **E-Commerce** | Add PCI DSS compliance gates for payment code |

---

## Usage

```bash
# Activate quality gates domain
cp memory/domains/quality-gates.md memory/constitution.domain.md

# Or combine with other domains
cat memory/domains/production.md memory/domains/quality-gates.md > memory/constitution.domain.md

# Run gate validation
/speckit.analyze --profile quality-gates
```

---

## Related Templates

- `templates/shared/ci-templates.md` - GitHub Actions/GitLab CI workflows with gates
- `templates/shared/metrics-framework.md` - SQS calculation and quality metrics
- `templates/commands/analyze.md` - Quality gate validation command
