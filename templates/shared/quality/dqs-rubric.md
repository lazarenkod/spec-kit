# DQS (Design Quality Score) Rubric v1.0

> **Formal definition of the 25-checkpoint design quality scoring system**

---

## Overview

The Design Quality Score (DQS) measures design specification readiness for implementation across 5 dimensions with 25 individual checkpoints. This rubric ensures design specs meet world-class standards before development begins.

**Formula**: `DQS = VisualHierarchy + Consistency + Accessibility + Responsiveness + InteractionDesign`

**Maximum Score**: 100 points

---

## Thresholds

| Score Range | Status | Action Required |
|-------------|--------|-----------------|
| **≥70** | Ready for Implementation | Proceed to code generation |
| **50-69** | Needs Improvement | Address flagged checkpoints |
| **<50** | Major Rework Required | Block implementation, significant design revision needed |

---

## Dimension 1: Visual Hierarchy (25 points)

*Measures clarity of information architecture and visual weight distribution*

| ID | Checkpoint | Points | Scoring Guidance |
|----|------------|--------|------------------|
| VH-01 | **Clear Primary Actions** | 5 | CTAs visually distinct, single primary action per screen |
| VH-02 | **Consistent Heading Levels** | 5 | H1→H6 hierarchy preserved, no skipped levels |
| VH-03 | **Appropriate White Space** | 5 | Consistent spacing system, content breathing room |
| VH-04 | **Visual Weight Balance** | 5 | F-pattern or Z-pattern layout, balanced composition |
| VH-05 | **Content Scanning Support** | 5 | Bullet points, bold keywords, chunked content |

### Scoring Scale (per checkpoint)
- **5 points**: Fully compliant, no issues
- **4 points**: Minor issues (1-2 instances needing fix)
- **3 points**: Moderate issues (3-5 instances)
- **2 points**: Significant issues (6-10 instances)
- **1 point**: Major issues (>10 instances)
- **0 points**: Not addressed at all

### Anti-Patterns

| Bad | Good |
|-----|------|
| Multiple primary CTAs per screen | Single primary CTA with clear visual dominance |
| Walls of text without structure | Chunked content with headers, lists, highlights |
| Inconsistent spacing between elements | 4px/8px grid system consistently applied |
| All elements same visual weight | Clear hierarchy: primary → secondary → tertiary |

---

## Dimension 2: Consistency (20 points)

*Measures adherence to design system tokens and patterns*

| ID | Checkpoint | Points | Scoring Guidance |
|----|------------|--------|------------------|
| CN-01 | **Token Usage** | 4 | All colors, spacing, typography use defined tokens |
| CN-02 | **Component Reuse** | 4 | Existing components used, no unnecessary variants |
| CN-03 | **Naming Conventions** | 4 | BEM/consistent naming for custom CSS classes |
| CN-04 | **Interaction Patterns** | 4 | Same actions trigger same feedback patterns |
| CN-05 | **Icon System Adherence** | 4 | Single icon library, consistent sizing and style |

### Scoring Scale (per checkpoint)
- **4 points**: 100% compliant
- **3 points**: 80-99% compliant
- **2 points**: 60-79% compliant
- **1 point**: 40-59% compliant
- **0 points**: <40% compliant

### Consistency Indicators

| Indicator | Expected |
|-----------|----------|
| Token deviation | 0 custom hex/pixel values |
| Component variants | ≤3 per component type |
| Icon sources | 1 library only |
| Interaction patterns | Documented in design system |

---

## Dimension 3: Accessibility (25 points)

*Measures WCAG 2.1 AA compliance and inclusive design*

| ID | Checkpoint | Points | Scoring Guidance |
|----|------------|--------|------------------|
| AC-01 | **Color Contrast** | 5 | Text 4.5:1, UI 3:1, large text 3:1 |
| AC-02 | **Touch Targets** | 5 | Minimum 44×44px for all interactive elements |
| AC-03 | **Focus Indicators** | 5 | Visible focus ring on all focusable elements |
| AC-04 | **Screen Reader Support** | 5 | ARIA labels, semantic HTML, alt text |
| AC-05 | **Reduced Motion** | 5 | Respects `prefers-reduced-motion` media query |

### Scoring Scale (per checkpoint)
- **5 points**: All items pass WCAG 2.1 AA
- **4 points**: 90%+ items pass
- **3 points**: 70-89% items pass
- **2 points**: 50-69% items pass
- **1 point**: 30-49% items pass
- **0 points**: <30% items pass

### WCAG 2.1 AA Quick Reference

| Criterion | Requirement | Tool |
|-----------|-------------|------|
| 1.4.3 | Text contrast ≥4.5:1 | Contrast checker |
| 1.4.11 | UI component contrast ≥3:1 | Contrast checker |
| 2.5.5 | Touch target ≥44×44px | Manual measure |
| 2.4.7 | Visible focus indicator | Manual inspection |
| 2.3.3 | Disable motion on preference | CSS `prefers-reduced-motion` |

---

## Dimension 4: Responsiveness (15 points)

*Measures adaptation across device sizes and contexts*

| ID | Checkpoint | Points | Scoring Guidance |
|----|------------|--------|------------------|
| RS-01 | **Breakpoint Definitions** | 3 | Mobile/tablet/desktop breakpoints documented |
| RS-02 | **Layout Adaptation** | 3 | Grid adjusts gracefully at each breakpoint |
| RS-03 | **Touch vs Pointer** | 3 | Larger touch targets on touch devices |
| RS-04 | **Content Priority** | 3 | Mobile shows essential content first |
| RS-05 | **Image Optimization** | 3 | Responsive images, appropriate formats |

