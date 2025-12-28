#!/usr/bin/env bash
# Verify deployed application
# Called by ship.sh for --only verify or full cycle
# Runs smoke tests, acceptance tests, and generates verify-results.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# =============================================================================
# CONFIGURATION
# =============================================================================

ENV=""
BASE_URL=""
CONFIG=""
STATE_DIR=""
FEATURE_DIR=""
VERBOSE=false

# Test results
declare -a SMOKE_RESULTS=()
declare -a ACCEPTANCE_RESULTS=()
SMOKE_PASSED=0
SMOKE_FAILED=0
ACCEPTANCE_PASSED=0
ACCEPTANCE_FAILED=0
ACCEPTANCE_SKIPPED=0

# =============================================================================
# ARGUMENT PARSING
# =============================================================================

while [[ $# -gt 0 ]]; do
    case $1 in
        --env)
            ENV="$2"
            shift 2
            ;;
        --base-url)
            BASE_URL="$2"
            shift 2
            ;;
        --config)
            CONFIG="$2"
            shift 2
            ;;
        --state-dir)
            STATE_DIR="$2"
            shift 2
            ;;
        --feature-dir)
            FEATURE_DIR="$2"
            shift 2
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

log() {
    echo "[verify] $1"
}

log_verbose() {
    [[ "$VERBOSE" == "true" ]] && echo "[verify:verbose] $1"
}

log_test() {
    local status="$1"
    local name="$2"
    local duration="$3"
    local error="${4:-}"

    if [[ "$status" == "PASS" ]]; then
        echo "  ✓ $name (${duration}ms)"
    else
        echo "  ✗ $name (${duration}ms)"
        [[ -n "$error" ]] && echo "    Error: $error"
    fi
}

# HTTP request with timeout and response capture
http_request() {
    local method="$1"
    local url="$2"
    local expected_status="${3:-200}"
    local timeout="${4:-10}"

    local start_time=$(date +%s%3N 2>/dev/null || echo "0")
    local response
    local http_code

    # Make request
    response=$(curl -s -w "\n%{http_code}" \
        -X "$method" \
        --max-time "$timeout" \
        --connect-timeout 5 \
        "$url" 2>&1) || true

    local end_time=$(date +%s%3N 2>/dev/null || echo "0")
    local duration=$((end_time - start_time))

    # Extract status code (last line)
    http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')

    # Check status
    if [[ "$http_code" == "$expected_status" ]]; then
        echo "PASS|$duration|$body"
    else
        echo "FAIL|$duration|Expected $expected_status, got $http_code"
    fi
}

# =============================================================================
# SMOKE TESTS
# =============================================================================

run_smoke_tests() {
    log "Running smoke tests..."

    local results_count=0

    # Test 1: Health endpoint
    log_verbose "Testing health endpoint..."
    local result=$(http_request "GET" "$BASE_URL/health" "200" "10")
    local status=$(echo "$result" | cut -d'|' -f1)
    local duration=$(echo "$result" | cut -d'|' -f2)
    local detail=$(echo "$result" | cut -d'|' -f3-)

    SMOKE_RESULTS+=("health|$status|$duration|$detail")
    log_test "$status" "Health check" "$duration" "$([ "$status" == "FAIL" ] && echo "$detail")"

    if [[ "$status" == "PASS" ]]; then
        ((SMOKE_PASSED++))
    else
        ((SMOKE_FAILED++))
    fi

    # Test 2: Readiness endpoint
    log_verbose "Testing readiness endpoint..."
    result=$(http_request "GET" "$BASE_URL/ready" "200" "10")
    status=$(echo "$result" | cut -d'|' -f1)
    duration=$(echo "$result" | cut -d'|' -f2)
    detail=$(echo "$result" | cut -d'|' -f3-)

    SMOKE_RESULTS+=("readiness|$status|$duration|$detail")
    log_test "$status" "Readiness check" "$duration" "$([ "$status" == "FAIL" ] && echo "$detail")"

    if [[ "$status" == "PASS" ]]; then
        ((SMOKE_PASSED++))
    else
        ((SMOKE_FAILED++))
    fi

    # Test 3: API base path
    log_verbose "Testing API base path..."
    result=$(http_request "GET" "$BASE_URL/api" "200" "10")
    # Also accept 404 for /api if it redirects to /api/v1
    local api_status=$(echo "$result" | cut -d'|' -f1)
    if [[ "$api_status" == "FAIL" ]]; then
        # Try /api/v1
        result=$(http_request "GET" "$BASE_URL/api/v1" "200" "10")
    fi
    status=$(echo "$result" | cut -d'|' -f1)
    duration=$(echo "$result" | cut -d'|' -f2)
    detail=$(echo "$result" | cut -d'|' -f3-)

    SMOKE_RESULTS+=("api-base|$status|$duration|$detail")
    log_test "$status" "API base path" "$duration" "$([ "$status" == "FAIL" ] && echo "$detail")"

    if [[ "$status" == "PASS" ]]; then
        ((SMOKE_PASSED++))
    else
        ((SMOKE_FAILED++))
    fi

    log "Smoke tests: $SMOKE_PASSED passed, $SMOKE_FAILED failed"
}

