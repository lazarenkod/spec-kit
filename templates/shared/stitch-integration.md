# Google Stitch Integration Module

> Browser automation module for generating high-fidelity visual mockups from wireframes using Google Stitch (stitch.withgoogle.com).

## Overview

Google Stitch is an AI-powered design tool from Google Labs that generates UI designs from text prompts using Gemini 2.5 Pro/Flash. Since Stitch has no public API, this module uses Playwright browser automation to:

1. Navigate to stitch.withgoogle.com
2. Authenticate via Google OAuth (persistent session)
3. Generate UI mockups from wireframe-derived prompts
4. Export results in multiple formats (HTML, PNG, Figma)

## Prerequisites

### Required Dependencies

```bash
# Check Playwright installation
npm ls playwright || npm install playwright

# Install browser if needed
npx playwright install chromium
```

### Directory Structure

```text
.speckit/stitch/
├── session/                    # Playwright persistent context (browser profile)
│   └── Default/                # Chromium profile data
├── usage.json                  # Rate limit tracking
└── prompts-cache/              # Saved prompts for retry/manual mode
    ├── {feature}/
    │   └── {screen-name}.txt

.preview/stitch-mockups/
├── {feature}/
│   ├── {screen-name}/
│   │   ├── stitch-output.html
│   │   ├── stitch-output.css
│   │   ├── screenshot-desktop.png
│   │   ├── screenshot-mobile.png
│   │   ├── figma-clipboard.json
│   │   └── prompt.txt
│   └── index.html              # Feature gallery
└── index.html                  # Master gallery
```

---

## Phase 0: Preflight Check

```text
FUNCTION stitch_preflight_check():

  1. CHECK Playwright installation:
     RUN: npm ls playwright --json
     IF not found:
       LOG "Installing Playwright..."
       RUN: npm install playwright
       IF fails: ERROR "Failed to install Playwright"

  2. CHECK browser availability:
     RUN: npx playwright install chromium --dry-run
     IF not installed:
       LOG "Installing Chromium browser..."
       RUN: npx playwright install chromium
       IF fails: ERROR "Failed to install Chromium"

  3. CHECK session directory:
     IF NOT EXISTS .speckit/stitch/session/:
       CREATE directory
       SET needs_auth = true
     ELSE:
       SET needs_auth = false

  4. CHECK rate limits:
     IF EXISTS .speckit/stitch/usage.json:
       LOAD usage data
       current_month = DATE.format("YYYY-MM")

       IF usage.month != current_month:
         RESET usage counters
         LOG "New month - rate limits reset"

       IF usage.standard.used >= 350:
         WARN "Standard mode rate limit reached (350/month)"
         SUGGEST "Use --manual mode or wait for next month"

       IF usage.standard.used >= 300:
         WARN "Approaching rate limit: {used}/350 generations this month"

  5. RETURN {
       playwright_ready: true,
       browser_ready: true,
       needs_auth: needs_auth,
       rate_limit_ok: usage.standard.used < 350
     }
```

---

## Phase 1: Authentication

### Persistent Browser Context

```text
FUNCTION stitch_create_browser_context():

  # Playwright persistent context preserves:
  # - Cookies (Google OAuth session)
  # - Local storage
  # - IndexedDB

  context = playwright.chromium.launchPersistentContext(
    userDataDir: ".speckit/stitch/session/",
    headless: false,  # Must be visible for OAuth
    viewport: { width: 1440, height: 900 },
    args: [
      "--disable-blink-features=AutomationControlled",
      "--no-first-run"
    ]
  )

  RETURN context
```

### Authentication Flow

