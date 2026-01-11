# v0.dev Generation Skill

Skill for generating production-ready React components using Vercel's v0.dev AI.

## Trigger Conditions

Use this skill when:
- Generating React/Vue/Svelte components from design specs
- Converting component specifications to production code
- Need high-quality, accessible UI components
- Design.md contains component specifications

## Prerequisites

```yaml
required_files:
  - design.md (with component specifications)
  - constitution.md (for design tokens)

optional_files:
  - .speckit/cache/v0/ (component cache)
```

## Execution Flow

### 1. Load Design Context

```text
FUNCTION load_design_context():

  # Load design tokens from constitution
  constitution = read("constitution.md")
  tokens = extract_design_tokens(constitution)

  # Load component spec from design.md
  design = read("design.md")
  components = extract_component_specs(design)

  RETURN {
    tokens: tokens,
    components: components,
    framework: constitution.design_system.framework OR "react"
  }
```

### 2. Load Few-Shot Examples (NEW v0.2.0)

```text
FUNCTION load_few_shot_examples(component_type):
  """
  Load high-quality implementation examples for the component type.

  Research shows 3-5 examples provide optimal few-shot performance.
  Examples include full TypeScript code, accessibility patterns,
  and anti-pattern prevention guidance.
  """

  # Normalize component type to match file names
  normalized_type = component_type.lower().replace(" ", "-")

  # Map common component types to example files
  type_map = {
    "button": "button-examples",
    "input": "input-examples",
    "form": "form-examples",
    "card": "card-examples",
    "navigation": "navigation-examples",
    "nav": "navigation-examples",
    "modal": "modal-examples",
    "dialog": "modal-examples",
    "table": "table-examples",
    "list": "list-examples",
    "avatar": "avatar-examples",
    "badge": "badge-examples"
  }

  # Get mapped file name or use normalized type
  file_name = type_map.get(normalized_type, f"{normalized_type}-examples")
  examples_path = f"templates/shared/few-shot-examples/{file_name}.md"

  IF exists(examples_path):
    LOG f"Loading few-shot examples for {component_type} from {examples_path}"
    examples = read(examples_path)
    RETURN examples

  LOG f"No few-shot examples found for {component_type}"
  RETURN null
```

### 3. Code Optimization (NEW v0.4.0)