# =============================================================================
# ACCEPTANCE TESTS
# =============================================================================

run_acceptance_tests() {
    log "Running acceptance tests..."

    local repo_root=$(get_repo_root)
    local spec_file=""

    # Find spec.md
    if [[ -n "$FEATURE_DIR" && -f "$FEATURE_DIR/spec.md" ]]; then
        spec_file="$FEATURE_DIR/spec.md"
    fi

    # Check for verify.yaml configuration
    if [[ -n "$CONFIG" && -f "$CONFIG" ]]; then
        log_verbose "Using verify.yaml configuration: $CONFIG"
        run_acceptance_from_config "$CONFIG"
        return
    fi

    # Fallback: Look for test files
    local test_dirs=(
        "$repo_root/tests/e2e"
        "$repo_root/tests/integration"
        "$repo_root/test/e2e"
        "$repo_root/e2e"
    )

    local found_tests=false

    for test_dir in "${test_dirs[@]}"; do
        if [[ -d "$test_dir" ]]; then
            log_verbose "Found test directory: $test_dir"
            found_tests=true
            run_tests_in_directory "$test_dir"
        fi
    done

    if [[ "$found_tests" == "false" ]]; then
        log "No acceptance test directories found, skipping"
        return 0
    fi

    log "Acceptance tests: $ACCEPTANCE_PASSED passed, $ACCEPTANCE_FAILED failed, $ACCEPTANCE_SKIPPED skipped"
}

run_acceptance_from_config() {
    local config_file="$1"

    # Parse verify.yaml for acceptance tests
    # Using basic YAML parsing with grep/sed (yq not required)
    local in_acceptance=false
    local current_test=""
    local current_ref=""
    local current_type=""
    local current_script=""

    while IFS= read -r line; do
        # Detect acceptance section
        if [[ "$line" =~ ^[[:space:]]*acceptance: ]]; then
            in_acceptance=true
            continue
        fi

        # Exit acceptance section on new top-level section
        if [[ "$in_acceptance" == "true" && "$line" =~ ^[[:space:]]{0,2}[a-z]+: && ! "$line" =~ ^[[:space:]]{4,} ]]; then
            in_acceptance=false
            continue
        fi

        if [[ "$in_acceptance" != "true" ]]; then
            continue
        fi

        # Parse test entries
        if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*name:[[:space:]]*(.+) ]]; then
            # Execute previous test if exists
            if [[ -n "$current_test" ]]; then
                execute_acceptance_test "$current_test" "$current_ref" "$current_type" "$current_script"
            fi
            current_test="${BASH_REMATCH[1]}"
            current_ref=""
            current_type=""
            current_script=""
        elif [[ "$line" =~ ^[[:space:]]*ref:[[:space:]]*(.+) ]]; then
            current_ref="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ ^[[:space:]]*type:[[:space:]]*(.+) ]]; then
            current_type="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ ^[[:space:]]*script:[[:space:]]*(.+) ]]; then
            current_script="${BASH_REMATCH[1]}"
        fi
    done < "$config_file"

    # Execute last test
    if [[ -n "$current_test" ]]; then
        execute_acceptance_test "$current_test" "$current_ref" "$current_type" "$current_script"
    fi
}

