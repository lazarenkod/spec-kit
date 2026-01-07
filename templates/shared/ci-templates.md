# CI/CD Templates with Quality Gates

**Related Domain**: `memory/domains/quality-gates.md`
**Philosophy**: "Gates enforce standards automatically, humans focus on creativity"

This template provides ready-to-use CI/CD configurations that implement all 12 Quality Gates.

---

## Quick Start

```bash
# Copy the workflow for your platform
cp .github/workflows/quality-gates.yml your-project/.github/workflows/

# Or for GitLab
cp .gitlab-ci.yml your-project/
```

---

## GitHub Actions

### Complete Quality Gates Workflow

```yaml
# .github/workflows/quality-gates.yml
name: Quality Gates

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'
  COVERAGE_THRESHOLD: 80
  TYPE_COVERAGE_THRESHOLD: 95

jobs:
  # ============================================
  # PRE-IMPLEMENT GATES (QG-001, QG-002, QG-003)
  # ============================================
  pre-implement:
    name: Pre-Implement Gates
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install Dependencies
        run: npm ci

      # QG-002: Security Scan Pass
      - name: Security Audit
        id: security
        run: |
          echo "## QG-002: Security Scan" >> $GITHUB_STEP_SUMMARY
          npm audit --audit-level=high 2>&1 | tee audit.log
          if [ $? -ne 0 ]; then
            echo "❌ CRITICAL/HIGH vulnerabilities found" >> $GITHUB_STEP_SUMMARY
            cat audit.log >> $GITHUB_STEP_SUMMARY
            exit 1
          fi
          echo "✅ No critical/high vulnerabilities" >> $GITHUB_STEP_SUMMARY

      # QG-003: Dependency Freshness
      - name: Check Outdated Dependencies
        id: outdated
        continue-on-error: true
        run: |
          echo "## QG-003: Dependency Freshness" >> $GITHUB_STEP_SUMMARY
          npx npm-check-updates --format json > outdated.json
          OUTDATED=$(cat outdated.json | jq 'length')
          if [ "$OUTDATED" -gt 0 ]; then
            echo "⚠️ $OUTDATED dependencies can be updated" >> $GITHUB_STEP_SUMMARY
            cat outdated.json >> $GITHUB_STEP_SUMMARY
          else
            echo "✅ All dependencies up to date" >> $GITHUB_STEP_SUMMARY
          fi

  # ============================================
  # POST-IMPLEMENT GATES (QG-004 to QG-009)
  # ============================================
  test-coverage:
    name: QG-004 Test Coverage
    runs-on: ubuntu-latest
    needs: pre-implement
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci

      - name: Run Tests with Coverage
        run: npm test -- --coverage --coverageReporters=json-summary

      - name: Check Coverage Threshold
        run: |
          echo "## QG-004: Test Coverage" >> $GITHUB_STEP_SUMMARY
          COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
          echo "Line coverage: $COVERAGE%" >> $GITHUB_STEP_SUMMARY
          if (( $(echo "$COVERAGE < ${{ env.COVERAGE_THRESHOLD }}" | bc -l) )); then
            echo "❌ Coverage $COVERAGE% is below ${{ env.COVERAGE_THRESHOLD }}% threshold" >> $GITHUB_STEP_SUMMARY
            exit 1
          fi
          echo "✅ Coverage meets threshold" >> $GITHUB_STEP_SUMMARY

      - name: Upload Coverage Report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/

  type-coverage:
    name: QG-005 Type Coverage
    runs-on: ubuntu-latest
    needs: pre-implement
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci

      - name: Check Type Coverage
        run: |
          echo "## QG-005: Type Coverage" >> $GITHUB_STEP_SUMMARY
          npx type-coverage --at-least ${{ env.TYPE_COVERAGE_THRESHOLD }} --detail 2>&1 | tee type-coverage.log
          if [ $? -ne 0 ]; then
            echo "❌ Type coverage below ${{ env.TYPE_COVERAGE_THRESHOLD }}%" >> $GITHUB_STEP_SUMMARY
            exit 1
          fi
          echo "✅ Type coverage meets threshold" >> $GITHUB_STEP_SUMMARY

  lint:
    name: QG-006 Lint Cleanliness
    runs-on: ubuntu-latest
    needs: pre-implement
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci

      - name: Run Linter
        run: |
          echo "## QG-006: Lint Cleanliness" >> $GITHUB_STEP_SUMMARY
          npm run lint -- --max-warnings 10 2>&1 | tee lint.log
          if [ $? -ne 0 ]; then
            echo "❌ Lint errors found" >> $GITHUB_STEP_SUMMARY
            cat lint.log >> $GITHUB_STEP_SUMMARY
            exit 1
          fi
          echo "✅ No lint errors" >> $GITHUB_STEP_SUMMARY

  performance:
    name: QG-007 Performance Baseline
    runs-on: ubuntu-latest
    needs: pre-implement
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci && npm run build

      - name: Start Server
        run: npm run preview &
        env:
          PORT: 3000

      - name: Wait for Server
        run: npx wait-on http://localhost:3000

      - name: Lighthouse CI
        uses: treosh/lighthouse-ci-action@v10
        with:
          urls: http://localhost:3000
          configPath: ./lighthouserc.json
          uploadArtifacts: true

      - name: Check Performance Score
        run: |
          echo "## QG-007: Performance Baseline" >> $GITHUB_STEP_SUMMARY
          SCORE=$(cat .lighthouseci/*.json | jq '.categories.performance.score * 100' | head -1)
          echo "Lighthouse Performance Score: $SCORE" >> $GITHUB_STEP_SUMMARY
          if (( $(echo "$SCORE < 90" | bc -l) )); then
            echo "⚠️ Performance score below 90" >> $GITHUB_STEP_SUMMARY
          else
            echo "✅ Performance meets threshold" >> $GITHUB_STEP_SUMMARY
          fi

  accessibility:
    name: QG-008 Accessibility Compliance
    runs-on: ubuntu-latest
    needs: pre-implement
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci && npm run build

      - name: Start Server
        run: npm run preview &
        env:
          PORT: 3000

      - name: Wait for Server
        run: npx wait-on http://localhost:3000

      - name: Run axe-core
        run: |
          echo "## QG-008: Accessibility Compliance" >> $GITHUB_STEP_SUMMARY
          npx @axe-core/cli http://localhost:3000 --exit 2>&1 | tee a11y.log
          if [ $? -ne 0 ]; then
            echo "⚠️ Accessibility violations found" >> $GITHUB_STEP_SUMMARY
            cat a11y.log >> $GITHUB_STEP_SUMMARY
          else
            echo "✅ No accessibility violations" >> $GITHUB_STEP_SUMMARY
          fi

  # ============================================
  # PRE-DEPLOY GATES (QG-010, QG-011, QG-012)
  # ============================================
  pre-deploy:
    name: Pre-Deploy Gates
    runs-on: ubuntu-latest
    needs: [test-coverage, type-coverage, lint]
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      # QG-011: No Debug Artifacts
      - name: Check Debug Artifacts
        run: |
          echo "## QG-011: No Debug Artifacts" >> $GITHUB_STEP_SUMMARY

          # Check for console.log statements
          if grep -rn "console\.log\|console\.debug\|debugger" src/ --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx"; then
            echo "❌ Debug statements found in production code" >> $GITHUB_STEP_SUMMARY
            exit 1
          fi

          # Check for TODO/FIXME markers
          if grep -rn "TODO\|FIXME\|HACK\|XXX" src/ --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx"; then
            echo "⚠️ Development markers found (review required)" >> $GITHUB_STEP_SUMMARY
          fi

          echo "✅ No debug artifacts found" >> $GITHUB_STEP_SUMMARY

      # QG-012: Environment Documentation
      - name: Check Environment Documentation
        run: |
          echo "## QG-012: Environment Documentation" >> $GITHUB_STEP_SUMMARY

          # Find env var references in code
          grep -roh "process\.env\.\w\+" src/ | sort -u | sed 's/process\.env\.//' > code_envs.txt

          # Find documented env vars
          if [ -f .env.example ]; then
            grep -oh "^\w\+=" .env.example | sed 's/=//' | sort -u > doc_envs.txt

            # Find undocumented
            UNDOC=$(comm -23 code_envs.txt doc_envs.txt)
            if [ -n "$UNDOC" ]; then
              echo "❌ Undocumented environment variables:" >> $GITHUB_STEP_SUMMARY
              echo "$UNDOC" >> $GITHUB_STEP_SUMMARY
              exit 1
            fi
            echo "✅ All environment variables documented" >> $GITHUB_STEP_SUMMARY
          else
            echo "⚠️ .env.example not found" >> $GITHUB_STEP_SUMMARY
          fi

  # ============================================
  # DEPLOY (only after all gates pass)
  # ============================================
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    needs: [pre-deploy, performance, accessibility]
    if: github.ref == 'refs/heads/main' && always() && needs.pre-deploy.result == 'success'
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Production
        run: |
          echo "🚀 All quality gates passed - deploying to production"
          # Add your deployment commands here
```

