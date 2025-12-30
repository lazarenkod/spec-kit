# Persona to Interaction Patterns

Map JTBD-enhanced personas from concept.md to specific interaction patterns and design decisions.

## Input: Persona Structure from Concept

```yaml
persona:
  id: P01
  name: "Busy Professional"
  jtbd:
    - "When I have limited time, I want to complete tasks quickly, so I don't fall behind"
    - "When I'm multitasking, I want clear status updates, so I know what's happening"
  pain_points:
    - "Complex interfaces that require learning"
    - "Slow loading times during peak hours"
  device_preference: mobile > desktop
  tech_savviness: high
  frequency: daily
  session_length: "2-5 minutes"
```

## Mapping Algorithm

### Step 1: JTBD → Interaction Principles

```text
FOR each jtbd IN persona.jtbd:

  1. PARSE: "When {context}, I want {action}, so {outcome}"

  2. MAP to interaction principles:

     | JTBD Context | Design Principle |
     |--------------|------------------|
     | "limited time" | Minimize steps, progressive disclosure |
     | "multitasking" | Persistent status, non-blocking actions |
     | "on the go" | Touch-friendly, offline support |
     | "uncertain" | Clear feedback, undo support |
     | "first time" | Guided experience, tooltips |
     | "routine task" | Shortcuts, keyboard navigation |
     | "important decision" | Confirmation, review states |
     | "collaborative work" | Real-time sync, presence indicators |

  3. OUTPUT: interaction_principles
```

### Step 2: Pain Points → Anti-Patterns

```text
FOR each pain_point IN persona.pain_points:

  1. IDENTIFY design anti-patterns to avoid:

     | Pain Point | Anti-Pattern to Avoid |
     |------------|----------------------|
     | "Complex interfaces" | Deep nesting, hidden actions |
     | "Slow loading" | Blocking spinners, large bundles |
     | "Inconsistent behavior" | Platform-specific patterns |
     | "Information overload" | Dense layouts, no hierarchy |
     | "Unclear errors" | Technical jargon, no recovery path |
     | "Manual repetition" | No defaults, no bulk actions |
     | "Context switching" | Multiple tabs, external links |
     | "Data loss fear" | No auto-save, no drafts |

  2. OUTPUT: anti_patterns
```

### Step 3: Device Preference → Layout Strategy

```text
ANALYZE persona.device_preference:

| Preference | Layout Strategy |
|------------|-----------------|
| mobile > desktop | Mobile-first, touch targets, bottom navigation |
| desktop > mobile | Dense layouts, keyboard shortcuts, side panels |
| tablet primary | Flexible grid, split views, touch + keyboard |
| mixed/equal | Responsive breakpoints, feature parity |

OUTPUT: layout_strategy
```

### Step 4: Tech Savviness → Complexity Level

```text
ANALYZE persona.tech_savviness:

| Level | Interaction Complexity |
|-------|------------------------|
| low | Simple flows, explicit labels, minimal options |
| medium | Standard patterns, some advanced features hidden |
| high | Power user features, keyboard shortcuts, customization |
| expert | CLI options, API access, automation support |

OUTPUT: complexity_level
```

### Step 5: Session Characteristics → UX Optimizations

```text
ANALYZE persona.frequency AND persona.session_length:

| Pattern | UX Optimization |
|---------|-----------------|
| daily + short (< 5 min) | Quick actions, recent items, shortcuts |
| daily + long (> 30 min) | Workspace memory, focus modes, autosave |
| weekly + medium | Onboarding reminders, change highlights |
| monthly + long | Re-onboarding, guided tours, what's new |
| infrequent + short | Simple flows, no learning curve |

OUTPUT: session_optimizations
```

## Output: Persona Design Profile

```markdown
## Design Profile: {Persona Name}

### Interaction Principles
1. {principle_1}
2. {principle_2}
3. {principle_3}

### Layout Strategy
- **Primary Device**: {device}
- **Breakpoint Priority**: {mobile | tablet | desktop}
- **Navigation Pattern**: {bottom_nav | sidebar | header}

### Complexity Level
- **Default Mode**: {simplified | standard | advanced}
- **Progressive Disclosure**: {yes | no}
- **Shortcut Support**: {none | basic | comprehensive}

### Session Optimizations
- **Quick Start**: {recent_items | favorites | search}
- **State Persistence**: {auto_save_interval}
- **Exit Behavior**: {confirm | auto_save | draft}

### Anti-Patterns to Avoid
- ❌ {anti_pattern_1}
- ❌ {anti_pattern_2}
- ❌ {anti_pattern_3}

### Component Recommendations
| Component | Recommendation |
|-----------|----------------|
| Button | {size, position, feedback} |
| Form | {layout, validation timing} |
| Navigation | {type, depth, mobile variant} |
| Feedback | {toast vs inline, duration} |
```

## Example: Full Mapping

### Input (from concept.md)

```yaml
P01: Busy Professional
  jtbd:
    - "When I have 5 minutes between meetings, I want to check status, so I stay informed"
    - "When something needs my attention, I want clear notifications, so I don't miss it"
  pain_points:
    - "Slow-loading dashboards"
    - "Too many clicks to complete simple tasks"
  device_preference: mobile > desktop
  tech_savviness: high
  frequency: daily
  session_length: "2-5 minutes"
```

### Output

```markdown
## Design Profile: Busy Professional

### Interaction Principles
1. **Glanceable information**: Dashboard shows key metrics at first sight
2. **One-tap actions**: Primary actions accessible without drilling down
3. **Smart notifications**: Priority-based, actionable, non-intrusive
4. **Offline-capable**: Core reads work without network

### Layout Strategy
- **Primary Device**: Mobile
- **Breakpoint Priority**: Mobile → Desktop (no tablet optimization)
- **Navigation Pattern**: Bottom navigation (4-5 items max)

### Complexity Level
- **Default Mode**: Standard with power-user shortcuts
- **Progressive Disclosure**: Yes (advanced options in overflow menu)
- **Shortcut Support**: Comprehensive (swipe gestures, long-press)

### Session Optimizations
- **Quick Start**: Most recent item + pending actions
- **State Persistence**: Auto-save every 30 seconds
- **Exit Behavior**: Background sync, no confirmation needed

### Anti-Patterns to Avoid
- ❌ Full-page loading spinners
- ❌ Multi-step wizards for simple actions
- ❌ Desktop-only features
- ❌ Notification overload

### Component Recommendations
| Component | Recommendation |
|-----------|----------------|
| Button | Large touch targets (48px), haptic feedback |
| Form | Single-column, inline validation, smart defaults |
| Navigation | Bottom bar, 4 items + More, swipe between sections |
| Feedback | Toast with undo, 3s duration, stack max 2 |
```

## Integration with Design Process

```text
1. FOR each persona IN concept.personas:
     RUN persona-to-patterns.md algorithm
     OUTPUT design_profile

2. WHEN designing screens:
     CHECK primary persona for this journey/feature
     APPLY design profile principles
     VALIDATE against anti-patterns

3. IN component specifications:
     REFERENCE persona recommendations
     DOCUMENT trade-offs for multi-persona features
```