execute_acceptance_test() {
    local name="$1"
    local ref="$2"
    local type="$3"
    local script="$4"

    local repo_root=$(get_repo_root)
    local start_time=$(date +%s%3N 2>/dev/null || echo "0")
    local status="SKIP"
    local error=""

    case "$type" in
        api)
            # API tests - look for test file
            if [[ -n "$script" && -f "$repo_root/$script" ]]; then
                if run_api_test "$repo_root/$script"; then
                    status="PASS"
                else
                    status="FAIL"
                    error="Test execution failed"
                fi
            else
                error="Script not found: $script"
            fi
            ;;
        playwright)
            # Playwright E2E tests
            if [[ -n "$script" && -f "$repo_root/$script" ]]; then
                if run_playwright_test "$repo_root/$script"; then
                    status="PASS"
                else
                    status="FAIL"
                    error="Playwright test failed"
                fi
            else
                error="Script not found: $script"
            fi
            ;;
        cypress)
            # Cypress E2E tests
            if [[ -n "$script" && -f "$repo_root/$script" ]]; then
                if run_cypress_test "$repo_root/$script"; then
                    status="PASS"
                else
                    status="FAIL"
                    error="Cypress test failed"
                fi
            else
                error="Script not found: $script"
            fi
            ;;
        http)
            # Simple HTTP test (inline in verify.yaml)
            status="SKIP"
            error="HTTP tests require full YAML parsing"
            ;;
        manual)
            status="SKIP"
            error="Manual verification required"
            ;;
        *)
            status="SKIP"
            error="Unknown test type: $type"
            ;;
    esac

    local end_time=$(date +%s%3N 2>/dev/null || echo "0")
    local duration=$((end_time - start_time))

    ACCEPTANCE_RESULTS+=("$ref|$name|$status|$duration|$error")
    log_test "$status" "$name [$ref]" "$duration" "$error"

    case "$status" in
        PASS) ((ACCEPTANCE_PASSED++)) ;;
        FAIL) ((ACCEPTANCE_FAILED++)) ;;
        SKIP) ((ACCEPTANCE_SKIPPED++)) ;;
    esac
}

run_tests_in_directory() {
    local test_dir="$1"
    local repo_root=$(get_repo_root)

    # Detect test runner
    if [[ -f "$repo_root/package.json" ]]; then
        # Node.js project
        if grep -q '"playwright"' "$repo_root/package.json" 2>/dev/null; then
            run_playwright_suite "$test_dir"
        elif grep -q '"cypress"' "$repo_root/package.json" 2>/dev/null; then
            run_cypress_suite "$test_dir"
        elif grep -q '"jest"' "$repo_root/package.json" 2>/dev/null; then
            run_jest_suite "$test_dir"
        elif grep -q '"vitest"' "$repo_root/package.json" 2>/dev/null; then
            run_vitest_suite "$test_dir"
        fi
    elif [[ -f "$repo_root/pytest.ini" || -f "$repo_root/pyproject.toml" ]]; then
        # Python project
        run_pytest_suite "$test_dir"
    elif [[ -f "$repo_root/go.mod" ]]; then
        # Go project
        run_go_tests "$test_dir"
    fi
}

# =============================================================================
# TEST RUNNERS
# =============================================================================

run_api_test() {
    local script="$1"
    local repo_root=$(get_repo_root)

    cd "$repo_root"

    # Detect and run based on file extension
    case "$script" in
        *.ts|*.js)
            if command -v npx &> /dev/null; then
                PLAYWRIGHT_BASE_URL="$BASE_URL" npx ts-node "$script" 2>/dev/null || \
                PLAYWRIGHT_BASE_URL="$BASE_URL" node "$script" 2>/dev/null
            fi
            ;;
        *.py)
            if command -v python &> /dev/null; then
                BASE_URL="$BASE_URL" python "$script" 2>/dev/null
            fi
            ;;
        *)
            return 1
            ;;
    esac
}

