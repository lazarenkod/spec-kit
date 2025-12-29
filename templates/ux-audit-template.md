# UX Audit Report: [FEATURE_NAME]

**Date**: [DATE] | **Auditor**: Vision-Powered UX Validation (Step 1.7)
**Feature**: [FEATURE_DIR] | **Spec**: [spec.md link]

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Screens Analyzed** | [count] |
| **Screenshots Captured** | [count] (viewports × states) |
| **Overall UX Score** | [0-100]/100 |
| **Assessment** | [PASS / WARN / FAIL] |

### Violation Summary

| Severity | Count | Status | Action |
|----------|-------|--------|--------|
| CRITICAL | [n] | [BLOCKING / RESOLVED] | Must fix before deploy |
| HIGH | [n] | [REVIEW NEEDED / ADDRESSED] | Should fix, warn if not |
| MEDIUM | [n] | [LOGGED] | Add to backlog |
| LOW | [n] | [OPTIONAL] | Nice to have |

---

## Critical Issues (Must Fix Before Deployment)

<!--
  CRITICAL issues block deployment. Each must be addressed and re-validated.
  Remove this section if no CRITICAL issues found.
-->

### [CRIT-001] [Issue Title]

| Attribute | Value |
|-----------|-------|
| **Screen** | [screen_name] |
| **Viewport** | [mobile / tablet / desktop] |
| **State** | [default / loading / error / empty / success] |
| **Principle Violated** | [UXQ-xxx / H-x / UX-xxx] |
| **Element** | [description of UI element, e.g., "Login form email input"] |

