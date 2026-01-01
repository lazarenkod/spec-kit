---
description: Create visual specifications, design systems, and mockups
persona: ux-designer-agent
modes:
  feature_design: "Default - spec file exists"
  design_system: "--design-system OR no spec"
  concept_design: "--concept AND concept.md exists"
  mockup_generation: "--mockup AND design artifacts exist"
orchestration:
  agents: [ux-designer-agent, product-designer-agent, motion-designer-agent]
  optional: [promo-designer-agent]
  flow: sequential
handoffs:
  - label: Generate Preview
    agent: speckit.preview
    send: true
  - label: Build Technical Plan
    agent: speckit.plan
  - label: Create Tasks
    agent: speckit.tasks
  - label: Analyze Consistency
    agent: speckit.analyze
  - label: UX Audit
    agent: speckit.analyze
    condition: ["UXQ domain active"]
  - label: Generate Promo Materials
    agent: speckit.design-promo
    condition: ["--promo flag"]
  - label: Continue Next Wave
    agent: speckit.design
    condition: ["MODE == concept_design", "WAVE < total"]
  - label: Retry Failed Mockups
    agent: speckit.design
    condition: ["MODE == mockup_generation", "failed_count > 0"]
claude_code:
  model: opus
  reasoning_mode: extended
  thinking_budget: 8000
  cache_control: {system_prompt: ephemeral, constitution: ephemeral, artifacts: ephemeral}
  semantic_cache: {enabled: true, encoder: all-MiniLM-L6-v2, threshold: 0.95, scope: session}
  plan_mode_trigger: true
skills:
  - interaction-design
  - wireframe-spec
  - wireframe-preview
  - accessibility-audit
  - ux-audit
  - v0-generation
  - component-codegen
  - motion-generation
  - stitch-generation
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-spec
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireSpec
---

## Input
```text
$ARGUMENTS
```

---

## Mode Selection

```text
IF --concept AND concept.md exists:
  MODE = concept_design
  WAVE = --wave N (default 1) | --all
ELIF --mockup AND design_artifacts_exist:
  MODE = mockup_generation
  MOCKUP_MODE = auto | --manual | --reauth
  MOCKUP_SCREENS = --screens "csv" | "all"
  MOCKUP_SCOPE = feature | --all (app)
ELIF --design-system OR no spec file:
  MODE = design_system_generation
ELSE:
  MODE = feature_design
```

---

## Design System Generation Mode

### Brand Inputs

| Type | Field | Example |
|------|-------|---------|
| Required | brand_name | "Acme Corp" |
| Required | primary_color | "#3B82F6" |
| Required | product_type | saas / marketing / mobile / admin |
| Optional | logo_file, secondary_colors, font_preference, style_keywords |

### Product Type Presets

| Type | Spacing | Radius | Shadow | Components |
|------|---------|--------|--------|------------|
| saas | compact (4px) | md (6px) | subtle | DataTable, Dashboard, Sidebar, Charts |
| marketing | generous (8px) | lg (12px) | dramatic | Hero, FeatureGrid, CTABanner, PricingTable |
| mobile | touch (8px) | xl (16px) | elevation | BottomNav, SwipeCard, BottomSheet, FAB |
| admin | compact (4px) | sm (4px) | flat | DataGrid, TreeView, FormBuilder, Breadcrumbs |

### Generation Workflow

```text
Step DS-1: Load preset from product_type
Step DS-2: Generate color palette (50-950 scale + semantic)
Step DS-3: Generate typography (display → caption)
Step DS-4: Generate spacing & layout tokens
Step DS-5: Generate component library (Core → Layout → Feedback → Preset-specific)
Step DS-6: Output files:
  - design-system/tokens.css, tokens.json, tailwind.config.js, theme.ts
  - design-tokens/figma-tokens.json (if Figma enabled)
  - .storybook/ (if Storybook enabled)
```

---

## Concept Design Mode

### Output Structure

```text
specs/app-design/
├── index.md                    # Overview + App-DQS
├── design-system.md            # Global tokens
├── navigation.md               # Sitemap, route map
├── foundations/                # UXF-AUTH/ERROR/LAYOUT/NAV/FTUE/FEEDBACK/ADMIN
├── waves/wave-{N}/             # EPIC-NNN.FNN-design.md
├── journeys/                   # J000-golden-path.md, J001-*.md
├── motion/                     # motion-system.md, transitions.md
└── components/inventory.md     # Master component list
```