### Scoring Scale (per checkpoint)
- **3 points**: Fully specified for all breakpoints
- **2 points**: Most breakpoints covered
- **1 point**: Only desktop specified
- **0 points**: No responsive considerations

### Breakpoint Standards

| Breakpoint | Width | Columns | Target |
|------------|-------|---------|--------|
| Mobile | <640px | 4 | Phone portrait |
| Tablet | 640-1024px | 8 | Tablet, phone landscape |
| Desktop | 1024-1440px | 12 | Laptop, desktop |
| Wide | >1440px | 12 (max-width) | Large monitors |

---

## Dimension 5: Interaction Design (15 points)

*Measures quality of animations, feedback, and state management*

| ID | Checkpoint | Points | Scoring Guidance |
|----|------------|--------|------------------|
| ID-01 | **State Definitions** | 3 | All states documented (hover, active, disabled, etc.) |
| ID-02 | **Animation Timing** | 3 | Easing curves and durations specified |
| ID-03 | **Loading States** | 3 | Skeleton, spinner, progress indicators defined |
| ID-04 | **Error Handling** | 3 | Inline errors, toasts, modals for different severities |
| ID-05 | **Success Feedback** | 3 | Confirmation patterns defined |

### Scoring Scale (per checkpoint)
- **3 points**: All scenarios covered with specifications
- **2 points**: Main scenarios covered
- **1 point**: Partial coverage
- **0 points**: Not specified

### Interaction Patterns Reference

| Interaction | Timing | Easing |
|-------------|--------|--------|
| Hover | 150ms | ease-out |
| Focus | instant | - |
| Modal enter | 200ms | ease-out |
| Modal exit | 150ms | ease-in |
| Skeleton pulse | 1.5s | ease-in-out (infinite) |
| Toast enter | 300ms | ease-out |
| Toast exit | 200ms | ease-in |

---

## DQS Calculation Worksheet

```markdown
## DQS Score Calculation

### Visual Hierarchy (max 25)
- [ ] VH-01 Clear Primary Actions: __/5
- [ ] VH-02 Consistent Heading Levels: __/5
- [ ] VH-03 Appropriate White Space: __/5
- [ ] VH-04 Visual Weight Balance: __/5
- [ ] VH-05 Content Scanning Support: __/5
**Visual Hierarchy Total**: __/25

### Consistency (max 20)
- [ ] CN-01 Token Usage: __/4
- [ ] CN-02 Component Reuse: __/4
- [ ] CN-03 Naming Conventions: __/4
- [ ] CN-04 Interaction Patterns: __/4
- [ ] CN-05 Icon System Adherence: __/4
**Consistency Total**: __/20

### Accessibility (max 25)
- [ ] AC-01 Color Contrast: __/5
- [ ] AC-02 Touch Targets: __/5
- [ ] AC-03 Focus Indicators: __/5
- [ ] AC-04 Screen Reader Support: __/5
- [ ] AC-05 Reduced Motion: __/5
**Accessibility Total**: __/25

### Responsiveness (max 15)
- [ ] RS-01 Breakpoint Definitions: __/3
- [ ] RS-02 Layout Adaptation: __/3
- [ ] RS-03 Touch vs Pointer: __/3
- [ ] RS-04 Content Priority: __/3
- [ ] RS-05 Image Optimization: __/3
**Responsiveness Total**: __/15

### Interaction Design (max 15)
- [ ] ID-01 State Definitions: __/3
- [ ] ID-02 Animation Timing: __/3
- [ ] ID-03 Loading States: __/3
- [ ] ID-04 Error Handling: __/3
- [ ] ID-05 Success Feedback: __/3
**Interaction Design Total**: __/15

---

## TOTAL DQS: __/100

**Status**: [ ] Ready (≥70) | [ ] Needs Work (50-69) | [ ] Block (<50)
```

---

## Automated Validation

DQS can be partially automated using the following tools:

| Checkpoint | Tool | Automation Level |
|------------|------|------------------|
| AC-01 Color Contrast | axe-core, Lighthouse | Full |
| AC-02 Touch Targets | Custom CSS validation | Partial |
| AC-03 Focus Indicators | axe-core | Full |
| AC-04 Screen Reader | axe-core, ARIA linting | Partial |
| CN-01 Token Usage | Stylelint with token rules | Full |
| CN-05 Icon Adherence | ESLint import rules | Full |
| RS-05 Image Optimization | Lighthouse | Full |

---

## Integration

### With /speckit.design

The design command SHOULD generate specifications that score ≥70 DQS by default.

### With /speckit.preview

Preview pipeline includes DQS validation step:
```bash
/speckit.preview --validate-dqs
```

### With /speckit.analyze

```bash
/speckit.analyze --profile dqs
```

Generates full DQS assessment with per-checkpoint scores.

### Quality Gates

| Gate ID | Threshold | Action |
|---------|-----------|--------|
| QG-DQS | DQS ≥ 70 | Block code generation |
| QG-A11Y | AC-* ≥ 60% | Block deployment |
| QG-WCAG | AC-01 = 5 | Block production |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-01-03 | Initial 25-checkpoint rubric |

---

*DQS Rubric v1.0 | Part of Spec Kit Design Quality Framework*
