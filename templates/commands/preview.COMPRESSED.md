---
description: Generate interactive previews from design specifications
persona: product-designer-agent
handoffs:
  - label: Implement Feature
    agent: speckit.implement
    auto: false
  - label: Update Design
    agent: speckit.design
    auto: false
preview_config:
  port: 3456
  output_dir: ".preview"
  auto_open: true
claude_code:
  model: opus
  reasoning_mode: extended
  thinking_budget: 6000
---

## Input
```text
$ARGUMENTS
```

---

## Purpose

Generates **interactive visual previews** from design specifications:
1. Converts ASCII wireframes → visual HTML
2. Generates production-ready components via v0.dev
3. Captures Playwright screenshots for all states/viewports
4. Validates design quality (DQS)
5. Auto-generates Storybook stories

**When to use**: After `/speckit.design`, before `/speckit.implement`

---

## Preview Types

| Type | Input | Output | Use Case |
|------|-------|--------|----------|
| Wireframe | ASCII in design.md | Visual HTML | Layout validation |
| Component | Component spec | Interactive React | State/variant testing |
| Flow | Screen flow | Multi-page demo | Journey validation |
| Animation | Motion spec | Animated preview | Timing review |
| Mockup | Stitch-generated | Comparison gallery | High-fidelity validation |

---

## Workflow (8 Steps)

### Step 0: Load Configuration

```text
READ constitution.md → design_system.preset, framework, language
READ design.md → tokens, components, flows, motion specs

DETERMINE preview_scope:
  component:{name} | screen:{name} | flow:{name} | all
```

### Step 1: Wireframe to Visual Conversion

```text
FOR EACH wireframe IN design.md:
  1. Parse ASCII structure (regions, placeholders, hierarchy)
  2. Map to HTML structure
  3. Apply design tokens (--background, --spacing-X)
  4. OUTPUT: .preview/wireframes/{screen_name}.html
```

### Step 2: Component Preview Generation

```text
FOR EACH component IN design.md:
  1. Extract states (default, hover, active, focus, disabled, loading, error)
  2. Extract variants (primary, secondary, ghost) and sizes (sm, md, lg)
  3. Generate via v0.dev (if complex) or template
  4. Create preview wrapper with state toggles

  OUTPUT:
    .preview/components/{name}/
    ├── {name}.tsx
    ├── {name}.stories.tsx
    └── preview.html
```

### Step 3: Flow Preview Generation

```text
FOR EACH flow IN design.md (Mermaid diagrams):
  1. Parse flow graph (nodes = screens, edges = navigation)
  2. Generate page per node with navigation buttons
  3. Create flow runner with state persistence

  OUTPUT: .preview/flows/{flow_name}/index.html + screens
```

### Step 4: Animation Preview

```text
FOR EACH animation IN design.md:
  1. Parse: duration, easing, keyframes, trigger
  2. Generate CSS @keyframes
  3. Create demo with play/pause, speed control, stepping

  OUTPUT: .preview/animations/{name}.html
```

### Step 5: Stitch Mockup Gallery (if exists)

```text
IF .preview/stitch-mockups/ exists:
  1. Scan for mockups (html, css, screenshots, figma JSON)
  2. Generate side-by-side comparison pages (wireframe vs mockup)
  3. Create gallery index with filtering

  OUTPUT:
    .preview/mockup-comparisons/{feature}/{screen}.html
    .preview/stitch-mockups/gallery.html
```

### Step 6: Screenshot Capture

```text
viewports = [mobile(375), tablet(768), desktop(1440)]
themes = [light, dark]

FOR EACH preview × viewport × theme:
  Playwright → .preview/screenshots/{name}_{viewport}_{theme}.png

FOR EACH component × state:
  Trigger state → capture → .preview/screenshots/{component}_{state}.png
```

### Step 7: Design Quality Score (DQS)

| Category | Points | Checks |
|----------|--------|--------|
| Visual Quality | 40 | Contrast, typography hierarchy, spacing consistency |
| Accessibility | 30 | ARIA labels, keyboard nav, focus indicators |
| Consistency | 20 | Token usage, pattern adherence |
| Implementation | 10 | TypeScript, code quality |

```text
Grade: A (≥90) | B (≥80) | C (≥70) | D (≥60) | F (<60)
Status: score ≥ 80 → Production Ready
```

### Step 8: Preview Server

```text
1. Start HTTP server on port 3456 (or find available)
2. Generate index.html with links to all previews
3. Open browser (if auto_open)

OUTPUT: http://localhost:{port}
```

---

## CLI Flags

| Flag | Description |
|------|-------------|
| `--component X` | Preview specific component |
| `--screen X` | Preview specific screen |
| `--no-screenshots` | Skip screenshot capture |
| `--no-validation` | Skip DQS validation |
| `--storybook-only` | Generate Storybook only |
| `--port N` | Specify port |
| `--no-open` | Don't auto-open browser |
| `--theme dark` | Dark mode only |
| `--viewport mobile` | Specific viewport only |
| `--mockups` | Serve Stitch mockups gallery |

---

## Quality Gates

| Gate | Check |
|------|-------|
| Wireframes Converted | All wireframes → HTML |
| Components Generated | All components have preview files |
| Screenshots Captured | All states × viewports captured |
| DQS Calculated | Score available |
| Server Accessible | Preview server running |

---

## Output Format

```text
┌─────────────────────────────────────────────────────────────┐
│ /speckit.preview Complete                                    │
├─────────────────────────────────────────────────────────────┤
│ Output: .preview/                                            │
│                                                              │
│ Generated:                                                   │
│   Wireframes: {n}  Components: {n}  Flows: {n}              │
│   Animations: {n}  Mockups: {n}  Screenshots: {n}           │
│                                                              │
│ Design Quality Score:                                        │
│   Visual: {x}/40  Accessibility: {x}/30                     │
│   Consistency: {x}/20  Implementation: {x}/10               │
│   Total: {x}/100  Grade: {A-F}                              │
│                                                              │
│ Status: {Production Ready | Needs Work}                     │
│                                                              │
│ Preview: http://localhost:{port}                            │
└─────────────────────────────────────────────────────────────┘
```

### Next Steps

| Condition | Action |
|-----------|--------|
| DQS ≥ 80 | → `/speckit.implement` |
| DQS < 80 | → Fix issues, `/speckit.design`, re-run preview |

---

## Dependencies

```json
{
  "playwright": "^1.40.0",
  "@storybook/react": "^7.6.0",
  "vite": "^5.0.0"
}
```

Missing dependencies → HTML previews still work, skip screenshots/Storybook

---

## Context

{ARGS}
