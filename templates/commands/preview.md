---
description: Generate interactive previews from design specifications. Converts wireframes to visual HTML, generates component previews, captures screenshots, and runs design quality validation.
persona: product-designer-agent
handoffs:
  - label: Implement Feature
    agent: speckit.implement
    prompt: Implement feature using generated preview components
    send: true
  - label: Update Design
    agent: speckit.design
    prompt: Refine design based on preview feedback
  - label: Generate More Components
    agent: speckit.design-generate
    prompt: Generate additional component variants
claude_code:
  model: opus
  reasoning_mode: extended
  thinking_budget: 16000
  cache_hierarchy: full
  orchestration:
    max_parallel: 3
    fail_fast: true
    wave_overlap:
      enabled: true
      overlap_threshold: 0.80
  subagents:
    # Wave 1: Preview Generation (parallel)
    - role: wireframe-converter
      role_group: FRONTEND
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Convert ASCII wireframes from design.md to visual HTML.
        Parse layout regions, map to HTML structure, apply design tokens.
        Generate responsive HTML files in .preview/wireframes/.
        Include CSS variables from design system.

    - role: component-previewer
      role_group: FRONTEND
      parallel: true
      depends_on: []
      priority: 10
      model_override: sonnet
      prompt: |
        Generate component previews from design.md specifications.
        For each component: extract states, variants, sizes, props.
        Use v0.dev for complex components, templates for simple ones.
        Create preview wrappers with all states in grid layout.
        Output to .preview/components/{name}/.

    # Wave 2: Capture & Validation (parallel, after generation)
    - role: screenshot-capturer
      role_group: TESTING
      parallel: true
      depends_on: [wireframe-converter, component-previewer]
      priority: 20
      model_override: haiku
      prompt: |
        Capture Playwright screenshots for all previews.
        Use viewports: mobile (375x812), tablet (768x1024), desktop (1440x900).
        Capture both light and dark themes if configured.
        For components, capture each state (hover, focus, disabled, etc.).
        Output to .preview/screenshots/.

    - role: design-quality-validator
      role_group: REVIEW
      parallel: true
      depends_on: [wireframe-converter]
      priority: 20
      model_override: sonnet
      prompt: |
        Calculate Design Quality Score (DQS) for generated previews.
        Check: contrast ratios, typography hierarchy, spacing consistency.
        Verify accessibility: ARIA labels, keyboard navigation, focus indicators.
        Validate token usage and component pattern adherence.
        Generate DQS report with grade and issues list.
skills:
  - name: wireframe-preview
    trigger: "When converting ASCII wireframes to visual HTML"
    usage: "Read templates/skills/wireframe-preview.md for conversion rules"
  - name: component-codegen
    trigger: "When generating React/Vue components from specs"
    usage: "Read templates/skills/component-codegen.md for generation templates"
  - name: v0-generation
    trigger: "When using v0.dev for component generation"
    usage: "Read templates/shared/v0-integration.md for API and prompts"
  - name: visual-regression
    trigger: "When capturing screenshots for baseline"
    usage: "Read templates/shared/visual-regression.md for Playwright setup"
preview_config:
  port: 3456
  output_dir: ".preview"
  screenshot_dir: ".preview/screenshots"
  auto_open: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

This command generates **interactive visual previews** from design specifications, enabling design validation without a human designer. It:

1. **Converts wireframes**: Transforms ASCII wireframes to visual HTML/React
2. **Generates components**: Creates production-ready components via v0.dev
3. **Captures screenshots**: Takes Playwright screenshots for all states/viewports
4. **Validates quality**: Runs Design Quality Score (DQS) checks
5. **Creates Storybook**: Auto-generates Storybook stories for components

**When to use**:
- After `/speckit.design` to visualize the design
- Before `/speckit.implement` to validate design decisions
- During design iteration to see changes
- For design review without Figma access

## Preview Types

| Type | Input | Output | Use Case |
|------|-------|--------|----------|
| Wireframe | ASCII wireframe in design.md | Visual HTML page | Quick layout validation |
| Component | Component spec in design.md | Interactive React component | State/variant testing |
| Flow | Screen flow in design.md | Multi-page navigation demo | User journey validation |
| Animation | Motion spec in design.md | Animated preview | Timing/easing review |
| Mockup | Stitch-generated mockups | Gallery with side-by-side comparison | High-fidelity visual validation |

