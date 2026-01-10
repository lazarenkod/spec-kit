#!/usr/bin/env bash
# verify-prerequisites.sh - Check prerequisites for /speckit.verify command
#
# Checks:
# 1. Implementation complete (all tasks done)
# 2. Staging environment available (Docker or remote URL)
# 3. Test framework ready (test command runs)
#
# Exit codes:
# 0 - All prerequisites met
# 1 - One or more prerequisites failed

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASS_COUNT=0
FAIL_COUNT=0

# Helper functions
pass() {
  echo -e "${GREEN}✅ PASS${NC}: $1"
  ((PASS_COUNT++))
}

fail() {
  echo -e "${RED}❌ FAIL${NC}: $1"
  ((FAIL_COUNT++))
}

warn() {
  echo -e "${YELLOW}⚠️  WARN${NC}: $1"
}

info() {
  echo "ℹ️  $1"
}

# ============================================================================
# CHECK 1: Implementation Complete (tasks.md)
# ============================================================================
check_implementation_complete() {
  info "Checking if implementation is complete..."

  # Find tasks.md in specs/ directory
  TASKS_FILE=$(find specs -name "tasks.md" -type f 2>/dev/null | head -n 1)

  if [ -z "$TASKS_FILE" ]; then
    fail "tasks.md not found in specs/ directory"
    echo "   Run /speckit.implement first"
    return 1
  fi

  # Count tasks by status
  TOTAL_TASKS=$(grep -c "^- \[.\] T[0-9]" "$TASKS_FILE" 2>/dev/null || echo "0")
  COMPLETED_TASKS=$(grep -c "^- \[x\] T[0-9]" "$TASKS_FILE" 2>/dev/null || echo "0")
  SKIPPED_TASKS=$(grep -c "^- \[~\] T[0-9]" "$TASKS_FILE" 2>/dev/null || echo "0")
  IN_PROGRESS_TASKS=$(grep -c "^- \[>\] T[0-9]" "$TASKS_FILE" 2>/dev/null || echo "0")
  PENDING_TASKS=$(grep -c "^- \[ \] T[0-9]" "$TASKS_FILE" 2>/dev/null || echo "0")

  DONE_TASKS=$((COMPLETED_TASKS + SKIPPED_TASKS))

  if [ "$TOTAL_TASKS" -eq 0 ]; then
    fail "No tasks found in $TASKS_FILE"
    return 1
  fi

  if [ "$IN_PROGRESS_TASKS" -gt 0 ]; then
    fail "Implementation not complete: $IN_PROGRESS_TASKS tasks in progress"
    echo "   Complete all tasks before verification"
    return 1
  fi

  if [ "$PENDING_TASKS" -gt 0 ]; then
    fail "Implementation not complete: $PENDING_TASKS tasks pending"
    echo "   Complete all tasks before verification"
    return 1
  fi

  pass "Implementation complete ($DONE_TASKS/$TOTAL_TASKS tasks done)"
  return 0
}

# ============================================================================
# CHECK 2: Staging Environment Available
# ============================================================================
check_staging_available() {
  info "Checking if staging environment is available..."

  # Check for remote staging URL in environment
  if [ -n "${STAGING_URL:-}" ]; then
    # Test remote staging URL
    if command -v curl >/dev/null 2>&1; then
      if curl -f -s -o /dev/null -w "%{http_code}" "$STAGING_URL" >/dev/null 2>&1; then
        pass "Remote staging URL accessible: $STAGING_URL"
        return 0
      else
        warn "Remote staging URL not accessible: $STAGING_URL"
      fi
    fi
  fi

  # Check for Docker Compose staging
  if [ -f ".speckit/staging/docker-compose.yaml" ] || [ -f ".speckit/staging/docker-compose.yml" ]; then
    COMPOSE_FILE=$([ -f ".speckit/staging/docker-compose.yaml" ] && echo ".speckit/staging/docker-compose.yaml" || echo ".speckit/staging/docker-compose.yml")

    if ! command -v docker >/dev/null 2>&1; then
      fail "Docker not found (required for local staging)"
      echo "   Install Docker or set STAGING_URL environment variable"
      return 1
    fi

    if ! command -v docker-compose >/dev/null 2>&1 && ! docker compose version >/dev/null 2>&1; then
      fail "docker-compose not found"
      echo "   Install docker-compose or set STAGING_URL environment variable"
      return 1
    fi

    # Check if services are running
    COMPOSE_CMD=$(command -v docker-compose >/dev/null 2>&1 && echo "docker-compose" || echo "docker compose")
    RUNNING_SERVICES=$($COMPOSE_CMD -f "$COMPOSE_FILE" ps --services --filter "status=running" 2>/dev/null | wc -l)

    if [ "$RUNNING_SERVICES" -eq 0 ]; then
      fail "Staging services not running"
      echo "   Run: /speckit.staging or manually start services"
      return 1
    fi

    # Check health of key services
    UNHEALTHY=0

    # Check postgres (test-db)
    if $COMPOSE_CMD -f "$COMPOSE_FILE" ps test-db 2>/dev/null | grep -q "running"; then
      if ! docker exec $(docker ps -q -f "name=test-db") pg_isready >/dev/null 2>&1; then
        warn "PostgreSQL (test-db) not ready"
        ((UNHEALTHY++))
      fi
    fi

    # Check redis (test-redis)
    if $COMPOSE_CMD -f "$COMPOSE_FILE" ps test-redis 2>/dev/null | grep -q "running"; then
      if ! docker exec $(docker ps -q -f "name=test-redis") redis-cli ping >/dev/null 2>&1; then
        warn "Redis (test-redis) not ready"
        ((UNHEALTHY++))
      fi
    fi

    if [ "$UNHEALTHY" -gt 0 ]; then
      fail "Staging services unhealthy ($UNHEALTHY services)"
      echo "   Wait for services to become healthy or restart them"
      return 1
    fi

    pass "Local staging available ($RUNNING_SERVICES services healthy)"
    return 0
  fi

  # Check for localhost application
  if command -v curl >/dev/null 2>&1; then
    for PORT in 3000 8000 8080 5000; do
      if curl -f -s -o /dev/null "http://localhost:$PORT" 2>/dev/null; then
        pass "Application running on localhost:$PORT"
        return 0
      fi
    done
  fi

  fail "No staging environment found"
  echo "   Options:"
  echo "   1. Run /speckit.staging to provision Docker staging"
  echo "   2. Start your application locally"
  echo "   3. Set STAGING_URL environment variable to remote staging"
  return 1
}