```text
FUNCTION optimize_component_code(code, component_name):
  """
  Apply performance and quality optimizations to generated component code.
  Ensures production-ready output that meets Core Web Vitals targets.
  """

  optimizations = {
    bundle_size: {},
    performance: {},
    validation: {}
  }

  # 1. Bundle Size Optimization
  # Target: Max 5KB gzipped per component
  original_size = calculate_gzipped_size(code)

  # 1.1 Tree Shaking
  # Remove unused imports and dead code
  code = remove_unused_imports(code)
  code = remove_dead_code(code)

  # 1.2 Code Splitting
  # Extract large dependencies to separate chunks
  IF component_has_icons AND icon_count > 5:
    code = extract_icon_imports(code)
    # Dynamic import: const Icons = await import('./icons');

  IF component_has_charts:
    code = lazy_load_chart_library(code)
    # const Chart = lazy(() => import('recharts'));

  # 1.3 Minification-Friendly Patterns
  # Use shorter variable names in production
  code = use_consistent_naming(code)

  optimized_size = calculate_gzipped_size(code)
  optimizations.bundle_size = {
    original: original_size,
    optimized: optimized_size,
    savings: f"{((original_size - optimized_size) / original_size * 100):.1f}%"
  }

  IF optimized_size > 5120:  # 5KB in bytes
    WARN f"Component {component_name} exceeds 5KB target ({optimized_size} bytes)"

  # 2. Performance Optimization

  # 2.1 Automatic Memoization
  # Wrap expensive components in React.memo
  IF component_has_complex_render:
    code = wrap_with_memo(code, component_name)
    # export const Button = memo(function Button(props) { ... });

  # 2.2 Callback Optimization
  # Wrap event handlers in useCallback
  handlers = extract_event_handlers(code)
  FOR handler IN handlers:
    IF handler.is_inline:
      code = wrap_handler_with_useCallback(code, handler)

  # 2.3 Expensive Calculations
  # Wrap computations in useMemo
  calculations = detect_expensive_calculations(code)
  FOR calc IN calculations:
    IF calc.runs_on_every_render:
      code = wrap_with_useMemo(code, calc)

  # 2.4 Lazy Loading
  # Dynamic imports for non-critical components
  IF component_has_modal OR component_has_drawer:
    code = add_lazy_loading(code)
    # const Modal = lazy(() => import('./Modal'));

  optimizations.performance = {
    memoization: "auto",
    lazy_loading: component_has_modal OR component_has_drawer,
    callbacks_optimized: len(handlers),
    memos_added: len(calculations)
  }

  # 3. Validation

  # 3.1 Lighthouse Accessibility Score
  # Target: >= 90
  a11y_issues = run_axe_core(code)
  IF a11y_issues:
    FOR issue IN a11y_issues:
      IF issue.severity == "critical":
        code = fix_accessibility_issue(code, issue)

  # 3.2 TypeScript Strict Mode
  ts_errors = run_typescript_check(code, strict_mode=true)
  IF ts_errors:
    FOR error IN ts_errors:
      code = fix_typescript_error(code, error)

  # 3.3 ESLint Rules
  eslint_warnings = run_eslint(code, rules={
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "warn",
    "jsx-a11y/alt-text": "error",
    "jsx-a11y/anchor-is-valid": "error"
  })

  optimizations.validation = {
    lighthouse_a11y_score: calculate_a11y_score(code),
    typescript_strict: len(ts_errors) == 0,
    eslint_clean: len([w for w in eslint_warnings if w.severity == "error"]) == 0
  }

  # 4. Generate Optimization Report
  report = f"""
  ## Code Optimization Report: {component_name}

  ### Bundle Size
  - Original: {original_size} bytes
  - Optimized: {optimized_size} bytes
  - Savings: {optimizations.bundle_size.savings}
  - Status: {"✓ PASS" if optimized_size <= 5120 else "⚠ WARN"}

  ### Performance
  - Memoization: {optimizations.performance.memoization}
  - Lazy loading: {"✓ Enabled" if optimizations.performance.lazy_loading else "○ Not needed"}
  - Callbacks optimized: {optimizations.performance.callbacks_optimized}
  - Memos added: {optimizations.performance.memos_added}

  ### Validation
  - Lighthouse A11y: {optimizations.validation.lighthouse_a11y_score}/100
  - TypeScript strict: {"✓ PASS" if optimizations.validation.typescript_strict else "✗ FAIL"}
  - ESLint: {"✓ CLEAN" if optimizations.validation.eslint_clean else "⚠ WARNINGS"}
  """

  write(f".speckit/reports/optimization-{component_name}.md", report)

  RETURN {
    code: code,
    optimizations: optimizations,
    report: report
  }


# Helper Functions

FUNCTION calculate_gzipped_size(code):
  import gzip
  compressed = gzip.compress(code.encode('utf-8'))
  RETURN len(compressed)

FUNCTION remove_unused_imports(code):
  # Parse AST to find unused imports
  imports = parse_imports(code)
  used_identifiers = extract_used_identifiers(code)

  FOR import_statement IN imports:
    imported_names = import_statement.names
    FOR name IN imported_names:
      IF name NOT IN used_identifiers:
        code = code.replace(import_statement.line, "")

  RETURN code

FUNCTION wrap_with_memo(code, component_name):
  # Add React.memo wrapper
  pattern = f"export (const|function) {component_name}"
  replacement = f"export const {component_name} = memo(function {component_name}"

  code = regex_replace(code, pattern, replacement)

  # Add memo import if not present
  IF "memo" NOT IN code:
    code = add_import(code, "react", ["memo"])

  RETURN code

FUNCTION wrap_handler_with_useCallback(code, handler):
  # Detect inline handlers
  pattern = f"{handler.prop}={{\\(.*?\\) => (.*?)}}"

  # Extract to useCallback
  callback_code = f"""
  const {handler.name} = useCallback(({handler.params}) => {{
    {handler.body}
  }}, [{handler.dependencies}]);
  """

  # Insert before return statement
  code = insert_before_return(code, callback_code)

  # Replace inline handler with callback reference
  code = regex_replace(code, pattern, f"{handler.prop}={{{handler.name}}}")

  RETURN code

FUNCTION wrap_with_useMemo(code, calculation):
  # Wrap expensive calculation in useMemo
  memo_code = f"""
  const {calculation.variable} = useMemo(() => {{
    {calculation.code}
  }}, [{calculation.dependencies}]);
  """

  # Replace inline calculation with memoized version
  code = code.replace(calculation.code, calculation.variable)
  code = insert_before_return(code, memo_code)

  RETURN code

FUNCTION add_lazy_loading(code):
  # Find component imports that should be lazy
  lazy_candidates = ["Modal", "Drawer", "Dialog", "Sheet"]

  FOR component IN lazy_candidates:
    IF component IN code:
      # Convert to lazy import
      import_line = find_import_line(code, component)
      IF import_line:
        lazy_import = f"const {component} = lazy(() => import('{component}'));"
        code = code.replace(import_line, lazy_import)

        # Add lazy import from React
        IF "lazy" NOT IN code:
          code = add_import(code, "react", ["lazy"])

        # Wrap usage in Suspense
        code = wrap_in_suspense(code, component)

  RETURN code

FUNCTION run_axe_core(code):
  # Simulate axe-core accessibility check
  issues = []

  # Check for missing alt text
  IF regex_match(r'<img(?![^>]*alt=)', code):
    issues.append({
      type: "missing-alt-text",
      severity: "critical",
      element: "img"
    })

  # Check for missing ARIA labels on buttons
  IF regex_match(r'<button[^>]*>\\s*<[^>]*/>\\s*</button>', code):
    # Icon-only button without aria-label
    IF NOT regex_match(r'aria-label=', code):
      issues.append({
        type: "missing-aria-label",
        severity: "critical",
        element: "button"
      })

  RETURN issues

FUNCTION fix_accessibility_issue(code, issue):
  IF issue.type == "missing-alt-text":
    # Add placeholder alt text
    code = regex_replace(code, r'<img ', '<img alt="TODO: Add description" ')

  IF issue.type == "missing-aria-label":
    # Infer label from context
    code = regex_replace(
      code,
      r'<button([^>]*)>',
      r'<button\1 aria-label="Action button">'
    )

  RETURN code
```