## Outline

### 0. Load Configuration

```text
READ constitution.md:
  - design_system.preset → Load tokens
  - design_system.framework → Target framework
  - language → Artifact language

READ design.md:
  - Visual language → Color/typography tokens
  - Component specifications → Components to generate
  - Screen flows → Pages to preview
  - Motion specifications → Animations to include

DETERMINE preview_scope:
  IF user_input specifies component:
    scope = "component:{component_name}"
  ELIF user_input specifies screen:
    scope = "screen:{screen_name}"
  ELIF user_input specifies flow:
    scope = "flow:{flow_name}"
  ELSE:
    scope = "all"
```

### 1. Wireframe to Visual Conversion

```text
FOR EACH wireframe IN design.md:

  1. Parse ASCII wireframe structure:
     - Identify layout regions (header, sidebar, main, footer)
     - Extract component placeholders
     - Detect hierarchy (nesting levels)

  2. Map to HTML structure:
     ```
     +----------------------------------+    →    <header>
     |  [Header - Navigation context]   |    →      <nav>...</nav>
     +----------------------------------+    →    </header>
     |  [Sidebar]  |  [Main Content]    |    →    <div class="layout">
     |             |                    |    →      <aside>...</aside>
     +-------------+--------------------+    →      <main>...</main>
     ```

  3. Apply design tokens:
     - Background: var(--background)
     - Text: var(--foreground)
     - Spacing: var(--spacing-X)
     - Border radius: var(--radius-X)

  4. Generate HTML file:
     OUTPUT: .preview/wireframes/{screen_name}.html

  5. Include responsive meta + CSS variables
```

### 2. Component Preview Generation

```text
FOR EACH component IN design.md Component Specifications:

  1. Extract component definition:
     - States: default, hover, active, focus, disabled, loading, error
     - Variants: primary, secondary, ghost, etc.
     - Sizes: sm, md, lg
     - Props: documented properties

  2. Determine generation method:
     IF v0_api_available AND component.complexity == "high":
       method = "v0.dev"
       Read templates/shared/v0-integration.md
     ELSE:
       method = "template"
       Read templates/skills/component-codegen.md

  3. Generate component code:
     v0_prompt = build_v0_prompt(component, design_tokens)
     code = generate_component(method, v0_prompt)

  4. Create preview wrapper:
     - Import component
     - Render all states in grid
     - Render all variants
     - Add state toggle controls

  5. Output files:
     .preview/components/{component_name}/
     ├── {component_name}.tsx          # Component code
     ├── {component_name}.stories.tsx  # Storybook stories
     └── preview.html                  # Standalone preview
```

### 3. Flow Preview Generation

```text
FOR EACH flow IN design.md Screen Flows:

  1. Parse flow diagram (Mermaid):
     ```mermaid
     graph LR
       A[Welcome] --> B[Profile]
       B --> C[Preferences]
     ```

  2. Generate page for each node:
     - Use wireframe conversion for layout
     - Add navigation buttons for edges
     - Include transition animations

  3. Create flow runner:
     - Entry point: first node
     - Navigation: click to traverse edges
     - State persistence: maintain form data across screens

  4. Output:
     .preview/flows/{flow_name}/
     ├── index.html      # Flow entry
     ├── {screen_1}.html
     ├── {screen_2}.html
     └── flow.json       # Navigation config
```

### 4. Animation Preview

```text
FOR EACH animation IN design.md Motion Specifications:

  1. Parse animation spec:
     - Duration, easing, delay
     - Keyframes
     - Trigger (click, hover, load)

  2. Generate CSS keyframes:
     @keyframes {animation_name} { ... }

  3. Create demo element:
     - Element with animation applied
     - Play/pause control
     - Speed control (0.25x, 0.5x, 1x, 2x)
     - Frame-by-frame stepping

  4. Output:
     .preview/animations/{animation_name}.html
```

### 4.5. Stitch Mockup Gallery

