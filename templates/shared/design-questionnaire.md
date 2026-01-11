# Design System Questionnaire

## Purpose

Collect detailed design preferences through interactive questions to generate precise design tokens. This questionnaire should be used in `design_system` and `concept_design` modes.

---

## Question Categories

### Visual Foundation (Questions 1-6)

| # | Question | Header | Options | Default | Impact |
|---|----------|--------|---------|---------|--------|
| 1 | Theme Mode | Theme | Light only / Dark only / Both (with system toggle) | Both | `color-scheme`, background colors, text colors |
| 2 | Color Palette Strategy | Palette | Monochromatic / Complementary / Analogous / Triadic | Complementary | Secondary/accent color generation algorithm |
| 3 | Visual Style | Style | Minimal & Clean / Bold & Vibrant / Soft & Friendly / Professional & Corporate | Minimal | Overall aesthetic presets |
| 4 | Corner Radius | Corners | Sharp (0-2px) / Soft (4-8px) / Rounded (12-16px) / Pill (full) | Soft | `--radius-sm/md/lg/xl` tokens |
| 5 | Visual Density | Density | Compact / Comfortable / Spacious | Comfortable | Spacing scale multiplier |
| 6 | Shadow Style | Shadows | None / Subtle / Elevated / Dramatic | Subtle | `--shadow-sm/md/lg/xl` tokens |

### Typography (Questions 7-9)

| # | Question | Header | Options | Default | Impact |
|---|----------|--------|---------|---------|--------|
| 7 | Heading Weight | Headings | Bold / Light / Mixed weights | Bold | `--font-weight-heading` token |
| 8 | Base Font Size | Font Size | Small (14px) / Medium (16px) / Large (18px) | Medium | Type scale base, accessibility |
| 9 | Font Pairing | Fonts | Sans + Sans / Serif + Sans / Monospace | Sans + Sans | `--font-family-heading/body` tokens |

### Iconography & Motion (Questions 10-12)

| # | Question | Header | Options | Default | Impact |
|---|----------|--------|---------|---------|--------|
| 10 | Icon Style | Icons | Outlined / Filled / Duotone | Outlined | Icon library recommendation |
| 11 | Animation Level | Animation | Minimal / Standard / Rich | Standard | Motion token complexity |
| 12 | Transition Speed | Speed | Fast (150ms) / Normal (250ms) / Slow (400ms) | Normal | `--duration-fast/normal/slow` tokens |

### Design Presets (Questions 13-14)

| # | Question | Header | Options | Default | Impact |
|---|----------|--------|---------|---------|--------|
| 13 | Framework Preset | Framework | shadcn/ui / MUI / Tailwind / Vuetify / Bootstrap / Angular Material / Skeleton UI / None | shadcn/ui | Component library structure, base tokens, component mappings |
| 14 | Aesthetic Preset | Aesthetic | None / Linear / Stripe / Vercel / Notion / Apple / Airbnb / GitHub / Slack / Figma | None | Visual brand style: colors, typography, spacing, shadows, motion |

### UX Quality (Questions 15-19)

| # | Question | Header | Options | Default | Conditional | Impact |
|---|----------|--------|---------|---------|-------------|--------|
| 15 | Usability Target Level | Usability | Best-in-class / Competitive / Acceptable / Low priority | Competitive | Always | Usability testing requirements in design specs |
| 16 | User Flow Complexity | Flow | Simple / Moderate / Complex / Very Complex | Moderate | IF app_type ∈ [web, mobile, desktop] | Navigation system design, information architecture |
| 17 | Design Accessibility Level | A11y Design | Inclusive / Proactive / Compliance+ / Compliance Only | Compliance+ | IF app_type ∈ [web, mobile, desktop] | Accessibility patterns beyond WCAG compliance |
| 18 | Error Prevention Strategy | Errors | Proactive / Reactive / Minimal | Reactive | IF usability_target ∈ [best, competitive] | Validation patterns, error handling UX |
| 19 | Responsive Design Strategy | Responsive | Mobile-First / Desktop-First / Platform-Optimized / Fluid | Mobile-First | IF app_type == web | Breakpoint system, responsive behavior |

### Brand & Audience (Questions 20-24)

