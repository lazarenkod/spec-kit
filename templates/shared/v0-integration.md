# v0.dev Integration Guide

Integration guide for using Vercel's v0.dev AI to generate React components from design specifications.

## Overview

v0.dev generates React components using shadcn/ui and Tailwind CSS. This integration enables:

- **Component generation**: Convert design specs to production code
- **Design token injection**: Apply your design system to generated code
- **Iterative refinement**: Modify and improve generated components
- **Export ready**: Output directly to your codebase

## Configuration

### Environment Variables

```bash
# .env or constitution.md reference
V0_API_KEY=v0_xxxxx           # v0.dev API key (when API available)
```

### constitution.md Configuration

```yaml
design_system:
  ai_generation:
    enabled: true
    provider: "v0.dev"
    mode: "manual"              # manual | api (when available)
    cache:
      enabled: true
      ttl_hours: 24
      storage: ".speckit/cache/v0"
    fallback: "template"        # Use templates if v0 unavailable
```

## Generation Modes

### Manual Mode (Current)

When v0 API is not available, use the web interface:

```text
MANUAL_WORKFLOW:

1. Build prompt from design spec:
   - Read templates/shared/v0-prompts.md
   - Inject design tokens
   - Include component requirements

2. Present prompt to user:
   "Copy this prompt to v0.dev and paste the result:"
   [formatted prompt]

3. User interaction:
   - User goes to v0.dev
   - Pastes prompt
   - Copies generated code
   - Pastes back to terminal

4. Process result:
   - Validate against design system
   - Apply any token corrections
   - Save to .preview/components/
```

### API Mode (Future)

When v0 API becomes available:

```text
API_WORKFLOW:

1. Build request:
   POST https://api.v0.dev/generate
   Headers:
     Authorization: Bearer {V0_API_KEY}
     Content-Type: application/json
   Body:
     {
       "prompt": {built_prompt},
       "framework": "react",
       "styling": "tailwind",
       "typescript": true
     }

2. Poll for completion:
   GET https://api.v0.dev/generations/{id}

3. Retrieve code:
   Extract component code from response

4. Process and save
```

## Prompt Engineering

### System Prompt Template

```text
You are generating a React component using:
- Framework: React with TypeScript
- Styling: Tailwind CSS
- Component Library: shadcn/ui
- Icons: Lucide React

Design System Tokens:
```yaml
colors:
  primary: "{tokens.colors.primary}"
  secondary: "{tokens.colors.secondary}"
  background: "{tokens.colors.background}"
  foreground: "{tokens.colors.foreground}"
  muted: "{tokens.colors.muted}"
  accent: "{tokens.colors.accent}"
  destructive: "{tokens.colors.destructive}"
  border: "{tokens.colors.border}"

typography:
  font_family: "{tokens.typography.font_family}"
  font_sizes:
    sm: "{tokens.typography.scale.sm}"
    base: "{tokens.typography.scale.base}"
    lg: "{tokens.typography.scale.lg}"

spacing:
  unit: "{tokens.spacing.unit}"
  scale: [0, 1, 2, 3, 4, 5, 6, 8, 10, 12]

radii:
  sm: "{tokens.radii.sm}"
  md: "{tokens.radii.md}"
  lg: "{tokens.radii.lg}"
```

Requirements:
- Use CSS variables for colors (e.g., `bg-primary` maps to `var(--primary)`)
- Include all component states
- Make fully accessible (ARIA, keyboard nav)
- Support dark mode via class strategy
- Export both component and types
```

### Component Prompt Template

```text
Create a {component_name} component with the following specifications:

## Purpose
{component.purpose}

## States
{FOR state IN component.states}
- {state.name}: {state.description}
{ENDFOR}

## Variants
{FOR variant IN component.variants}
- {variant.name}: {variant.description}
{ENDFOR}

## Size Variants
{FOR size IN component.sizes}
- {size.name}: height={size.height}, padding={size.padding}, fontSize={size.font_size}
{ENDFOR}

## Props Interface
```typescript
interface {ComponentName}Props {
  {FOR prop IN component.props}
  {prop.name}{prop.optional ? "?" : ""}: {prop.type}; // {prop.description}
  {ENDFOR}
}
```

## Accessibility Requirements
- Role: {component.a11y.role}
- Keyboard: {component.a11y.keyboard}
- ARIA: {component.a11y.aria}
- Focus: {component.a11y.focus}

## Example Usage
```tsx
<{ComponentName}
  {FOR prop IN component.example_props}
  {prop.name}={prop.value}
  {ENDFOR}
/>
```

Please generate a production-ready component that:
1. Uses shadcn/ui primitives where applicable
2. Implements all states and variants using CVA
3. Includes proper TypeScript types
4. Has accessible focus management
5. Supports the design tokens provided
```