```text
FUNCTION stitch_authenticate(context):

  page = context.pages[0] OR context.newPage()

  1. NAVIGATE to Stitch:
     await page.goto("https://stitch.withgoogle.com")
     await page.waitForLoadState("networkidle")

  2. CHECK if already authenticated:
     # Look for workspace indicators
     workspace_selector = '.workspace, [data-workspace], main[role="main"]'
     login_selector = 'button:has-text("Sign in"), [data-action="sign-in"]'

     IF await page.locator(workspace_selector).count() > 0:
       LOG "Already authenticated"
       RETURN { authenticated: true, page: page }

     IF await page.locator(login_selector).count() > 0:
       LOG "Authentication required"

       3. PROMPT user for manual sign-in:
          DISPLAY """
          ┌─────────────────────────────────────────────────────────────┐
          │  Google Stitch Authentication Required                       │
          ├─────────────────────────────────────────────────────────────┤
          │                                                             │
          │  A browser window has opened to stitch.withgoogle.com       │
          │                                                             │
          │  Please sign in with your Google account.                   │
          │  The session will be saved for future use.                  │
          │                                                             │
          │  Waiting for authentication...                              │
          └─────────────────────────────────────────────────────────────┘
          """

       4. WAIT for successful auth:
          await page.waitForSelector(workspace_selector, {
            timeout: 300000  # 5 minutes for user to complete OAuth
          })

          LOG "Authentication successful!"
          RETURN { authenticated: true, page: page }

  ERROR "Could not detect Stitch interface state"
```

### Re-authentication

```text
FUNCTION stitch_reauth(context):
  # Force re-authentication (--reauth flag)

  1. CLEAR session:
     DELETE .speckit/stitch/session/*

  2. CREATE fresh context:
     context = stitch_create_browser_context()

  3. RUN auth flow:
     RETURN stitch_authenticate(context)
```

---

## Phase 2: Wireframe Discovery

### Scan Design Artifacts

```text
FUNCTION stitch_discover_wireframes(scope):

  wireframes = []

  # Define scan paths based on scope
  IF scope == "feature":
    paths = [
      "specs/{current_feature}/design.md"
    ]
  ELIF scope == "app":
    paths = [
      "specs/app-design/foundations/*.md",
      "specs/app-design/waves/**/*-design.md",
      "specs/app-design/journeys/*.md"
    ]
  ELIF scope.screens:
    # Specific screens from --screens flag
    paths = resolve_screen_paths(scope.screens)

  FOR each path IN paths:
    FOR each file IN glob(path):
      content = READ file

      # Extract ASCII wireframe blocks
      wireframe_blocks = REGEX.findAll(
        content,
        /```(?:text|ascii)?\n([\s\S]*?┌[\s\S]*?┘[\s\S]*?)```/g
      )

      FOR each block IN wireframe_blocks:
        wireframe = {
          source_file: file,
          screen_name: extract_screen_name(file, block),
          ascii_content: block,
          components: extract_components(block),
          context: extract_surrounding_context(content, block)
        }
        wireframes.push(wireframe)

  RETURN wireframes
```

### Extract Screen Name

```text
FUNCTION extract_screen_name(file, block):

  # Try to find screen name from context
  # 1. Look for "### Screen: {name}" header before block
  # 2. Look for "## {name}" section header
  # 3. Derive from filename

  IF preceding_header MATCHES /###?\s+(?:Screen:?\s+)?(.+)/i:
    RETURN slugify(match[1])

  RETURN slugify(basename(file, ".md"))
```

### Extract Components

```text
FUNCTION extract_components(ascii_block):

  components = []

  # Common patterns in ASCII wireframes
  patterns = {
    button: /\[([^\]]+)\]/g,           # [Button Text]
    input: /\[_+\]|\[Input\]/gi,       # [____] or [Input]
    header: /^[│├┤].*Header/mi,
    sidebar: /Sidebar|Nav/i,
    card: /┌─+┐[\s\S]*?└─+┘/g,
    table: /\|.*\|.*\|/g,
    icon: /\([●○◆◇★☆]\)/g
  }

  FOR each pattern_name, regex IN patterns:
    matches = ascii_block.matchAll(regex)
    FOR each match IN matches:
      components.push({
        type: pattern_name,
        content: match[0],
        position: match.index
      })

  RETURN components
```

---

## Phase 3: Prompt Generation

### Load Design Context

