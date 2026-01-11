#!/usr/bin/env bash
# Verification Test Suite for v0.2.0
# Tests all Week 1 + Week 2 features

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results
PASSED=0
FAILED=0
WARNINGS=0

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Spec Kit v0.2.0 Verification Test Suite${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Helper functions
test_pass() {
  echo -e "${GREEN}✓${NC} $1"
  ((PASSED++))
}

test_fail() {
  echo -e "${RED}✗${NC} $1"
  ((FAILED++))
}

test_warn() {
  echo -e "${YELLOW}⚠${NC} $1"
  ((WARNINGS++))
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST 1: Chain-of-Thought Reasoning Active
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}Test 1: Chain-of-Thought Reasoning in Design Agents${NC}"
echo "Checking: templates/commands/design.md"

COT_COUNT=0

# Check design-researcher agent (line ~196)
if grep -q "## Reasoning Process (Think step-by-step):" "$PROJECT_ROOT/templates/commands/design.md"; then
  if grep -A 20 "role: design-researcher" "$PROJECT_ROOT/templates/commands/design.md" | grep -q "Step 1: Analyze Requirements"; then
    test_pass "design-researcher has chain-of-thought"
    ((COT_COUNT++))
  fi
fi

# Check ux-designer agent (line ~243)
if grep -A 20 "role: ux-designer" "$PROJECT_ROOT/templates/commands/design.md" | grep -q "Step 1: Analyze Requirements"; then
  test_pass "ux-designer has chain-of-thought"
  ((COT_COUNT++))
fi

# Check product-designer agent (line ~266)
if grep -A 20 "role: product-designer" "$PROJECT_ROOT/templates/commands/design.md" | grep -q "Step 1: Analyze Requirements"; then
  test_pass "product-designer has chain-of-thought"
  ((COT_COUNT++))
fi

if [ $COT_COUNT -ge 3 ]; then
  test_pass "Chain-of-thought prompts active (found $COT_COUNT agents)"
else
  test_fail "Chain-of-thought prompts incomplete (found only $COT_COUNT agents)"
fi

echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST 2: Quality Gates Enforcement
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}Test 2: Inline Quality Gates Configured${NC}"
echo "Checking: templates/commands/design.md"

GATES_FOUND=0

# Check pre_gates section
if grep -q "pre_gates:" "$PROJECT_ROOT/templates/commands/design.md"; then
  if grep -A 5 "pre_gates:" "$PROJECT_ROOT/templates/commands/design.md" | grep -q "IG-DESIGN-001"; then
    test_pass "Pre-gate IG-DESIGN-001 (Spec Quality Check) configured"
    ((GATES_FOUND++))
  fi
fi

# Check gates section
if grep -q "^gates:" "$PROJECT_ROOT/templates/commands/design.md"; then
  if grep -A 10 "^gates:" "$PROJECT_ROOT/templates/commands/design.md" | grep -q "QG-DQS-001"; then
    test_pass "Post-gate QG-DQS-001 (Minimum DQS) configured"
    ((GATES_FOUND++))
  fi
  if grep -A 10 "^gates:" "$PROJECT_ROOT/templates/commands/design.md" | grep -q "QG-DQS-002"; then
    test_pass "Post-gate QG-DQS-002 (Accessibility) configured"
    ((GATES_FOUND++))
  fi
  if grep -A 10 "^gates:" "$PROJECT_ROOT/templates/commands/design.md" | grep -q "QG-DQS-003"; then
    test_pass "Post-gate QG-DQS-003 (Token Compliance) configured"
    ((GATES_FOUND++))
  fi
fi

if [ $GATES_FOUND -ge 4 ]; then
  test_pass "Quality gates enforcement active (found $GATES_FOUND gates)"
else
  test_fail "Quality gates incomplete (found only $GATES_FOUND gates)"
fi

echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST 3: Few-Shot Examples Loaded
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}Test 3: Few-Shot Examples Library${NC}"
echo "Checking: templates/shared/few-shot-examples/"

EXAMPLES_DIR="$PROJECT_ROOT/templates/shared/few-shot-examples"
EXPECTED_FILES=(
  "button-examples.md"
  "input-examples.md"
  "card-examples.md"
  "form-examples.md"
  "navigation-examples.md"
  "modal-examples.md"
  "table-examples.md"
  "list-examples.md"
  "avatar-examples.md"
  "badge-examples.md"
)

FILES_FOUND=0

if [ ! -d "$EXAMPLES_DIR" ]; then
  test_fail "Few-shot examples directory not found"
else
  for file in "${EXPECTED_FILES[@]}"; do
    if [ -f "$EXAMPLES_DIR/$file" ]; then
      # Check if file has content (at least 100 lines)
      LINE_COUNT=$(wc -l < "$EXAMPLES_DIR/$file")
      if [ "$LINE_COUNT" -gt 100 ]; then
        test_pass "$file exists and has content ($LINE_COUNT lines)"
        ((FILES_FOUND++))
      else
        test_warn "$file exists but may be incomplete ($LINE_COUNT lines)"
      fi
    else
      test_fail "$file not found"
    fi
  done
