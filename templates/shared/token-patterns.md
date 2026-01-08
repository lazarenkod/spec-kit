# Design Token Detection Patterns

This document defines regex patterns and detection rules for identifying design token violations in generated mockups.

## Overview

The token compliance validator uses these patterns to detect hardcoded values that should use design tokens.

```
┌─────────────────────────────────────────────────────────────────┐
│                  TOKEN DETECTION FLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Parse CSS/HTML files                                        │
│  2. Extract all style values                                    │
│  3. Match against violation patterns                            │
│  4. Cross-reference with design.md tokens                       │
│  5. Generate compliance report                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Color Token Patterns

### Detection Regex

```javascript
const colorPatterns = {
  // Hex colors (short and long)
  hex_short: /#[0-9a-fA-F]{3}\b/g,
  hex_long: /#[0-9a-fA-F]{6}\b/g,
  hex_alpha: /#[0-9a-fA-F]{8}\b/g,

  // RGB/RGBA
  rgb: /rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)/gi,
  rgba: /rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)/gi,

  // HSL/HSLA
  hsl: /hsl\(\s*\d+\s*,\s*[\d.]+%\s*,\s*[\d.]+%\s*\)/gi,
  hsla: /hsla\(\s*\d+\s*,\s*[\d.]+%\s*,\s*[\d.]+%\s*,\s*[\d.]+\s*\)/gi,

  // Modern color functions
  color_mix: /color-mix\([^)]+\)/gi,
  oklch: /oklch\([^)]+\)/gi,

  // Named colors (common ones that should be tokens)
  named: /\b(white|black|red|blue|green|yellow|gray|grey|transparent)\b/gi
};
```

### Allowed Color Patterns

```javascript
const allowedColorPatterns = [
  // CSS variables
  /var\(--[\w-]+\)/,

  // Tailwind classes (in class attributes)
  /\b(bg|text|border|ring|fill|stroke)-[\w-]+/,

  // currentColor keyword
  /\bcurrentColor\b/i,

  // inherit/initial/unset
  /\b(inherit|initial|unset)\b/,

  // Gradients using tokens
  /linear-gradient\([^)]*var\(--[^)]+\)[^)]*\)/
];
```

### Color Token Mapping

```yaml
color_token_map:
  # Near-match mapping for auto-fix suggestions
  "#3b82f6": "--color-primary"
  "#60a5fa": "--color-primary-light"
  "#2563eb": "--color-primary-dark"
  "#10b981": "--color-success"
  "#ef4444": "--color-error"
  "#f59e0b": "--color-warning"
  "#6b7280": "--color-gray-500"
  "#374151": "--color-gray-700"
  "#f3f4f6": "--color-gray-100"
  "#ffffff": "--color-white"
  "#000000": "--color-black"

  # Common alpha values
  "rgba(0, 0, 0, 0.5)": "--color-overlay"
  "rgba(0, 0, 0, 0.1)": "--color-shadow"
  "rgba(255, 255, 255, 0.9)": "--color-backdrop"
```

---

## Spacing Token Patterns

### Detection Regex

```javascript
const spacingPatterns = {
  // Pixel values
  pixels: /:\s*(\d+)px(?:\s|;|$)/g,

  // Rem/em values
  rem: /:\s*([\d.]+)rem(?:\s|;|$)/g,
  em: /:\s*([\d.]+)em(?:\s|;|$)/g,

  // Shorthand properties
  margin_shorthand: /margin:\s*([^;]+)/g,
  padding_shorthand: /padding:\s*([^;]+)/g,
  gap_shorthand: /gap:\s*([^;]+)/g,

  // Calc with hardcoded values
  calc_hardcoded: /calc\([^)]*\d+px[^)]*\)/g
};
```

### Allowed Spacing Patterns

```javascript
const allowedSpacingPatterns = [
  // CSS variables
  /var\(--[\w-]+\)/,

  // Zero values
  /^0$/,
  /^0px$/,

  // Auto/fit-content
  /\b(auto|fit-content|min-content|max-content)\b/,

  // Percentage values (responsive)
  /\d+%/,

  // Viewport units (responsive)
  /\d+(vw|vh|vmin|vmax|dvh|svh|lvh)/,

  // Tailwind spacing classes
  /\b(p|m|gap|space)-[\w-]+/
];
```

### Spacing Token Scale

```yaml
spacing_scale:
  # Standard 4px base scale
  "0": "0"
  "4px": "--space-1"
  "8px": "--space-2"
  "12px": "--space-3"
  "16px": "--space-4"
  "20px": "--space-5"
  "24px": "--space-6"
  "32px": "--space-8"
  "40px": "--space-10"
  "48px": "--space-12"
  "64px": "--space-16"
  "80px": "--space-20"
  "96px": "--space-24"

  # Rem equivalents (16px base)
  "0.25rem": "--space-1"
  "0.5rem": "--space-2"
  "0.75rem": "--space-3"
  "1rem": "--space-4"
  "1.25rem": "--space-5"
  "1.5rem": "--space-6"
  "2rem": "--space-8"
  "2.5rem": "--space-10"
  "3rem": "--space-12"