```text
IF EXISTS(.preview/stitch-mockups/):

  1. Scan mockup directory:
     mockups = []
     FOR EACH feature_dir IN .preview/stitch-mockups/*/:
       FOR EACH screen_dir IN feature_dir/*/:
         mockup = {
           feature: feature_dir.name,
           screen: screen_dir.name,
           html: screen_dir/stitch-output.html,
           css: screen_dir/stitch-output.css,
           desktop: screen_dir/screenshot-desktop.png,
           mobile: screen_dir/screenshot-mobile.png,
           figma: screen_dir/figma-clipboard.json,
           prompt: screen_dir/prompt.txt
         }
         mockups.append(mockup)

  2. Generate mockup comparison pages:
     FOR EACH mockup IN mockups:

       # Find corresponding wireframe
       wireframe = find_wireframe(mockup.feature, mockup.screen)

       # Create side-by-side comparison page
       comparison_page = """
       <div class="mockup-comparison">
         <div class="comparison-header">
           <h2>{mockup.screen}</h2>
           <span class="feature-badge">{mockup.feature}</span>
         </div>

         <div class="comparison-grid">
           <div class="wireframe-panel">
             <h3>Wireframe</h3>
             <iframe src="{wireframe.html}"></iframe>
           </div>

           <div class="mockup-panel">
             <h3>Visual Mockup</h3>
             <iframe src="{mockup.html}"></iframe>
           </div>
         </div>

         <div class="mockup-assets">
           <a href="{mockup.desktop}" download>Desktop PNG</a>
           <a href="{mockup.mobile}" download>Mobile PNG</a>
           <button onclick="copyFigma('{mockup.figma}')">Copy to Figma</button>
           <a href="{mockup.html}" target="_blank">Open Full Screen</a>
         </div>

         <details class="prompt-details">
           <summary>Generation Prompt</summary>
           <pre>{read(mockup.prompt)}</pre>
         </details>
       </div>
       """

       OUTPUT: .preview/mockup-comparisons/{feature}/{screen}.html

  3. Generate mockup gallery index:
     gallery_index = """
     <h1>Visual Mockups Gallery</h1>

     <div class="gallery-stats">
       <span>Total Mockups: {mockups.length}</span>
       <span>Features: {unique_features.length}</span>
     </div>

     <div class="gallery-filters">
       <select id="feature-filter">
         <option value="all">All Features</option>
         {FOR feature IN unique_features: <option>{feature}</option>}
       </select>
       <button onclick="toggleView('grid')">Grid</button>
       <button onclick="toggleView('list')">List</button>
     </div>

     <div class="mockup-grid">
       {FOR mockup IN mockups:
         <div class="mockup-card" data-feature="{mockup.feature}">
           <img src="{mockup.desktop}" alt="{mockup.screen}">
           <div class="card-info">
             <h3>{mockup.screen}</h3>
             <span class="feature">{mockup.feature}</span>
           </div>
           <div class="card-actions">
             <a href="mockup-comparisons/{mockup.feature}/{mockup.screen}.html">
               Compare
             </a>
           </div>
         </div>
       }
     </div>
     """

     OUTPUT: .preview/stitch-mockups/gallery.html

  4. Include in main preview index:
     ADD link to .preview/stitch-mockups/gallery.html
     ADD mockup count to stats
```

### 5. Screenshot Capture

```text
FUNCTION capture_screenshots():

  viewports = [
    { name: "mobile", width: 375, height: 812 },
    { name: "tablet", width: 768, height: 1024 },
    { name: "desktop", width: 1440, height: 900 }
  ]

  themes = ["light", "dark"]  # If dark mode configured

  FOR EACH preview_file IN .preview/:
    FOR EACH viewport IN viewports:
      FOR EACH theme IN themes:

        1. Launch Playwright browser
        2. Set viewport size
        3. Set color scheme (prefers-color-scheme)
        4. Navigate to preview file
        5. Wait for animations to complete
        6. Capture screenshot

        OUTPUT: .preview/screenshots/{name}_{viewport}_{theme}.png

  FOR EACH component IN .preview/components/:
    FOR EACH state IN component.states:

      1. Navigate to component preview
      2. Trigger state (hover, focus, etc.)
      3. Capture screenshot

      OUTPUT: .preview/screenshots/{component}_{state}.png

  RETURN screenshot_manifest
```

### 6. Design Quality Score (DQS) Validation