```text
FUNCTION stitch_load_design_context():

  context = {}

  # Load design system tokens
  IF EXISTS specs/app-design/design-system.md:
    design_system = PARSE specs/app-design/design-system.md
    context.colors = design_system.colors
    context.typography = design_system.typography
    context.style = design_system.style_keywords

  ELIF EXISTS memory/constitution.md:
    constitution = PARSE memory/constitution.md
    context.colors = constitution.design_system.colors
    context.brand_name = constitution.project_name

  # Load persona context
  IF EXISTS specs/concept.md:
    concept = PARSE specs/concept.md
    context.personas = concept.personas
    context.primary_persona = concept.personas[0]

  RETURN context
```

### Generate Stitch Prompt

```text
FUNCTION stitch_generate_prompt(wireframe, design_context):

  # Load prompt template
  READ templates/shared/stitch-prompts.md

  # Analyze wireframe structure
  layout = analyze_layout(wireframe.ascii_content)
  components = wireframe.components

  # Build prompt from template
  prompt = TEMPLATE("""
    Create a {screen_type} screen for {app_name}.

    ## Layout
    {layout_description}

    ## Components
    {component_list}

    ## Style
    - Primary color: {primary_color}
    - Font: {font_family}
    - Theme: {theme}
    - Border radius: {border_radius}
    - Style: {style_keywords}

    ## Content
    {content_description}

    ## Additional Context
    {persona_context}

    Mood: {mood}
  """, {
    screen_type: detect_screen_type(wireframe),
    app_name: design_context.brand_name OR "Application",
    layout_description: layout.description,
    component_list: format_components(components),
    primary_color: design_context.colors?.primary OR "#3B82F6",
    font_family: design_context.typography?.font_family OR "Inter, system-ui",
    theme: design_context.theme OR "light",
    border_radius: design_context.border_radius OR "8px",
    style_keywords: design_context.style?.join(", ") OR "modern, clean",
    content_description: wireframe.context,
    persona_context: format_persona_context(design_context.primary_persona),
    mood: detect_mood(design_context.style)
  })

  # Save prompt for retry/manual mode
  WRITE prompt TO .speckit/stitch/prompts-cache/{feature}/{screen}.txt

  RETURN prompt
```

### Analyze Layout

```text
FUNCTION analyze_layout(ascii_content):

  layout = {
    has_header: /Header|Nav.*bar/i.test(ascii_content),
    has_sidebar: /Sidebar|Side.*nav/i.test(ascii_content),
    has_footer: /Footer|Action.*bar/i.test(ascii_content),
    columns: detect_columns(ascii_content),
    sections: detect_sections(ascii_content)
  }

  # Generate description
  parts = []

  IF layout.has_header:
    parts.push("Header/navigation bar at top")

  IF layout.has_sidebar:
    parts.push("Sidebar navigation on left")

  IF layout.columns > 1:
    parts.push("{columns}-column layout in main area".format(layout.columns))

  IF layout.has_footer:
    parts.push("Footer/action bar at bottom")

  layout.description = parts.join(", ") OR "Single column layout"

  RETURN layout
```

---

## Phase 4: Generation Pipeline

### DOM Selectors

```text
# Load selectors from versioned file
READ templates/shared/stitch-selectors.md

SELECTORS = {
  # Input
  promptInput: 'textarea[placeholder*="Describe"], .prompt-input, [data-testid="prompt-input"]',
  generateButton: 'button:has-text("Generate"), [data-action="generate"], button[type="submit"]',

  # Loading
  loadingSpinner: '[data-loading="true"], .loading-indicator, [aria-busy="true"]',
  loadingComplete: '.preview-container, [data-preview], canvas',

  # Canvas/Preview
  previewCanvas: '.preview-container, [data-preview], .design-canvas',
  previewFrame: 'iframe.preview-frame',

  # Export
  exportButton: 'button:has-text("Export"), [aria-label*="Export"], button:has-text("Code")',
  codeTab: '[data-tab="code"], button:has-text("Code")',
  htmlOption: 'button:has-text("HTML"), [data-format="html"]',
  tailwindOption: 'button:has-text("Tailwind"), [data-format="tailwind"]',
  copyButton: 'button:has-text("Copy"), [aria-label*="Copy"]',
  codeOutput: 'pre, code, .code-output, [data-code]',

  # Figma
  figmaButton: 'button:has-text("Figma"), [aria-label*="Figma"], button:has-text("Copy to Figma")',

  # Error
  errorMessage: '.error-message, [role="alert"], .toast-error'
}
```