run_playwright_test() {
    local script="$1"
    local repo_root=$(get_repo_root)

    cd "$repo_root"

    if command -v npx &> /dev/null; then
        PLAYWRIGHT_BASE_URL="$BASE_URL" npx playwright test "$script" --reporter=line 2>/dev/null
    else
        log_verbose "npx not found, skipping Playwright test"
        return 1
    fi
}

run_playwright_suite() {
    local test_dir="$1"
    local repo_root=$(get_repo_root)

    log_verbose "Running Playwright test suite..."

    cd "$repo_root"

    if command -v npx &> /dev/null; then
        local output
        local exit_code=0

        output=$(PLAYWRIGHT_BASE_URL="$BASE_URL" npx playwright test "$test_dir" --reporter=json 2>&1) || exit_code=$?

        # Parse results (simplified)
        if [[ $exit_code -eq 0 ]]; then
            ((ACCEPTANCE_PASSED++))
            ACCEPTANCE_RESULTS+=("E2E|playwright-suite|PASS|0|")
            log_test "PASS" "Playwright suite" "0"
        else
            ((ACCEPTANCE_FAILED++))
            ACCEPTANCE_RESULTS+=("E2E|playwright-suite|FAIL|0|Exit code: $exit_code")
            log_test "FAIL" "Playwright suite" "0" "Exit code: $exit_code"
        fi
    fi
}

run_cypress_test() {
    local script="$1"
    local repo_root=$(get_repo_root)

    cd "$repo_root"

    if command -v npx &> /dev/null; then
        CYPRESS_BASE_URL="$BASE_URL" npx cypress run --spec "$script" 2>/dev/null
    else
        return 1
    fi
}

run_cypress_suite() {
    local test_dir="$1"
    local repo_root=$(get_repo_root)

    log_verbose "Running Cypress test suite..."

    cd "$repo_root"

    if command -v npx &> /dev/null; then
        local exit_code=0
        CYPRESS_BASE_URL="$BASE_URL" npx cypress run --spec "$test_dir/**/*.cy.{js,ts}" 2>/dev/null || exit_code=$?

        if [[ $exit_code -eq 0 ]]; then
            ((ACCEPTANCE_PASSED++))
            ACCEPTANCE_RESULTS+=("E2E|cypress-suite|PASS|0|")
            log_test "PASS" "Cypress suite" "0"
        else
            ((ACCEPTANCE_FAILED++))
            ACCEPTANCE_RESULTS+=("E2E|cypress-suite|FAIL|0|Exit code: $exit_code")
            log_test "FAIL" "Cypress suite" "0" "Exit code: $exit_code"
        fi
    fi
}

run_jest_suite() {
    local test_dir="$1"
    local repo_root=$(get_repo_root)

    log_verbose "Running Jest test suite..."

    cd "$repo_root"

    if command -v npx &> /dev/null; then
        local exit_code=0
        BASE_URL="$BASE_URL" npx jest "$test_dir" --passWithNoTests 2>/dev/null || exit_code=$?

        if [[ $exit_code -eq 0 ]]; then
            ((ACCEPTANCE_PASSED++))
            ACCEPTANCE_RESULTS+=("UNIT|jest-suite|PASS|0|")
            log_test "PASS" "Jest suite" "0"
        else
            ((ACCEPTANCE_FAILED++))
            ACCEPTANCE_RESULTS+=("UNIT|jest-suite|FAIL|0|Exit code: $exit_code")
            log_test "FAIL" "Jest suite" "0" "Exit code: $exit_code"
        fi
    fi
}

run_vitest_suite() {
    local test_dir="$1"
    local repo_root=$(get_repo_root)

    log_verbose "Running Vitest test suite..."

    cd "$repo_root"

    if command -v npx &> /dev/null; then
        local exit_code=0
        BASE_URL="$BASE_URL" npx vitest run "$test_dir" 2>/dev/null || exit_code=$?

        if [[ $exit_code -eq 0 ]]; then
            ((ACCEPTANCE_PASSED++))
            ACCEPTANCE_RESULTS+=("UNIT|vitest-suite|PASS|0|")
            log_test "PASS" "Vitest suite" "0"
        else
            ((ACCEPTANCE_FAILED++))
            ACCEPTANCE_RESULTS+=("UNIT|vitest-suite|FAIL|0|Exit code: $exit_code")
            log_test "FAIL" "Vitest suite" "0" "Exit code: $exit_code"
        fi
    fi
}

