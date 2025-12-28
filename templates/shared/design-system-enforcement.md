# Design System Enforcement Guide

This document provides context for AI agents enforcing design system principles during code generation and validation.

## Overview

Design System Enforcement ensures UI code adheres to configured design tokens and component library patterns. It integrates with:
- **`/speckit.implement`**: Code generation with design system context
- **`/speckit.analyze`**: Pass Z validation for design system compliance
- **Vision Validation**: Visual consistency checks against tokens

## Configuration Loading

### Reading Design System Config

Extract the `design_system` YAML block from `memory/constitution.md`:

```text
1. Read memory/constitution.md
2. Parse YAML block under "## Design System Configuration"
3. If preset specified, load from design-system-presets.md
4. Merge preset with custom overrides
5. Validate required fields: framework, enforcement_level
```

### Configuration Schema

```yaml
design_system:
  preset: "string"              # Optional: shadcn/ui, mui, tailwind, etc.
  framework: "string"           # Required: component library identifier
  theme:
    colors:
      primary: "#hex"
      secondary: "#hex"
      background: "#hex"
      foreground: "#hex"
      # ... additional color tokens
    typography:
      font_family: "string"
      font_family_mono: "string"
      scale:
        xs: "rem"
        sm: "rem"
        base: "rem"
        # ... additional sizes
    spacing:
      unit: "string"            # Base spacing unit
    radii:
      sm: "rem"
      md: "rem"
      lg: "rem"
  component_library_url: "url"  # Documentation reference
  enforcement_level: "string"   # strict | warn | off
```

## Enforcement Levels

| Level | Behavior | Use Case |
|-------|----------|----------|
| `strict` | Violations block deployment; CRITICAL/HIGH severity | Production CI/CD, strict design compliance |
| `warn` | Violations reported; MEDIUM/HIGH severity | Development, gradual adoption |
| `off` | No validation performed | Legacy code, rapid prototyping |

### Severity Mapping

| Principle | Strict Mode | Warn Mode |
|-----------|-------------|-----------|
| DSS-001 (Components) | HIGH | MEDIUM |
| DSS-002 (Colors) | CRITICAL | HIGH |
| DSS-003 (Typography) | HIGH | MEDIUM |

## Code Analysis Rules

### DSS-001: Component Library Compliance

**Purpose**: Ensure library components are used before custom implementations.

#### Detection Patterns by Framework

**React/shadcn/ui**:
```text
# Custom component indicators when library equivalent exists
PATTERN: /function\s+(?:Custom)?(?:Button|Input|Select|Modal|Dialog|Card)\s*\(/
MATCH: "function CustomButton(" when @shadcn/ui configured

# Should use instead:
import { Button } from "@/components/ui/button"
```

**Vue/Vuetify**:
```text
# Custom component indicators
PATTERN: /<template>[\s\S]*<(?:custom-|my-)(button|input|select)/
MATCH: "<custom-button>" when vuetify configured

# Should use instead:
<v-btn>
```

**Angular Material**:
```text
# Custom component indicators
PATTERN: /@Component[\s\S]*selector:\s*['"](?:app|custom)-(button|input)/
MATCH: "selector: 'app-button'" when @angular/material configured

# Should use instead:
<button mat-button>
```

#### Allowlist Patterns

Components allowed to be custom (not triggering DSS-001):
- `*Layout*`, `*Container*`, `*Page*`
- `*Provider*`, `*Context*`
- Components extending library primitives (documented via comments)

---

### DSS-002: Color Token Compliance

**Purpose**: All colors must reference design tokens, not hardcoded values.

#### Detection Patterns

```text
# Hardcoded hex colors (6 or 3 digit)
PATTERN: /#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b
EXCLUDE: *.config.*, theme.*, tokens.*, tailwind.config.*

# Hardcoded RGB/RGBA
PATTERN: /rgba?\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+/
EXCLUDE: Same as above

# Hardcoded HSL/HSLA
PATTERN: /hsla?\s*\(\s*\d+\s*,\s*[\d.]+%\s*,\s*[\d.]+%/
EXCLUDE: Same as above

# CSS-in-JS hardcoded colors
PATTERN: /(?:color|background|border|fill|stroke):\s*['"]?#[0-9A-Fa-f]/
```

#### Allowed Exceptions

Colors in these contexts are exempt:
1. **Token definition files**: `theme.ts`, `tokens.css`, `tailwind.config.*`, `*.tokens.*`
2. **Gradient from tokens**: `linear-gradient(var(--primary), var(--secondary))`
3. **Third-party overrides**: Must include comment `// DSS-002 exception: [reason]`
4. **SVG assets**: `.svg` files (decorative, not semantic)
5. **Test files**: `*.test.*`, `*.spec.*`