### 4. Build v0.dev Prompt

```text
FUNCTION build_v0_prompt(component, tokens):

  # Load few-shot examples if available (NEW v0.2.0)
  few_shot_examples = load_few_shot_examples(component.type)

  system_prompt = """
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
"""

  # Append few-shot examples if available (NEW v0.2.0)
  IF few_shot_examples:
    system_prompt += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 High-Quality Implementation Examples (Few-Shot Learning)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Study these examples carefully. They demonstrate:
- Proper token usage (prevents AP-VIS-001)
- Accessibility patterns (WCAG 2.1 AA)
- Touch targets (44×44px minimum)
- Focus indicators
- Error handling
- Loading states
- Anti-pattern prevention

{few_shot_examples}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Apply the patterns above to your implementation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

  user_prompt = build_component_prompt(component)

  RETURN {
    system: system_prompt,
    user: user_prompt
  }

FUNCTION build_component_prompt(component):

  prompt = f"""
Create a {component.name} component with the following specifications:

## Purpose
{component.purpose}

## States
"""

  FOR state IN component.states:
    prompt += f"- {state.name}: {state.description}\n"

  prompt += "\n## Variants\n"
  FOR variant IN component.variants:
    prompt += f"- {variant.name}: {variant.description}\n"

  prompt += "\n## Size Variants\n"
  FOR size IN component.sizes:
    prompt += f"- {size.name}: height={size.height}, padding={size.padding}, fontSize={size.font_size}\n"

  prompt += f"""
## Props Interface
```typescript
interface {component.name}Props {{
"""
  FOR prop IN component.props:
    optional = "?" IF prop.optional ELSE ""
    prompt += f"  {prop.name}{optional}: {prop.type}; // {prop.description}\n"
  prompt += "}\n```\n"

  prompt += f"""
## Accessibility Requirements
- Role: {component.a11y.role}
- Keyboard: {component.a11y.keyboard}
- ARIA: {component.a11y.aria}
- Focus: {component.a11y.focus}

Please generate a production-ready component that:
1. Uses shadcn/ui primitives where applicable
2. Implements all states and variants using CVA
3. Includes proper TypeScript types
4. Has accessible focus management
5. Supports the design tokens provided
"""

  RETURN prompt
```

### 4. Check Cache

```text
FUNCTION check_cache(component, tokens):

  cache_key = hash(component.spec + tokens)
  cache_path = f".speckit/cache/v0/{component.name}"

  IF exists(cache_path):
    metadata = read_json(f"{cache_path}/metadata.json")
    stored_hash = read(f"{cache_path}/spec.hash")

    # Validate cache
    IF stored_hash == cache_key:
      IF now() - metadata.generated_at < TTL_HOURS * 3600:
        LOG f"Cache hit for {component.name}"
        RETURN read(f"{cache_path}/code.tsx")

  RETURN null
```

### 5. Generate via v0.dev

```text
FUNCTION generate_via_v0(prompt, mode):

  IF mode == "api" AND v0_api_available:
    # API mode (future)
    response = http_post("https://api.v0.dev/generate", {
      headers: {
        "Authorization": f"Bearer {env.V0_API_KEY}",
        "Content-Type": "application/json"
      },
      body: {
        "prompt": prompt.user,
        "system": prompt.system,
        "framework": "react",
        "styling": "tailwind",
        "typescript": true
      }
    })

    # Poll for completion
    WHILE response.status == "processing":
      sleep(2000)
      response = http_get(f"https://api.v0.dev/generations/{response.id}")

    RETURN response.code

  ELSE:
    # Manual mode
    formatted_prompt = format_for_manual_entry(prompt)

    DISPLAY """
    ┌─────────────────────────────────────────────────────────────┐
    │ v0.dev Generation Required                                   │
    └─────────────────────────────────────────────────────────────┘