| # | Question | Header | Options | Default | Conditional | Impact |
|---|----------|--------|---------|---------|-------------|--------|
| 20 | Brand Personality Archetype | Brand | Innovator / Trusted Advisor / Friend / Performer / Minimalist | Trusted Advisor | Always | Visual and interaction design personality |
| 21 | Tone of Voice | Tone | Formal / Professional / Conversational / Playful / Technical | Professional | Always | Microcopy, error messages, onboarding |
| 22 | Target Audience Sophistication | Audience | Expert / Intermediate / Beginner / Non-technical | Intermediate | Always | UI complexity, onboarding depth |
| 23 | Emotional Design Goal | Emotion | Confidence / Delight / Empowerment / Calm / Excitement | Confidence | Always | Emotional tone for interactions and visuals |
| 24 | Audience Demographics Priority | Demographics | Age Diversity / Global Audience / Neurodiversity / Low Bandwidth / None | None | IF usability_target != low | Demographic-specific design patterns (multi-select) |

**Framework Preset** determines component structure and library integration:
- **shadcn/ui** (React/Next.js) - Modern, customizable components with Radix UI primitives
- **MUI** (React) - Material Design components with extensive theming
- **Tailwind** - Utility-first CSS framework (no component library)
- **Vuetify** (Vue.js) - Material Design components for Vue
- **Bootstrap** - Classic Bootstrap components
- **Angular Material** (Angular) - Material Design for Angular
- **Skeleton UI** (Svelte) - Modern Svelte component library
- **None** - Custom implementation, no framework preset

**Aesthetic Preset** applies brand-inspired visual style (independent from framework):
- **None** - Use framework defaults or custom tokens only
- **Linear** - Clean, minimal, keyboard-first (Dev tools, productivity apps)
- **Stripe** - Professional, trustworthy, fintech-grade (Fintech, enterprise dashboards)
- **Vercel** - Modern, bold, dark-friendly (Developer platforms, documentation)
- **Notion** - Warm, approachable, content-first (Content tools, collaboration)
- **Apple** - Premium, refined, sophisticated (Consumer products, iOS/macOS)
- **Airbnb** - Friendly, travel-inspired (Marketplaces, travel platforms)
- **GitHub** - Developer-focused, monospace-friendly (Code platforms, version control)
- **Slack** - Vibrant, playful, team-oriented (Communication tools, team collaboration)
- **Figma** - Creative, colorful, design-tool aesthetic (Design tools, creative apps)

**Token Priority**: Custom overrides → Aesthetic preset → Framework preset → Defaults

---

## Interactive Collection Flow