### Generate Single Mockup

```text
FUNCTION stitch_generate_mockup(page, prompt, output_dir):

  TRY:
    1. ENSURE on Stitch page:
       current_url = page.url()
       IF NOT current_url.includes("stitch.withgoogle.com"):
         await page.goto("https://stitch.withgoogle.com")
         await page.waitForLoadState("networkidle")

    2. CLEAR previous prompt:
       input = await page.waitForSelector(SELECTORS.promptInput, { timeout: 10000 })
       await input.click({ clickCount: 3 })  # Select all
       await input.press("Backspace")

    3. TYPE new prompt:
       # Type with human-like delays to avoid detection
       await input.type(prompt, { delay: 50 })

    4. CLICK generate:
       generate_btn = await page.waitForSelector(SELECTORS.generateButton)
       await generate_btn.click()

    5. WAIT for generation:
       # Wait for loading to start
       await page.waitForSelector(SELECTORS.loadingSpinner, { timeout: 5000 })
         .catch(() => {})  # OK if we miss the spinner

       # Wait for loading to complete
       await page.waitForSelector(SELECTORS.loadingComplete, {
         timeout: 60000,
         state: "visible"
       })

       # Additional wait for render
       await page.waitForTimeout(2000)

    6. CHECK for errors:
       error = await page.$(SELECTORS.errorMessage)
       IF error:
         error_text = await error.textContent()
         THROW Error("Generation failed: " + error_text)

    7. UPDATE usage tracking:
       usage = LOAD .speckit/stitch/usage.json
       usage.standard.used += 1
       usage.last_generation = new Date().toISOString()
       SAVE usage TO .speckit/stitch/usage.json

    8. RETURN success:
       RETURN { success: true, page: page }

  CATCH error:
    LOG error.message
    RETURN { success: false, error: error.message }
```

---

## Phase 5: Export Pipeline

### Export HTML/CSS

```text
FUNCTION stitch_export_html(page, output_dir):

  TRY:
    1. OPEN export panel:
       export_btn = await page.waitForSelector(SELECTORS.exportButton, { timeout: 5000 })
       await export_btn.click()
       await page.waitForTimeout(500)

    2. SELECT HTML format:
       # Try Tailwind first (preferred), fallback to plain HTML
       tailwind_option = await page.$(SELECTORS.tailwindOption)
       IF tailwind_option:
         await tailwind_option.click()
       ELSE:
         html_option = await page.$(SELECTORS.htmlOption)
         IF html_option:
           await html_option.click()

       await page.waitForTimeout(500)

    3. COPY code:
       copy_btn = await page.waitForSelector(SELECTORS.copyButton)
       await copy_btn.click()

       # Get code from clipboard or code output element
       code = await page.evaluate(() => navigator.clipboard.readText())
         .catch(async () => {
           # Fallback: read from code output element
           code_el = await page.$(SELECTORS.codeOutput)
           RETURN code_el ? await code_el.textContent() : null
         })

       IF NOT code:
         THROW Error("Could not extract code")

    4. PARSE and save:
       # Separate HTML and CSS if combined
       IF code.includes("<style>"):
         html_match = code.match(/<style>([\s\S]*?)<\/style>/)
         css = html_match ? html_match[1] : ""
         html = code.replace(/<style>[\s\S]*?<\/style>/, "")
       ELSE:
         html = code
         css = ""

       WRITE html TO {output_dir}/stitch-output.html
       IF css:
         WRITE css TO {output_dir}/stitch-output.css

    5. CLOSE export panel:
       await page.keyboard.press("Escape")

    RETURN { success: true, files: ["stitch-output.html", "stitch-output.css"] }

  CATCH error:
    LOG "HTML export failed: " + error.message
    RETURN { success: false, error: error.message }
```