# ============================================================================
# CHECK 3: Test Framework Ready
# ============================================================================
check_test_framework_ready() {
  info "Checking if test framework is ready..."

  # Detect test framework from common files
  TEST_CMD=""
  FRAMEWORK=""

  # Node.js / TypeScript
  if [ -f "package.json" ]; then
    if grep -q "\"jest\"" package.json 2>/dev/null; then
      TEST_CMD="npm test -- --passWithNoTests"
      FRAMEWORK="Jest"
    elif grep -q "\"vitest\"" package.json 2>/dev/null; then
      TEST_CMD="npm test"
      FRAMEWORK="Vitest"
    elif grep -q "\"mocha\"" package.json 2>/dev/null; then
      TEST_CMD="npm test"
      FRAMEWORK="Mocha"
    else
      # Check for test script
      if grep -q "\"test\":" package.json 2>/dev/null; then
        TEST_CMD="npm test"
        FRAMEWORK="npm test"
      fi
    fi
  fi

  # Python
  if [ -f "pyproject.toml" ] || [ -f "pytest.ini" ] || [ -f "setup.py" ]; then
    if command -v pytest >/dev/null 2>&1; then
      TEST_CMD="pytest --collect-only"
      FRAMEWORK="pytest"
    elif [ -f "pyproject.toml" ] && grep -q "pytest" pyproject.toml 2>/dev/null; then
      TEST_CMD="python -m pytest --collect-only"
      FRAMEWORK="pytest"
    fi
  fi

  # Go
  if [ -f "go.mod" ]; then
    TEST_CMD="go test ./... -count=0"
    FRAMEWORK="go test"
  fi

  # Rust
  if [ -f "Cargo.toml" ]; then
    TEST_CMD="cargo test --no-run"
    FRAMEWORK="cargo test"
  fi

  if [ -z "$TEST_CMD" ]; then
    fail "Test framework not detected"
    echo "   Install a test framework (Jest, pytest, etc.)"
    echo "   See: memory/domains/test-framework-registry.md"
    return 1
  fi

  # Run test command to verify it works
  info "Testing framework: $FRAMEWORK"
  if eval "$TEST_CMD" >/dev/null 2>&1; then
    pass "Test framework ready ($FRAMEWORK)"
    return 0
  else
    fail "Test command failed: $TEST_CMD"
    echo "   Fix test framework configuration"
    return 1
  fi
}

# ============================================================================
# MAIN
# ============================================================================
main() {
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Verification Prerequisites Check"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo

  # Run all checks
  check_implementation_complete || true
  echo
  check_staging_available || true
  echo
  check_test_framework_ready || true

  echo
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Summary: $PASS_COUNT passed, $FAIL_COUNT failed"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  if [ "$FAIL_COUNT" -gt 0 ]; then
    echo
    echo -e "${RED}Prerequisites not met. Cannot run verification.${NC}"
    exit 1
  else
    echo
    echo -e "${GREEN}All prerequisites met. Ready for verification.${NC}"
    exit 0
  fi
}

main "$@"
