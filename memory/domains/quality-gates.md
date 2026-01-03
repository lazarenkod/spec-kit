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

## Summary

| Type | Count |
|------|-------|
| Design Quality Gates | 3 |
| Pre-Implement Gates | 5 |
| Post-Implement Gates | 7 |
| Pre-Deploy Gates | 5 |
| Security Gates | 5 |
| **Total QG Principles** | **20** |
| MUST level | 16 |
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
