# Mockup Quality Score (MQS) Rubric

This document defines the scoring system for evaluating mockup quality in `/speckit.preview`.

## Overview

MQS is a 0-100 score that measures mockup fidelity across six dimensions. It extends the Design Quality Score (DQS) with mockup-specific validation.

```
┌─────────────────────────────────────────────────────────────────┐
│                    MQS CALCULATION                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  MQS = Σ (dimension_score × weight)                             │
│                                                                  │
│  ┌──────────────────┬────────┬────────┐                         │
│  │ Dimension        │ Points │ Weight │                         │
│  ├──────────────────┼────────┼────────┤                         │
│  │ Visual Fidelity  │ 0-25   │ 25%    │                         │
│  │ Token Compliance │ 0-20   │ 20%    │                         │
│  │ Accessibility    │ 0-20   │ 20%    │                         │
│  │ Responsiveness   │ 0-15   │ 15%    │                         │
│  │ Interaction      │ 0-10   │ 10%    │                         │
│  │ Polish           │ 0-10   │ 10%    │                         │
│  ├──────────────────┼────────┼────────┤                         │
│  │ TOTAL            │ 0-100  │ 100%   │                         │
│  └──────────────────┴────────┴────────┘                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Quality Gates

| MQS Range | Status | Action |
|-----------|--------|--------|
| **80-100** | Production Ready | Approve for deployment |
| **60-79** | Needs Polish | Review and fix issues |
| **40-59** | Major Issues | Significant rework needed |
| **0-39** | Regenerate | Discard and regenerate |

---

## Dimension 1: Visual Fidelity (25 points)

Measures how closely the mockup matches professional design standards.

### Scoring Breakdown

| Criterion | Points | Description |
|-----------|--------|-------------|
| Layout Accuracy | 8 | Matches wireframe/spec structure |
| Visual Hierarchy | 5 | Clear content prioritization |
| Color Harmony | 5 | Palette cohesion and balance |
| Professional Appearance | 4 | Non-"AI", polished look |
| Brand Alignment | 3 | Matches brand identity |

### Evaluation Criteria

```yaml
layout_accuracy:
  8_points:
    - All elements positioned per spec
    - Grid alignment perfect
    - Proportions match design
  5_points:
    - Most elements correct
    - Minor alignment issues
    - Acceptable proportions
  0_points:
    - Significant layout errors
    - Missing elements
    - Broken structure

visual_hierarchy:
  5_points:
    - Clear primary/secondary/tertiary
    - Eye flow follows intent
    - Emphasis where needed
  3_points:
    - Mostly clear hierarchy
    - Some confusion points
  0_points:
    - Flat, no hierarchy
    - Competing elements
    - Unclear focus

color_harmony:
  5_points:
    - Cohesive palette
    - Appropriate contrast
    - Mood matches intent
  3_points:
    - Mostly harmonious
    - Minor clashes
  0_points:
    - Jarring combinations
    - Random colors
    - No palette coherence

professional_appearance:
  4_points:
    - Looks hand-crafted
    - No AI artifacts
    - Polished details
  2_points:
    - Acceptable quality
    - Minor rough edges
  0_points:
    - Obviously AI-generated
    - Generic/templated look
    - Unfinished feel

brand_alignment:
  3_points:
    - Matches brand guidelines
    - Correct logo/assets usage
    - Voice/tone consistent
  1_point:
    - Partial alignment
    - Some deviations
  0_points:
    - Off-brand appearance
    - Incorrect usage
```

---

## Dimension 2: Token Compliance (20 points)

Measures adherence to design system tokens.

### Scoring Breakdown

| Criterion | Points | Description |
|-----------|--------|-------------|
| Color Tokens | 6 | All colors from design system |
| Spacing Tokens | 6 | All spacing from grid system |
| Typography Tokens | 5 | All fonts from type scale |
| Other Tokens | 3 | Shadows, radii, etc. |

### Compliance Calculation

```
token_score = (compliant_values / total_values) × max_points

Example:
  Colors: 45/52 compliant = 86.5% × 6 = 5.19 points
  Spacing: 38/40 compliant = 95% × 6 = 5.70 points
  Typography: 18/18 compliant = 100% × 5 = 5.00 points
  Other: 5/8 compliant = 62.5% × 3 = 1.88 points
  TOTAL: 17.77 points (rounded to 18)
```

### Violation Categories

```yaml
critical_violations:
  - Hardcoded hex colors in CSS
  - Magic number spacing values
  - Inline style overrides
  - Custom font-size outside scale

warning_violations:
  - Near-match token values
  - Computed values that could use tokens
  - Shorthand properties mixing tokens/values