```text
STEP 1: Basic Brand Inputs (existing)
  - brand_name
  - primary_color
  - product_type (saas/marketing/mobile/admin)

STEP 2: Extended Design Discovery (NEW)
  USE AskUserQuestion tool with batched questions:

  Batch 1 (Visual Foundation):
    Q1: "What theme mode should the design system support?"
        Options: ["Light only", "Dark only", "Both (with system toggle) (Recommended)"]

    Q2: "What color palette strategy do you prefer?"
        Options: ["Monochromatic (single hue)", "Complementary (opposite colors)",
                  "Analogous (adjacent colors)", "Triadic (3 evenly spaced)"]

    Q3: "What overall visual style fits your brand?"
        Options: ["Minimal & Clean (Recommended)", "Bold & Vibrant",
                  "Soft & Friendly", "Professional & Corporate"]

    Q4: "What corner radius style do you prefer?"
        Options: ["Sharp (0-2px)", "Soft (4-8px) (Recommended)",
                  "Rounded (12-16px)", "Pill (fully rounded)"]

  Batch 2 (Typography & Motion):
    Q5: "What visual density suits your users?"
        Options: ["Compact (data-heavy)", "Comfortable (Recommended)", "Spacious (content-focused)"]

    Q6: "What shadow style should components have?"
        Options: ["None (flat)", "Subtle (Recommended)", "Elevated", "Dramatic"]

    Q7: "What heading weight style do you prefer?"
        Options: ["Bold (Recommended)", "Light", "Mixed weights"]

    Q8: "What base font size for body text?"
        Options: ["Small (14px)", "Medium (16px) (Recommended)", "Large (18px)"]

  Batch 3 (Icons & Motion):
    Q9: "What icon style fits your product?"
        Options: ["Outlined (Recommended)", "Filled", "Duotone"]

    Q10: "What level of animation/motion?"
         Options: ["Minimal", "Standard (Recommended)", "Rich"]

  Batch 4 (Design Presets - NEW v0.1.2):
    Q11: "Which component framework/library will you use?"
         Header: "Framework"
         Options: [
           "shadcn/ui - Modern React components (Recommended)",
           "MUI - Material Design (React)",
           "Tailwind - Utility CSS only",
           "Vuetify - Material Design (Vue)",
           "Bootstrap - Classic Bootstrap",
           "Angular Material - Material Design (Angular)",
           "Skeleton UI - Modern Svelte",
           "None - Custom implementation"
         ]
         Description: "Framework preset provides component structure and library integration"

    Q12: "Which brand aesthetic would you like to apply?"
         Header: "Aesthetic"
         Options: [
           "None - Use framework defaults",
           "Linear - Clean, minimal (Dev tools)",
           "Stripe - Professional (Fintech)",
           "Vercel - Modern, bold (Developer platforms)",
           "Notion - Warm, approachable (Content/Collaboration)",
           "Apple - Premium, refined (Consumer products)",
           "Airbnb - Friendly (Marketplaces)",
           "GitHub - Developer-focused (Code platforms)",
           "Slack - Vibrant, playful (Communication)",
           "Figma - Creative, colorful (Design tools)"
         ]
         Description: "Aesthetic preset applies brand-inspired visual style (colors, typography, spacing)"

  Batch 5 (UX Quality - NEW v0.6.2):
    Q13: "What is your target usability level?"
         Header: "Usability"
         Options: [
           "Best-in-class - Top 10% of industry, extensive user testing, A/B testing",
           "Competitive - Industry average, basic usability testing (Recommended)",
           "Acceptable - Functional, minimal testing",
           "Low priority - Prototype, no testing needed"
         ]
         Description: "Sets usability expectations and testing rigor for design specs"
         Store as: design_system.ux_quality.usability_target

    Q14: "What user flow complexity does your app have?"
         Header: "Flow"
         Conditional: IF app_type ∈ [web-application, mobile-application, desktop-application]
         Options: [
           "Simple - 1-3 screens, linear flow, minimal navigation",
           "Moderate - 4-8 screens, some branches, standard navigation (Recommended)",
           "Complex - 9-20 screens, multiple paths, advanced navigation",
           "Very Complex - 20+ screens, multi-level navigation, user roles"
         ]
         Description: "Determines navigation system complexity and information architecture needs"
         Store as: design_system.ux_quality.flow_complexity

    Q15: "What design-focused accessibility level do you need?"
         Header: "A11y Design"
         Conditional: IF app_type ∈ [web-application, mobile-application, desktop-application]
         Options: [
           "Inclusive - Accessibility as core feature, user testing with disabled users",
           "Proactive - Exceeds WCAG AA, inclusive design patterns",
           "Compliance+ - WCAG AA + design best practices (Recommended)",
           "Compliance Only - Minimum WCAG level from constitution"
         ]
         Description: "Sets design-specific accessibility beyond WCAG compliance"
         Store as: design_system.ux_quality.design_a11y_level

    Q16: "What error prevention strategy should the design use?"
         Header: "Errors"
         Conditional: IF usability_target ∈ [best-in-class, competitive]
         Options: [
           "Proactive - Inline validation, auto-correct, smart defaults, confirmation dialogs",
           "Reactive - Clear error messages, easy recovery, helpful guidance (Recommended)",
           "Minimal - Basic error messages, standard browser validation"
         ]
         Description: "Defines how design prevents and handles user errors"
         Store as: design_system.ux_quality.error_prevention

    Q17: "What responsive design strategy fits your needs?"
         Header: "Responsive"
         Conditional: IF app_type == web-application
         Options: [
           "Mobile-First - Design for mobile, progressively enhance for desktop (Recommended)",
           "Desktop-First - Design for desktop, adapt for mobile",
           "Platform-Optimized - Separate designs for mobile/tablet/desktop",
           "Fluid - Single fluid design, no breakpoints"
         ]
         Description: "Defines multi-device design approach"
         Store as: design_system.ux_quality.responsive_strategy

  Batch 6 (Brand & Audience - NEW v0.6.2):
    Q18: "What brand personality archetype fits your product?"
         Header: "Brand"
         Options: [
           "Innovator - Cutting-edge, bold, experimental",
           "Trusted Advisor - Professional, stable, authoritative (Recommended)",
           "Friend - Approachable, warm, conversational",
           "Performer - Exciting, dynamic, high-energy",
           "Minimalist - Clean, restrained, focused"
         ]
         Description: "Guides visual and interaction design personality"
         Store as: design_system.brand_audience.brand_archetype

    Q19: "What tone of voice should the interface use?"
         Header: "Tone"
         Options: [
           "Formal - Third-person, no contractions, technical terminology",
           "Professional - Second-person, some contractions, clear explanations (Recommended)",
           "Conversational - Casual, contractions, everyday language",
           "Playful - Humor, personality, creative language",
           "Technical - Precise, jargon-appropriate, documentation-style"
         ]
         Description: "Guides microcopy, error messages, onboarding"
         Store as: design_system.brand_audience.tone_of_voice

    Q20: "What is your target audience sophistication level?"
         Header: "Audience"
         Options: [
           "Expert - Power users, keyboard shortcuts, advanced features visible",
           "Intermediate - Some experience, progressive disclosure, contextual help (Recommended)",
           "Beginner - First-time users, tooltips, onboarding flows, simple UI",
           "Non-technical - Minimal jargon, guided workflows, visual cues"
         ]
         Description: "Sets UI complexity and onboarding depth"
         Store as: design_system.brand_audience.audience_sophistication

    Q21: "What emotional design goal should interactions target?"
         Header: "Emotion"
         Options: [
           "Confidence - Trust, security, reliability (Recommended)",
           "Delight - Joy, surprise, playful interactions",
           "Empowerment - Capability, control, achievement",
           "Calm - Serenity, focus, minimal distraction",
           "Excitement - Energy, urgency, action"
         ]
         Description: "Sets emotional tone for interactions and visuals"
         Store as: design_system.brand_audience.emotional_goal

    Q22: "Which audience demographics should design prioritize?"
         Header: "Demographics"
         Conditional: IF usability_target != low-priority
         MultiSelect: true
         Options: [
           "Age Diversity - Support wide age range (children, seniors)",
           "Global Audience - Internationalization, RTL support, cultural sensitivity",
           "Neurodiversity - Cognitive accessibility, ADHD-friendly, autism-friendly",
           "Low Bandwidth - Optimized assets, progressive loading, offline support",
           "None - No specific demographic focus (Recommended)"
         ]
         Description: "Identifies specific audience needs for inclusive design"
         Store as: design_system.brand_audience.demographics_priority (array)

STEP 3: Store Responses
  design_preferences = {
    theme_mode: response_1,
    color_strategy: response_2,
    visual_style: response_3,
    corner_radius: response_4,
    visual_density: response_5,
    shadow_style: response_6,
    heading_weight: response_7,
    base_font_size: response_8,
    icon_style: response_9,
    animation_level: response_10,
    framework_preset: response_11,          # NEW v0.1.2: Framework selection
    aesthetic_preset: response_12,          # NEW v0.1.2: Aesthetic selection
    usability_target: response_13,          # NEW v0.6.2: UX quality
    flow_complexity: response_14,           # NEW v0.6.2: UX quality (conditional)
    design_a11y_level: response_15,         # NEW v0.6.2: UX quality (conditional)
    error_prevention: response_16,          # NEW v0.6.2: UX quality (conditional)
    responsive_strategy: response_17,       # NEW v0.6.2: UX quality (conditional)
    brand_archetype: response_18,           # NEW v0.6.2: Brand & audience
    tone_of_voice: response_19,             # NEW v0.6.2: Brand & audience
    audience_sophistication: response_20,   # NEW v0.6.2: Brand & audience
    emotional_goal: response_21,            # NEW v0.6.2: Brand & audience
    demographics_priority: response_22      # NEW v0.6.2: Brand & audience (array, conditional)
  }
```