### Export Screenshots

```text
FUNCTION stitch_export_screenshots(page, output_dir):

  TRY:
    1. FIND preview element:
       preview = await page.waitForSelector(SELECTORS.previewCanvas)

       # If preview is in iframe, switch context
       preview_frame = await page.$(SELECTORS.previewFrame)
       IF preview_frame:
         frame = await preview_frame.contentFrame()
         preview = await frame.$("body")

    2. CAPTURE desktop screenshot (1440px):
       await page.setViewportSize({ width: 1440, height: 900 })
       await page.waitForTimeout(500)

       await preview.screenshot({
         path: "{output_dir}/screenshot-desktop.png",
         type: "png"
       })
       LOG "Saved desktop screenshot"

    3. CAPTURE mobile screenshot (375px):
       await page.setViewportSize({ width: 375, height: 812 })
       await page.waitForTimeout(500)

       await preview.screenshot({
         path: "{output_dir}/screenshot-mobile.png",
         type: "png"
       })
       LOG "Saved mobile screenshot"

    4. RESTORE viewport:
       await page.setViewportSize({ width: 1440, height: 900 })

    RETURN { success: true, files: ["screenshot-desktop.png", "screenshot-mobile.png"] }

  CATCH error:
    LOG "Screenshot export failed: " + error.message
    RETURN { success: false, error: error.message }
```

### Export to Figma

```text
FUNCTION stitch_export_figma(page, output_dir):

  TRY:
    1. FIND Figma export button:
       figma_btn = await page.$(SELECTORS.figmaButton)

       IF NOT figma_btn:
         LOG "Figma export not available for this design"
         RETURN { success: false, error: "Figma export not available" }

    2. CLICK Figma export:
       await figma_btn.click()
       await page.waitForTimeout(1000)

    3. CAPTURE clipboard data:
       # Figma uses clipboard for transfer
       clipboard_data = await page.evaluate(() => {
         return navigator.clipboard.read()
           .then(items => items[0]?.getType("text/html"))
           .then(blob => blob?.text())
       })

       IF clipboard_data:
         WRITE clipboard_data TO {output_dir}/figma-clipboard.json

         LOG """
         Figma export ready!
         To import: Open Figma → Cmd/Ctrl+V to paste
         Clipboard data saved to: {output_dir}/figma-clipboard.json
         """

    RETURN { success: true, files: ["figma-clipboard.json"] }

  CATCH error:
    LOG "Figma export failed: " + error.message
    RETURN { success: false, error: error.message }
```

---

## Phase 6: Gallery Generation

### Generate Feature Gallery

```text
FUNCTION stitch_generate_feature_gallery(feature_name, screens):

  html = TEMPLATE("""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{feature_name} - Stitch Mockups</title>
      <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: Inter, system-ui, sans-serif; background: #f5f5f5; }
        .header { padding: 2rem; background: white; border-bottom: 1px solid #e5e5e5; }
        .header h1 { font-size: 1.5rem; font-weight: 600; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 2rem; padding: 2rem; }
        .card { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .card img { width: 100%; aspect-ratio: 16/10; object-fit: cover; }
        .card-body { padding: 1rem; }
        .card-title { font-weight: 600; margin-bottom: 0.5rem; }
        .card-actions { display: flex; gap: 0.5rem; margin-top: 1rem; }
        .btn { padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.875rem; cursor: pointer; border: none; }
        .btn-primary { background: #3b82f6; color: white; }
        .btn-secondary { background: #f3f4f6; color: #374151; }
        .badge { display: inline-block; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; background: #dcfce7; color: #166534; }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>{feature_name}</h1>
        <p>Generated {count} mockups via Google Stitch</p>
      </div>
      <div class="grid">
        {screen_cards}
      </div>
    </body>
    </html>
  """, {
    feature_name: feature_name,
    count: screens.length,
    screen_cards: screens.map(screen => TEMPLATE("""
      <div class="card">
        <img src="{screen_name}/screenshot-desktop.png" alt="{screen_name}">
        <div class="card-body">
          <div class="card-title">{screen_name}</div>
          <span class="badge">Generated</span>
          <div class="card-actions">
            <a href="{screen_name}/stitch-output.html" class="btn btn-primary">View HTML</a>
            <a href="{screen_name}/screenshot-mobile.png" class="btn btn-secondary">Mobile</a>
            <a href="{screen_name}/prompt.txt" class="btn btn-secondary">Prompt</a>
          </div>
        </div>
      </div>
    """, screen)).join("")
  })

  WRITE html TO .preview/stitch-mockups/{feature_name}/index.html
```

