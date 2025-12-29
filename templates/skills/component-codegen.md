# Component Code Generation Skill

Skill for generating React/Vue/Svelte components from design specifications using templates and patterns.

## Trigger Conditions

Use this skill when:
- v0.dev is unavailable or not configured
- Need simple/medium complexity components
- Want deterministic, template-based output
- Generating components without external API calls

## Prerequisites

```yaml
required_files:
  - design.md (with component specifications)
  - constitution.md (for design tokens and framework)

optional_files:
  - existing components for pattern matching
```

## Component Complexity Assessment

```text
FUNCTION assess_complexity(component):

  score = 0

  # State complexity
  score += len(component.states) * 2

  # Variant complexity
  score += len(component.variants) * 1.5

  # Props complexity
  score += len(component.props) * 1

  # Interaction complexity
  IF component.has_animations:
    score += 5
  IF component.has_form_elements:
    score += 3
  IF component.has_async_operations:
    score += 4

  # Determine tier
  IF score < 10:
    RETURN "simple"
  ELIF score < 25:
    RETURN "moderate"
  ELSE:
    RETURN "complex"
```

## Template Library

### Base Component Template

```tsx
// {ComponentName}.tsx
import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const {componentName}Variants = cva(
  // Base styles
  '{baseStyles}',
  {
    variants: {
      variant: {
        {variants}
      },
      size: {
        {sizes}
      },
    },
    defaultVariants: {
      variant: '{defaultVariant}',
      size: '{defaultSize}',
    },
  }
)

export interface {ComponentName}Props
  extends React.{HTMLElement}HTMLAttributes<HTML{HTMLElement}Element>,
    VariantProps<typeof {componentName}Variants> {
  {additionalProps}
}

const {ComponentName} = React.forwardRef<HTML{HTMLElement}Element, {ComponentName}Props>(
  ({ className, variant, size, {destructuredProps}, ...props }, ref) => {
    return (
      <{htmlElement}
        className={cn({componentName}Variants({ variant, size, className }))}
        ref={ref}
        {...props}
      >
        {children}
      </{htmlElement}>
    )
  }
)
{ComponentName}.displayName = '{ComponentName}'

export { {ComponentName}, {componentName}Variants }
```

### Button Template

```text
TEMPLATE button:

  base_styles: """
    inline-flex items-center justify-center whitespace-nowrap rounded-md
    text-sm font-medium ring-offset-background transition-colors
    focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring
    focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50
  """

  variants:
    default: "bg-primary text-primary-foreground hover:bg-primary/90"
    destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90"
    outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground"
    secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80"
    ghost: "hover:bg-accent hover:text-accent-foreground"
    link: "text-primary underline-offset-4 hover:underline"

  sizes:
    default: "h-10 px-4 py-2"
    sm: "h-9 rounded-md px-3"
    lg: "h-11 rounded-md px-8"
    icon: "h-10 w-10"

  html_element: "button"

  additional_props:
    - "asChild?: boolean"
    - "loading?: boolean"
```

### Input Template

```text
TEMPLATE input:

  base_styles: """
    flex h-10 w-full rounded-md border border-input bg-background px-3 py-2
    text-sm ring-offset-background file:border-0 file:bg-transparent
    file:text-sm file:font-medium placeholder:text-muted-foreground
    focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring
    focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50
  """

  variants:
    default: ""
    error: "border-destructive focus-visible:ring-destructive"

  sizes:
    default: "h-10"
    sm: "h-9 text-xs"
    lg: "h-12 text-base"

  html_element: "input"

  additional_props:
    - "error?: boolean"
    - "errorMessage?: string"
```

### Card Template

```text
TEMPLATE card:

  base_styles: """
    rounded-lg border bg-card text-card-foreground shadow-sm
  """

  sub_components:
    - CardHeader: "flex flex-col space-y-1.5 p-6"
    - CardTitle: "text-2xl font-semibold leading-none tracking-tight"
    - CardDescription: "text-sm text-muted-foreground"
    - CardContent: "p-6 pt-0"
    - CardFooter: "flex items-center p-6 pt-0"

  html_element: "div"
```

### Dialog Template

```text
TEMPLATE dialog:

  requires: "@radix-ui/react-dialog"

  sub_components:
    - DialogTrigger
    - DialogPortal
    - DialogOverlay: """
        fixed inset-0 z-50 bg-black/80
        data-[state=open]:animate-in data-[state=closed]:animate-out
        data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0
      """
    - DialogContent: """
        fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%]
        translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg
        duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out
        data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0
        data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95
        data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%]
        data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%]
        sm:rounded-lg
      """
    - DialogHeader: "flex flex-col space-y-1.5 text-center sm:text-left"
    - DialogFooter: "flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2"
    - DialogTitle: "text-lg font-semibold leading-none tracking-tight"
    - DialogDescription: "text-sm text-muted-foreground"
    - DialogClose

  html_element: "div"
```