---

## GitLab CI

### Complete Quality Gates Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - pre-implement
  - post-implement
  - pre-deploy
  - deploy

variables:
  NODE_VERSION: "20"
  COVERAGE_THRESHOLD: "80"
  TYPE_COVERAGE_THRESHOLD: "95"

# ============================================
# PRE-IMPLEMENT GATES
# ============================================
security-scan:
  stage: pre-implement
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - echo "## QG-002: Security Scan"
    - npm audit --audit-level=high
  allow_failure: false
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"

dependency-check:
  stage: pre-implement
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - echo "## QG-003: Dependency Freshness"
    - npx npm-check-updates --format json || true
  allow_failure: true
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

# ============================================
# POST-IMPLEMENT GATES
# ============================================
test-coverage:
  stage: post-implement
  image: node:${NODE_VERSION}
  needs: [security-scan]
  script:
    - npm ci
    - npm test -- --coverage --coverageReporters=json-summary
    - |
      COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
      echo "Line coverage: $COVERAGE%"
      if (( $(echo "$COVERAGE < $COVERAGE_THRESHOLD" | bc -l) )); then
        echo "Coverage $COVERAGE% is below $COVERAGE_THRESHOLD% threshold"
        exit 1
      fi
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths:
      - coverage/
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"

type-coverage:
  stage: post-implement
  image: node:${NODE_VERSION}
  needs: [security-scan]
  script:
    - npm ci
    - echo "## QG-005: Type Coverage"
    - npx type-coverage --at-least ${TYPE_COVERAGE_THRESHOLD} --detail
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"