### Generate Master Gallery

```text
FUNCTION stitch_generate_master_gallery(features):

  stats = {
    total: 0,
    generated: 0,
    failed: 0
  }

  FOR each feature IN features:
    stats.total += feature.screens.length
    stats.generated += feature.screens.filter(s => s.success).length
    stats.failed += feature.screens.filter(s => !s.success).length

  html = TEMPLATE("""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Stitch Mockups Gallery</title>
      <style>
        /* ... similar styles ... */
        .stats { display: flex; gap: 2rem; margin-top: 1rem; }
        .stat { text-align: center; }
        .stat-value { font-size: 2rem; font-weight: 700; }
        .stat-label { font-size: 0.875rem; color: #6b7280; }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>Stitch Mockups Gallery</h1>
        <div class="stats">
          <div class="stat">
            <div class="stat-value">{total}</div>
            <div class="stat-label">Total Screens</div>
          </div>
          <div class="stat">
            <div class="stat-value" style="color: #16a34a">{generated}</div>
            <div class="stat-label">Generated</div>
          </div>
          <div class="stat">
            <div class="stat-value" style="color: #dc2626">{failed}</div>
            <div class="stat-label">Failed</div>
          </div>
        </div>
      </div>
      <div class="features">
        {feature_list}
      </div>
    </body>
    </html>
  """, {
    total: stats.total,
    generated: stats.generated,
    failed: stats.failed,
    feature_list: features.map(f => """
      <a href="{f.name}/index.html" class="feature-card">
        <h2>{f.name}</h2>
        <p>{f.screens.length} screens</p>
      </a>
    """).join("")
  })

  WRITE html TO .preview/stitch-mockups/index.html
```

---

## Phase 7: Error Handling

### Error Recovery Strategy

```text
ERRORS = {
  SESSION_EXPIRED: {
    detection: "redirect to accounts.google.com",
    recovery: stitch_reauth,
    retry: true
  },
  RATE_LIMIT: {
    detection: "429, quota exceeded, rate limit",
    recovery: stitch_fallback_manual,
    retry: false
  },
  CAPTCHA: {
    detection: "recaptcha, captcha, verify you're human",
    recovery: stitch_pause_for_user,
    retry: true
  },
  GENERATION_TIMEOUT: {
    detection: "timeout after 60s",
    recovery: stitch_retry_once,
    retry: true,
    max_retries: 1
  },
  EXPORT_FAILED: {
    detection: "clipboard empty, no code output",
    recovery: stitch_screenshot_fallback,
    retry: false
  },
  NETWORK_ERROR: {
    detection: "net::ERR_, network error",
    recovery: stitch_retry_with_backoff,
    retry: true,
    max_retries: 3
  }
}

FUNCTION stitch_handle_error(error, context):

  FOR each error_type, handler IN ERRORS:
    IF error.message.match(handler.detection):

      LOG "Detected error: {error_type}"

      IF handler.retry AND context.retries < (handler.max_retries OR 1):
        context.retries += 1
        LOG "Attempting recovery: {handler.recovery.name}"
        RETURN handler.recovery(context)

      ELSE:
        LOG "Max retries reached or non-recoverable error"
        RETURN { success: false, error: error_type, fallback: true }

  # Unknown error
  LOG "Unknown error: {error.message}"
  RETURN { success: false, error: "UNKNOWN", message: error.message }
```

### Fallback to Manual Mode

