# Vision-Powered UX Validation Guide

This document provides context for AI agents performing automated visual UX validation via the `/speckit.implement` command's Step 1.7.

## Overview

Vision-Powered UX Validation uses Claude's vision capabilities to analyze UI screenshots against established UX quality principles, Nielsen's heuristics, and common anti-patterns. This ensures consistent, accessible, and user-friendly interfaces before deployment.

## Screenshot Capture Strategy

### Viewport Breakpoints

| Name | Width | Height | Rationale |
|------|-------|--------|-----------|
| mobile | 375px | 812px | iPhone 12/13/14 Pro baseline |
| tablet | 768px | 1024px | iPad portrait (common tablet) |
| desktop | 1440px | 900px | Common laptop resolution |

### State Triggers

Each screen should be captured in multiple states to validate complete UX flows:

| State | How to Trigger | Purpose | Example |
|-------|---------------|---------|---------|
| default | Initial page load | Baseline appearance | Normal form display |
| loading | Mock slow API (3s delay) | Loading indicator presence | Spinner, skeleton, progress bar |
| error | Mock 500/4xx response | Error message handling | Form validation, API failure |
| empty | Mock empty array response | Empty state design | No results, first-time user |
| success | Mock successful action | Success feedback | Toast, redirect, confirmation |

### Playwright MCP Screenshot Commands

```text
# Navigate to screen
browser_navigate(url)

# Set viewport
browser_resize(width, height)

# Trigger state (via evaluate or mock)
browser_evaluate("window.__mockApiState = 'loading'")

# Capture screenshot
browser_take_screenshot(filename)
```

## Vision Analysis Prompts

### Quick Check (per screenshot)

Use this compact prompt for individual screenshot analysis:

```text
Analyze this UI screenshot. Check for:

1. ACCESSIBILITY: Form labels present? Contrast ratio adequate? Touch targets 44x44px+?
2. FEEDBACK: Loading indicators visible? Error messages helpful? Success confirmation shown?
3. CONSISTENCY: Matches design system? Standard UI patterns used?
4. CLARITY: Labels intuitive? No jargon? Actions discoverable?
5. RESPONSIVENESS: Content fits viewport? No horizontal scroll? Text readable?

Report violations as:
- ID: [UXQ-xxx / H-x / UX-xxx]
- Severity: [CRITICAL / HIGH / MEDIUM / LOW]
- Element: [what UI element]
- Issue: [what's wrong]
- Suggestion: [how to fix]
```

### Deep Audit (full screen flow)

Use this comprehensive prompt for complete user journey analysis:

```text
Analyze this user flow across multiple screens.

## User Journey Context
- Flow: [login → dashboard → action → confirmation]
- User Goal: [what user is trying to accomplish]
- Entry Point: [where user started]

## Analysis Dimensions

### Mental Model Alignment (UXQ-001)
- Do labels match user expectations?
- Is terminology consistent with domain?
- Are actions predictable?

### Friction Analysis (UXQ-003)
- Is each step necessary?
- Could steps be combined?
- Are there unnecessary confirmations?

### Error Empathy (UXQ-005)
- Are error messages helpful (not blaming)?
- Do errors suggest solutions?
- Is recovery path clear?

### System Status (H1)
- Is current state always visible?
- Are progress indicators present?
- Is async feedback provided?

### Cognitive Load (UX-005)
- Too many choices at once?
- Information hierarchy clear?
- Progressive disclosure used?

Output a journey assessment with friction points marked.
```

### Accessibility Focus

Use this prompt for WCAG-specific visual checks:

```text
Perform visual accessibility audit against WCAG 2.1 AA:

## Color & Contrast
- [ ] Text contrast ratio ≥ 4.5:1 (normal text)
- [ ] Text contrast ratio ≥ 3:1 (large text, 18px+ or 14px+ bold)
- [ ] UI component contrast ≥ 3:1 against background
- [ ] Color not sole means of conveying information

## Touch & Click Targets
- [ ] Interactive elements ≥ 44x44px (iOS) / 48x48px (Android)
- [ ] Adequate spacing between targets (≥ 8px)
- [ ] Click/tap areas match visible bounds

## Visual Indicators
- [ ] Focus states visible on interactive elements
- [ ] Error states not color-only (icon or text)
- [ ] Required fields clearly marked

## Text & Readability
- [ ] Font size ≥ 16px for body text
- [ ] Line height ≥ 1.5 for body text
- [ ] No text in images (unless decorative)

Flag any violations with WCAG criterion reference.
```

## Severity Classification

| Severity | Criteria | Detection Signals | Action Required |
|----------|----------|-------------------|-----------------|
| CRITICAL | Blocks core task OR accessibility barrier | Missing form labels, <3:1 contrast, no error message, broken layout | BLOCK deployment |
| HIGH | Significant usability issue | Confusing labels, hidden primary actions, no loading state, unclear errors | WARN, recommend fix before deploy |
| MEDIUM | Minor friction, polish needed | Inconsistent spacing, verbose text, minor alignment issues | Log in backlog |
| LOW | Enhancement opportunity | Could be more delightful, micro-interactions missing | Optional improvement |

### Severity Examples

**CRITICAL (Must Fix)**:
- Form input without visible label (a11y violation)
- Error message that only says "Error" (unhelpful)
- Primary action button not visible without scrolling
- Text contrast ratio below 3:1
- Mobile layout completely broken