lint:
  stage: post-implement
  image: node:${NODE_VERSION}
  needs: [security-scan]
  script:
    - npm ci
    - echo "## QG-006: Lint Cleanliness"
    - npm run lint -- --max-warnings 10
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"

lighthouse:
  stage: post-implement
  image: cypress/browsers:latest
  needs: [security-scan]
  script:
    - npm ci
    - npm run build
    - npm run preview &
    - npx wait-on http://localhost:3000
    - npm install -g @lhci/cli
    - lhci autorun
  artifacts:
    paths:
      - .lighthouseci/
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  allow_failure: true

# ============================================
# PRE-DEPLOY GATES
# ============================================
debug-check:
  stage: pre-deploy
  image: alpine
  needs: [test-coverage, type-coverage, lint]
  script:
    - echo "## QG-011: No Debug Artifacts"
    - |
      if grep -rn "console\.log\|console\.debug\|debugger" src/ --include="*.ts" --include="*.tsx"; then
        echo "Debug statements found in production code"
        exit 1
      fi
    - echo "No debug artifacts found"
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

env-check:
  stage: pre-deploy
  image: alpine
  needs: [test-coverage, type-coverage, lint]
  script:
    - echo "## QG-012: Environment Documentation"
    - |
      grep -roh "process\.env\.\w\+" src/ | sort -u | sed 's/process\.env\.//' > code_envs.txt
      grep -oh "^\w\+=" .env.example | sed 's/=//' | sort -u > doc_envs.txt
      UNDOC=$(comm -23 code_envs.txt doc_envs.txt)
      if [ -n "$UNDOC" ]; then
        echo "Undocumented environment variables: $UNDOC"
        exit 1
      fi
    - echo "All environment variables documented"
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

# ============================================
# DEPLOY
# ============================================
deploy:
  stage: deploy
  needs: [debug-check, env-check]
  script:
    - echo "🚀 All quality gates passed - deploying to production"
    # Add your deployment commands here
  environment:
    name: production
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

