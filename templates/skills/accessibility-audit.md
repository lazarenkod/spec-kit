---
description: Audit specification or implementation for WCAG accessibility compliance with empowerment framing
---

## User Input

```text
$ARGUMENTS
```

## Purpose

This skill performs comprehensive accessibility audit against WCAG 2.1 guidelines, framing accessibility as user empowerment (UXQ-010) rather than mere compliance. Can audit specifications (design phase) or code (implementation phase).

## When to Use

- After `/speckit.specify` to validate accessibility requirements
- After `/speckit.wireframe-spec` to check design accessibility
- Before release to verify WCAG compliance
- When UXQ domain is active (accessibility is MUST)

## Execution Steps

### 1. Determine Audit Mode

```text
IF code/implementation exists:
  MODE = CODE_AUDIT
  Use Explore agent for DOM/code analysis
ELSE:
  MODE = SPEC_AUDIT
  Analyze specification documents
```

### 2. Load Context

```text
1. Read memory/constitution.md for a11y requirements (CMP-004, UXQ-010)
2. Read spec.md for feature requirements
3. Read interaction-spec.md if exists
4. Read wireframes.md if exists
5. Identify target WCAG level (default: 2.1 AA)
```

### 3. WCAG 2.1 Principle Checklist

Evaluate against POUR principles:

#### Perceivable

```markdown
## 1. Perceivable

### 1.1 Text Alternatives (Level A)

**Requirement**: All non-text content has text alternatives.

**Spec Audit**:
- [ ] Images have alt text requirements specified
- [ ] Icons have accessible names defined
- [ ] Charts/graphs have data table alternatives
- [ ] Decorative images marked as such

**Code Audit**:
- [ ] All `<img>` have meaningful `alt` attributes
- [ ] Icon buttons have `aria-label` or visible text
- [ ] SVGs have `<title>` or `aria-label`
- [ ] Background images with meaning have alternatives

**Finding**: [PASS/WARN/FAIL]

### 1.2 Time-based Media (Level A/AA)

**Requirement**: Alternatives for audio/video content.

- [ ] Videos have captions specified
- [ ] Audio has transcripts specified
- [ ] Live content has real-time captions

**Finding**: [PASS/WARN/FAIL/N/A]

### 1.3 Adaptable (Level A)

**Requirement**: Content can be presented in different ways.

- [ ] Information not conveyed by layout alone
- [ ] Reading sequence is logical
- [ ] Sensory characteristics not sole cue

**Finding**: [PASS/WARN/FAIL]

### 1.4 Distinguishable (Level A/AA/AAA)

**Requirement**: Users can perceive content clearly.

| Criterion | Level | Status |
|-----------|-------|--------|
| 1.4.1 Use of Color | A | [ ] Color not sole indicator |
| 1.4.2 Audio Control | A | [ ] Auto-play audio controllable |
| 1.4.3 Contrast (Min) | AA | [ ] 4.5:1 text, 3:1 large text |
| 1.4.4 Resize Text | AA | [ ] 200% zoom without loss |
| 1.4.5 Images of Text | AA | [ ] Real text preferred |
| 1.4.10 Reflow | AA | [ ] No horizontal scroll at 320px |
| 1.4.11 Non-text Contrast | AA | [ ] 3:1 for UI components |
| 1.4.12 Text Spacing | AA | [ ] Custom spacing supported |
| 1.4.13 Content on Hover/Focus | AA | [ ] Dismissible, hoverable, persistent |
```

#### Operable

```markdown
## 2. Operable

### 2.1 Keyboard Accessible (Level A)

**Requirement**: All functionality available from keyboard.

- [ ] All interactive elements keyboard accessible
- [ ] No keyboard traps
- [ ] Shortcuts documented (if any)

**Code Audit**:
- [ ] All clickable elements have keyboard handlers
- [ ] Focus can move in and out of all components
- [ ] Modal focus is trapped appropriately

**Finding**: [PASS/WARN/FAIL]

### 2.2 Enough Time (Level A/AA)

**Requirement**: Users have enough time to read/use content.

- [ ] Time limits adjustable or can be turned off
- [ ] Auto-updating content can be paused
- [ ] Session timeouts warned with extension option

**Finding**: [PASS/WARN/FAIL/N/A]

### 2.3 Seizures and Physical Reactions (Level A)

**Requirement**: Content doesn't cause seizures.

- [ ] No content flashes more than 3 times/second
- [ ] Animation can be paused/disabled

**Finding**: [PASS/WARN/FAIL]

### 2.4 Navigable (Level A/AA)

| Criterion | Level | Status |
|-----------|-------|--------|
| 2.4.1 Bypass Blocks | A | [ ] Skip links provided |
| 2.4.2 Page Titled | A | [ ] Descriptive page titles |
| 2.4.3 Focus Order | A | [ ] Logical focus sequence |
| 2.4.4 Link Purpose | A | [ ] Link text describes destination |
| 2.4.5 Multiple Ways | AA | [ ] Multiple navigation methods |
| 2.4.6 Headings/Labels | AA | [ ] Descriptive headings |
| 2.4.7 Focus Visible | AA | [ ] Visible focus indicators |

### 2.5 Input Modalities (Level A/AA)

| Criterion | Level | Status |
|-----------|-------|--------|
| 2.5.1 Pointer Gestures | A | [ ] Simple pointer alternative |
| 2.5.2 Pointer Cancellation | A | [ ] Up-event for activation |
| 2.5.3 Label in Name | A | [ ] Accessible name contains visible text |
| 2.5.4 Motion Actuation | A | [ ] Motion not required |
```

#### Understandable

