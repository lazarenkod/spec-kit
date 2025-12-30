# {FOUNDATION_NAME} Design

> UX Foundation: {FOUNDATION_ID} | Generated from concept.md

## Traceability

| Source | Reference |
|--------|-----------|
| UX Foundation | UXF-{FOUNDATION} |
| Journeys | {journey_references} |
| Concept Features | {feature_references} |

---

## Scenario Inventory

| Scenario ID | Name | Priority | Journey Touchpoints |
|-------------|------|----------|---------------------|
| UXF-{FOUNDATION}-001 | {scenario_name} | Critical | J000 (step 2), J002 (step 5) |
| UXF-{FOUNDATION}-002 | {scenario_name} | High | J000 (step 3) |
| UXF-{FOUNDATION}-003 | {scenario_name} | Medium | J001 (step 1) |
<!-- Add more scenarios from concept.md -->

---

## Scenario Designs

### UXF-{FOUNDATION}-001: {Scenario Name}

**Description**: {scenario_description}
**Trigger**: {when_this_scenario_occurs}
**User Goal**: {what_user_wants_to_achieve}

#### Screen: {screen_name}

```text
┌────────────────────────────────────────────────────────────┐
│ {Header / Nav Bar}                                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                                                      │  │
│  │  [Main Content / Form / Component]                   │  │
│  │                                                      │  │
│  │                                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  ┌───────────────┐  ┌───────────────┐                      │
│  │ Primary CTA   │  │ Secondary     │                      │
│  └───────────────┘  └───────────────┘                      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

#### State Variations

| State | Trigger | Visual Changes | User Action |
|-------|---------|----------------|-------------|
| Default | Page load | Standard view | Can interact |
| Loading | Action in progress | Spinner, disabled inputs | Wait |
| Success | Action completed | Confirmation message, redirect | Continue |
| Error | Action failed | Error message, retry option | Fix and retry |
| Empty | No data | Empty state illustration, CTA | Create first item |

#### Component Specifications

**{Component Name}**

| Property | Value |
|----------|-------|
| Purpose | {why_this_component_exists} |
| Variants | {list_of_variants} |
| States | default, hover, focus, disabled, loading, error |
| Accessibility | {a11y_requirements} |

```yaml
component: {ComponentName}
props:
  variant: "primary" | "secondary" | "ghost"
  size: "sm" | "md" | "lg"
  disabled: boolean
  loading: boolean

accessibility:
  role: "button" | "link" | ...
  aria-label: "{descriptive_label}"
  keyboard: "Enter/Space to activate"
  focus-visible: true
```

#### Responsive Behavior

| Breakpoint | Layout Changes |
|------------|----------------|
| Mobile (< 640px) | {mobile_specific_changes} |
| Tablet (640-1024px) | {tablet_changes} |
| Desktop (> 1024px) | {desktop_layout} |

---

### UXF-{FOUNDATION}-002: {Scenario Name}

<!-- Repeat the same structure for each scenario -->

**Description**: {scenario_description}
**Trigger**: {when_this_scenario_occurs}
**User Goal**: {what_user_wants_to_achieve}

#### Screen: {screen_name}

```text
<!-- Wireframe here -->
```

#### State Variations

| State | Trigger | Visual Changes | User Action |
|-------|---------|----------------|-------------|
<!-- States table -->

---

## Accessibility Requirements

### WCAG Compliance

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 1.3.1 Info and Relationships | Form labels properly associated | Use `htmlFor` or `aria-labelledby` |
| 1.4.3 Contrast | 4.5:1 for normal text, 3:1 for large | Use design system colors |
| 2.1.1 Keyboard | All interactive elements reachable | Logical tab order, visible focus |
| 2.4.6 Headings | Descriptive headings | Use semantic heading hierarchy |
| 4.1.2 Name, Role, Value | Programmatically determinable | Use semantic HTML, ARIA when needed |

### Screen Reader Announcements

| Action | Announcement |
|--------|--------------|
| Form validation error | "Error: {field_name}, {error_message}" |
| Success state | "Success: {action_completed}" |
| Loading state | "Loading, please wait" |
| Dialog open | "Dialog opened: {dialog_title}" |

---

## Animation & Transitions

Reference: [templates/shared/animation-presets/micro-interactions.md](../shared/animation-presets/micro-interactions.md)

| Element | Animation | Duration | Easing |
|---------|-----------|----------|--------|
| Form validation | Shake + border color | 300ms | spring |
| Success feedback | Fade in + scale | 200ms | ease-out |
| Modal open | Scale up + backdrop | 200ms | ease-out |
| Loading spinner | Rotate | 1000ms | linear |

---

## Error Handling

### Error States

| Error Type | Visual Treatment | Recovery Action |
|------------|------------------|-----------------|
| Validation | Inline error message, red border | Fix input |
| Network | Toast notification | Retry button |
| Permission | Alert dialog | Request permission |
| System | Full-page error | Contact support |

### Error Messages

| Context | Message Pattern | Example |
|---------|-----------------|---------|
| Required field | "{Field} is required" | "Email is required" |
| Invalid format | "Please enter a valid {field}" | "Please enter a valid email" |
| Server error | "Something went wrong. Please try again." | - |
| Unauthorized | "Please sign in to continue." | - |

---

## Component List

Components used in this foundation design:

| Component | Usage | Shared/Specific |
|-----------|-------|-----------------|
| Button | Primary/secondary actions | Shared |
| Input | Form fields | Shared |
| Toast | Feedback messages | Shared |
| {FoundationSpecificComponent} | {usage} | Specific |

---

## Design Quality Score (DQS)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Scenario Coverage | {score}/100 | All UXF-{FOUNDATION}-xxx designed |
| State Completeness | {score}/100 | All states defined |
| Accessibility | {score}/100 | WCAG AA compliance |
| Responsiveness | {score}/100 | All breakpoints covered |
| Traceability | {score}/100 | Linked to journeys/features |
| **Overall DQS** | **{total_score}/100** | |