#### Fix Suggestions

| Found | Suggested Fix |
|-------|---------------|
| `color: "#3B82F6"` | `color: "var(--primary)"` or `color: colors.primary` |
| `background: "#FFFFFF"` | `background: "var(--background)"` or `bg-background` |
| `border: "1px solid #E5E7EB"` | `border: "1px solid var(--border)"` |

---

### DSS-003: Typography Token Compliance

**Purpose**: Text styling should use typography tokens, not hardcoded values.

#### Detection Patterns

```text
# Hardcoded font-family
PATTERN: /font-family:\s*['"]?(?!var\(|inherit|unset)/
EXCLUDE: *.config.*, theme.*, tokens.*

# Hardcoded font-size (px values)
PATTERN: /font-size:\s*\d+px/
EXCLUDE: Same as above

# Hardcoded line-height
PATTERN: /line-height:\s*(?:\d+px|\d\.\d(?!rem))/
EXCLUDE: Same as above

# Tailwind arbitrary font values
PATTERN: /text-\[\d+px\]|font-\[['"][^var]/
```

#### Allowed Exceptions

1. **Token definition files**: Same as DSS-002
2. **Icon sizing**: Font-size for icon fonts with comment
3. **Third-party component overrides**: With documented exception
4. **Print stylesheets**: `@media print` contexts

---

## Vision Validation Integration

### Design System Vision Prompt

Use this prompt when running vision validation with design system context:

```text
Analyze this UI screenshot for design system compliance.

## Configured Design System

Framework: [FRAMEWORK]
Primary Color: [PRIMARY_HEX]
Secondary Color: [SECONDARY_HEX]
Font Family: [FONT_FAMILY]

## Checks

### DSS-002: Color Compliance
1. Compare visible colors against configured palette
2. Flag colors that appear inconsistent (>5% difference)
3. Check for obvious hardcoded colors vs. design tokens

### DSS-003: Typography Compliance
1. Verify font family consistency across text elements
2. Check font sizes align with configured scale
3. Flag non-standard typography that doesn't match tokens

### Component Consistency (DSS-001)
1. Identify UI components (buttons, inputs, cards, etc.)
2. Verify consistent styling within component types
3. Flag components that appear custom vs. library standard

## Output Format

For each issue found:
- ID: [DSS-00x]
- Element: [what UI element]
- Expected: [token/value from config]
- Actual: [what was detected]
- Severity: [based on enforcement_level]
```

### Color Tolerance Calculation

When comparing screenshot colors to tokens:

```text
Tolerance threshold: 5% (12.75 on 0-255 scale)

Algorithm:
1. Extract dominant color from element region
2. Convert both to RGB
3. Calculate Euclidean distance:
   distance = sqrt((r1-r2)² + (g1-g2)² + (b1-b2)²)
4. Max possible distance: 441.67 (black to white)
5. Percentage difference: (distance / 441.67) * 100
6. Flag if percentage > 5%
```

---

## Self-Review Criteria

Add these criteria to implementation self-review checklist:

### SR-IMPL-18: No Hardcoded Colors

```text
ID: SR-IMPL-18
Check: All color values reference design tokens
Method: Grep for hardcoded hex/RGB/HSL patterns
Pass: Zero matches outside allowed exceptions
Fail: Any hardcoded color in UI code
```

### SR-IMPL-19: Component Library Used

```text
ID: SR-IMPL-19
Check: Library components used where equivalent exists
Method: Analyze imports and component usage
Pass: No custom components duplicating library functionality
Fail: Custom component when library alternative exists
```

### SR-IMPL-20: Typography Tokens Used

```text
ID: SR-IMPL-20
Check: Typography values reference design tokens
Method: Grep for hardcoded font-family/size/weight patterns
Pass: Zero matches outside allowed exceptions
Fail: Any hardcoded typography in UI code
```

---

## Auto-Fix Rules

### AF-006: Hardcoded Hex to CSS Variable

```text
ID: AF-006
Trigger: Hardcoded hex color detected
Action: Replace with CSS variable reference

Before: color: "#3B82F6"
After:  color: "var(--primary)"

Before: className="text-[#3B82F6]"
After:  className="text-primary"

Logic:
1. Match hex to closest design token (Euclidean distance)
2. If distance < 5%, suggest token name
3. If distance >= 5%, warn about undefined color
```

### AF-007: Custom Component to Library Import

```text
ID: AF-007
Trigger: Custom component detected with library equivalent
Action: Suggest library import and usage

Before:
function CustomButton({ children, onClick }) {
  return <button onClick={onClick}>{children}</button>
}

After:
import { Button } from "@/components/ui/button"
// Use: <Button onClick={onClick}>{children}</Button>

Logic:
1. Identify component type from name/structure
2. Check if library equivalent exists for configured framework
3. Generate import statement and usage example
```