---

## Conditional Logic Rules

This table documents when conditional questions (Q14-Q17, Q22) are asked based on constitution settings or previous answers:

| Question | Trigger Condition | Source | Notes |
|----------|------------------|---------|-------|
| Q14 (Flow Complexity) | IF app_type ∈ [web-application, mobile-application, desktop-application] | constitution.md → app_type (Q1) | Skip for CLI tools, APIs, libraries |
| Q15 (Design A11y Level) | IF app_type ∈ [web-application, mobile-application, desktop-application] | constitution.md → app_type (Q1) | Skip for non-visual apps |
| Q16 (Error Prevention) | IF usability_target ∈ [best-in-class, competitive] | Q13 (Usability Target) | Skip for acceptable/low priority projects |
| Q17 (Responsive Strategy) | IF app_type == web-application | constitution.md → app_type (Q1) | Only for web apps, not mobile/desktop |
| Q22 (Demographics Priority) | IF usability_target != low-priority | Q13 (Usability Target) | Skip for prototypes with no testing |

**Conditional Logic Flow**:
```text
Q1-Q12 (Visual Style - always asked)
  ↓
Q13 (Usability Target - always asked)
  ↓
IF app_type ∈ [web, mobile, desktop]:
  Q14 (Flow Complexity)
  Q15 (Design A11y Level)

IF usability_target ∈ [best, competitive]:
  Q16 (Error Prevention)

IF app_type == web:
  Q17 (Responsive Strategy)

Q18-Q21 (Brand & Audience - always asked)
  ↓
IF usability_target != low:
  Q22 (Demographics Priority - multi-select)
```

