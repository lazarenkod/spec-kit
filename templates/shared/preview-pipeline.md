# Preview Pipeline

Complete pipeline for generating interactive previews from design specifications.

## Pipeline Overview

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                         PREVIEW PIPELINE                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │
│  │   spec.md    │───►│  design.md   │───►│   Preview    │               │
│  │              │    │              │    │   Parser     │               │
│  └──────────────┘    └──────────────┘    └──────┬───────┘               │
│                                                  │                       │
│         ┌────────────────────────────────────────┼─────────────────┐    │
│         │                                        │                 │    │
│         ▼                                        ▼                 ▼    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐              │
│  │  Wireframe   │    │  Component   │    │  Animation   │              │
│  │  Generator   │    │  Generator   │    │  Generator   │              │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘              │
│         │                   │                   │                       │
│         ▼                   ▼                   ▼                       │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐              │
│  │    HTML/     │    │    React     │    │   CSS/       │              │
│  │    SVG       │    │    Vue/Svelte│    │   Framer     │              │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘              │
│         │                   │                   │                       │
│         └───────────────────┼───────────────────┘                       │
│                             │                                           │
│                             ▼                                           │
│                      ┌──────────────┐                                   │
│                      │   Preview    │                                   │
│                      │   Server     │                                   │
│                      │  :3456       │                                   │
│                      └──────┬───────┘                                   │
│                             │                                           │
│              ┌──────────────┼──────────────┐                           │
│              ▼              ▼              ▼                           │
│       ┌──────────┐   ┌──────────┐   ┌──────────┐                      │
│       │Screenshot│   │Storybook │   │  Vision  │                      │
│       │ Capture  │   │ Stories  │   │Validation│                      │
│       └──────────┘   └──────────┘   └──────────┘                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Pipeline Stages

### Stage 1: Design Parsing

```text
FUNCTION parse_design_artifacts():

  # Load design specification
  design_md = read("design.md")

  # Extract preview targets
  targets = {
    wireframes: extract_ascii_wireframes(design_md),
    components: extract_component_specs(design_md),
    animations: extract_animation_specs(design_md),
    flows: extract_user_flows(design_md)
  }

  # Load design tokens
  constitution = read("constitution.md")
  tokens = extract_design_tokens(constitution)

  RETURN PreviewContext(
    targets: targets,
    tokens: tokens,
    framework: constitution.design_system.framework
  )
```

### Stage 2: Wireframe Generation

```text
FUNCTION generate_wireframes(context):

  output_dir = ".preview/wireframes"
  mkdir_p(output_dir)

  FOR wireframe IN context.targets.wireframes:

    # Parse ASCII structure
    structure = parse_ascii_wireframe(wireframe.content)

    # Map to HTML elements
    html = ascii_to_html(structure, context.tokens)

    # Apply design tokens
    css = generate_wireframe_styles(context.tokens)

    # Output files
    write(f"{output_dir}/{wireframe.name}/index.html", html)
    write(f"{output_dir}/{wireframe.name}/styles.css", css)

    # Generate responsive variants
    FOR breakpoint IN ["mobile", "tablet", "desktop"]:
      responsive_html = apply_breakpoint(html, breakpoint)
      write(f"{output_dir}/{wireframe.name}/{breakpoint}.html", responsive_html)

    # Capture screenshots
    screenshots = capture_wireframe_screenshots(
      f"{output_dir}/{wireframe.name}",
      breakpoints: ["375px", "768px", "1280px"]
    )

    wireframe.output = {
      html: f"{output_dir}/{wireframe.name}/index.html",
      screenshots: screenshots
    }

  RETURN context.targets.wireframes
```

### Stage 3: Component Generation