```text
FUNCTION validate_dqs(previews, screenshots):

  score = 0
  issues = []

  # Visual Quality (40 points)
  FOR EACH screenshot IN screenshots:

    # Contrast check (via Claude Vision)
    contrast_result = vision_check(screenshot, "contrast_ratios")
    IF contrast_result.all_pass:
      score += 3
    ELSE:
      issues.append(f"Contrast issue: {contrast_result.failures}")

    # Typography hierarchy
    typography_result = vision_check(screenshot, "typography_hierarchy")
    score += typography_result.score  # 0-2

    # Spacing consistency
    spacing_result = vision_check(screenshot, "spacing_consistency")
    score += spacing_result.score  # 0-2

  # Accessibility (30 points)
  FOR EACH component IN components:

    # ARIA check
    IF component.has_aria_labels:
      score += 3
    ELSE:
      issues.append(f"{component.name}: Missing ARIA labels")

    # Keyboard check
    IF component.keyboard_navigable:
      score += 2

    # Focus indicator
    IF component.visible_focus:
      score += 2

  # Consistency (20 points)
  token_usage = check_css_for_tokens(previews)
  score += token_usage.score  # 0-10

  pattern_adherence = check_component_patterns(components)
  score += pattern_adherence.score  # 0-10

  # Implementation (10 points)
  typescript_check = lint_typescript(components)
  score += typescript_check.score  # 0-5

  code_quality = format_check(components)
  score += code_quality.score  # 0-5

  RETURN DQSResult(
    score=score,
    grade=calculate_grade(score),
    issues=issues,
    passed=score >= 80
  )
```

### 7. Storybook Generation

```text
IF storybook_enabled:

  FOR EACH component IN .preview/components/:

    story_template = """
    import type { Meta, StoryObj } from '@storybook/react'
    import { {ComponentName} } from './{component_name}'

    const meta: Meta<typeof {ComponentName}> = {
      title: 'Components/{ComponentName}',
      component: {ComponentName},
      parameters: {
        layout: 'centered',
      },
      tags: ['autodocs'],
    }

    export default meta
    type Story = StoryObj<typeof meta>

    export const Default: Story = {
      args: {
        {default_props}
      },
    }

    // Generate story for each variant
    {variant_stories}

    // Generate story for each state
    {state_stories}
    """

    OUTPUT: .preview/components/{component_name}/{component_name}.stories.tsx

  # Generate Storybook config if not exists
  IF NOT exists(.storybook/):
    generate_storybook_config()
```

### 8. Preview Server

```text
FUNCTION start_preview_server():

  1. Check if port 3456 available
     IF not available:
       port = find_available_port(3456, 3500)

  2. Start simple HTTP server:
     - Serve .preview/ directory
     - Enable hot reload for file changes
     - CORS enabled for local development

  3. Generate index page:
     .preview/index.html with:
     - Links to all wireframes
     - Links to all components
     - Links to all flows
     - Links to all animations
     - Links to Stitch mockups gallery (if exists)
     - DQS score badge
     - Screenshot gallery
     - Mockup comparison quick access (if mockups exist)

  4. Open browser (if auto_open enabled):
     open http://localhost:{port}

  RETURN server_url
```

## Validation Gates

Before completing, verify:

- [ ] All wireframes converted to HTML
- [ ] All components have preview files
- [ ] All component states captured in screenshots
- [ ] Screenshots taken for all viewports
- [ ] Stitch mockups gallery generated (if mockups exist)
- [ ] Mockup comparison pages created (if mockups exist)
- [ ] DQS score calculated
- [ ] Storybook stories generated (if enabled)
- [ ] Preview server accessible

## Output

After completion:

```text
## Preview Generated ✓

**Output Directory**: .preview/

### Files Generated

| Type | Count | Location |
|------|-------|----------|
| Wireframes | {N} | .preview/wireframes/ |
| Components | {N} | .preview/components/ |
| Flows | {N} | .preview/flows/ |
| Animations | {N} | .preview/animations/ |
| Mockups | {N} | .preview/stitch-mockups/ |
| Screenshots | {N} | .preview/screenshots/ |
| Stories | {N} | .preview/components/*/*.stories.tsx |

### Design Quality Score

| Category | Score | Max |
|----------|-------|-----|
| Visual Quality | {X} | 40 |
| Accessibility | {X} | 30 |
| Consistency | {X} | 20 |
| Implementation | {X} | 10 |
| **Total** | **{X}** | **100** |

**Grade**: {A/B/C/D/F}
**Status**: {Production Ready / Needs Work / Not Ready}

### Issues Found

{list of DQS issues if any}

### Preview Server

🌐 **URL**: http://localhost:{port}

- Wireframes: http://localhost:{port}/wireframes/
- Components: http://localhost:{port}/components/
- Flows: http://localhost:{port}/flows/
- Mockups: http://localhost:{port}/stitch-mockups/gallery.html
- Screenshots: http://localhost:{port}/screenshots/

### Recommended Next Steps

{IF score >= 80}
  - Run `/speckit.implement` to build the feature
  - Screenshots available as visual regression baseline
{ELSE}
  - Address DQS issues listed above
  - Run `/speckit.design` to refine design
  - Re-run `/speckit.preview` after fixes
{ENDIF}
```