**Cross-Question Integration**:
- IF constitution accessibility_level >= wcag22-aa → Q15 defaults to "Compliance+"
- IF concept differentiation = "User Experience" → Q13 defaults to "Best-in-class"
- IF Q18 (Archetype) = "Innovator" → Q3 visual style recommendations lean "Bold & Vibrant"
- IF Q19 (Tone) = "Technical" → Q9 font pairing recommendations include monospace

---

## Token Generation Mappings

### Theme Mode

```yaml
"Light only":
  color-scheme: light
  --bg-primary: white
  --text-primary: slate-900

"Dark only":
  color-scheme: dark
  --bg-primary: slate-900
  --text-primary: white

"Both":
  # Generate both themes with CSS media query support
  @media (prefers-color-scheme: dark) { ... }
```

### Color Strategy

```yaml
"Monochromatic":
  # Generate shades/tints of primary only
  secondary: primary-600
  accent: primary-400

"Complementary":
  # Use color wheel opposite
  secondary: hue_rotate(primary, 180)
  accent: hue_rotate(primary, 30)

"Analogous":
  # Use adjacent hues
  secondary: hue_rotate(primary, 30)
  accent: hue_rotate(primary, -30)

"Triadic":
  # Use 3 evenly spaced hues
  secondary: hue_rotate(primary, 120)
  accent: hue_rotate(primary, 240)
```

### Corner Radius

```yaml
"Sharp":
  --radius-sm: 0px
  --radius-md: 2px
  --radius-lg: 4px
  --radius-xl: 4px
  --radius-full: 2px

"Soft":
  --radius-sm: 4px
  --radius-md: 6px
  --radius-lg: 8px
  --radius-xl: 12px
  --radius-full: 9999px

"Rounded":
  --radius-sm: 8px
  --radius-md: 12px
  --radius-lg: 16px
  --radius-xl: 24px
  --radius-full: 9999px

"Pill":
  --radius-sm: 9999px
  --radius-md: 9999px
  --radius-lg: 9999px
  --radius-xl: 9999px
  --radius-full: 9999px
```

### Visual Density

```yaml
"Compact":
  --spacing-base: 4px
  --spacing-scale: 1.25
  # 4, 5, 6, 8, 10, 12, 16, 20, 24...

"Comfortable":
  --spacing-base: 4px
  --spacing-scale: 1.5
  # 4, 6, 9, 14, 20, 30, 45...

"Spacious":
  --spacing-base: 8px
  --spacing-scale: 1.5
  # 8, 12, 18, 27, 40, 60...
```

### Shadow Style

```yaml
"None":
  --shadow-sm: none
  --shadow-md: none
  --shadow-lg: none
  --shadow-xl: none

"Subtle":
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05)
  --shadow-md: 0 2px 4px rgba(0,0,0,0.1)
  --shadow-lg: 0 4px 6px rgba(0,0,0,0.1)
  --shadow-xl: 0 8px 16px rgba(0,0,0,0.1)

"Elevated":
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.1)
  --shadow-md: 0 4px 8px rgba(0,0,0,0.15)
  --shadow-lg: 0 8px 16px rgba(0,0,0,0.15)
  --shadow-xl: 0 16px 32px rgba(0,0,0,0.2)

"Dramatic":
  --shadow-sm: 0 4px 8px rgba(0,0,0,0.2)
  --shadow-md: 0 8px 16px rgba(0,0,0,0.25)
  --shadow-lg: 0 16px 32px rgba(0,0,0,0.25)
  --shadow-xl: 0 24px 48px rgba(0,0,0,0.3)
```

