---
description: Create text-based wireframe specifications with layout, hierarchy, and responsive annotations
---

## User Input

```text
$ARGUMENTS
```

## Purpose

This skill creates detailed text-based wireframe specifications using ASCII diagrams and structured annotations. Provides developers with clear layout guidance without requiring visual design tools.

## When to Use

- After `/speckit.specify` to visualize UI structure
- When communicating layout to developers
- Before implementation to align on structure
- When visual design tools are not available

## Execution Steps

### 1. Identify Screens/Views

Parse from user input or spec:

```text
1. Read spec.md for UI requirements
2. Read user flows from interaction spec (if exists)
3. Identify screens to wireframe:
   - Entry points (landing, login)
   - Core feature screens
   - Supporting screens (settings, help)
   - Error and empty states
4. Map screen relationships
```

### 2. Define Information Architecture

For each screen:

```markdown
## Screen: [Name]

**URL/Route**: [path]
**User Goal**: [JTBD this screen serves]
**Entry Points**: [How user arrives]
**Exit Points**: [Where user can go]

### Information Hierarchy

1. **Primary** (immediate attention)
   - [Most important element/action]

2. **Secondary** (supporting)
   - [Context and details]

3. **Tertiary** (available but not prominent)
   - [Advanced options, secondary actions]

### Content Inventory

| Element | Type | Content | Required |
|---------|------|---------|----------|
| [name] | heading/text/image/etc | [content] | yes/no |
```

### 3. Create ASCII Wireframes

Use consistent notation:

```text
NOTATION GUIDE:
+------------------+  Box = Container/Section
|                  |
+------------------+

[Button Text]         Square brackets = Button/Action
(Link Text)           Parentheses = Link
<Input Field>         Angle brackets = Input
{Dropdown ▼}          Braces = Select/Dropdown
[●] Option            Radio button
[✓] Option            Checkbox
─────────────         Horizontal rule/divider
│                     Vertical divider
...                   Truncated content
→                     Navigation/flow direction
```

### 4. Wireframe Template

```markdown
## Wireframe: [Screen Name]

### Desktop Layout (>1024px)

```
+------------------------------------------------------------------+
|  [Logo]                    (Nav 1) (Nav 2) (Nav 3)    [Profile ▼] |
+------------------------------------------------------------------+
|                                                                    |
|  +------------------------+  +----------------------------------+  |
|  |                        |  |                                  |  |
|  |  # Page Title          |  |  Secondary Content Area          |  |
|  |                        |  |                                  |  |
|  |  Description text      |  |  - Item 1                        |  |
|  |  explaining context    |  |  - Item 2                        |  |
|  |                        |  |  - Item 3                        |  |
|  |  <Primary Input     >  |  |                                  |  |
|  |  <Secondary Input   >  |  |  +------------------------------+|  |
|  |                        |  |  |  Nested Component            ||  |
|  |  [Primary Action    ]  |  |  +------------------------------+|  |
|  |  (Secondary Link)      |  |                                  |  |
|  |                        |  |                                  |  |
|  +------------------------+  +----------------------------------+  |
|                                                                    |
+------------------------------------------------------------------+
|  Footer: (Link) (Link) (Link)                    © 2025 Company   |
+------------------------------------------------------------------+
```

### Mobile Layout (<640px)

```
+---------------------------+
|  [☰]  [Logo]    [Profile] |
+---------------------------+
|                           |
|  # Page Title             |
|                           |
|  Description text         |
|  explaining context       |
|                           |
|  <Primary Input        >  |
|  <Secondary Input      >  |
|                           |
|  [    Primary Action    ] |
|                           |
|  ─────────────────────── |
|                           |
|  Secondary Content        |
|  - Item 1                 |
|  - Item 2                 |
|  - Item 3                 |
|                           |
+---------------------------+
```

### Annotations

| # | Element | Notes |
|---|---------|-------|
| 1 | Logo | Links to home, 120x40px max |
| 2 | Primary Input | Auto-focus on load |
| 3 | Primary Action | Disabled until form valid |
```

### 5. Define Responsive Behavior

```markdown
### Responsive Breakpoints

| Breakpoint | Width | Layout Changes |
|------------|-------|----------------|
| Mobile | <640px | Single column, hamburger nav |
| Tablet | 640-1024px | 2 columns, condensed nav |
| Desktop | >1024px | Full layout, expanded nav |

### Element Behavior

| Element | Mobile | Tablet | Desktop |
|---------|--------|--------|---------|
| Navigation | Hamburger menu | Icons only | Full text |
| Sidebar | Hidden (drawer) | Collapsed | Visible |
| Grid | 1 column | 2 columns | 3 columns |
| Images | Full width | 50% | 33% |

### Touch Considerations

- Tap targets: minimum 44x44px
- Swipe: [supported gestures]
- Pull-to-refresh: [if applicable]
```

### 6. Document Component Patterns

```markdown
### Reusable Patterns

#### Card Pattern
```
+---------------------------+
|  [Image/Icon]             |
|  ## Title                 |
|  Meta info | Date         |
|  Description text...      |
|  (Action) (Action)        |
+---------------------------+
```
Used in: [list screens]

#### Form Pattern
```
+---------------------------+
|  Label                    |
|  <Input                >  |
|  Helper text              |
|                           |
|  Label                    |
|  <Input                >  |
|  ⚠ Error message          |
|                           |
|  [Submit]  (Cancel)       |
+---------------------------+
```
Used in: [list screens]

#### Empty State Pattern
```
+---------------------------+
|                           |
|      [Illustration]       |
|                           |
|  ## No Items Yet          |
|  Helpful text explaining  |
|  what to do next          |
|                           |
|  [Create First Item]      |
|                           |
+---------------------------+
```
Used in: [list screens when empty]
```

### 7. Generate Wireframe Document

Create `specs/[feature]/wireframes.md`:

```markdown
# Wireframe Specification: [Feature]

**Spec**: [spec.md path]
**Date**: [DATE]
**Author**: Claude Code (wireframe-spec skill)

## Screen Map

```
[Login] → [Dashboard] → [Detail View]
              ↓
         [Settings]
```

## Screen Count: [N]

| Screen | Priority | Status |
|--------|----------|--------|
| [Name] | P1 | ✓ Wireframed |

---

## Screens

### 1. [Screen Name]

[Full wireframe with all layouts and annotations]

---

### 2. [Screen Name]

[Full wireframe]

---

## Component Library

[Reusable patterns]

## Responsive Matrix

[Full breakpoint behavior]

## Design Tokens Reference

| Token | Value | Usage |
|-------|-------|-------|
| spacing-xs | 4px | Inline elements |
| spacing-sm | 8px | Related elements |
| spacing-md | 16px | Section padding |
| spacing-lg | 24px | Major sections |
| spacing-xl | 48px | Page sections |

## Developer Notes

- Framework: [recommended CSS framework if any]
- Grid system: [columns, gutters]
- Z-index layers: [modal, dropdown, tooltip, etc.]
```

## Output

1. Wireframe spec saved to `specs/[feature]/wireframes.md`
2. Screen count and coverage summary
3. Component patterns identified
4. Recommended next: `/speckit.interaction-design` or implementation

## Integration with Spec Kit

Feeds into:
- `/speckit.plan` → UI architecture decisions
- `/speckit.implement` → Developer layout guide
- UX Designer persona → Design deliverables
- `/speckit.analyze` → Validate all screens covered
