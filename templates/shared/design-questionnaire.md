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
    animation_level: response_10
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
  animation_level: "Standard"
}
```