### Animation Level

```yaml
"Minimal":
  --duration-fast: 100ms
  --duration-normal: 150ms
  --duration-slow: 200ms
  --motion-easing: ease-out
  # Only essential transitions (hover, focus)

"Standard":
  --duration-fast: 150ms
  --duration-normal: 250ms
  --duration-slow: 400ms
  --motion-easing: cubic-bezier(0.4, 0, 0.2, 1)
  # Common micro-interactions

"Rich":
  --duration-fast: 200ms
  --duration-normal: 350ms
  --duration-slow: 500ms
  --motion-easing: cubic-bezier(0.34, 1.56, 0.64, 1)
  # Full motion design with springs, staggers
```

### Framework Preset (NEW v0.1.2)

```yaml
"shadcn/ui":
  framework: "shadcn/ui"
  component_library: "@/components/ui/*"
  # Load framework preset from design-system-presets.md
  # Provides: component mappings, base tokens, Radix UI integration

"MUI":
  framework: "mui"
  component_library: "@mui/material"
  # Load framework preset from design-system-presets.md
  # Provides: Material Design tokens, theme customization

"Tailwind":
  framework: "tailwind"
  component_library: "none"
  # Load framework preset from design-system-presets.md
  # Provides: Tailwind config tokens, no components

"Vuetify":
  framework: "vuetify"
  component_library: "vuetify/components"
  # Load framework preset from design-system-presets.md
  # Provides: Vue Material components, theme system

"Bootstrap":
  framework: "bootstrap"
  component_library: "bootstrap/dist/js/bootstrap.bundle"
  # Load framework preset from design-system-presets.md
  # Provides: Bootstrap variables, component classes

"Angular Material":
  framework: "angular-material"
  component_library: "@angular/material"
  # Load framework preset from design-system-presets.md
  # Provides: Angular Material tokens, component modules

"Skeleton UI":
  framework: "skeleton"
  component_library: "@skeletonlabs/skeleton"
  # Load framework preset from design-system-presets.md
  # Provides: Svelte components, Tailwind integration

"None":
  framework: "none"
  # No framework preset, use custom tokens only
```

### Aesthetic Preset (NEW v0.1.2)

```yaml
"None":
  aesthetic: null
  # Use framework defaults or custom tokens only

"Linear":
  aesthetic: "linear"
  # Load aesthetic preset from design-aesthetic-presets.md
  # Accent: Purple #5e6ad2, Font: Inter 13px
  # Overrides visual tokens: colors, typography, spacing, shadows

"Stripe":
  aesthetic: "stripe"
  # Load aesthetic preset from design-aesthetic-presets.md
  # Accent: Indigo #635bff, Font: Söhne 16px

"Vercel":
  aesthetic: "vercel"
  # Load aesthetic preset from design-aesthetic-presets.md
  # Accent: Black #000000, Font: Inter 16px

"Notion":
  aesthetic: "notion"
  # Load aesthetic preset from design-aesthetic-presets.md
  # Accent: Coral #eb5757, Font: Inter 16px

"Apple":
  aesthetic: "apple"
  # Load aesthetic preset from design-aesthetic-presets.md
  # Accent: Blue #007aff, Font: SF Pro 17px

"Airbnb":
  aesthetic: "airbnb"
  # Load aesthetic preset from design-aesthetic-presets.md
  # Accent: Rausch #ff385c, Font: Cereal 16px

"GitHub":
  aesthetic: "github"
  # Load aesthetic preset from design-aesthetic-presets.md
  # Accent: Blue #0969da, Font: System 14px

"Slack":
  aesthetic: "slack"
  # Load aesthetic preset from design-aesthetic-presets.md
  # Accent: Aubergine #611f69, Font: Lato 15px

"Figma":
  aesthetic: "figma"
  # Load aesthetic preset from design-aesthetic-presets.md
  # Accent: Purple #a259ff, Font: Inter 14px
```

**Token Resolution Logic**:

```text
1. Start with defaults
2. IF framework_preset != "None":
     Apply framework preset tokens (structure, component mappings)
3. IF aesthetic_preset != "None":
     Apply aesthetic preset tokens (colors, typography, spacing, shadows, motion)
     NOTE: Aesthetic OVERRIDES framework visual tokens but NOT component mappings
4. Apply custom overrides from design_preferences and constitution.md
   NOTE: Custom overrides have HIGHEST priority

Priority: Custom > Aesthetic > Framework > Defaults
```