fi

# Check v0-generation.md integration
if grep -q "load_few_shot_examples" "$PROJECT_ROOT/templates/skills/v0-generation.md"; then
  test_pass "Few-shot loading function integrated in v0-generation.md"
  ((FILES_FOUND++))
else
  test_fail "Few-shot loading function not found in v0-generation.md"
fi

if [ $FILES_FOUND -ge 10 ]; then
  test_pass "Few-shot examples library complete ($FILES_FOUND/11 checks passed)"
else
  test_fail "Few-shot examples library incomplete ($FILES_FOUND/11 checks passed)"
fi

echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST 4: Anti-Patterns Detection
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}Test 4: Anti-Patterns Library${NC}"
echo "Checking: templates/shared/design-anti-patterns.md"

ANTIPATTERNS_FILE="$PROJECT_ROOT/templates/shared/design-anti-patterns.md"

if [ ! -f "$ANTIPATTERNS_FILE" ]; then
  test_fail "Anti-patterns file not found"
else
  # Check for major anti-pattern categories
  CATEGORIES=0

  if grep -q "## Visual Anti-Patterns" "$ANTIPATTERNS_FILE"; then
    test_pass "Visual anti-patterns category exists"
    ((CATEGORIES++))
  fi

  if grep -q "## Accessibility Anti-Patterns" "$ANTIPATTERNS_FILE"; then
    test_pass "Accessibility anti-patterns category exists"
    ((CATEGORIES++))
  fi

  if grep -q "## Component Anti-Patterns" "$ANTIPATTERNS_FILE"; then
    test_pass "Component anti-patterns category exists"
    ((CATEGORIES++))
  fi

  # Check for specific anti-patterns
  AP_COUNT=$(grep -c "AP-[A-Z]*-[0-9]*:" "$ANTIPATTERNS_FILE" || echo "0")

  if [ "$AP_COUNT" -ge 40 ]; then
    test_pass "Anti-patterns library comprehensive ($AP_COUNT patterns documented)"
  elif [ "$AP_COUNT" -ge 20 ]; then
    test_warn "Anti-patterns library partial ($AP_COUNT patterns documented)"
  else
    test_fail "Anti-patterns library incomplete ($AP_COUNT patterns documented)"
  fi

  # Check integration in design command
  if grep -q "design-anti-patterns.md" "$PROJECT_ROOT/templates/commands/design.md"; then
    test_pass "Anti-patterns integrated in design command"
  else
    test_warn "Anti-patterns not explicitly referenced in design command"
  fi
fi

echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST 5: Retina Screenshots Configuration
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}Test 5: Retina/HiDPI Screenshots${NC}"
echo "Checking: templates/commands/preview.md"

PREVIEW_FILE="$PROJECT_ROOT/templates/commands/preview.md"

if [ ! -f "$PREVIEW_FILE" ]; then
  test_fail "Preview command file not found"
else
  # Check for deviceScaleFactor configuration
  if grep -q "deviceScaleFactor: 2" "$PREVIEW_FILE"; then
    test_pass "Retina configuration found (deviceScaleFactor: 2)"
  else
    test_fail "Retina configuration not found"
  fi

  # Check for 2x output dimensions documentation
  if grep -q "750×1624px" "$PREVIEW_FILE"; then
    test_pass "2x mobile output dimensions documented (750×1624px)"
  else
    test_warn "2x mobile output dimensions not documented"
  fi

  if grep -q "1536×2048px" "$PREVIEW_FILE"; then
    test_pass "2x tablet output dimensions documented (1536×2048px)"
  else
    test_warn "2x tablet output dimensions not documented"
  fi

  if grep -q "2880×1800px" "$PREVIEW_FILE"; then
    test_pass "2x desktop output dimensions documented (2880×1800px)"
  else
    test_warn "2x desktop output dimensions not documented"
  fi

  # Check COMMANDS_GUIDE.md documentation
  if grep -q "Screenshot Quality (NEW v0.2.0)" "$PROJECT_ROOT/docs/COMMANDS_GUIDE.md"; then
    test_pass "Retina screenshots documented in COMMANDS_GUIDE.md"
  else
    test_warn "Retina screenshots not documented in COMMANDS_GUIDE.md"
  fi
fi

echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SUMMARY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Test Summary${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  ${GREEN}✓ Passed:${NC}   $PASSED"
echo -e "  ${RED}✗ Failed:${NC}   $FAILED"
echo -e "  ${YELLOW}⚠ Warnings:${NC} $WARNINGS"
echo ""

TOTAL=$((PASSED + FAILED))
if [ $TOTAL -gt 0 ]; then
  SUCCESS_RATE=$((PASSED * 100 / TOTAL))
  echo -e "  Success Rate: ${SUCCESS_RATE}%"
  echo ""
fi

if [ $FAILED -eq 0 ]; then
  echo -e "${GREEN}✓ All critical tests passed!${NC}"
  echo -e "${GREEN}✓ v0.2.0 features verified successfully${NC}"
  exit 0
else
  echo -e "${RED}✗ Some tests failed. Please review the results above.${NC}"
  exit 1
fi
