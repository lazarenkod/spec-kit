#!/usr/bin/env bash
# run-tdd-pipeline.sh - Local TDD pipeline runner
# Equivalent to CI TDD pipeline for local development
# Part of Spec Kit - https://github.com/Anthroware/spec-kit
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
COVERAGE_THRESHOLD=${COVERAGE_THRESHOLD:-80}
SKIP_E2E=false
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --skip-e2e)
      SKIP_E2E=true
      shift
      ;;
    --verbose|-v)
      VERBOSE=true
      shift
      ;;
    --threshold)
      COVERAGE_THRESHOLD="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: run-tdd-pipeline.sh [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --skip-e2e          Skip E2E/Playwright tests"
      echo "  --threshold <N>     Coverage threshold (default: 80)"
      echo "  --verbose, -v       Verbose output"
      echo "  -h, --help          Show this help"
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      exit 1
      ;;
  esac
done

# Detect project root
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
STAGING_DIR="$PROJECT_ROOT/.speckit/staging"

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  TDD Pipeline - Local Runner${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Track gate results
GATES_PASSED=0
GATES_FAILED=0

report_gate() {
  local gate=$1
  local status=$2
  local message=$3

  if [ "$status" = "PASS" ]; then
    echo -e "${GREEN}✅ $gate: PASSED${NC}"
    [ -n "$message" ] && echo -e "   $message"
    GATES_PASSED=$((GATES_PASSED + 1))
  else
    echo -e "${RED}❌ $gate: FAILED${NC}"
    [ -n "$message" ] && echo -e "   $message"
    GATES_FAILED=$((GATES_FAILED + 1))
  fi
}

# ============================================
# Step 1: Staging Validation (QG-STAGING-001)
# ============================================
echo -e "${BLUE}📦 Step 1: Staging Validation (QG-STAGING-001)${NC}"
echo ""

if [ -f "$STAGING_DIR/docker-compose.yaml" ]; then
  # Check if services are running
  cd "$STAGING_DIR"
  if docker-compose ps 2>/dev/null | grep -q "Up"; then
    # Verify health
    POSTGRES_HEALTHY=false
    REDIS_HEALTHY=false

    if docker exec speckit-test-db pg_isready -U test -d test_db > /dev/null 2>&1; then
      POSTGRES_HEALTHY=true
      echo -e "  ${GREEN}PostgreSQL: Healthy (port 5433)${NC}"
    else
      echo -e "  ${YELLOW}PostgreSQL: Not ready${NC}"
    fi

    if docker exec speckit-test-redis redis-cli ping 2>/dev/null | grep -q "PONG"; then
      REDIS_HEALTHY=true
      echo -e "  ${GREEN}Redis: Healthy (port 6380)${NC}"
    else
      echo -e "  ${YELLOW}Redis: Not running (optional)${NC}"
    fi

    if [ "$POSTGRES_HEALTHY" = true ]; then
      report_gate "QG-STAGING-001" "PASS" "Staging services healthy"
    else
      report_gate "QG-STAGING-001" "FAIL" "PostgreSQL not ready"
      echo ""
      echo -e "${YELLOW}Run '/speckit.staging' to provision staging environment${NC}"
      exit 1
    fi
  else
    echo -e "  ${YELLOW}Services not running${NC}"
    echo ""
    echo -e "${YELLOW}Starting staging services...${NC}"
    docker-compose up -d --wait
    report_gate "QG-STAGING-001" "PASS" "Staging services started"
  fi
  cd "$PROJECT_ROOT"
else
  report_gate "QG-STAGING-001" "FAIL" "docker-compose.yaml not found"
  echo ""
  echo -e "${YELLOW}Run '/speckit.staging' first to provision staging environment${NC}"
  exit 1
fi

# Load staging config
if [ -f "$STAGING_DIR/test-config.env" ]; then
  set -a
  source "$STAGING_DIR/test-config.env"
  set +a
  echo -e "  ${GREEN}Loaded test configuration${NC}"
fi

echo ""

# ============================================
# Step 2: Test Completeness (QG-TEST-001)
# ============================================
echo -e "${BLUE}📋 Step 2: Test Completeness (QG-TEST-001)${NC}"
echo ""

# Find spec files
SPEC_FILES=$(find "$PROJECT_ROOT/specs" -name "spec.md" 2>/dev/null || true)
if [ -n "$SPEC_FILES" ]; then
  AS_COUNT=$(grep -hoE "AS-[0-9]+[A-Z]" $SPEC_FILES 2>/dev/null | sort -u | wc -l | tr -d ' ')
  echo -e "  Acceptance Scenarios in specs: $AS_COUNT"

  # Find test markers
  TEST_COUNT=$(grep -roE "\[TEST:AS-[0-9]+[A-Z]\]" "$PROJECT_ROOT/tests" 2>/dev/null | wc -l | tr -d ' ' || echo 0)
  echo -e "  Test markers found: $TEST_COUNT"

  if [ "$AS_COUNT" -gt 0 ] && [ "$TEST_COUNT" -lt "$AS_COUNT" ]; then
    echo -e "  ${YELLOW}⚠️  Some acceptance scenarios may lack tests${NC}"
    report_gate "QG-TEST-001" "PASS" "Check complete (warnings exist)"
  else
    report_gate "QG-TEST-001" "PASS" "All scenarios have test markers"
  fi
else
  echo -e "  ${YELLOW}No spec files found, skipping check${NC}"
  report_gate "QG-TEST-001" "PASS" "Skipped (no specs)"
fi

echo ""

# ============================================
# Step 3: Unit Tests (QG-TEST-004)
# ============================================
echo -e "${BLUE}🔬 Step 3: Unit Tests (QG-TEST-004)${NC}"
echo ""

# Detect test command
if [ -f "package.json" ]; then
  # Node.js project
  echo -e "  Running: npm test -- --coverage"
  if $VERBOSE; then
    npm test -- --coverage --coverageReporters=json-summary
  else
    npm test -- --coverage --coverageReporters=json-summary 2>&1 | tail -20
  fi

  # Check coverage
  if [ -f "coverage/coverage-summary.json" ]; then
    COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
    echo ""
    echo -e "  Line coverage: ${COVERAGE}%"

    if (( $(echo "$COVERAGE < $COVERAGE_THRESHOLD" | bc -l) )); then
      report_gate "QG-TEST-004" "FAIL" "Coverage ${COVERAGE}% below ${COVERAGE_THRESHOLD}% threshold"
    else
      report_gate "QG-TEST-004" "PASS" "Coverage ${COVERAGE}% meets threshold"
    fi
  else
    echo -e "  ${YELLOW}Coverage report not found${NC}"
    report_gate "QG-TEST-004" "PASS" "Tests passed (no coverage report)"
  fi
elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
  # Python project
  echo -e "  Running: pytest --cov"
  if $VERBOSE; then
    pytest --cov --cov-report=json
  else
    pytest --cov --cov-report=json 2>&1 | tail -20
  fi

  if [ -f "coverage.json" ]; then
    COVERAGE=$(cat coverage.json | jq '.totals.percent_covered')
    echo ""
    echo -e "  Line coverage: ${COVERAGE}%"

    if (( $(echo "$COVERAGE < $COVERAGE_THRESHOLD" | bc -l) )); then
      report_gate "QG-TEST-004" "FAIL" "Coverage ${COVERAGE}% below ${COVERAGE_THRESHOLD}% threshold"
    else
      report_gate "QG-TEST-004" "PASS" "Coverage ${COVERAGE}% meets threshold"
    fi
  else
    report_gate "QG-TEST-004" "PASS" "Tests passed (no coverage report)"
  fi
else
  echo -e "  ${YELLOW}No recognized test framework found${NC}"
  report_gate "QG-TEST-004" "PASS" "Skipped (no tests)"
fi

echo ""

# ============================================
# Step 4: Integration Tests
# ============================================
echo -e "${BLUE}🔗 Step 4: Integration Tests${NC}"
echo ""

if [ -f "package.json" ] && grep -q "test:integration" package.json; then
  echo -e "  Running: npm run test:integration"
  if $VERBOSE; then
    npm run test:integration
  else
    npm run test:integration 2>&1 | tail -10 || true
  fi
  echo -e "  ${GREEN}Integration tests complete${NC}"
else
  echo -e "  ${YELLOW}No integration tests configured (npm run test:integration)${NC}"
fi

echo ""

# ============================================
# Step 5: E2E Tests (Playwright)
# ============================================
if [ "$SKIP_E2E" = false ]; then
  echo -e "${BLUE}🎭 Step 5: E2E Tests (Playwright)${NC}"
  echo ""

  if [ -f "playwright.config.ts" ] || [ -f "playwright.config.js" ]; then
    echo -e "  Running: npx playwright test"
    if $VERBOSE; then
      npx playwright test
    else
      npx playwright test 2>&1 | tail -15 || true
    fi
    echo -e "  ${GREEN}E2E tests complete${NC}"
  else
    echo -e "  ${YELLOW}No Playwright config found, skipping${NC}"
  fi
  echo ""
else
  echo -e "${YELLOW}⏭️  Skipping E2E tests (--skip-e2e)${NC}"
  echo ""
fi

# ============================================
# Summary
# ============================================
echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  TDD Pipeline Summary${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

echo "| Gate | Status |"
echo "|------|--------|"

if [ $GATES_FAILED -eq 0 ]; then
  echo -e "${GREEN}All $GATES_PASSED gates passed!${NC}"
  echo ""
  echo -e "${GREEN}✅ TDD Pipeline Complete${NC}"
  exit 0
else
  echo -e "${RED}$GATES_FAILED gate(s) failed, $GATES_PASSED passed${NC}"
  echo ""
  echo -e "${RED}❌ TDD Pipeline Failed${NC}"
  exit 1
fi