## CLI Flags

```bash
# Preview specific component
speckit preview --component Button

# Preview specific screen
speckit preview --screen Dashboard

# Skip screenshot capture (faster)
speckit preview --no-screenshots

# Skip DQS validation
speckit preview --no-validation

# Generate Storybook only
speckit preview --storybook-only

# Specify output directory
speckit preview --output ./my-preview

# Specify port
speckit preview --port 4000

# Don't auto-open browser
speckit preview --no-open

# Dark mode only
speckit preview --theme dark

# Specific viewport only
speckit preview --viewport mobile

# Serve Stitch mockups gallery only
speckit preview --mockups

# Serve mockups with comparison view
speckit preview --mockups --compare

# Filter mockups by feature
speckit preview --mockups --feature onboarding
```

## Example

**User Input**: "Preview the onboarding wizard components"

**Process**:
1. Load design.md for onboarding feature
2. Find components: WizardStepper, OnboardingCard, StepIndicator
3. Generate each component via v0.dev
4. Create preview pages with all states
5. Capture screenshots (mobile, tablet, desktop × light, dark)
6. Calculate DQS score
7. Generate Storybook stories
8. Start preview server

**Output**:

```text
## Preview Generated ✓

### Files Generated

| Type | Count | Location |
|------|-------|----------|
| Wireframes | 5 | .preview/wireframes/ |
| Components | 3 | .preview/components/ |
| Screenshots | 36 | .preview/screenshots/ |
| Stories | 3 | .preview/components/*/*.stories.tsx |

### Design Quality Score

| Category | Score | Max |
|----------|-------|-----|
| Visual Quality | 38 | 40 |
| Accessibility | 28 | 30 |
| Consistency | 18 | 20 |
| Implementation | 9 | 10 |
| **Total** | **93** | **100** |

**Grade**: A
**Status**: Production Ready ✓

### Preview Server

🌐 **URL**: http://localhost:3456

Components:
- WizardStepper: http://localhost:3456/components/wizard-stepper/
- OnboardingCard: http://localhost:3456/components/onboarding-card/
- StepIndicator: http://localhost:3456/components/step-indicator/

### Recommended Next Steps

- Run `/speckit.implement` to build the feature
- Screenshots available as visual regression baseline at .preview/screenshots/
```

## Integration with Vision Validation

The DQS validation uses Claude Vision to analyze screenshots:

```text
VISION_CHECKS:

  contrast_ratios:
    prompt: |
      Analyze this UI screenshot for color contrast issues.
      Check text against backgrounds.
      Report any elements with contrast ratio < 4.5:1.
      Return: { pass: boolean, issues: string[] }

  typography_hierarchy:
    prompt: |
      Analyze the visual hierarchy of text in this screenshot.
      Check if headings are visually distinct from body text.
      Check if font sizes follow logical progression.
      Return: { score: 0-2, feedback: string }

  spacing_consistency:
    prompt: |
      Analyze spacing in this UI screenshot.
      Check if spacing follows a consistent system.
      Identify any irregular gaps or crowded areas.
      Return: { score: 0-2, feedback: string }

  touch_targets:
    prompt: |
      Analyze interactive elements in this mobile screenshot.
      Check if buttons/links appear to be at least 44x44px.
      Identify any elements that look too small to tap.
      Return: { pass: boolean, issues: string[] }
```

## Dependencies

For full functionality, the preview system requires:

```json
{
  "devDependencies": {
    "playwright": "^1.40.0",
    "@storybook/react": "^7.6.0",
    "vite": "^5.0.0"
  }
}
```

If dependencies are missing, the command will:
1. Warn about missing capabilities
2. Skip screenshot capture if Playwright missing
3. Skip Storybook if @storybook/react missing
4. Still generate HTML previews (no dependencies needed)