## Generation Pipeline

### 1. Parse Component Spec

```text
FUNCTION parse_component_spec(design_md, component_name):

  # Find component section in design.md
  component_section = extract_section(design_md, f"### {component_name}")

  IF NOT component_section:
    RETURN null

  # Parse YAML/structured content
  spec = {
    name: component_name,
    purpose: extract_field(component_section, "Purpose"),
    states: parse_list(component_section, "States"),
    variants: parse_list(component_section, "Variants"),
    sizes: parse_list(component_section, "Sizes"),
    props: parse_props(component_section, "Props"),
    a11y: parse_a11y(component_section, "Accessibility"),
  }

  RETURN spec
```

### 2. Select Template

```text
FUNCTION select_template(spec):

  # Match by component type
  component_type = classify_component(spec.name, spec.purpose)

  template_map = {
    "button": "button",
    "input": "input",
    "textarea": "input",
    "select": "select",
    "checkbox": "checkbox",
    "radio": "radio",
    "switch": "switch",
    "card": "card",
    "dialog": "dialog",
    "modal": "dialog",
    "drawer": "drawer",
    "sheet": "drawer",
    "tabs": "tabs",
    "accordion": "accordion",
    "dropdown": "dropdown",
    "menu": "dropdown",
    "tooltip": "tooltip",
    "popover": "popover",
    "alert": "alert",
    "toast": "toast",
    "badge": "badge",
    "avatar": "avatar",
    "progress": "progress",
    "skeleton": "skeleton",
  }

  IF component_type IN template_map:
    RETURN load_template(template_map[component_type])
  ELSE:
    RETURN load_template("generic")
```

### 3. Apply Spec to Template

```text
FUNCTION apply_spec_to_template(template, spec, tokens):

  code = template.code

  # Replace placeholders
  code = code.replace("{ComponentName}", spec.name)
  code = code.replace("{componentName}", camel_case(spec.name))
  code = code.replace("{baseStyles}", build_base_styles(spec, tokens))

  # Build variants
  variants_code = build_variants(spec.variants, tokens)
  code = code.replace("{variants}", variants_code)

  # Build sizes
  sizes_code = build_sizes(spec.sizes, tokens)
  code = code.replace("{sizes}", sizes_code)

  # Build props
  props_code = build_props_interface(spec.props)
  code = code.replace("{additionalProps}", props_code)

  # Set HTML element
  code = code.replace("{htmlElement}", template.html_element)
  code = code.replace("{HTMLElement}", pascal_case(template.html_element))

  # Handle children
  IF spec.has_children:
    code = code.replace("{children}", "{children}")
  ELSE:
    code = code.replace("{children}", "")

  RETURN code


FUNCTION build_variants(variants, tokens):

  lines = []

  FOR variant IN variants:
    styles = map_variant_to_styles(variant, tokens)
    lines.append(f"        {variant.name}: \"{styles}\",")

  RETURN "\n".join(lines)


FUNCTION build_sizes(sizes, tokens):

  lines = []

  FOR size IN sizes:
    height = tokens.spacing[size.height] OR size.height
    padding = tokens.spacing[size.padding] OR size.padding
    font = tokens.typography[size.font_size] OR size.font_size

    styles = f"h-{height} px-{padding} text-{font}"
    lines.append(f"        {size.name}: \"{styles}\",")

  RETURN "\n".join(lines)
```

### 4. Add Accessibility

```text
FUNCTION add_accessibility(code, spec):

  a11y = spec.a11y

  # Add role if not implicit
  IF a11y.role AND a11y.role != "button":
    code = add_attribute(code, f'role="{a11y.role}"')

  # Add aria-label pattern
  IF a11y.needs_label:
    code = add_prop(code, "ariaLabel?: string")
    code = add_attribute(code, 'aria-label={ariaLabel}')

  # Add aria-describedby for hints
  IF a11y.has_description:
    code = add_prop(code, "ariaDescribedBy?: string")
    code = add_attribute(code, 'aria-describedby={ariaDescribedBy}')

  # Add keyboard handlers
  IF a11y.keyboard:
    code = add_keyboard_handlers(code, a11y.keyboard)

  # Add focus management
  IF a11y.focus:
    code = add_focus_management(code, a11y.focus)

  RETURN code


FUNCTION add_keyboard_handlers(code, keyboard_spec):

  handlers = []

  IF "Enter" IN keyboard_spec OR "Space" IN keyboard_spec:
    handlers.append("""
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          onClick?.(e as any)
        }
      }}
    """)

  IF "Escape" IN keyboard_spec:
    handlers.append("""
      onKeyDown={(e) => {
        if (e.key === 'Escape') {
          onClose?.()
        }
      }}
    """)

  FOR handler IN handlers:
    code = inject_prop(code, handler)

  RETURN code
```