```text
FUNCTION generate_components(context):

  output_dir = ".preview/components"
  mkdir_p(output_dir)

  FOR component IN context.targets.components:

    # Assess complexity
    complexity = assess_complexity(component)

    # Choose generation strategy
    IF complexity == "simple" OR complexity == "moderate":
      # Use template-based generation
      code = component_codegen_pipeline(component.name)
    ELSE:
      # Use v0.dev for complex components
      code = v0_generation_pipeline(component.name)

    # Output component files
    component_dir = f"{output_dir}/{kebab_case(component.name)}"
    write(f"{component_dir}/{component.name}.tsx", code)
    write(f"{component_dir}/index.ts", generate_exports(component.name))

    # Generate Storybook story
    story = generate_story(component, code)
    write(f"{component_dir}/{component.name}.stories.tsx", story)

    # Generate preview HTML
    preview = generate_component_preview(component, code, context.tokens)
    write(f"{component_dir}/preview.html", preview)

    component.output = {
      component: f"{component_dir}/{component.name}.tsx",
      story: f"{component_dir}/{component.name}.stories.tsx",
      preview: f"{component_dir}/preview.html"
    }

  RETURN context.targets.components
```

### Stage 4: Animation Generation

```text
FUNCTION generate_animations(context):

  output_dir = ".preview/animations"
  mkdir_p(output_dir)

  # Load animation presets
  presets = load_animation_presets()

  # Generate CSS keyframes
  css_keyframes = generate_css_keyframes(context.targets.animations, presets)
  write(f"{output_dir}/keyframes.css", css_keyframes)

  # Generate Framer Motion variants
  framer_variants = generate_framer_variants(context.targets.animations)
  write(f"{output_dir}/framer-variants.ts", framer_variants)

  # Generate Tailwind config extension
  tailwind_config = generate_tailwind_keyframes(context.targets.animations)
  write(f"{output_dir}/tailwind-keyframes.js", tailwind_config)

  # Generate animation preview page
  preview_html = generate_animation_showcase(context.targets.animations)
  write(f"{output_dir}/preview.html", preview_html)

  # Capture animation GIFs
  FOR animation IN context.targets.animations:
    gif = capture_animation_gif(
      f"{output_dir}/preview.html#{animation.name}",
      duration: animation.total_duration + 500
    )
    animation.gif = gif

  RETURN context.targets.animations
```

### Stage 5: Flow Preview Generation

```text
FUNCTION generate_flow_previews(context):

  output_dir = ".preview/flows"
  mkdir_p(output_dir)

  FOR flow IN context.targets.flows:

    flow_dir = f"{output_dir}/{kebab_case(flow.name)}"
    mkdir_p(flow_dir)

    # Generate screens
    screens = []
    FOR step IN flow.steps:
      screen_html = generate_flow_screen(step, context.tokens)
      screen_path = f"{flow_dir}/{step.id}.html"
      write(screen_path, screen_html)
      screens.append({
        id: step.id,
        path: screen_path,
        next: step.next_steps
      })

    # Generate flow navigation
    navigation = generate_flow_navigation(screens)
    write(f"{flow_dir}/navigation.js", navigation)

    # Generate flow index
    index = generate_flow_index(flow, screens)
    write(f"{flow_dir}/index.html", index)

    # Generate flow diagram
    diagram = generate_flow_diagram(flow)
    write(f"{flow_dir}/diagram.svg", diagram)

    flow.output = {
      index: f"{flow_dir}/index.html",
      diagram: f"{flow_dir}/diagram.svg",
      screens: screens
    }

  RETURN context.targets.flows
```

### Stage 6: Preview Server

