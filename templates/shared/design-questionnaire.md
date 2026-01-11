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
    framework_preset: response_11,      # NEW: Framework selection
    aesthetic_preset: response_12       # NEW: Aesthetic selection
  }
```

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
  framework_preset: "shadcn/ui",        # NEW v0.1.2
  aesthetic_preset: "None"              # NEW v0.1.2
}
```

**Override with flags**:
- If `--library <name>` flag passed: `framework_preset = flag_value`
- If `--aesthetic <name>` flag passed: `aesthetic_preset = flag_value`
- Flags take precedence over questionnaire responses and defaults
