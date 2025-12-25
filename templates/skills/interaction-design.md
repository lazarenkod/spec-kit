---
description: Define component interaction patterns, states, and behaviors for specification
---

## User Input

```text
$ARGUMENTS
```

## Purpose

This skill creates detailed interaction specifications for UI components, defining all states, transitions, feedback patterns, and accessibility behaviors. Produces developer-ready interaction documentation.

## When to Use

- After `/speckit.specify` to detail UI interactions
- When designing new components or patterns
- Before implementation to align on behaviors
- When reviewing existing interactions for consistency

## Execution Steps

### 1. Identify Components

Parse from user input or spec:

```text
1. Read spec.md for UI requirements (FR-UI-xxx)
2. Identify interactive components:
   - Forms and inputs
   - Buttons and actions
   - Navigation elements
   - Modals and overlays
   - Lists and data displays
   - Feedback elements
3. Prioritize by user journey criticality
```

### 2. Define Component States

For each component, document all states:

```markdown
## Component: [Name]

**Type**: [Button/Input/Modal/etc.]
**Purpose**: [What user achieves]
**JTBD**: [Which job this serves]

### State Matrix

| State | Visual Appearance | Trigger | Behavior | Duration |
|-------|-------------------|---------|----------|----------|
| Default | [description] | Initial load | [none] | - |
| Hover | [description] | Mouse enter | [feedback] | Instant |
| Focus | [description] | Tab/Click | [outline] | While focused |
| Active | [description] | Mouse down | [pressed] | While pressed |
| Loading | [description] | Action initiated | [spinner/progress] | Until complete |
| Success | [description] | Action complete | [confirmation] | 2-3 seconds |
| Error | [description] | Validation fail | [message] | Until resolved |
| Disabled | [description] | Condition unmet | [no interaction] | Until enabled |

### State Transitions

```mermaid
stateDiagram-v2
    [*] --> Default
    Default --> Hover: mouse enter
    Hover --> Default: mouse leave
    Hover --> Active: mouse down
    Active --> Loading: action
    Loading --> Success: complete
    Loading --> Error: fail
    Success --> Default: timeout
    Error --> Default: user fixes
```
```

### 3. Define Micro-Interactions

Document feedback patterns:

```markdown
### Micro-Interactions

#### On Action Initiation
- **Visual**: [what changes]
- **Motion**: [animation type, duration, easing]
- **Sound**: [if applicable]
- **Haptic**: [if mobile]

#### On Success
- **Visual**: [success indicator]
- **Motion**: [celebration animation]
- **Message**: [confirmation text]
- **Next Step**: [where focus goes]

#### On Error
- **Visual**: [error indicator]
- **Motion**: [attention draw]
- **Message**: [helpful error text - UXQ-005]
- **Recovery**: [what user can do]

#### Reduced Motion Alternative
- **Default animation**: [full animation]
- **prefers-reduced-motion**: [simplified version]
```

### 4. Define Input Behaviors

For form inputs:

```markdown
### Input: [Field Name]

**Type**: [text/email/password/select/etc.]
**Purpose**: [what data is collected]

#### Validation
| Rule | Trigger | Message |
|------|---------|---------|
| Required | On blur (empty) | "[Field] is required" |
| Format | On change (debounced) | "Please enter a valid [type]" |
| Length | On change | "Must be [X-Y] characters" |
| Custom | [trigger] | [message] |

#### Auto-Behaviors
- Auto-format: [e.g., phone number formatting]
- Auto-complete: [browser autocomplete attribute]
- Auto-focus: [when to auto-focus]
- Auto-advance: [move to next field when complete]

#### Keyboard Support
- Enter: [action]
- Escape: [action]
- Tab: [next element]
- Arrows: [for selects/sliders]

#### Accessibility
- Label: [associated label]
- Description: [aria-describedby]
- Error: [aria-invalid, aria-errormessage]
- Required: [aria-required]
```

### 5. Define Navigation Patterns

```markdown
### Navigation: [Pattern Name]

**Context**: [where this applies]

#### Keyboard Navigation
| Key | Action |
|-----|--------|
| Tab | Move to next interactive element |
| Shift+Tab | Move to previous element |
| Enter/Space | Activate current element |
| Escape | Close/Cancel current context |
| Arrow keys | [specific behavior] |

#### Focus Management
- Initial focus: [where focus starts]
- Focus trap: [if modal/overlay, trap focus within]
- Focus return: [where focus goes on close]
- Focus visible: [ensure visible focus indicator]

#### Screen Reader Announcements
| Event | Announcement |
|-------|--------------|
| [event] | "[announcement text]" |
| Page load | "[page title and context]" |
| Error | "[error description]" |
| Success | "[success confirmation]" |
```

### 6. Generate Interaction Spec Document

Create `specs/[feature]/interaction-spec.md`:

```markdown
# Interaction Specification: [Feature]

**Spec**: [spec.md path]
**Date**: [DATE]
**Author**: Claude Code (interaction-design skill)

## Overview

**Feature**: [name]
**Key Interactions**: [count] components documented
**Accessibility Level**: WCAG [2.1 AA/AAA]

## Component Inventory

| Component | Type | States | Priority |
|-----------|------|--------|----------|
| [Name] | [type] | [count] | P1/P2/P3 |

## Detailed Specifications

### [Component 1]
[Full state matrix, transitions, micro-interactions]

### [Component 2]
[Full specification]

## Global Patterns

### Loading States
[Standard loading pattern for this feature]

### Error Handling
[Standard error pattern - UXQ-005 compliant]

### Success Feedback
[Standard success pattern - UXQ-004 delight]

### Empty States
[Empty state pattern - UXQ-006 FTUE]

## Animation Tokens

| Animation | Duration | Easing | Reduced Motion |
|-----------|----------|--------|----------------|
| Fade | 150ms | ease-out | instant |
| Slide | 200ms | ease-in-out | fade |
| Scale | 100ms | ease-out | none |
| Bounce | 300ms | spring | none |

## Accessibility Checklist

- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible
- [ ] Focus order logical
- [ ] Screen reader announcements defined
- [ ] Reduced motion alternatives provided
- [ ] Color not sole indicator
- [ ] Touch targets ≥44px

## Developer Notes

[Implementation hints, library recommendations, gotchas]
```

## Output

1. Interaction spec saved to `specs/[feature]/interaction-spec.md`
2. Component count summary
3. Accessibility checklist status
4. Recommended next: `/speckit.wireframe-spec` or implementation

## Integration with Spec Kit

Feeds into:
- `/speckit.plan` → Component architecture decisions
- `/speckit.implement` → Developer implementation guide
- `/speckit.analyze` → UXQ-003 friction validation
- UX Designer persona → Design deliverables
