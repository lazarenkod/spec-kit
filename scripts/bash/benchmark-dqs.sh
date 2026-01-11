#!/usr/bin/env bash
# DQS Benchmarking Framework for v0.2.0
# Measures design quality improvements

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BENCHMARK_DIR="$PROJECT_ROOT/.benchmark"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Test components for benchmarking
TEST_COMPONENTS=(
  "button"
  "input"
  "card"
  "form"
  "navigation"
  "modal"
  "table"
  "list"
  "avatar"
  "badge"
)

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  DQS Benchmarking Framework v0.2.0${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Create benchmark directory
mkdir -p "$BENCHMARK_DIR/baseline"
mkdir -p "$BENCHMARK_DIR/v0.2.0"
mkdir -p "$BENCHMARK_DIR/reports"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BASELINE MEASUREMENT (Without v0.2.0 Features)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${CYAN}Phase 1: Baseline Measurement (Without v0.2.0 Features)${NC}"
echo ""
echo "This would measure DQS for components generated WITHOUT:"
echo "  - Chain-of-thought reasoning"
echo "  - Few-shot examples"
echo "  - Anti-patterns library"
echo ""
echo "Expected baseline DQS: 50-60"
echo ""

# Generate baseline measurement template
cat > "$BENCHMARK_DIR/baseline/measurement-template.md" << 'EOF'
# Baseline DQS Measurement

## Component: [COMPONENT_NAME]

### DQS Rubric (0-100)

#### 1. Visual Design (20 points)
- [ ] **Aesthetic Quality (5)** - Professional, polished appearance
- [ ] **Consistency (5)** - Follows design system tokens
- [ ] **Whitespace (5)** - Proper spacing and breathing room
- [ ] **Typography (5)** - Readable hierarchy

**Visual Score:** __/20

#### 2. Accessibility (20 points)
- [ ] **Color Contrast (5)** - WCAG 2.1 AA (4.5:1)
- [ ] **Touch Targets (5)** - 44×44px minimum
- [ ] **Focus Indicators (5)** - Visible focus rings
- [ ] **ARIA Labels (5)** - Proper semantic markup

**Accessibility Score:** __/20

#### 3. Component States (15 points)
- [ ] **Default State (3)** - Clear initial state
- [ ] **Hover/Active (3)** - Interactive feedback
- [ ] **Disabled (3)** - Proper disabled styling
- [ ] **Loading (3)** - Loading state present
- [ ] **Error (3)** - Error state handling

**States Score:** __/15

#### 4. Responsiveness (15 points)
- [ ] **Mobile (5)** - Works on small screens
- [ ] **Tablet (5)** - Adapts to medium screens
- [ ] **Desktop (5)** - Optimized for large screens

**Responsiveness Score:** __/15

#### 5. Token Compliance (15 points)
- [ ] **Colors (5)** - Uses design tokens (no hardcoded)
- [ ] **Spacing (5)** - Uses spacing scale
- [ ] **Typography (5)** - Uses type scale

**Token Compliance Score:** __/15

#### 6. Code Quality (15 points)
- [ ] **TypeScript (3)** - Proper types
- [ ] **Props Interface (3)** - Clear API
- [ ] **Composability (3)** - Reusable patterns
- [ ] **Performance (3)** - Optimized rendering
- [ ] **Documentation (3)** - Clear comments

**Code Quality Score:** __/15

---

### Total DQS: __/100

### Issues Found
- Issue 1: [Description]
- Issue 2: [Description]
- ...

### Notes
[Any observations about the baseline generation quality]

EOF

echo -e "${GREEN}✓${NC} Baseline measurement template created"
echo -e "  Location: $BENCHMARK_DIR/baseline/measurement-template.md"
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# v0.2.0 MEASUREMENT (With v0.2.0 Features)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${CYAN}Phase 2: v0.2.0 Measurement (With v0.2.0 Features)${NC}"
echo ""
echo "This would measure DQS for components generated WITH:"
echo "  ✓ Chain-of-thought reasoning"
echo "  ✓ Few-shot examples"
echo "  ✓ Anti-patterns library"
echo "  ✓ Quality gates"
echo ""
echo "Expected v0.2.0 DQS: 70+"
echo ""

# Generate v0.2.0 measurement template
cp "$BENCHMARK_DIR/baseline/measurement-template.md" "$BENCHMARK_DIR/v0.2.0/measurement-template.md"

echo -e "${GREEN}✓${NC} v0.2.0 measurement template created"
echo -e "  Location: $BENCHMARK_DIR/v0.2.0/measurement-template.md"
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# COMPARISON REPORT TEMPLATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cat > "$BENCHMARK_DIR/reports/comparison-template.md" << 'EOF'
# DQS Comparison Report: Baseline vs v0.2.0

## Executive Summary

| Metric | Baseline | v0.2.0 | Improvement |
|--------|----------|--------|-------------|
| **DQS Total** | __/100 | __/100 | +__ |
| **Visual Design** | __/20 | __/20 | +__ |
| **Accessibility** | __/20 | __/20 | +__ |
| **Component States** | __/15 | __/15 | +__ |
| **Responsiveness** | __/15 | __/15 | +__ |
| **Token Compliance** | __/15 | __/15 | +__ |
| **Code Quality** | __/15 | __/15 | +__ |

**Target Improvement:** +15-20 points
**Actual Improvement:** __ points

## Detailed Comparison

### Visual Design

**Baseline Issues:**
- [List issues found in baseline]

**v0.2.0 Improvements:**
- [List improvements from v0.2.0 features]

**Impact:** Chain-of-thought reasoning helped address [specific improvements]

---

### Accessibility

**Baseline Issues:**
- [List accessibility issues]

**v0.2.0 Improvements:**
- [List accessibility improvements]

**Impact:** Few-shot examples demonstrated proper patterns for [specific improvements]

---

### Token Compliance

**Baseline Issues:**
- [List hardcoded values]

**v0.2.0 Improvements:**
- [List token usage improvements]

**Impact:** Anti-patterns library prevented [specific anti-patterns]

---

## Feature Impact Analysis

### Chain-of-Thought Reasoning
- **Expected Impact:** +40% quality (Stanford research)
- **Observed Impact:** [Actual observations]
- **Key Improvements:** [List specific improvements]

### Few-Shot Examples
- **Expected Impact:** Optimal performance with 3-5 examples
- **Observed Impact:** [Actual observations]
- **Key Improvements:** [List specific improvements]

### Anti-Patterns Library
- **Expected Impact:** 59-64% issue reduction
- **Observed Impact:** [Actual observations]
- **Key Improvements:** [List specific improvements]

## Success Criteria

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| DQS Improvement | +15-20 | __ | [PASS/FAIL] |
| Token Compliance | 90%+ | __% | [PASS/FAIL] |
| First-Pass Success | 60%+ | __% | [PASS/FAIL] |
| Anti-Pattern Rate | <15% | __% | [PASS/FAIL] |

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

## Next Steps

- [ ] Proceed with v0.3.0 (AI mockups, perceptual diff)
- [ ] OR iterate on v0.2.0 based on findings

---

**Benchmark Date:** [DATE]
**Evaluator:** [NAME]
**Version:** v0.2.0

EOF

echo -e "${GREEN}✓${NC} Comparison report template created"
echo -e "  Location: $BENCHMARK_DIR/reports/comparison-template.md"
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# QUICK SCORING CHECKLIST
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cat > "$BENCHMARK_DIR/reports/quick-checklist.md" << 'EOF'
# Quick DQS Scoring Checklist

Use this for rapid component evaluation.

## Component: __________

### Visual (20 points)
- [ ] Professional appearance (5)
- [ ] Uses design tokens (5)
- [ ] Good whitespace (5)
- [ ] Clear typography (5)

### Accessibility (20 points)
- [ ] WCAG AA contrast 4.5:1 (5)
- [ ] Touch targets 44×44px (5)
- [ ] Visible focus rings (5)
- [ ] ARIA labels present (5)

### States (15 points)
- [ ] Default (3)
- [ ] Hover (3)
- [ ] Disabled (3)
- [ ] Loading (3)
- [ ] Error (3)

### Responsive (15 points)
- [ ] Mobile works (5)
- [ ] Tablet works (5)
- [ ] Desktop optimized (5)

### Tokens (15 points)
- [ ] Color tokens (5)
- [ ] Spacing tokens (5)
- [ ] Type tokens (5)

### Code (15 points)
- [ ] TypeScript (3)
- [ ] Props interface (3)
- [ ] Composable (3)
- [ ] Performant (3)
- [ ] Documented (3)

---

**Total: __/100**

### Quick Issues
1.
2.
3.

### Quick Wins
1.
2.
3.

EOF

echo -e "${GREEN}✓${NC} Quick scoring checklist created"
echo -e "  Location: $BENCHMARK_DIR/reports/quick-checklist.md"
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# USAGE INSTRUCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cat > "$BENCHMARK_DIR/README.md" << 'EOF'
# DQS Benchmarking Guide

## Overview

This directory contains templates and tools for measuring Design Quality Score (DQS) improvements in v0.2.0.

## Directory Structure

```
.benchmark/
├── baseline/              # Baseline measurements (without v0.2.0)
│   └── measurement-template.md
├── v0.2.0/               # v0.2.0 measurements (with features)
│   └── measurement-template.md
├── reports/              # Comparison reports
│   ├── comparison-template.md
│   └── quick-checklist.md
└── README.md            # This file
```

## Benchmarking Process

### Phase 1: Baseline Measurement

1. **Generate components WITHOUT v0.2.0 features:**
   - Disable chain-of-thought (comment out reasoning sections)
   - Remove few-shot examples loading
   - Skip anti-patterns checks

2. **For each test component:**
   ```bash
   # Generate component (baseline mode)
   /speckit.design --component button --baseline-mode

   # Measure DQS
   cp baseline/measurement-template.md baseline/button-dqs.md
   # Fill in scores manually
   ```

3. **Expected baseline DQS: 50-60**

### Phase 2: v0.2.0 Measurement

1. **Generate same components WITH v0.2.0 features:**
   - Chain-of-thought active
   - Few-shot examples loaded
   - Anti-patterns library enabled
   - Quality gates enforced

2. **For each test component:**
   ```bash
   # Generate component (v0.2.0 mode)
   /speckit.design --component button

   # Measure DQS
   cp v0.2.0/measurement-template.md v0.2.0/button-dqs.md
   # Fill in scores manually
   ```

3. **Expected v0.2.0 DQS: 70+**

### Phase 3: Comparison

1. **Calculate improvements:**
   - Total DQS delta
   - Dimension-by-dimension improvements
   - Issue reduction rates

2. **Generate comparison report:**
   ```bash
   cp reports/comparison-template.md reports/v0.2.0-comparison.md
   # Fill in comparison data
   ```

3. **Expected improvement: +15-20 points**

## Test Components

The benchmark uses 10 standard components:

1. Button
2. Input
3. Card
4. Form
5. Navigation
6. Modal
7. Table
8. List
9. Avatar
10. Badge

## Success Criteria

| Metric | Target | How to Measure |
|--------|--------|----------------|
| DQS Improvement | +15-20 | Total score delta |
| Token Compliance | 90%+ | Count hardcoded values |
| First-Pass Success | 60%+ | Components needing no fixes |
| Anti-Pattern Rate | <15% | Issues per component |

## Tips for Accurate Measurement

1. **Be consistent:** Use same rubric for both baseline and v0.2.0
2. **Document issues:** Note specific problems found
3. **Use quick checklist:** For rapid initial evaluation
4. **Review examples:** Compare against few-shot examples for reference
5. **Measure multiple:** Test all 10 components for statistical validity

## Expected Timeline

- Baseline generation: 2-3 hours
- v0.2.0 generation: 2-3 hours
- Measurement: 1-2 hours
- Comparison report: 1 hour

**Total:** 6-9 hours

## Automation Opportunities

Future improvements could automate:
- Token compliance checking (grep for hardcoded colors)
- Contrast ratio calculation
- Touch target measurement
- ARIA attribute validation

EOF

echo -e "${GREEN}✓${NC} Benchmarking guide created"
echo -e "  Location: $BENCHMARK_DIR/README.md"
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SUMMARY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Benchmarking Framework Ready${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Created benchmarking templates and guides:"
echo ""
echo -e "  ${GREEN}✓${NC} Baseline measurement template"
echo -e "  ${GREEN}✓${NC} v0.2.0 measurement template"
echo -e "  ${GREEN}✓${NC} Comparison report template"
echo -e "  ${GREEN}✓${NC} Quick scoring checklist"
echo -e "  ${GREEN}✓${NC} Benchmarking guide (README.md)"
echo ""
echo "Test Components (10):"
for component in "${TEST_COMPONENTS[@]}"; do
  echo -e "  • $component"
done
echo ""
echo -e "${CYAN}Next Steps:${NC}"
echo ""
echo "1. Generate baseline components (WITHOUT v0.2.0 features)"
echo "2. Measure baseline DQS using templates"
echo "3. Generate v0.2.0 components (WITH v0.2.0 features)"
echo "4. Measure v0.2.0 DQS using templates"
echo "5. Create comparison report"
echo ""
echo -e "${YELLOW}Expected Results:${NC}"
echo "  Baseline DQS:    50-60"
echo "  v0.2.0 DQS:      70+"
echo "  Improvement:     +15-20 points"
echo ""
echo -e "Benchmark directory: ${CYAN}$BENCHMARK_DIR${NC}"
echo ""