```text
FUNCTION stitch_fallback_manual(pending_wireframes):

  # Save all pending prompts
  FOR each wireframe IN pending_wireframes:
    prompt = stitch_generate_prompt(wireframe)
    path = ".speckit/stitch/prompts-cache/{feature}/{screen}.txt"
    WRITE prompt TO path

  # Generate manual guide
  guide = TEMPLATE("""
    # Manual Mockup Generation Guide

    Automation encountered issues. Please generate mockups manually.

    ## Steps

    1. Open https://stitch.withgoogle.com
    2. Sign in with your Google account
    3. For each screen below, copy the prompt and generate

    ## Pending Screens

    {screen_list}

    ## After Generation

    Export each result:
    1. Click "Export" → "Tailwind" or "HTML"
    2. Save to: `.preview/stitch-mockups/{feature}/{screen}/stitch-output.html`
    3. Take screenshots at 1440px and 375px width
    4. (Optional) Click "Copy to Figma" for Figma import

    ## Re-run Automation

    After resolving issues, re-run:
    ```bash
    /speckit.design --mockup
    ```
  """, {
    screen_list: pending_wireframes.map(w => """
      ### {w.screen_name}

      **Prompt file**: `.speckit/stitch/prompts-cache/{w.feature}/{w.screen_name}.txt`

      **Output to**: `.preview/stitch-mockups/{w.feature}/{w.screen_name}/`

      - [ ] Generated
      - [ ] HTML exported
      - [ ] Screenshots captured
    """).join("\n")
  })

  WRITE guide TO .speckit/stitch/manual-generation-guide.md
  LOG "Manual generation guide saved to .speckit/stitch/manual-generation-guide.md"

  # Open in editor
  EXEC: code .speckit/stitch/manual-generation-guide.md
    OR open .speckit/stitch/manual-generation-guide.md
```

---

## Phase 8: Quality Report

### Generate Report

```text
FUNCTION stitch_generate_report(results):

  report = {
    total: results.length,
    generated: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length,
    exports: {
      html: results.filter(r => r.exports?.html).length,
      screenshots: results.filter(r => r.exports?.screenshots).length,
      figma: results.filter(r => r.exports?.figma).length
    },
    usage: LOAD .speckit/stitch/usage.json
  }

  markdown = TEMPLATE("""
    # Mockup Generation Report

    **Generated**: {timestamp}
    **Tool**: Google Stitch (via browser automation)

    ## Summary

    | Metric | Value |
    |--------|-------|
    | Total Screens | {total} |
    | Generated | {generated} |
    | Failed | {failed} |
    | Success Rate | {success_rate}% |

    ## Export Status

    | Format | Count |
    |--------|-------|
    | HTML/CSS | {html} |
    | Screenshots | {screenshots} |
    | Figma | {figma} |

    ## Rate Limit Status

    - Standard mode: {used}/{limit} ({remaining} remaining)
    - Month: {month}

    ## Screen Details

    | Screen | Status | HTML | Desktop | Mobile | Figma |
    |--------|--------|------|---------|--------|-------|
    {screen_rows}

    ## Failed Screens

    {failed_details}

    ## Next Steps

    {next_steps}
  """, {
    timestamp: new Date().toISOString(),
    total: report.total,
    generated: report.generated,
    failed: report.failed,
    success_rate: Math.round(report.generated / report.total * 100),
    html: report.exports.html,
    screenshots: report.exports.screenshots,
    figma: report.exports.figma,
    used: report.usage.standard.used,
    limit: 350,
    remaining: 350 - report.usage.standard.used,
    month: report.usage.month,
    screen_rows: results.map(r => """
      | {r.screen_name} | {r.success ? '✅' : '❌'} | {r.exports?.html ? '✅' : '❌'} | {r.exports?.desktop ? '✅' : '❌'} | {r.exports?.mobile ? '✅' : '❌'} | {r.exports?.figma ? '✅' : '❌'} |
    """).join("\n"),
    failed_details: results.filter(r => !r.success).map(r => """
      - **{r.screen_name}**: {r.error}
    """).join("\n") OR "None",
    next_steps: report.failed > 0
      ? "- Retry failed screens: `/speckit.design --mockup --retry`\n- Or use manual mode: See `.speckit/stitch/manual-generation-guide.md`"
      : "- Preview mockups: Open `.preview/stitch-mockups/index.html`\n- Continue to planning: `/speckit.plan`"
  })

  WRITE markdown TO .preview/stitch-mockups/mockup-report.md
  LOG "Report saved to .preview/stitch-mockups/mockup-report.md"

  RETURN report
```

