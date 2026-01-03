# Design Token Export Formats

Standard export formats for design tokens in Spec Kit design specifications.

## Overview

Design tokens are the atomic values (colors, spacing, typography, etc.) that define a design system. Exporting tokens in multiple formats ensures compatibility across different tools and frameworks in the development pipeline.

## CSS Custom Properties

Native browser variables for direct stylesheet usage.

```css
:root {
  /* Colors */
  --color-primary: #2563EB;
  --color-primary-hover: #1D4ED8;
  --color-secondary: #64748B;
  --color-success: #10B981;
  --color-error: #EF4444;

  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;

  /* Typography */
  --font-family-base: 'Inter', sans-serif;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
}
```

## Tailwind Config

Integration with Tailwind CSS utility classes.

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: 'var(--color-primary)',
          hover: 'var(--color-primary-hover)',
        },
        secondary: 'var(--color-secondary)',
        success: 'var(--color-success)',
        error: 'var(--color-error)',
      },
      spacing: {
        xs: 'var(--spacing-xs)',
        sm: 'var(--spacing-sm)',
        md: 'var(--spacing-md)',
        lg: 'var(--spacing-lg)',
        xl: 'var(--spacing-xl)',
      },
      fontFamily: {
        base: ['var(--font-family-base)'],
      },
    }
  }
}
```

## JSON Tokens (Style Dictionary)

Platform-agnostic format for token transformation pipelines.

```json
{
  "color": {
    "primary": {
      "value": "#2563EB",
      "type": "color",
      "description": "Primary brand color"
    },
    "primary-hover": {
      "value": "#1D4ED8",
      "type": "color"
    }
  },
  "spacing": {
    "xs": { "value": "4px", "type": "spacing" },
    "sm": { "value": "8px", "type": "spacing" },
    "md": { "value": "16px", "type": "spacing" }
  },
  "font": {
    "family": {
      "base": { "value": "Inter, sans-serif", "type": "fontFamily" }
    },
    "size": {
      "base": { "value": "16px", "type": "fontSize" }
    }
  }
}
```

## Figma Variables Export

Figma-native format supporting design modes (light/dark themes).

```json
{
  "variables": [
    {
      "name": "color/primary",
      "resolvedType": "COLOR",
      "valuesByMode": {
        "light": "#2563EB",
        "dark": "#3B82F6"
      }
    },
    {
      "name": "color/background",
      "resolvedType": "COLOR",
      "valuesByMode": {
        "light": "#FFFFFF",
        "dark": "#1E293B"
      }
    },
    {
      "name": "spacing/md",
      "resolvedType": "FLOAT",
      "valuesByMode": {
        "default": 16
      }
    }
  ],
  "variableCollections": [
    {
      "name": "Primitives",
      "modes": ["light", "dark"]
    }
  ]
}
```

## Format Comparison

| Format | Use Case | Pros | Cons |
|--------|----------|------|------|
| **CSS Custom Properties** | Direct browser usage | Native support, runtime theming | No build-time optimization |
| **Tailwind Config** | Utility-first CSS | Purged CSS, consistent API | Requires Tailwind setup |
| **JSON (Style Dictionary)** | Multi-platform tokens | Transform to any format | Requires build pipeline |
| **Figma Variables** | Design-dev handoff | Mode support, Figma-native | Figma-specific |

## Recommended Pipeline

1. **Source of Truth**: JSON tokens (Style Dictionary format)
2. **Design Tool**: Figma Variables (synced from JSON)
3. **Development**: CSS Custom Properties + Tailwind Config (generated from JSON)

This ensures single-source token management with automated synchronization across design and development environments.