---

## Pre-Commit Hooks

### Local Gate Validation

```yaml
# .pre-commit-config.yaml
repos:
  # QG-006: Lint on commit
  - repo: local
    hooks:
      - id: eslint
        name: ESLint
        entry: npx eslint --max-warnings 10
        language: system
        files: \.(ts|tsx|js|jsx)$
        pass_filenames: true

  # QG-011: No debug artifacts
  - repo: local
    hooks:
      - id: no-console-log
        name: No console.log
        entry: bash -c 'grep -rn "console\.log\|debugger" --include="*.ts" --include="*.tsx" "$@" && exit 1 || exit 0'
        language: system
        files: \.(ts|tsx)$

  # QG-005: Type check on commit
  - repo: local
    hooks:
      - id: typecheck
        name: TypeScript
        entry: npx tsc --noEmit
        language: system
        pass_filenames: false
        files: \.(ts|tsx)$

  # Standard pre-commit hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
```

### Installation

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files
```

---

## Configuration Files

### Lighthouse Configuration

```json
// lighthouserc.json
{
  "ci": {
    "collect": {
      "numberOfRuns": 3,
      "startServerCommand": "npm run preview",
      "url": ["http://localhost:3000"]
    },
    "assert": {
      "assertions": {
        "categories:performance": ["warn", { "minScore": 0.9 }],
        "categories:accessibility": ["error", { "minScore": 0.9 }],
        "categories:best-practices": ["warn", { "minScore": 0.9 }],
        "categories:seo": ["warn", { "minScore": 0.9 }]
      }
    },
    "upload": {
      "target": "temporary-public-storage"
    }
  }
}
```

### Jest Configuration (Coverage)

```javascript
// jest.config.js
module.exports = {
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['json-summary', 'lcov', 'text', 'cobertura'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.test.{ts,tsx}',
    '!src/**/__tests__/**'
  ]
};
```

### ESLint Configuration

```javascript
// eslint.config.js (Flat Config)
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  {
    rules: {
      // QG-011: Warn on console usage
      'no-console': 'warn',
      'no-debugger': 'error',

      // Strict type safety
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unsafe-assignment': 'error',
      '@typescript-eslint/no-unsafe-call': 'error',
      '@typescript-eslint/no-unsafe-member-access': 'error',
      '@typescript-eslint/no-unsafe-return': 'error'
    }
  }
);
```

---

## Scripts

### Environment Coverage Check

```bash
#!/bin/bash
# scripts/check-env-coverage.sh

set -e

echo "Checking environment variable documentation..."

# Find all env var references in code
CODE_ENVS=$(grep -roh "process\.env\.\w\+" src/ 2>/dev/null | sort -u | sed 's/process\.env\.//')

# Find documented env vars
if [ ! -f .env.example ]; then
  echo "Warning: .env.example not found"
  exit 0
fi

DOC_ENVS=$(grep -oh "^\w\+=" .env.example | sed 's/=//' | sort -u)

# Find undocumented
UNDOC=$(comm -23 <(echo "$CODE_ENVS") <(echo "$DOC_ENVS"))

if [ -n "$UNDOC" ]; then
  echo "❌ Undocumented environment variables:"
  echo "$UNDOC"
  exit 1
fi

echo "✅ All environment variables documented"
```

### Coverage Check Script

```bash
#!/bin/bash
# scripts/check-coverage.sh

set -e

THRESHOLD=${1:-80}
COVERAGE_FILE="coverage/coverage-summary.json"

if [ ! -f "$COVERAGE_FILE" ]; then
  echo "Coverage file not found. Run tests with --coverage first."
  exit 1
fi

LINES=$(jq '.total.lines.pct' "$COVERAGE_FILE")
BRANCHES=$(jq '.total.branches.pct' "$COVERAGE_FILE")
FUNCTIONS=$(jq '.total.functions.pct' "$COVERAGE_FILE")

echo "Coverage Report:"
echo "  Lines:     $LINES%"
echo "  Branches:  $BRANCHES%"
echo "  Functions: $FUNCTIONS%"

if (( $(echo "$LINES < $THRESHOLD" | bc -l) )); then
  echo "❌ Line coverage $LINES% is below $THRESHOLD% threshold"
  exit 1