```text
FUNCTION start_preview_server(port = 3456):

  server_config = {
    root: ".preview",
    port: port,
    routes: {
      "/": "index.html",
      "/wireframes/*": "wireframes/",
      "/components/*": "components/",
      "/animations": "animations/preview.html",
      "/flows/*": "flows/",
      "/api/screenshots": screenshot_api,
      "/api/validate": vision_api
    },
    middleware: [
      hot_reload(),
      cors(),
      static_files()
    ]
  }

  # Generate index page
  index = generate_preview_index()
  write(".preview/index.html", index)

  # Start server
  server = http_server(server_config)

  LOG f"Preview server started at http://localhost:{port}"
  LOG "  /wireframes   - Wireframe previews"
  LOG "  /components   - Component previews"
  LOG "  /animations   - Animation showcase"
  LOG "  /flows        - User flow previews"

  RETURN server


FUNCTION generate_preview_index():

  wireframes = glob(".preview/wireframes/*/index.html")
  components = glob(".preview/components/*/preview.html")
  animations = exists(".preview/animations/preview.html")
  flows = glob(".preview/flows/*/index.html")

  html = f"""
<!DOCTYPE html>
<html>
<head>
  <title>Design Preview | Spec-Kit</title>
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <header>
    <h1>Design Preview</h1>
    <nav>
      <a href="#wireframes">Wireframes</a>
      <a href="#components">Components</a>
      <a href="#animations">Animations</a>
      <a href="#flows">Flows</a>
    </nav>
  </header>

  <main>
    <section id="wireframes">
      <h2>Wireframes</h2>
      <div class="preview-grid">
        {generate_preview_cards(wireframes)}
      </div>
    </section>

    <section id="components">
      <h2>Components</h2>
      <div class="preview-grid">
        {generate_preview_cards(components)}
      </div>
    </section>

    <section id="animations">
      <h2>Animations</h2>
      <a href="/animations" class="preview-card">View Animation Showcase</a>
    </section>

    <section id="flows">
      <h2>User Flows</h2>
      <div class="preview-grid">
        {generate_preview_cards(flows)}
      </div>
    </section>
  </main>

  <script src="/preview.js"></script>
</body>
</html>
"""

  RETURN html
```

## Screenshot Capture

### Playwright Integration

```text
FUNCTION capture_screenshots(preview_path, options):

  browser = playwright.chromium.launch()

  screenshots = {}

  FOR viewport IN options.viewports:
    page = browser.new_page(viewport: viewport)
    page.goto(f"file://{preview_path}")

    # Wait for fonts and images
    page.wait_for_load_state("networkidle")

    # Wait for animations to complete
    IF options.wait_for_animations:
      page.wait_for_timeout(options.animation_delay OR 500)

    # Capture screenshot
    screenshot_path = f"{preview_path}.{viewport.name}.png"
    page.screenshot(
      path: screenshot_path,
      full_page: options.full_page OR false
    )

    screenshots[viewport.name] = screenshot_path

    page.close()

  browser.close()

  RETURN screenshots


FUNCTION capture_component_states(component_path, states):

  browser = playwright.chromium.launch()
  page = browser.new_page()
  page.goto(f"file://{component_path}")

  screenshots = {}

  FOR state IN states:

    # Apply state
    IF state == "hover":
      element = page.locator("[data-preview-target]")
      element.hover()
    ELIF state == "focus":
      element = page.locator("[data-preview-target]")
      element.focus()
    ELIF state == "active":
      element = page.locator("[data-preview-target]")
      element.dispatch_event("mousedown")
    ELIF state == "disabled":
      page.evaluate("document.querySelector('[data-preview-target]').disabled = true")

    # Wait for state transition
    page.wait_for_timeout(100)

    # Capture
    screenshot_path = f"{component_path}.{state}.png"
    page.screenshot(path: screenshot_path)

    screenshots[state] = screenshot_path

  browser.close()

  RETURN screenshots
```

### Animation GIF Capture

```text
FUNCTION capture_animation_gif(url, options):

  browser = playwright.chromium.launch()
  page = browser.new_page()
  page.goto(url)

  frames = []
  frame_duration = 1000 / options.fps  # Default 30 fps
  total_frames = (options.duration / frame_duration)

  FOR i IN range(total_frames):
    frame = page.screenshot(type: "png")
    frames.append(frame)
    page.wait_for_timeout(frame_duration)

  browser.close()

  # Combine frames into GIF
  gif_path = f"{url.path}.gif"
  create_gif(frames, gif_path, fps: options.fps)

  RETURN gif_path
```

## Storybook Generation

### Story Template