**HIGH (Should Fix)**:
- Submit button with no loading indicator
- Success action with no feedback
- Confusing toggle/switch labels
- Empty state with no guidance
- Form with no validation feedback

**MEDIUM (Nice to Fix)**:
- Inconsistent button styles
- Overly verbose helper text
- Minor spacing inconsistencies
- Icon without tooltip

**LOW (Consider)**:
- Could add micro-animation
- Hover states could be richer
- Empty state could be more engaging

## Integration with Existing Frameworks

### UXQ Principles (memory/domains/uxq.md)

Vision validation focuses on principles that can be visually verified:

| ID | Principle | Visual Check |
|----|-----------|--------------|
| UXQ-001 | Mental Model Alignment | Labels, terminology, iconography |
| UXQ-003 | Friction Justification | Step count, form fields, modal depth |
| UXQ-005 | Error Empathy | Error message content, tone, recovery guidance |
| UXQ-006 | FTUE Clear Guidance | Onboarding UI, empty states, hints |
| UXQ-010 | Accessibility | Contrast, targets, focus states |

Non-visual principles (UXQ-002, UXQ-004, UXQ-007, etc.) are validated by `/speckit.analyze` during spec review.

### Nielsen Heuristics (memory/knowledge/frameworks/nielsen-heuristics.md)

Vision validation focuses on visually-observable heuristics:

| ID | Heuristic | Visual Check |
|----|-----------|--------------|
| H1 | Visibility of System Status | Loading indicators, progress bars, status badges |
| H2 | Match Between System and Real World | Labels, icons, metaphors |
| H4 | Consistency and Standards | UI patterns, component usage, layout |
| H6 | Recognition Rather Than Recall | Visible options, labels, suggestions |
| H8 | Aesthetic and Minimalist Design | Clutter, information density, whitespace |

Process heuristics (H3 user control, H5 error prevention, H7 flexibility, H9 error recovery, H10 help) are validated by flow analysis.

### Anti-Patterns (memory/knowledge/anti-patterns/ux.md)

Vision validation can detect these visual anti-patterns:

| ID | Anti-Pattern | Visual Detection Signals |
|----|--------------|-------------------------|
| UX-001 | Modal Overload | Multiple overlapping modals, modal on modal |
| UX-003 | Form Abandonment Design | Very long forms, no progress indicator, reset buttons |
| UX-005 | Cognitive Overload | Dense text, many actions, complex tables |
| UX-007 | Mobile Neglect | Small touch targets, horizontal scroll, tiny text |
| UX-009 | Dark Pattern Indicators | Pre-checked opt-ins, hidden costs, confirm-shaming |

Flow-based anti-patterns (UX-002 infinite scroll, UX-004 dead ends, etc.) require user journey analysis.

## Report Generation

### UX Audit Report Structure

The generated `specs/{feature}/ux-audit.md` follows this structure:

```markdown
# UX Audit Report: [FEATURE_NAME]

**Date**: [DATE] | **Screens**: [count] | **Score**: [0-100]

## Summary

| Severity | Count | Status |
|----------|-------|--------|
| CRITICAL | [n] | [BLOCKING / RESOLVED] |
| HIGH | [n] | [REVIEW NEEDED] |
| MEDIUM | [n] | [LOGGED] |
| LOW | [n] | [OPTIONAL] |

**Overall Assessment**: [PASS / WARN / FAIL]

## Critical Issues (Must Fix)

### [ISSUE-001] [Title]
- **Screen**: [screen_name] @ [viewport]
- **Principle**: [UXQ-xxx / H-x]
- **Element**: [description]
- **Issue**: [what's wrong]
- **Suggestion**: [how to fix]
- **Screenshot**: ![issue](screenshots/issue-001.png)

[... additional issues ...]

## Screenshots Analyzed

| Screen | Mobile | Tablet | Desktop | States Captured |
|--------|--------|--------|---------|-----------------|
| Login | ✓ | ✓ | ✓ | default, error |
| Dashboard | ✓ | ✓ | ✓ | default, loading, empty |
```

## Skip Conditions

Vision validation is skipped when:

1. `--no-vision` flag passed to `/speckit.implement`
2. No `[VR:VR-xxx]` markers in tasks.md AND no FRONTEND role_group
3. Playwright MCP server unavailable
4. Feature has no UI (API-only, CLI, library)
5. `vision_validation.enabled: false` in YAML config

When skipped, SR-IMPL-14 through SR-IMPL-17 are marked as `N/A`.

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|------------|
| No screenshots captured | Playwright MCP not running | Start MCP server, check config |
| Vision analysis timeout | Large/complex screenshots | Reduce viewport count, simplify states |
| False positives | Context mismatch | Provide more specific screen context |
| Missing screens | VR markers not set | Add `[VR:VR-xxx]` to UI tasks |
| State not triggering | Mock setup incorrect | Verify API mock configuration |

## Performance Considerations

- **Screenshot count**: screens × viewports × states (e.g., 5 × 3 × 5 = 75 screenshots)
- **Vision API calls**: One per screenshot for quick check, batched for deep audit
- **Recommended limits**: ≤10 screens, ≤3 viewports, ≤5 states per screen
- **Timeout**: 60s per screenshot capture, 30s per vision analysis

For large features, consider:
- Prioritizing critical user flows
- Reducing state coverage to essential ones
- Running vision validation separately with `/speckit.ux-audit`