## Design Token Injection

### Token Mapping

```text
FUNCTION inject_design_tokens(prompt, constitution):

  tokens = load_design_tokens(constitution)

  # Map token values to Tailwind classes
  tailwind_mapping = {
    colors: {
      primary: "primary",           # bg-primary, text-primary
      secondary: "secondary",
      background: "background",
      foreground: "foreground",
      muted: "muted",
      accent: "accent",
      destructive: "destructive",
      border: "border",
    },
    spacing: {
      1: "1",    # p-1, m-1, gap-1
      2: "2",
      3: "3",
      4: "4",
      6: "6",
      8: "8",
    },
    radii: {
      sm: "sm",  # rounded-sm
      md: "md",
      lg: "lg",
      xl: "xl",
      full: "full",
    }
  }

  # Inject into prompt
  prompt = prompt.replace("{tokens.colors.primary}", tokens.colors.primary)
  # ... repeat for all tokens

  RETURN prompt
```

### CSS Variables Setup

Generated components expect these CSS variables:

```css
/* globals.css or tailwind.config.js */
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --card: 0 0% 100%;
  --card-foreground: 222.2 84% 4.9%;
  --popover: 0 0% 100%;
  --popover-foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
  --secondary: 210 40% 96.1%;
  --secondary-foreground: 222.2 47.4% 11.2%;
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;
  --accent: 210 40% 96.1%;
  --accent-foreground: 222.2 47.4% 11.2%;
  --destructive: 0 84.2% 60.2%;
  --destructive-foreground: 210 40% 98%;
  --border: 214.3 31.8% 91.4%;
  --input: 214.3 31.8% 91.4%;
  --ring: 222.2 84% 4.9%;
  --radius: 0.5rem;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  /* ... dark mode values */
}
```

## Component Categories

### Supported Component Types

| Category | Components | v0 Support |
|----------|------------|------------|
| **Forms** | Input, Select, Checkbox, Radio, Switch, Slider | Excellent |
| **Actions** | Button, IconButton, ToggleGroup | Excellent |
| **Layout** | Card, Dialog, Drawer, Sheet, Tabs | Excellent |
| **Feedback** | Alert, Toast, Progress, Skeleton | Good |
| **Navigation** | Tabs, Breadcrumb, Pagination, Menu | Good |
| **Data** | Table, DataTable, List | Good |
| **Complex** | DatePicker, Combobox, Command | Moderate |

### Component Complexity Tiers

```text
COMPLEXITY_TIERS:

  simple:
    - Button, Input, Checkbox, Radio, Switch
    - Single file, no sub-components
    - v0 handles well

  moderate:
    - Card, Dialog, Tabs, Alert, Toast
    - May have sub-components
    - v0 handles with guidance

  complex:
    - DataTable, DatePicker, Combobox
    - Multiple files, many states
    - May need manual refinement

FUNCTION determine_complexity(component):
  IF component.sub_components > 0:
    RETURN "moderate"
  IF component.states.length > 5:
    RETURN "moderate"
  IF component.has_external_deps:
    RETURN "complex"
  RETURN "simple"
```

## Validation Pipeline

### Post-Generation Validation

```text
FUNCTION validate_generated_code(code, spec):

  issues = []

  # 1. TypeScript Check
  ts_result = typescript_check(code)
  IF ts_result.errors:
    issues.append({
      type: "typescript",
      severity: "error",
      details: ts_result.errors
    })

  # 2. Design Token Usage
  hardcoded_colors = find_hardcoded_colors(code)
  IF hardcoded_colors:
    issues.append({
      type: "tokens",
      severity: "warning",
      details: f"Found hardcoded colors: {hardcoded_colors}"
    })

  # 3. Accessibility Check
  a11y_result = check_accessibility(code)
  IF a11y_result.missing_aria:
    issues.append({
      type: "accessibility",
      severity: "error",
      details: a11y_result.missing_aria
    })

  # 4. Component States
  missing_states = spec.states - extract_states(code)
  IF missing_states:
    issues.append({
      type: "completeness",
      severity: "warning",
      details: f"Missing states: {missing_states}"
    })

  # 5. Props Interface Match
  IF NOT props_match(code, spec.props):
    issues.append({
      type: "interface",
      severity: "error",
      details: "Props interface doesn't match specification"
    })

  RETURN ValidationResult(
    passed=len([i for i in issues if i.severity == "error"]) == 0,
    issues=issues
  )
```

### Auto-Correction