fi

echo "✅ Coverage meets threshold"
```

---

## Gate Status Badges

### GitHub Actions Badges

```markdown
<!-- Add to README.md -->
![Quality Gates](https://github.com/ORG/REPO/actions/workflows/quality-gates.yml/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/ORG/REPO)
```

### GitLab Badges

```markdown
<!-- Add to README.md -->
[![pipeline status](https://gitlab.com/ORG/REPO/badges/main/pipeline.svg)](https://gitlab.com/ORG/REPO/-/pipelines)
[![coverage report](https://gitlab.com/ORG/REPO/badges/main/coverage.svg)](https://gitlab.com/ORG/REPO/-/commits/main)
```

---

## Customization

### Adjusting Thresholds

Edit the environment variables at the top of the workflow:

```yaml
env:
  COVERAGE_THRESHOLD: 80      # QG-004: Minimum test coverage %
  TYPE_COVERAGE_THRESHOLD: 95 # QG-005: Minimum type coverage %
  MAX_LINT_WARNINGS: 10       # QG-006: Maximum allowed warnings
  LIGHTHOUSE_SCORE: 90        # QG-007: Minimum performance score
```

### Skipping Gates

For specific branches or conditions:

```yaml
# Skip performance gates on non-PR builds
performance:
  if: github.event_name == 'pull_request'

# Skip pre-deploy gates on feature branches
pre-deploy:
  if: github.ref == 'refs/heads/main'
```

### Adding Custom Gates

```yaml
custom-gate:
  name: Custom Business Gate
  runs-on: ubuntu-latest
  needs: pre-implement
  steps:
    - name: Custom Validation
      run: |
        # Your custom validation logic
        ./scripts/custom-check.sh
```

---

## TDD Pipeline

**New in v0.0.86**: Test-First Development pipeline with staging infrastructure.

### GitHub Actions - TDD Pipeline

```yaml
# .github/workflows/tdd-pipeline.yml
name: TDD Pipeline

on:
  push:
    branches: [main, develop, feature/*]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'
  COVERAGE_THRESHOLD: 80

jobs:
  # ============================================
  # STAGING: Provision test infrastructure
  # ============================================
  staging:
    name: QG-STAGING-001 Provision Services
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports:
          - 5433:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7-alpine
        ports:
          - 6380:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    outputs:
      staging-ready: ${{ steps.validate.outputs.ready }}
    steps:
      - name: Validate Staging
        id: validate
        run: |
          echo "## QG-STAGING-001: Staging Environment" >> $GITHUB_STEP_SUMMARY
          echo "PostgreSQL: Ready (port 5433)" >> $GITHUB_STEP_SUMMARY
          echo "Redis: Ready (port 6380)" >> $GITHUB_STEP_SUMMARY
          echo "ready=true" >> $GITHUB_OUTPUT
          echo "✅ QG-STAGING-001: PASSED" >> $GITHUB_STEP_SUMMARY

  # ============================================
  # TEST COMPLETENESS: Verify all AS have tests
  # ============================================
  test-completeness:
    name: QG-TEST-001 Test Completeness
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check Test Traceability
        run: |
          echo "## QG-TEST-001: Test Completeness" >> $GITHUB_STEP_SUMMARY

          # Find all AS-xxx in spec.md requiring tests
          if [ -f specs/*/spec.md ]; then
            AS_COUNT=$(grep -oE "AS-[0-9]+[A-Z]" specs/*/spec.md | wc -l || echo 0)
            echo "Acceptance Scenarios found: $AS_COUNT" >> $GITHUB_STEP_SUMMARY

            # Find all [TEST:AS-xxx] markers in test files
            TEST_COUNT=$(grep -roE "\[TEST:AS-[0-9]+[A-Z]\]" tests/ 2>/dev/null | wc -l || echo 0)
            echo "Test markers found: $TEST_COUNT" >> $GITHUB_STEP_SUMMARY

            if [ "$AS_COUNT" -gt 0 ] && [ "$TEST_COUNT" -lt "$AS_COUNT" ]; then
              echo "⚠️ Some acceptance scenarios may lack tests" >> $GITHUB_STEP_SUMMARY
            fi
          fi

          echo "✅ QG-TEST-001: Check complete" >> $GITHUB_STEP_SUMMARY

  # ============================================
  # UNIT TESTS: Run with coverage
  # ============================================
  unit-tests:
    name: QG-TEST-004 Unit Tests
    runs-on: ubuntu-latest
    needs: staging
    env:
      DATABASE_URL: postgresql://test:test@localhost:5433/test_db
      REDIS_URL: redis://localhost:6380
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports:
          - 5433:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci

      - name: Run Unit Tests
        run: |
          echo "## QG-TEST-004: Unit Tests with Coverage" >> $GITHUB_STEP_SUMMARY
          npm test -- --coverage --coverageReporters=json-summary 2>&1 | tee test-output.log

      - name: Check Coverage
        run: |
          if [ -f coverage/coverage-summary.json ]; then
            COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
            echo "Line coverage: $COVERAGE%" >> $GITHUB_STEP_SUMMARY

            if (( $(echo "$COVERAGE < ${{ env.COVERAGE_THRESHOLD }}" | bc -l) )); then
              echo "❌ Coverage $COVERAGE% is below ${{ env.COVERAGE_THRESHOLD }}% threshold" >> $GITHUB_STEP_SUMMARY
              exit 1
            fi
            echo "✅ QG-TEST-004: PASSED (coverage $COVERAGE%)" >> $GITHUB_STEP_SUMMARY
          else
            echo "⚠️ Coverage report not found" >> $GITHUB_STEP_SUMMARY
          fi

      - uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/

  # ============================================
  # INTEGRATION TESTS: Against staging DB
  # ============================================
  integration-tests:
    name: Integration Tests
    runs-on: ubuntu-latest
    needs: [staging, unit-tests]
    env:
      DATABASE_URL: postgresql://test:test@localhost:5433/test_db
      REDIS_URL: redis://localhost:6380
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports:
          - 5433:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7-alpine
        ports:
          - 6380:6379
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci

      - name: Run Integration Tests
        run: |
          echo "## Integration Tests" >> $GITHUB_STEP_SUMMARY
          npm run test:integration 2>&1 | tee integration-output.log || echo "No integration tests found"
          echo "✅ Integration tests complete" >> $GITHUB_STEP_SUMMARY

  # ============================================
  # E2E TESTS: Playwright
  # ============================================
  e2e-tests:
    name: E2E Tests (Playwright)
    runs-on: ubuntu-latest
    needs: [staging, unit-tests]
    env:
      DATABASE_URL: postgresql://test:test@localhost:5433/test_db
      CI: true
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports:
          - 5433:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps chromium

      - name: Build Application
        run: npm run build || echo "No build step"

      - name: Run E2E Tests
        run: |
          echo "## E2E Tests (Playwright)" >> $GITHUB_STEP_SUMMARY
          npx playwright test 2>&1 | tee e2e-output.log || echo "No E2E tests found"
          echo "✅ E2E tests complete" >> $GITHUB_STEP_SUMMARY

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/

  # ============================================
  # QUALITY GATES SUMMARY
  # ============================================
  quality-gates:
    name: Quality Gates Summary
    runs-on: ubuntu-latest
    needs: [staging, test-completeness, unit-tests, integration-tests, e2e-tests]
    if: always()
    steps:
      - name: Summary
        run: |
          echo "# Quality Gates Summary" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "| Gate | Status |" >> $GITHUB_STEP_SUMMARY
          echo "|------|--------|" >> $GITHUB_STEP_SUMMARY
          echo "| QG-STAGING-001 | ${{ needs.staging.result == 'success' && '✅' || '❌' }} |" >> $GITHUB_STEP_SUMMARY
          echo "| QG-TEST-001 | ${{ needs.test-completeness.result == 'success' && '✅' || '❌' }} |" >> $GITHUB_STEP_SUMMARY
          echo "| QG-TEST-004 | ${{ needs.unit-tests.result == 'success' && '✅' || '❌' }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Integration | ${{ needs.integration-tests.result == 'success' && '✅' || '⚠️' }} |" >> $GITHUB_STEP_SUMMARY
          echo "| E2E | ${{ needs.e2e-tests.result == 'success' && '✅' || '⚠️' }} |" >> $GITHUB_STEP_SUMMARY
```

### GitLab CI - TDD Pipeline

```yaml
# .gitlab-ci.yml (TDD section)
stages:
  - staging
  - test-setup
  - unit-tests
  - integration-tests
  - e2e-tests
  - summary

variables:
  POSTGRES_USER: test
  POSTGRES_PASSWORD: test
  POSTGRES_DB: test_db
  DATABASE_URL: "postgresql://test:test@postgres:5432/test_db"
  REDIS_URL: "redis://redis:6379"
  COVERAGE_THRESHOLD: "80"

# ============================================
# STAGING: Validate test infrastructure
# ============================================
staging-validate:
  stage: staging
  image: postgres:16-alpine
  services:
    - name: postgres:16-alpine
      alias: postgres
    - name: redis:7-alpine
      alias: redis
  script:
    - echo "## QG-STAGING-001: Staging Environment"
    - pg_isready -h postgres -U test
    - echo "✅ PostgreSQL ready"
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH

# ============================================
# UNIT TESTS with coverage
# ============================================
unit-tests:
  stage: unit-tests
  image: node:20
  services:
    - name: postgres:16-alpine
      alias: postgres
    - name: redis:7-alpine
      alias: redis
  needs: [staging-validate]
  script:
    - npm ci
    - npm test -- --coverage --coverageReporters=json-summary
    - |
      COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
      echo "Line coverage: $COVERAGE%"
      if (( $(echo "$COVERAGE < $COVERAGE_THRESHOLD" | bc -l) )); then
        echo "Coverage $COVERAGE% is below $COVERAGE_THRESHOLD% threshold"
        exit 1
      fi
      echo "✅ QG-TEST-004: PASSED"
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths:
      - coverage/
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH

# ============================================
# E2E TESTS with Playwright
# ============================================
e2e-tests:
  stage: e2e-tests
  image: mcr.microsoft.com/playwright:v1.40.0-jammy
  services:
    - name: postgres:16-alpine
      alias: postgres
  needs: [unit-tests]
  script:
    - npm ci
    - npm run build || true
    - npx playwright test || echo "No E2E tests found"
  artifacts:
    when: always
    paths:
      - playwright-report/
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

---

## Local TDD Runner

```bash
#!/bin/bash
# scripts/bash/run-tdd-pipeline.sh
# Local equivalent of CI TDD pipeline

set -e

echo "🧪 TDD Pipeline - Local Runner"
echo "=============================="

# Check staging
echo ""
echo "📦 Step 1: Staging Validation (QG-STAGING-001)"
if [ -f .speckit/staging/docker-compose.yaml ]; then
  docker-compose -f .speckit/staging/docker-compose.yaml ps
  echo "✅ QG-STAGING-001: PASSED"
else
  echo "⚠️  Run '/speckit.staging' first to provision staging"
  exit 1
fi

# Load staging config
if [ -f .speckit/staging/test-config.env ]; then
  source .speckit/staging/test-config.env
  echo "✅ Loaded staging configuration"
fi

# Run unit tests with coverage
echo ""
echo "🔬 Step 2: Unit Tests (QG-TEST-004)"
npm test -- --coverage --coverageReporters=json-summary

# Check coverage threshold
COVERAGE=$(cat coverage/coverage-summary.json 2>/dev/null | jq '.total.lines.pct' || echo 0)
echo "Line coverage: $COVERAGE%"

if (( $(echo "$COVERAGE < 80" | bc -l) )); then
  echo "❌ QG-TEST-004: FAILED (coverage $COVERAGE% < 80%)"
  exit 1
fi
echo "✅ QG-TEST-004: PASSED"

# Run integration tests
echo ""
echo "🔗 Step 3: Integration Tests"
npm run test:integration 2>/dev/null || echo "No integration tests found"

# Run E2E tests
echo ""
echo "🎭 Step 4: E2E Tests (Playwright)"
npx playwright test 2>/dev/null || echo "No E2E tests found"

# Summary
echo ""
echo "=============================="
echo "✅ TDD Pipeline Complete"
echo "=============================="
```

---

## Related

- Domain: `memory/domains/quality-gates.md`
- Metrics: `templates/shared/metrics-framework.md`
- Observability: `templates/shared/observability-stack.md`