**Issue**: [Clear description of what's wrong]

**Impact**: [Why this matters to users - e.g., "Screen reader users cannot identify the input purpose"]

**Suggestion**: [Specific actionable fix - e.g., "Add visible `<label for='email'>Email</label>` above the input field"]

**Screenshot**:
![CRIT-001](screenshots/[screen]_[viewport]_[state]_crit001.png)

**Validation Criteria**: [What to check after fix - e.g., "Label visible and associated via `for` attribute"]

---

## High Priority Issues (Should Fix)

<!--
  HIGH issues cause significant usability problems but don't completely block users.
  These should be addressed before deployment if possible.
-->

### [HIGH-001] [Issue Title]

| Attribute | Value |
|-----------|-------|
| **Screen** | [screen_name] |
| **Viewport** | [mobile / tablet / desktop] |
| **State** | [default / loading / error / empty / success] |
| **Principle Violated** | [UXQ-xxx / H-x / UX-xxx] |
| **Element** | [description of UI element] |

**Issue**: [Description]

**Suggestion**: [Fix recommendation]

---

## Medium Priority Issues (Backlog)

<!--
  MEDIUM issues are minor friction points or polish opportunities.
  Log for future sprints but don't block deployment.
-->

| ID | Screen | Viewport | Principle | Issue Summary | Suggestion |
|----|--------|----------|-----------|---------------|------------|
| MED-001 | [screen] | [viewport] | [principle] | [brief issue] | [brief fix] |
| MED-002 | [screen] | [viewport] | [principle] | [brief issue] | [brief fix] |

---

## Low Priority Issues (Optional Enhancements)

<!--
  LOW issues are enhancement opportunities, not problems.
  Consider for future polish passes.
-->

| ID | Screen | Observation | Enhancement Idea |
|----|--------|-------------|------------------|
| LOW-001 | [screen] | [what could be improved] | [how to enhance] |

---

## Screenshots Analyzed

### Coverage Matrix

| Screen | Mobile (375×812) | Tablet (768×1024) | Desktop (1440×900) | States |
|--------|:----------------:|:-----------------:|:------------------:|--------|
| [screen_1] | ✓ | ✓ | ✓ | default, error |
| [screen_2] | ✓ | ✓ | ✓ | default, loading, empty |
| [screen_3] | ✓ | ✓ | ✓ | default, success |

### Screenshot Gallery

<details>
<summary>Click to expand screenshot gallery</summary>

#### [Screen 1 Name]

| State | Mobile | Tablet | Desktop |
|-------|--------|--------|---------|
| default | ![Screen 1 mobile default](screenshots/screen1_mobile_default.png) | ![Screen 1 tablet default](screenshots/screen1_tablet_default.png) | ![Screen 1 desktop default](screenshots/screen1_desktop_default.png) |
| error | ![Screen 1 mobile error](screenshots/screen1_mobile_error.png) | ![Screen 1 tablet error](screenshots/screen1_tablet_error.png) | ![Screen 1 desktop error](screenshots/screen1_desktop_error.png) |

#### [Screen 2 Name]

| State | Mobile | Tablet | Desktop |
|-------|--------|--------|---------|
| default | ![Screen 2 mobile default](screenshots/screen2_mobile_default.png) | ![Screen 2 tablet default](screenshots/screen2_tablet_default.png) | ![Screen 2 desktop default](screenshots/screen2_desktop_default.png) |
| loading | ![Screen 2 mobile loading](screenshots/screen2_mobile_loading.png) | ![Screen 2 tablet loading](screenshots/screen2_tablet_loading.png) | ![Screen 2 desktop loading](screenshots/screen2_desktop_loading.png) |
| empty | ![Screen 2 mobile empty](screenshots/screen2_mobile_empty.png) | ![Screen 2 tablet empty](screenshots/screen2_tablet_empty.png) | ![Screen 2 desktop empty](screenshots/screen2_desktop_empty.png) |

</details>

---

## Validation Methodology

### Frameworks Applied

| Framework | Source | Focus Areas |
|-----------|--------|-------------|
| UXQ Principles | `memory/domains/uxq.md` | Mental model, friction, error empathy, accessibility |
| Nielsen Heuristics | `memory/knowledge/frameworks/nielsen-heuristics.md` | Visibility, consistency, recognition, minimalism |
| UX Anti-Patterns | `memory/knowledge/anti-patterns/ux.md` | Modal overload, cognitive overload, mobile neglect |

### Principles Checked

**UXQ (Visual)**:
- [x] UXQ-001: Mental Model Alignment
- [x] UXQ-003: Friction Justification
- [x] UXQ-005: Error Empathy
- [x] UXQ-006: FTUE Clear Guidance
- [x] UXQ-010: Accessibility

**Nielsen Heuristics (Visual)**:
- [x] H1: Visibility of System Status
- [x] H2: Match Between System and Real World
- [x] H4: Consistency and Standards
- [x] H6: Recognition Rather Than Recall
- [x] H8: Aesthetic and Minimalist Design

**Anti-Patterns Scanned**:
- [x] UX-001: Modal Overload
- [x] UX-003: Form Abandonment Design
- [x] UX-005: Cognitive Overload
- [x] UX-007: Mobile Neglect

---

## Score Breakdown

| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Accessibility (UXQ-010, H4) | 30% | [0-100] | [calculated] |
| Feedback & Status (H1, UXQ-005) | 25% | [0-100] | [calculated] |
| Clarity & Consistency (UXQ-001, H2, H6) | 25% | [0-100] | [calculated] |
| Efficiency & Minimalism (UXQ-003, H8) | 20% | [0-100] | [calculated] |
| **Overall** | 100% | — | **[final score]** |

### Scoring Rubric

| Score Range | Assessment | Description |
|-------------|------------|-------------|
| 90-100 | Excellent | No issues or only LOW observations |
| 80-89 | Good | Few MEDIUM issues, no HIGH or CRITICAL |
| 70-79 | Acceptable | Some HIGH issues, recommend fixes |
| 60-69 | Needs Work | Multiple HIGH issues or 1 CRITICAL |
| <60 | Failing | Multiple CRITICAL issues, blocks deployment |

---

## Recommendations Summary

### Immediate Actions (Pre-Deploy)

1. [ ] [Fix CRIT-001: Add form labels for accessibility]
2. [ ] [Fix CRIT-002: Improve error message clarity]
3. [ ] [Fix HIGH-001: Add loading indicators to async actions]

### Short-Term (Next Sprint)

1. [ ] [Address HIGH-002: Improve empty state messaging]
2. [ ] [Address MED-001 through MED-003: Spacing consistency]

### Long-Term (Backlog)

1. [ ] [LOW-001: Add micro-animations for delight]
2. [ ] [LOW-002: Enhance tooltip interactions]

---

## Re-Validation Checklist

After addressing issues, re-run vision validation and verify:

- [ ] All CRITICAL issues resolved and removed from report
- [ ] HIGH issues addressed or documented with justification
- [ ] Overall UX Score improved to acceptable range (≥70)
- [ ] Screenshot gallery updated with fixed screens
- [ ] Gate status changed from FAIL → PASS or WARN

---

## Appendix: Related Documentation

- **Feature Spec**: `specs/[feature]/spec.md`
- **Design Reference**: `specs/[feature]/design.md`
- **Tasks with VR markers**: `specs/[feature]/tasks.md`
- **Vision Validation Guide**: `templates/shared/vision-validation.md`
- **UXQ Domain**: `memory/domains/uxq.md`
- **Nielsen Heuristics**: `memory/knowledge/frameworks/nielsen-heuristics.md`
- **UX Anti-Patterns**: `memory/knowledge/anti-patterns/ux.md`

---

*Generated by Vision-Powered UX Validation (Step 1.7) on [TIMESTAMP]*
*Tool: Claude Opus with vision | Viewports: 3 | States: 5*