```text
FUNCTION auto_correct(code, issues):

  FOR issue IN issues:

    IF issue.type == "tokens" AND issue.severity == "warning":
      # Replace hardcoded colors with tokens
      FOR color IN issue.details:
        code = code.replace(color, map_to_token(color))

    IF issue.type == "accessibility":
      # Add missing ARIA attributes
      code = inject_aria_attributes(code, issue.details)

  RETURN code
```

## Caching Strategy

### Cache Structure

```text
.speckit/cache/v0/
├── manifest.json           # Cache index
├── button/
│   ├── spec.hash           # Hash of input spec
│   ├── code.tsx            # Generated code
│   └── metadata.json       # Generation metadata
├── card/
│   └── ...
└── data-table/
    └── ...
```

### Cache Logic

```text
FUNCTION get_or_generate(component_spec):

  cache_key = hash(component_spec + design_tokens)
  cache_path = f".speckit/cache/v0/{component_spec.name}"

  # Check cache
  IF exists(cache_path) AND cache_valid(cache_path, cache_key):
    LOG f"Cache hit for {component_spec.name}"
    RETURN read_cached(cache_path)

  # Generate new
  LOG f"Generating {component_spec.name} via v0.dev"
  code = generate_via_v0(component_spec)

  # Validate
  validation = validate_generated_code(code, component_spec)
  IF NOT validation.passed:
    code = auto_correct(code, validation.issues)

  # Cache
  write_cache(cache_path, code, cache_key)

  RETURN code


FUNCTION cache_valid(cache_path, expected_hash):
  stored_hash = read(f"{cache_path}/spec.hash")
  metadata = read_json(f"{cache_path}/metadata.json")

  # Check hash match
  IF stored_hash != expected_hash:
    RETURN false

  # Check TTL
  IF now() - metadata.generated_at > TTL_HOURS * 3600:
    RETURN false

  RETURN true
```

## Error Handling

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Import errors | Missing shadcn component | Run `npx shadcn-ui@latest add {component}` |
| Type errors | Incomplete props | Add missing props to interface |
| Style mismatch | Wrong token mapping | Check CSS variables match constitution |
| Missing state | Incomplete prompt | Add state to prompt, regenerate |
| A11y warnings | Missing ARIA | Auto-inject or manual fix |

### Fallback Strategy

```text
IF v0_generation_fails:

  1. Log error with details
  2. Check if template available:
     template_path = f"templates/components/{component.name}.tsx"
     IF exists(template_path):
       RETURN use_template(template_path, component)

  3. If no template, generate minimal:
     RETURN generate_minimal_component(component)

  4. Notify user:
     WARN "v0 generation failed, using fallback template"
```

## Best Practices

### Do's

- ✅ Always include design tokens in prompt
- ✅ Specify all states explicitly
- ✅ Include accessibility requirements
- ✅ Validate generated code before saving
- ✅ Cache successful generations
- ✅ Use TypeScript strict mode

### Don'ts

- ❌ Skip validation step
- ❌ Use hardcoded colors in prompts
- ❌ Ignore accessibility requirements
- ❌ Generate without design system context
- ❌ Trust generated code without review
- ❌ Regenerate when cached version exists

## Example: Full Generation Flow

```text
INPUT: Button component spec from design.md

1. Load spec:
   {
     name: "Button",
     states: ["default", "hover", "active", "focus", "disabled", "loading"],
     variants: ["primary", "secondary", "ghost", "destructive"],
     sizes: ["sm", "md", "lg"]
   }

2. Build prompt:
   - Load system prompt template
   - Inject design tokens from constitution
   - Add component-specific requirements

3. Generate:
   - Mode: manual (present prompt to user)
   - User pastes to v0.dev
   - User copies result back

4. Validate:
   - TypeScript: ✓
   - Tokens: ✓ (all colors use variables)
   - A11y: ✓ (has aria-disabled, focus ring)
   - States: ✓ (all 6 states implemented)
   - Interface: ✓ (matches spec)

5. Save:
   - .preview/components/button/button.tsx
   - .preview/components/button/button.stories.tsx
   - Cache to .speckit/cache/v0/button/

6. Report:
   "✓ Button component generated successfully"
   "  States: 6/6"
   "  Variants: 4/4"
   "  DQS: 95/100"
```

## Integration Points

| Command | v0 Usage |
|---------|----------|
| `/speckit.design` | Optional component generation step |
| `/speckit.design-generate` | Primary component generation |
| `/speckit.preview` | Generate components for preview |
| `/speckit.implement` | Use cached/generated components |

## Future Enhancements

When v0 API becomes publicly available:

1. **Batch generation**: Generate multiple components in parallel
2. **Iteration**: Refine generated code with follow-up prompts
3. **Version control**: Track generation history
4. **Team sharing**: Share cached components across team
5. **Custom models**: Fine-tune for specific design systems