### UX Quality Settings (NEW v0.6.2)

```yaml
# Q13: Usability Target Level
"Best-in-class":
  usability_target: best
  # Impact: Design specs include:
  # - Comprehensive usability testing plan (A/B tests, user testing, metrics)
  # - Success metrics: Task completion rate >= 90%
  # - Detailed user research requirements

"Competitive":
  usability_target: competitive
  # Impact: Design specs include:
  # - Basic usability testing plan (user testing, metrics)
  # - Success metrics: Task completion rate >= 80%
  # - Standard user research requirements

"Acceptable":
  usability_target: acceptable
  # Impact: Design specs include:
  # - Minimal usability testing plan (metrics only)
  # - No formal user testing required

"Low priority":
  usability_target: low
  # Impact: No usability testing plan required


# Q14: User Flow Complexity (conditional on app_type)
"Simple":
  flow_complexity: simple
  # Impact: Linear navigation, 1-3 screens, minimal IA

"Moderate":
  flow_complexity: moderate
  # Impact: Standard navigation, 4-8 screens, simple IA

"Complex":
  flow_complexity: complex
  # Impact: Advanced navigation, 9-20 screens, multi-level IA

"Very Complex":
  flow_complexity: very-complex
  # Impact: Multi-role navigation, 20+ screens, comprehensive IA


# Q15: Design Accessibility Level (conditional on app_type)
"Inclusive":
  design_a11y_level: inclusive
  # Impact: User testing with disabled users, innovative a11y patterns

"Proactive":
  design_a11y_level: proactive
  # Impact: Exceeds WCAG AA, inclusive design patterns

"Compliance+":
  design_a11y_level: compliance-plus
  # Impact: WCAG AA + design best practices

"Compliance Only":
  design_a11y_level: compliance-only
  # Impact: Minimum WCAG level from constitution


# Q16: Error Prevention Strategy (conditional on usability_target)
"Proactive":
  error_prevention: proactive
  # Impact: Inline validation, auto-correct, smart defaults, confirmations

"Reactive":
  error_prevention: reactive
  # Impact: Clear error messages, easy recovery, helpful guidance

"Minimal":
  error_prevention: minimal
  # Impact: Basic error messages, standard browser validation


# Q17: Responsive Design Strategy (conditional on app_type == web)
"Mobile-First":
  responsive_strategy: mobile-first
  # Impact: Design for mobile, progressively enhance for desktop
  # Breakpoints: 640px (sm), 768px (md), 1024px (lg), 1280px (xl)

"Desktop-First":
  responsive_strategy: desktop-first
  # Impact: Design for desktop, adapt for mobile
  # Breakpoints: 1280px (lg), 1024px (md), 768px (sm), 640px (xs)

"Platform-Optimized":
  responsive_strategy: platform-optimized
  # Impact: Separate designs for mobile/tablet/desktop

"Fluid":
  responsive_strategy: fluid
  # Impact: Single fluid design, no breakpoints, container queries
```

### Brand & Audience Settings (NEW v0.6.2)