run_pytest_suite() {
    local test_dir="$1"
    local repo_root=$(get_repo_root)

    log_verbose "Running pytest test suite..."

    cd "$repo_root"

    if command -v pytest &> /dev/null; then
        local exit_code=0
        BASE_URL="$BASE_URL" pytest "$test_dir" -v 2>/dev/null || exit_code=$?

        if [[ $exit_code -eq 0 ]]; then
            ((ACCEPTANCE_PASSED++))
            ACCEPTANCE_RESULTS+=("UNIT|pytest-suite|PASS|0|")
            log_test "PASS" "Pytest suite" "0"
        else
            ((ACCEPTANCE_FAILED++))
            ACCEPTANCE_RESULTS+=("UNIT|pytest-suite|FAIL|0|Exit code: $exit_code")
            log_test "FAIL" "Pytest suite" "0" "Exit code: $exit_code"
        fi
    fi
}

run_go_tests() {
    local test_dir="$1"
    local repo_root=$(get_repo_root)

    log_verbose "Running Go test suite..."

    cd "$repo_root"

    if command -v go &> /dev/null; then
        local exit_code=0
        BASE_URL="$BASE_URL" go test -v "./$test_dir/..." 2>/dev/null || exit_code=$?

        if [[ $exit_code -eq 0 ]]; then
            ((ACCEPTANCE_PASSED++))
            ACCEPTANCE_RESULTS+=("UNIT|go-test-suite|PASS|0|")
            log_test "PASS" "Go test suite" "0"
        else
            ((ACCEPTANCE_FAILED++))
            ACCEPTANCE_RESULTS+=("UNIT|go-test-suite|FAIL|0|Exit code: $exit_code")
            log_test "FAIL" "Go test suite" "0" "Exit code: $exit_code"
        fi
    fi
}

# =============================================================================
# RESULTS GENERATION
# =============================================================================

generate_results() {
    local results_file="$STATE_DIR/last-verify.json"
    local results_md="$FEATURE_DIR/verify-results.md"
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    local git_sha=$(git rev-parse HEAD 2>/dev/null || echo "unknown")

    # Determine overall verdict
    local verdict="PASS"
    if [[ $SMOKE_FAILED -gt 0 ]]; then
        verdict="FAIL"
    elif [[ $ACCEPTANCE_FAILED -gt 0 ]]; then
        verdict="FAIL"
    elif [[ $SMOKE_PASSED -eq 0 && $ACCEPTANCE_PASSED -eq 0 ]]; then
        verdict="NO_TESTS"
    fi

    # Save JSON results
    mkdir -p "$STATE_DIR"
    cat > "$results_file" << EOF
{
  "environment": "$ENV",
  "base_url": "$BASE_URL",
  "timestamp": "$timestamp",
  "git_sha": "$git_sha",
  "verdict": "$verdict",
  "smoke": {
    "passed": $SMOKE_PASSED,
    "failed": $SMOKE_FAILED,
    "total": $((SMOKE_PASSED + SMOKE_FAILED))
  },
  "acceptance": {
    "passed": $ACCEPTANCE_PASSED,
    "failed": $ACCEPTANCE_FAILED,
    "skipped": $ACCEPTANCE_SKIPPED,
    "total": $((ACCEPTANCE_PASSED + ACCEPTANCE_FAILED + ACCEPTANCE_SKIPPED))
  },
  "results": {
    "smoke": [
$(print_json_array "${SMOKE_RESULTS[@]:-}")
    ],
    "acceptance": [
$(print_json_array "${ACCEPTANCE_RESULTS[@]:-}")
    ]
  }
}
EOF

    log "Saved results to $results_file"

    # Generate Markdown results if feature dir exists
    if [[ -n "$FEATURE_DIR" && -d "$FEATURE_DIR" ]]; then
        generate_markdown_results "$results_md" "$timestamp" "$git_sha" "$verdict"
        log "Generated verify-results.md"
    fi

    # Update spec.md with verification status
    update_spec_verification "$verdict" "$timestamp"
}