### 8-Phase Workflow

| Phase | Agent | Output | When |
|-------|-------|--------|------|
| 0 | - | Validate concept, CQS gate | Always |
| 1 | Product Designer | design-system.md | Wave 1/all |
| 2 | UX Designer | foundations/{foundation}-design.md | Wave 1/all |
| 3 | UX Designer | navigation.md | Wave 1/all |
| 4 | UX Designer | journeys/{journey}-design.md | Wave 1/all |
| 5 | UX/Product | waves/wave-{N}/{feature}-design.md | Per wave |
| 6 | Motion Designer | motion/motion-system.md, transitions.md | Wave 1/all |
| 7 | - | components/inventory.md | Wave 1/all |
| 8 | - | index.md + App-DQS | Always |

### CQS Quality Gate [REF:VG-002]

```text
CQS >= 80 → Proceed (production-quality)
CQS 60-79 → Proceed with warnings
CQS < 60 → Prompt user to continue
```

### App-DQS Formula

```text
App-DQS = design_system × 0.15 + foundations × 0.20 + journeys × 0.20
        + features × 0.30 + traceability × 0.15
```

---

## Mockup Generation Mode

### Prerequisites

- Playwright installed
- Chromium browser
- Design artifacts exist

### 8-Phase Pipeline

| Phase | Action |
|-------|--------|
| 1 | Preflight Check (Playwright, Chromium, artifacts) |
| 2 | Authentication (Google OAuth, session persistence) |
| 3 | Wireframe Discovery (scan specs/app-design/) |
| 4 | Prompt Generation (wireframe → natural language) |
| 5 | Stitch Generation (submit prompts, wait) |
| 6 | Export (HTML, Tailwind, Screenshots, Figma JSON) |
| 7 | Gallery Generation (per-feature indexes) |
| 8 | Fallback (manual mode if automation fails) |

### Output

```text
.preview/stitch-mockups/
├── {screen-name}/
│   ├── index.html          # Generated HTML
│   ├── styles.css          # Tailwind CSS
│   ├── desktop.png         # Screenshot
│   ├── mobile.png          # Mobile screenshot
│   └── figma.json          # Figma-ready JSON
└── gallery.html            # Master gallery
```

### Rate Limits

- Standard: 350/month
- Experimental: 50/month
- Tracked in `.speckit/stitch/usage.json`

---

## Feature Design Mode (Default)

### Workflow (13 Steps)

```text
Step 0.5: Check Figma Import → extract tokens/components
Step 0.75: Library Recommendation → suggest component library

Phase 1 (UX Designer Agent):
  1. Initialize design document
  2. Design Discovery → platform, complexity, a11y tier
  3. Visual Language → colors, typography, spacing, icons
  4. Component Inventory → states, variants, anatomy, a11y
  5. Screen Flow Mapping → journey → screens
  6. Interaction Specifications → triggers, feedback, duration
  7. Accessibility Audit → WCAG checklist
  8. Responsive Strategy → breakpoints, behaviors
  9. Write design.md

Phase 2 (Product Designer Agent):
  10. Visual Language Refinement → tokens, variants
  11. Code Generation (optional) → v0.dev or template

Phase 3 (Motion Designer Agent):
  12. Animation System → tokens, micro-interactions, transitions
  13. Load Animation Presets
```

### Visual Language Tokens

| Category | Tokens |
|----------|--------|
| Colors | primary, secondary, accent, semantic (success/warning/error/info), neutral |
| Typography | display, h1-h6, body, caption, code |
| Spacing | 4px base: xs(4) sm(8) md(16) lg(24) xl(32) 2xl(48) 3xl(64) |
| Icons | Library + sizes (sm 16, md 20, lg 24, xl 32) |

### Component Specification

```text
FOR EACH component:
  - States: default, hover, active, focus, disabled, loading, error, success
  - Variants: size (sm/md/lg), style (primary/secondary/ghost)
  - Anatomy: sub-elements
  - Accessibility: ARIA role, keyboard, focus, screen reader
  - Responsive: mobile/tablet/desktop behaviors
```

### Accessibility Requirements

```text
WCAG 2.1 Level [A/AA/AAA]:
- Contrast: ≥4.5:1 (AA), ≥7:1 (AAA)
- Touch targets: ≥44x44px
- Focus indicators: visible
- Keyboard: all functionality accessible
- Screen reader: proper ARIA, announcements
```