```

### Magic Number Detection

```javascript
// Values that are often magic numbers
const magicNumberPatterns = {
  // Suspicious single values
  suspicious_values: [
    /:\s*[1357]\d*px/,  // Odd pixel values
    /:\s*\d{3,}px/,     // Large pixel values
  ],

  // Common magic numbers to flag
  magic_numbers: [
    '13px', '17px', '19px', '23px', '27px', '29px',
    '31px', '37px', '41px', '43px', '47px', '53px'
  ]
};
```

---

## Typography Token Patterns

### Detection Regex

```javascript
const typographyPatterns = {
  // Font size
  font_size_px: /font-size:\s*(\d+)px/gi,
  font_size_rem: /font-size:\s*([\d.]+)rem/gi,

  // Font weight
  font_weight: /font-weight:\s*(\d{3})/g,

  // Line height
  line_height_px: /line-height:\s*(\d+)px/gi,
  line_height_unitless: /line-height:\s*([\d.]+)(?!\w)/g,

  // Letter spacing
  letter_spacing: /letter-spacing:\s*(-?[\d.]+)(px|em|rem)?/gi,

  // Font family
  font_family: /font-family:\s*([^;]+)/gi
};
```

### Typography Scale

```yaml
typography_scale:
  # Font sizes (using type scale)
  "12px": "--text-xs"
  "14px": "--text-sm"
  "16px": "--text-base"
  "18px": "--text-lg"
  "20px": "--text-xl"
  "24px": "--text-2xl"
  "30px": "--text-3xl"
  "36px": "--text-4xl"
  "48px": "--text-5xl"
  "60px": "--text-6xl"

  # Font weights
  "300": "--font-light"
  "400": "--font-normal"
  "500": "--font-medium"
  "600": "--font-semibold"
  "700": "--font-bold"

  # Line heights
  "1": "--leading-none"
  "1.25": "--leading-tight"
  "1.375": "--leading-snug"
  "1.5": "--leading-normal"
  "1.625": "--leading-relaxed"
  "2": "--leading-loose"
```

---

## Border and Shadow Patterns

### Detection Regex

```javascript
const borderShadowPatterns = {
  // Border radius
  border_radius_px: /border-radius:\s*(\d+)px/gi,
  border_radius_individual: /border-(top|bottom)-(left|right)-radius:\s*(\d+)px/gi,

  // Border width
  border_width: /border(-\w+)?:\s*(\d+)px\s/gi,

  // Box shadow (detect hardcoded values)
  box_shadow: /box-shadow:\s*([^;]+)/gi,

  // Drop shadow
  drop_shadow: /drop-shadow\([^)]+\)/gi
};
```

### Border/Shadow Token Scale

```yaml
border_radius_scale:
  "0": "--radius-none"
  "2px": "--radius-sm"
  "4px": "--radius-md"
  "6px": "--radius-lg"
  "8px": "--radius-xl"
  "12px": "--radius-2xl"
  "16px": "--radius-3xl"
  "9999px": "--radius-full"

shadow_scale:
  "0 1px 2px 0 rgb(0 0 0 / 0.05)": "--shadow-sm"
  "0 1px 3px 0 rgb(0 0 0 / 0.1)": "--shadow-md"
  "0 4px 6px -1px rgb(0 0 0 / 0.1)": "--shadow-lg"
  "0 10px 15px -3px rgb(0 0 0 / 0.1)": "--shadow-xl"
  "0 20px 25px -5px rgb(0 0 0 / 0.1)": "--shadow-2xl"