### AF-008: Hardcoded Font-Size to Token

```text
ID: AF-008
Trigger: Hardcoded font-size detected
Action: Replace with typography token

Before: font-size: "16px"
After:  font-size: "var(--text-base)" or className="text-base"

Before: style={{ fontSize: 14 }}
After:  style={{ fontSize: 'var(--text-sm)' }} or className="text-sm"

Logic:
1. Map px value to closest scale token
2. Account for rem conversion (base 16px)
3. Suggest appropriate CSS variable or utility class
```

---

## Integration with /speckit.analyze

### Pass Z: Design System Validation

Pass Z is activated when `design_system` block exists in constitution.md and `enforcement_level` is not `off`.

#### Validation Steps

```text
Pass Z: Design System Compliance

Z.1: Configuration Validation
    - Verify design_system block is valid YAML
    - Check required fields present (framework, enforcement_level)
    - Load preset if specified

Z.2: DSS-002 Color Compliance
    - Scan UI source files for color patterns
    - Exclude allowlisted files (*.config.*, tokens.*, etc.)
    - Report violations with file:line references

Z.3: DSS-001 Component Compliance
    - Scan for custom component patterns
    - Cross-reference with configured framework's component list
    - Report custom components with library alternatives

Z.4: DSS-003 Typography Compliance
    - Scan for hardcoded typography patterns
    - Report violations with suggested token replacements

Z.5: Token Coverage Analysis
    - Calculate % of UI code using design tokens
    - Report token utilization metrics
```

#### Report Output

```markdown
## Pass Z: Design System Compliance

**Framework**: [configured framework]
**Enforcement**: [strict/warn/off]
**Token Coverage**: [X]%

### Violations

| ID | File | Line | Issue | Severity |
|----|------|------|-------|----------|
| DSS-002 | src/Button.tsx | 15 | Hardcoded color: #3B82F6 | HIGH |
| DSS-001 | src/CustomModal.tsx | 1 | Custom component, use Dialog from library | MEDIUM |
| DSS-003 | src/Header.tsx | 22 | Hardcoded font-size: 24px | MEDIUM |

### Token Utilization

| Category | Tokens Defined | Tokens Used | Coverage |
|----------|---------------|-------------|----------|
| Colors | 8 | 6 | 75% |
| Typography | 7 | 5 | 71% |
| Spacing | 4 | 2 | 50% |
```

---

## Error Messages

### DSS-001 Violation

```text
[DSS-001] Component Library Violation
Location: src/components/CustomButton.tsx:15
Message: Custom button component detected. Framework 'shadcn/ui' provides <Button>.
Suggestion: Import from '@/components/ui/button' instead of creating custom.
Severity: MEDIUM (warn mode) | HIGH (strict mode)
```

### DSS-002 Violation

```text
[DSS-002] Color Token Violation
Location: src/styles/header.css:42
Message: Hardcoded color '#FF5733' not in design system.
Closest token: 'destructive' (#EF4444, 8% difference)
Suggestion: Use 'var(--destructive)' or add token to constitution.md
Severity: HIGH (warn mode) | CRITICAL (strict mode)
```

### DSS-003 Violation

```text
[DSS-003] Typography Token Violation
Location: src/components/Title.tsx:8
Message: Hardcoded font-size '24px' should use typography token.
Suggestion: Use 'var(--text-2xl)' or 'text-2xl' class (24px = 1.5rem)
Severity: MEDIUM (warn mode) | HIGH (strict mode)
```

---

## Skip Conditions

Design System Enforcement is skipped when:

1. **No configuration**: `design_system` block missing from constitution.md
2. **Enforcement disabled**: `enforcement_level: "off"`
3. **Non-UI project**: No frontend framework detected in Technology Constraints
4. **API-only features**: Feature spec has no UI components (`[VR:*]` markers absent)
5. **Backend files**: Files in `server/`, `api/`, `backend/`, `lib/` directories

When skipped:
- Pass Z is marked as `SKIPPED` in analyze report
- SR-IMPL-18/19/20 are marked as `N/A` in self-review
- Vision validation skips design system checks

---

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|------------|
| False positives in config files | Exclude patterns not matching | Add file to allowlist pattern |
| Unknown color token suggestions | Token not defined in config | Add token to constitution.md theme.colors |
| Wrong library component suggested | Framework mismatch | Verify framework setting matches project |
| Pass Z not running | Missing design_system block | Add configuration to constitution.md |
| Vision validation inaccurate colors | Screenshot quality/compression | Use PNG format, verify color profile |