acceptable:
  - One-off values with clear justification
  - Third-party component overrides
  - Browser-specific adjustments
```

---

## Dimension 3: Accessibility (20 points)

Measures WCAG compliance and usability.

### Scoring Breakdown

| Criterion | Points | Description |
|-----------|--------|-------------|
| Color Contrast | 6 | Text readable against backgrounds |
| Touch Targets | 5 | Minimum 44×44px interactive areas |
| Focus Indicators | 4 | Visible keyboard focus states |
| ARIA Labels | 3 | Proper semantic markup |
| Motion Safety | 2 | Respects reduced-motion |

### Contrast Scoring

```yaml
contrast_levels:
  6_points:
    - All text ≥ 4.5:1 (AA)
    - Large text ≥ 3:1
    - No exceptions
  4_points:
    - 90%+ compliant
    - Minor violations only
  2_points:
    - 70-90% compliant
    - Some readability issues
  0_points:
    - < 70% compliant
    - Major readability problems
```

### Touch Target Scoring

```yaml
touch_targets:
  5_points:
    - All targets ≥ 44×44px (AAA)
    - Adequate spacing between
    - Finger-friendly design
  3_points:
    - Most targets compliant
    - Minor violations (32-44px)
    - Acceptable mobile use
  1_point:
    - Many small targets
    - Crowded interactive areas
  0_points:
    - Critical violations (<24px)
    - Unusable on touch devices
```

### Focus Indicator Scoring

```yaml
focus_indicators:
  4_points:
    - All interactive elements have visible focus
    - Focus style is high-contrast
    - Tab order is logical
  2_points:
    - Most elements have focus
    - Some weak indicators
  0_points:
    - Missing focus states
    - Keyboard navigation broken
```

---

## Dimension 4: Responsiveness (15 points)

Measures adaptation across viewport sizes.

### Scoring Breakdown

| Criterion | Points | Description |
|-----------|--------|-------------|
| Breakpoint Handling | 5 | Proper layout changes |
| Content Reflow | 5 | Text/images adapt well |
| Touch Adaptation | 3 | Mobile-specific adjustments |
| Orientation Support | 2 | Portrait/landscape work |

### Breakpoint Scoring

```yaml
breakpoints:
  mobile: 375px
  tablet: 768px
  desktop: 1024px
  wide: 1440px

scoring:
  5_points:
    - All breakpoints implemented
    - Smooth transitions
    - No horizontal scroll
  3_points:
    - Major breakpoints work
    - Minor issues at edges
  0_points:
    - Broken at mobile/desktop
    - Layout collapse
    - Unusable at some sizes
```

---

## Dimension 5: Interaction Design (10 points)

Measures interactive behavior completeness.

### Scoring Breakdown

| Criterion | Points | Description |
|-----------|--------|-------------|
| State Coverage | 4 | All states defined (hover, active, etc.) |
| Transitions | 3 | Smooth, purposeful animations |
| Feedback | 3 | Clear user feedback mechanisms |

### State Coverage Scoring

```yaml
required_states:
  - default
  - hover
  - active/pressed
  - focus
  - disabled
  - loading (where applicable)
  - error (where applicable)

scoring:
  4_points:
    - All applicable states defined
    - States visually distinct
    - Consistent across components
  2_points:
    - Core states defined
    - Some missing (e.g., loading)
  0_points:
    - Only default state
    - No interactive feedback
```

---

## Dimension 6: Polish (10 points)

Measures attention to detail and finish quality.

### Scoring Breakdown

| Criterion | Points | Description |
|-----------|--------|-------------|
| Consistency | 4 | Same patterns used throughout |
| Alignment | 3 | Pixel-perfect positioning |
| Micro-details | 3 | Shadows, borders, corners |

### Consistency Scoring

```yaml
consistency_checks:
  - Button styles match across pages
  - Icon sizes uniform
  - Spacing patterns repeated
  - Color usage predictable
  - Typography application consistent

scoring:
  4_points:
    - Perfect consistency
    - Design system followed
    - No one-off variations
  2_points:
    - Mostly consistent
    - Minor deviations
  0_points:
    - Inconsistent styling
    - Random variations
    - No system adherence
```

---

## MQS Report Template

```markdown
# Mockup Quality Report

**Generated**: {timestamp}
**Feature**: {feature_name}
**Screens Analyzed**: {count}

## Overall Score: {score}/100 ({status})