```

---

## Inline Style Detection

### HTML Inline Style Patterns

```javascript
const inlineStylePatterns = {
  // style attribute
  style_attr: /style\s*=\s*["']([^"']+)["']/gi,

  // Specific inline properties to flag
  inline_color: /style\s*=\s*["'][^"']*color\s*:[^"']+["']/gi,
  inline_font: /style\s*=\s*["'][^"']*font-[^"']+["']/gi,
  inline_margin: /style\s*=\s*["'][^"']*margin[^"']+["']/gi,
  inline_padding: /style\s*=\s*["'][^"']*padding[^"']+["']/gi
};
```

### Allowed Inline Styles

```javascript
const allowedInlinePatterns = [
  // CSS variables in inline styles
  /style\s*=\s*["'][^"']*var\(--[\w-]+\)[^"']*["']/,

  // Dynamic values (transforms, positions for JS)
  /style\s*=\s*["'][^"']*transform[^"']+["']/,

  // Width/height for images (performance)
  /style\s*=\s*["'][^"']*(width|height)\s*:\s*\d+px[^"']*["']/
];
```

---

## Violation Severity Levels

```yaml
severity_levels:
  critical:
    description: "Must fix before deployment"
    patterns:
      - Hardcoded colors in critical UI elements
      - Spacing that breaks layout on resize
      - Typography that doesn't match brand
    auto_fix: true

  warning:
    description: "Should fix for consistency"
    patterns:
      - Near-match values (off by 1-2px)
      - Inline styles that could use classes
      - Computed values with hardcoded parts
    auto_fix: true

  info:
    description: "Consider for polish"
    patterns:
      - Third-party overrides
      - One-off intentional values
      - Browser-specific adjustments
    auto_fix: false
```

---

## Auto-Fix Mappings

### Color Auto-Fix

```javascript
function suggestColorFix(hardcodedColor, designTokens) {
  // Exact match
  const exactMatch = designTokens.find(t => t.value === hardcodedColor);
  if (exactMatch) return `var(${exactMatch.name})`;

  // Fuzzy match (within deltaE of 5)
  const fuzzyMatch = findClosestColor(hardcodedColor, designTokens, 5);
  if (fuzzyMatch) return `var(${fuzzyMatch.name}) /* was: ${hardcodedColor} */`;

  // No match - suggest creating token
  return `/* TODO: Add token for ${hardcodedColor} */`;
}
```

### Spacing Auto-Fix

```javascript
function suggestSpacingFix(hardcodedValue, spacingScale) {
  const numericValue = parseInt(hardcodedValue, 10);

  // Find nearest scale value
  const nearest = spacingScale.reduce((prev, curr) => {
    return Math.abs(curr.px - numericValue) < Math.abs(prev.px - numericValue)
      ? curr
      : prev;
  });

  // If within 2px, suggest fix
  if (Math.abs(nearest.px - numericValue) <= 2) {
    return `var(${nearest.token})`;
  }

  return null;
}
```

---

## Report Format

### Compliance Report Structure

```markdown
## Token Compliance Report

**Scanned**: {file_count} files
**Total Values**: {total_values}
**Compliant**: {compliant_count} ({percentage}%)

### Summary by Category

| Category | Compliant | Violations | Compliance |
|----------|-----------|------------|------------|
| Colors | {c_ok}/{c_total} | {c_violations} | {c_pct}% |
| Spacing | {s_ok}/{s_total} | {s_violations} | {s_pct}% |
| Typography | {t_ok}/{t_total} | {t_violations} | {t_pct}% |
| Borders/Shadows | {b_ok}/{b_total} | {b_violations} | {b_pct}% |

### Violations

#### Critical

| File | Line | Property | Found | Suggested |
|------|------|----------|-------|-----------|
| {file} | {line} | {prop} | {value} | {fix} |

#### Warning

| File | Line | Property | Found | Suggested |
|------|------|----------|-------|-----------|
| {file} | {line} | {prop} | {value} | {fix} |

### Auto-Fix Script

Run the following to apply automatic fixes:

```bash
.preview/reports/token-fixes.sh
```
```

---

## Design.md Token Extraction

### Expected Token Format in design.md

```markdown
## Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| --color-primary | #3b82f6 | Primary actions, links |
| --color-primary-light | #60a5fa | Hover states |
| --color-primary-dark | #2563eb | Active states |

## Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| --space-1 | 4px | Tight spacing |
| --space-2 | 8px | Default spacing |
| --space-4 | 16px | Component padding |

## Typography Scale

| Token | Value | Usage |
|-------|-------|-------|
| --text-sm | 14px | Secondary text |
| --text-base | 16px | Body text |
| --text-lg | 18px | Lead text |
```

### Token Extraction Algorithm

```javascript
function extractTokensFromDesignMd(content) {
  const tokens = {
    colors: [],
    spacing: [],
    typography: [],
    borders: [],
    shadows: []
  };

  // Parse markdown tables
  const tableRegex = /\|([^|]+)\|([^|]+)\|([^|]+)\|/g;

  // Categorize based on token name prefix
  // --color-* → colors
  // --space-* → spacing
  // --text-*, --font-*, --leading-* → typography
  // --radius-*, --border-* → borders
  // --shadow-* → shadows

  return tokens;
}
```