```yaml
# Q18: Brand Personality Archetype
"Innovator":
  brand_archetype: innovator
  # Impact: Cutting-edge visual style, experimental interactions
  # Recommendations: Bold colors, asymmetric layouts, rich animations

"Trusted Advisor":
  brand_archetype: trusted-advisor
  # Impact: Professional, stable, authoritative
  # Recommendations: Conservative colors, structured layouts, subtle animations

"Friend":
  brand_archetype: friend
  # Impact: Approachable, warm, conversational
  # Recommendations: Warm colors, friendly typography, welcoming layouts

"Performer":
  brand_archetype: performer
  # Impact: Exciting, dynamic, high-energy
  # Recommendations: Vibrant colors, bold typography, rich motion

"Minimalist":
  brand_archetype: minimalist
  # Impact: Clean, restrained, focused
  # Recommendations: Monochrome palette, simple typography, minimal motion


# Q19: Tone of Voice
"Formal":
  tone_of_voice: formal
  # Impact: Third-person, no contractions, technical terminology
  # Example: "An error has occurred. Please contact support."

"Professional":
  tone_of_voice: professional
  # Impact: Second-person, some contractions, clear explanations
  # Example: "We couldn't process your request. Please try again."

"Conversational":
  tone_of_voice: conversational
  # Impact: Casual, contractions, everyday language
  # Example: "Oops! Something went wrong. Let's try that again."

"Playful":
  tone_of_voice: playful
  # Impact: Humor, personality, creative language
  # Example: "Whoopsie! Our hamsters fell asleep. Wake them up?"

"Technical":
  tone_of_voice: technical
  # Impact: Precise, jargon-appropriate, documentation-style
  # Example: "Error 400: Invalid request payload. Check schema."


# Q20: Target Audience Sophistication
"Expert":
  audience_sophistication: expert
  # Impact: Keyboard shortcuts, advanced features visible, minimal onboarding

"Intermediate":
  audience_sophistication: intermediate
  # Impact: Progressive disclosure, contextual help, standard onboarding

"Beginner":
  audience_sophistication: beginner
  # Impact: Tooltips, onboarding flows, simple UI, extensive guidance

"Non-technical":
  audience_sophistication: non-technical
  # Impact: Minimal jargon, guided workflows, visual cues, step-by-step


# Q21: Emotional Design Goal
"Confidence":
  emotional_goal: confidence
  # Impact: Trust, security, reliability
  # Patterns: Consistent layouts, predictable interactions, clear feedback

"Delight":
  emotional_goal: delight
  # Impact: Joy, surprise, playful interactions
  # Patterns: Micro-interactions, celebrations, playful animations

"Empowerment":
  emotional_goal: empowerment
  # Impact: Capability, control, achievement
  # Patterns: Progress indicators, undo/redo, customization options

"Calm":
  emotional_goal: calm
  # Impact: Serenity, focus, minimal distraction
  # Patterns: Whitespace, soft colors, gentle transitions

"Excitement":
  emotional_goal: excitement
  # Impact: Energy, urgency, action
  # Patterns: Bold colors, dynamic animations, attention-grabbing CTAs


# Q22: Audience Demographics Priority (multi-select, conditional)
demographics_priority: [
  "age-diversity",        # IF selected: Age-friendly patterns (seniors, children)
  "global-audience",      # IF selected: i18n-ready, RTL support, cultural sensitivity
  "neurodiversity",       # IF selected: Cognitive a11y, ADHD-friendly, autism-friendly
  "low-bandwidth"         # IF selected: Optimized assets, progressive loading, offline
]
# IF none selected: demographics_priority = []
```

---

## Icon Library Recommendations

| Style | Recommended Libraries |
|-------|----------------------|
| Outlined | Lucide, Heroicons (outline), Phosphor (regular) |
| Filled | Heroicons (solid), Phosphor (fill), Bootstrap Icons |
| Duotone | Phosphor (duotone), Font Awesome Pro (duotone) |

---

## Skip Questionnaire Flag

If user passes `--quick` or `--defaults`, skip questionnaire and use defaults:

```text
design_preferences = {
  # Visual Style (Q1-Q12)
  theme_mode: "Both",
  color_strategy: "Complementary",
  visual_style: "Minimal",
  corner_radius: "Soft",
  visual_density: "Comfortable",
  shadow_style: "Subtle",
  heading_weight: "Bold",
  base_font_size: "Medium",
  icon_style: "Outlined",
  animation_level: "Standard",

  # Design Presets (Q13-Q14) - NEW v0.1.2
  framework_preset: "shadcn/ui",
  aesthetic_preset: "None",

  # UX Quality (Q15-Q19) - NEW v0.6.2
  usability_target: "Competitive",
  flow_complexity: "Moderate",           # IF app_type ∈ [web, mobile, desktop]
  design_a11y_level: "Compliance+",      # IF app_type ∈ [web, mobile, desktop]
  error_prevention: "Reactive",          # IF usability_target ∈ [best, competitive]
  responsive_strategy: "Mobile-First",   # IF app_type == web

  # Brand & Audience (Q20-Q24) - NEW v0.6.2
  brand_archetype: "Trusted Advisor",
  tone_of_voice: "Professional",
  audience_sophistication: "Intermediate",
  emotional_goal: "Confidence",
  demographics_priority: []              # IF usability_target != low
}
```

**Override with flags**:
- If `--library <name>` flag passed: `framework_preset = flag_value`
- If `--aesthetic <name>` flag passed: `aesthetic_preset = flag_value`
- Flags take precedence over questionnaire responses and defaults