┌────────────────────┬───────┬────────┬─────────────────────┐
│ Dimension          │ Score │ Weight │ Status              │
├────────────────────┼───────┼────────┼─────────────────────┤
│ Visual Fidelity    │ {vf}  │ 25%    │ {vf_status}         │
│ Token Compliance   │ {tc}  │ 20%    │ {tc_status}         │
│ Accessibility      │ {a11y}│ 20%    │ {a11y_status}       │
│ Responsiveness     │ {resp}│ 15%    │ {resp_status}       │
│ Interaction Design │ {int} │ 10%    │ {int_status}        │
│ Polish             │ {pol} │ 10%    │ {pol_status}        │
├────────────────────┼───────┼────────┼─────────────────────┤
│ **TOTAL**          │ **{t}**│100%   │ {overall_status}    │
└────────────────────┴───────┴────────┴─────────────────────┘

## Top Issues

1. **{issue_1}** ({dimension}, -{points} pts)
   - Location: {file}:{line}
   - Fix: {suggestion}

2. **{issue_2}** ({dimension}, -{points} pts)
   - Location: {file}:{line}
   - Fix: {suggestion}

3. **{issue_3}** ({dimension}, -{points} pts)
   - Location: {file}:{line}
   - Fix: {suggestion}

## Auto-Fixable Issues

| Issue | Location | Auto-Fix Available |
|-------|----------|-------------------|
| Hardcoded color #3b82f6 | button.css:12 | → var(--color-primary) |
| Touch target 32px | nav.css:45 | → min-height: 44px |
| Missing hover state | card.css:78 | → Add :hover rule |

## Quality Gate: {PASSED/FAILED}

{gate_message}
```

---

## Integration Points

### Input Sources

```yaml
mockup-quality-analyzer:
  provides:
    - visual_fidelity_score
    - polish_score
    - issue_locations

token-compliance-validator:
  provides:
    - token_compliance_score
    - violation_list
    - auto_fix_suggestions

accessibility-overlay-generator:
  provides:
    - contrast_issues
    - aria_issues
    - overlay_images

touch-target-validator:
  provides:
    - touch_target_score
    - violation_list

state-matrix-generator:
  provides:
    - interaction_score
    - missing_states

visual-regression-validator:
  provides:
    - diff_percentage
    - regression_detected
```

### Output Artifacts

```
.preview/reports/
├── mqs-report.md          # Human-readable report
├── mqs-score.json         # Machine-readable score
├── issues.json            # All issues with locations
└── auto-fix.sh            # Script to apply auto-fixes
```

---

## Scoring Examples

### Example 1: High-Quality Mockup (MQS 92)

```yaml
visual_fidelity: 24/25
  - Layout perfect (8/8)
  - Clear hierarchy (5/5)
  - Harmonious colors (5/5)
  - Professional look (4/4)
  - Minor brand issue (2/3)

token_compliance: 19/20
  - 98% colors compliant
  - 100% spacing compliant
  - 100% typography compliant
  - 1 shadow hardcoded

accessibility: 18/20
  - Perfect contrast (6/6)
  - All targets ≥44px (5/5)
  - Focus on most elements (3/4)
  - All ARIA labels (3/3)
  - Reduced motion respected (1/2)

responsiveness: 14/15
  - All breakpoints work (5/5)
  - Good reflow (4/5)
  - Touch adapted (3/3)
  - Orientation support (2/2)

interaction: 9/10
  - All states defined (4/4)
  - Smooth transitions (3/3)
  - Minor feedback gap (2/3)

polish: 8/10
  - Consistent (3/4)
  - Aligned (3/3)
  - Minor detail gap (2/3)

TOTAL: 92/100 - Production Ready
```

### Example 2: Needs Work (MQS 67)

```yaml
visual_fidelity: 18/25
  - Layout issues (5/8)
  - Unclear hierarchy (3/5)
  - Colors ok (4/5)
  - AI look (2/4)
  - Brand ok (4/3→3)

token_compliance: 12/20
  - 70% colors compliant
  - 80% spacing compliant
  - 90% typography compliant
  - Several hardcoded values

accessibility: 14/20
  - Good contrast (5/6)
  - Some small targets (3/5)
  - Focus mostly ok (3/4)
  - Missing ARIA (1/3)
  - Motion ok (2/2)

responsiveness: 10/15
  - Most breakpoints (3/5)
  - Reflow issues (3/5)
  - Basic touch (2/3)
  - Portrait only (0/2)

interaction: 6/10
  - Core states only (2/4)
  - Basic transitions (2/3)
  - Limited feedback (2/3)

polish: 7/10
  - Some inconsistency (2/4)
  - Mostly aligned (3/3)
  - Details ok (2/3)

TOTAL: 67/100 - Needs Polish
```