### 5. Generate Sub-Components

```text
FUNCTION generate_sub_components(template, spec):

  IF NOT template.sub_components:
    RETURN []

  components = []

  FOR sub IN template.sub_components:
    sub_code = f"""
const {sub.name} = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }}, ref) => (
  <div
    ref={{ref}}
    className={{cn("{sub.styles}", className)}}
    {{...props}}
  />
))
{sub.name}.displayName = "{sub.name}"
"""
    components.append({
      name: sub.name,
      code: sub_code
    })

  RETURN components
```

### 6. Output Files

```text
FUNCTION output_component(spec, code, sub_components, output_dir):

  component_dir = f"{output_dir}/{kebab_case(spec.name)}"
  mkdir_p(component_dir)

  # Main component with sub-components
  full_code = code
  FOR sub IN sub_components:
    full_code += "\n\n" + sub.code

  # Add exports
  exports = [spec.name] + [s.name FOR s IN sub_components]
  full_code += f"\n\nexport {{ {', '.join(exports)} }}"

  write(f"{component_dir}/{spec.name}.tsx", full_code)

  # Generate index
  write(f"{component_dir}/index.ts", f"export * from './{spec.name}'")

  RETURN {
    main: f"{component_dir}/{spec.name}.tsx",
    index: f"{component_dir}/index.ts"
  }
```

## Complete Pipeline

```text
FUNCTION component_codegen_pipeline(component_name):

  # 1. Load context
  design_md = read("design.md")
  constitution = read("constitution.md")
  tokens = extract_design_tokens(constitution)

  # 2. Parse spec
  spec = parse_component_spec(design_md, component_name)
  IF NOT spec:
    ERROR f"Component '{component_name}' not found in design.md"

  # 3. Assess complexity
  complexity = assess_complexity(spec)
  LOG f"Component complexity: {complexity}"

  IF complexity == "complex":
    WARN "Complex component - consider using v0.dev for better results"

  # 4. Select template
  template = select_template(spec)

  # 5. Apply spec
  code = apply_spec_to_template(template, spec, tokens)

  # 6. Add accessibility
  code = add_accessibility(code, spec)

  # 7. Generate sub-components
  sub_components = generate_sub_components(template, spec)

  # 8. Output
  output_dir = ".preview/components"
  files = output_component(spec, code, sub_components, output_dir)

  RETURN {
    code: code,
    files: files,
    complexity: complexity
  }
```

## Framework Adapters

### Vue Adapter

```text
FUNCTION adapt_to_vue(react_code, spec):

  vue_template = """
<script setup lang="ts">
import { computed } from 'vue'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

{variantsDefinition}

interface Props {
  {propsInterface}
}

const props = withDefaults(defineProps<Props>(), {
  {defaultProps}
})

const classes = computed(() =>
  cn({componentName}Variants({
    variant: props.variant,
    size: props.size,
  }), props.class)
)
</script>

<template>
  <{element} :class="classes" v-bind="$attrs">
    <slot />
  </{element}>
</template>
"""

  # Convert React to Vue
  vue_code = vue_template
  vue_code = inject_variants(vue_code, react_code)
  vue_code = convert_props_to_vue(vue_code, spec.props)

  RETURN vue_code
```

### Svelte Adapter

```text
FUNCTION adapt_to_svelte(react_code, spec):

  svelte_template = """
<script lang="ts">
  import { cva, type VariantProps } from 'class-variance-authority'
  import { cn } from '$lib/utils'

  {variantsDefinition}

  type $$Props = {propsInterface}

  export let variant: $$Props['variant'] = '{defaultVariant}'
  export let size: $$Props['size'] = '{defaultSize}'
  let className: string = ''
  export { className as class }

  $: classes = cn({componentName}Variants({ variant, size }), className)
</script>

<{element} class={classes} {...$$restProps}>
  <slot />
</{element}>
"""

  svelte_code = svelte_template
  svelte_code = inject_variants(svelte_code, react_code)
  svelte_code = convert_props_to_svelte(svelte_code, spec.props)

  RETURN svelte_code
```

## Usage Example

```text
# Generate Button component

result = component_codegen_pipeline("Button")

# Output:
{
  code: "// Full Button component code...",
  files: {
    main: ".preview/components/button/Button.tsx",
    index: ".preview/components/button/index.ts"
  },
  complexity: "simple"
}
```

## Fallback Behavior

This skill serves as fallback when:
- v0.dev is unavailable
- API quota exceeded
- Manual v0 workflow rejected by user
- Simple components that don't need AI generation

```text
IF v0_generation_fails:
  LOG "Falling back to template-based generation"
  RETURN component_codegen_pipeline(component_name)
```
