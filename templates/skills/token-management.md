# Skill: Token Management

> Extract, validate, and export design tokens from design specifications to multiple formats.

---

## Prerequisites

- **Required**: `specs/[feature]/design.md` with Visual Language section
- **Optional**: `specs/app-design/design_system.md` for global tokens
- **Optional**: Existing token files for merge/update operations

## Triggers

- After `/speckit.design` generates Visual Language section
- When design tokens need export to development frameworks
- When validating token naming consistency

## Commands

### `/token extract`
Extract tokens from design specification into structured format.

### `/token validate`
Validate token naming conventions and completeness.

### `/token export --format [css|tailwind|json|figma]`
Export tokens to specified format.

### `/token sync`
Synchronize tokens with Figma Variables (bidirectional).

---

## Token Categories

| Category | Prefix | Examples |
|----------|--------|----------|
| Color | `color-` | `color-primary`, `color-text-secondary` |
| Typography | `text-` | `text-h1`, `text-body-sm` |
| Spacing | `space-` | `space-4`, `space-8` |
| Border Radius | `radius-` | `radius-sm`, `radius-lg` |
| Shadow | `shadow-` | `shadow-md`, `shadow-xl` |
| Z-Index | `z-` | `z-modal`, `z-dropdown` |

## Semantic Naming Pattern

`{category}-{property}[-{variant}][-{state}]`

### Examples
- `color-primary` → Primary brand color
- `color-primary-hover` → Primary on hover
- `text-body-sm` → Small body text
- `space-4` → 16px spacing (4 × 4px base)

---

## Extraction Process

### Step 1: Parse Visual Language

Extract from design.md tables:
- Color Palette table → color tokens
- Typography Scale table → text tokens
- Spacing System table → space tokens
- Border Radius table → radius tokens
- Shadow System table → shadow tokens

### Step 2: Generate Token Object

```json
{
  "tokens": {
    "color": {
      "primary": { "value": "#2563EB", "type": "color" },
      "primary-hover": { "value": "#1D4ED8", "type": "color" }
    },
    "text": {
      "h1": { "value": "2.25rem", "weight": "700", "type": "typography" }
    },
    "space": {
      "4": { "value": "16px", "type": "dimension" }
    }
  },
  "themes": {
    "light": { "color-primary": "#2563EB" },
    "dark": { "color-primary": "#3B82F6" }
  }
}
```

---

## Validation Rules

### Naming Validation

| Rule | Pattern | Error |
|------|---------|-------|
| Category prefix | `/^(color|text|space|radius|shadow|z)-/` | Missing category prefix |
| No magic values | No raw hex/px in code | Use token reference |
| Theme parity | Light token → Dark token | Missing dark mode value |

### Completeness Check

- [ ] All colors have contrast ratios documented
- [ ] Typography includes weight and line-height
- [ ] Spacing follows 4px grid
- [ ] All tokens have semantic names

---

## Export Formats

### CSS Custom Properties

```css
:root {
  /* Colors */
  --color-primary: #2563EB;
  --color-primary-hover: #1D4ED8;
  --color-secondary: #6B7280;

  /* Typography */
  --text-h1-size: 2.25rem;
  --text-h1-weight: 700;
  --text-h1-line-height: 1.2;

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-4: 16px;

  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
}

[data-theme="dark"] {
  --color-primary: #3B82F6;
  --color-primary-hover: #60A5FA;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-primary: #3B82F6;
  }
}
```

### Tailwind Config

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: 'var(--color-primary)',
          hover: 'var(--color-primary-hover)',
        },
        secondary: 'var(--color-secondary)',
      },
      spacing: {
        '1': 'var(--space-1)',
        '2': 'var(--space-2)',
        '4': 'var(--space-4)',
      },
      borderRadius: {
        sm: 'var(--radius-sm)',
        DEFAULT: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
      },
      boxShadow: {
        sm: 'var(--shadow-sm)',
        DEFAULT: 'var(--shadow-md)',
      },
      fontSize: {
        h1: ['var(--text-h1-size)', { lineHeight: 'var(--text-h1-line-height)', fontWeight: 'var(--text-h1-weight)' }],
      },
    },
  },
}
```

### JSON (Style Dictionary)

```json
{
  "color": {
    "primary": {
      "value": "#2563EB",
      "type": "color",
      "description": "Primary brand color for CTAs and active states"
    },
    "primary-hover": {
      "value": "#1D4ED8",
      "type": "color",
      "description": "Primary color on hover"
    }
  },
  "text": {
    "h1": {
      "size": { "value": "2.25rem", "type": "dimension" },
      "weight": { "value": "700", "type": "fontWeight" },
      "lineHeight": { "value": "1.2", "type": "number" }
    }
  },
  "space": {
    "4": {
      "value": "16px",
      "type": "dimension",
      "description": "Standard component spacing"
    }
  }
}
```

### Figma Variables

```json
{
  "version": "1.0",
  "collections": [
    {
      "name": "Design Tokens",
      "modes": ["Light", "Dark"],
      "variables": [
        {
          "name": "color/primary",
          "type": "COLOR",
          "valuesByMode": {
            "Light": "#2563EB",
            "Dark": "#3B82F6"
          }
        },
        {
          "name": "space/4",
          "type": "FLOAT",
          "valuesByMode": {
            "Light": 16,
            "Dark": 16
          }
        }
      ]
    }
  ]
}
```

---

## Integration

### With /speckit.design

Tokens are automatically extracted when design.md is generated:
```
/speckit.design → design.md created
                ↓
              /token extract (auto-triggered)
                ↓
              tokens.json generated
```

### With /speckit.implement

```
/speckit.implement
  ↓
  Check tokens.json exists
  ↓
  Generate CSS variables
  ↓
  Configure framework (Tailwind/CSS Modules)
```

### With /speckit.preview

```
/speckit.preview
  ↓
  Load tokens.json
  ↓
  Inject CSS variables into preview
```

---

## Output Files

| Command | Output |
|---------|--------|
| `/token extract` | `specs/[feature]/tokens.json` |
| `/token export --format css` | `src/styles/tokens.css` |
| `/token export --format tailwind` | `tailwind.config.tokens.js` |
| `/token export --format json` | `tokens/design-tokens.json` |
| `/token export --format figma` | `tokens/figma-variables.json` |

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `NO_VISUAL_LANGUAGE` | design.md missing Visual Language section | Run `/speckit.design` first |
| `INVALID_TOKEN_NAME` | Token doesn't follow naming convention | Rename to `{category}-{property}` |
| `MISSING_DARK_MODE` | Light token without dark equivalent | Add dark mode value |
| `CONTRAST_VIOLATION` | Color contrast below 4.5:1 | Adjust color values |

---

*Token Management Skill v1.0 | Part of Spec Kit Design Framework*