```text
FUNCTION generate_story(component, code):

  variants = extract_variants(component)
  states = extract_states(component)

  story = f"""
import type {{ Meta, StoryObj }} from '@storybook/react'
import {{ {component.name} }} from './{component.name}'

const meta: Meta<typeof {component.name}> = {{
  title: 'Components/{component.name}',
  component: {component.name},
  parameters: {{
    layout: 'centered',
    docs: {{
      description: {{
        component: '{component.purpose}'
      }}
    }}
  }},
  tags: ['autodocs'],
  argTypes: {{
    {generate_arg_types(component.props)}
  }}
}}

export default meta
type Story = StoryObj<typeof meta>

// Default story
export const Default: Story = {{
  args: {{
    {generate_default_args(component)}
  }}
}}

// Variant stories
{generate_variant_stories(component, variants)}

// State stories
{generate_state_stories(component, states)}

// Interactive story
export const Interactive: Story = {{
  args: {{
    {generate_default_args(component)}
  }},
  play: async ({{ canvasElement }}) => {{
    // Interaction testing
    {generate_interaction_tests(component)}
  }}
}}
"""

  RETURN story


FUNCTION generate_variant_stories(component, variants):

  stories = ""

  FOR variant IN variants:
    stories += f"""
export const {pascal_case(variant.name)}: Story = {{
  args: {{
    variant: '{variant.name}',
    children: '{component.name}'
  }}
}}
"""

  RETURN stories
```

### Storybook Config

```text
FUNCTION generate_storybook_config():

  main_config = """
import type { StorybookConfig } from '@storybook/react-vite'

const config: StorybookConfig = {
  stories: [
    '../.preview/components/**/*.stories.@(ts|tsx)'
  ],
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-a11y',
    '@storybook/addon-interactions'
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {}
  }
}

export default config
"""

  preview_config = """
import type { Preview } from '@storybook/react'
import '../.preview/styles.css'

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i
      }
    },
    viewport: {
      viewports: {
        mobile: { name: 'Mobile', styles: { width: '375px', height: '667px' } },
        tablet: { name: 'Tablet', styles: { width: '768px', height: '1024px' } },
        desktop: { name: 'Desktop', styles: { width: '1280px', height: '800px' } }
      }
    }
  }
}

export default preview
"""

  write(".storybook/main.ts", main_config)
  write(".storybook/preview.ts", preview_config)
```

## Vision Validation

```text
FUNCTION vision_validate_preview(screenshot_path, spec):

  prompt = f"""
Analyze this UI screenshot against the design specification.

Specification:
{spec}

Validate:
1. Layout matches wireframe structure
2. Visual hierarchy is correct
3. Spacing is consistent
4. Typography follows design tokens
5. Colors match design system
6. All elements are present
7. Accessibility indicators visible (focus rings, etc.)

Score each category 0-100 and provide overall assessment.

Return JSON:
{{
  "layout_score": number,
  "hierarchy_score": number,
  "spacing_score": number,
  "typography_score": number,
  "color_score": number,
  "completeness_score": number,
  "accessibility_score": number,
  "overall_score": number,
  "issues": [
    {{
      "category": string,
      "severity": "error" | "warning" | "info",
      "description": string,
      "suggestion": string
    }}
  ]
}}
"""

  result = claude_vision_analyze(screenshot_path, prompt)

  RETURN VisionValidationResult(result)
```

## Complete Pipeline Execution

```text
FUNCTION run_preview_pipeline():

  LOG "Starting preview pipeline..."

  # Stage 1: Parse
  LOG "Parsing design artifacts..."
  context = parse_design_artifacts()

  # Stage 2: Wireframes
  LOG f"Generating {len(context.targets.wireframes)} wireframes..."
  wireframes = generate_wireframes(context)

  # Stage 3: Components
  LOG f"Generating {len(context.targets.components)} components..."
  components = generate_components(context)

  # Stage 4: Animations
  LOG f"Generating animations..."
  animations = generate_animations(context)

  # Stage 5: Flows
  LOG f"Generating {len(context.targets.flows)} user flows..."
  flows = generate_flow_previews(context)

  # Stage 6: Start server
  LOG "Starting preview server..."
  server = start_preview_server()

  # Generate summary
  summary = {
    wireframes: len(wireframes),
    components: len(components),
    animations: len(animations),
    flows: len(flows),
    server_url: server.url,
    screenshots: collect_all_screenshots()
  }

  LOG f"""
  ┌─────────────────────────────────────────────────┐
  │ Preview Pipeline Complete                        │
  ├─────────────────────────────────────────────────┤
  │ Wireframes:  {summary.wireframes:4}                              │
  │ Components:  {summary.components:4}                              │
  │ Animations:  {summary.animations:4}                              │
  │ User Flows:  {summary.flows:4}                              │
  ├─────────────────────────────────────────────────┤
  │ Server: {summary.server_url}                     │
  └─────────────────────────────────────────────────┘
  """

  RETURN summary
```