    Please copy the following prompt to v0.dev:

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {formatted_prompt}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Steps:
    1. Go to https://v0.dev
    2. Paste the prompt above
    3. Copy the generated code
    4. Paste the code below when prompted

    """

    code = wait_for_user_input("Paste v0.dev generated code:")
    RETURN code
```

### 6. Validate Generated Code

```text
FUNCTION validate_generated_code(code, spec):

  issues = []

  # 1. TypeScript Check
  ts_result = run_typescript_check(code)
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
  IF NOT has_aria_labels(code):
    issues.append({
      type: "accessibility",
      severity: "error",
      details: "Missing ARIA labels"
    })

  IF NOT has_keyboard_support(code):
    issues.append({
      type: "accessibility",
      severity: "warning",
      details: "May be missing keyboard support"
    })

  # 4. Component States
  implemented_states = extract_states_from_code(code)
  missing_states = spec.states - implemented_states
  IF missing_states:
    issues.append({
      type: "completeness",
      severity: "warning",
      details: f"Missing states: {missing_states}"
    })

  # 5. Props Interface Match
  IF NOT props_interface_matches(code, spec.props):
    issues.append({
      type: "interface",
      severity: "error",
      details: "Props interface doesn't match specification"
    })

  RETURN ValidationResult(
    passed = len([i for i in issues if i.severity == "error"]) == 0,
    issues = issues
  )


FUNCTION find_hardcoded_colors(code):
  # Patterns to detect
  patterns = [
    r'#[0-9a-fA-F]{3,8}',           # Hex colors
    r'rgb\([^)]+\)',                 # RGB
    r'rgba\([^)]+\)',                # RGBA
    r'hsl\([^)]+\)',                 # HSL
  ]

  # Exclude comments and strings in certain contexts
  found = []
  FOR pattern IN patterns:
    matches = regex_find_all(pattern, code)
    FOR match IN matches:
      IF NOT is_in_comment(match, code):
        found.append(match)

  RETURN found


FUNCTION has_aria_labels(code):
  # Check for common ARIA attributes
  aria_patterns = [
    r'aria-label',
    r'aria-labelledby',
    r'aria-describedby',
    r'role=',
  ]

  FOR pattern IN aria_patterns:
    IF regex_match(pattern, code):
      RETURN true

  RETURN false
```

### 7. Auto-Correct Issues

```text
FUNCTION auto_correct(code, issues):

  FOR issue IN issues:

    IF issue.type == "tokens" AND issue.severity == "warning":
      # Replace hardcoded colors with tokens
      FOR color IN issue.details:
        token = map_color_to_token(color)
        IF token:
          code = code.replace(color, token)

    IF issue.type == "accessibility" AND "ARIA" in issue.details:
      # Inject basic ARIA attributes
      code = inject_aria_attributes(code)

  RETURN code


FUNCTION map_color_to_token(hex_color):
  # Common mappings
  color_map = {
    "#000000": "var(--foreground)",
    "#ffffff": "var(--background)",
    "#f3f4f6": "var(--muted)",
    "#e5e7eb": "var(--border)",
    "#3b82f6": "var(--primary)",
    "#ef4444": "var(--destructive)",
  }

  # Fuzzy match for similar colors
  closest = find_closest_color(hex_color, color_map.keys())
  IF color_distance(hex_color, closest) < 10:
    RETURN color_map[closest]

  RETURN null
```

### 8. Cache Result

```text
FUNCTION cache_result(component, code, tokens):

  cache_key = hash(component.spec + tokens)
  cache_path = f".speckit/cache/v0/{component.name}"

  mkdir_p(cache_path)

  # Write code
  write(f"{cache_path}/code.tsx", code)

  # Write hash
  write(f"{cache_path}/spec.hash", cache_key)

  # Write metadata
  write_json(f"{cache_path}/metadata.json", {
    "generated_at": now(),
    "component": component.name,
    "version": component.version,
    "tokens_hash": hash(tokens)
  })

  LOG f"Cached {component.name} at {cache_path}"
```

### 9. Output Files

```text
FUNCTION output_component(component, code, output_dir):

  component_dir = f"{output_dir}/{kebab_case(component.name)}"
  mkdir_p(component_dir)

  # Main component file
  write(f"{component_dir}/{component.name}.tsx", code)

  # Generate types file if not inline
  types = extract_types(code)
  IF types:
    write(f"{component_dir}/{component.name}.types.ts", types)

  # Generate index export
  index_content = f"""
export {{ {component.name} }} from './{component.name}'
export type {{ {component.name}Props }} from './{component.name}'
"""
  write(f"{component_dir}/index.ts", index_content)

  # Generate basic story
  story = generate_storybook_story(component, code)
  write(f"{component_dir}/{component.name}.stories.tsx", story)

  RETURN {
    component: f"{component_dir}/{component.name}.tsx",
    types: f"{component_dir}/{component.name}.types.ts",
    index: f"{component_dir}/index.ts",
    story: f"{component_dir}/{component.name}.stories.tsx"
  }
```

## Complete Pipeline

```text
FUNCTION v0_generation_pipeline(component_name):

  # 1. Load context
  context = load_design_context()
  component = find_component(context.components, component_name)

  IF NOT component:
    ERROR f"Component '{component_name}' not found in design.md"

  # 2. Check cache first
  cached = check_cache(component, context.tokens)
  IF cached:
    RETURN cached

  # 3. Build prompt
  prompt = build_v0_prompt(component, context.tokens)

  # 4. Generate
  mode = get_v0_mode()  # "api" or "manual"
  code = generate_via_v0(prompt, mode)

  # 5. Validate
  validation = validate_generated_code(code, component)

  IF NOT validation.passed:
    LOG "Validation issues found, attempting auto-correction..."
    code = auto_correct(code, validation.issues)

    # Re-validate
    validation = validate_generated_code(code, component)
    IF NOT validation.passed:
      WARN "Some issues remain after auto-correction"
      DISPLAY validation.issues

  # 6. Cache
  cache_result(component, code, context.tokens)

  # 7. Output
  output_dir = ".preview/components"
  files = output_component(component, code, output_dir)

  RETURN {
    code: code,
    files: files,
    validation: validation
  }
```

## Error Handling

```text
ERROR_HANDLERS:

  v0_timeout:
    message: "v0.dev generation timed out"
    action: "Use fallback template generation"
    fallback: component-codegen skill

  invalid_code:
    message: "Generated code failed validation"
    action: "Prompt user to regenerate or use template"

  missing_spec:
    message: "Component not found in design.md"
    action: "List available components, ask user to specify"

  cache_corrupted:
    message: "Cache entry corrupted"
    action: "Clear cache and regenerate"
```

## Usage Example

```text
# In /speckit.preview or /speckit.design-generate

WHEN generating component "Button":

  1. Call v0_generation_pipeline("Button")

  2. Result:
     {
       code: "// Generated Button component...",
       files: {
         component: ".preview/components/button/Button.tsx",
         story: ".preview/components/button/Button.stories.tsx"
       },
       validation: {
         passed: true,
         issues: []
       }
     }

  3. Component ready for preview at:
     http://localhost:3456/components/button/
```

## Configuration

```yaml
# constitution.md
design_system:
  ai_generation:
    enabled: true
    provider: "v0.dev"
    mode: "manual"  # or "api" when available
    cache:
      enabled: true
      ttl_hours: 24
      storage: ".speckit/cache/v0"
    validation:
      typescript: true
      accessibility: true
      tokens: true
    fallback: "template"  # Use component-codegen if v0 fails
```