### Breakpoints

| Name | Range | Behavior |
|------|-------|----------|
| mobile | 0-639px | Touch-first, stacking |
| tablet | 640-1023px | Touch + hover |
| desktop | 1024-1279px | Mouse + keyboard |
| wide | 1280px+ | Extended layouts |

---

## Output Structure

### Feature Design

```text
specs/{feature-id}/design.md
.preview/
├── components/{name}/{Component}.tsx, .stories.tsx
└── animations/tokens.css, framer-variants.ts
```

### Design Quality Score (DQS) [REF:VG-008]

```text
DQS = Σ(criterion × weight) where:
- Color tokens defined: 10%
- Contrast valid: 15%
- Typography complete: 10%
- Component states: 15%
- Accessibility: 20%
- Screen flows: 15%
- Responsive: 10%
- Traceability: 5%

Threshold: MVP ≥ 70, Production ≥ 85
```

---

## Self-Review Phase [REF:SR-001]

### Criteria

| ID | Check | Severity |
|----|-------|----------|
| SR-DESIGN-01 | Color tokens defined | CRITICAL |
| SR-DESIGN-02 | Contrast ratios ≥4.5:1 | CRITICAL |
| SR-DESIGN-03 | Typography scale complete | HIGH |
| SR-DESIGN-04 | Component states listed | HIGH |
| SR-DESIGN-05 | Accessibility documented | HIGH |
| SR-DESIGN-06 | Screen flows mapped | HIGH |
| SR-DESIGN-07 | Responsive defined | MEDIUM |
| SR-DESIGN-08 | Interactions specified | MEDIUM |
| SR-DESIGN-09 | Traceability to FR/AS | MEDIUM |
| SR-DESIGN-10 | WCAG checklist complete | HIGH |

### Validation Loop

```text
FOR iteration IN 1..3:
  RUN contrast_validation()
  RUN component_completeness()
  RUN accessibility_check()
  IF all pass → BREAK
  ELSE → fix issues, re-validate

VERDICT:
  PASS → All CRITICAL/HIGH pass, a11y valid
  FAIL → CRITICAL issues → self-correct
  WARN → Only MEDIUM → proceed with warnings
```

---

## Quality Rules [REF:QI-001]

### Design-Specific Forbidden Phrases

```text
FORBIDDEN: "modern look", "clean aesthetic", "user-friendly", "intuitive design",
           "sleek and professional", "visually appealing", "seamless experience",
           "nice color palette", "good contrast", "improved usability"
```

### Design Writing Rules

```text
- Name actual colors: "#3B82F6 (Blue 500)" not "a nice blue"
- Specify exact values: "16px" not "appropriate spacing"
- Reference tokens: "color.primary.500" not "the primary color"
- Commit to aesthetic: "Brutalist typography" not "modern fonts"
- Explain WHY: "Large touch targets (48px) for motor impairments"
```

### Pre-Generation Gate

```text
✓ All colors use HEX or tokens
✓ All spacing uses explicit values
✓ All typography specifies weight/size/line-height
✓ All rationale explains user benefit
✓ All a11y claims include WCAG level
```

---

## Report Summary

```text
┌─────────────────────────────────────────────────────────────┐
│ /speckit.design Complete                                    │
├─────────────────────────────────────────────────────────────┤
│ Mode: {feature_design | design_system | concept | mockup}   │
│ Artifact: specs/{feature}/design.md                         │
│                                                             │
│ Agents: ✓ UX Designer  ✓ Product Designer  ✓ Motion Designer│
│                                                             │
│ Tokens: {N}   Components: {M}   Screens: {S}   Animations: {A}│
│ DQS: {score}/100 — {level}                                  │
│ Accessibility: WCAG {level}                                 │
└─────────────────────────────────────────────────────────────┘
```

### Traceability

| Spec Reference | Design Artifact |
|----------------|-----------------|
| FR-xxx | Component [name] |
| AS-xxx | Screen [name] |
| NFR-xxx | Accessibility item |

### Next Steps

| Action | Command |
|--------|---------|
| Interactive preview | /speckit.preview |
| Technical plan | /speckit.plan |
| UX audit | /speckit.analyze --ux |
| Promo materials | /speckit.design --promo |

---

## Context

{ARGS}