## Output Structure

```text
.preview/
├── index.html              # Preview gallery home
├── styles.css              # Global preview styles
├── preview.js              # Hot reload + interactions
│
├── wireframes/
│   ├── dashboard/
│   │   ├── index.html      # Main wireframe
│   │   ├── styles.css      # Wireframe styles
│   │   ├── mobile.html     # Mobile variant
│   │   ├── tablet.html     # Tablet variant
│   │   ├── desktop.html    # Desktop variant
│   │   └── screenshots/
│   │       ├── mobile.png
│   │       ├── tablet.png
│   │       └── desktop.png
│   └── [screen-name]/
│
├── components/
│   ├── button/
│   │   ├── Button.tsx
│   │   ├── Button.stories.tsx
│   │   ├── index.ts
│   │   ├── preview.html
│   │   └── screenshots/
│   │       ├── default.png
│   │       ├── hover.png
│   │       ├── focus.png
│   │       └── disabled.png
│   └── [component-name]/
│
├── animations/
│   ├── keyframes.css       # CSS keyframes
│   ├── framer-variants.ts  # Framer Motion
│   ├── tailwind-keyframes.js
│   ├── preview.html        # Animation showcase
│   └── gifs/
│       ├── fade-in.gif
│       ├── slide-up.gif
│       └── [animation].gif
│
├── flows/
│   ├── onboarding/
│   │   ├── index.html      # Flow player
│   │   ├── diagram.svg     # Flow visualization
│   │   ├── navigation.js   # Step navigation
│   │   └── steps/
│   │       ├── welcome.html
│   │       ├── profile.html
│   │       └── complete.html
│   └── [flow-name]/
│
└── validation/
    ├── report.json         # Validation results
    ├── issues.md           # Human-readable issues
    └── scores.json         # DQS scores per artifact
```

## Configuration

```yaml
# constitution.md
design_system:
  preview:
    enabled: true
    port: 3456
    hot_reload: true

    screenshots:
      enabled: true
      viewports:
        - name: mobile
          width: 375
          height: 667
        - name: tablet
          width: 768
          height: 1024
        - name: desktop
          width: 1280
          height: 800
      format: png
      quality: 90

    storybook:
      enabled: true
      auto_generate: true
      addons:
        - essentials
        - a11y
        - interactions

    validation:
      enabled: true
      vision: true
      min_score: 80

    animations:
      capture_gifs: true
      fps: 30
      max_duration: 3000
```

## Error Handling

```text
ERROR_HANDLERS:

  parse_error:
    message: "Failed to parse design.md"
    action: "Check design.md format and required sections"

  generation_error:
    message: "Component generation failed"
    action: "Use fallback template or report issue"
    fallback: component-codegen skill

  screenshot_error:
    message: "Screenshot capture failed"
    action: "Check Playwright installation"
    command: "npx playwright install chromium"

  server_error:
    message: "Preview server failed to start"
    action: "Check port availability"
    alternatives: [3457, 3458, 3459]

  validation_error:
    message: "Vision validation failed"
    action: "Continue without validation"
    severity: "warning"
```

## CLI Usage

```bash
# Generate all previews
speckit preview

# Generate specific type
speckit preview --wireframes
speckit preview --components
speckit preview --animations

# Start server only (assumes previews exist)
speckit preview --serve

# Generate with screenshots
speckit preview --screenshots

# Generate with Storybook
speckit preview --storybook

# Validate with Claude Vision
speckit preview --validate

# Full pipeline with all options
speckit preview --all --validate --screenshots --storybook
```