---

## Main Orchestration

```text
FUNCTION stitch_main(options):

  LOG "Starting Google Stitch mockup generation..."

  # Phase 0: Preflight
  preflight = stitch_preflight_check()
  IF NOT preflight.playwright_ready OR NOT preflight.browser_ready:
    ERROR "Preflight check failed"
    RETURN

  IF NOT preflight.rate_limit_ok:
    IF options.force:
      WARN "Proceeding despite rate limit (--force)"
    ELSE:
      LOG "Rate limit reached. Use --manual mode."
      stitch_fallback_manual([])
      RETURN

  # Phase 1: Authentication
  context = stitch_create_browser_context()
  auth_result = stitch_authenticate(context)
  IF NOT auth_result.authenticated:
    ERROR "Authentication failed"
    RETURN

  page = auth_result.page

  # Phase 2: Discover wireframes
  scope = options.all ? "app" : "feature"
  IF options.screens:
    scope = { screens: options.screens.split(",") }

  wireframes = stitch_discover_wireframes(scope)
  LOG "Found {wireframes.length} wireframes to process"

  IF wireframes.length == 0:
    WARN "No wireframes found. Run /speckit.design first."
    RETURN

  # Phase 3: Load design context
  design_context = stitch_load_design_context()

  # Phase 4-5: Generate and export each
  results = []

  FOR each wireframe IN wireframes:
    LOG "Processing: {wireframe.screen_name}"

    # Create output directory
    output_dir = ".preview/stitch-mockups/{wireframe.feature}/{wireframe.screen_name}"
    MKDIR output_dir

    # Generate prompt
    prompt = stitch_generate_prompt(wireframe, design_context)
    WRITE prompt TO {output_dir}/prompt.txt

    # Generate mockup
    gen_result = stitch_generate_mockup(page, prompt, output_dir)

    IF gen_result.success:
      # Export all formats
      html_result = stitch_export_html(page, output_dir)
      screenshot_result = stitch_export_screenshots(page, output_dir)
      figma_result = stitch_export_figma(page, output_dir)

      results.push({
        screen_name: wireframe.screen_name,
        feature: wireframe.feature,
        success: true,
        exports: {
          html: html_result.success,
          desktop: screenshot_result.success,
          mobile: screenshot_result.success,
          figma: figma_result.success
        }
      })
    ELSE:
      results.push({
        screen_name: wireframe.screen_name,
        feature: wireframe.feature,
        success: false,
        error: gen_result.error
      })

  # Phase 6: Generate galleries
  features = group_by_feature(results)
  FOR each feature IN features:
    stitch_generate_feature_gallery(feature.name, feature.screens)
  stitch_generate_master_gallery(features)

  # Phase 8: Generate report
  report = stitch_generate_report(results)

  # Close browser
  await context.close()

  # Output summary
  LOG """
  ┌─────────────────────────────────────────────────────────────────────┐
  │  STITCH MOCKUP GENERATION COMPLETE                                  │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │  Generated: {report.generated}/{report.total} mockups               │
  │  Success rate: {report.success_rate}%                               │
  │                                                                     │
  │  Exports:                                                           │
  │    HTML/CSS: {report.exports.html}                                  │
  │    Screenshots: {report.exports.screenshots}                        │
  │    Figma: {report.exports.figma}                                    │
  │                                                                     │
  │  Rate limit: {report.usage.standard.used}/350 this month            │
  │                                                                     │
  │  Output: .preview/stitch-mockups/                                   │
  │  Report: .preview/stitch-mockups/mockup-report.md                   │
  │                                                                     │
  │  Next: Open index.html to preview all mockups                       │
  └─────────────────────────────────────────────────────────────────────┘
  """

  RETURN report
```