```markdown
## 3. Understandable

### 3.1 Readable (Level A/AA)

- [ ] Language of page specified
- [ ] Language of parts specified (if mixed)
- [ ] Unusual words explained

**Finding**: [PASS/WARN/FAIL]

### 3.2 Predictable (Level A/AA)

- [ ] No unexpected context changes on focus
- [ ] No unexpected context changes on input
- [ ] Consistent navigation across pages
- [ ] Consistent identification of components

**Finding**: [PASS/WARN/FAIL]

### 3.3 Input Assistance (Level A/AA)

| Criterion | Level | Status | UXQ Alignment |
|-----------|-------|--------|---------------|
| 3.3.1 Error Identification | A | [ ] | UXQ-005 |
| 3.3.2 Labels/Instructions | A | [ ] | - |
| 3.3.3 Error Suggestion | AA | [ ] | UXQ-005 |
| 3.3.4 Error Prevention | AA | [ ] | UXQ-003 |

**UXQ-005 Compliance** (Error Empathy):
- [ ] Errors explain what went wrong in user terms
- [ ] Errors suggest how to fix
- [ ] Errors don't blame user
```

#### Robust

```markdown
## 4. Robust

### 4.1 Compatible (Level A/AA)

- [ ] Valid HTML (parsing)
- [ ] Name, role, value for custom components
- [ ] Status messages announced without focus

**Code Audit**:
- [ ] Custom components use appropriate ARIA
- [ ] ARIA roles match behavior
- [ ] Live regions used for dynamic updates
```

### 4. Assistive Technology Testing

```markdown
## Assistive Technology Compatibility

### Screen Reader Testing

| Screen Reader | Browser | Status | Notes |
|---------------|---------|--------|-------|
| VoiceOver | Safari | [ ] | Primary Mac/iOS |
| NVDA | Chrome | [ ] | Primary Windows |
| JAWS | Chrome | [ ] | Enterprise |
| TalkBack | Chrome | [ ] | Android |

### Key Interactions to Test

| Action | Expected Announcement | Status |
|--------|----------------------|--------|
| Page load | "[Page title] loaded" | [ ] |
| Form error | "Error: [field] [message]" | [ ] |
| Success | "[Action] completed" | [ ] |
| Modal open | "[Modal title] dialog" | [ ] |
| Modal close | Focus returns to trigger | [ ] |

### Keyboard-Only Navigation

| Flow | Keyboard Path | Status |
|------|---------------|--------|
| [User journey 1] | [key sequence] | [ ] |
| [User journey 2] | [key sequence] | [ ] |
```

### 5. Empowerment Framing (UXQ-010)

```markdown
## Accessibility as Empowerment

### Who Benefits

| User Group | Challenge | How We Empower |
|------------|-----------|----------------|
| Blind users | Can't see UI | Full screen reader support, meaningful descriptions |
| Low vision | Difficulty reading | High contrast, zoom support, text sizing |
| Motor impaired | Can't use mouse | Complete keyboard access, large targets |
| Deaf/HoH | Can't hear audio | Captions, visual alerts, transcripts |
| Cognitive | Processing difficulty | Clear language, consistent patterns, error help |
| Temporary | Situational limits | One-hand use, outdoor visibility, quiet mode |

### Beyond Compliance

Instead of just meeting WCAG, we actively empower by:
- [ ] Providing multiple ways to accomplish tasks
- [ ] Anticipating user needs proactively
- [ ] Making accessibility features discoverable
- [ ] Testing with actual users with disabilities
```

### 6. Generate Audit Report

```markdown
# Accessibility Audit Report

**Feature**: [spec path]
**Date**: [DATE]
**Target Level**: WCAG 2.1 [AA/AAA]
**Mode**: [SPEC_AUDIT/CODE_AUDIT]
**Auditor**: Claude Code (accessibility-audit skill)

## Executive Summary

**Overall Compliance**: [PASS/CONCERNS/FAIL]
**Level A**: [X/Y criteria met]
**Level AA**: [X/Y criteria met]
**Level AAA**: [X/Y criteria met] (if targeted)

## Compliance by Principle

| Principle | Criteria | Passed | Failed | Warnings |
|-----------|----------|--------|--------|----------|
| Perceivable | [N] | [N] | [N] | [N] |
| Operable | [N] | [N] | [N] | [N] |
| Understandable | [N] | [N] | [N] | [N] |
| Robust | [N] | [N] | [N] | [N] |

## Critical Issues

### [ISSUE-001]: [Title]
- **WCAG Criterion**: [X.X.X]
- **Level**: [A/AA/AAA]
- **Location**: [component/screen]
- **Impact**: [who is affected]
- **Recommendation**: [fix]
- **Empowerment View**: [how fixing empowers users]

## Recommendations

### Must Fix (Level A failures)
1. [Issue with fix]

### Should Fix (Level AA failures)
1. [Issue with fix]

### Enhance (Beyond compliance)
1. [Opportunity to better empower users]

## Testing Checklist

- [ ] Keyboard navigation test
- [ ] Screen reader test (VoiceOver/NVDA)
- [ ] Color contrast verification
- [ ] Zoom to 200% test
- [ ] Motion/animation preferences
- [ ] Mobile accessibility test

## UXQ-010 Assessment

**Empowerment Score**: [1-5]
- 1: Compliance-focused only
- 3: Meets requirements, some empowerment
- 5: Proactively empowers all users

**Evidence**: [how we go beyond compliance]
```

## Output

1. Audit report (inline or saved to `specs/[feature]/accessibility-audit.md`)
2. Compliance summary by WCAG level
3. Prioritized issues list
4. UXQ-010 empowerment assessment

## Integration with Spec Kit

Feeds into:
- `/speckit.specify` → Accessibility requirements
- `/speckit.analyze` → UXQ compliance (Pass X)
- `/speckit.implement` → Developer a11y requirements
- UX Designer persona → Inclusive design guidance