print_json_array() {
    local first=true
    for item in "$@"; do
        [[ -z "$item" ]] && continue

        local ref=$(echo "$item" | cut -d'|' -f1)
        local name=$(echo "$item" | cut -d'|' -f2)
        local status=$(echo "$item" | cut -d'|' -f3)
        local duration=$(echo "$item" | cut -d'|' -f4)
        local error=$(echo "$item" | cut -d'|' -f5-)

        # Handle smoke tests (different format)
        if [[ "$name" == "PASS" || "$name" == "FAIL" || "$name" == "SKIP" ]]; then
            name="$ref"
            status=$(echo "$item" | cut -d'|' -f2)
            duration=$(echo "$item" | cut -d'|' -f3)
            error=$(echo "$item" | cut -d'|' -f4-)
            ref=""
        fi

        [[ "$first" == "false" ]] && echo ","
        first=false

        cat << EOF
      {
        "ref": "$ref",
        "name": "$name",
        "status": "$status",
        "duration": $duration,
        "error": "$error"
      }
EOF
    done
}

generate_markdown_results() {
    local output_file="$1"
    local timestamp="$2"
    local git_sha="$3"
    local verdict="$4"

    local verdict_emoji="✅"
    [[ "$verdict" == "FAIL" ]] && verdict_emoji="❌"
    [[ "$verdict" == "NO_TESTS" ]] && verdict_emoji="⚠️"

    cat > "$output_file" << EOF
# Verification Results

**Environment**: $ENV
**Timestamp**: $timestamp
**Git SHA**: \`$git_sha\`
**Base URL**: $BASE_URL

## Summary

| Category | Total | Passed | Failed | Skipped |
|----------|-------|--------|--------|---------|
| Smoke | $((SMOKE_PASSED + SMOKE_FAILED)) | $SMOKE_PASSED | $SMOKE_FAILED | 0 |
| Acceptance | $((ACCEPTANCE_PASSED + ACCEPTANCE_FAILED + ACCEPTANCE_SKIPPED)) | $ACCEPTANCE_PASSED | $ACCEPTANCE_FAILED | $ACCEPTANCE_SKIPPED |

**Verdict**: $verdict_emoji $verdict

## Smoke Tests

| Name | Status | Duration |
|------|--------|----------|
EOF

    for result in "${SMOKE_RESULTS[@]:-}"; do
        [[ -z "$result" ]] && continue
        local name=$(echo "$result" | cut -d'|' -f1)
        local status=$(echo "$result" | cut -d'|' -f2)
        local duration=$(echo "$result" | cut -d'|' -f3)

        local status_icon="✅"
        [[ "$status" == "FAIL" ]] && status_icon="❌"
        [[ "$status" == "SKIP" ]] && status_icon="⏭️"

        echo "| $name | $status_icon $status | ${duration}ms |" >> "$output_file"
    done

    cat >> "$output_file" << EOF

## Acceptance Tests

| Ref | Name | Status | Duration | Error |
|-----|------|--------|----------|-------|
EOF

    for result in "${ACCEPTANCE_RESULTS[@]:-}"; do
        [[ -z "$result" ]] && continue
        local ref=$(echo "$result" | cut -d'|' -f1)
        local name=$(echo "$result" | cut -d'|' -f2)
        local status=$(echo "$result" | cut -d'|' -f3)
        local duration=$(echo "$result" | cut -d'|' -f4)
        local error=$(echo "$result" | cut -d'|' -f5-)

        local status_icon="✅"
        [[ "$status" == "FAIL" ]] && status_icon="❌"
        [[ "$status" == "SKIP" ]] && status_icon="⏭️"

        echo "| $ref | $name | $status_icon $status | ${duration}ms | $error |" >> "$output_file"
    done

    # Add failed tests section if any
    if [[ $SMOKE_FAILED -gt 0 || $ACCEPTANCE_FAILED -gt 0 ]]; then
        cat >> "$output_file" << EOF

## Failed Tests

EOF
        for result in "${SMOKE_RESULTS[@]:-}" "${ACCEPTANCE_RESULTS[@]:-}"; do
            [[ -z "$result" ]] && continue
            local status=$(echo "$result" | cut -d'|' -f2)
            # Handle different formats
            if [[ "$status" != "FAIL" ]]; then
                status=$(echo "$result" | cut -d'|' -f3)
            fi

            if [[ "$status" == "FAIL" ]]; then
                local name=$(echo "$result" | cut -d'|' -f1)
                local error=$(echo "$result" | cut -d'|' -f4-)

                cat >> "$output_file" << EOF
### $name

**Error**: $error

**Suggested Action**: Investigate the failure and fix the underlying issue.

EOF
            fi
        done
    fi
}

update_spec_verification() {
    local verdict="$1"
    local timestamp="$2"

    # Find spec.md
    local spec_file=""
    if [[ -n "$FEATURE_DIR" && -f "$FEATURE_DIR/spec.md" ]]; then
        spec_file="$FEATURE_DIR/spec.md"
    else
        return 0
    fi

    # Check if spec.md has a verification status section
    if grep -q "## Verification Status" "$spec_file" 2>/dev/null; then
        # Update existing section
        local status_icon="✅"
        [[ "$verdict" == "FAIL" ]] && status_icon="❌"
        [[ "$verdict" == "NO_TESTS" ]] && status_icon="⚠️"

        # Create temp file with updated content
        local temp_file=$(mktemp)
        local in_verification=false
        local updated=false

        while IFS= read -r line; do
            if [[ "$line" =~ ^##[[:space:]]+Verification[[:space:]]+Status ]]; then
                in_verification=true
                echo "$line" >> "$temp_file"
                echo "" >> "$temp_file"
                echo "**Last Verified**: $timestamp ($ENV)" >> "$temp_file"
                echo "**Status**: $status_icon $verdict" >> "$temp_file"
                echo "" >> "$temp_file"
                updated=true
                continue
            fi

            if [[ "$in_verification" == "true" ]]; then
                # Skip old verification content until next section
                if [[ "$line" =~ ^## ]]; then
                    in_verification=false
                    echo "$line" >> "$temp_file"
                fi
                continue
            fi

            echo "$line" >> "$temp_file"
        done < "$spec_file"

        if [[ "$updated" == "true" ]]; then
            mv "$temp_file" "$spec_file"
            log "Updated verification status in spec.md"
        else
            rm "$temp_file"
        fi
    fi
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    if [[ -z "$ENV" || -z "$BASE_URL" || -z "$STATE_DIR" ]]; then
        echo "Missing required arguments" >&2
        echo "Usage: verify.sh --env <env> --base-url <url> --state-dir <dir> [--config <verify.yaml>] [--feature-dir <dir>]" >&2
        exit 1
    fi

    log "Verifying deployment for environment: $ENV"
    log "Base URL: $BASE_URL"
    log_verbose "Config: $CONFIG"
    log_verbose "Feature dir: $FEATURE_DIR"

    # Wait for service to be ready
    log "Waiting for service to be ready..."
    local retries=0
    local max_retries=30

    while [[ $retries -lt $max_retries ]]; do
        if curl -s --max-time 5 "$BASE_URL/health" > /dev/null 2>&1; then
            log "Service is ready"
            break
        fi
        ((retries++))
        log_verbose "Waiting for service... ($retries/$max_retries)"
        sleep 2
    done

    if [[ $retries -eq $max_retries ]]; then
        log "Warning: Service may not be fully ready after $max_retries attempts"
    fi

    # Run tests
    run_smoke_tests
    run_acceptance_tests

    # Generate results
    generate_results

    # Summary
    local total_passed=$((SMOKE_PASSED + ACCEPTANCE_PASSED))
    local total_failed=$((SMOKE_FAILED + ACCEPTANCE_FAILED))

    log "Verification complete: $total_passed passed, $total_failed failed"

    # Exit with error if any tests failed
    if [[ $total_failed -gt 0 ]]; then
        exit 1
    fi
}

main "$@"
